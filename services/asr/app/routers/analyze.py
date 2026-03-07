from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Header

from ..schemas.requests import ASRAnalyzeRequest
from ..schemas.responses import AnalyzeResult

router = APIRouter(tags=["analyze"])


@router.post("/internal/analyze")
async def analyze(payload: ASRAnalyzeRequest, x_request_id: str = Header(alias="X-Request-Id")) -> dict:
    tokens = [token.strip(".,!?").lower() for token in payload.transcript.split() if token.strip()]
    keywords = [word for word, _ in Counter(tokens).most_common(5)]
    speaking_rate = max(80, min(190, len(tokens) * 12))
    summary = payload.transcript[:240] if payload.transcript else "No transcript content received."
    return AnalyzeResult(request_id=x_request_id, keywords=keywords, speaking_rate_wpm=speaking_rate, summary=summary).model_dump()
