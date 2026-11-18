"""Welcome Screen — language selector.

The first screen shown. Allows the customer to select language (Indonesian / English).
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QApplication,
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QBrush, QColor

from .base_screen import BaseScreen
from app_core.config import Config

config = Config.instance()


class WelcomeScreen(BaseScreen):
    """Welcome screen with language selection."""

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top gradient bar
        top_bar = QFrame(self)
        top_bar.setFixedHeight(120)
        top_bar.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                              "stop:0 #0B1220, stop:1 #1E293B);")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 20, 30, 20)
        top_layout.setSpacing(16)

        # Logo / app title
        logo_label = QLabel("Xinoobie")
        logo_label.setStyleSheet(
            "font-size: 48px; font-weight: 700; color: #3B82F6; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        top_layout.addWidget(logo_label)

        # Spacer
        top_layout.addStretch(1)

        # Language button (visible on welcome)
        lang_btn = QPushButton("Bahasa")
        lang_btn.setMinimumSize(120, 44)
        lang_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 8px; font-size: 16px; font-weight: 600; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        top_layout.addWidget(lang_btn)
        lang_btn.clicked.connect(self._on_lang_clicked)

        layout.addWidget(top_bar, alignment=Qt.AlignHCenter)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.3); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        # Icon placeholder
        icon_container = QFrame(self)
        icon_container.setFixedSize(120, 120)
        icon_container.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #3B82F6, stop:1 #1D4ED8); border-radius: 24px;"
        )
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel("📷")
        icon_label.setStyleSheet("font-size: 56px;")
        icon_layout.addWidget(icon_label)
        card_layout.addWidget(icon_container)

        # Title
        title = QLabel("Xinoobie Photobooth")
        title.setStyleSheet(
            "font-size: 36px; font-weight: 700; color: #F8FAFC; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Silakan pilih bahasa yang Anda inginkan")
        subtitle.setStyleSheet(
            "font-size: 18px; color: #94A3B8; margin-top: 8px;"
        )
        card_layout.addWidget(subtitle)

        # Language chips (2 buttons)
        lang_row = QHBoxLayout()
        lang_row.addStretch(1)

        # Language 1: Indonesia
        lang_id = QPushButton("🇮🇩 Indonesia")
        lang_id.setMinimumSize(280, 60)
        lang_id.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; "
            "padding: 0 24px; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
            "QPushButton:checked { background-color: #0B1220; "
            "border: 3px solid #3B82F6; }"
        )
        lang_id.setCheckable(True)
        lang_id.setChecked(True)
        lang_row.addWidget(lang_id)

        # Language 2: English
        lang_en = QPushButton("🇺🇸 English")
        lang_en.setMinimumSize(280, 60)
        lang_en.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; "
            "padding: 0 24px; }"
            "QPushButton:hover { background-color: #475569; }"
            "QPushButton:checked { background-color: #0B1220; "
            "border: 3px solid #3B82F6; }"
        )
        lang_en.setCheckable(True)
        lang_row.addWidget(lang_en)

        card_layout.addLayout(lang_row)

        # Start button (prominent)
        start_btn = QPushButton("Mulai Sesi")
        start_btn.setMinimumSize(400, 72)
        start_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; "
            "margin-top: 24px; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        start_btn.clicked.connect(self._on_start_clicked)
        card_layout.addWidget(start_btn)

        layout.addWidget(card)

        # Set initial language
        lang_en.setChecked(True)  # Default English

    def _on_lang_clicked(self):
        """Handle language selection button."""
        self._switch_to_language()

    def _on_start_clicked(self):
        """Handle start session button."""
        # Start by going to language selection (to set language properly)
        try:
            from .screens import get_screen
            from ..main_window import MainApplicationWindow

            screen = self.parent_widget()
            main_win = None
            # Find main window from parent chain
            w = self.parent()
            while w:
                from ..main_window import MainApplicationWindow
                if isinstance(w, MainApplicationWindow):
                    main_win = w
                    break
                w = w.parent()

            if main_win:
                main_win.show_screen("language")
        except Exception as exc:
            self.logger.error("Could not navigate to language: %s", exc)

    def _switch_to_language(self):
        """Navigate to language screen."""
        try:
            from ..main_window import MainApplicationWindow

            w = self.parent()
            while w:
                from ..main_window import MainApplicationWindow
                if isinstance(w, MainApplicationWindow):
                    w.show_screen("language")
                    break
                w = w.parent()
        except Exception as exc:
            self.logger.error("Navigation error: %s", exc)
