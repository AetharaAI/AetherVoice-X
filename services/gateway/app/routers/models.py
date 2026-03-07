from __future__ import annotations

from fastapi import APIRouter, Depends

from ..clients.asr_client import ASRClient
from ..clients.tts_client import TTSClient
from ..dependencies import get_asr_client, get_auth_context, get_tts_client
from ..schemas.common import ModelCatalogResponse
from aether_common.auth import AuthContext, ensure_scopes

router = APIRouter(tags=["models"])


@router.get("/v1/models", response_model=ModelCatalogResponse)
async def list_models(
    auth: AuthContext = Depends(get_auth_context),
    asr_client: ASRClient = Depends(get_asr_client),
    tts_client: TTSClient = Depends(get_tts_client),
) -> ModelCatalogResponse:
    ensure_scopes(auth, {"voice:asr"})
    models = await asr_client.models()
    models.extend(await tts_client.models())
    return ModelCatalogResponse(models=models)
