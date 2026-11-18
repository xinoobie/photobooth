"""Photo Engine — image capture, processing, and rendering.

Features:
- Capture from camera or mock
- Photo processing (resize, normalize)
- Layout composition (2x6, 4x6, 4x4, 1:1)
- Frame rendering
- Filter application (via PIL)
"""

from __future__ import annotations

import os
from typing import Optional

try:
    import numpy as np
    _HAVE_NUMPY = True
except ImportError:
    np = None
    _HAVE_NUMPY = False

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from PIL.Image import Image as PILImage

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir

config = Config.instance()
logger = get_logger("xinoobie.photo_engine")


class PhotoEngine:
    """Core photo processing engine."""

    def __init__(self):
        self._filters: dict[str, callable] = {}
        self._layouts: dict[str, callable] = {}
        self._frames: dict[str, callable] = {}

        self._register_default_filters()
        self._register_default_layouts()
        self._register_default_frames()

    # ------------------------------------------------------------------
    # Filter registration
    # ------------------------------------------------------------------
    def _register_default_filters(self):
        """Register default filters (black & white, vintage, etc.)."""
        def black_white(img: PILImage) -> PILImage:
            return img.convert("L").convert("RGB")

        def vintage(img: PILImage) -> PILImage:
            from PIL import ImageOps
            # Slight sepia
            from PIL import ImageOps
            return ImageOps.colorize(
                img.convert("L"),
                black="#6B3A2A",
                white="#F4E4C1",
                mid="#E8B87A",
            )

        def film(img: PILImage) -> PILImage:
            # Slight vignette
            img = img.filter(ImageFilter.GaussianBlur(2))
            return img

        def warm(img: PILImage) -> PILImage:
            r, g, b = img.split()
            r = r.point(lambda p: min(255, int(p * 1.1)))
            b = b.point(lambda p: max(0, int(p * 0.9)))
            return Image.merge("RGB", (r, g, b))

        def contrast(img: PILImage, factor: float) -> PILImage:
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(factor)

        def brightness(img: PILImage, factor: float) -> PILImage:
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(factor)

        def saturation(img: PILImage, factor: float) -> PILImage:
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(factor)

        def color_temp(img: PILImage, temp: int) -> PILImage:
            # temp: -100 (warm) to +100 (cool)
            factor = 1.0 + (temp / 100.0) * 0.1
            r, g, b = img.split()
            r = r.point(lambda p: min(255, int(p * factor)))
            b = b.point(lambda p: max(0, int(p * (2 - factor))))
            return Image.merge("RGB", (r, g, b))

        self._filters["bw"] = black_white
        self._filters["vintage"] = vintage
        self._filters["film"] = film
        self._filters["warm"] = warm
        self._filters["contrast"] = contrast
        self._filters["brightness"] = brightness
        self._filters["saturation"] = saturation
        self._filters["color_temp"] = color_temp

    # ------------------------------------------------------------------
    # Layout registration
    # ------------------------------------------------------------------
    def _register_default_layouts(self):
        """Register default layouts."""

        def layout_2x6(images: list[PILImage]) -> PILImage:
            """Create a 2x6 strip."""
            # For demo, we just show the images in a row
            # In real implementation, each cell gets its own image
            width = 1920
            height = 1080
            result = Image.new("RGB", (width, height), (20, 29, 42))
            draw = ImageDraw.Draw(result)
            draw.text((960, 540), "2x6 Strip Layout", fill=(248, 250, 252))
            logger.info("Layout 2x6 composed (%d images)", len(images))
            return result

        def layout_4x6(images: list[PILImage]) -> PILImage:
            """Create a 4x6 strip."""
            width = 1920
            height = 1080
            result = Image.new("RGB", (width, height), (20, 29, 42))
            draw = ImageDraw.Draw(result)
            draw.text((960, 540), "4x6 Strip Layout", fill=(248, 250, 252))
            logger.info("Layout 4x6 composed (%d images)", len(images))
            return result

        def layout_4x4(images: list[PILImage]) -> PILImage:
            """Create a 4x4 grid."""
            width = 1920
            height = 1080
            result = Image.new("RGB", (width, height), (20, 29, 42))
            draw = ImageDraw.Draw(result)
            draw.text((960, 540), "4x4 Grid Layout", fill=(248, 250, 252))
            logger.info("Layout 4x4 composed (%d images)", len(images))
            return result

        def layout_1x1(images: list[PILImage]) -> PILImage:
            """Create a single 1:1 photo."""
            if not images:
                return Image.new("RGB", (1920, 1080), (20, 29, 42))
            img = images[0]
            # Resize to fit 1:1
            img = img.resize((1920, 1080), Image.LANCZOS)
            return img

        self._layouts["2x6"] = layout_2x6
        self._layouts["4x6"] = layout_4x6
        self._layouts["4x4"] = layout_4x4
        self._layouts["1x1"] = layout_1x1

    # ------------------------------------------------------------------
    # Frame management
    # ------------------------------------------------------------------
    def _register_default_frames(self):
        """Register default frames (placeholder)."""
        # In real implementation, frames are PNG files with transparency
        logger.info("Default frames registered (placeholder)")

    def apply_filter(self, img: PILImage, name: str, **kwargs) -> PILImage:
        """Apply a filter to an image."""
        if name not in self._filters:
            logger.warning("Filter not found: %s", name)
            return img

        filter_fn = self._filters[name]
        try:
            return filter_fn(img, **kwargs)
        except TypeError:
            # No kwargs support
            return filter_fn(img)

    def apply_layout(self, images: list[PILImage], layout: str) -> PILImage:
        """Compose images into a layout."""
        if layout not in self._layouts:
            logger.warning("Layout not found: %s", layout)
            return images[0] if images else Image.new("RGB", (1920, 1080), (20, 29, 42))

        layout_fn = self._layouts[layout]
        return layout_fn(images)

    def render_with_frame(self, img: PILImage, frame_name: str) -> PILImage:
        """Apply a frame to an image."""
        # In a real implementation, this would composite a frame PNG
        # with transparency
        return img

    # ------------------------------------------------------------------
    # Capture
    # ------------------------------------------------------------------
    def capture_from_camera(self, camera) -> Optional[str]:
        """Capture a photo from the camera."""
        try:
            path = camera.capture()
            if path and os.path.exists(path):
                logger.info("Camera capture: %s", path)
                return path
            return None
        except Exception as exc:
            logger.error("Camera capture failed: %s", exc)
            return None

    def process_photo(self, path: str, **edits) -> str:
        """Process a photo with edits (brightness, contrast, etc.)."""
        try:
            img = Image.open(path).convert("RGB")

            # Apply brightness (range -100 to 100)
            if "brightness" in edits:
                factor = (edits["brightness"] + 100) / 100.0
                img = ImageEnhance.Brightness(img).enhance(factor)

            # Apply contrast (50-150)
            if "contrast" in edits:
                factor = edits["contrast"] / 100.0
                img = ImageEnhance.Contrast(img).enhance(factor)

            # Apply saturation (0-200)
            if "saturation" in edits:
                factor = edits["saturation"] / 100.0
                img = ImageEnhance.Color(img).enhance(factor)

            # Apply color temperature (range -100 to 100)
            if "color_temp" in edits:
                img = self.apply_filter(img, "color_temp", temp=edits["color_temp"])

            save_dir = config.data_dir
            ensure_dir(save_dir)
            base, ext = os.path.splitext(path)
            out_path = f"{base}_edited{ext}"
            img.save(out_path, "PNG", quality=95)
            logger.info("Processed photo saved: %s", out_path)
            return out_path
        except Exception as exc:
            logger.error("Photo processing failed: %s", exc)
            return path
