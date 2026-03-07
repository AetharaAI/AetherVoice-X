from __future__ import annotations

import time


def now_ms() -> int:
    return int(time.time() * 1000)


def elapsed_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)
