"""Retake Screen — select photo to retake.

Display recent photos and allow the user to select one for re-taking.
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


class RetakeScreen(BaseScreen):
    """Retake screen — let user select photo to retake."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._photo_count = 2

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

        title = QLabel("Retake Foto")
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

        # Instruction
        instruction = QLabel("Pilih foto yang ingin di-retake")
        instruction.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        instruction.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(instruction)

        # Photo list
        list_widget = QListWidget()
        list_widget.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 150px; padding: 12px; "
            "border-radius: 10px; margin: 8px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        for i in range(self._photo_count):
            item = QListWidgetItem(list_widget)
            item.setData(Qt.UserRole, i)

            # Photo preview
            photo_img = QLabel(f"📷 Foto {i+1}")
            photo_img.setStyleSheet(
                "background-color: #334155; border-radius: 10px; "
                "border: 2px solid #475569; display: flex; "
                "align-items: center; justify-content: center; "
                "font-size: 20px; color: #64748B;"
            )
            photo_img.setFixedSize(140, 140)

            # Action buttons
            btn = QPushButton("Retake")
            btn.setStyleSheet(
                "QPushButton { background-color: #3B82F6; color: white; "
                "border-radius: 8px; font-size: 14px; font-weight: 600; }"
                "QPushButton:hover { background-color: #1D4ED8; }"
            )
            btn.clicked.connect(lambda _, idx=i: self._on_retake(idx))

            row = QHBoxLayout()
            row.addWidget(photo_img)
            row.addWidget(btn)

            row_widget = QWidget()
            row_widget.setLayout(row)
            list_widget.addItem(item)
            list_widget.setItemWidget(item, row_widget)

        content_layout.addWidget(list_widget)

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

    def _on_retake(self, idx: int):
        """Handle retake selection."""
        self.logger.info("Retake selected: photo %d", idx)
        # In demo, just go back to capture
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
            main_win.show_screen("capture")

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
            main_win.show_screen("capture")
