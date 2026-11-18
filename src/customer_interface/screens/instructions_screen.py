"""Instructions Screen.

Display photo instructions (where to stand, what to do).
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config


class InstructionsScreen(BaseScreen):
    """Instructions screen."""

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

        title = QLabel("Instruksi")
        title.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        top_layout.addWidget(title)

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.3); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(24)

        # Icon placeholder
        icon_container = QFrame(self)
        icon_container.setFixedSize(160, 160)
        icon_container.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #3B82F6, stop:1 #1D4ED8); border-radius: 32px;"
        )
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel("📷")
        icon_label.setStyleSheet("font-size: 72px;")
        icon_layout.addWidget(icon_label)
        card_layout.addWidget(icon_container)

        # Instructions title
        title_text = QLabel("Posisikan Diri Anda")
        title_text.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(title_text)

        # Instruction text
        instruction = QLabel(
            "• Letakkan diri Anda di tengah area terang\n"
            "• Jaga jarak 1–2 meter dari kamera\n"
            "• Poskan wajah Anda di tengah frame\n"
            "• Tuangkan air mata? (optional playfully)\n"
            "• Datarkan kaki Anda agar tetap stabil"
        )
        instruction.setStyleSheet(
            "font-size: 18px; color: #94A3B8; line-height: 1.6; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(instruction)

        # Proceed button
        proceed = QPushButton("Lanjut")
        proceed.setMinimumSize(400, 72)
        proceed.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        proceed.clicked.connect(self._on_next)
        card_layout.addWidget(proceed)

        layout.addWidget(card)

    def _on_next(self):
        """Navigate to live preview."""
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
            main_win.show_screen("live_preview")
