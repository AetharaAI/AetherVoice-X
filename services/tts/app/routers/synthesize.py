from __future__ import annotations

from fastapi import APIRouter, Header, Request

from ..schemas.requests import TTSRequest

router = APIRouter(tags=["synthesize"])


@router.post("/internal/synthesize")
async def synthesize(
    payload: dict,
    request: Request,
    x_request_id: str = Header(alias="X-Request-Id"),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
    x_session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict:
    tts_request = TTSRequest(
        request_id=x_request_id,
        session_id=x_session_id,
        tenant_id=x_tenant_id,
        **payload,
    )
    result, _audio_bytes = await request.app.state.synthesis_service.synthesize(tts_request)
    return result.model_dump()
