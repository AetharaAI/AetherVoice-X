from __future__ import annotations

import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
import jwt

sys.path.append(str(Path(__file__).resolve().parents[2] / "services" / "worker-common"))
psycopg_module = types.ModuleType("psycopg")
psycopg_rows_module = types.ModuleType("psycopg.rows")
psycopg_rows_module.dict_row = object()
psycopg_pool_module = types.ModuleType("psycopg_pool")


class _UnusedAsyncConnectionPool:
    def __init__(self, *args, **kwargs) -> None:
        _ = (args, kwargs)


psycopg_pool_module.AsyncConnectionPool = _UnusedAsyncConnectionPool
sys.modules.setdefault("psycopg", psycopg_module)
sys.modules.setdefault("psycopg.rows", psycopg_rows_module)
sys.modules.setdefault("psycopg_pool", psycopg_pool_module)

from aether_common.auth import resolve_auth_context


class DummyDB:
    def __init__(self, row=None) -> None:
        self.row = row

    async def fetch_one(self, _query: str, _params: dict) -> dict | None:
        return self.row


class DummyRequest:
    def __init__(self, api_key: str | None = None, authorization: str | None = None) -> None:
        self.headers = {}
        if api_key is not None:
            self.headers["X-API-Key"] = api_key
        if authorization is not None:
            self.headers["Authorization"] = authorization


@pytest.mark.asyncio
async def test_platform_validated_key_uses_platform_scopes(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_validate(api_key: str, settings) -> dict:
        assert api_key == "ap_live_test"
        assert settings.platform_key_validation_url == "https://platform.example/api/internal/keys/validate"
        return {
            "valid": True,
            "apiKeyId": "key_123",
            "userId": "user_123",
            "planSlug": "pro",
            "scopes": ["voice:asr", "voice:tts", "voice:turn"],
        }

    monkeypatch.setattr("aether_common.auth._validate_platform_api_key", fake_validate)

    settings = SimpleNamespace(
        api_key_header="X-API-Key",
        platform_key_validation_url="https://platform.example/api/internal/keys/validate",
        platform_internal_secret="secret",
        default_tenant_id="00000000-0000-0000-0000-000000000001",
        auth_mode="strict",
        jwt_secret="unused",
    )

    auth = await resolve_auth_context(DummyRequest("ap_live_test"), settings, DummyDB(), None)

    assert auth.auth_type == "platform_api_key"
    assert auth.tenant_id == "00000000-0000-0000-0000-000000000001"
    assert auth.api_key == "ap_live_test"
    assert auth.api_key_id == "key_123"
    assert auth.user_id == "user_123"
    assert auth.plan_slug == "pro"
    assert auth.scopes == {"voice:asr", "voice:tts", "voice:turn"}


@pytest.mark.asyncio
async def test_invalid_platform_key_falls_back_to_legacy_local_key_store(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_validate(_api_key: str, _settings):
        return None

    monkeypatch.setattr("aether_common.auth._validate_platform_api_key", fake_validate)

    settings = SimpleNamespace(
        api_key_header="X-API-Key",
        platform_key_validation_url="https://platform.example/api/internal/keys/validate",
        platform_internal_secret="secret",
        default_tenant_id="00000000-0000-0000-0000-000000000001",
        auth_mode="strict",
        jwt_secret="unused",
    )

    auth = await resolve_auth_context(
        DummyRequest("legacy_key"),
        settings,
        DummyDB({"tenant_id": "11111111-1111-1111-1111-111111111111"}),
        None,
    )

    assert auth.auth_type == "api_key"
    assert auth.tenant_id == "11111111-1111-1111-1111-111111111111"
    assert "voice:tts" in auth.scopes


@pytest.mark.asyncio
async def test_platform_validation_outage_returns_service_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_validate(_api_key: str, _settings):
        raise HTTPException(status_code=503, detail="Platform key validation is unavailable")

    monkeypatch.setattr("aether_common.auth._validate_platform_api_key", fake_validate)

    settings = SimpleNamespace(
        api_key_header="X-API-Key",
        platform_key_validation_url="https://platform.example/api/internal/keys/validate",
        platform_internal_secret="secret",
        default_tenant_id="00000000-0000-0000-0000-000000000001",
        auth_mode="strict",
        jwt_secret="unused",
    )

    with pytest.raises(HTTPException) as exc_info:
        await resolve_auth_context(DummyRequest("ap_live_test"), settings, DummyDB(), None)

    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_scriber_install_bearer_token_resolves_install_context() -> None:
    settings = SimpleNamespace(
        api_key_header="X-API-Key",
        platform_key_validation_url=None,
        platform_internal_secret=None,
        default_tenant_id="00000000-0000-0000-0000-000000000001",
        auth_mode="strict",
        jwt_secret="scriber-secret",
    )

    token = jwt.encode(
        {
            "sub": "scriber-install:install_123",
            "tenant_id": "00000000-0000-0000-0000-000000000001",
            "auth_type": "scriber_install",
            "install_id": "install_123",
            "plan_slug": "trial",
            "scopes": ["voice:asr"],
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

    auth = await resolve_auth_context(
        DummyRequest(authorization=f"Bearer {token}"),
        settings,
        DummyDB(),
        f"Bearer {token}",
    )

    assert auth.auth_type == "scriber_install"
    assert auth.install_id == "install_123"
    assert auth.plan_slug == "trial"
    assert auth.scopes == {"voice:asr"}
