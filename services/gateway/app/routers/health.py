from __future__ import annotations

from fastapi import APIRouter, Depends

from ..clients.asr_client import ASRClient
from ..clients.tts_client import TTSClient
from ..dependencies import get_asr_client, get_tts_client
from ..schemas.common import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/v1/health", response_model=HealthStatus)
async def health(asr_client: ASRClient = Depends(get_asr_client), tts_client: TTSClient = Depends(get_tts_client)) -> HealthStatus:
    dependencies = {"asr": "unknown", "tts": "unknown"}
    try:
        dependencies["asr"] = (await asr_client.health())["status"]
    except Exception:
        dependencies["asr"] = "degraded"
    try:
        dependencies["tts"] = (await tts_client.health())["status"]
    except Exception:
        dependencies["tts"] = "degraded"
    overall = "ok" if all(value == "ok" for value in dependencies.values()) else "degraded"
    return HealthStatus(status=overall, service="gateway", dependencies=dependencies)
