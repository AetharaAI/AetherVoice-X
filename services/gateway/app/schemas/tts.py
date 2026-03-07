from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from aether_common.schemas import RequestMetadata, TimingBreakdown


class TTSStyle(BaseModel):
    speed: float = 1.0
    emotion: str = "neutral"
    speaker_hint: str | None = None


class TTSRequest(BaseModel):
    model: str = "auto"
    voice: str = "default"
    text: str
    format: str = "wav"
    sample_rate: int = 24000
    stream: bool = False
    style: TTSStyle = Field(default_factory=TTSStyle)
    metadata: RequestMetadata = Field(default_factory=RequestMetadata)


class TTSResponse(BaseModel):
    request_id: str
    model_used: str
    audio_url: str
    duration_ms: int
    timings: TimingBreakdown


class TTSStreamStartRequest(BaseModel):
    model: str = "moss_realtime"
    voice: str = "default"
    sample_rate: int = 24000
    format: str = "wav"
    context_mode: str = "conversation"
    metadata: RequestMetadata = Field(default_factory=RequestMetadata)


class TTSStreamStartResponse(BaseModel):
    session_id: str
    ws_url: str


class TTSEvent(BaseModel):
    type: str
    session_id: str
    text: str | None = None
    audio_b64: str | None = None
    format: str | None = None
    sequence: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
