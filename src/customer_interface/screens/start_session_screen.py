"""Start Session Screen.

Displays a simple "Start Session" button after language is selected.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.utils import generate_session_id
from app_core.config import Config


class StartSessionScreen(BaseScreen):
    """Start session screen."""

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

        # Session info (blank)
        session_info = QLabel("Sesi: —")
        session_info.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'JetBrains Mono', monospace;"
        )
        top_layout.addWidget(session_info)

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.3); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        # Icon
        icon_container = QFrame(self)
        icon_container.setFixedSize(160, 160)
        icon_container.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #3B82F6, stop:1 #1D4ED8); border-radius: 32px;"
        )
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel("📸")
        icon_label.setStyleSheet("font-size: 72px;")
        icon_layout.addWidget(icon_label)
        card_layout.addWidget(icon_container)

        # Title
        title = QLabel("Mulai Sesi Baru")
        title.setStyleSheet(
            "font-size: 36px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Siap untuk memulai sesi foto?")
        subtitle.setStyleSheet(
            "font-size: 18px; color: #94A3B8; margin-top: 8px;"
        )
        card_layout.addWidget(subtitle)

        # Start button
        start_btn = QPushButton("Mulai Sesi")
        start_btn.setMinimumSize(400, 72)
        start_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        start_btn.clicked.connect(self._on_start)
        card_layout.addWidget(start_btn)

        layout.addWidget(card, alignment=Qt.AlignCenter)

        # Generate initial session ID
        self._init_session_id()

    def _init_session_id(self):
        """Generate a session ID for the upcoming session."""
        self.session_id = generate_session_id("S")
        self.logger.info("Session ID generated: %s", self.session_id)

    def _on_start(self):
        """Handle start button."""
        from ..main_window import MainApplicationWindow
        from .screens import get_screen

        main_win = None
        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()

        if main_win:
            # Generate a new session ID if not already set
            self._init_session_id()
            main_win.session_id = self.session_id
            main_win.show_screen("package")
