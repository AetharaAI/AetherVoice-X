from __future__ import annotations

import asyncio
import base64
import io
import sys
import types
import wave

sys.modules.setdefault("boto3", types.SimpleNamespace(client=lambda *args, **kwargs: None))

from services.tts.app.adapters.voxtream_realtime import VoxtreamRealtimeAdapter
from services.tts.app.schemas.requests import TTSStreamStartRequest
from services.tts.app.schemas.responses import StreamCompletion, StreamSession, TimingBreakdown
from services.tts.app.services.streaming_service import StreamingService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _wav_bytes() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(b"\x00\x00" * 240)
    return buffer.getvalue()


def _b64_wav() -> str:
    return base64.b64encode(_wav_bytes()).decode("ascii")


def _request(model: str = "voxtream2_realtime", voice: str = "test_voice") -> TTSStreamStartRequest:
    return TTSStreamStartRequest(
        request_id="req_vx_1",
        session_id="sess_vx_1",
        tenant_id="tenant_test",
        model=model,
        voice=voice,
        sample_rate=24000,
        format="wav",
        context_mode="conversation",
        metadata={},
    )


# ---------------------------------------------------------------------------
# Adapter _start_payload tests
# ---------------------------------------------------------------------------


def test_start_payload_includes_prompt_audio_b64_when_present() -> None:
    """
    When extra contains reference_audio_b64, _start_payload must forward it as
    prompt_audio_b64 so the provider can decode it cross-container.
    """
    adapter = VoxtreamRealtimeAdapter.__new__(VoxtreamRealtimeAdapter)
    b64 = _b64_wav()
    request = _request()
    request = request.model_copy(
        update={
            "metadata": {
                "extra": {
                    "reference_audio_b64": b64,
                    "reference_audio_path": "/tmp/aether-storage/tts-studio/voice-assets/test.wav",
                }
            }
        }
    )
    payload = VoxtreamRealtimeAdapter._start_payload(request, model_name="voxtream2_realtime")

    # base64 must be forwarded
    assert payload["prompt_audio_b64"] == b64
    # path is also forwarded (provider prefers path if set; b64 is the cross-container fallback)
    assert payload["prompt_audio_path"] == "/tmp/aether-storage/tts-studio/voice-assets/test.wav"


def test_start_payload_includes_prompt_audio_path_when_no_b64() -> None:
    """
    When only reference_audio_path is present (e.g. shared-mount scenario),
    prompt_audio_path must be forwarded and prompt_audio_b64 must be absent.
    """
    adapter = VoxtreamRealtimeAdapter.__new__(VoxtreamRealtimeAdapter)
    request = _request()
    request = request.model_copy(
        update={
            "metadata": {
                "extra": {
                    "reference_audio_path": "/shared/audio-refs/bella_voice_ref.wav",
                }
            }
        }
    )
    payload = VoxtreamRealtimeAdapter._start_payload(request, model_name="voxtream2_realtime")

    assert payload["prompt_audio_path"] == "/shared/audio-refs/bella_voice_ref.wav"
    assert "prompt_audio_b64" not in payload


def test_start_payload_omits_audio_fields_when_no_reference() -> None:
    """
    When neither reference_audio_path nor reference_audio_b64 is in extra,
    neither prompt field may appear in the payload.  The provider will 400,
    which is the expected loud failure (prevents silent misconfiguration).
    """
    request = _request()
    payload = VoxtreamRealtimeAdapter._start_payload(request, model_name="voxtream2_realtime")

    assert "prompt_audio_path" not in payload
    assert "prompt_audio_b64" not in payload


def test_start_payload_forwards_speaking_rate_from_realtime_tuning() -> None:
    """speaking_rate in realtime_tuning must be forwarded to the provider."""
    request = _request()
    request = request.model_copy(
        update={
            "metadata": {
                "extra": {
                    "reference_audio_b64": _b64_wav(),
                    "realtime_tuning": {"speaking_rate": 2.5},
                }
            }
        }
    )
    payload = VoxtreamRealtimeAdapter._start_payload(request, model_name="voxtream2_realtime")

    assert payload["speaking_rate"] == 2.5


# ---------------------------------------------------------------------------
# Streaming service include_audio_bytes tests
# ---------------------------------------------------------------------------


class FakeRedis:
    def __init__(self) -> None:
        self.records: dict = {}

    async def hset(self, key: str, mapping: dict) -> None:
        self.records[key] = dict(mapping)


class FakeStorage:
    def upload_bytes(self, bucket: str, key: str, audio_bytes: bytes, content_type: str) -> str:
        return f"s3://{bucket}/{key}"


class FakeTelemetry:
    def session_started(self) -> None: ...
    def session_ended(self) -> None: ...


class FakeVoxtreamAdapter:
    name = "voxtream2_realtime"
    supports_streaming = True
    supports_batch = False
    configured = True
    ready = True

    def __init__(self) -> None:
        self.last_start_request = None

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        self.last_start_request = request
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)


class FakeKokoroAdapter:
    name = "kokoro_realtime"
    supports_streaming = True
    supports_batch = False
    configured = True
    ready = True

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        return StreamSession(session_id=request.session_id, model=self.name, expires_in_seconds=3600)


class FakeRegistry:
    def __init__(self, adapter, fallback) -> None:
        self.adapter = adapter
        self._fallback = fallback

    def get(self, name: str):
        return self.adapter

    def fallback_stream(self):
        return self._fallback


class FakeSettings:
    s3_bucket_tts = "voice-tts-output"


class FakeStudioServiceWithAudio:
    """Studio service that emulates a voice record with resolved reference bytes."""

    REF_B64 = _b64_wav()
    REF_PATH = "/tmp/aether-storage/tts-studio/voice-assets/test_voice-abc123.wav"

    def resolve_voice_metadata(
        self,
        tenant_id: str,
        *,
        voice_id: str,
        model: str,
        metadata: dict,
        include_audio_bytes: bool = False,
    ) -> dict:
        extra: dict = {}
        extra["resolved_voice"] = {
            "voice_id": voice_id,
            "display_name": "Test Voice",
            "reference_audio_path": self.REF_PATH,
        }
        extra["reference_audio_path"] = self.REF_PATH
        if include_audio_bytes:
            extra["reference_audio_b64"] = self.REF_B64
        return extra

    def resolve_stream_runtime_truth(
        self, tenant_id: str, *, requested_route: str, runtime_path_used: str, voice_id: str, metadata: dict, fallback_route_used
    ) -> dict:
        extra = (metadata.get("extra") or {}) if isinstance(metadata, dict) else {}
        return {
            "requested_route": requested_route,
            "runtime_path_used": runtime_path_used,
            "live_chunk_source_route": f"{runtime_path_used}.full_stream",
            "final_artifact_source_route": f"{runtime_path_used}.stream_finalize",
            "selected_voice_id": voice_id,
            "selected_voice_asset": "Test Voice",
            "requested_preset": voice_id,
            "resolved_conditioning_asset": extra.get("reference_audio_path"),
            "actual_runtime_conditioning_source": extra.get("reference_audio_path") or "missing",
            "conditioning_active": bool(extra.get("reference_audio_path")),
            "fallback_route_used": fallback_route_used,
            "fallback_voice_path": extra.get("reference_audio_path") or "",
            "notes": [],
        }


def test_streaming_service_embeds_audio_bytes_for_voxtream2() -> None:
    """
    When the resolved adapter is voxtream2_realtime, the streaming service must
    call resolve_voice_metadata with include_audio_bytes=True so that the
    reference WAV is embedded as base64 and can travel cross-container.
    """
    adapter = FakeVoxtreamAdapter()
    studio = FakeStudioServiceWithAudio()

    service = StreamingService(
        registry=FakeRegistry(adapter, FakeKokoroAdapter()),
        synthesis_service=None,
        redis=FakeRedis(),
        telemetry=FakeTelemetry(),
        storage=FakeStorage(),
        settings=FakeSettings(),
        studio_service=studio,
    )

    asyncio.run(service.start(_request(model="voxtream2_realtime")))

    assert adapter.last_start_request is not None
    extra = adapter.last_start_request.metadata.get("extra") or {}
    # bytes must be embedded so _start_payload can set prompt_audio_b64
    assert extra.get("reference_audio_b64") == FakeStudioServiceWithAudio.REF_B64, (
        "include_audio_bytes was not True for voxtream2_realtime — provider will 400"
    )


def test_streaming_service_does_not_embed_audio_bytes_for_kokoro() -> None:
    """
    Kokoro is a preset-voice model. Embedding WAV bytes for it is wasteful and
    wrong.  include_audio_bytes must remain False for non-Voxtream routes.
    """
    kokoro = FakeKokoroAdapter()
    studio = FakeStudioServiceWithAudio()

    service = StreamingService(
        registry=FakeRegistry(kokoro, kokoro),
        synthesis_service=None,
        redis=FakeRedis(),
        telemetry=FakeTelemetry(),
        storage=FakeStorage(),
        settings=FakeSettings(),
        studio_service=studio,
    )

    asyncio.run(service.start(_request(model="kokoro_realtime")))
    # No assertion needed on a specific call — just verify it doesn't raise
    # and the session is registered (kokoro adapter doesn't capture the request)
    assert "sess_vx_1" in service.sessions
    extra = service.sessions["sess_vx_1"]["request"].metadata.get("extra") or {}
    assert "reference_audio_b64" not in extra, (
        "Audio bytes must not be embedded for kokoro_realtime — unnecessary payload bloat"
    )


def test_start_stream_posts_route_alias_not_hf_model_id() -> None:
    """
    Regression guard: provider runtime validates model alias (voxtream2_realtime),
    not HF model ID (herimor/voxtream2).
    """

    class FakeResponse:
        def __init__(self, payload: dict) -> None:
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return self._payload

    class FakeClient:
        def __init__(self) -> None:
            self.last_json: dict | None = None

        async def post(self, _path: str, json: dict) -> FakeResponse:
            self.last_json = json
            return FakeResponse({"session_id": json["session_id"], "model": json["model"], "expires_in_seconds": 3600})

    adapter = VoxtreamRealtimeAdapter.__new__(VoxtreamRealtimeAdapter)
    adapter.name = "voxtream2_realtime"
    adapter.model_name = "herimor/voxtream2"
    adapter.base_url = "http://voxtream2-provider:8075"
    adapter.timeout_seconds = 120.0
    adapter.client = FakeClient()
    adapter.configured = True
    adapter.ready = True

    req = _request(model="voxtream2_realtime")
    asyncio.run(adapter.start_stream(req))

    assert adapter.client.last_json is not None
    assert adapter.client.last_json["model"] == "voxtream2_realtime"
