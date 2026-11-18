"""App Core — shared services for Xinoobie Photobooth."""

from __future__ import annotations

from .config import Config
from .logging_config import get_logger
from .error_handler import handle_exception

# Instantiate the global logger
logger = get_logger("xinoobie.app_core")

# Configuration singleton
config = Config.instance()

__all__ = ["config", "logger"]
