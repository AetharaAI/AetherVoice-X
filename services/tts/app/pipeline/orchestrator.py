from .text_normalize import prepare_text
from .voice_resolver import resolve_voice


def build_input(text: str, voice: str) -> tuple[str, str]:
    return prepare_text(text), resolve_voice(voice)
