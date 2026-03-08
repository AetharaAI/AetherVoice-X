from __future__ import annotations

import asyncio
import json
from contextlib import suppress

import httpx
import websockets
from websockets.exceptions import InvalidStatus

from .base import BaseASRAdapter
from ..logging import logger
from ..schemas.requests import ASRFileRequest, ASRStreamStartRequest, AudioFrame
from ..schemas.responses import ASRResult, ASRSegment, StreamSession, TimingBreakdown
from ..utils.audio_io import decode_payload_b64, estimate_wav_duration_ms, pcm16_to_wav_bytes
from ..utils.time import elapsed_ms


def _coerce_ms(value: object) -> int:
    if value is None:
        return 0
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0
    if numeric > 1000:
        return int(numeric)
    return int(numeric * 1000)


def _derive_ws_url(base_url: str | None, ws_url: str | None) -> str:
    if ws_url:
        return ws_url.rstrip("/")
    if not base_url:
        return ""
    return base_url.rstrip("/").replace("https://", "wss://").replace("http://", "ws://")


class VoxtralRealtimeAdapter(BaseASRAdapter):
    name = "voxtral_realtime"
    supports_streaming = True
    supports_batch = True
    supports_timestamps = True
    supports_language_detection = True

    def __init__(
        self,
        *,
        base_url: str | None,
        ws_url: str | None,
        model_name: str,
        api_key: str | None = None,
        partial_window_ms: int = 480,
        timeout_seconds: float = 90.0,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.ws_url = _derive_ws_url(self.base_url, ws_url)
        self.model_name = model_name
        self.api_key = api_key.strip() if api_key and api_key.strip() else None
        self.partial_window_ms = partial_window_ms
        self.ready = bool(self.base_url or self.ws_url)
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout_seconds) if self.base_url else None
        self._sessions: dict[str, dict] = {}
        logger.info(
            "voxtral_adapter_initialized",
            extra={
                "voxtral_ready": self.ready,
                "voxtral_base_url": self.base_url or "unset",
                "voxtral_ws_url": self.ws_url or "unset",
                "voxtral_model_name": self.model_name,
                "voxtral_partial_window_ms": self.partial_window_ms,
                "voxtral_api_key_configured": bool(self.api_key),
            },
        )

    def _http_headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {"Authorization": f"Bearer {self.api_key}"}

    def _realtime_headers(self) -> tuple[dict[str, str], bool]:
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}, False
        # Temporary dev/local fallback for internal docker traffic when the
        # sidecar is started with --api-key EMPTY and no explicit key is wired.
        return {"Authorization": "Bearer EMPTY"}, True

    async def _transcribe_wav_bytes(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        if not self.base_url or self._client is None:
            raise RuntimeError("Voxtral realtime upstream is not configured")
        started = __import__("time").perf_counter()
        logger.info(
            "voxtral_upstream_request_started",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "model_used": self.name,
                "voxtral_base_url": self.base_url,
                "voxtral_model_name": self.model_name,
                "audio_bytes": len(audio_bytes),
                "task": request.task,
            },
        )
        fields: list[tuple[str, str]] = [
            ("model", self.model_name),
            ("response_format", "verbose_json" if request.timestamps else "json"),
        ]
        if request.language and request.language != "auto":
            fields.append(("language", request.language))
        if request.task and request.task != "transcribe":
            fields.append(("task", request.task))
        if request.timestamps:
            fields.append(("timestamp_granularities[]", "segment"))
        files = {"file": (f"{request.request_id}.wav", audio_bytes, "audio/wav")}
        response = await self._client.post("/v1/audio/transcriptions", data=fields, files=files, headers=self._http_headers())
        if response.is_error:
            detail = response.text
            logger.error(
                "voxtral_upstream_failed",
                extra={
                    "request_id": request.request_id,
                    "session_id": request.session_id,
                    "status_code": response.status_code,
                    "detail": detail,
                },
            )
            raise RuntimeError(f"Voxtral upstream transcription failed ({response.status_code}): {detail}")
        payload = response.json()
        timings = TimingBreakdown(inference_ms=elapsed_ms(started), total_ms=elapsed_ms(started))
        segments_payload = payload.get("segments") or payload.get("chunks") or []
        segments = [
            ASRSegment(
                segment_id=str(segment.get("id", index)),
                start_ms=_coerce_ms(segment.get("start")),
                end_ms=_coerce_ms(segment.get("end")),
                text=str(segment.get("text", "")).strip(),
                confidence=segment.get("avg_logprob") or segment.get("confidence"),
            )
            for index, segment in enumerate(segments_payload, start=1)
            if str(segment.get("text", "")).strip()
        ]
        text = str(payload.get("text", "")).strip()
        if not text and segments:
            text = " ".join(segment.text for segment in segments).strip()
        duration_ms = segments[-1].end_ms if segments else estimate_wav_duration_ms(audio_bytes)
        language_detected = payload.get("language")
        if language_detected in {"", "auto"}:
            language_detected = None
        logger.info(
            "voxtral_upstream_request_completed",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "model_used": self.name,
                "segments_count": len(segments),
                "text_chars": len(text),
                "inference_ms": timings.inference_ms,
            },
        )
        return ASRResult(
            request_id=request.request_id,
            session_id=request.session_id,
            task=request.task,
            model_requested=request.model,
            model_used=self.name,
            language_detected=language_detected,
            duration_ms=duration_ms,
            text=text,
            segments=segments,
            timings=timings,
            artifacts={"voxtral_raw_response": json.dumps(payload)},
        )

    async def _recv_until(self, websocket, session_id: str, wanted_types: set[str], timeout_seconds: float = 5.0) -> dict:
        while True:
            message = await asyncio.wait_for(websocket.recv(), timeout=timeout_seconds)
            payload = json.loads(message)
            message_type = payload.get("type")
            if message_type in wanted_types:
                return payload
            logger.info(
                "voxtral_upstream_event_ignored",
                extra={"session_id": session_id, "event_type": message_type},
            )

    async def _receiver_loop(self, session_id: str) -> None:
        state = self._sessions[session_id]
        websocket = state["upstream"]
        queue: asyncio.Queue[dict] = state["events"]
        try:
            async for message in websocket:
                payload = json.loads(message)
                message_type = payload.get("type")
                if message_type == "transcription.delta":
                    delta = str(payload.get("delta", "")).strip()
                    if not delta:
                        continue
                    state["partial_text"] = f"{state['partial_text']}{delta}".strip()
                    await queue.put(
                        {
                            "type": "partial_transcript",
                            "session_id": session_id,
                            "seq": state["last_seq"],
                            "stable": False,
                            "text": state["partial_text"],
                            "start_ms": 0,
                            "end_ms": state["buffered_ms"],
                        }
                    )
                elif message_type == "transcription.done":
                    state["final_payload"] = payload
                    state["done"].set()
                    await queue.put({"type": "upstream_done", "session_id": session_id})
                elif message_type == "error":
                    state["error"] = payload
                    state["done"].set()
                    await queue.put({"type": "upstream_error", "session_id": session_id, "error": payload})
                else:
                    logger.info(
                        "voxtral_upstream_event",
                        extra={"session_id": session_id, "event_type": message_type},
                    )
        except Exception as exc:
            state["error"] = {"type": "error", "error": str(exc)}
            state["done"].set()
            with suppress(asyncio.QueueFull):
                await queue.put({"type": "upstream_error", "session_id": session_id, "error": repr(exc)})
            logger.error(
                "voxtral_receiver_failed",
                extra={"session_id": session_id, "error": repr(exc)},
            )

    async def transcribe_file(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        return await self._transcribe_wav_bytes(request, audio_bytes)

    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        if not self.ws_url:
            raise RuntimeError("Voxtral realtime upstream is not configured")
        headers, fallback_auth_used = self._realtime_headers()
        ws_target = f"{self.ws_url}/v1/realtime"
        auth_header_sent = "Authorization" in headers
        logger.info(
            "voxtral_ws_connecting",
            extra={
                "session_id": request.session_id,
                "request_id": request.request_id,
                "voxtral_ws_url": ws_target,
                "auth_header_sent": auth_header_sent,
                "api_key_configured": bool(self.api_key),
                "fallback_auth_used": fallback_auth_used,
            },
        )
        try:
            websocket = await websockets.connect(
                ws_target,
                max_size=None,
                additional_headers=headers,
            )
        except InvalidStatus as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code in {401, 403}:
                raise RuntimeError(
                    f"Voxtral realtime websocket auth failed for {ws_target} "
                    f"(auth_header_sent={auth_header_sent}, fallback_auth_used={fallback_auth_used})"
                ) from exc
            raise RuntimeError(
                f"Voxtral realtime websocket handshake failed for {ws_target} "
                f"(status={status_code}, auth_header_sent={auth_header_sent}, fallback_auth_used={fallback_auth_used})"
            ) from exc
        except Exception as exc:
            raise RuntimeError(
                f"Voxtral realtime websocket connect failed for {ws_target} "
                f"(auth_header_sent={auth_header_sent}, fallback_auth_used={fallback_auth_used})"
            ) from exc
        created = await self._recv_until(websocket, request.session_id, {"session.created"})
        await websocket.send(json.dumps({"type": "session.update", "model": self.model_name}))
        logger.info(
            "voxtral_stream_started",
            extra={
                "session_id": request.session_id,
                "request_id": request.request_id,
                "model_used": self.name,
                "voxtral_base_url": self.base_url,
                "voxtral_ws_url": self.ws_url,
                "voxtral_model_name": self.model_name,
                "sample_rate": request.sample_rate,
                "channels": request.channels,
                "upstream_session_id": created.get("id"),
                "auth_header_sent": auth_header_sent,
                "fallback_auth_used": fallback_auth_used,
            },
        )
        self._sessions[request.session_id] = {
            "request": request,
            "buffered_ms": 0,
            "last_partial_ms": 0,
            "last_seq": 0,
            "partial_text": "",
            "events": asyncio.Queue(),
            "done": asyncio.Event(),
            "error": None,
            "final_payload": None,
            "upstream": websocket,
        }
        self._sessions[request.session_id]["receiver_task"] = asyncio.create_task(self._receiver_loop(request.session_id))
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)

    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[dict]:
        state = self._sessions[session_id]
        pcm_bytes = decode_payload_b64(frame.payload_b64)
        bytes_per_ms = max(frame.sample_rate * frame.channels * 2 / 1000, 1)
        state["buffered_ms"] += int(len(pcm_bytes) / bytes_per_ms)
        state["last_seq"] = frame.seq
        await state["upstream"].send(
            json.dumps(
                {
                    "type": "input_audio_buffer.append",
                    "audio": frame.payload_b64,
                }
            )
        )
        if state["buffered_ms"] - state["last_partial_ms"] >= self.partial_window_ms:
            await state["upstream"].send(json.dumps({"type": "input_audio_buffer.commit"}))
            state["last_partial_ms"] = state["buffered_ms"]
        logger.info(
            "voxtral_stream_partial_window_ready",
            extra={
                "session_id": session_id,
                "seq": frame.seq,
                "buffered_ms": state["buffered_ms"],
                "partial_window_ms": self.partial_window_ms,
            },
        )
        events: list[dict] = []
        while True:
            try:
                event = state["events"].get_nowait()
            except asyncio.QueueEmpty:
                break
            if event["type"] == "partial_transcript":
                events.append(event)
            elif event["type"] == "upstream_error":
                raise RuntimeError(f"Voxtral realtime upstream error: {event['error']}")
        return events

    async def end_stream(self, session_id: str) -> ASRResult:
        state = self._sessions.pop(session_id)
        logger.info(
            "voxtral_stream_finishing",
            extra={
                "session_id": session_id,
                "buffered_ms": state["buffered_ms"],
                "model_used": self.name,
            },
        )
        await state["upstream"].send(json.dumps({"type": "input_audio_buffer.commit", "final": True}))
        await asyncio.wait_for(state["done"].wait(), timeout=15.0)
        receiver_task = state.get("receiver_task")
        if receiver_task is not None:
            receiver_task.cancel()
            with suppress(asyncio.CancelledError):
                await receiver_task
        await state["upstream"].close()
        if state["error"] is not None:
            raise RuntimeError(f"Voxtral realtime upstream error: {state['error']}")
        payload = state["final_payload"] or {}
        text = str(payload.get("text", "")).strip() or state["partial_text"]
        return ASRResult(
            request_id=f"{session_id}_voxtral_final",
            session_id=session_id,
            task="transcribe",
            model_requested=self.name,
            model_used=self.name,
            language_detected=payload.get("language"),
            duration_ms=state["buffered_ms"],
            text=text,
            segments=[
                ASRSegment(
                    segment_id="seg_1",
                    start_ms=0,
                    end_ms=state["buffered_ms"],
                    text=text,
                )
            ]
            if text
            else [],
            timings=TimingBreakdown(total_ms=state["buffered_ms"]),
            artifacts={"voxtral_realtime_final": json.dumps(payload)},
        )
