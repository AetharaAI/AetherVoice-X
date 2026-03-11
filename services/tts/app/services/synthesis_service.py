from __future__ import annotations

import io
import wave
from typing import Any

from aether_common.storage import StorageManager
from aether_common.telemetry import voice_model_fallback_total

from ..logging import logger
from ..pipeline.orchestrator import build_input
from ..schemas.requests import TTSRequest
from ..schemas.responses import TTSResult, TimingBreakdown
from .studio_service import StudioService
from .model_registry import ModelRegistry


class SynthesisService:
    def __init__(self, registry: ModelRegistry, storage: StorageManager, settings, studio_service: StudioService) -> None:
        self.registry = registry
        self.storage = storage
        self.settings = settings
        self.studio_service = studio_service

    def _estimate_duration_ms(self, audio_bytes: bytes) -> int:
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                return int(wav_file.getnframes() / wav_file.getframerate() * 1000)
        except Exception:
            return 0

    def _resolve_voice_metadata(self, request: TTSRequest) -> dict:
        return self.studio_service.resolve_voice_metadata(
            request.tenant_id,
            voice_id=request.voice,
            model=request.model,
            metadata=request.metadata,
            include_audio_bytes=False,
        )

    @staticmethod
    def _chatterbox_safe_voice(request: TTSRequest) -> tuple[str, dict[str, Any]]:
        metadata = dict(request.metadata)
        extra = dict(metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        resolved_voice = extra.get("resolved_voice")
        if not isinstance(resolved_voice, dict):
            return request.voice, metadata

        runtime_target = str(resolved_voice.get("runtime_target") or "").strip()
        source_model = str(resolved_voice.get("source_model") or "").strip()
        if runtime_target == "chatterbox" or source_model == "chatterbox":
            return request.voice, metadata

        extra["fallback_original_voice_id"] = request.voice
        extra["fallback_voice_route"] = "chatterbox_default"
        metadata["extra"] = extra
        return "default", metadata

    async def synthesize(self, request: TTSRequest) -> tuple[TTSResult, bytes]:
        started = __import__("time").perf_counter()
        text, voice = build_input(request.text, request.voice)
        metadata = dict(request.metadata)
        metadata["extra"] = self._resolve_voice_metadata(request)
        prepared = request.model_copy(update={"text": text, "voice": voice, "metadata": metadata})
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_batch()
        selected_voice = (prepared.metadata.get("extra") or {}).get("resolved_voice") if isinstance(prepared.metadata, dict) else None
        fallback_route_used: str | None = None
        try:
            audio_bytes, output_format = await adapter.synthesize(prepared)
        except Exception as exc:
            if adapter.name != "chatterbox":
                fallback = self.registry.fallback_batch()
                voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
                fallback_voice, fallback_metadata = self._chatterbox_safe_voice(prepared)
                audio_bytes, output_format = await fallback.synthesize(
                    prepared.model_copy(
                        update={
                            "model": fallback.name,
                            "voice": fallback_voice,
                            "metadata": fallback_metadata,
                        }
                    )
                )
                fallback_route_used = fallback.name
                adapter = fallback
            else:
                raise exc
        duration_ms = self._estimate_duration_ms(audio_bytes)
        key = f"tts/{request.tenant_id}/{request.session_id or 'no-session'}/{request.request_id}.{output_format}"
        audio_url = self.storage.upload_bytes(self.settings.s3_bucket_tts, key, audio_bytes, f"audio/{output_format}")
        timings = TimingBreakdown(inference_ms=int((__import__("time").perf_counter() - started) * 1000), encode_ms=0, total_ms=int((__import__("time").perf_counter() - started) * 1000))
        logger.info(
            "tts_completed",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "route": "/internal/synthesize",
                "tenant_id": request.tenant_id,
                "model_requested": request.model,
                "model_used": adapter.name,
                "total_ms": timings.total_ms,
                "status": "ok",
            },
        )
        return (
            TTSResult(
                request_id=request.request_id,
                model_used=adapter.name,
                audio_url=audio_url,
                duration_ms=duration_ms,
                timings=timings,
                artifacts={
                    "format": output_format,
                    "selected_voice_id": selected_voice.get("voice_id") if isinstance(selected_voice, dict) else prepared.voice,
                    "selected_voice_asset": selected_voice.get("display_name") if isinstance(selected_voice, dict) else prepared.voice,
                    "resolved_conditioning_asset": (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                    or (prepared.metadata.get("extra") or {}).get("generation_prompt"),
                    "actual_runtime_conditioning_source": (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                    or (prepared.metadata.get("extra") or {}).get("generation_prompt")
                    or "default",
                    "fallback_route_used": fallback_route_used,
                    "requested_model": request.model,
                },
            ),
            audio_bytes,
        )
