from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TTSStyle(BaseModel):
    speed: float = 1.0
    emotion: str = "neutral"
    speaker_hint: str | None = None


class TTSRequest(BaseModel):
    request_id: str
    session_id: str | None = None
    tenant_id: str
    model: str = "auto"
    voice: str = "default"
    text: str
    format: str = "wav"
    sample_rate: int = 24000
    stream: bool = False
    style: TTSStyle = Field(default_factory=TTSStyle)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TTSStreamStartRequest(BaseModel):
    request_id: str
    session_id: str
    tenant_id: str
    model: str = "moss_realtime"
    voice: str = "default"
    sample_rate: int = 24000
    format: str = "wav"
    context_mode: str = "conversation"
    metadata: dict[str, Any] = Field(default_factory=dict)
