from __future__ import annotations

import asyncio

from services.tts.app.adapters.voxtral_tts import VoxtralTTSAdapter
from services.tts.app.schemas.requests import TTSRequest, TTSStreamStartRequest


def _request(voice: str = "voxtral_casual_female") -> TTSRequest:
    return TTSRequest(
        request_id="req_vx_tts_1",
        session_id="sess_vx_tts_1",
        tenant_id="tenant_test",
        model="voxtral_tts",
        voice=voice,
        text="This is a short smoke test.",
        format="wav",
        sample_rate=24000,
        stream=False,
        metadata={
            "extra": {
                "resolved_voice": {
                    "voice_id": "voxtral_casual_female",
                    "display_name": "Voxtral Casual Female",
                    "runtime_target": "voxtral_tts",
                    "default_params": {"voxtral_voice": "casual_female"},
                }
            }
        },
    )


def test_voxtral_tts_synthesize_posts_provider_contract_and_returns_audio() -> None:
    class FakeResponse:
        headers = {"content-type": "audio/wav"}
        content = b"RIFF....WAVE"

        def raise_for_status(self) -> None:
            return None

    class FakeClient:
        def __init__(self) -> None:
            self.calls: list[tuple[str, dict]] = []

        async def post(self, path: str, json: dict | None = None) -> FakeResponse:
            self.calls.append((path, dict(json or {})))
            return FakeResponse()

    adapter = VoxtralTTSAdapter.__new__(VoxtralTTSAdapter)
    adapter.base_url = "http://host.docker.internal:8000"
    adapter.model_name = "/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603"
    adapter.default_voice = "casual_female"
    adapter.client = FakeClient()
    adapter.ready = False

    result = asyncio.run(adapter.synthesize(_request()))

    assert adapter.client.calls[0][0] == "/v1/audio/speech"
    assert adapter.client.calls[0][1]["model"] == "/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603"
    assert adapter.client.calls[0][1]["voice"] == "casual_female"
    assert result.audio_bytes == b"RIFF....WAVE"
    assert result.output_format == "wav"
    assert result.artifacts["runtime_path_used"] == "voxtral_tts"
    assert adapter.ready is True


def test_voxtral_tts_stream_lifecycle_emits_audio_chunk_and_completion() -> None:
    class FakeResponse:
        headers = {"content-type": "audio/wav"}
        content = b"RIFF....WAVE"

        def raise_for_status(self) -> None:
            return None

    class FakeClient:
        def __init__(self) -> None:
            self.calls: list[tuple[str, dict]] = []

        async def post(self, path: str, json: dict | None = None) -> FakeResponse:
            self.calls.append((path, dict(json or {})))
            return FakeResponse()

    adapter = VoxtralTTSAdapter.__new__(VoxtralTTSAdapter)
    adapter.base_url = "http://host.docker.internal:8000"
    adapter.model_name = "/mnt/aetherpro/models/audio/mistralai/Voxtral-4B-TTS-2603"
    adapter.default_voice = "casual_female"
    adapter.client = FakeClient()
    adapter.ready = False
    adapter._stream_sessions = {}

    start = TTSStreamStartRequest(
        request_id="req_vx_stream_1",
        session_id="sess_vx_stream_1",
        tenant_id="tenant_test",
        model="voxtral_tts",
        voice="voxtral_casual_female",
        format="wav",
        metadata={
            "extra": {
                "resolved_voice": {
                    "voice_id": "voxtral_casual_female",
                    "display_name": "Voxtral Casual Female",
                    "runtime_target": "voxtral_tts",
                    "default_params": {"voxtral_voice": "casual_female"},
                }
            }
        },
    )
    session = asyncio.run(adapter.start_stream(start))
    events = asyncio.run(adapter.push_text(start.session_id, "Streaming test payload."))
    completion, audio_bytes = asyncio.run(adapter.end_stream(start.session_id))

    assert session.session_id == "sess_vx_stream_1"
    assert events
    assert events[0]["type"] == "audio_chunk"
    assert completion.model_used == "voxtral_tts"
    assert completion.artifacts["voxtral_tts_voice"] == "casual_female"
    assert audio_bytes == b"RIFF....WAVE"
    assert adapter.client.calls[0][0] == "/v1/audio/speech"
