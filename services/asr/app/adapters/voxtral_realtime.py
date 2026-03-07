from __future__ import annotations

import json
from pathlib import Path

import httpx

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
        model_name: str,
        api_key: str | None = None,
        partial_window_ms: int = 1600,
        timeout_seconds: float = 90.0,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.model_name = model_name
        self.api_key = api_key
        self.partial_window_ms = partial_window_ms
        self.ready = bool(self.base_url)
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout_seconds) if self.ready else None
        self._sessions: dict[str, dict] = {}
        logger.info(
            "voxtral_adapter_initialized",
            extra={
                "voxtral_ready": self.ready,
                "voxtral_base_url": self.base_url or "unset",
                "voxtral_model_name": self.model_name,
                "voxtral_partial_window_ms": self.partial_window_ms,
            },
        )

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {"Authorization": f"Bearer {self.api_key}"}

    async def _transcribe_wav_bytes(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        if not self.ready or self._client is None:
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
        response = await self._client.post("/v1/audio/transcriptions", data=fields, files=files, headers=self._headers())
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

    async def transcribe_file(self, request: ASRFileRequest, audio_bytes: bytes) -> ASRResult:
        return await self._transcribe_wav_bytes(request, audio_bytes)

    async def start_stream(self, request: ASRStreamStartRequest) -> StreamSession:
        if not self.ready:
            raise RuntimeError("Voxtral realtime upstream is not configured")
        logger.info(
            "voxtral_stream_started",
            extra={
                "session_id": request.session_id,
                "request_id": request.request_id,
                "model_used": self.name,
                "voxtral_base_url": self.base_url,
                "voxtral_model_name": self.model_name,
                "sample_rate": request.sample_rate,
                "channels": request.channels,
            },
        )
        self._sessions[request.session_id] = {
            "request": request,
            "buffer": bytearray(),
            "buffered_ms": 0,
            "last_partial_text": "",
            "last_partial_ms": 0,
        }
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)

    async def push_audio_frame(self, session_id: str, frame: AudioFrame) -> list[dict]:
        state = self._sessions[session_id]
        pcm_bytes = decode_payload_b64(frame.payload_b64)
        state["buffer"].extend(pcm_bytes)
        bytes_per_ms = max(frame.sample_rate * frame.channels * 2 / 1000, 1)
        state["buffered_ms"] = int(len(state["buffer"]) / bytes_per_ms)
        if state["buffered_ms"] - state["last_partial_ms"] < self.partial_window_ms:
            return []
        logger.info(
            "voxtral_stream_partial_window_ready",
            extra={
                "session_id": session_id,
                "seq": frame.seq,
                "buffered_ms": state["buffered_ms"],
                "partial_window_ms": self.partial_window_ms,
            },
        )
        wav_bytes = pcm16_to_wav_bytes(
            bytes(state["buffer"]),
            sample_rate=frame.sample_rate,
            channels=frame.channels,
        )
        request = ASRFileRequest(
            request_id=f"{session_id}_voxtral_partial_{frame.seq}",
            session_id=session_id,
            tenant_id=state["request"].tenant_id,
            model=self.name,
            task="transcribe",
            language=state["request"].language,
            timestamps=True,
            storage_mode="ephemeral",
            metadata=state["request"].metadata,
        )
        result = await self._transcribe_wav_bytes(request, wav_bytes)
        if not result.text or result.text == state["last_partial_text"]:
            return []
        state["last_partial_text"] = result.text
        state["last_partial_ms"] = state["buffered_ms"]
        return [
            {
                "type": "partial_transcript",
                "session_id": session_id,
                "seq": frame.seq,
                "stable": False,
                "text": result.text,
                "start_ms": result.segments[0].start_ms if result.segments else 0,
                "end_ms": result.segments[-1].end_ms if result.segments else state["buffered_ms"],
            }
        ]

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
        wav_bytes = pcm16_to_wav_bytes(
            bytes(state["buffer"]),
            sample_rate=state["request"].sample_rate,
            channels=state["request"].channels,
        )
        request = ASRFileRequest(
            request_id=f"{session_id}_voxtral_final",
            session_id=session_id,
            tenant_id=state["request"].tenant_id,
            model=self.name,
            task="transcribe",
            language=state["request"].language,
            timestamps=True,
            storage_mode="ephemeral",
            metadata=state["request"].metadata,
        )
        result = await self._transcribe_wav_bytes(request, wav_bytes)
        if not result.segments:
            result.duration_ms = state["buffered_ms"]
        return result
