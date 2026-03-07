from __future__ import annotations

from aether_common.model_aliases import normalize_asr_model_name

from ..adapters.faster_whisper import FasterWhisperAdapter
from ..adapters.qwen3_asr import Qwen3ASRAdapter
from ..adapters.voxtral_realtime import VoxtralRealtimeAdapter
from ..config import get_settings


class ModelRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        voxtral = VoxtralRealtimeAdapter(
            base_url=settings.voxtral_realtime_base_url,
            model_name=settings.voxtral_realtime_model_name or settings.voxtral_model_id,
            api_key=settings.voxtral_realtime_api_key,
            partial_window_ms=settings.voxtral_stream_partial_window_ms,
            timeout_seconds=settings.voxtral_realtime_timeout_seconds,
        )
        self.adapters = {
            "faster_whisper": FasterWhisperAdapter(
                model_source=settings.faster_whisper_model_path or settings.faster_whisper_model_size,
                device=settings.asr_device,
                compute_type=settings.asr_compute_type,
            ),
            "voxtral_realtime": voxtral,
            "qwen3_asr": Qwen3ASRAdapter(),
        }

    def get(self, name: str):
        return self.adapters[normalize_asr_model_name(name)]

    def fallback_batch(self):
        return self.adapters["faster_whisper"]

    def fallback_stream(self):
        if getattr(self.adapters["voxtral_realtime"], "ready", False):
            return self.adapters["voxtral_realtime"]
        return self.adapters["faster_whisper"]

    def model_info(self) -> list[dict]:
        return [
            {
                "name": adapter.name,
                "kind": "asr",
                "supports_streaming": adapter.supports_streaming,
                "supports_batch": adapter.supports_batch,
                "status": "ready" if getattr(adapter, "ready", False) or adapter.name == "faster_whisper" else "scaffold",
                "features": [
                    feature
                    for feature, enabled in (
                        ("timestamps", adapter.supports_timestamps),
                        ("language_detection", adapter.supports_language_detection),
                    )
                    if enabled
                ],
                "route_priority": 10 if adapter.name == "voxtral_realtime" else 20,
                "memory_footprint": "external-service" if adapter.name == "voxtral_realtime" and getattr(adapter, "ready", False) else "model-managed",
            }
            for adapter in self.adapters.values()
        ]
