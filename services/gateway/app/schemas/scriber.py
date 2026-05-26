from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


PlanSlug = Literal["founder", "pro", "studio"]
EntitlementStatus = Literal["trial", "active", "paywalled", "past_due", "canceled"]


class ScriberBootstrapRequest(BaseModel):
    install_id: str = Field(min_length=8, max_length=128)
    app_version: str | None = Field(default=None, max_length=64)
    platform: str | None = Field(default="linux", max_length=64)


class ScriberEntitlementResponse(BaseModel):
    install_id: str
    session_token: str | None = None
    entitlement_status: EntitlementStatus
    plan_slug: str | None = None
    free_seconds_granted: int
    free_seconds_used: int
    free_seconds_remaining: int
    can_transcribe: bool
    checkout_pending: bool = False


class ScriberCheckoutRequest(BaseModel):
    install_id: str = Field(min_length=8, max_length=128)
    plan_slug: PlanSlug
    app_version: str | None = Field(default=None, max_length=64)


class ScriberCheckoutResponse(BaseModel):
    checkout_url: str
    checkout_session_id: str
    plan_slug: PlanSlug


class ScriberAuthSessionRequest(BaseModel):
    install_id: str = Field(min_length=8, max_length=128)
    access_token: str = Field(min_length=16)
    id_token: str = Field(min_length=16)
    app_version: str | None = Field(default=None, max_length=64)
    platform: str | None = Field(default="linux", max_length=64)


class ScriberAuthUserResponse(BaseModel):
    subject: str
    email: str | None = None
    preferred_username: str | None = None
    roles: list[str] = Field(default_factory=list)


class ScriberAuthSessionResponse(ScriberEntitlementResponse):
    user: ScriberAuthUserResponse
