from __future__ import annotations

import asyncio
import base64
import io
import sys
import types
import wave

sys.modules.setdefault("boto3", types.SimpleNamespace(client=lambda *args, **kwargs: None))

from services.tts.app.schemas.requests import TTSStreamStartRequest
from services.tts.app.schemas.responses import StreamCompletion, TTSResult, TimingBreakdown
from services.tts.app.services.streaming_service import StreamingService


def _wav_bytes() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(b"\x00\x00" * 240)
    return buffer.getvalue()


class FakeRedis:
    def __init__(self) -> None:
        self.records: dict[str, dict] = {}

    async def hset(self, key: str, mapping: dict) -> None:
        self.records[key] = dict(mapping)


class FakeStorage:
    def __init__(self) -> None:
        self.uploads: list[tuple[str, str]] = []

    def upload_bytes(self, bucket: str, key: str, audio_bytes: bytes, content_type: str) -> str:
        self.uploads.append((bucket, key))
        assert audio_bytes
        assert content_type == "audio/wav"
        return f"s3://{bucket}/{key}"


class FakeTelemetry:
    def __init__(self) -> None:
        self.started = 0
        self.ended = 0

    def session_started(self) -> None:
        self.started += 1

    def session_ended(self) -> None:
        self.ended += 1


class FakeSynthesisService:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def synthesize(self, request) -> tuple[TTSResult, bytes]:
        self.calls.append(request.text)
        audio_bytes = _wav_bytes()
        return (
            TTSResult(
                request_id=request.request_id,
                model_used="chatterbox",
                audio_url=f"s3://voice-tts-output/{request.request_id}.wav",
                duration_ms=10,
                timings=TimingBreakdown(total_ms=5),
                artifacts={"format": "wav"},
            ),
            audio_bytes,
        )


class FakeMossAdapter:
    name = "moss_realtime"
    supports_streaming = True
    supports_batch = False
    configured = True
    ready = True

    def __init__(self) -> None:
        self.started = False
        self.pushed: list[str] = []

    async def start_stream(self, request) -> object:
        self.started = True
        return object()

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        self.pushed.append(text)
        return [
            {
                "type": "audio_chunk",
                "session_id": session_id,
                "sequence": len(self.pushed),
                "audio_b64": base64.b64encode(_wav_bytes()).decode("ascii"),
                "format": "wav",
                "metadata": {},
            }
        ]

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        return (
            StreamCompletion(
                model_used=self.name,
                format="wav",
                duration_ms=10,
                timings=TimingBreakdown(total_ms=7),
                artifacts={"chunk_count": len(self.pushed)},
            ),
            _wav_bytes(),
        )


class FakeChatterboxAdapter:
    name = "chatterbox"
    supports_streaming = False
    supports_batch = True
    configured = True
    ready = True


class FakeRegistry:
    def __init__(self, adapter, fallback) -> None:
        self.adapter = adapter
        self.fallback = fallback

    def get(self, name: str):
        return self.adapter

    def fallback_stream(self):
        return self.fallback


class FakeSettings:
    s3_bucket_tts = "voice-tts-output"


def _request(model: str = "moss_realtime") -> TTSStreamStartRequest:
    return TTSStreamStartRequest(
        request_id="req_1",
        session_id="sess_1",
        tenant_id="tenant_1",
        model=model,
        voice="default",
        sample_rate=24000,
        format="wav",
        context_mode="conversation",
        metadata={"source": "test"},
    )


def test_streaming_service_uses_adapter_driven_streaming_for_moss() -> None:
    service = StreamingService(
        registry=FakeRegistry(FakeMossAdapter(), FakeChatterboxAdapter()),
        synthesis_service=FakeSynthesisService(),
        redis=FakeRedis(),
        telemetry=FakeTelemetry(),
        storage=FakeStorage(),
        settings=FakeSettings(),
    )

    start = asyncio.run(service.start(_request()))
    events = asyncio.run(service.push("sess_1", "Hello from MOSS."))
    result, audio_bytes = asyncio.run(service.finish("sess_1"))

    assert start["model"] == "moss_realtime"
    assert events and events[0]["type"] == "audio_chunk"
    assert result.model_used == "moss_realtime"
    assert result.audio_url.startswith("s3://voice-tts-output/tts/tenant_1/sess_1/")
    assert audio_bytes.startswith(b"RIFF")


def test_streaming_service_falls_back_to_microbatch_when_streaming_adapter_is_unavailable() -> None:
    chatterbox = FakeChatterboxAdapter()
    synthesis_service = FakeSynthesisService()
    service = StreamingService(
        registry=FakeRegistry(chatterbox, chatterbox),
        synthesis_service=synthesis_service,
        redis=FakeRedis(),
        telemetry=FakeTelemetry(),
        storage=FakeStorage(),
        settings=FakeSettings(),
    )

    start = asyncio.run(service.start(_request(model="moss_realtime")))
    events = asyncio.run(service.push("sess_1", "fallback chunk"))
    result, audio_bytes = asyncio.run(service.finish("sess_1"))

    assert start["model"] == "chatterbox"
    assert events and events[0]["type"] == "audio_chunk"
    assert synthesis_service.calls == ["fallback chunk", "fallback chunk"]
    assert result.model_used == "chatterbox"
    assert audio_bytes.startswith(b"RIFF")
