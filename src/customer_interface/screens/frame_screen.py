"""Frame Selection Screen.

Display available frames (PNG with transparency) for selection.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger
import os

config = Config.instance()


class FrameScreen(BaseScreen):
    """Frame selection screen."""

    def __init__(self, parent=None):
        self._selected_frame = None
        self.logger = get_logger("xinoobie.customer_interface.screens.FrameScreen")
        self._available_frames = self._load_frames()
        super().__init__(parent)

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar
        top_bar = QFrame(self)
        top_bar.setFixedHeight(100)
        top_bar.setStyleSheet("background-color: #0F172A; border-radius: 0;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 20, 30, 20)
        top_layout.setSpacing(16)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(44, 44)
        back_btn.setStyleSheet(
            "QPushButton { color: #94A3B8; font-size: 24px; }"
            "QPushButton:hover { color: #F8FAFC; background-color: #334155; }"
        )
        top_layout.addWidget(back_btn)
        top_layout.addStretch(1)

        title = QLabel("Pilih Frame")
        title.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        top_layout.addWidget(title)

        layout.addWidget(top_bar)

        # Main content
        content = QWidget(self)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.addWidget(QLabel("PILIH FRAME"))
        header.addStretch(1)
        content_layout.addLayout(header)

        # Scrollable frame list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:vertical { width: 8px; background: #0F172A; "
            "border-radius: 4px; }"
            "QScrollBar::handle:vertical { background: #3B82F6; "
            "border-radius: 4px; min-height: 30px; }"
        )

        list_widget = QListWidget()
        list_widget.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 110px; padding: 8px; "
            "border-radius: 10px; margin: 6px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        if not self._available_frames:
            empty = QLabel("Tidak ada frame tersedia")
            empty.setStyleSheet(
                "color: #94A3B8; font-size: 18px; padding: 40px; "
                "text-align: center;"
            )
            list_widget.addItem(empty)
        else:
            for frame_name in self._available_frames:
                item = QListWidgetItem(list_widget)
                item.setData(Qt.UserRole, frame_name)

                # Frame preview thumbnail
                thumb = QLabel()
                thumb.setFixedSize(80, 80)
                thumb.setStyleSheet(
                    "background-color: #334155; border-radius: 6px; "
                    "border: 1px solid #475569;"
                )
                # Try to load the frame image if available
                frame_path = self._get_frame_path(frame_name)
                if frame_path and os.path.exists(frame_path):
                    pixmap = QPixmap(frame_path).scaled(
                        80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    thumb.setPixmap(pixmap)
                else:
                    thumb.setText(frame_name[:10])
                    thumb.setAlignment(Qt.AlignCenter)

                # Frame info
                info = QLabel(frame_name)
                info.setStyleSheet(
                    "font-size: 14px; color: #F8FAFC; margin-top: 4px;"
                )

                # Select button
                select_btn = QPushButton("Pilih")
                select_btn.setStyleSheet(
                    "QPushButton { background-color: #3B82F6; color: white; "
                    "border-radius: 8px; font-size: 14px; font-weight: 600; }"
                    "QPushButton:hover { background-color: #1D4ED8; }"
                )
                select_btn.clicked.connect(
                    lambda _, name=frame_name: self._on_select(name)
                )

                row = QVBoxLayout()
                row.addWidget(thumb)
                row.addWidget(info)
                row.addWidget(select_btn)

                row_widget = QWidget()
                row_widget.setLayout(row)
                list_widget.addItem(item)
                list_widget.setItemWidget(item, row_widget)

        scroll.setWidget(list_widget)
        content_layout.addWidget(scroll)

        # Bottom buttons
        bottom = QHBoxLayout()
        bottom.addStretch(1)

        back_btn = QPushButton("Kembali")
        back_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 8px; font-size: 16px; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        bottom.addWidget(back_btn)

        bottom.addStretch(1)

        next_btn = QPushButton("Lanjut →")
        next_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 20px; font-weight: 700; "
            "min-width: 200px; }"
            "QPushButton:hover { background-color: #059669; }"
            "QPushButton:disabled { background-color: #4B5563; }"
        )
        next_btn.clicked.connect(self._on_next)
        bottom.addWidget(next_btn)

        content_layout.addLayout(bottom)
        layout.addWidget(content)

    def _load_frames(self) -> list[str]:
        """Load available frames (PNG files in assets/frames)."""
        frames_dir = Config.instance().data_dir / "frames"
        frame_names = []

        if frames_dir.exists():
            for f in frames_dir.glob("*.png"):
                frame_names.append(f.stem)
            # Also check assets/frames
            alt_dir = Config.instance().data_dir.parent / "assets" / "frames"
            if alt_dir.exists():
                for f in alt_dir.glob("*.png"):
                    if f.stem not in frame_names:
                        frame_names.append(f.stem)

        # If no frames found, create a default frame
        if not frame_names:
            self._create_default_frame()
            frame_names = ["default"]

        return sorted(frame_names)

    def _create_default_frame(self):
        """Create a default frame (PNG) for demo."""
        frames_dir = Config.instance().data_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        # Create a simple frame image
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Outer border
        draw.rectangle([40, 40, 560, 560], outline=(59, 130, 246, 255), width=8)
        # Inner border
        draw.rectangle([80, 80, 520, 520], outline=(30, 64, 224, 255), width=4)
        # Corner highlights
        draw.rectangle([40, 300, 80, 340], fill=(59, 130, 246, 180))
        draw.rectangle([520, 300, 560, 340], fill=(59, 130, 246, 180))
        draw.rectangle([300, 40, 340, 80], fill=(59, 130, 246, 180))
        draw.rectangle([300, 520, 340, 560], fill=(59, 130, 246, 180))

        img.save(frames_dir / "default.png")
        self.logger.info("Default frame created at %s", frames_dir / "default.png")

    def _get_frame_path(self, frame_name: str) -> str:
        """Get the file path for a frame by name."""
        candidates = [
            Config.instance().data_dir / "frames" / f"{frame_name}.png",
            Config.instance().data_dir.parent / "assets" / "frames" / f"{frame_name}.png",
            Config.instance().data_dir.parent / "assets" / "frames" / f"{frame_name}.png",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return ""

    def _on_select(self, frame_name: str):
        """Handle frame selection."""
        self._selected_frame = frame_name
        self.logger.info("Frame selected: %s", frame_name)
        QMessageBox.information(
            self, "Frame Terpilih", f"Frame '{frame_name}' dipilih."
        )

    def _on_next(self):
        """Handle next button."""
        if not self._selected_frame:
            QMessageBox.warning(
                self, "Pilih Frame", "Silakan pilih frame terlebih dahulu."
            )
            return

        from ..main_window import MainApplicationWindow
        main_win = None
        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()

        if main_win:
            main_win.selected_frame = self._selected_frame
            main_win.show_screen("filter")
