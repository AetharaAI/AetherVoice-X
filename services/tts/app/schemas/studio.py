from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


VoiceType = Literal["preset", "cloned", "generated", "imported", "fallback"]
RouteTarget = Literal["moss_realtime", "moss_tts", "moss_ttsd", "moss_voice_generator", "chatterbox"]
ProviderName = Literal["openai", "openrouter", "litellm", "anthropic"]


class VoiceRecord(BaseModel):
    voice_id: str
    display_name: str
    tenant_id: str | None = None
    type: VoiceType
    source_model: str
    runtime_target: RouteTarget
    reference_audio_path: str | None = None
    reference_text: str | None = None
    generation_prompt: str | None = None
    sample_rate: int = 24000
    language: str = "en"
    tags: list[str] = Field(default_factory=list)
    default_params: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class VoiceCreateRequest(BaseModel):
    display_name: str
    type: VoiceType
    source_model: str
    runtime_target: RouteTarget
    reference_audio_path: str | None = None
    reference_text: str | None = None
    generation_prompt: str | None = None
    sample_rate: int = 24000
    language: str = "en"
    tags: list[str] = Field(default_factory=list)
    default_params: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class LLMRoutingConfig(BaseModel):
    provider: ProviderName = "litellm"
    model: str | None = None
    base_url: str | None = None
    enabled: bool = False
    mode: Literal["manual", "asr_llm_tts", "shadow"] = "manual"
    system_prompt: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RouteDescriptor(BaseModel):
    name: RouteTarget
    label: str
    mode: Literal["stream", "batch", "dialogue", "voice-design"]
    status: Literal["ready", "configured", "staged", "missing"]
    model_path: str | None = None
    notes: str | None = None
    fallback_target: str | None = None


class ProviderSummary(BaseModel):
    provider: ProviderName
    label: str
    enabled: bool
    base_url: str | None = None
    auth_configured: bool = False
    notes: str | None = None


class ProviderModel(BaseModel):
    id: str
    label: str
    provider: ProviderName


class ExamplePreset(BaseModel):
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)
    generation_prompt: str


class StudioOverview(BaseModel):
    routes: list[RouteDescriptor] = Field(default_factory=list)
    voices: list[VoiceRecord] = Field(default_factory=list)
    providers: list[ProviderSummary] = Field(default_factory=list)
    routing: LLMRoutingConfig = Field(default_factory=LLMRoutingConfig)
    example_presets: list[ExamplePreset] = Field(default_factory=list)
    canonical_model_root: str
