from __future__ import annotations

from fastapi import APIRouter, Depends, Response

from ..dependencies import get_auth_context
from aether_common.auth import AuthContext, ensure_scopes
from aether_common.telemetry import metrics_content_type, metrics_payload

router = APIRouter(tags=["metrics"])


@router.get("/v1/metrics")
async def get_metrics(auth: AuthContext = Depends(get_auth_context)) -> Response:
    ensure_scopes(auth, {"voice:metrics:read"})
    return Response(content=metrics_payload(), media_type=metrics_content_type())
