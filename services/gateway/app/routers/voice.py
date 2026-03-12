from __future__ import annotations

from urllib.parse import quote

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from ..clients.tts_client import TTSClient
from ..dependencies import get_auth_context, get_quota_service, get_session_service, get_tts_client
from ..schemas.voice import VoiceTurnRequest, VoiceTurnResponse
from ..services.quota_service import QuotaService
from ..services.router_policy import choose_tts_model
from ..services.session_service import SessionService
from ..utils.ids import prefixed_id
from aether_common.auth import AuthContext, ensure_scopes
from aether_common.settings import Settings

router = APIRouter(tags=["voice"])


def _browser_artifact_url(storage_uri: str) -> str:
    return f"/api/v1/tts/artifacts/download?uri={quote(storage_uri, safe='')}"


@router.post("/v1/voice/turn", response_model=VoiceTurnResponse)
async def voice_turn(
    payload: VoiceTurnRequest,
    request: Request,
    auth: AuthContext = Depends(get_auth_context),
    quota_service: QuotaService = Depends(get_quota_service),
    tts_client: TTSClient = Depends(get_tts_client),
    session_service: SessionService = Depends(get_session_service),
) -> VoiceTurnResponse:
    ensure_scopes(auth, {"voice:tts"})
    await quota_service.check(auth, "/v1/voice/turn")
    request_id = getattr(request.state, "request_id", prefixed_id("req"))
    session_id = prefixed_id("sess_voice")
    settings: Settings = request.app.state.settings
    routing = await tts_client.studio_routing()
    tts_model = choose_tts_model(payload.tts_model, streaming=False, context_mode="batch", settings=settings)
    metadata = payload.metadata.model_dump()
    metadata["tenant_id"] = auth.tenant_id
    extra = dict(metadata.get("extra") or {})
    extra.update(
        {
            "source_transcript_text": payload.transcript_text,
            "asr_session_id": extra.get("asr_session_id"),
            "voice_turn_mode": "asr_llm_tts",
            "llm_routing_provider": routing.get("provider"),
            "llm_routing_model": routing.get("model"),
        }
    )
    metadata["extra"] = extra
    model_requested = f"llm:{routing.get('model') or 'unconfigured'} | tts:{payload.tts_model}"
    initial_model_used = f"llm:{routing.get('model') or 'unconfigured'} | tts:{tts_model}"
    await session_service.create_session(session_id, auth.tenant_id, "voice_turn", model_requested, initial_model_used, metadata)
    await session_service.save_transcript(session_id, None, payload.transcript_text, [])

    internal_payload = payload.model_dump()
    internal_payload["tts_model"] = tts_model
    internal_payload["metadata"] = metadata
    try:
        result = await tts_client.voice_turn(internal_payload, request_id=request_id, session_id=session_id, tenant_id=auth.tenant_id)
    except httpx.HTTPStatusError as exc:
        detail = tts_client._upstream_error_detail(exc.response, "voice turn")
        await session_service.record_request(
            request_id,
            session_id,
            "voice_turn",
            "/v1/voice/turn",
            model_requested,
            initial_model_used,
            "error",
            {"total_ms": 0},
            error_message=detail,
        )
        raise HTTPException(status_code=exc.response.status_code if 400 <= exc.response.status_code < 500 else 502, detail=detail) from exc
    except httpx.RequestError as exc:
        detail = f"tts voice turn failed: {exc}"
        await session_service.record_request(
            request_id,
            session_id,
            "voice_turn",
            "/v1/voice/turn",
            model_requested,
            initial_model_used,
            "error",
            {"total_ms": 0},
            error_message=detail,
        )
        raise HTTPException(status_code=502, detail=detail) from exc
    storage_uri = result["audio_url"]
    artifacts = dict(result.get("artifacts") or {})
    artifacts.setdefault("storage_uri", storage_uri)
    artifacts.setdefault("asr_session_id", extra.get("asr_session_id"))
    result["artifacts"] = artifacts
    result["audio_url"] = _browser_artifact_url(storage_uri)
    await session_service.record_request(
        request_id,
        session_id,
        "voice_turn",
        "/v1/voice/turn",
        model_requested,
        f"llm:{result['llm_model_used']} | tts:{result['tts_model_used']}",
        "ok",
        {"inference_ms": result["timings"]["total_ms"], "total_ms": result["timings"]["total_ms"]},
        audio_duration_ms=result["duration_ms"],
        fallback_used=result["tts_model_used"] != tts_model,
    )
    await session_service.save_tts_output(
        session_id,
        result["tts_model_used"],
        payload.voice,
        result["response_text"],
        storage_uri,
        result["duration_ms"],
    )
    result["session_id"] = session_id
    return VoiceTurnResponse.model_validate(result)
