from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Response

from aether_common.postgres import PostgresPool
from aether_common.redis import RedisManager
from aether_common.storage import StorageManager
from aether_common.telemetry import metrics_content_type, metrics_payload

from .clients.asr_client import ASRClient
from .clients.tts_client import TTSClient
from .config import get_settings
from .dependencies import get_asr_client, get_tts_client
from .logging import logger
from .middleware.metrics import MetricsMiddleware
from .middleware.request_id import RequestIDMiddleware
from .routers import asr, health, metrics, models, sessions, tts
from .services.quota_service import QuotaService
from .services.session_service import SessionService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = PostgresPool(settings.postgres_url)
    await db.open()
    redis_manager = RedisManager(settings.redis_url)
    redis = await redis_manager.connect()
    storage = StorageManager(
        settings.s3_endpoint,
        settings.s3_access_key,
        settings.s3_secret_key,
        settings.s3_region,
        settings.local_storage_root,
    )
    for bucket in (
        settings.s3_bucket_raw,
        settings.s3_bucket_normalized,
        settings.s3_bucket_transcripts,
        settings.s3_bucket_tts,
        settings.s3_bucket_debug,
    ):
        storage.ensure_bucket(bucket)
    app.state.settings = settings
    app.state.db = db
    app.state.redis = redis
    app.state.storage = storage
    app.state.asr_client = ASRClient(settings.gateway_asr_base_url)
    app.state.tts_client = TTSClient(settings.gateway_tts_base_url)
    app.state.quota_service = QuotaService()
    app.state.session_service = SessionService(db, redis)
    logger.info("gateway_started")
    try:
        yield
    finally:
        await app.state.asr_client.close()
        await app.state.tts_client.close()
        await redis_manager.close()
        await db.close()
        logger.info("gateway_stopped")


app = FastAPI(
    title="Aether Voice Gateway",
    version="1.0.0",
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
    lifespan=lifespan,
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(MetricsMiddleware, service_name=settings.service_name)
app.include_router(health.router)
app.include_router(models.router)
app.include_router(asr.router)
app.include_router(tts.router)
app.include_router(sessions.router)
app.include_router(metrics.router)
app.include_router(health.router, prefix="/api", include_in_schema=False)
app.include_router(models.router, prefix="/api", include_in_schema=False)
app.include_router(asr.router, prefix="/api", include_in_schema=False)
app.include_router(tts.router, prefix="/api", include_in_schema=False)
app.include_router(sessions.router, prefix="/api", include_in_schema=False)
app.include_router(metrics.router, prefix="/api", include_in_schema=False)


@app.get("/metrics", include_in_schema=False)
async def internal_metrics() -> Response:
    return Response(content=metrics_payload(), media_type=metrics_content_type())


@app.get("/api/health", include_in_schema=False)
async def compatibility_health(asr_client: ASRClient = Depends(get_asr_client), tts_client: TTSClient = Depends(get_tts_client)):
    return await health.health(asr_client=asr_client, tts_client=tts_client)
