from __future__ import annotations

import io
import wave

from aether_common.telemetry import voice_model_fallback_total, voice_tts_time_to_first_chunk_ms
from redis.asyncio import Redis

from ..pipeline.audio_encode import audio_to_b64
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import TTSResult
from .model_registry import ModelRegistry
from .synthesis_service import SynthesisService
from .telemetry_service import TelemetryService


class StreamingService:
    def __init__(self, registry: ModelRegistry, synthesis_service: SynthesisService, redis: Redis, telemetry: TelemetryService, storage, settings) -> None:
        self.registry = registry
        self.synthesis_service = synthesis_service
        self.redis = redis
        self.telemetry = telemetry
        self.storage = storage
        self.settings = settings
        self.sessions: dict[str, dict] = {}

    def _estimate_duration_ms(self, audio_bytes: bytes) -> int:
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                return int(wav_file.getnframes() / wav_file.getframerate() * 1000)
        except Exception:
            return 0

    def _store_stream_audio(self, *, tenant_id: str, session_id: str, request_id: str, audio_bytes: bytes, output_format: str) -> str:
        key = f"tts/{tenant_id}/{session_id}/{request_id}.{output_format}"
        return self.storage.upload_bytes(
            self.settings.s3_bucket_tts,
            key,
            audio_bytes,
            f"audio/{output_format}",
        )

    async def start(self, request: TTSStreamStartRequest) -> dict:
        fallback_used = False
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_stream()
            fallback_used = adapter.name != request.model
        stream_session = None
        adapter_configured = getattr(adapter, "configured", False) or getattr(adapter, "ready", False)
        if not adapter.supports_streaming or not adapter_configured:
            fallback_used = True
            fallback = self.registry.fallback_stream()
            if fallback.name != adapter.name:
                voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
            adapter = fallback
            adapter_configured = getattr(adapter, "configured", False) or getattr(adapter, "ready", False)
        if adapter.supports_streaming and adapter_configured:
            try:
                stream_session = await adapter.start_stream(request)
            except Exception:
                fallback_used = True
                fallback = self.registry.fallback_stream()
                if fallback.name != adapter.name:
                    voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
                adapter = fallback
        self.sessions[request.session_id] = {
            "request": request,
            "adapter": adapter,
            "mode": "adapter" if stream_session is not None else "microbatch",
            "chunks": [],
            "sequence": 0,
            "text_fragments": [],
            "started_at": __import__("time").perf_counter(),
            "first_chunk_recorded": False,
        }
        await self.redis.hset(
            f"voice:session:{request.session_id}:meta",
            mapping={
                "session_id": request.session_id,
                "tenant_id": request.tenant_id,
                "type": "tts_stream",
                "model": adapter.name,
                "status": "active",
                "fallback_used": str(fallback_used).lower(),
            },
        )
        self.telemetry.session_started()
        return {"session_id": request.session_id, "model": adapter.name, "expires_in_seconds": 3600}

    async def push(self, session_id: str, text: str) -> list[dict]:
        state = self.sessions[session_id]
        state["text_fragments"].append(text)
        if state["mode"] == "adapter":
            events = await state["adapter"].push_text(session_id, text)
            if not state["first_chunk_recorded"] and any(event.get("type") == "audio_chunk" for event in events):
                state["first_chunk_recorded"] = True
                voice_tts_time_to_first_chunk_ms.labels(service="tts").observe((__import__("time").perf_counter() - state["started_at"]) * 1000)
            return events
        state["sequence"] += 1
        state["chunks"].append(text)
        request = TTSRequest(
            request_id=f"{session_id}_{state['sequence']}",
            session_id=session_id,
            tenant_id=state["request"].tenant_id,
            model=state["adapter"].name,
            voice=state["request"].voice,
            text=text,
            format=state["request"].format,
            sample_rate=state["request"].sample_rate,
            stream=True,
            metadata=state["request"].metadata,
        )
        result, audio_bytes = await self.synthesis_service.synthesize(request)
        if not state["first_chunk_recorded"]:
            state["first_chunk_recorded"] = True
            voice_tts_time_to_first_chunk_ms.labels(service="tts").observe((__import__("time").perf_counter() - state["started_at"]) * 1000)
        return [
            {
                "type": "audio_chunk",
                "session_id": session_id,
                "sequence": state["sequence"],
                "audio_b64": audio_to_b64(audio_bytes),
                "format": request.format,
                "metadata": {"audio_url": result.audio_url},
            }
        ]

    async def finish(self, session_id: str) -> tuple[TTSResult, bytes]:
        state = self.sessions.pop(session_id)
        try:
            if state["mode"] == "adapter":
                completion, audio_bytes = await state["adapter"].end_stream(session_id)
                output_format = completion.format or "wav"
                request_id = f"{session_id}_final"
                audio_url = self._store_stream_audio(
                    tenant_id=state["request"].tenant_id,
                    session_id=session_id,
                    request_id=request_id,
                    audio_bytes=audio_bytes,
                    output_format=output_format,
                )
                result = TTSResult(
                    request_id=request_id,
                    model_used=completion.model_used,
                    audio_url=audio_url,
                    duration_ms=completion.duration_ms or self._estimate_duration_ms(audio_bytes),
                    timings=completion.timings,
                    artifacts={**completion.artifacts, "format": output_format},
                )
            else:
                joined_text = " ".join(state["chunks"]).strip()
                request = TTSRequest(
                    request_id=f"{session_id}_final",
                    session_id=session_id,
                    tenant_id=state["request"].tenant_id,
                    model=state["adapter"].name,
                    voice=state["request"].voice,
                    text=joined_text,
                    format=state["request"].format,
                    sample_rate=state["request"].sample_rate,
                    stream=True,
                    metadata=state["request"].metadata,
                )
                result, audio_bytes = await self.synthesis_service.synthesize(request)
            await self.redis.hset(f"voice:session:{session_id}:meta", mapping={"status": "ended"})
            return result, audio_bytes
        finally:
            self.telemetry.session_ended()
