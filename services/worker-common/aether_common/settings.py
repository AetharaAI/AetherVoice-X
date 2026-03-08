from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = Field(default="unknown", validation_alias=AliasChoices("SERVICE_NAME"))
    app_env: str = Field(default="development", validation_alias=AliasChoices("APP_ENV"))
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("LOG_LEVEL"))
    auth_mode: Literal["optional", "strict"] = Field(default="optional", validation_alias=AliasChoices("AUTH_MODE"))

    jwt_secret: str = Field(default="change_me", validation_alias=AliasChoices("JWT_SECRET"))
    api_key_header: str = Field(default="X-API-Key", validation_alias=AliasChoices("API_KEY_HEADER"))

    postgres_url: str = Field(default="postgresql://voice:voice@localhost:5432/aether_voice", validation_alias=AliasChoices("POSTGRES_URL"))
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias=AliasChoices("REDIS_URL"))

    s3_endpoint: str | None = Field(default=None, validation_alias=AliasChoices("S3_ENDPOINT"))
    s3_access_key: str | None = Field(default=None, validation_alias=AliasChoices("S3_ACCESS_KEY"))
    s3_secret_key: str | None = Field(default=None, validation_alias=AliasChoices("S3_SECRET_KEY"))
    s3_region: str = Field(default="us-east-1", validation_alias=AliasChoices("S3_REGION"))
    s3_bucket_raw: str = Field(default="voice-raw-audio", validation_alias=AliasChoices("S3_BUCKET_RAW"))
    s3_bucket_normalized: str = Field(default="voice-normalized-audio", validation_alias=AliasChoices("S3_BUCKET_NORMALIZED"))
    s3_bucket_transcripts: str = Field(default="voice-transcripts", validation_alias=AliasChoices("S3_BUCKET_TRANSCRIPTS"))
    s3_bucket_tts: str = Field(default="voice-tts-output", validation_alias=AliasChoices("S3_BUCKET_TTS"))
    s3_bucket_debug: str = Field(default="voice-debug-artifacts", validation_alias=AliasChoices("S3_BUCKET_DEBUG"))
    local_storage_root: str = Field(default="/tmp/aether-storage", validation_alias=AliasChoices("LOCAL_STORAGE_ROOT"))

    gateway_host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("GATEWAY_HOST"))
    gateway_port: int = Field(default=8080, validation_alias=AliasChoices("GATEWAY_PORT"))
    asr_host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("ASR_HOST"))
    asr_port: int = Field(default=8090, validation_alias=AliasChoices("ASR_PORT"))
    tts_host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("TTS_HOST"))
    tts_port: int = Field(default=8091, validation_alias=AliasChoices("TTS_PORT"))
    frontend_port: int = Field(default=3000, validation_alias=AliasChoices("FRONTEND_PORT"))

    gateway_asr_base_url: str = Field(default="http://localhost:8090", validation_alias=AliasChoices("GATEWAY_ASR_BASE_URL"))
    gateway_tts_base_url: str = Field(default="http://localhost:8091", validation_alias=AliasChoices("GATEWAY_TTS_BASE_URL"))
    gateway_asr_ws_url: str = Field(default="ws://localhost:8090", validation_alias=AliasChoices("GATEWAY_ASR_WS_URL"))
    gateway_tts_ws_url: str = Field(default="ws://localhost:8091", validation_alias=AliasChoices("GATEWAY_TTS_WS_URL"))

    default_asr_model: str = Field(default="voxtral_realtime", validation_alias=AliasChoices("DEFAULT_ASR_MODEL", "DEFAULT_STREAM_ASR_MODEL"))
    default_batch_asr_model: str = Field(default="faster_whisper", validation_alias=AliasChoices("DEFAULT_BATCH_ASR_MODEL"))
    default_tts_model: str = Field(default="chatterbox", validation_alias=AliasChoices("DEFAULT_TTS_MODEL", "DEFAULT_BATCH_TTS_MODEL"))
    default_stream_tts_model: str = Field(default="moss_realtime", validation_alias=AliasChoices("DEFAULT_STREAM_TTS_MODEL"))

    enable_qwen3_asr: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_QWEN3_ASR"))
    enable_sentinel: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_SENTINEL"))
    enable_phi_overlay: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_PHI_OVERLAY"))
    enable_metrics: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_METRICS"))
    enable_swagger: bool = Field(default=True, validation_alias=AliasChoices("ENABLE_SWAGGER"))

    hf_token: str | None = Field(default=None, validation_alias=AliasChoices("HF_TOKEN"))
    hf_home: str | None = Field(default=None, validation_alias=AliasChoices("HF_HOME"))
    huggingface_hub_cache: str | None = Field(default=None, validation_alias=AliasChoices("HUGGINGFACE_HUB_CACHE"))
    transformers_cache: str | None = Field(default=None, validation_alias=AliasChoices("TRANSFORMERS_CACHE"))
    aether_model_root: str = Field(default="/models", validation_alias=AliasChoices("AETHER_MODEL_ROOT"))

    voxtral_model_id: str = Field(default="mistralai/Voxtral-Mini-4B-Realtime-2602", validation_alias=AliasChoices("VOXTRAL_MODEL_ID"))
    voxtral_http_base_url: str | None = Field(default=None, validation_alias=AliasChoices("VOXTRAL_HTTP_BASE_URL", "VOXTRAL_REALTIME_BASE_URL"))
    voxtral_ws_base_url: str | None = Field(default=None, validation_alias=AliasChoices("VOXTRAL_WS_BASE_URL", "VOXTRAL_REALTIME_WS_URL"))
    voxtral_api_key: str | None = Field(default=None, validation_alias=AliasChoices("VOXTRAL_API_KEY", "VOXTRAL_REALTIME_API_KEY"))
    voxtral_realtime_model_name: str | None = Field(default=None, validation_alias=AliasChoices("VOXTRAL_REALTIME_MODEL_NAME"))
    voxtral_realtime_timeout_seconds: float = Field(default=90.0, validation_alias=AliasChoices("VOXTRAL_REALTIME_TIMEOUT_SECONDS"))
    voxtral_stream_partial_window_ms: int = Field(default=480, validation_alias=AliasChoices("VOXTRAL_STREAM_PARTIAL_WINDOW_MS"))
    faster_whisper_model_size: str = Field(default="small", validation_alias=AliasChoices("FASTER_WHISPER_MODEL_SIZE"))
    qwen3_asr_model_id: str = Field(default="Qwen/Qwen3-ASR-1.7B", validation_alias=AliasChoices("QWEN3_ASR_MODEL_ID"))
    sentinel_model_id: str = Field(default="trishtan/voxtral-sentinel-4b", validation_alias=AliasChoices("SENTINEL_MODEL_ID"))
    phi_mm_model_id: str = Field(default="microsoft/Phi-4-multimodal-instruct", validation_alias=AliasChoices("PHI_MM_MODEL_ID"))
    chatterbox_base_url: str = Field(default="http://localhost:8000", validation_alias=AliasChoices("CHATTERBOX_BASE_URL"))
    chatterbox_default_voice: str = Field(default="Emily.wav", validation_alias=AliasChoices("CHATTERBOX_DEFAULT_VOICE"))
    moss_model_id: str = Field(default="OpenMOSS-Team/MOSS-TTS-Realtime", validation_alias=AliasChoices("MOSS_MODEL_ID"))

    faster_whisper_model_path: str | None = Field(default=None, validation_alias=AliasChoices("FASTER_WHISPER_MODEL_PATH"))
    voxtral_model_path: str | None = Field(default=None, validation_alias=AliasChoices("VOXTRAL_MODEL_PATH"))
    qwen3_asr_model_path: str | None = Field(default=None, validation_alias=AliasChoices("QWEN3_ASR_MODEL_PATH"))
    moss_model_path: str | None = Field(default=None, validation_alias=AliasChoices("MOSS_MODEL_PATH"))
    phi_mm_model_path: str | None = Field(default=None, validation_alias=AliasChoices("PHI_MM_MODEL_PATH"))

    asr_device: str = Field(default="cpu", validation_alias=AliasChoices("ASR_DEVICE"))
    asr_compute_type: str = Field(default="int8", validation_alias=AliasChoices("ASR_COMPUTE_TYPE"))
    asr_gpu_ids: str = Field(default="1", validation_alias=AliasChoices("ASR_GPU_IDS"))

    frontend_public_origin: str | None = Field(default=None, validation_alias=AliasChoices("FRONTEND_PUBLIC_ORIGIN"))
    vite_api_base_url: str | None = Field(default=None, validation_alias=AliasChoices("VITE_API_BASE_URL"))
    vite_ws_base_url: str | None = Field(default=None, validation_alias=AliasChoices("VITE_WS_BASE_URL"))

    default_tenant_id: str = "00000000-0000-0000-0000-000000000001"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
