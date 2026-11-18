"""Layout Engine - compose photos into photo strips.

Supports:
- 2x6 strip
- 4x6 strip
- 4x4 grid
- 1:1 digital
- Custom canvas size
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger
from PIL import Image

config = Config.instance()
logger = get_logger("xinoobie.layout_engine")


@dataclass
class Layout:
    """A layout definition."""
    id: str
    name: str
    cols: int
    rows: int
    cell_width: int
    cell_height: int
    is_type_strip: bool = False


class LayoutManager:
    """Manages photo layouts."""

    def __init__(self):
        self._layouts: dict[str, Layout] = {}
        self._register_default()

    def _register_default(self):
        """Register built-in layouts."""

        # 2x6 strip (common for Korean photobooths)
        self._layouts["2x6"] = Layout(
            id="2x6",
            name="2x6 Strip",
            cols=2,
            rows=6,
            cell_width=320,
            cell_height=220,
            is_type_strip=True,
        )

        # 4x6 strip
        self._layouts["4x6"] = Layout(
            id="4x6",
            name="4x6 Strip",
            cols=4,
            rows=6,
            cell_width=320,
            cell_height=220,
            is_type_strip=True,
        )

        # 4x4 grid
        self._layouts["4x4"] = Layout(
            id="4x4",
            name="4x4 Grid",
            cols=4,
            rows=4,
            cell_width=240,
            cell_height=240,
        )

        # 1:1 digital
        self._layouts["1x1"] = Layout(
            id="1x1",
            name="1:1 Digital",
            cols=1,
            rows=1,
            cell_width=1080,
            cell_height=1080,
        )

    def get_all(self) -> list[Layout]:
        """Get all layouts."""
        return list(self._layouts.values())

    def get_by_id(self, layout_id: str) -> Optional[Layout]:
        """Get a layout by ID."""
        return self._layouts.get(layout_id)

    def compose(self, images: list[Image.Image], layout_id: str) -> Optional[Image.Image]:
        """Compose images into a layout."""
        layout = self.get_by_id(layout_id)
        if not layout or not images:
            return None

        # Calculate canvas size
        canvas_w = layout.cols * layout.cell_width
        canvas_h = layout.rows * layout.cell_height
        result = Image.new("RGB", (canvas_w, canvas_h), (20, 29, 42))

        for idx, img in enumerate(images):
            if idx >= layout.cols * layout.rows:
                break
            # Calculate position
            col = idx % layout.cols
            row = idx // layout.cols
            x = col * layout.cell_width
            y = row * layout.cell_height

            # Resize and paste image
            resized = img.resize((layout.cell_width, layout.cell_height), Image.LANCZOS)
            result.paste(resized, (x, y))

        logger.info("Composed %d images using layout %s", len(images), layout_id)
        return result
