from __future__ import annotations

import httpx

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamSession, TTSResult


class ChatterboxAdapter(BaseTTSAdapter):
    name = "chatterbox"
    supports_streaming = False
    supports_batch = True

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=120.0)

    async def close(self) -> None:
        await self.client.aclose()

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        payload = {
            "voice": request.voice,
            "text": request.text,
            "format": request.format,
            "sample_rate": request.sample_rate,
            "style": request.style.model_dump(),
        }
        candidates = [f"{self.base_url}/synthesize", f"{self.base_url}/v1/synthesize"]
        last_exc: Exception | None = None
        for url in candidates:
            try:
                response = await self.client.post(url, json=payload)
                response.raise_for_status()
                if response.headers.get("content-type", "").startswith("audio/"):
                    return response.content, request.format
                body = response.json()
                if "audio_b64" in body:
                    import base64

                    return base64.b64decode(body["audio_b64"]), body.get("format", request.format)
                if "audio_url" in body:
                    follow_up = await self.client.get(body["audio_url"])
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
