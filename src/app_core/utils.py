"""Utility functions used across the application."""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path
from typing import Any

import log_utils
import logging

logger = logging.getLogger("xinoobie.app_core.utils")


def atomic_save(file_path: Path, data: bytes, max_retries: int = 3) -> Path:
    """Write a file atomically: write to temp, then rename.

    Guarantees the file is not partially written if the process crashes.
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Use .tmp suffix for the temporary file
    tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    for attempt in range(max_retries):
        try:
            tmp_path.write_bytes(data)
            # Flush and fsync to persist
            tmp_path.flush()
            os.fsync(tmp_path.fileno())
            # Atomic rename on same filesystem
            shutil.move(str(tmp_path), str(file_path))
            logger.debug("Atomic save: %s (%d bytes)", file_path, len(data))
            return file_path
        except OSError as exc:
            logger.warning("Atomic save attempt %d failed: %s", attempt + 1, exc)
            if tmp_path.exists():
                tmp_path.unlink()
            if attempt == max_retries - 1:
                raise
    raise RuntimeError("Unreachable fallback in atomic_save")


def generate_session_id(prefix: str = "S") -> str:
    """Generate a unique session identifier."""
    timestamp = uuid.uuid4().hex[:8].upper()
    return f"{prefix}-{timestamp}"


def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist. Silent if already exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_size(file_path: Path) -> int:
    """Return file size in bytes. Returns 0 if file does not exist."""
    p = Path(file_path)
    return p.stat().st_size if p.exists() else 0


def is_image_file(file_path: Path) -> bool:
    """Check if a file has an image extension."""
    suffix = Path(file_path).suffix.lower()
    return suffix in {
        ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif", ".gif",
    }


def resolve_photo_path(session_id: str, photo_index: int, ext: str = ".jpg") -> Path:
    """Generate a storage path for a session photo.

    Layout: storage/<session_id>/<photo_index><ext>
    """
    return Path("storage") / session_id / f"{photo_index}{ext}"


def path_to_relative_storage(path: Path) -> str:
    """Convert an absolute storage path to a relative one (for logging/DB)."""
    return str(Path(path).resolve().relative_to(Path.cwd()))
