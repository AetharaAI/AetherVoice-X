from __future__ import annotations

from aether_common.telemetry import voice_model_fallback_total, voice_tts_time_to_first_chunk_ms
from redis.asyncio import Redis

from ..pipeline.audio_encode import audio_to_b64
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import TTSResult
from .model_registry import ModelRegistry
from .synthesis_service import SynthesisService
from .telemetry_service import TelemetryService


class StreamingService:
    def __init__(self, registry: ModelRegistry, synthesis_service: SynthesisService, redis: Redis, telemetry: TelemetryService) -> None:
        self.registry = registry
        self.synthesis_service = synthesis_service
        self.redis = redis
        self.telemetry = telemetry
        self.sessions: dict[str, dict] = {}

    async def start(self, request: TTSStreamStartRequest) -> dict:
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_stream()
        fallback_used = False
        if not adapter.supports_streaming:
            fallback_used = True
            fallback = self.registry.fallback_stream()
            voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
            adapter = fallback
        self.sessions[request.session_id] = {
            "request": request,
            "adapter": adapter,
            "chunks": [],
            "sequence": 0,
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
        self.telemetry.session_ended()
        return result, audio_bytes
