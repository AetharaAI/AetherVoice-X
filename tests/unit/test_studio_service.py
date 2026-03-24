from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from services.tts.app.schemas.studio import VoiceCreateRequest
from services.tts.app.services.studio_service import StudioService


def _settings(tmp_path: Path) -> SimpleNamespace:
    model_root = tmp_path / "models"
    return SimpleNamespace(
        local_storage_root=str(tmp_path / "storage"),
        studio_litellm_base_url=None,
        studio_openai_base_url=None,
        studio_openai_api_key=None,
        studio_openrouter_base_url=None,
        studio_openrouter_api_key=None,
        studio_litellm_api_key=None,
        studio_litellm_auth_header="Authorization",
        chatterbox_default_voice="Emily.wav",
        kokoro_default_voice="af_sky",
        kokoro_model_path=str(model_root / "audio" / "kokoro"),
        kokoro_realtime_base_url=None,
        voxtream_model_path=str(model_root / "audio" / "voxtream"),
        voxtream_realtime_base_url=None,
        voxtream2_model_path=str(model_root / "audio" / "voxtream2"),
        voxtream2_realtime_base_url=None,
        host_model_root=str(model_root),
        aether_model_root="/models",
        chatterbox_base_url=None,
        qwen_provider_base_url=None,
        qwen_provider_default_voice="Ryan",
    )


def test_import_voice_asset_upserts_generated_voice_with_reference_audio(tmp_path: Path) -> None:
    service = StudioService(_settings(tmp_path))
    created = service.create_voice(
        "tenant_1",
        VoiceCreateRequest(
            voice_id="seed_calm_female_default",
            display_name="Calm Female Default",
            type="generated",
            source_model="chatterbox",
            runtime_target="chatterbox",
            generation_prompt="Calm female dispatcher voice.",
            tags=["generated"],
            notes="text only",
        ),
    )

    imported = service.import_voice_asset(
        tenant_id="tenant_1",
        filename="preview.wav",
        payload=b"RIFFpreview",
        display_name="Calm Female Default",
        source_model="chatterbox",
        runtime_target="chatterbox",
        notes="preview bound",
        tags=["generated", "voice-design"],
        voice_id=created.voice_id,
        voice_type="generated",
        reference_text="A technician is being dispatched to your location now.",
        generation_prompt="Calm female dispatcher voice.",
        default_params={"save_to_library": True},
    )

    matching = [voice for voice in service.list_voices("tenant_1") if voice.voice_id == created.voice_id]
    assert len(matching) == 1
    assert imported.voice_id == created.voice_id
    assert imported.type == "generated"
    assert imported.reference_audio_path is not None
    assert imported.reference_audio_path.endswith(".wav")
    assert imported.generation_prompt == "Calm female dispatcher voice."
    assert imported.reference_text == "A technician is being dispatched to your location now."


def test_resolve_voice_metadata_uses_saved_generated_reference_audio(tmp_path: Path) -> None:
    service = StudioService(_settings(tmp_path))
    imported = service.import_voice_asset(
        tenant_id="tenant_1",
        filename="preview.wav",
        payload=b"RIFFpreview",
        display_name="Calm Female Default",
        source_model="chatterbox",
        runtime_target="chatterbox",
        notes="preview bound",
        tags=["generated", "voice-design"],
        voice_type="generated",
        reference_text="Please hold for a moment.",
        generation_prompt="Calm female dispatcher voice.",
        default_params={"save_to_library": True},
    )

    extra = service.resolve_voice_metadata(
        "tenant_1",
        voice_id=imported.voice_id,
        model="chatterbox",
        metadata={"source": "test"},
        include_audio_bytes=False,
    )

    assert extra["selected_voice_id"] == imported.voice_id
    assert extra["selected_voice_asset"] == imported.display_name
    assert extra["reference_audio_path"] == imported.reference_audio_path
    assert extra["generation_prompt"] == "Calm female dispatcher voice."


def test_kokoro_route_and_runtime_truth_use_builtin_voice_defaults(tmp_path: Path) -> None:
    model_root = tmp_path / "models" / "audio" / "kokoro"
    model_root.mkdir(parents=True)
    service = StudioService(_settings(tmp_path))

    routes = {route.name: route for route in service.overview("tenant_1").routes}
    assert "kokoro_realtime" in routes
    assert routes["kokoro_realtime"].model_path is not None

    runtime = service.resolve_stream_runtime_truth(
        "tenant_1",
        requested_route="kokoro_realtime",
        runtime_path_used="kokoro_realtime",
        voice_id="af_sky",
        metadata={"source": "test"},
        fallback_route_used=None,
    )

    assert runtime["selected_voice_id"] == "af_sky"
    assert runtime["actual_runtime_conditioning_source"] == "af_sky"
    assert runtime["live_chunk_source_route"] == "kokoro_realtime.sentence_stream"


def test_voxtream_route_and_runtime_truth_use_reference_audio_assets(tmp_path: Path) -> None:
    original_root = tmp_path / "models" / "audio" / "voxtream"
    original_root.mkdir(parents=True)
    v2_root = tmp_path / "models" / "audio" / "voxtream2"
    v2_root.mkdir(parents=True)
    service = StudioService(_settings(tmp_path))
    imported = service.import_voice_asset(
        tenant_id="tenant_1",
        filename="reference.wav",
        payload=b"RIFFreference",
        display_name="Dispatch Clone",
        source_model="imported",
        runtime_target="voxtream_realtime",
        notes="reference ready",
        tags=["telephony", "voxtream"],
    )

    routes = {route.name: route for route in service.overview("tenant_1").routes}
    assert "voxtream_realtime" in routes
    assert "voxtream2_realtime" in routes
    assert routes["voxtream_realtime"].present_on_disk is True
    assert routes["voxtream2_realtime"].present_on_disk is True

    runtime = service.resolve_stream_runtime_truth(
        "tenant_1",
        requested_route="voxtream_realtime",
        runtime_path_used="voxtream_realtime",
        voice_id=imported.voice_id,
        metadata={"source": "test"},
        fallback_route_used=None,
    )

    assert runtime["selected_voice_id"] == imported.voice_id
    assert runtime["resolved_conditioning_asset"] == imported.reference_audio_path
    assert runtime["actual_runtime_conditioning_source"] == imported.reference_audio_path
    assert runtime["live_chunk_source_route"] == "voxtream_realtime.full_stream"

    runtime_v2 = service.resolve_stream_runtime_truth(
        "tenant_1",
        requested_route="voxtream2_realtime",
        runtime_path_used="voxtream2_realtime",
        voice_id=imported.voice_id,
        metadata={"source": "test"},
        fallback_route_used=None,
    )

    assert runtime_v2["resolved_conditioning_asset"] == imported.reference_audio_path
    assert runtime_v2["actual_runtime_conditioning_source"] == imported.reference_audio_path
    assert runtime_v2["live_chunk_source_route"] == "voxtream2_realtime.full_stream"
