from aether_common.telemetry import configure_logging

from .config import get_settings


logger = configure_logging(get_settings().service_name, get_settings().log_level)
