from __future__ import annotations

import httpx
from urllib.parse import urljoin

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamSession, TTSResult


class ChatterboxAdapter(BaseTTSAdapter):
    name = "chatterbox"
    supports_streaming = False
    supports_batch = True

    def __init__(self, base_url: str, *, default_voice: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.default_voice = default_voice
        self.client = httpx.AsyncClient(timeout=120.0)

    async def close(self) -> None:
        await self.client.aclose()

    def _resolve_voice_file(self, voice: str) -> str:
        candidate = (voice or "").strip()
        if not candidate or candidate == "default":
            return self.default_voice
        if "." in candidate:
            return candidate
        return f"{candidate}.wav"

    def _resolve_voice_name(self, voice_file: str) -> str:
        return voice_file.rsplit(".", 1)[0]

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        voice_file = self._resolve_voice_file(request.voice)
        voice_name = self._resolve_voice_name(voice_file)
        candidates = [
            (
                f"{self.base_url}/tts",
                {
                    "text": request.text,
                    "voice_mode": "predefined",
                    "predefined_voice_id": voice_file,
                    "output_format": request.format,
                    "split_text": True,
                    "chunk_size": 120,
                    "speed_factor": request.style.speed,
                    "language": "en",
                },
            ),
            (
                f"{self.base_url}/v1/audio/speech",
                {
                    "model": self.name,
                    "input": request.text,
                    "voice": voice_name,
                    "response_format": request.format,
                    "speed": request.style.speed,
                },
            ),
        ]
        last_exc: Exception | None = None
        for url, payload in candidates:
            try:
                response = await self.client.post(url, json=payload, headers={"Accept": f"audio/{request.format}"})
                response.raise_for_status()
                if response.headers.get("content-type", "").startswith("audio/"):
                    return response.content, request.format
                body = response.json()
                if "audio_b64" in body:
                    import base64

                    return base64.b64decode(body["audio_b64"]), body.get("format", request.format)
                if "audio_url" in body:
                    follow_up = await self.client.get(urljoin(f"{self.base_url}/", body["audio_url"]))
                    follow_up.raise_for_status()
                    return follow_up.content, body.get("format", request.format)
            except Exception as exc:  # pragma: no cover - depends on external Chatterbox shape
                last_exc = exc
        raise RuntimeError(f"Unable to synthesize via Chatterbox passthrough: {last_exc}")

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")

    async def end_stream(self, session_id: str) -> TTSResult:
        raise NotImplementedError("Chatterbox streaming is not implemented; use micro-batch fallback")
