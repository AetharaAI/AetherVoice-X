from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from aether_common.postgres import PostgresPool
from aether_common.redis import RedisManager
from aether_common.storage import StorageManager
from aether_common.telemetry import metrics_content_type, metrics_payload

from .config import get_settings
from .logging import logger
from .routers import health, stream, studio, synthesize
from .services.model_registry import ModelRegistry
from .services.streaming_service import StreamingService
from .services.studio_service import StudioService
from .services.synthesis_service import SynthesisService
from .services.telemetry_service import TelemetryService

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
    storage.ensure_bucket(settings.s3_bucket_tts)
    registry = ModelRegistry()
    studio_service = StudioService(settings)
    synthesis_service = SynthesisService(registry, storage, settings)
    app.state.db = db
    app.state.redis = redis
    app.state.storage = storage
    app.state.registry = registry
    app.state.studio_service = studio_service
    app.state.synthesis_service = synthesis_service
    app.state.streaming_service = StreamingService(registry, synthesis_service, redis, TelemetryService(), storage, settings, studio_service)
    logger.info("tts_started")
    try:
        yield
    finally:
        await registry.close()
        await redis_manager.close()
        await db.close()
        logger.info("tts_stopped")


app = FastAPI(
    title="Aether Voice TTS",
    version="1.0.0",
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
    lifespan=lifespan,
)
app.include_router(health.router)
app.include_router(synthesize.router)
app.include_router(stream.router)
app.include_router(studio.router)


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=metrics_payload(), media_type=metrics_content_type())
