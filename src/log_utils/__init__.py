"""Logging — Xinoobie Photobooth."""

from .logger import get_logger

logger = get_logger("xinoobie.logging")


def setup_logging() -> None:
    """Ensure logging is configured and ready."""
    log_file = __import__("pathlib").Path("logs") / "xinoobie.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Logging initialized")


__all__ = ["get_logger", "setup_logging"]
