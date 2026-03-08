from __future__ import annotations

import json

from redis.asyncio import Redis

from aether_common.telemetry import (
    voice_asr_stream_time_to_final_ms,
    voice_asr_stream_time_to_first_partial_ms,
    voice_model_fallback_total,
)

from ..logging import logger
from ..schemas.requests import ASRStreamStartRequest, AudioFrame
from ..schemas.responses import ASRResult
from ..utils.time import now_ms
from .model_registry import ModelRegistry
from .telemetry_service import TelemetryService


class StreamingService:
    def __init__(self, registry: ModelRegistry, redis: Redis, telemetry: TelemetryService) -> None:
        self.registry = registry
        self.redis = redis
        self.telemetry = telemetry
        self.sessions: dict[str, dict] = {}

    async def start(self, request: ASRStreamStartRequest) -> dict:
        metadata = request.metadata if isinstance(request.metadata, dict) else {}
        metadata_extra = metadata.get("extra") if isinstance(metadata.get("extra"), dict) else {}
        allow_fallback = bool(metadata_extra.get("allow_stream_fallback", request.model == "auto"))
        original_requested_model = str(metadata_extra.get("requested_model", request.model))
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_stream()
        fallback_used = False
        if not getattr(adapter, "ready", True) or not adapter.supports_streaming:
            if not allow_fallback:
                raise RuntimeError(f"Requested realtime model '{original_requested_model}' is not configured or ready")
            fallback_used = True
            fallback = self.registry.fallback_stream()
            voice_model_fallback_total.labels(service="asr", requested=request.model, used=fallback.name).inc()
            adapter = fallback
        logger.info(
            "stream_adapter_selected",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "model_requested": original_requested_model,
                "model_used": adapter.name,
                "fallback_used": fallback_used,
                "allow_fallback": allow_fallback,
            },
        )
        session = await adapter.start_stream(request.model_copy(update={"model": adapter.name}))
        self.sessions[request.session_id] = {
            "adapter": adapter,
            "request": request,
            "started_at_ms": now_ms(),
            "first_partial_recorded": False,
        }
        await self.redis.hset(
            f"voice:session:{request.session_id}:meta",
            mapping={
                "session_id": request.session_id,
                "tenant_id": request.tenant_id,
                "type": "asr_stream",
                "model": adapter.name,
                "status": "active",
                "started_at": str(now_ms()),
                "triage_enabled": str(request.triage_enabled).lower(),
                "fallback_used": str(fallback_used).lower(),
            },
        )
        self.telemetry.session_started()
        payload = session.model_dump()
        payload["model_used"] = adapter.name
        payload["fallback_used"] = fallback_used
        payload["model_requested"] = original_requested_model
        return payload

    async def push(self, session_id: str, frame: AudioFrame) -> list[dict]:
        state = self.sessions[session_id]
        events = await state["adapter"].push_audio_frame(session_id, frame)
        if events:
            logger.info(
                "stream_events_emitted",
                extra={
                    "session_id": session_id,
                    "model_used": state["adapter"].name,
                    "seq": frame.seq,
                    "events_count": len(events),
                },
            )
        for event in events:
            await self.redis.rpush(f"voice:session:{session_id}:events", json.dumps(event))
            if event["type"] == "partial_transcript" and not state["first_partial_recorded"]:
                state["first_partial_recorded"] = True
                voice_asr_stream_time_to_first_partial_ms.labels(service="asr").observe(now_ms() - state["started_at_ms"])
        return events

    async def finish(self, session_id: str) -> ASRResult:
        state = self.sessions.pop(session_id)
        result = await state["adapter"].end_stream(session_id)
        await self.redis.set(
            f"voice:session:{session_id}:asr:final",
            result.model_dump_json(),
        )
        await self.redis.hset(
            f"voice:session:{session_id}:meta",
            mapping={"status": "ended", "ended_at": str(now_ms())},
        )
        voice_asr_stream_time_to_final_ms.labels(service="asr").observe(now_ms() - state["started_at_ms"])
        self.telemetry.session_ended()
        logger.info(
            "stream_completed",
            extra={
                "request_id": result.request_id,
                "session_id": session_id,
                "route": "/internal/stream",
                "tenant_id": state["request"].tenant_id,
                "model_requested": state["request"].model,
                "model_used": result.model_used,
                "audio_duration_ms": result.duration_ms,
                "total_ms": result.timings.total_ms,
                "status": "ok",
            },
        )
        return result
