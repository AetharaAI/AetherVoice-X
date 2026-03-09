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
    "moss_tts": "moss_tts",
    "moss-tts": "moss_tts",
    "openmoss-team/moss-tts": "moss_tts",
    "moss_ttsd": "moss_ttsd",
    "moss-ttsd": "moss_ttsd",
    "moss-ttsd-v1.0": "moss_ttsd",
    "openmoss-team/moss-ttsd-v1.0": "moss_ttsd",
    "moss_voice_generator": "moss_voice_generator",
    "moss-voice-generator": "moss_voice_generator",
    "openmoss-team/moss-voicegenerator": "moss_voice_generator",
    "moss_soundeffect": "moss_soundeffect",
    "moss-soundeffect": "moss_soundeffect",
    "moss_sound_effect": "moss_soundeffect",
    "moss-sound-effect": "moss_soundeffect",
    "openmoss-team/moss-soundeffect": "moss_soundeffect",
}


def normalize_asr_model_name(name: str) -> str:
    return ASR_MODEL_ALIASES.get(name.strip().lower(), name)


def normalize_tts_model_name(name: str) -> str:
    return TTS_MODEL_ALIASES.get(name.strip().lower(), name)
