"""Logger factory for Xinoobie Photobooth."""

from __future__ import annotations

import logging.handlers
from datetime import date
from pathlib import Path

from app_core.config import Config

_config = Config.instance()
_log_dir = _config.log_dir


def get_logger(name: str = "xinoobie") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                          datefmt="%H:%M:%S")
    )
    logger.addHandler(console)

    # Rotating file handler
    log_path = _log_dir / f"xinoobie_{date.today().strftime('%Y%m%d')}.log"
    _log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s | "
            "%(filename)s:%(lineno)d",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
