from __future__ import annotations

from pydantic import BaseModel, Field

from aether_common.schemas import ModelInfo


class HealthStatus(BaseModel):
    status: str
    service: str
    dependencies: dict[str, str] = Field(default_factory=dict)


class ModelCatalogResponse(BaseModel):
    models: list[ModelInfo]
