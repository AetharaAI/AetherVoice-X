from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/internal/health")
async def health(request: Request) -> dict:
    return {"status": "ok", "service": "tts", "models": [model["name"] for model in request.app.state.registry.model_info()]}


@router.get("/internal/models")
async def models(request: Request) -> dict:
    return {"models": request.app.state.registry.model_info()}
