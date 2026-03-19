from __future__ import annotations

from aether_common.model_aliases import normalize_tts_model_name

from ..adapters.chatterbox import ChatterboxAdapter
from ..adapters.kokoro_realtime import KokoroRealtimeAdapter
from ..adapters.qwen_customvoice import QwenCustomVoiceAdapter
from ..adapters.qwen_customvoice_streaming import QwenCustomVoiceStreamingAdapter
from ..config import get_settings


class ModelRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        self.adapters = {
            "chatterbox": ChatterboxAdapter(
                settings.chatterbox_base_url,
                default_voice=settings.chatterbox_default_voice,
            ),
            "qwen_customvoice": QwenCustomVoiceAdapter(
                base_url=settings.qwen_provider_base_url,
                model_name=settings.qwen_provider_model_alias,
                default_voice=settings.qwen_provider_default_voice,
                default_language=settings.qwen_provider_default_language,
                timeout_seconds=settings.qwen_provider_timeout_seconds,
            ),
            "qwen_customvoice_streaming": QwenCustomVoiceStreamingAdapter(
                base_url=settings.qwen_provider_base_url,
                model_name=settings.qwen_provider_streaming_model_alias,
                default_voice=settings.qwen_provider_default_voice,
                default_language=settings.qwen_provider_default_language,
                timeout_seconds=settings.qwen_provider_timeout_seconds,
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
        preferred = self.adapters.get("qwen_customvoice")
        if preferred is not None and (getattr(preferred, "ready", False) or getattr(preferred, "configured", False)):
            return preferred
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
                        else (
                            ["provider_http", "batch", "builtin_qwen_voices", "instruction_control"]
                            if adapter.name == "qwen_customvoice"
                            else (
                                ["provider_http", "streaming", "builtin_qwen_voices", "provider_incremental_stream"]
                                if adapter.name == "qwen_customvoice_streaming"
                                else ["realtime", "preset_voices", "adapter_driven_streaming"]
                            )
                        )
                    ),
                    "route_priority": (
                        5
                        if adapter.name == "kokoro_realtime"
                        else (10 if adapter.name == "qwen_customvoice_streaming" else (15 if adapter.name == "qwen_customvoice" else 30))
                    ),
                    "memory_footprint": (
                        "external-service"
                        if adapter.name in {"kokoro_realtime", "qwen_customvoice", "qwen_customvoice_streaming"} and (getattr(adapter, "ready", False) or getattr(adapter, "configured", False))
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
