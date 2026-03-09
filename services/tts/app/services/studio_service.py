from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx

from ..schemas.studio import (
    ExamplePreset,
    LLMRoutingConfig,
    ProviderModel,
    ProviderSummary,
    RouteDescriptor,
    StudioOverview,
    VoiceCreateRequest,
    VoiceRecord,
)


EXAMPLE_PRESETS = [
    ExamplePreset(
        title="Warm female dispatcher",
        description="Calm service voice for phone-based resolution and ETA updates.",
        tags=["telephony", "warm", "dispatcher"],
        generation_prompt="Warm female dispatcher voice with calm authority, clean articulation, and telephony-friendly pacing.",
    ),
    ExamplePreset(
        title="Calm documentary narrator",
        description="Neutral, polished narration for explainer or documentary reads.",
        tags=["narration", "calm", "documentary"],
        generation_prompt="Calm documentary narrator with polished diction, medium pace, and gentle authority.",
    ),
    ExamplePreset(
        title="Gritty field technician",
        description="Blue-collar service voice with slight rasp and practical energy.",
        tags=["service", "field", "gritty"],
        generation_prompt="Gritty field technician voice with slight rasp, practical tone, and confident service cadence.",
    ),
    ExamplePreset(
        title="Noir detective monologue",
        description="Moody late-night narration voice with cinematic delivery.",
        tags=["noir", "monologue", "cinematic"],
        generation_prompt="Noir detective monologue voice with smoky texture, reflective pacing, and cinematic emphasis.",
    ),
    ExamplePreset(
        title="Stoic motivational narrator",
        description="Controlled inspirational voice for training and guidance content.",
        tags=["motivational", "stoic", "narration"],
        generation_prompt="Stoic motivational narrator with controlled intensity, crisp pacing, and grounded conviction.",
    ),
    ExamplePreset(
        title="Scientific abstract reader",
        description="Precise academic voice for technical summaries and papers.",
        tags=["scientific", "academic", "technical"],
        generation_prompt="Scientific abstract reader with precise diction, measured rhythm, and neutral academic tone.",
    ),
    ExamplePreset(
        title="Children's story narrator",
        description="Bright, friendly storytelling voice for family content.",
        tags=["children", "story", "friendly"],
        generation_prompt="Children's story narrator with bright warmth, playful cadence, and clear expressive delivery.",
    ),
    ExamplePreset(
        title="Fairy tale villain monologue",
        description="Stylized dramatic voice for theatrical character work.",
        tags=["villain", "fantasy", "dramatic"],
        generation_prompt="Fairy tale villain monologue voice with theatrical menace, elegant diction, and dramatic pauses.",
    ),
]


PROVIDER_LABELS = {
    "openai": "OpenAI",
    "openrouter": "OpenRouter",
    "litellm": "LiteLLM",
    "anthropic": "Anthropic",
}


class StudioService:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.base_dir = Path(settings.local_storage_root) / "tts-studio"
        self.asset_dir = self.base_dir / "voice-assets"
        self.registry_path = self.base_dir / "voice-registry.json"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self._write_registry(
                {
                    "voices": [voice.model_dump() for voice in self._seed_voices()],
                    "routing": LLMRoutingConfig(
                        provider="litellm",
                        base_url=self.settings.studio_litellm_base_url,
                        enabled=bool(self.settings.studio_litellm_base_url),
                        mode="manual",
                    ).model_dump(),
                }
            )

    def _seed_voices(self) -> list[VoiceRecord]:
        return [
            VoiceRecord(
                voice_id="moss_default",
                display_name="MOSS Default Voice",
                type="preset",
                source_model="moss_realtime",
                runtime_target="moss_realtime",
                tags=["openmoss", "default", "realtime"],
                notes="Baseline OpenMOSS realtime voice binding until custom conditioning is attached.",
            ),
            VoiceRecord(
                voice_id="chatterbox_default",
                display_name=self.settings.chatterbox_default_voice.rsplit(".", 1)[0],
                type="fallback",
                source_model="chatterbox",
                runtime_target="chatterbox",
                reference_audio_path=self.settings.chatterbox_default_voice,
                tags=["chatterbox", "fallback", "batch"],
                notes="Existing Chatterbox fallback voice preserved for stable batch output.",
            ),
        ]

    def _read_registry(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def _write_registry(self, payload: dict[str, Any]) -> None:
        self.registry_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _canonical_model_path(self, leaf: str) -> Path:
        return Path(self.settings.openmoss_model_root) / leaf

    def _container_model_path(self, leaf: str) -> Path:
        return Path(self.settings.aether_model_root) / "audio" / "OpenMOSS-Team" / leaf

    def _model_candidates(self, leaf: str) -> list[Path]:
        canonical_root = Path(self.settings.openmoss_model_root)
        host_root = Path(self.settings.host_model_root)
        container_root = Path(self.settings.aether_model_root)
        candidates: list[Path] = [canonical_root / leaf]

        try:
            relative_root = canonical_root.relative_to(host_root)
        except ValueError:
            relative_root = None

        if relative_root is not None:
            candidates.append(container_root / relative_root / leaf)

        candidates.append(self._container_model_path(leaf))

        deduped: list[Path] = []
        seen: set[str] = set()
        for candidate in candidates:
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(candidate)
        return deduped

    def _model_exists(self, leaf: str) -> bool:
        return any(candidate.exists() for candidate in self._model_candidates(leaf))

    def _route_status(self, leaf: str, *, requires_endpoint: bool = False, endpoint: str | None = None) -> str:
        model_exists = self._model_exists(leaf)
        if requires_endpoint:
            if model_exists and endpoint:
                return "ready"
            if model_exists:
                return "configured"
            return "missing"
        if model_exists:
            return "configured"
        return "missing"

    def _route_catalog(self) -> list[RouteDescriptor]:
        return [
            RouteDescriptor(
                name="moss_realtime",
                label="OpenMOSS Realtime",
                mode="stream",
                status=self._route_status("MOSS-TTS-Realtime", requires_endpoint=True, endpoint=self.settings.moss_realtime_base_url),
                model_path=str(self._canonical_model_path("MOSS-TTS-Realtime")),
                notes="Live agent lane with session-bound streaming.",
                fallback_target="chatterbox",
            ),
            RouteDescriptor(
                name="moss_tts",
                label="OpenMOSS TTS",
                mode="batch",
                status=self._route_status("MOSS-TTS"),
                model_path=str(self._canonical_model_path("MOSS-TTS")),
                notes="Premium single-speaker batch narration and cloning lane.",
                fallback_target="chatterbox",
            ),
            RouteDescriptor(
                name="moss_ttsd",
                label="OpenMOSS TTSD",
                mode="dialogue",
                status=self._route_status("MOSS-TTSD-v1.0"),
                model_path=str(self._canonical_model_path("MOSS-TTSD-v1.0")),
                notes="Multi-speaker dialogue and scripted scene generation.",
                fallback_target="chatterbox",
            ),
            RouteDescriptor(
                name="moss_voice_generator",
                label="OpenMOSS Voice Generator",
                mode="voice-design",
                status=self._route_status("MOSS-VoiceGenerator"),
                model_path=str(self._canonical_model_path("MOSS-VoiceGenerator")),
                notes="Text-described voice design. Save generated personas into the voice library.",
            ),
            RouteDescriptor(
                name="chatterbox",
                label="Chatterbox Fallback",
                mode="batch",
                status="ready" if self.settings.chatterbox_base_url else "configured",
                model_path=None,
                notes="Existing stable batch fallback preserved for compatibility.",
            ),
        ]

    def _provider_config(self, provider: str) -> tuple[str | None, str | None, dict[str, str], str | None]:
        if provider == "openai":
            base_url = self.settings.studio_openai_base_url
            api_key = self.settings.studio_openai_api_key
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            return base_url, api_key, headers, "Standard OpenAI-compatible /models discovery."
        if provider == "openrouter":
            base_url = self.settings.studio_openrouter_base_url
            api_key = self.settings.studio_openrouter_api_key
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            return base_url, api_key, headers, "OpenRouter /models discovery through backend-held auth."
        if provider == "litellm":
            base_url = self.settings.studio_litellm_base_url
            api_key = self.settings.studio_litellm_api_key
            header_name = self.settings.studio_litellm_auth_header or "Authorization"
            headers = {header_name: f"Bearer {api_key}" if header_name.lower() == "authorization" and api_key else (api_key or "")}
            headers = {key: value for key, value in headers.items() if value}
            return base_url, api_key, headers, "Internal LiteLLM or proxy gateway model discovery."
        return None, None, {}, "Anthropic is stubbed for this pass."

    def list_providers(self) -> list[ProviderSummary]:
        providers: list[ProviderSummary] = []
        for provider in ("openai", "openrouter", "litellm", "anthropic"):
            base_url, api_key, _headers, notes = self._provider_config(provider)
            providers.append(
                ProviderSummary(
                    provider=provider,
                    label=PROVIDER_LABELS[provider],
                    enabled=bool(base_url) or provider == "anthropic",
                    base_url=base_url,
                    auth_configured=bool(api_key) or provider == "anthropic",
                    notes=notes,
                )
            )
        return providers

    async def list_provider_models(self, provider: str) -> list[ProviderModel]:
        if provider == "anthropic":
            return []
        base_url, _api_key, headers, _notes = self._provider_config(provider)
        if not base_url:
            return []
        async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=20.0) as client:
            response = await client.get("/models", headers=headers)
            response.raise_for_status()
            payload = response.json()
        records = payload.get("data") if isinstance(payload, dict) else payload
        if isinstance(payload, dict) and "models" in payload and isinstance(payload["models"], list):
            records = payload["models"]
        models: list[ProviderModel] = []
        if isinstance(records, list):
            for entry in records:
                if isinstance(entry, str):
                    models.append(ProviderModel(id=entry, label=entry, provider=provider))
                    continue
                if not isinstance(entry, dict):
                    continue
                model_id = str(entry.get("id") or entry.get("name") or "")
                if not model_id:
                    continue
                models.append(
                    ProviderModel(
                        id=model_id,
                        label=str(entry.get("name") or entry.get("id")),
                        provider=provider,
                    )
                )
        return sorted(models, key=lambda item: item.label.lower())

    def list_voices(self, tenant_id: str) -> list[VoiceRecord]:
        registry = self._read_registry()
        voices = [VoiceRecord.model_validate(entry) for entry in registry.get("voices", [])]
        filtered = [voice for voice in voices if voice.tenant_id in {None, tenant_id}]
        return sorted(filtered, key=lambda voice: (voice.type, voice.display_name.lower()))

    def create_voice(self, tenant_id: str, payload: VoiceCreateRequest) -> VoiceRecord:
        registry = self._read_registry()
        voice = VoiceRecord(
            voice_id=self._slugify(payload.display_name),
            tenant_id=tenant_id,
            **payload.model_dump(),
        )
        registry.setdefault("voices", []).append(voice.model_dump())
        self._write_registry(registry)
        return voice

    def import_voice_asset(
        self,
        *,
        tenant_id: str,
        filename: str,
        payload: bytes,
        display_name: str,
        source_model: str,
        runtime_target: str,
        notes: str | None,
        tags: list[str],
    ) -> VoiceRecord:
        suffix = Path(filename).suffix or ".wav"
        voice_id = self._slugify(display_name)
        asset_path = self.asset_dir / f"{voice_id}-{uuid4().hex[:10]}{suffix}"
        asset_path.write_bytes(payload)
        return self.create_voice(
            tenant_id,
            VoiceCreateRequest(
                display_name=display_name,
                type="imported" if source_model == "imported" else "cloned",
                source_model=source_model,
                runtime_target=runtime_target,
                reference_audio_path=asset_path.as_posix(),
                tags=tags,
                notes=notes,
            ),
        )

    def get_routing(self) -> LLMRoutingConfig:
        registry = self._read_registry()
        return LLMRoutingConfig.model_validate(registry.get("routing") or {})

    def save_routing(self, payload: LLMRoutingConfig) -> LLMRoutingConfig:
        registry = self._read_registry()
        registry["routing"] = payload.model_dump()
        self._write_registry(registry)
        return payload

    def overview(self, tenant_id: str) -> StudioOverview:
        return StudioOverview(
            routes=self._route_catalog(),
            voices=self.list_voices(tenant_id),
            providers=self.list_providers(),
            routing=self.get_routing(),
            example_presets=EXAMPLE_PRESETS,
            canonical_model_root=str(self.settings.openmoss_model_root),
        )

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
        return slug or f"voice_{uuid4().hex[:8]}"
