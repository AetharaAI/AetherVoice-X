from __future__ import annotations

import asyncio
import sys
import types

import httpx

sys.modules.setdefault("boto3", types.SimpleNamespace(client=lambda *args, **kwargs: None))

from services.tts.app.schemas.responses import TTSResult, TimingBreakdown
from services.tts.app.schemas.studio import LLMRoutingConfig
from services.tts.app.schemas.voice import VoiceTurnRequest
from services.tts.app.services.voice_turn_service import VoiceTurnService


class FakeStudioService:
    def __init__(self, *, enabled: bool = True) -> None:
        self.routing = LLMRoutingConfig(
            provider="litellm",
            model="qwen3-32b",
            base_url="http://litellm.local/v1",
            enabled=enabled,
            mode="asr_llm_tts",
            system_prompt="Keep replies short and spoken-ready.",
        )

    def get_routing(self) -> LLMRoutingConfig:
        return self.routing

    def resolve_provider_request_config(self, provider: str, *, base_url_override: str | None = None) -> tuple[str, dict[str, str]]:
        assert provider == "litellm"
        return (base_url_override or self.routing.base_url or "").rstrip("/"), {"Authorization": "Bearer test"}

    def resolve_voice_metadata(
        self,
        tenant_id: str,
        *,
        voice_id: str,
        model: str,
        metadata: dict,
        include_audio_bytes: bool,
    ) -> dict:
        return {
            "voice_id": voice_id,
            "display_name": "Sky",
            "runtime_target": model,
            "source_model": model,
            "include_audio_bytes": include_audio_bytes,
        }

    def resolve_stream_runtime_truth(
        self,
        tenant_id: str,
        *,
        requested_route: str,
        runtime_path_used: str,
        voice_id: str,
        metadata: dict,
        fallback_route_used: str | None,
    ) -> dict:
        return {
            "requested_route": requested_route,
            "runtime_path_used": runtime_path_used,
            "live_chunk_source_route": runtime_path_used,
            "final_artifact_source_route": runtime_path_used,
            "selected_voice_id": voice_id,
            "selected_voice_asset": "Sky",
            "requested_preset": voice_id,
            "resolved_conditioning_asset": voice_id,
            "actual_runtime_conditioning_source": voice_id,
            "conditioning_active": True,
            "fallback_route_used": fallback_route_used,
            "fallback_voice_path": None,
            "notes": [],
        }


class FakeSynthesisService:
    def __init__(self) -> None:
        self.requests = []

    async def synthesize(self, request):
        self.requests.append(request)
        return (
            TTSResult(
                request_id=request.request_id,
                model_used="moss_tts",
                audio_url="s3://voice-tts-output/reply.wav",
                duration_ms=1400,
                timings=TimingBreakdown(inference_ms=321, total_ms=321),
                artifacts={"selected_voice_id": request.voice},
            ),
            b"RIFFreply",
        )


class FakeStorage:
    def __init__(self) -> None:
        self.uploads = []

    def upload_bytes(self, bucket: str, key: str, audio_bytes: bytes, content_type: str) -> str:
        self.uploads.append((bucket, key, audio_bytes, content_type))
        return f"s3://{bucket}/{key}"


class FakeStreamingAdapter:
    name = "kokoro_realtime"
    supports_streaming = True
    supports_batch = False
    configured = True
    ready = True

    def __init__(self) -> None:
        self.started = []
        self.pushed = []
        self.completed = []
        self.ended = []

    async def start_stream(self, request):
        self.started.append(request)
        return None

    async def push_text(self, session_id: str, text: str):
        self.pushed.append((session_id, text))
        return [{"type": "audio_chunk", "sequence": 1, "metadata": {"source": "push"}}]

    async def complete_text(self, session_id: str):
        self.completed.append(session_id)
        return [{"type": "audio_chunk", "sequence": 2, "metadata": {"source": "complete"}}]

    async def end_stream(self, session_id: str):
        self.ended.append(session_id)
        return (
            types.SimpleNamespace(
                model_used="kokoro_realtime",
                format="wav",
                duration_ms=900,
                timings=TimingBreakdown(inference_ms=180, total_ms=220),
                artifacts={"selected_voice_id": "af_sky"},
            ),
            b"RIFFreply",
        )


class FakeRegistry:
    def __init__(self, adapter: FakeStreamingAdapter) -> None:
        self.adapter = adapter

    def get(self, name: str):
        assert name == "kokoro_realtime"
        return self.adapter

    def fallback_stream(self):
        return self.adapter


def _request() -> VoiceTurnRequest:
    return VoiceTurnRequest(
        request_id="req_voice_1",
        session_id="sess_voice_1",
        tenant_id="tenant_1",
        transcript_text="Can you confirm the technician is still on the way?",
        voice="moss_default",
        tts_model="moss_tts",
        metadata={"source": "test"},
    )


def test_voice_turn_service_generates_llm_reply_then_synthesizes_tts() -> None:
    synthesis = FakeSynthesisService()

    def client_factory(**kwargs):
        transport = httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json={
                    "id": "chatcmpl_123",
                    "model": "qwen3-32b",
                    "choices": [
                        {
                            "message": {
                                "content": "Yes. The technician is still en route and should arrive shortly."
                            }
                        }
                    ],
                },
            )
        )
        return httpx.AsyncClient(base_url=kwargs["base_url"], transport=transport)

    service = VoiceTurnService(
        settings=object(),
        studio_service=FakeStudioService(),
        synthesis_service=synthesis,
        client_factory=client_factory,
    )

    result = asyncio.run(service.generate_turn(_request()))

    assert synthesis.requests
    assert synthesis.requests[0].text == "Yes. The technician is still en route and should arrive shortly."
    assert synthesis.requests[0].metadata["extra"]["source_transcript_text"] == _request().transcript_text
    assert synthesis.requests[0].metadata["extra"]["llm_provider"] == "litellm"
    assert synthesis.requests[0].metadata["source"] == "test"
    assert result.response_text.startswith("Yes.")
    assert result.llm_provider == "litellm"
    assert result.llm_model_used == "qwen3-32b"
    assert result.tts_model_used == "moss_tts"
    assert result.audio_url == "s3://voice-tts-output/reply.wav"
    assert result.timings.total_ms >= result.tts_timings.total_ms


def test_voice_turn_service_requires_enabled_routing() -> None:
    service = VoiceTurnService(
        settings=object(),
        studio_service=FakeStudioService(enabled=False),
        synthesis_service=FakeSynthesisService(),
        client_factory=lambda **kwargs: httpx.AsyncClient(base_url=kwargs["base_url"]),
    )

    try:
        asyncio.run(service.generate_turn(_request()))
    except ValueError as exc:
        assert "disabled" in str(exc)
    else:
        raise AssertionError("Expected disabled routing to fail.")


def test_voice_turn_service_strips_reserved_and_think_tags_before_tts() -> None:
    synthesis = FakeSynthesisService()

    def client_factory(**kwargs):
        transport = httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json={
                    "id": "chatcmpl_456",
                    "model": "minicpm-v-4.5",
                    "choices": [
                        {
                            "message": {
                                "content": "<reserved_12><think>I should ask for more context.</think><reserved_13> What can I help you with today?"
                            }
                        }
                    ],
                },
            )
        )
        return httpx.AsyncClient(base_url=kwargs["base_url"], transport=transport)

    service = VoiceTurnService(
        settings=object(),
        studio_service=FakeStudioService(),
        synthesis_service=synthesis,
        client_factory=client_factory,
    )

    result = asyncio.run(service.generate_turn(_request()))

    assert synthesis.requests
    assert synthesis.requests[0].text == "What can I help you with today?"
    assert result.response_text == "What can I help you with today?"


def test_voice_turn_service_uses_streaming_lane_for_kokoro() -> None:
    synthesis = FakeSynthesisService()
    synthesis.registry = FakeRegistry(FakeStreamingAdapter())
    synthesis.storage = FakeStorage()

    class FakeSettings:
        s3_bucket_tts = "voice-tts-output"

    def client_factory(**kwargs):
        transport = httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json={
                    "id": "chatcmpl_stream_1",
                    "model": "qwen3-32b",
                    "choices": [
                        {
                            "message": {
                                "content": "Thank you for calling. This is Monica, how may I assist you today?"
                            }
                        }
                    ],
                },
            )
        )
        return httpx.AsyncClient(base_url=kwargs["base_url"], transport=transport)

    service = VoiceTurnService(
        settings=FakeSettings(),
        studio_service=FakeStudioService(),
        synthesis_service=synthesis,
        client_factory=client_factory,
    )

    request = _request().model_copy(update={"tts_model": "kokoro_realtime", "voice": "af_sky"})
    result = asyncio.run(service.generate_turn(request))

    adapter = synthesis.registry.adapter
    assert not synthesis.requests
    assert adapter.started
    assert adapter.pushed == [("sess_voice_1", "Thank you for calling. This is Monica, how may I assist you today?")]
    assert adapter.completed == ["sess_voice_1"]
    assert adapter.ended == ["sess_voice_1"]
    assert synthesis.storage.uploads
    assert result.tts_model_used == "kokoro_realtime"
    assert result.audio_url.endswith("sess_voice_1/sess_voice_1_final.wav")
    assert result.artifacts["tts_mode"] == "streaming"
    assert result.artifacts["tts_chunk_events"] == 2
