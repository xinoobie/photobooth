"""Structured logging setup for Xinoobie Photobooth."""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

from .config import Config

def setup_logging(config: Config | None = None) -> None:
    """Ensure logging is configured and ready."""
    log_dir = (config or _config).log_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    get_logger("xinoobie.app_core.logging_config").info("Logging initialized")


__all__ = ["get_logger", "setup_logging"]

_config = Config.instance()
_log_dir = _config.log_dir

_logger = logging.getLogger("xinoobie.app_core.logging_config")


def _get_logger_name() -> str:
    # Logger name = module path without 'src'
    import inspect
    frame = inspect.currentframe()
    module_name = ""
    if frame:
        module_name = frame.f_globals.get("__name__", "xinoobie")
    return module_name.rsplit(".", 1)[-1]


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance, configured once for the application."""
    logger_name = name or _get_logger_name()
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    # File handler (DEBUG and above)
    log_file = _log_dir / f"xinoobie_{Path(__import__('datetime').date.today().strftime('%Y%m%d'))}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s | "
        "%(filename)s:%(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
