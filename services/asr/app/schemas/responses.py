from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TimingBreakdown(BaseModel):
    queue_ms: int = 0
    preprocess_ms: int = 0
    inference_ms: int = 0
    postprocess_ms: int = 0
    total_ms: int = 0


class ASRSegment(BaseModel):
    segment_id: str
    start_ms: int
    end_ms: int
    text: str
    confidence: float | None = None


class ASRResult(BaseModel):
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
    artifacts: dict[str, Any] = Field(default_factory=dict)


class StreamSession(BaseModel):
    session_id: str
    model: str
    expires_in_seconds: int = 3600


class TriageResult(BaseModel):
    request_id: str
    classification: str
    priority: float
    analysis: str
    recommended_action: str
    requires_human_review: bool = True


class AnalyzeResult(BaseModel):
    request_id: str
    keywords: list[str] = Field(default_factory=list)
    speaking_rate_wpm: int = 0
    summary: str
