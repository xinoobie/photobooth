"""Storage Engine - manage photo storage and backup.

Features:
- Photo file management
- Automatic backup
- Storage usage
- Cleanup expired files
- Safe storage (not in temp)
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir

config = Config.instance()
logger = get_logger("xinoobie.storage_engine")


class StorageManager:
    """Manages photo storage."""

    def __init__(self, storage_dir: str | None = None):
        self.storage_dir = storage_dir or os.path.join(config.data_dir, "photos")
        ensure_dir(self.storage_dir)

        # Subdirectories
        self._captures_dir = os.path.join(self.storage_dir, "captures")
        self._final_dir = os.path.join(self.storage_dir, "final")
        self._processed_dir = os.path.join(self.storage_dir, "processed")
        self._temp_dir = os.path.join(self.storage_dir, "temp")

        # Auto-cleanup config
        self._max_storage_mb = 1000  # 1 GB
        self._retention_days = 30

        ensure_dir(self._captures_dir)
        ensure_dir(self._final_dir)
        ensure_dir(self._processed_dir)
        ensure_dir(self._temp_dir)

    def save_capture(self, file_path: str, session_id: str,
                     order: int = 0) -> str:
        """Save a capture photo."""
        base = os.path.basename(file_path)
        ext = os.path.splitext(base)[1]
        safe_name = f"session_{session_id}_{order}_{datetime.now().strftime('%H%M%S')}{ext}"
        dest = os.path.join(self._captures_dir, safe_name)
        shutil.copy2(file_path, dest)
        logger.info("Capture saved: %s", dest)
        return dest

    def save_final_photo(self, img_path: str, session_id: str,
                         photo_id: str, layout: str) -> str:
        """Save a final processed photo."""
        safe_name = f"session_{session_id}_photo_{photo_id}_{layout}.png"
        dest = os.path.join(self._final_dir, safe_name)
        shutil.copy2(img_path, dest)
        logger.info("Final photo saved: %s", dest)
        return dest

    def get_storage_usage(self) -> dict:
        """Get storage usage statistics."""
        usage = {}
        for label, d in [("captures", self._captures_dir),
                         ("final", self._final_dir),
                         ("processed", self._processed_dir)]:
            total = 0
            count = 0
            if os.path.exists(d):
                for f in os.listdir(d):
                    fpath = os.path.join(d, f)
                    if os.path.isfile(fpath):
                        total += os.path.getsize(fpath)
                        count += 1
            usage[label] = {
                "path": d,
                "total_bytes": total,
                "total_mb": total / (1024 * 1024),
                "file_count": count,
            }
        return usage

    def cleanup_old_photos(self):
        """Remove photos older than retention period."""
        cutoff = datetime.now(timezone.utc).timestamp() - (self._retention_days * 86400)
        cleaned = 0
        for d in [self._captures_dir, self._final_dir, self._processed_dir]:
            if not os.path.exists(d):
                continue
            for f in os.listdir(d):
                fpath = os.path.join(d, f)
                if os.path.isfile(fpath):
                    try:
                        if os.path.getmtime(fpath) < cutoff:
                            os.remove(fpath)
                            cleaned += 1
                    except Exception as exc:
                        logger.warning("Failed to delete %s: %s", fpath, exc)
        logger.info("Cleaned %d old photos", cleaned)

    def get_total_usage_mb(self) -> float:
        """Get total storage usage in MB."""
        total = 0
        for d in [self._captures_dir, self._final_dir, self._processed_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    fpath = os.path.join(d, f)
                    if os.path.isfile(fpath):
                        total += os.path.getsize(fpath)
        return total / (1024 * 1024)
