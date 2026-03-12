from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request

from ..schemas.voice import VoiceTurnRequest

router = APIRouter(tags=["voice"])


@router.post("/internal/voice/turn")
async def generate_voice_turn(
    payload: dict,
    request: Request,
    x_request_id: str = Header(alias="X-Request-Id"),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
    x_session_id: str | None = Header(default=None, alias="X-Session-Id"),
) -> dict:
    voice_turn_request = VoiceTurnRequest(
        request_id=x_request_id,
        session_id=x_session_id,
        tenant_id=x_tenant_id,
        **payload,
    )
    try:
        result = await request.app.state.voice_turn_service.generate_turn(voice_turn_request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return result.model_dump()
