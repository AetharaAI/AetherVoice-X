from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PartialTranscriptEvent(BaseModel):
    type: Literal["partial_transcript"] = "partial_transcript"
    session_id: str
    seq: int
    stable: bool = False
    text: str
    start_ms: int = 0
    end_ms: int = 0


class FinalTranscriptEvent(BaseModel):
    type: Literal["final_transcript"] = "final_transcript"
    session_id: str
    stable: bool = True
    text: str
    segments: list[dict] = Field(default_factory=list)


class StreamErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    session_id: str
    detail: str
