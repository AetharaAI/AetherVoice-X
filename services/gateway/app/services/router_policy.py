from __future__ import annotations

from aether_common.model_aliases import normalize_asr_model_name, normalize_tts_model_name
from aether_common.settings import Settings


def choose_asr_model(
    requested: str,
    *,
    streaming: bool,
    language: str,
    task: str = "transcribe",
    triage_enabled: bool = False,
    settings: Settings,
) -> str:
    if requested and requested != "auto":
        return normalize_asr_model_name(requested)
    if task == "triage" or triage_enabled:
        return "voxtral_realtime" if streaming else normalize_asr_model_name(settings.default_batch_asr_model)
    if streaming:
        return normalize_asr_model_name(settings.default_asr_model)
    if language != "auto" and language != "en" and settings.enable_qwen3_asr:
        return "qwen3_asr"
    return normalize_asr_model_name(settings.default_batch_asr_model)


def choose_tts_model(requested: str, *, streaming: bool, context_mode: str, settings: Settings) -> str:
    if requested and requested != "auto":
        return normalize_tts_model_name(requested)
    if streaming and context_mode == "conversation":
        return normalize_tts_model_name(settings.default_stream_tts_model)
    return normalize_tts_model_name(settings.default_tts_model)
