from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ASRFileRequest(BaseModel):
    request_id: str
    session_id: str
    tenant_id: str
    model: str = "auto"
    task: Literal["transcribe", "translate"] = "transcribe"
    language: str = "auto"
    timestamps: bool = True
    diarization: bool = False
    response_format: str = "json"
    storage_mode: Literal["persist", "ephemeral"] = "persist"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ASRStreamStartRequest(BaseModel):
    request_id: str
    session_id: str
    tenant_id: str
    model: str = "auto"
    language: str = "auto"
    sample_rate: int = 16000
    encoding: str = "pcm_s16le"
    channels: int = 1
    triage_enabled: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AudioFrame(BaseModel):
    type: str = "audio_frame"
    seq: int
    timestamp_ms: int
    sample_rate: int = 16000
    encoding: str = "pcm_s16le"
    channels: int = 1
    payload_b64: str


class ASRTriageRequest(BaseModel):
    session_id: str
    input_mode: str = "transcript_plus_audio"
    model: str = "sentinel"
    domain: str = "electrical_emergency"
    transcript: str
    audio_ref: str | None = None


class ASRAnalyzeRequest(BaseModel):
    session_id: str | None = None
    transcript: str
    metadata: dict[str, Any] = Field(default_factory=dict)
