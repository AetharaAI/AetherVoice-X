from __future__ import annotations

import io
import wave
from typing import Any

from aether_common.storage import StorageManager
from aether_common.telemetry import voice_model_fallback_total

from ..logging import logger
from ..adapters.base import BatchSynthesisResult
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
    def _adapter_runtime_truth(adapter: Any) -> dict[str, str]:
        return {
            "adapter_name": str(getattr(adapter, "name", adapter.__class__.__name__)),
            "adapter_kind": adapter.__class__.__name__,
            "adapter_base_url": str(getattr(adapter, "base_url", "") or ""),
            "adapter_configured": "true" if bool(getattr(adapter, "configured", False)) else "false",
            "adapter_ready": "true" if bool(getattr(adapter, "ready", False)) else "false",
        }

    @staticmethod
    def _coerce_batch_result(result: BatchSynthesisResult | tuple[bytes, str]) -> BatchSynthesisResult:
        if isinstance(result, BatchSynthesisResult):
            return result
        audio_bytes, output_format = result
        return BatchSynthesisResult(audio_bytes=audio_bytes, output_format=output_format)

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
        existing_extra = dict(metadata.get("extra") or {}) if isinstance(metadata.get("extra"), dict) else {}
        metadata["extra"] = {
            **existing_extra,
            **self._resolve_voice_metadata(request),
        }
        prepared = request.model_copy(update={"text": text, "voice": voice, "metadata": metadata})
        try:
            adapter = self.registry.get(request.model)
        except KeyError:
            adapter = self.registry.fallback_batch()
        requested_adapter = adapter
        requested_adapter_truth = self._adapter_runtime_truth(requested_adapter)
        selected_voice = (prepared.metadata.get("extra") or {}).get("resolved_voice") if isinstance(prepared.metadata, dict) else None
        fallback_route_used: str | None = None
        fallback_reason: str | None = None
        fallback_exception_type: str | None = None
        fallback_exception_message: str | None = None
        try:
            batch_result = self._coerce_batch_result(await adapter.synthesize(prepared))
        except Exception as exc:
            fallback_exception_type = exc.__class__.__name__
            fallback_exception_message = str(exc)
            if adapter.name != "chatterbox":
                fallback = self.registry.fallback_batch()
                voice_model_fallback_total.labels(service="tts", requested=request.model, used=fallback.name).inc()
                fallback_voice, fallback_metadata = self._chatterbox_safe_voice(prepared)
                batch_result = self._coerce_batch_result(await fallback.synthesize(
                    prepared.model_copy(
                        update={
                            "model": fallback.name,
                            "voice": fallback_voice,
                            "metadata": fallback_metadata,
                        }
                    )
                ))
                fallback_route_used = fallback.name
                fallback_reason = f"{requested_adapter.name} synthesize failed"
                adapter = fallback
            else:
                raise exc
        audio_bytes = batch_result.audio_bytes
        output_format = batch_result.output_format
        resolved_adapter_truth = self._adapter_runtime_truth(adapter)
        upstream_artifacts = dict(batch_result.artifacts or {})
        model_used = str(batch_result.model_used or adapter.name)
        duration_ms = self._estimate_duration_ms(audio_bytes)
        key = f"tts/{request.tenant_id}/{request.session_id or 'no-session'}/{request.request_id}.{output_format}"
        audio_url = self.storage.upload_bytes(self.settings.s3_bucket_tts, key, audio_bytes, f"audio/{output_format}")
        total_ms = int((__import__("time").perf_counter() - started) * 1000)
        timings = TimingBreakdown(
            inference_ms=int(batch_result.timings.get("inference_ms") or total_ms),
            encode_ms=int(batch_result.timings.get("encode_ms") or 0),
            total_ms=int(batch_result.timings.get("total_ms") or total_ms),
        )
        runtime_truth = {
            "request_id": request.request_id,
            "session_id": request.session_id or "",
            "requested_model": request.model,
            "requested_voice_id": request.voice,
            "runtime_path_used": str(upstream_artifacts.get("runtime_path_used") or model_used),
            "requested_adapter_name": requested_adapter_truth["adapter_name"],
            "requested_adapter_kind": requested_adapter_truth["adapter_kind"],
            "requested_adapter_base_url": requested_adapter_truth["adapter_base_url"],
            "requested_adapter_configured": requested_adapter_truth["adapter_configured"],
            "requested_adapter_ready": requested_adapter_truth["adapter_ready"],
            "resolved_adapter_name": resolved_adapter_truth["adapter_name"],
            "resolved_adapter_kind": resolved_adapter_truth["adapter_kind"],
            "resolved_adapter_base_url": resolved_adapter_truth["adapter_base_url"],
            "resolved_adapter_configured": resolved_adapter_truth["adapter_configured"],
            "resolved_adapter_ready": resolved_adapter_truth["adapter_ready"],
            "resolved_voice_id": str(selected_voice.get("voice_id") or prepared.voice) if isinstance(selected_voice, dict) else prepared.voice,
            "resolved_voice_asset": str(selected_voice.get("display_name") or prepared.voice) if isinstance(selected_voice, dict) else prepared.voice,
            "resolved_voice_runtime_target": str(selected_voice.get("runtime_target") or "") if isinstance(selected_voice, dict) else "",
            "resolved_voice_source_model": str(selected_voice.get("source_model") or "") if isinstance(selected_voice, dict) else "",
            "resolved_reference_audio_path": str(
                upstream_artifacts.get("original_reference_audio_path")
                or upstream_artifacts.get("resolved_conditioning_asset")
                or (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                or ""
            ),
            "normalized_reference_audio_path": str(upstream_artifacts.get("normalized_reference_audio_path") or ""),
            "actual_runtime_conditioning_source": str(
                upstream_artifacts.get("actual_runtime_conditioning_source")
                or (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                or (prepared.metadata.get("extra") or {}).get("generation_prompt")
                or "default"
            ),
            "fallback_route_used": fallback_route_used or "",
            "fallback_reason": fallback_reason or "",
            "fallback_exception_type": fallback_exception_type or "",
            "fallback_exception_message": fallback_exception_message or "",
        }
        logger.info(
            "tts_completed",
            extra={
                "request_id": request.request_id,
                "session_id": request.session_id,
                "route": "/internal/synthesize",
                "tenant_id": request.tenant_id,
                "model_requested": request.model,
                "model_used": model_used,
                "total_ms": timings.total_ms,
                "status": "ok",
            },
        )
        logger.info("tts_runtime_truth", extra=runtime_truth)
        return (
            TTSResult(
                request_id=request.request_id,
                model_used=model_used,
                audio_url=audio_url,
                duration_ms=duration_ms,
                timings=timings,
                artifacts={
                    **upstream_artifacts,
                    "format": output_format,
                    "selected_voice_id": selected_voice.get("voice_id") if isinstance(selected_voice, dict) else prepared.voice,
                    "selected_voice_asset": selected_voice.get("display_name") if isinstance(selected_voice, dict) else prepared.voice,
                    "resolved_conditioning_asset": upstream_artifacts.get("resolved_conditioning_asset")
                    or (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                    or (prepared.metadata.get("extra") or {}).get("generation_prompt"),
                    "actual_runtime_conditioning_source": upstream_artifacts.get("actual_runtime_conditioning_source")
                    or (prepared.metadata.get("extra") or {}).get("reference_audio_path")
                    or (prepared.metadata.get("extra") or {}).get("generation_prompt")
                    or "default",
                    "fallback_route_used": fallback_route_used,
                    "fallback_reason": fallback_reason or "",
                    "fallback_exception_type": fallback_exception_type or "",
                    "fallback_exception_message": fallback_exception_message or "",
                    "requested_model": request.model,
                    **runtime_truth,
                },
            ),
            audio_bytes,
        )
