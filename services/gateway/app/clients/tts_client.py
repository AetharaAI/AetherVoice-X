from __future__ import annotations

import json

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

    async def voice_turn(self, payload: dict, *, request_id: str, session_id: str | None, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Tenant-Id": tenant_id}
        if session_id:
            headers["X-Session-Id"] = session_id
        response = await self.client.post("/internal/voice/turn", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def start_stream(self, payload: dict, *, request_id: str, session_id: str, tenant_id: str) -> dict:
        headers = {"X-Request-Id": request_id, "X-Session-Id": session_id, "X-Tenant-Id": tenant_id}
        response = await self.client.post("/internal/stream/start", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def studio_overview(self, *, tenant_id: str) -> dict:
        response = await self.client.get("/internal/studio/overview", headers={"X-Tenant-Id": tenant_id})
        response.raise_for_status()
        return response.json()

    async def studio_voices(self, *, tenant_id: str) -> dict:
        response = await self.client.get("/internal/studio/voices", headers={"X-Tenant-Id": tenant_id})
        response.raise_for_status()
        return response.json()

    async def create_studio_voice(self, payload: dict, *, tenant_id: str) -> dict:
        response = await self.client.post("/internal/studio/voices", headers={"X-Tenant-Id": tenant_id}, json=payload)
        response.raise_for_status()
        return response.json()

    async def import_studio_voice(self, form: dict, files: dict, *, tenant_id: str) -> dict:
        response = await self.client.post("/internal/studio/voices/import", headers={"X-Tenant-Id": tenant_id}, data=form, files=files)
        response.raise_for_status()
        return response.json()

    async def studio_providers(self) -> dict:
        response = await self.client.get("/internal/studio/providers")
        response.raise_for_status()
        return response.json()

    async def studio_provider_models(self, provider: str) -> dict:
        response = await self.client.get(f"/internal/studio/providers/{provider}/models")
        response.raise_for_status()
        return response.json()

    async def studio_routing(self) -> dict:
        response = await self.client.get("/internal/studio/routing")
        response.raise_for_status()
        return response.json()

    async def save_studio_routing(self, payload: dict) -> dict:
        response = await self.client.post("/internal/studio/routing", json=payload)
        response.raise_for_status()
        return response.json()

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
        return f"tts {operation} failed: {detail}"

    async def warm_studio_route(self, route_name: str, *, tenant_id: str) -> dict:
        try:
            response = await self.client.post(
                f"/internal/studio/routes/{route_name}/warmup",
                headers={"X-Tenant-Id": tenant_id},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(self._upstream_error_detail(exc.response, "studio warmup")) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"tts studio warmup upstream request failed: {exc}") from exc
        return response.json()
