from __future__ import annotations

from aether_common.model_aliases import normalize_tts_model_name

from ..adapters.chatterbox import ChatterboxAdapter
from ..adapters.kokoro_realtime import KokoroRealtimeAdapter
from ..config import get_settings


class ModelRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        self.adapters = {
            "chatterbox": ChatterboxAdapter(
                settings.chatterbox_base_url,
                default_voice=settings.chatterbox_default_voice,
            ),
            "kokoro_realtime": KokoroRealtimeAdapter(
                base_url=settings.kokoro_realtime_base_url,
                model_name=settings.kokoro_model_id,
                timeout_seconds=settings.kokoro_realtime_timeout_seconds,
            ),
        }

    def get(self, name: str):
        return self.adapters[normalize_tts_model_name(name)]

    def fallback_batch(self):
        return self.adapters["chatterbox"]

    def fallback_stream(self):
        for name in ("kokoro_realtime",):
            adapter = self.adapters.get(name)
            if adapter is not None and (getattr(adapter, "ready", False) or getattr(adapter, "configured", False)):
                return adapter
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
                        else ["realtime", "preset_voices", "adapter_driven_streaming"]
                    ),
                    "route_priority": 5 if adapter.name == "kokoro_realtime" else 30,
                    "memory_footprint": (
                        "external-service"
                        if adapter.name == "kokoro_realtime" and (getattr(adapter, "ready", False) or getattr(adapter, "configured", False))
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
