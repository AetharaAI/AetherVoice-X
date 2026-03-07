from __future__ import annotations

import asyncio
import time

import httpx


async def run(count: int = 10) -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8080", timeout=30.0) as client:
        started = time.perf_counter()
        responses = await asyncio.gather(*[client.get("/v1/health") for _ in range(count)])
        elapsed = (time.perf_counter() - started) * 1000
        print(f"completed={len(responses)} total_ms={elapsed:.2f} avg_ms={elapsed / count:.2f}")


if __name__ == "__main__":
    asyncio.run(run())
