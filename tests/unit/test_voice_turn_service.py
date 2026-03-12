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
