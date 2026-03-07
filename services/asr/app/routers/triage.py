from __future__ import annotations

from fastapi import APIRouter, Header, Request

from ..schemas.requests import ASRTriageRequest

router = APIRouter(tags=["triage"])


@router.post("/internal/triage")
async def triage(payload: ASRTriageRequest, request: Request, x_request_id: str = Header(alias="X-Request-Id")) -> dict:
    result = await request.app.state.triage_service.classify(x_request_id, payload)
    return result.model_dump()
