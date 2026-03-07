from __future__ import annotations

import json

from aether_common.storage import StorageManager
from aether_common.telemetry import voice_model_fallback_total

from ..logging import logger
from ..pipeline.audio_normalize import normalize_audio
from ..pipeline.orchestrator import finalize_text
from ..schemas.requests import ASRFileRequest
from ..schemas.responses import ASRResult
from ..utils.audio_io import estimate_wav_duration_ms
from ..utils.time import elapsed_ms
from .model_registry import ModelRegistry


class TranscriptionService:
    def __init__(self, registry: ModelRegistry, storage: StorageManager, settings) -> None:
        self.registry = registry
        self.storage = storage
        self.settings = settings

    async def transcribe(self, request: ASRFileRequest, audio_bytes: bytes, format_hint: str | None = None) -> ASRResult:
        started = __import__("time").perf_counter()
        normalized = normalize_audio(audio_bytes, format_hint=format_hint, target_sample_rate=16000)
        preprocess_ms = elapsed_ms(started)
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_batch()
        if not getattr(adapter, "ready", True) or not adapter.supports_batch:
            adapter = self.registry.fallback_batch()
        used_fallback = False
        try:
            result = await adapter.transcribe_file(request, normalized)
        except Exception as exc:
            if adapter.name != "faster_whisper":
                used_fallback = True
                fallback = self.registry.fallback_batch()
                voice_model_fallback_total.labels(service="asr", requested=request.model, used=fallback.name).inc()
                result = await fallback.transcribe_file(request.model_copy(update={"model": fallback.name}), normalized)
            else:
                raise exc
        result.text = finalize_text(result.text)
        result.duration_ms = estimate_wav_duration_ms(normalized)
        result.timings.preprocess_ms = preprocess_ms
        result.timings.total_ms = elapsed_ms(started)
        if request.storage_mode == "persist":
            raw_key = f"raw/{request.tenant_id}/{request.session_id}/{request.request_id}.wav"
            normalized_key = f"normalized/{request.tenant_id}/{request.session_id}/{request.request_id}.wav"
            transcript_key = f"transcripts/{request.tenant_id}/{request.session_id}/{request.request_id}.json"
            raw_uri = self.storage.upload_bytes(self.settings.s3_bucket_raw, raw_key, audio_bytes, "audio/wav")
            normalized_uri = self.storage.upload_bytes(self.settings.s3_bucket_normalized, normalized_key, normalized, "audio/wav")
            transcript_uri = self.storage.upload_json(self.settings.s3_bucket_transcripts, transcript_key, result.model_dump())
            result.artifacts = {"raw_audio": raw_uri, "normalized_audio": normalized_uri, "transcript": transcript_uri}
        logger.info(
            "transcription_completed",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "route": "/internal/transcribe",
                "tenant_id": request.tenant_id,
                "model_requested": request.model,
                "model_used": result.model_used,
                "audio_duration_ms": result.duration_ms,
                "preprocess_ms": result.timings.preprocess_ms,
                "inference_ms": result.timings.inference_ms,
                "postprocess_ms": result.timings.postprocess_ms,
                "total_ms": result.timings.total_ms,
                "fallback_used": used_fallback,
                "status": "ok",
            },
        )
        return result
