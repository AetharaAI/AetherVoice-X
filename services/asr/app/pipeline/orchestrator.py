from __future__ import annotations

from .postprocess import clean_transcript


def finalize_text(text: str) -> str:
    return clean_transcript(text)
