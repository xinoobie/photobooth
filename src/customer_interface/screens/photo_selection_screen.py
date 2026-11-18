"""Photo Selection Screen — select final photos for the session.

Display all captured photos with a multi-select grid.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .base_screen import BaseScreen
from app_core.config import Config
import os

config = Config.instance()


class PhotoSelectionScreen(BaseScreen):
    """Photo selection screen — multi-select final photos."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_photos = []
        self._photo_count = 2  # 2x6 strip default

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

        title = QLabel("Pilih Foto")
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

        # Photo grid
        grid = QListWidget()
        grid.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 180px; padding: 12px; "
            "border-radius: 12px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        # Generate placeholder photos
        for i in range(self._photo_count):
            item = QListWidgetItem(grid)
            item.setData(Qt.UserRole, i)

            photo_img = QLabel(f"📷 Foto {i+1}")
            photo_img.setStyleSheet(
                "background-color: #334155; border-radius: 10px; "
                "border: 2px solid #475569; display: flex; "
                "align-items: center; justify-content: center;"
            )
            photo_img.setFixedSize(160, 160)
            photo_img.setAlignment(Qt.AlignCenter)
            photo_img.setStyleSheet(
                "background-color: #334155; border-radius: 10px; "
                "border: 2px solid #555;"
            )

            select_check = QLabel("✓" if i == 0 else "")
            select_check.setStyleSheet(
                "font-size: 28px; color: #3B82F6;"
            )
            select_check.setAlignment(Qt.AlignCenter)

            info = QLabel(f"Foto {i+1}")
            info.setStyleSheet(
                "font-size: 12px; color: #64748B; margin-top: 6px; "
                "text-align: center;"
            )

            row = QVBoxLayout()
            row.addWidget(photo_img)
            row.addWidget(select_check)
            row.addWidget(info)

            row_widget = QWidget()
            row_widget.setLayout(row)
            grid.addItem(item)
            grid.setItemWidget(item, row_widget)

        content_layout.addWidget(grid)

        # Selection summary
        summary = QLabel("Foto terpilih: 1/2")
        summary.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        content_layout.addWidget(summary)

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

    def _on_next(self):
        """Handle next button."""
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
            main_win.show_screen("photo_editor")
