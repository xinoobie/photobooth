"""Capture Screen — shows captured photos and selection.

Displays photos taken during the session. In Phase 1, shows a placeholder
with options to retake or continue.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.utils import ensure_dir
import os

config = Config.instance()


class CaptureScreen(BaseScreen):
    """Capture screen showing individual photos."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._captured_photos = []
        self._retake_limit = 3

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

        session_label = QLabel("Sesi: —")
        session_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'JetBrains Mono', monospace;"
        )
        top_layout.addWidget(session_label)

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(16)

        # Photo grid placeholder
        grid_label = QLabel("Foto 1/2")
        grid_label.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-weight: 600; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        grid_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(grid_label)

        # Photo placeholder
        photo_placeholder = QLabel("📷  Foto akan muncul di sini")
        photo_placeholder.setAlignment(Qt.AlignCenter)
        photo_placeholder.setFixedSize(600, 400)
        photo_placeholder.setStyleSheet(
            "background-color: #0F172A; border-radius: 12px; "
            "border: 3px dashed #334155; font-size: 24px; color: #64748B;"
        )
        card_layout.addWidget(photo_placeholder)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        # Retake button
        retake_btn = QPushButton("Retake")
        retake_btn.setMinimumSize(140, 60)
        retake_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        retake_btn.clicked.connect(self._on_retake)
        btn_row.addWidget(retake_btn)

        # View gallery
        gallery_btn = QPushButton("Lihat Galeri")
        gallery_btn.setMinimumSize(180, 60)
        gallery_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        gallery_btn.clicked.connect(self._on_gallery)
        btn_row.addWidget(gallery_btn)

        # Continue button
        continue_btn = QPushButton("Lanjut →")
        continue_btn.setMinimumSize(200, 60)
        continue_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        continue_btn.clicked.connect(self._on_continue)
        btn_row.addWidget(continue_btn)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)

        # Simulate photo capture
        self._simulate_capture()

    def _simulate_capture(self):
        """Simulate a photo capture for demo purposes."""
        import time
        for i in range(2):
            time.sleep(0.5)
            self.countdown_label = QLabel(f"Foto {i+1}/2")
            self.countdown_label.setStyleSheet(
                "font-size: 18px; color: #94A3B8; "
                "font-family: 'Segoe UI', sans-serif;"
            )
            self.logger.info("Simulated photo %d captured", i + 1)

    def _on_retake(self):
        """Handle retake."""
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
            main_win.show_screen("retake")

    def _on_gallery(self):
        """Show gallery view."""
        self._open_gallery()

    def _open_gallery(self):
        """Open gallery view."""
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
            main_win.show_screen("photo_selection")

    def _on_continue(self):
        """Continue to next step."""
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
            # Check if we need to take more photos
            # For demo, just continue
            main_win.show_screen("photo_selection")


class CaptureStageScreen(BaseScreen):
    """Stage-based capture simulation.

    Simplified for Phase 1 - shows a simple progress simulation.
    """

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

        session_label = QLabel("Sesi: —")
        session_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'JetBrains Mono', monospace;"
        )
        top_layout.addWidget(session_label)

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(20)

        # Timer
        timer = QLabel("2")
        timer.setStyleSheet(
            "font-size: 100px; font-weight: 900; color: #F8FAFC; "
            "font-family: 'JetBrains Mono', monospace;"
        )
        timer.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(timer)

        # Status
        status = QLabel("Foto sedang diproses...")
        status.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        status.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(status)

        # Progress bar
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(50)
        progress.setStyleSheet(
            "QProgressBar { border: 2px solid #334155; border-radius: 8px; "
            "background-color: #0F172A; height: 8px; }"
            "QProgressBar::chunk { background-color: #3B82F6; border-radius: 4px; }"
        )
        card_layout.addWidget(progress)

        # Button
        btn = QPushButton("Selesai")
        btn.setMinimumSize(200, 60)
        btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        btn.clicked.connect(self._on_done)
        card_layout.addWidget(btn)

        layout.addWidget(card)

        import time
        time.sleep(2)
        self._on_done()

    def _on_done(self):
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
            main_win.show_screen("photo_selection")
