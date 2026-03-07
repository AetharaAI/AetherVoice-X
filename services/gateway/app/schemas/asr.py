from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from aether_common.schemas import RequestMetadata, TimingBreakdown


class ASRTranscribeRequest(BaseModel):
    model: str = "auto"
    task: Literal["transcribe", "translate"] = "transcribe"
    language: str = "auto"
    timestamps: bool = True
    diarization: bool = False
    response_format: str = "json"
    storage_mode: Literal["persist", "ephemeral"] = "persist"
    metadata: RequestMetadata = Field(default_factory=RequestMetadata)
    audio_url: str | None = None


class ASRSegment(BaseModel):
    segment_id: str
    start_ms: int
    end_ms: int
    text: str
    confidence: float | None = None


class ASRTranscribeResponse(BaseModel):
    request_id: str
    session_id: str
    task: str
    model_requested: str
    model_used: str
    language_detected: str | None = None
    duration_ms: int = 0
    text: str
    segments: list[ASRSegment] = Field(default_factory=list)
    timings: TimingBreakdown


class ASRStreamStartRequest(BaseModel):
    model: str = "auto"
    language: str = "auto"
    sample_rate: int = 16000
    encoding: str = "pcm_s16le"
    channels: int = 1
    triage_enabled: bool = False
    metadata: RequestMetadata = Field(default_factory=RequestMetadata)


class ASRStreamStartResponse(BaseModel):
    session_id: str
    ws_url: str
    expires_in_seconds: int = 3600


class ASRTriageRequest(BaseModel):
    session_id: str
    input_mode: Literal["transcript", "audio", "transcript_plus_audio"] = "transcript_plus_audio"
    model: str = "sentinel"
    domain: str = "electrical_emergency"
    transcript: str
    audio_ref: str | None = None


class ASRTriageResponse(BaseModel):
    request_id: str
    classification: str
    priority: float
    analysis: str
    recommended_action: str
    requires_human_review: bool = True


class ASRAnalyzeRequest(BaseModel):
    session_id: str | None = None
    transcript: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ASRAnalyzeResponse(BaseModel):
    request_id: str
    keywords: list[str] = Field(default_factory=list)
    speaking_rate_wpm: int = 0
    summary: str
