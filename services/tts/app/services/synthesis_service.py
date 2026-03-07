from __future__ import annotations

import io
import wave

from aether_common.storage import StorageManager
from aether_common.telemetry import voice_model_fallback_total

from ..logging import logger
from ..pipeline.orchestrator import build_input
from ..schemas.requests import TTSRequest
from ..schemas.responses import TTSResult, TimingBreakdown
from .model_registry import ModelRegistry


class SynthesisService:
    def __init__(self, registry: ModelRegistry, storage: StorageManager, settings) -> None:
        self.registry = registry
        self.storage = storage
        self.settings = settings

    def _estimate_duration_ms(self, audio_bytes: bytes) -> int:
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                return int(wav_file.getnframes() / wav_file.getframerate() * 1000)
        except Exception:
            return 0

    async def synthesize(self, request: TTSRequest) -> tuple[TTSResult, bytes]:
        started = __import__("time").perf_counter()
        text, voice = build_input(request.text, request.voice)
        prepared = request.model_copy(update={"text": text, "voice": voice})
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_batch()
        try:
            audio_bytes, output_format = await adapter.synthesize(prepared)
        except Exception as exc:
            if adapter.name != "chatterbox":
                fallback = self.registry.fallback_batch()
                voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
                audio_bytes, output_format = await fallback.synthesize(prepared.model_copy(update={"model": fallback.name}))
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
                artifacts={"format": output_format},
            ),
            audio_bytes,
        )
