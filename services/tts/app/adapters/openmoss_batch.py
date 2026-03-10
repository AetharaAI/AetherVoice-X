from __future__ import annotations

import base64
import json

import httpx

from .base import BaseTTSAdapter
from ..schemas.requests import TTSRequest, TTSStreamStartRequest
from ..schemas.responses import StreamCompletion, StreamSession, TimingBreakdown


class OpenMOSSBatchAdapter(BaseTTSAdapter):
    supports_streaming = False
    supports_batch = True

    def __init__(self, *, name: str, base_url: str | None, timeout_seconds: float = 180.0) -> None:
        self.name = name
        self.base_url = (base_url or "").rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout_seconds) if self.base_url else None
        self.configured = bool(self.base_url)
        self.ready = self._probe_health()

    def _probe_health(self) -> bool:
        if not self.base_url:
            return False
        try:
            response = httpx.get(f"{self.base_url}/health", timeout=min(self.timeout_seconds, 3.0))
            return response.is_success
        except Exception:
            return False

    def refresh_health(self) -> bool:
        self.ready = self._probe_health()
        return self.ready

    def _upstream_error_detail(self, response: httpx.Response, operation: str) -> str:
        detail: str | None = None
        try:
            payload = response.json()
            if isinstance(payload, dict):
                raw_detail = payload.get("detail")
                if isinstance(raw_detail, str) and raw_detail.strip():
                    detail = raw_detail.strip()
                elif raw_detail is not None:
                    detail = json.dumps(raw_detail)
        except Exception:
            detail = None
        if not detail:
            detail = response.text.strip() or response.reason_phrase or "upstream request failed"
        return f"{self.name} {operation} failed: {detail}"

    async def warmup(self, metadata: dict | None = None) -> dict:
        if not self.base_url or self.client is None:
            raise RuntimeError(f"{self.name} upstream is not configured")
        try:
            response = await self.client.post(
                "/v1/warmup",
                json={"metadata": metadata or {}},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(self._upstream_error_detail(exc.response, "warmup")) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"{self.name} warmup upstream request failed: {exc}") from exc
        self.ready = True
        return response.json()

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()

    async def synthesize(self, request: TTSRequest) -> tuple[bytes, str]:
        if not self.base_url or self.client is None:
            raise RuntimeError(f"{self.name} upstream is not configured")
        try:
            response = await self.client.post(
                "/v1/synthesize",
                json={
                    "text": request.text,
                    "format": request.format,
                    "sample_rate": request.sample_rate,
                    "voice": request.voice,
                    "style": request.style.model_dump(),
                    "metadata": request.metadata,
                },
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(self._upstream_error_detail(exc.response, "synthesis")) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"{self.name} synthesis upstream request failed: {exc}") from exc
        payload = response.json()
        audio_b64 = payload.get("audio_b64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise RuntimeError(f"{self.name} upstream did not return audio")
        self.ready = True
        return base64.b64decode(audio_b64), str(payload.get("format", request.format))

    async def start_stream(self, request: TTSStreamStartRequest) -> StreamSession:
        raise NotImplementedError(f"{self.name} does not support streaming")

    async def push_text(self, session_id: str, text: str) -> list[dict]:
        raise NotImplementedError(f"{self.name} does not support streaming")

    async def end_stream(self, session_id: str) -> tuple[StreamCompletion, bytes]:
        raise NotImplementedError(f"{self.name} does not support streaming")
