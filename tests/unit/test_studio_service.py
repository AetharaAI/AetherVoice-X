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
        chatterbox_default_voice="Emily.wav",
        openmoss_model_root=str(model_root / "audio" / "OpenMOSS-Team"),
        host_model_root=str(model_root),
        aether_model_root="/models",
        moss_realtime_base_url=None,
        moss_tts_base_url=None,
        moss_ttsd_base_url=None,
        moss_voice_generator_base_url=None,
        chatterbox_base_url=None,
        moss_prompt_audio_path=None,
    )


def test_import_voice_asset_upserts_generated_voice_with_reference_audio(tmp_path: Path) -> None:
    service = StudioService(_settings(tmp_path))
    created = service.create_voice(
        "tenant_1",
        VoiceCreateRequest(
            voice_id="seed_calm_female_default",
            display_name="Calm Female Default",
            type="generated",
            source_model="moss_voice_generator",
            runtime_target="moss_tts",
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
        source_model="moss_voice_generator",
        runtime_target="moss_tts",
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
        source_model="moss_voice_generator",
        runtime_target="moss_tts",
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
        model="moss_realtime",
        metadata={"source": "test"},
        include_audio_bytes=False,
    )

    assert extra["selected_voice_id"] == imported.voice_id
    assert extra["selected_voice_asset"] == imported.display_name
    assert extra["reference_audio_path"] == imported.reference_audio_path
    assert extra["generation_prompt"] == "Calm female dispatcher voice."
