from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .requests import TTSStyle
from .responses import TimingBreakdown


class VoiceTurnRequest(BaseModel):
    request_id: str
    session_id: str | None = None
    tenant_id: str
    transcript_text: str
    voice: str = "default"
    tts_model: str = "kokoro_realtime"
    format: str = "wav"
    sample_rate: int = 24000
    style: TTSStyle = Field(default_factory=TTSStyle)
    metadata: dict[str, Any] = Field(default_factory=dict)


class VoiceTurnTimings(BaseModel):
    llm_ms: int = 0
    tts_ms: int = 0
    total_ms: int = 0


class VoiceTurnResult(BaseModel):
    request_id: str
    transcript_text: str
    response_text: str
    llm_provider: str
    llm_model_requested: str
    llm_model_used: str
    llm_base_url: str | None = None
    llm_request_id: str | None = None
    llm_timings: TimingBreakdown = Field(default_factory=TimingBreakdown)
    tts_model_requested: str
    tts_model_used: str
    audio_url: str
    duration_ms: int
    tts_timings: TimingBreakdown = Field(default_factory=TimingBreakdown)
    timings: VoiceTurnTimings = Field(default_factory=VoiceTurnTimings)
    artifacts: dict[str, Any] = Field(default_factory=dict)
