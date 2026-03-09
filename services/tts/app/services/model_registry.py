from __future__ import annotations

from aether_common.model_aliases import normalize_tts_model_name

from ..adapters.chatterbox import ChatterboxAdapter
from ..adapters.moss_realtime import MossRealtimeAdapter
from ..adapters.openmoss_batch import OpenMOSSBatchAdapter
from ..config import get_settings


class ModelRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        self.adapters = {
            "chatterbox": ChatterboxAdapter(
                settings.chatterbox_base_url,
                default_voice=settings.chatterbox_default_voice,
            ),
            "moss_realtime": MossRealtimeAdapter(
                base_url=settings.moss_realtime_base_url,
                model_name=settings.moss_model_id,
                timeout_seconds=settings.moss_realtime_timeout_seconds,
            ),
            "moss_tts": OpenMOSSBatchAdapter(
                name="moss_tts",
                base_url=settings.moss_tts_base_url,
                timeout_seconds=settings.moss_tts_timeout_seconds,
            ),
            "moss_ttsd": OpenMOSSBatchAdapter(
                name="moss_ttsd",
                base_url=settings.moss_ttsd_base_url,
                timeout_seconds=settings.moss_ttsd_timeout_seconds,
            ),
            "moss_voice_generator": OpenMOSSBatchAdapter(
                name="moss_voice_generator",
                base_url=settings.moss_voice_generator_base_url,
                timeout_seconds=settings.moss_voice_generator_timeout_seconds,
            ),
            "moss_soundeffect": OpenMOSSBatchAdapter(
                name="moss_soundeffect",
                base_url=settings.moss_soundeffect_base_url,
                timeout_seconds=settings.moss_soundeffect_timeout_seconds,
            ),
        }

    def get(self, name: str):
        return self.adapters[normalize_tts_model_name(name)]

    def fallback_batch(self):
        return self.adapters["chatterbox"]

    def fallback_stream(self):
        moss = self.adapters.get("moss_realtime")
        if moss is not None and (getattr(moss, "ready", False) or getattr(moss, "configured", False)):
            return moss
        return self.adapters["chatterbox"]

    def model_info(self) -> list[dict]:
        models: list[dict] = []
        for adapter in self.adapters.values():
            refresh = getattr(adapter, "refresh_health", None)
            if callable(refresh):
                refresh()
            models.append(
                {
                    "name": adapter.name,
                    "kind": "tts",
                    "supports_streaming": adapter.supports_streaming,
                    "supports_batch": adapter.supports_batch,
                    "status": (
                        "ready"
                        if (adapter.name == "chatterbox" or getattr(adapter, "ready", False))
                        else ("configured" if getattr(adapter, "configured", False) else "unavailable")
                    ),
                    "features": (
                        ["http_passthrough"]
                        if adapter.name == "chatterbox"
                        else (["realtime", "adapter_driven_streaming"] if adapter.name == "moss_realtime" else ["openmoss", "batch_http"])
                    ),
                    "route_priority": (
                        10
                        if adapter.name == "moss_realtime"
                        else (15 if adapter.name == "moss_tts" else (16 if adapter.name == "moss_ttsd" else (17 if adapter.name == "moss_voice_generator" else 30)))
                    ),
                    "memory_footprint": (
                        "external-service"
                        if adapter.name == "moss_realtime" and (getattr(adapter, "ready", False) or getattr(adapter, "configured", False))
                        else ("external" if adapter.name == "chatterbox" else "external-service")
                    ),
                }
            )
        return models

    async def close(self) -> None:
        for adapter in self.adapters.values():
            close = getattr(adapter, "close", None)
            if close is not None:
                await close()
