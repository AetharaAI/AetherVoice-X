from __future__ import annotations

import asyncio
import json
from typing import Any

import websockets
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, WebSocket, WebSocketDisconnect, status
from starlette.datastructures import UploadFile as StarletteUploadFile

from ..clients.asr_client import ASRClient, ASRUpstreamError
from ..logging import logger
from ..config import get_settings
from ..dependencies import get_asr_client, get_auth_context, get_quota_service, get_session_service
from ..schemas.asr import (
    ASRAnalyzeRequest,
    ASRAnalyzeResponse,
    ASRStreamStartRequest,
    ASRStreamStartResponse,
    ASRTriageRequest,
    ASRTriageResponse,
    ASRTranscribeRequest,
    ASRTranscribeResponse,
)
from ..services.quota_service import QuotaService
from ..services.router_policy import choose_asr_model
from ..services.session_service import SessionService
from ..utils.audio import read_upload
from ..utils.ids import prefixed_id
from aether_common.auth import AuthContext, ensure_scopes
from aether_common.settings import Settings

router = APIRouter(tags=["asr"])


async def parse_transcribe_request(request: Request) -> tuple[ASRTranscribeRequest, UploadFile | None]:
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        payload = ASRTranscribeRequest.model_validate(await request.json())
        return payload, None
    form = await request.form()
    metadata = form.get("metadata")
    payload = ASRTranscribeRequest(
        model=form.get("model", "auto"),
        task=form.get("task", "transcribe"),
        language=form.get("language", "auto"),
        timestamps=form.get("timestamps", "true") in {"true", "True", True},
        diarization=form.get("diarization", "false") in {"true", "True", True},
        response_format=form.get("response_format", "json"),
        storage_mode=form.get("storage_mode", "persist"),
        metadata=json.loads(metadata) if isinstance(metadata, str) and metadata else {},
        audio_url=form.get("audio_url"),
    )
    file = form.get("file")
    return payload, file if isinstance(file, (UploadFile, StarletteUploadFile)) else None


@router.post("/v1/asr/transcribe", response_model=ASRTranscribeResponse)
async def transcribe(
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    quota_service: QuotaService = Depends(get_quota_service),
    asr_client: ASRClient = Depends(get_asr_client),
    session_service: SessionService = Depends(get_session_service),
) -> ASRTranscribeResponse:
    ensure_scopes(auth, {"voice:asr"})
    await quota_service.check(auth, "/v1/asr/transcribe")
    payload, upload = await parse_transcribe_request(request)
    if upload is None:
        raise HTTPException(status_code=400, detail="ASR batch transcription requires multipart form-data with a 'file' field.")
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    session_id = prefixed_id("sess")
    settings = get_settings()
    model_used = choose_asr_model(
        payload.model,
        streaming=False,
        language=payload.language,
        task=payload.task,
        settings=settings,
    )
    metadata = payload.metadata.model_dump()
    metadata["tenant_id"] = auth.tenant_id
    await session_service.create_session(session_id, auth.tenant_id, "asr_batch", payload.model, model_used, metadata)
    audio_bytes, filename, content_type = await read_upload(upload)
    internal_payload = payload.model_dump()
    internal_payload["model"] = model_used
    internal_payload["metadata"] = metadata
    try:
        result = await asr_client.transcribe(
            internal_payload,
            audio_bytes=audio_bytes,
            filename=filename,
            content_type=content_type,
            request_id=request_id,
            session_id=session_id,
            tenant_id=auth.tenant_id,
        )
    except ASRUpstreamError as exc:
        await session_service.record_request(
            request_id,
            session_id,
            "asr_transcribe",
            "/v1/asr/transcribe",
            payload.model,
            model_used,
            "error",
            {"total_ms": 0},
            error_message=exc.detail,
        )
        raise HTTPException(status_code=exc.status_code if 400 <= exc.status_code < 500 else 502, detail=exc.detail) from exc
    await session_service.record_request(
        request_id,
        session_id,
        "asr_transcribe",
        "/v1/asr/transcribe",
        payload.model,
        result["model_used"],
        "ok",
        result["timings"],
        audio_duration_ms=result.get("duration_ms"),
        fallback_used=result["model_used"] != model_used,
    )
    await session_service.save_transcript(
        session_id,
        result.get("language_detected"),
        result["text"],
        result["segments"],
    )
    return ASRTranscribeResponse.model_validate(result)


@router.post("/v1/asr/stream/start", response_model=ASRStreamStartResponse)
async def start_stream(
    payload: ASRStreamStartRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    quota_service: QuotaService = Depends(get_quota_service),
    asr_client: ASRClient = Depends(get_asr_client),
    session_service: SessionService = Depends(get_session_service),
) -> ASRStreamStartResponse:
    ensure_scopes(auth, {"voice:asr"})
    await quota_service.check(auth, "/v1/asr/stream/start")
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    session_id = prefixed_id("sess_live")
    settings = get_settings()
    model_used = choose_asr_model(payload.model, streaming=True, language=payload.language, triage_enabled=payload.triage_enabled, settings=settings)
    metadata = payload.metadata.model_dump()
    metadata["tenant_id"] = auth.tenant_id
    await session_service.create_session(session_id, auth.tenant_id, "asr_stream", payload.model, model_used, metadata)
    internal_payload = payload.model_dump()
    internal_payload["model"] = model_used
    internal_payload["metadata"] = metadata
    await asr_client.start_stream(internal_payload, request_id=request_id, session_id=session_id, tenant_id=auth.tenant_id)
    return ASRStreamStartResponse(session_id=session_id, ws_url=f"/v1/asr/stream/{session_id}", expires_in_seconds=3600)


@router.websocket("/v1/asr/stream/{session_id}")
async def stream_proxy(websocket: WebSocket, session_id: str) -> None:
    settings: Settings = get_settings()
    await websocket.accept()
    upstream_url = f"{settings.gateway_asr_ws_url}/internal/stream/{session_id}"
    logger.info("gateway_stream_proxy_connecting", extra={"session_id": session_id, "upstream_url": upstream_url})
    try:
        async with websockets.connect(upstream_url, max_size=None) as upstream:
            logger.info("gateway_stream_proxy_connected", extra={"session_id": session_id, "upstream_url": upstream_url})
            async def client_to_upstream() -> None:
                while True:
                    message = await websocket.receive_text()
                    await upstream.send(message)

            async def upstream_to_client() -> None:
                async for message in upstream:
                    await websocket.send_text(message)

            await asyncio.gather(client_to_upstream(), upstream_to_client())
    except WebSocketDisconnect:
        logger.info("gateway_stream_proxy_disconnected", extra={"session_id": session_id})
        return
    except Exception as exc:
        logger.error(
            "gateway_stream_proxy_failed",
            extra={"session_id": session_id, "upstream_url": upstream_url, "error": repr(exc)},
        )
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)


@router.post("/v1/asr/triage", response_model=ASRTriageResponse)
async def triage(
    payload: ASRTriageRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    asr_client: ASRClient = Depends(get_asr_client),
    session_service: SessionService = Depends(get_session_service),
) -> ASRTriageResponse:
    ensure_scopes(auth, {"voice:triage"})
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    result = await asr_client.triage(payload.model_dump(), request_id=request_id, tenant_id=auth.tenant_id)
    await session_service.save_triage_result(payload.session_id, result, payload.domain)
    return ASRTriageResponse.model_validate(result)


@router.post("/v1/asr/analyze", response_model=ASRAnalyzeResponse)
async def analyze(
    payload: ASRAnalyzeRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    asr_client: ASRClient = Depends(get_asr_client),
) -> ASRAnalyzeResponse:
    ensure_scopes(auth, {"voice:asr"})
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    result = await asr_client.analyze(payload.model_dump(), request_id=request_id, tenant_id=auth.tenant_id)
    return ASRAnalyzeResponse.model_validate(result)
