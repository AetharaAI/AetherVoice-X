from __future__ import annotations

from aether_common.model_aliases import normalize_tts_model_name

from ..adapters.chatterbox import ChatterboxAdapter
from ..adapters.moss_realtime import MossRealtimeAdapter
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
        return [
            {
                "name": adapter.name,
                "kind": "tts",
                "supports_streaming": adapter.supports_streaming,
                "supports_batch": adapter.supports_batch,
                "status": (
                    "ready"
                    if adapter.name == "chatterbox" or getattr(adapter, "ready", False)
                    else "unavailable"
                ),
                "features": ["http_passthrough"] if adapter.name == "chatterbox" else ["realtime", "adapter_driven_streaming"],
                "route_priority": 10 if adapter.name == "moss_realtime" else 20,
                "memory_footprint": (
                    "external-service"
                    if adapter.name == "moss_realtime" and (getattr(adapter, "ready", False) or getattr(adapter, "configured", False))
                    else ("external" if adapter.name == "chatterbox" else "scaffold")
                ),
            }
            for adapter in self.adapters.values()
        ]

    async def close(self) -> None:
        for adapter in self.adapters.values():
            close = getattr(adapter, "close", None)
            if close is not None:
                await close()
