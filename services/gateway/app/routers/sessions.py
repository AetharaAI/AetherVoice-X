from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_auth_context, get_session_service
from ..schemas.sessions import SessionDetailResponse, SessionEndResponse, SessionListResponse
from ..services.session_service import SessionService
from aether_common.auth import AuthContext, ensure_scopes
from aether_common.schemas import SessionSummary

router = APIRouter(tags=["sessions"])


@router.get("/v1/sessions", response_model=SessionListResponse)
async def list_sessions(
    status: str | None = None,
    auth: AuthContext = Depends(get_auth_context),
    session_service: SessionService = Depends(get_session_service),
) -> SessionListResponse:
    ensure_scopes(auth, {"voice:sessions:read"})
    sessions = await session_service.list_sessions(status=status)
    return SessionListResponse(sessions=[SessionSummary.model_validate(item) for item in sessions])


@router.get("/v1/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    auth: AuthContext = Depends(get_auth_context),
    session_service: SessionService = Depends(get_session_service),
) -> SessionDetailResponse:
    ensure_scopes(auth, {"voice:sessions:read"})
    detail = await session_service.get_session_detail(session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionDetailResponse(
        session=SessionSummary.model_validate(detail["session"]),
        requests=detail["requests"],
        transcripts=detail["transcripts"],
        triage_results=detail["triage_results"],
        tts_outputs=detail["tts_outputs"],
    )


@router.post("/v1/sessions/{session_id}/end", response_model=SessionEndResponse)
async def end_session(
    session_id: str,
    auth: AuthContext = Depends(get_auth_context),
    session_service: SessionService = Depends(get_session_service),
) -> SessionEndResponse:
    ensure_scopes(auth, {"voice:sessions:read"})
    await session_service.end_session(session_id)
    return SessionEndResponse(session_id=session_id, status="ended")
