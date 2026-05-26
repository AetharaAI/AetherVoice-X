from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from ..dependencies import get_scriber_service
from ..schemas.scriber import (
    ScriberAuthSessionRequest,
    ScriberAuthSessionResponse,
    ScriberBootstrapRequest,
    ScriberCheckoutRequest,
    ScriberCheckoutResponse,
    ScriberEntitlementResponse,
)
from ..services.scriber_service import ScriberService

router = APIRouter(tags=["scriber"])


@router.post("/v1/scriber/bootstrap", response_model=ScriberEntitlementResponse)
async def scriber_bootstrap(
    payload: ScriberBootstrapRequest,
    scriber_service: ScriberService = Depends(get_scriber_service),
) -> ScriberEntitlementResponse:
    await scriber_service.touch_install(
        payload.install_id,
        app_version=payload.app_version,
        platform=payload.platform,
    )
    snapshot = await scriber_service.get_snapshot(payload.install_id)
    session_token = scriber_service.issue_session_token(snapshot)
    return ScriberEntitlementResponse.model_validate(snapshot.to_payload(session_token))


@router.get("/v1/scriber/entitlement/{install_id}", response_model=ScriberEntitlementResponse)
async def scriber_entitlement(
    install_id: str,
    scriber_service: ScriberService = Depends(get_scriber_service),
) -> ScriberEntitlementResponse:
    snapshot = await scriber_service.get_snapshot(install_id)
    session_token = scriber_service.issue_session_token(snapshot)
    return ScriberEntitlementResponse.model_validate(snapshot.to_payload(session_token))


@router.post("/v1/scriber/checkout", response_model=ScriberCheckoutResponse)
async def scriber_checkout(
    payload: ScriberCheckoutRequest,
    scriber_service: ScriberService = Depends(get_scriber_service),
) -> ScriberCheckoutResponse:
    try:
        result = await scriber_service.create_checkout_session(
            payload.install_id,
            payload.plan_slug,
            app_version=payload.app_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ScriberCheckoutResponse.model_validate({
        **result,
        "plan_slug": payload.plan_slug,
    })


@router.post("/v1/scriber/auth/session", response_model=ScriberAuthSessionResponse)
async def scriber_auth_session(
    payload: ScriberAuthSessionRequest,
    scriber_service: ScriberService = Depends(get_scriber_service),
) -> ScriberAuthSessionResponse:
    try:
        result = await scriber_service.create_auth_session(
            payload.install_id,
            access_token=payload.access_token,
            id_token=payload.id_token,
            app_version=payload.app_version,
            platform=payload.platform,
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return ScriberAuthSessionResponse.model_validate(result)


@router.post("/v1/stripe/webhook")
async def scriber_stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="stripe-signature"),
    scriber_service: ScriberService = Depends(get_scriber_service),
) -> dict[str, bool]:
    body = await request.body()
    try:
        await scriber_service.handle_webhook(body, stripe_signature)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - upstream/SDK validation path
        raise HTTPException(status_code=400, detail=f"Stripe webhook failed: {exc}") from exc
    return {"ok": True}
