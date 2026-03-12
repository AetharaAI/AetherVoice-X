from __future__ import annotations

import base64
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
    VoiceType,
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
        registry = self._read_registry() if self.registry_path.exists() else self._bootstrap_registry()
        merged = self._ensure_seed_registry(registry)
        if merged != registry or not self.registry_path.exists():
            self._write_registry(merged)

    def _bootstrap_registry(self) -> dict[str, Any]:
        return {
            "voices": [voice.model_dump() for voice in self._seed_voices()],
            "routing": LLMRoutingConfig(
                provider="litellm",
                base_url=self.settings.studio_litellm_base_url,
                enabled=bool(self.settings.studio_litellm_base_url),
                mode="manual",
            ).model_dump(),
        }

    def _seed_payload_path(self) -> Path:
        return Path(__file__).resolve().parents[4] / "voice-studio" / "23-seed-voices-shapes.json"

    def _seed_registry_voices(self) -> list[VoiceRecord]:
        seed_path = self._seed_payload_path()
        if not seed_path.exists():
            return []
        payload = json.loads(seed_path.read_text(encoding="utf-8"))
        raw_voices = payload.get("seed_library", {}).get("voices", [])
        voices: list[VoiceRecord] = []
        for entry in raw_voices:
            if not isinstance(entry, dict):
                continue
            runtime_target = str(entry.get("runtime_target") or "").strip()
            if runtime_target not in {"moss_realtime", "moss_tts", "moss_ttsd", "moss_voice_generator", "chatterbox"}:
                continue
            default_style = dict(entry.get("default_style") or {})
            demo_text = entry.get("demo_sample_text")
            if demo_text:
                default_style.setdefault("demo_sample_text", demo_text)
            category = entry.get("category")
            if category:
                default_style.setdefault("seed_category", category)
            suggested_use_cases = entry.get("suggested_use_cases") or []
            notes = "Seeded voice design preset loaded from voice-studio."
            if suggested_use_cases:
                notes = f"{notes} Suggested use cases: {', '.join(str(item) for item in suggested_use_cases)}."
            voices.append(
                VoiceRecord(
                    voice_id=str(entry.get("voice_id") or self._slugify(str(entry.get('display_name') or 'seed_voice'))),
                    display_name=str(entry.get("display_name") or "Seed Voice"),
                    type="generated",
                    source_model=str(entry.get("source_model") or "moss_voice_generator"),
                    runtime_target=runtime_target,
                    reference_text=str(demo_text) if demo_text else None,
                    generation_prompt=str(entry.get("prompt")) if entry.get("prompt") else None,
                    tags=[str(tag) for tag in entry.get("tags") or []],
                    default_params=default_style,
                    notes=notes,
                )
            )
        return voices

    def _ensure_seed_registry(self, registry: dict[str, Any]) -> dict[str, Any]:
        merged = dict(registry)
        existing_records = [VoiceRecord.model_validate(entry) for entry in merged.get("voices", [])]
        by_id = {voice.voice_id: voice for voice in existing_records}
        for seed_voice in self._seed_voices():
            by_id.setdefault(seed_voice.voice_id, seed_voice)
        for seeded_voice in self._seed_registry_voices():
            by_id.setdefault(seeded_voice.voice_id, seeded_voice)
        merged["voices"] = [voice.model_dump() for voice in sorted(by_id.values(), key=lambda voice: (voice.type, voice.display_name.lower()))]
        merged.setdefault(
            "routing",
            LLMRoutingConfig(
                provider="litellm",
                base_url=self.settings.studio_litellm_base_url,
                enabled=bool(self.settings.studio_litellm_base_url),
                mode="manual",
            ).model_dump(),
        )
        return merged

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

    def _route_descriptor(
        self,
        *,
        name: str,
        label: str,
        mode: str,
        leaf: str | None,
        notes: str,
        fallback_target: str | None = None,
        requires_endpoint: bool = False,
        endpoint: str | None = None,
        runtime_wired: bool = False,
        force_disabled: bool = False,
    ) -> RouteDescriptor:
        present_on_disk = self._model_exists(leaf) if leaf else False
        endpoint_ready = self._endpoint_ready(endpoint) if endpoint else False
        configured = bool(endpoint) if leaf is None else present_on_disk or bool(endpoint)
        if force_disabled:
            status = "disabled" if present_on_disk or leaf is not None else "missing"
            invokable = False
        elif runtime_wired and endpoint_ready and ((present_on_disk or leaf is None) or not requires_endpoint):
            status = "ready"
            invokable = True
        elif configured:
            status = "staged"
            invokable = False
        else:
            status = "missing"
            invokable = False
        return RouteDescriptor(
            name=name,
            label=label,
            mode=mode,
            status=status,
            present_on_disk=present_on_disk if leaf else bool(endpoint),
            runtime_wired=runtime_wired,
            invokable=invokable,
            model_path=str(self._canonical_model_path(leaf)) if leaf else None,
            notes=notes,
            fallback_target=fallback_target,
        )

    def _endpoint_ready(self, endpoint: str | None) -> bool:
        if not endpoint:
            return False
        try:
            base = endpoint.rstrip("/")
            response = httpx.get(f"{base}/health", timeout=2.5)
            if response.is_success:
                return True
            if response.status_code == 404:
                fallback = httpx.get(base, timeout=2.5, follow_redirects=True)
                return fallback.is_success
            return False
        except Exception:
            return False

    def _route_catalog(self) -> list[RouteDescriptor]:
        return [
            self._route_descriptor(
                name="moss_realtime",
                label="OpenMOSS Realtime",
                mode="stream",
                leaf="MOSS-TTS-Realtime",
                requires_endpoint=True,
                endpoint=self.settings.moss_realtime_base_url,
                runtime_wired=True,
                notes="Live agent lane with session-bound streaming. Final WAV is runtime-backed. Live chunk path remains explicitly marked as experimental until chunk conditioning parity is proven.",
                fallback_target="chatterbox",
            ),
            self._route_descriptor(
                name="moss_tts",
                label="OpenMOSS TTS",
                mode="batch",
                leaf="MOSS-TTS",
                requires_endpoint=True,
                endpoint=self.settings.moss_tts_base_url,
                runtime_wired=True,
                notes="Single-speaker OpenMOSS batch synthesis route. Truth stays tied to both the canonical weights and a live sidecar health check.",
                fallback_target="chatterbox",
            ),
            self._route_descriptor(
                name="moss_ttsd",
                label="OpenMOSS TTSD",
                mode="dialogue",
                leaf="MOSS-TTSD-v1.0",
                requires_endpoint=True,
                endpoint=self.settings.moss_ttsd_base_url,
                runtime_wired=True,
                notes="Dialogue-focused OpenMOSS route for multi-speaker scenes. Readiness only flips when the TTSD sidecar is healthy.",
                fallback_target="chatterbox",
            ),
            self._route_descriptor(
                name="moss_voice_generator",
                label="OpenMOSS Voice Generator",
                mode="voice-design",
                leaf="MOSS-VoiceGenerator",
                requires_endpoint=True,
                endpoint=self.settings.moss_voice_generator_base_url,
                runtime_wired=True,
                notes="VoiceGenerator is the safest default path for studio voice-creation testing. It becomes invokable only when the dedicated sidecar is healthy.",
            ),
            self._route_descriptor(
                name="chatterbox",
                label="Chatterbox Fallback",
                mode="batch",
                leaf=None,
                endpoint=self.settings.chatterbox_base_url,
                requires_endpoint=True,
                runtime_wired=bool(self.settings.chatterbox_base_url),
                notes="Existing stable batch fallback preserved for compatibility.",
            ),
        ]

    def resolve_stream_runtime_truth(self, tenant_id: str, *, requested_route: str, runtime_path_used: str, voice_id: str, metadata: dict[str, Any], fallback_route_used: str | None) -> dict[str, Any]:
        voices = {voice.voice_id: voice for voice in self.list_voices(tenant_id)}
        extra = (metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        resolved_voice = extra.get("resolved_voice") if isinstance(extra, dict) else None
        selected_voice = (
            VoiceRecord.model_validate(resolved_voice)
            if isinstance(resolved_voice, dict)
            else voices.get(voice_id) or voices.get("moss_default") or voices.get("chatterbox_default")
        )
        realtime_profile = ((metadata.get("extra") or {}).get("realtime_profile") or {}) if isinstance(metadata, dict) else {}
        requested_preset = realtime_profile.get("voice_preset_id") if isinstance(realtime_profile, dict) else None
        notes: list[str] = []
        if runtime_path_used == "moss_realtime":
            selected_asset = str(extra.get("reference_audio_path") or "").strip() if isinstance(extra, dict) else ""
            if not selected_asset and selected_voice and selected_voice.reference_audio_path:
                selected_asset = selected_voice.reference_audio_path
            if selected_asset:
                conditioning_source = selected_asset
                conditioning_active = True
                notes.append("Realtime session is using the selected voice reference asset when present.")
            else:
                conditioning_source = self.settings.moss_prompt_audio_path or "moss_default_unconditioned"
                conditioning_active = bool(self.settings.moss_prompt_audio_path)
                if conditioning_active:
                    notes.append("Realtime session is falling back to the global prompt WAV because the selected voice has no reference asset.")
                else:
                    notes.append("Realtime session has no selected reference asset and no global prompt WAV fallback configured.")
                if selected_voice and selected_voice.generation_prompt:
                    notes.append("Voice Generator text prompts do not condition realtime directly; a reference WAV is still required for acoustic binding.")
            resolved_asset = selected_asset or None
            fallback_voice_path = self.settings.moss_prompt_audio_path or "moss_default_unconditioned"
            live_chunk_source_route = "moss_realtime.decoder_stream"
            final_artifact_source_route = "moss_realtime.final_decode"
        else:
            conditioning_source = selected_voice.reference_audio_path if selected_voice and selected_voice.reference_audio_path else "chatterbox_default_voice"
            conditioning_active = True
            resolved_asset = selected_voice.reference_audio_path if selected_voice else None
            fallback_voice_path = self.settings.chatterbox_default_voice
            live_chunk_source_route = runtime_path_used
            final_artifact_source_route = runtime_path_used
        return {
            "requested_route": requested_route,
            "runtime_path_used": runtime_path_used,
            "live_chunk_source_route": live_chunk_source_route,
            "final_artifact_source_route": final_artifact_source_route,
            "selected_voice_id": selected_voice.voice_id if selected_voice else voice_id,
            "selected_voice_asset": selected_voice.display_name if selected_voice else voice_id,
            "requested_preset": requested_preset or (selected_voice.voice_id if selected_voice else voice_id),
            "resolved_conditioning_asset": resolved_asset,
            "actual_runtime_conditioning_source": conditioning_source,
            "conditioning_active": conditioning_active,
            "fallback_route_used": fallback_route_used,
            "fallback_voice_path": fallback_voice_path,
            "notes": notes,
        }

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

    def resolve_provider_request_config(self, provider: str, *, base_url_override: str | None = None) -> tuple[str, dict[str, str]]:
        if provider == "anthropic":
            raise ValueError("Anthropic is still stubbed for generation in this pass.")
        base_url, _api_key, headers, _notes = self._provider_config(provider)
        resolved_base_url = (base_url_override or base_url or "").rstrip("/")
        if not resolved_base_url:
            raise ValueError(f"No base URL is configured for provider '{provider}'.")
        return resolved_base_url, headers

    async def list_provider_models(self, provider: str) -> list[ProviderModel]:
        if provider == "anthropic":
            return []
        try:
            base_url, headers = self.resolve_provider_request_config(provider)
        except ValueError:
            return []
        async with httpx.AsyncClient(base_url=base_url, timeout=20.0) as client:
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

    def resolve_voice_metadata(
        self,
        tenant_id: str,
        *,
        voice_id: str,
        model: str,
        metadata: dict[str, Any] | None,
        include_audio_bytes: bool = False,
    ) -> dict[str, Any]:
        voices = {voice.voice_id: voice for voice in self.list_voices(tenant_id)}
        selected = voices.get(voice_id) or voices.get("moss_default") or voices.get("chatterbox_default")
        extra = dict(metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        if selected is None:
            return extra
        resolved_voice = selected.model_dump(exclude_none=True)
        extra.setdefault("resolved_voice", resolved_voice)
        extra.setdefault("selected_voice_id", selected.voice_id)
        extra.setdefault("selected_voice_asset", selected.display_name)
        if selected.reference_audio_path:
            extra.setdefault("reference_audio_path", selected.reference_audio_path)
            if include_audio_bytes:
                reference_path = Path(selected.reference_audio_path)
                if reference_path.exists() and reference_path.is_file():
                    extra.setdefault("reference_audio_b64", base64.b64encode(reference_path.read_bytes()).decode("ascii"))
        if selected.reference_text:
            extra.setdefault("reference_text", selected.reference_text)
        if selected.generation_prompt:
            extra.setdefault("generation_prompt", selected.generation_prompt)
        if model == "moss_ttsd" and selected.reference_audio_path:
            extra.setdefault(
                "speaker_references",
                [
                    {
                        "speaker": "S1",
                        "audio_path": selected.reference_audio_path,
                        "prompt_text": selected.reference_text or "",
                        "voice_id": selected.voice_id,
                    }
                ],
            )
        return extra

    def create_voice(self, tenant_id: str, payload: VoiceCreateRequest) -> VoiceRecord:
        voice = VoiceRecord(
            voice_id=payload.voice_id or self._slugify(payload.display_name),
            tenant_id=tenant_id,
            **payload.model_dump(exclude={"voice_id"}),
        )
        self._upsert_voice(voice)
        return voice

    def _upsert_voice(self, voice: VoiceRecord) -> None:
        registry = self._read_registry()
        existing = [VoiceRecord.model_validate(entry) for entry in registry.get("voices", [])]
        retained = [entry for entry in existing if entry.voice_id != voice.voice_id]
        retained.append(voice)
        registry["voices"] = [entry.model_dump() for entry in sorted(retained, key=lambda item: (item.type, item.display_name.lower()))]
        self._write_registry(registry)

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
        voice_id: str | None = None,
        voice_type: VoiceType | None = None,
        reference_text: str | None = None,
        generation_prompt: str | None = None,
        default_params: dict[str, Any] | None = None,
    ) -> VoiceRecord:
        suffix = Path(filename).suffix or ".wav"
        resolved_voice_id = voice_id or self._slugify(display_name)
        asset_path = self.asset_dir / f"{resolved_voice_id}-{uuid4().hex[:10]}{suffix}"
        asset_path.write_bytes(payload)
        voice = VoiceRecord(
            voice_id=resolved_voice_id,
            tenant_id=tenant_id,
            display_name=display_name,
            type=voice_type or ("imported" if source_model == "imported" else "cloned"),
            source_model=source_model,
            runtime_target=runtime_target,
            reference_audio_path=asset_path.as_posix(),
            reference_text=reference_text,
            generation_prompt=generation_prompt,
            tags=tags,
            default_params=default_params or {},
            notes=notes,
        )
        self._upsert_voice(voice)
        return voice

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
