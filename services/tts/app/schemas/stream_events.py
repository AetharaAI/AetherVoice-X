from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AudioChunkEvent(BaseModel):
    type: Literal["audio_chunk"] = "audio_chunk"
    session_id: str
    sequence: int
    audio_b64: str
    format: str = "wav"
    metadata: dict[str, Any] = Field(default_factory=dict)


class FinalAudioEvent(BaseModel):
    type: Literal["final_audio"] = "final_audio"
    session_id: str
    audio_b64: str
    format: str = "wav"
    metadata: dict[str, Any] = Field(default_factory=dict)
