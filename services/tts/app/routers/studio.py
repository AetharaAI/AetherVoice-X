from __future__ import annotations

from fastapi import APIRouter, File, Form, Header, HTTPException, Request, UploadFile

from ..schemas.studio import LLMRoutingConfig, VoiceCreateRequest

router = APIRouter(tags=["studio"])


@router.get("/internal/studio/overview")
async def studio_overview(
    request: Request,
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    return request.app.state.studio_service.overview(x_tenant_id).model_dump()


@router.get("/internal/studio/voices")
async def list_voices(
    request: Request,
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    voices = request.app.state.studio_service.list_voices(x_tenant_id)
    return {"voices": [voice.model_dump() for voice in voices]}


@router.post("/internal/studio/voices")
async def create_voice(
    payload: VoiceCreateRequest,
    request: Request,
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    voice = request.app.state.studio_service.create_voice(x_tenant_id, payload)
    return voice.model_dump()


@router.post("/internal/studio/voices/import")
async def import_voice(
    request: Request,
    file: UploadFile = File(...),
    display_name: str = Form(...),
    source_model: str = Form(...),
    runtime_target: str = Form(...),
    notes: str | None = Form(default=None),
    tags: str = Form(default=""),
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    payload = await file.read()
    voice = request.app.state.studio_service.import_voice_asset(
        tenant_id=x_tenant_id,
        filename=file.filename or "reference.wav",
        payload=payload,
        display_name=display_name,
        source_model=source_model,
        runtime_target=runtime_target,
        notes=notes,
        tags=[tag.strip() for tag in tags.split(",") if tag.strip()],
    )
    return voice.model_dump()


@router.get("/internal/studio/providers")
async def list_providers(request: Request) -> dict:
    return {"providers": [provider.model_dump() for provider in request.app.state.studio_service.list_providers()]}


@router.get("/internal/studio/providers/{provider}/models")
async def list_provider_models(provider: str, request: Request) -> dict:
    models = await request.app.state.studio_service.list_provider_models(provider)
    return {"models": [model.model_dump() for model in models]}


@router.get("/internal/studio/routing")
async def get_routing(request: Request) -> dict:
    return request.app.state.studio_service.get_routing().model_dump()


@router.post("/internal/studio/routing")
async def save_routing(payload: LLMRoutingConfig, request: Request) -> dict:
    return request.app.state.studio_service.save_routing(payload).model_dump()


@router.post("/internal/studio/routes/{route_name}/warmup")
async def warm_route(
    route_name: str,
    request: Request,
    x_tenant_id: str = Header(alias="X-Tenant-Id"),
) -> dict:
    adapter = request.app.state.registry.get(route_name)
    try:
        result = await adapter.warmup({"tenant_id": x_tenant_id, "source": "tts_studio"})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    overview = request.app.state.studio_service.overview(x_tenant_id).model_dump()
    return {
        "route": route_name,
        "warmup": result,
        "overview": overview,
    }
