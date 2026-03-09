from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TimingBreakdown(BaseModel):
    queue_ms: int = 0
    inference_ms: int = 0
    encode_ms: int = 0
    total_ms: int = 0


class StreamRuntimeTruth(BaseModel):
    requested_route: str | None = None
    runtime_path_used: str
    live_chunk_source_route: str
    final_artifact_source_route: str
    selected_voice_id: str | None = None
    selected_voice_asset: str | None = None
    requested_preset: str | None = None
    resolved_conditioning_asset: str | None = None
    actual_runtime_conditioning_source: str
    conditioning_active: bool = False
    fallback_route_used: str | None = None
    fallback_voice_path: str | None = None
    notes: list[str] = Field(default_factory=list)


class StreamCompletion(BaseModel):
    model_used: str
    format: str = "wav"
    duration_ms: int = 0
    timings: TimingBreakdown = Field(default_factory=TimingBreakdown)
    artifacts: dict[str, Any] = Field(default_factory=dict)
    runtime: StreamRuntimeTruth | None = None


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
    fallback_used: bool = False
    runtime: StreamRuntimeTruth | None = None
