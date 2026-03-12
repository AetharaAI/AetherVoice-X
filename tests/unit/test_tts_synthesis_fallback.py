from __future__ import annotations

import asyncio
import io
import sys
import types
import wave

sys.modules.setdefault("boto3", types.SimpleNamespace(client=lambda *args, **kwargs: None))

from services.tts.app.adapters.chatterbox import ChatterboxAdapter
from services.tts.app.schemas.requests import TTSRequest
from services.tts.app.schemas.responses import TimingBreakdown
from services.tts.app.schemas.studio import VoiceRecord
from services.tts.app.services.synthesis_service import SynthesisService


def _wav_bytes() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(b"\x00\x00" * 240)
    return buffer.getvalue()


class FakeStorage:
    def upload_bytes(self, bucket: str, key: str, audio_bytes: bytes, content_type: str) -> str:
        assert bucket == "voice-tts-output"
        assert audio_bytes.startswith(b"RIFF")
        assert content_type == "audio/wav"
        return f"s3://{bucket}/{key}"


class FakeSettings:
    s3_bucket_tts = "voice-tts-output"


class FakeStudioService:
    def list_voices(self, tenant_id: str) -> list[VoiceRecord]:
        return [
            VoiceRecord(
                voice_id="moss_default",
                display_name="MOSS Default Voice",
                type="preset",
                source_model="moss_realtime",
                runtime_target="moss_realtime",
                tags=["openmoss"],
            ),
            VoiceRecord(
                voice_id="chatterbox_default",
                display_name="Emily",
                type="fallback",
                source_model="chatterbox",
                runtime_target="chatterbox",
                reference_audio_path="Emily.wav",
                tags=["chatterbox"],
            ),
        ]

    def resolve_voice_metadata(self, tenant_id: str, *, voice_id: str, model: str, metadata: dict, include_audio_bytes: bool = False) -> dict:
        for voice in self.list_voices(tenant_id):
            if voice.voice_id != voice_id:
                continue
            return {
                "resolved_voice": voice.model_dump(exclude_none=True),
                "selected_voice_id": voice.voice_id,
                "selected_voice_asset": voice.display_name,
                "reference_audio_path": voice.reference_audio_path,
            }
        return {}


class FakeFailingAdapter:
    name = "moss_voice_generator"
    supports_streaming = False
    supports_batch = True

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        raise RuntimeError("voice generator offline")


class FakeCapturingChatterboxAdapter:
    name = "chatterbox"
    supports_streaming = False
    supports_batch = True

    def __init__(self) -> None:
        self.requests: list[TTSRequest] = []

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        self.requests.append(request)
        return _wav_bytes(), "wav"


class FakeRegistry:
    def __init__(self, primary, fallback) -> None:
        self.primary = primary
        self.fallback = fallback

    def get(self, name: str):
        return self.primary

    def fallback_batch(self):
        return self.fallback


def _request() -> TTSRequest:
    return TTSRequest(
        request_id="req_1",
        session_id="sess_1",
        tenant_id="tenant_1",
        model="moss_voice_generator",
        voice="moss_default",
        text="Render a quick preview line.",
        format="wav",
        sample_rate=24000,
        style={"speed": 1.0, "emotion": "neutral"},
        metadata={"source": "test"},
    )


def test_synthesis_service_uses_chatterbox_safe_voice_on_openmoss_fallback() -> None:
    chatterbox = FakeCapturingChatterboxAdapter()
    service = SynthesisService(
        registry=FakeRegistry(FakeFailingAdapter(), chatterbox),
        storage=FakeStorage(),
        settings=FakeSettings(),
        studio_service=FakeStudioService(),
    )

    result, _audio_bytes = asyncio.run(service.synthesize(_request()))

    assert chatterbox.requests
    assert chatterbox.requests[0].voice == "default"
    assert chatterbox.requests[0].metadata["extra"]["fallback_original_voice_id"] == "moss_default"
    assert chatterbox.requests[0].metadata["extra"]["fallback_voice_route"] == "chatterbox_default"
    assert result.model_used == "chatterbox"
    assert result.artifacts["fallback_route_used"] == "chatterbox"
    assert result.artifacts["requested_adapter_name"] == "moss_voice_generator"
    assert result.artifacts["resolved_adapter_name"] == "chatterbox"
    assert result.artifacts["fallback_reason"] == "moss_voice_generator synthesize failed"
    assert result.artifacts["fallback_exception_type"] == "RuntimeError"


def test_chatterbox_adapter_defaults_non_chatterbox_registry_voice_ids() -> None:
    adapter = ChatterboxAdapter("https://tts.example", default_voice="Emily.wav")
    try:
        assert (
            adapter._resolve_voice_file(
                "moss_default",
                extra={"resolved_voice": {"runtime_target": "moss_realtime", "source_model": "moss_realtime"}},
            )
            == "Emily.wav"
        )
    finally:
        asyncio.run(adapter.close())


def test_chatterbox_adapter_uses_reference_asset_for_registry_fallback_voice() -> None:
    adapter = ChatterboxAdapter("https://tts.example", default_voice="Emily.wav")
    try:
        assert (
            adapter._resolve_voice_file(
                "chatterbox_default",
                extra={"resolved_voice": {"runtime_target": "chatterbox", "reference_audio_path": "/tmp/Olivia.wav"}},
            )
            == "Olivia.wav"
        )
    finally:
        asyncio.run(adapter.close())
