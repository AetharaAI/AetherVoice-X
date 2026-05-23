from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Iterable

import httpx
import jwt
from fastapi import Header, HTTPException, Request, status

from .postgres import PostgresPool
from .settings import Settings


@dataclass
class AuthContext:
    tenant_id: str
    subject: str = "local-operator"
    scopes: set[str] = field(default_factory=set)
    auth_type: str = "anonymous"
    api_key: str | None = None
    api_key_id: str | None = None
    user_id: str | None = None
    plan_slug: str | None = None
    install_id: str | None = None


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


async def _validate_platform_api_key(api_key: str, settings: Settings) -> dict[str, Any] | None:
    if not settings.platform_key_validation_url or not settings.platform_internal_secret:
        return None

    try:
        async with httpx.AsyncClient(timeout=settings.platform_internal_timeout_seconds) as client:
            response = await client.post(
                settings.platform_key_validation_url,
                json={"apiKey": api_key},
                headers={"x-platform-internal-secret": settings.platform_internal_secret},
            )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform key validation is unavailable",
        ) from exc

    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform key validation is unavailable",
        )

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform key validation is misconfigured",
        )

    if response.status_code not in {status.HTTP_200_OK, status.HTTP_403_FORBIDDEN}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform key validation returned an unexpected response",
        )

    payload = response.json()
    if payload.get("valid"):
        return payload
    return None


async def resolve_auth_context(
    request: Request,
    settings: Settings,
    db: PostgresPool,
    authorization: str | None = Header(default=None),
) -> AuthContext:
    api_key = request.headers.get(settings.api_key_header)
    if api_key:
        platform_result = await _validate_platform_api_key(api_key, settings)
        if platform_result:
            tenant_id = str(platform_result.get("tenantId") or platform_result.get("tenant_id") or settings.default_tenant_id)
            return AuthContext(
                tenant_id=tenant_id,
                subject=str(platform_result.get("userId") or platform_result.get("user_id") or "platform-api-key"),
                scopes=set(platform_result.get("scopes") or []),
                auth_type="platform_api_key",
                api_key=api_key,
                api_key_id=platform_result.get("apiKeyId") or platform_result.get("api_key_id"),
                user_id=platform_result.get("userId") or platform_result.get("user_id"),
                plan_slug=platform_result.get("planSlug") or platform_result.get("plan_slug"),
            )

        row = await db.fetch_one(
            """
            SELECT tenant_id
            FROM api_keys
            WHERE key_hash = %(key_hash)s AND is_active = TRUE
            """,
            {"key_hash": hash_api_key(api_key)},
        )
        if row:
            return AuthContext(
                tenant_id=str(row["tenant_id"]),
                subject="api-key",
                scopes={"voice:asr", "voice:tts", "voice:sessions:read", "voice:metrics:read", "voice:triage"},
                auth_type="api_key",
                api_key=api_key,
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token") from exc
        if payload.get("auth_type") == "scriber_install":
            return AuthContext(
                tenant_id=str(payload.get("tenant_id", settings.default_tenant_id)),
                subject=str(payload.get("sub", "scriber-install")),
                scopes=set(payload.get("scopes", [])),
                auth_type="scriber_install",
                plan_slug=payload.get("plan_slug"),
                install_id=payload.get("install_id"),
            )
        return AuthContext(
            tenant_id=str(payload.get("tenant_id", settings.default_tenant_id)),
            subject=str(payload.get("sub", "jwt-user")),
            scopes=set(payload.get("scopes", [])),
            auth_type="jwt",
        )

    if settings.auth_mode == "optional":
        return AuthContext(
            tenant_id=settings.default_tenant_id,
            scopes={"voice:asr", "voice:tts", "voice:sessions:read", "voice:metrics:read", "voice:triage"},
        )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")


def ensure_scopes(auth: AuthContext, required_scopes: Iterable[str]) -> None:
    missing = [scope for scope in required_scopes if scope not in auth.scopes]
    if missing:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scopes: {', '.join(missing)}")
