from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from ..clients.tts_client import TTSClient
from ..dependencies import get_auth_context, get_tts_client
from aether_common.auth import AuthContext, ensure_scopes

router = APIRouter(tags=["tts-studio"])


@router.get("/v1/tts/studio/overview")
async def studio_overview(
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.studio_overview(tenant_id=auth.tenant_id)


@router.get("/v1/tts/studio/voices")
async def list_voices(
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.studio_voices(tenant_id=auth.tenant_id)


@router.post("/v1/tts/studio/voices")
async def create_voice(
    payload: dict,
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.create_studio_voice(payload, tenant_id=auth.tenant_id)


@router.post("/v1/tts/studio/voices/import")
async def import_voice(
    file: UploadFile = File(...),
    display_name: str = Form(...),
    source_model: str = Form(...),
    runtime_target: str = Form(...),
    notes: str | None = Form(default=None),
    tags: str = Form(default=""),
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.import_studio_voice(
        {
            "display_name": display_name,
            "source_model": source_model,
            "runtime_target": runtime_target,
            "notes": notes or "",
            "tags": tags,
        },
        {
            "file": (
                file.filename or "reference.wav",
                await file.read(),
                file.content_type or "audio/wav",
            )
        },
        tenant_id=auth.tenant_id,
    )


@router.get("/v1/tts/studio/providers")
async def list_providers(
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.studio_providers()


@router.get("/v1/tts/studio/providers/{provider}/models")
async def provider_models(
    provider: str,
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.studio_provider_models(provider)


@router.get("/v1/tts/studio/routing")
async def get_routing(
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.studio_routing()


@router.post("/v1/tts/studio/routing")
async def save_routing(
    payload: dict,
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    return await tts_client.save_studio_routing(payload)


@router.post("/v1/tts/studio/routes/{route_name}/warmup")
async def warm_route(
    route_name: str,
    auth: AuthContext = Depends(get_auth_context),
    tts_client: TTSClient = Depends(get_tts_client),
) -> dict:
    ensure_scopes(auth, {"voice:tts"})
    try:
        return await tts_client.warm_studio_route(route_name, tenant_id=auth.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
