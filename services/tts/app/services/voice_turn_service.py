from __future__ import annotations

import io
import json
import re
import time
import wave
from typing import Any, Callable

import httpx
from aether_common.model_aliases import normalize_tts_model_name

from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import TTSResult, TimingBreakdown
from ..schemas.voice import VoiceTurnRequest, VoiceTurnResult, VoiceTurnTimings
from .studio_service import StudioService
from .synthesis_service import SynthesisService
from ..utils.text import normalize_text


class VoiceTurnService:
    _BLOCK_TAG_PATTERNS = (
        re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<tool_call>.*?</tool_call>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<tool_response>.*?</tool_response>", re.IGNORECASE | re.DOTALL),
    )
    _INLINE_TOKEN_PATTERNS = (
        re.compile(r"<\|reserved_\d+\|>", re.IGNORECASE),
        re.compile(r"<reserved_\d+>", re.IGNORECASE),
        re.compile(r"</?think>", re.IGNORECASE),
        re.compile(r"</?tool_call>", re.IGNORECASE),
        re.compile(r"</?tool_response>", re.IGNORECASE),
    )

    def __init__(
        self,
        settings,
        studio_service: StudioService,
        synthesis_service: SynthesisService,
        client_factory: Callable[..., httpx.AsyncClient] | None = None,
    ) -> None:
        self.settings = settings
        self.studio_service = studio_service
        self.synthesis_service = synthesis_service
        self.client_factory = client_factory or (lambda **kwargs: httpx.AsyncClient(timeout=45.0, **kwargs))
        self.registry = getattr(synthesis_service, "registry", None)

    @staticmethod
    def _content_text(content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str) and item.strip():
                    parts.append(item.strip())
                    continue
                if not isinstance(item, dict):
                    continue
                if isinstance(item.get("text"), str) and item["text"].strip():
                    parts.append(item["text"].strip())
                    continue
                if item.get("type") == "output_text" and isinstance(item.get("text"), str) and item["text"].strip():
                    parts.append(item["text"].strip())
            return "\n".join(parts).strip()
        return ""

    @classmethod
    def _extract_response_text(cls, payload: Any) -> str:
        if not isinstance(payload, dict):
            return ""
        choices = payload.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message") if isinstance(choices[0], dict) else None
            if isinstance(message, dict):
                text = cls._content_text(message.get("content"))
                if text:
                    return text
        output = payload.get("output")
        if isinstance(output, list):
            parts: list[str] = []
            for entry in output:
                if not isinstance(entry, dict):
                    continue
                text = cls._content_text(entry.get("content"))
                if text:
                    parts.append(text)
            if parts:
                return "\n".join(parts).strip()
        return cls._content_text(payload.get("content"))

    @classmethod
    def _sanitize_response_text(cls, text: str) -> str:
        cleaned = text or ""
        for pattern in cls._BLOCK_TAG_PATTERNS:
            cleaned = pattern.sub(" ", cleaned)
        for pattern in cls._INLINE_TOKEN_PATTERNS:
            cleaned = pattern.sub(" ", cleaned)
        cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
        cleaned = normalize_text(cleaned)
        return cleaned.strip()

    @staticmethod
    def _upstream_error_detail(response: httpx.Response) -> str:
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail") or payload.get("error") or payload.get("message")
                if isinstance(detail, dict):
                    return json.dumps(detail)
                if isinstance(detail, str) and detail.strip():
                    return detail.strip()
        except Exception:
            pass
        return response.text.strip() or response.reason_phrase or "LLM request failed"

    @staticmethod
    def _estimate_duration_ms(audio_bytes: bytes) -> int:
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                return int(wav_file.getnframes() / wav_file.getframerate() * 1000)
        except Exception:
            return 0

    def _supports_streaming_tts(self, model_name: str) -> bool:
        if self.registry is None:
            return False
        try:
            adapter = self.registry.get(model_name)
        except Exception:
            return False
        return bool(getattr(adapter, "supports_streaming", False))

    def _prepare_stream_request(self, request: VoiceTurnRequest, *, model_name: str) -> TTSStreamStartRequest:
        metadata = dict(request.metadata)
        metadata["extra"] = self.studio_service.resolve_voice_metadata(
            request.tenant_id,
            voice_id=request.voice,
            model=model_name,
            metadata=request.metadata,
            include_audio_bytes=model_name == "moss_realtime",
        )
        return TTSStreamStartRequest(
            request_id=request.request_id,
            session_id=request.session_id or f"{request.request_id}_stream",
            tenant_id=request.tenant_id,
            model=model_name,
            voice=request.voice,
            sample_rate=request.sample_rate,
            format=request.format,
            context_mode="conversation",
            metadata=metadata,
        )

    def _resolve_stream_runtime(self, request: TTSStreamStartRequest, *, runtime_path_used: str, fallback_route_used: str | None) -> dict[str, Any]:
        return self.studio_service.resolve_stream_runtime_truth(
            request.tenant_id,
            requested_route=request.model,
            runtime_path_used=runtime_path_used,
            voice_id=request.voice,
            metadata=request.metadata,
            fallback_route_used=fallback_route_used,
        )

    @staticmethod
    def _capture_stream_event_metrics(
        events: list[dict[str, Any]],
        *,
        started_at: float,
        first_chunk_ms: int | None,
        chunk_events: int,
    ) -> tuple[int | None, int]:
        next_first_chunk_ms = first_chunk_ms
        next_chunk_events = chunk_events
        for event in events:
            if event.get("type") != "audio_chunk":
                continue
            next_chunk_events += 1
            if next_first_chunk_ms is None:
                next_first_chunk_ms = int((time.perf_counter() - started_at) * 1000)
        return next_first_chunk_ms, next_chunk_events

    def _store_stream_audio(self, *, tenant_id: str, session_id: str, request_id: str, audio_bytes: bytes, output_format: str) -> str:
        key = f"tts/{tenant_id}/{session_id}/{request_id}.{output_format}"
        return self.synthesis_service.storage.upload_bytes(
            self.settings.s3_bucket_tts,
            key,
            audio_bytes,
            f"audio/{output_format}",
        )

    async def _synthesize_streaming_turn(self, request: VoiceTurnRequest, response_text: str) -> TTSResult:
        if self.registry is None:
            raise RuntimeError("Streaming TTS registry is not available")

        requested_model = normalize_tts_model_name(request.tts_model)
        try:
            adapter = self.registry.get(requested_model)
        except KeyError:
            adapter = self.registry.fallback_stream()
        fallback_route_used: str | None = None
        adapter_ready = bool(getattr(adapter, "supports_streaming", False)) and bool(
            getattr(adapter, "configured", False) or getattr(adapter, "ready", False)
        )
        if not adapter_ready:
            fallback = self.registry.fallback_stream()
            fallback_route_used = fallback.name if fallback.name != requested_model else None
            adapter = fallback

        prepared_request = self._prepare_stream_request(request, model_name=adapter.name)
        runtime_truth = self._resolve_stream_runtime(
            prepared_request,
            runtime_path_used=adapter.name,
            fallback_route_used=fallback_route_used,
        )
        started_at = time.perf_counter()
        first_chunk_ms: int | None = None
        chunk_events = 0
        try:
            await adapter.start_stream(prepared_request)
        except Exception:
            fallback = self.registry.fallback_stream()
            if fallback.name == adapter.name:
                raise
            fallback_route_used = fallback.name if fallback.name != requested_model else None
            adapter = fallback
            prepared_request = self._prepare_stream_request(request, model_name=adapter.name)
            runtime_truth = self._resolve_stream_runtime(
                prepared_request,
                runtime_path_used=adapter.name,
                fallback_route_used=fallback_route_used,
            )
            await adapter.start_stream(prepared_request)

        push_events = await adapter.push_text(prepared_request.session_id, response_text)
        first_chunk_ms, chunk_events = self._capture_stream_event_metrics(
            push_events,
            started_at=started_at,
            first_chunk_ms=first_chunk_ms,
            chunk_events=chunk_events,
        )
        complete_events = await adapter.complete_text(prepared_request.session_id)
        first_chunk_ms, chunk_events = self._capture_stream_event_metrics(
            complete_events,
            started_at=started_at,
            first_chunk_ms=first_chunk_ms,
            chunk_events=chunk_events,
        )
        completion, audio_bytes = await adapter.end_stream(prepared_request.session_id)
        total_ms = int((time.perf_counter() - started_at) * 1000)
        output_format = completion.format or request.format or "wav"
        request_id = f"{prepared_request.session_id}_final"
        audio_url = self._store_stream_audio(
            tenant_id=request.tenant_id,
            session_id=prepared_request.session_id,
            request_id=request_id,
            audio_bytes=audio_bytes,
            output_format=output_format,
        )
        timings = completion.timings.model_copy(
            update={
                "inference_ms": completion.timings.inference_ms or total_ms,
                "total_ms": completion.timings.total_ms or total_ms,
            }
        )
        return TTSResult(
            request_id=request_id,
            model_used=completion.model_used or adapter.name,
            audio_url=audio_url,
            duration_ms=completion.duration_ms or self._estimate_duration_ms(audio_bytes),
            timings=timings,
            artifacts={
                **dict(completion.artifacts or {}),
                "format": output_format,
                "runtime": runtime_truth,
                "requested_route": request.tts_model,
                "runtime_path_used": runtime_truth.get("runtime_path_used") or adapter.name,
                "live_chunk_source_route": runtime_truth.get("live_chunk_source_route") or adapter.name,
                "final_artifact_source_route": runtime_truth.get("final_artifact_source_route") or adapter.name,
                "fallback_route_used": runtime_truth.get("fallback_route_used") or fallback_route_used or "",
                "tts_mode": "streaming",
                "tts_first_chunk_ms": first_chunk_ms or 0,
                "tts_chunk_events": chunk_events,
            },
        )

    async def generate_turn(self, request: VoiceTurnRequest) -> VoiceTurnResult:
        transcript_text = request.transcript_text.strip()
        if not transcript_text:
            raise ValueError("A finalized transcript is required before generating a voice turn.")

        routing = self.studio_service.get_routing()
        if not routing.enabled:
            raise ValueError("Studio LLM routing is disabled. Save an enabled provider/model in TTS Studio first.")
        if not routing.model:
            raise ValueError("Studio LLM routing does not have a model selected yet.")

        base_url, headers = self.studio_service.resolve_provider_request_config(
            routing.provider,
            base_url_override=routing.base_url,
        )
        llm_started = time.perf_counter()
        llm_payload = {
            "model": routing.model,
            "messages": [
                {
                    "role": "system",
                    "content": routing.system_prompt or "Respond with short, spoken-ready voice agent replies.",
                },
                {"role": "user", "content": transcript_text},
            ],
            "stream": False,
            "temperature": 0.2,
        }

        async with self.client_factory(base_url=base_url) as client:
            response = await client.post("/chat/completions", headers=headers, json=llm_payload)
            if not response.is_success:
                raise RuntimeError(f"LLM generation failed: {self._upstream_error_detail(response)}")
            llm_response = response.json()

        response_text = self._sanitize_response_text(self._extract_response_text(llm_response))
        if not response_text:
            raise RuntimeError("LLM generation returned an empty reply.")

        llm_total_ms = int((time.perf_counter() - llm_started) * 1000)
        metadata = dict(request.metadata)
        extra = dict(metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        extra.update(
            {
                "source_transcript_text": transcript_text,
                "llm_provider": routing.provider,
                "llm_model_requested": routing.model,
                "llm_base_url": base_url,
                "llm_request_id": llm_response.get("id"),
            }
        )
        metadata["extra"] = extra

        if self._supports_streaming_tts(request.tts_model):
            tts_result = await self._synthesize_streaming_turn(
                request.model_copy(update={"metadata": metadata}),
                response_text,
            )
        else:
            tts_request = TTSRequest(
                request_id=request.request_id,
                session_id=request.session_id,
                tenant_id=request.tenant_id,
                model=request.tts_model,
                voice=request.voice,
                text=response_text,
                format=request.format,
                sample_rate=request.sample_rate,
                stream=False,
                style=request.style,
                metadata=metadata,
            )
            tts_result, _audio_bytes = await self.synthesis_service.synthesize(tts_request)
        tts_timings = tts_result.timings
        return VoiceTurnResult(
            request_id=request.request_id,
            transcript_text=transcript_text,
            response_text=response_text,
            llm_provider=routing.provider,
            llm_model_requested=routing.model,
            llm_model_used=str(llm_response.get("model") or routing.model),
            llm_base_url=base_url,
            llm_request_id=str(llm_response.get("id")) if llm_response.get("id") else None,
            llm_timings=TimingBreakdown(inference_ms=llm_total_ms, total_ms=llm_total_ms),
            tts_model_requested=request.tts_model,
            tts_model_used=tts_result.model_used,
            audio_url=tts_result.audio_url,
            duration_ms=tts_result.duration_ms,
            tts_timings=tts_timings,
            timings=VoiceTurnTimings(
                llm_ms=llm_total_ms,
                tts_ms=tts_timings.total_ms,
                total_ms=llm_total_ms + tts_timings.total_ms,
            ),
            artifacts={
                **dict(tts_result.artifacts),
                "llm_provider": routing.provider,
                "llm_model_requested": routing.model,
                "llm_model_used": str(llm_response.get("model") or routing.model),
            },
        )
