from .settings import Settings, get_settings
from .telemetry import configure_logging

try:
    from .auth import AuthContext
    from .postgres import PostgresPool
    from .redis import RedisManager
    from .storage import StorageManager
except ModuleNotFoundError:  # pragma: no cover - allows lightweight imports in test contexts
    AuthContext = None  # type: ignore[assignment]
    PostgresPool = None  # type: ignore[assignment]
    RedisManager = None  # type: ignore[assignment]
    StorageManager = None  # type: ignore[assignment]

__all__ = [
    "AuthContext",
    "PostgresPool",
    "RedisManager",
    "Settings",
    "StorageManager",
    "configure_logging",
    "get_settings",
]
