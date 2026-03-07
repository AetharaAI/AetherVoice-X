from __future__ import annotations

from redis.asyncio import Redis


class RedisManager:
    def __init__(self, url: str) -> None:
        self.url = url
        self._client: Redis | None = None

    async def connect(self) -> Redis:
        if self._client is None:
            self._client = Redis.from_url(self.url, decode_responses=True)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None
