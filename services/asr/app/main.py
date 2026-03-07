from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from aether_common.postgres import PostgresPool
from aether_common.redis import RedisManager
from aether_common.storage import StorageManager
from aether_common.telemetry import metrics_content_type, metrics_payload

from .config import get_settings
from .logging import logger
from .routers import analyze, health, stream, transcribe, triage
from .services.model_registry import ModelRegistry
from .services.streaming_service import StreamingService
from .services.telemetry_service import TelemetryService
from .services.transcription_service import TranscriptionService
from .services.triage_service import TriageService

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
        settings.s3_bucket_debug,
    ):
        storage.ensure_bucket(bucket)
    registry = ModelRegistry()
    app.state.db = db
    app.state.redis = redis
    app.state.storage = storage
    app.state.registry = registry
    app.state.transcription_service = TranscriptionService(registry, storage, settings)
    app.state.streaming_service = StreamingService(registry, redis, TelemetryService())
    app.state.triage_service = TriageService()
    logger.info("asr_started")
    try:
        yield
    finally:
        await redis_manager.close()
        await db.close()
        logger.info("asr_stopped")


app = FastAPI(
    title="Aether Voice ASR",
    version="1.0.0",
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
    lifespan=lifespan,
)
app.include_router(health.router)
app.include_router(transcribe.router)
app.include_router(stream.router)
app.include_router(triage.router)
app.include_router(analyze.router)


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=metrics_payload(), media_type=metrics_content_type())
