from __future__ import annotations


ASR_MODEL_ALIASES = {
    "faster_whisper": "faster_whisper",
    "faster-whisper": "faster_whisper",
    "faster-whisper-large-v3": "faster_whisper",
    "voxtral_realtime": "voxtral_realtime",
    "voxtral-realtime": "voxtral_realtime",
    "voxtral-mini-4b-realtime-2602": "voxtral_realtime",
    "qwen3_asr": "qwen3_asr",
    "qwen3-asr": "qwen3_asr",
    "qwen/qwen3-asr-1.7b": "qwen3_asr",
}

TTS_MODEL_ALIASES = {
    "chatterbox": "chatterbox",
    "moss_realtime": "moss_realtime",
    "moss-realtime": "moss_realtime",
    "moss-tts-realtime": "moss_realtime",
    "openmoss-team/moss-tts-realtime": "moss_realtime",
}


def normalize_asr_model_name(name: str) -> str:
    return ASR_MODEL_ALIASES.get(name.strip().lower(), name)


def normalize_tts_model_name(name: str) -> str:
    return TTS_MODEL_ALIASES.get(name.strip().lower(), name)
