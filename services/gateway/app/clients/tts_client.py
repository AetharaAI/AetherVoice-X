from __future__ import annotations

import httpx


class TTSClient:
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

    async def synthesize(self, payload: dict, *, request_id: str, session_id: str | None, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Tenant-Id": tenant_id}
        if session_id:
            headers["X-Session-Id"] = session_id
        response = await self.client.post("/internal/synthesize", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def start_stream(self, payload: dict, *, request_id: str, session_id: str, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Session-Id": session_id, "X-Tenant-Id": tenant_id}
        response = await self.client.post("/internal/stream/start", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
