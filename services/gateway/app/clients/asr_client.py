from __future__ import annotations

import json

import httpx

from ..logging import logger


class ASRUpstreamError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class ASRClient:
    def __init__(self, base_url: str) -> None:
        self.client = httpx.AsyncClient(base_url=base_url, timeout=120.0)

    async def close(self) -> None:
        await self.client.aclose()

    async def health(self) -> dict:
        response = await self.client.get("/internal/health")
        response.raise_for_status()
        return response.json()

    async def models(self) -> list[dict]:
        response = await self.client.get("/internal/models")
        response.raise_for_status()
        return response.json()["models"]

    async def transcribe(
        self,
        payload: dict,
        *,
        audio_bytes: bytes | None,
        filename: str | None,
        content_type: str | None,
        request_id: str,
        session_id: str,
        tenant_id: str,
    ) -> dict:
        headers = {"X-Request-Id": request_id, "X-Session-Id": session_id, "X-Tenant-Id": tenant_id}
        files = None
        if audio_bytes is not None:
            files = {"file": (filename or "audio.wav", audio_bytes, content_type or "audio/wav")}
        data = {**payload, "metadata": json.dumps(payload.get("metadata", {}))}
        response = await self.client.post("/internal/transcribe", headers=headers, data=data, files=files)
        if response.is_error:
            detail = response.text
            logger.error(
                "asr_upstream_transcribe_failed",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "tenant_id": tenant_id,
                    "status_code": response.status_code,
                    "detail": detail,
                },
            )
            raise ASRUpstreamError(response.status_code, detail)
        return response.json()

    async def start_stream(self, payload: dict, *, request_id: str, session_id: str, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Session-Id": session_id, "X-Tenant-Id": tenant_id}
        response = await self.client.post("/internal/stream/start", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def triage(self, payload: dict, *, request_id: str, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Tenant-Id": tenant_id}
        response = await self.client.post("/internal/triage", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def analyze(self, payload: dict, *, request_id: str, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Tenant-Id": tenant_id}
        response = await self.client.post("/internal/analyze", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
