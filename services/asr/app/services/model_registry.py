from __future__ import annotations

from aether_common.model_aliases import normalize_asr_model_name

from ..adapters.faster_whisper import FasterWhisperAdapter
from ..adapters.qwen3_asr import Qwen3ASRAdapter
from ..adapters.voxtral_realtime import VoxtralRealtimeAdapter
from ..config import get_settings


class ModelRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        self.adapters = {
            "faster_whisper": FasterWhisperAdapter(
                model_source=settings.faster_whisper_model_path or settings.faster_whisper_model_size,
                device=settings.asr_device,
                compute_type=settings.asr_compute_type,
            ),
            "voxtral_realtime": VoxtralRealtimeAdapter(),
            "qwen3_asr": Qwen3ASRAdapter(),
        }

    def get(self, name: str):
        return self.adapters[normalize_asr_model_name(name)]

    def fallback_batch(self):
        return self.adapters["faster_whisper"]

    def fallback_stream(self):
        return self.adapters["faster_whisper"]

    def model_info(self) -> list[dict]:
        return [
            {
                "name": adapter.name,
                "kind": "asr",
                "supports_streaming": adapter.supports_streaming,
                "supports_batch": adapter.supports_batch,
                "status": "ready" if adapter.name == "faster_whisper" else "scaffold",
                "features": [
                    feature
                    for feature, enabled in (
                        ("timestamps", adapter.supports_timestamps),
                        ("language_detection", adapter.supports_language_detection),
                    )
                    if enabled
                ],
                "route_priority": 10 if adapter.name == "voxtral_realtime" else 20,
                "memory_footprint": "model-managed",
            }
            for adapter in self.adapters.values()
        ]
