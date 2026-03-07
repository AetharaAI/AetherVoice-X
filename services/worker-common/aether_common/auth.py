from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable

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


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


async def resolve_auth_context(
    request: Request,
    settings: Settings,
    db: PostgresPool,
    authorization: str | None = Header(default=None),
) -> AuthContext:
    api_key = request.headers.get(settings.api_key_header)
    if api_key:
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
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token") from exc
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
