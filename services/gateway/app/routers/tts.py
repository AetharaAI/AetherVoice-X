from __future__ import annotations

import asyncio

import websockets
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, status

from ..clients.tts_client import TTSClient
from ..config import get_settings
from ..dependencies import get_auth_context, get_quota_service, get_session_service, get_tts_client
from ..schemas.tts import TTSRequest, TTSResponse, TTSStreamStartRequest, TTSStreamStartResponse
from ..services.quota_service import QuotaService
from ..services.router_policy import choose_tts_model
from ..services.session_service import SessionService
from ..utils.ids import prefixed_id
from aether_common.auth import AuthContext, ensure_scopes
from aether_common.settings import Settings

router = APIRouter(tags=["tts"])


@router.post("/v1/tts/synthesize", response_model=TTSResponse)
async def synthesize(
    payload: TTSRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    quota_service: QuotaService = Depends(get_quota_service),
    tts_client: TTSClient = Depends(get_tts_client),
    session_service: SessionService = Depends(get_session_service),
) -> TTSResponse:
    ensure_scopes(auth, {"voice:tts"})
    await quota_service.check(auth, "/v1/tts/synthesize")
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    session_id = prefixed_id("sess_tts")
    settings = get_settings()
    model_used = choose_tts_model(payload.model, streaming=payload.stream, context_mode="batch", settings=settings)
    metadata = payload.metadata.model_dump()
    metadata["tenant_id"] = auth.tenant_id
    await session_service.create_session(session_id, auth.tenant_id, "tts_batch", payload.model, model_used, metadata)
    internal_payload = payload.model_dump()
    internal_payload["model"] = model_used
    internal_payload["metadata"] = metadata
    result = await tts_client.synthesize(internal_payload, request_id=request_id, session_id=session_id, tenant_id=auth.tenant_id)
    await session_service.record_request(
        request_id,
        session_id,
        "tts_synthesize",
        "/v1/tts/synthesize",
        payload.model,
        result["model_used"],
        "ok",
        result["timings"],
        fallback_used=result["model_used"] != model_used,
    )
    await session_service.save_tts_output(session_id, result["model_used"], payload.voice, payload.text, result["audio_url"], result["duration_ms"])
    result["session_id"] = session_id
    return TTSResponse.model_validate(result)


@router.post("/v1/tts/stream/start", response_model=TTSStreamStartResponse)
async def start_tts_stream(
    payload: TTSStreamStartRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    quota_service: QuotaService = Depends(get_quota_service),
    tts_client: TTSClient = Depends(get_tts_client),
    session_service: SessionService = Depends(get_session_service),
) -> TTSStreamStartResponse:
    ensure_scopes(auth, {"voice:tts"})
    await quota_service.check(auth, "/v1/tts/stream/start")
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    session_id = prefixed_id("sess_tts_live")
    settings = get_settings()
    model_used = choose_tts_model(payload.model, streaming=True, context_mode=payload.context_mode, settings=settings)
    metadata = payload.metadata.model_dump()
    metadata["tenant_id"] = auth.tenant_id
    await session_service.create_session(session_id, auth.tenant_id, "tts_stream", payload.model, model_used, metadata)
    internal_payload = payload.model_dump()
    internal_payload["model"] = model_used
    internal_payload["metadata"] = metadata
    await tts_client.start_stream(internal_payload, request_id=request_id, session_id=session_id, tenant_id=auth.tenant_id)
    return TTSStreamStartResponse(session_id=session_id, ws_url=f"/api/v1/tts/stream/{session_id}")


@router.websocket("/api/v1/tts/stream/{session_id}")
@router.websocket("/v1/tts/stream/{session_id}")
@router.websocket("/ws/tts/stream/{session_id}")
async def tts_stream_proxy(websocket: WebSocket, session_id: str) -> None:
    settings: Settings = get_settings()
    await websocket.accept()
    upstream_url = f"{settings.gateway_tts_ws_url}/internal/stream/{session_id}"
    try:
        async with websockets.connect(upstream_url, max_size=None) as upstream:
            async def client_to_upstream() -> None:
                while True:
                    message = await websocket.receive_text()
                    await upstream.send(message)

            async def upstream_to_client() -> None:
                async for message in upstream:
                    await websocket.send_text(message)

            await asyncio.gather(client_to_upstream(), upstream_to_client())
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
