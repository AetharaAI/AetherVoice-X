from __future__ import annotations

from aether_common.auth import AuthContext


class QuotaService:
    async def check(self, auth: AuthContext, route: str) -> None:
        _ = (auth, route)
        return None
