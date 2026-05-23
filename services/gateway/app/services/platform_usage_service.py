from __future__ import annotations

from typing import Any

import httpx

from aether_common.auth import AuthContext
from aether_common.settings import Settings


class PlatformUsageService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def report(
        self,
        auth: AuthContext,
        *,
        service: str,
        metric: str,
        quantity: float,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if (
            auth.auth_type != "platform_api_key"
            or not auth.api_key
            or not self._settings.platform_usage_report_url
            or not self._settings.platform_internal_secret
            or quantity <= 0
        ):
            return

        payload: dict[str, Any] = {
            "apiKey": auth.api_key,
            "service": service,
            "metric": metric,
            "quantity": quantity,
            "source": "aether-voice-gateway",
        }
        if request_id:
            payload["requestId"] = request_id
        if metadata:
            payload["metadata"] = metadata

        try:
            async with httpx.AsyncClient(timeout=self._settings.platform_internal_timeout_seconds) as client:
                await client.post(
                    self._settings.platform_usage_report_url,
                    json=payload,
                    headers={"x-platform-internal-secret": self._settings.platform_internal_secret},
                )
        except httpx.HTTPError:
            return
