from __future__ import annotations

import io
import time
import wave
from typing import Any

from aether_common.telemetry import voice_model_fallback_total, voice_tts_time_to_first_chunk_ms
from redis.asyncio import Redis

from ..logging import logger
from ..pipeline.audio_encode import audio_to_b64
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamRuntimeTruth, TTSResult
from .model_registry import ModelRegistry
from .studio_service import StudioService
from .synthesis_service import SynthesisService
from .telemetry_service import TelemetryService


class StreamingService:
    def __init__(
        self,
        registry: ModelRegistry,
        synthesis_service: SynthesisService,
        redis: Redis,
        telemetry: TelemetryService,
        storage,
        settings,
        studio_service: StudioService,
    ) -> None:
        self.registry = registry
        self.synthesis_service = synthesis_service
        self.redis = redis
        self.telemetry = telemetry
        self.storage = storage
        self.settings = settings
        self.studio_service = studio_service
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

    def _runtime_truth(self, request: TTSStreamStartRequest, *, runtime_path_used: str, fallback_route_used: str | None) -> StreamRuntimeTruth:
        return StreamRuntimeTruth.model_validate(
            self.studio_service.resolve_stream_runtime_truth(
                request.tenant_id,
                requested_route=request.model,
                runtime_path_used=runtime_path_used,
                voice_id=request.voice,
                metadata=request.metadata,
                fallback_route_used=fallback_route_used,
            )
        )

    @staticmethod
    def _runtime_metadata(runtime: StreamRuntimeTruth) -> dict[str, Any]:
        return runtime.model_dump(exclude_none=True)

    async def start(self, request: TTSStreamStartRequest) -> dict:
        fallback_used = False
        fallback_route_used: str | None = None
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_stream()
            fallback_used = adapter.name != request.model
            fallback_route_used = adapter.name if fallback_used else None
        stream_session = None
        adapter_configured = getattr(adapter, "configured", False) or getattr(adapter, "ready", False)
        if not adapter.supports_streaming or not adapter_configured:
            fallback_used = True
            fallback = self.registry.fallback_stream()
            if fallback.name != adapter.name:
                voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
            adapter = fallback
            adapter_configured = getattr(adapter, "configured", False) or getattr(adapter, "ready", False)
            fallback_route_used = adapter.name if adapter.name != request.model else None
        if adapter.supports_streaming and adapter_configured:
            try:
                stream_session = await adapter.start_stream(request)
            except Exception:
                fallback_used = True
                fallback = self.registry.fallback_stream()
                if fallback.name != adapter.name:
                    voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
                adapter = fallback
                fallback_route_used = adapter.name if adapter.name != request.model else None
        runtime_truth = self._runtime_truth(
            request,
            runtime_path_used=adapter.name,
            fallback_route_used=fallback_route_used,
        )
        self.sessions[request.session_id] = {
            "request": request,
            "adapter": adapter,
            "mode": "adapter" if stream_session is not None else "microbatch",
            "chunks": [],
            "sequence": 0,
            "text_fragments": [],
            "started_at": time.perf_counter(),
            "first_chunk_recorded": False,
            "fallback_used": fallback_used,
            "runtime": runtime_truth,
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
                "selected_voice_id": runtime_truth.selected_voice_id or "",
                "resolved_conditioning_asset": runtime_truth.resolved_conditioning_asset or "",
                "runtime_path_used": runtime_truth.runtime_path_used,
                "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                "final_artifact_source_route": runtime_truth.final_artifact_source_route,
                "fallback_route_used": runtime_truth.fallback_route_used or "",
                "runtime_truth": str(self._runtime_metadata(runtime_truth)),
            },
        )
        self.telemetry.session_started()
        logger.info(
            "tts_stream_started",
            extra={
                "session_id": request.session_id,
                "requested_route": request.model,
                "runtime_path_used": runtime_truth.runtime_path_used,
                "selected_voice_id": runtime_truth.selected_voice_id,
                "resolved_conditioning_asset": runtime_truth.resolved_conditioning_asset,
                "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                "final_artifact_source_route": runtime_truth.final_artifact_source_route,
                "fallback_route_used": runtime_truth.fallback_route_used,
            },
        )
        return {
            "session_id": request.session_id,
            "model": adapter.name,
            "expires_in_seconds": 3600,
            "model_requested": request.model,
            "model_used": adapter.name,
            "fallback_used": fallback_used,
            "runtime": self._runtime_metadata(runtime_truth),
        }

    async def push(self, session_id: str, text: str) -> list[dict]:
        state = self.sessions[session_id]
        state["text_fragments"].append(text)
        runtime_truth: StreamRuntimeTruth = state["runtime"]
        logger.info(
            "tts_stream_text_push",
            extra={
                "session_id": session_id,
                "text_chars": len(text),
                "runtime_path_used": runtime_truth.runtime_path_used,
                "selected_voice_id": runtime_truth.selected_voice_id,
                "resolved_conditioning_asset": runtime_truth.resolved_conditioning_asset,
                "fallback_route_used": runtime_truth.fallback_route_used,
            },
        )
        if state["mode"] == "adapter":
            events = await state["adapter"].push_text(session_id, text)
            for event in events:
                event_metadata = dict(event.get("metadata") or {})
                event_metadata.update(
                    {
                        "runtime": self._runtime_metadata(runtime_truth),
                        "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    }
                )
                event["metadata"] = event_metadata
            if not state["first_chunk_recorded"] and any(event.get("type") == "audio_chunk" for event in events):
                state["first_chunk_recorded"] = True
                first_chunk_ms = int((time.perf_counter() - state["started_at"]) * 1000)
                voice_tts_time_to_first_chunk_ms.labels(service="tts").observe(first_chunk_ms)
                logger.info(
                    "tts_stream_first_chunk",
                    extra={
                        "session_id": session_id,
                        "first_chunk_ms": first_chunk_ms,
                        "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                        "runtime_path_used": runtime_truth.runtime_path_used,
                    },
                )
            if events:
                logger.info(
                    "tts_stream_chunk_batch",
                    extra={
                        "session_id": session_id,
                        "chunk_events": sum(1 for event in events if event.get("type") == "audio_chunk"),
                        "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                        "conditioning_source": runtime_truth.actual_runtime_conditioning_source,
                    },
                )
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
            first_chunk_ms = int((time.perf_counter() - state["started_at"]) * 1000)
            voice_tts_time_to_first_chunk_ms.labels(service="tts").observe(first_chunk_ms)
            logger.info(
                "tts_stream_first_chunk",
                extra={
                    "session_id": session_id,
                    "first_chunk_ms": first_chunk_ms,
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    "runtime_path_used": runtime_truth.runtime_path_used,
                },
            )
        return [
            {
                "type": "audio_chunk",
                "session_id": session_id,
                "sequence": state["sequence"],
                "audio_b64": audio_to_b64(audio_bytes),
                "format": request.format,
                "metadata": {
                    "audio_url": result.audio_url,
                    "runtime": self._runtime_metadata(runtime_truth),
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                },
            }
        ]

    async def complete_text(self, session_id: str) -> list[dict]:
        state = self.sessions[session_id]
        runtime_truth: StreamRuntimeTruth = state["runtime"]
        logger.info(
            "tts_stream_text_complete",
            extra={
                "session_id": session_id,
                "runtime_path_used": runtime_truth.runtime_path_used,
                "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                "selected_voice_id": runtime_truth.selected_voice_id,
                "resolved_conditioning_asset": runtime_truth.resolved_conditioning_asset,
                "fallback_route_used": runtime_truth.fallback_route_used,
            },
        )
        if state["mode"] != "adapter":
            return []
        events = await state["adapter"].complete_text(session_id)
        for event in events:
            event_metadata = dict(event.get("metadata") or {})
            event_metadata.update(
                {
                    "runtime": self._runtime_metadata(runtime_truth),
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                }
            )
            event["metadata"] = event_metadata
        if not state["first_chunk_recorded"] and any(event.get("type") == "audio_chunk" for event in events):
            state["first_chunk_recorded"] = True
            first_chunk_ms = int((time.perf_counter() - state["started_at"]) * 1000)
            voice_tts_time_to_first_chunk_ms.labels(service="tts").observe(first_chunk_ms)
            logger.info(
                "tts_stream_first_chunk",
                extra={
                    "session_id": session_id,
                    "first_chunk_ms": first_chunk_ms,
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    "runtime_path_used": runtime_truth.runtime_path_used,
                },
            )
        if events:
            logger.info(
                "tts_stream_chunk_batch",
                extra={
                    "session_id": session_id,
                    "chunk_events": sum(1 for event in events if event.get("type") == "audio_chunk"),
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    "conditioning_source": runtime_truth.actual_runtime_conditioning_source,
                },
            )
        return events

    async def finish(self, session_id: str) -> tuple[TTSResult, bytes]:
        state = self.sessions.pop(session_id)
        runtime_truth: StreamRuntimeTruth = state["runtime"]
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
                    artifacts={
                        **completion.artifacts,
                        "format": output_format,
                        "runtime": self._runtime_metadata(runtime_truth),
                        "requested_route": runtime_truth.requested_route or completion.model_used,
                        "runtime_path_used": runtime_truth.runtime_path_used,
                        "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                        "final_artifact_source_route": runtime_truth.final_artifact_source_route,
                        "fallback_route_used": runtime_truth.fallback_route_used,
                    },
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
                result.artifacts = {
                    **result.artifacts,
                    "runtime": self._runtime_metadata(runtime_truth),
                    "requested_route": runtime_truth.requested_route or request.model,
                    "runtime_path_used": runtime_truth.runtime_path_used,
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    "final_artifact_source_route": runtime_truth.final_artifact_source_route,
                    "fallback_route_used": runtime_truth.fallback_route_used,
                }
            await self.redis.hset(f"voice:session:{session_id}:meta", mapping={"status": "ended"})
            logger.info(
                "tts_stream_finished",
                extra={
                    "session_id": session_id,
                    "requested_route": runtime_truth.requested_route,
                    "runtime_path_used": runtime_truth.runtime_path_used,
                    "live_chunk_source_route": runtime_truth.live_chunk_source_route,
                    "final_artifact_source_route": runtime_truth.final_artifact_source_route,
                    "selected_voice_id": runtime_truth.selected_voice_id,
                    "resolved_conditioning_asset": runtime_truth.resolved_conditioning_asset,
                    "fallback_route_used": runtime_truth.fallback_route_used,
                    "duration_ms": result.duration_ms,
                },
            )
            return result, audio_bytes
        finally:
            self.telemetry.session_ended()
