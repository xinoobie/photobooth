"""Frame Engine - manage photo frames.

Features:
- Upload frames
- Delete frames
- Edit frames
- Preview frames
- Categorize frames
- Set frame price
- Enable/disable frames
- Set default frame
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir
from PIL import Image

config = Config.instance()
logger = get_logger("xinoobie.frame_engine")


@dataclass
class Frame:
    """A frame definition."""
    id: str
    name: str
    category: str
    path: str
    is_default: bool = False
    is_enabled: bool = True
    price: float = 0.0
    width: int = 1920
    height: int = 1080

    @property
    def display_name(self) -> str:
        """Get the display name (without path)."""
        return os.path.basename(self.path)


class FrameManager:
    """Manages frame assets."""

    def __init__(self, frame_dir: str | None = None):
        self.frame_dir = frame_dir or os.path.join(config.data_dir, "frames")
        ensure_dir(self.frame_dir)
        self._frames: dict[str, Frame] = {}
        self._default_frame: Optional[str] = None
        self._load_frames()

    def _load_frames(self):
        """Load all frames from the frames directory."""
        # Default frame (if any)
        default_path = os.path.join(self.frame_dir, "default.png")
        if os.path.exists(default_path):
            self._add_frame(
                Frame(
                    id="default",
                    name="Default",
                    category="Default",
                    path=default_path,
                    is_default=True,
                    is_enabled=True,
                )
            )

        # Scan for more frames
        for fname in os.listdir(self.frame_dir):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                if fname == 'default.png':
                    continue
                fpath = os.path.join(self.frame_dir, fname)
                try:
                    with Image.open(fpath) as img:
                        w, h = img.size
                    self._add_frame(
                        Frame(
                            id=fname,
                            name=fname,
                            category="Custom",
                            path=fpath,
                            width=w,
                            height=h,
                        )
                    )
                except Exception as exc:
                    logger.warning("Cannot load frame %s: %s", fname, exc)

        if not self._frames:
            logger.info("No frames found, using default only")

    def _add_frame(self, frame: Frame):
        """Add a frame definition."""
        self._frames[frame.id] = frame
        if frame.is_default:
            self._default_frame = frame.id

    def get_all(self) -> list[Frame]:
        """Get all frames."""
        return list(self._frames.values())

    def get_enabled(self) -> list[Frame]:
        """Get only enabled frames."""
        return [f for f in self._frames.values() if f.is_enabled]

    def get_by_id(self, frame_id: str) -> Optional[Frame]:
        """Get a frame by ID."""
        return self._frames.get(frame_id)

    def set_default(self, frame_id: str) -> bool:
        """Set a frame as default."""
        if frame_id in self._frames:
            self._default_frame = frame_id
            logger.info("Default frame set to: %s", frame_id)
            return True
        return False

    def toggle_enabled(self, frame_id: str, enabled: bool):
        """Enable or disable a frame."""
        if frame_id in self._frames:
            self._frames[frame_id].is_enabled = enabled
            logger.info("Frame %s enabled=%s", frame_id, enabled)

    def add_frame(self, file_path: str, name: str = "", category: str = "Custom") -> Optional[Frame]:
        """Add a new frame from a file."""
        ensure_dir(self.frame_dir)

        # Determine new filename
        ext = os.path.splitext(file_path)[1]
        if not name:
            name = os.path.splitext(os.path.basename(file_path))[0]

        new_path = os.path.join(self.frame_dir, f"{name}.png")
        if os.path.exists(new_path):
            # Add suffix
            base = os.path.splitext(os.path.basename(file_path))[0]
            counter = 1
            while os.path.exists(os.path.join(self.frame_dir, f"{base}_{counter}.png")):
                counter += 1
            new_path = os.path.join(self.frame_dir, f"{base}_{counter}.png")

        os.system(f"cp -f {file_path} {new_path}")

        frame = Frame(
            id=os.path.basename(new_path),
            name=name,
            category=category,
            path=new_path,
            is_enabled=True,
        )
        self._add_frame(frame)
        logger.info("Frame added: %s", frame.id)
        return frame

    def delete_frame(self, frame_id: str) -> bool:
        """Delete a frame."""
        if frame_id in self._frames:
            frame = self._frames[frame_id]
            try:
                if os.path.exists(frame.path):
                    os.remove(frame.path)
                del self._frames[frame_id]
                if self._default_frame == frame_id:
                    self._default_frame = None
                logger.info("Frame deleted: %s", frame_id)
                return True
            except Exception as exc:
                logger.error("Failed to delete frame %s: %s", frame_id, exc)
                return False
        return False

    def get_default(self) -> Optional[Frame]:
        """Get default frame."""
        if self._default_frame:
            return self._frames.get(self._default_frame)
        return None
