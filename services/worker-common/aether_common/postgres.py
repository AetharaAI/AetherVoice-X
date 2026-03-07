from __future__ import annotations

from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


def normalize_postgres_url(url: str) -> str:
    return url.replace("+psycopg", "").replace("+asyncpg", "")


class PostgresPool:
    def __init__(self, url: str) -> None:
        self.url = normalize_postgres_url(url)
        self.pool = AsyncConnectionPool(self.url, min_size=1, max_size=8, open=False, kwargs={"row_factory": dict_row})

    async def open(self) -> None:
        await self.pool.open()

    async def close(self) -> None:
        await self.pool.close()

    async def fetch_all(self, query: str, params: dict[str, Any] | tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
                rows = await cur.fetchall()
                return [dict(row) for row in rows]

    async def fetch_one(self, query: str, params: dict[str, Any] | tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
                row = await cur.fetchone()
                return dict(row) if row else None

    async def execute(self, query: str, params: dict[str, Any] | tuple[Any, ...] | None = None) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
            await conn.commit()
