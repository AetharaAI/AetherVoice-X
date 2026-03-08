from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TimingBreakdown(BaseModel):
    queue_ms: int = 0
    inference_ms: int = 0
    encode_ms: int = 0
    total_ms: int = 0


class StreamCompletion(BaseModel):
    model_used: str
    format: str = "wav"
    duration_ms: int = 0
    timings: TimingBreakdown = Field(default_factory=TimingBreakdown)
    artifacts: dict[str, Any] = Field(default_factory=dict)


class TTSResult(BaseModel):
    request_id: str
    model_used: str
    audio_url: str
    duration_ms: int
    timings: TimingBreakdown
    artifacts: dict[str, Any] = Field(default_factory=dict)


class StreamSession(BaseModel):
    session_id: str
    model: str
    expires_in_seconds: int = 3600
