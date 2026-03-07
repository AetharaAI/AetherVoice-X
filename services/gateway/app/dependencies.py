from __future__ import annotations

from fastapi import Depends, Header, Request
from redis.asyncio import Redis

from aether_common.auth import AuthContext, resolve_auth_context
from aether_common.postgres import PostgresPool
from aether_common.settings import Settings
from aether_common.storage import StorageManager

from .clients.asr_client import ASRClient
from .clients.tts_client import TTSClient
from .services.quota_service import QuotaService
from .services.session_service import SessionService


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_db(request: Request) -> PostgresPool:
    return request.app.state.db


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_storage(request: Request) -> StorageManager:
    return request.app.state.storage


def get_asr_client(request: Request) -> ASRClient:
    return request.app.state.asr_client


def get_tts_client(request: Request) -> TTSClient:
    return request.app.state.tts_client


def get_quota_service(request: Request) -> QuotaService:
    return request.app.state.quota_service


def get_session_service(request: Request) -> SessionService:
    return request.app.state.session_service


async def get_auth_context(
    request: Request,
    settings: Settings = Depends(get_settings),
    db: PostgresPool = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> AuthContext:
    return await resolve_auth_context(request, settings, db, authorization)
