"""Final Preview Screen — show the final photo with all elements applied.

User reviews the final photo (with frame, layout, filter) and proceeds to payment.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .base_screen import BaseScreen
from app_core.config import Config
import os

config = Config.instance()


class FinalPreviewScreen(BaseScreen):
    """Final preview screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._final_image_path = None

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

        # Final preview label
        preview_label = QLabel("PROSES FINAL...")
        preview_label.setStyleSheet(
            "font-size: 24px; color: #94A3B8; font-weight: 600; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        preview_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(preview_label)

        # Preview image placeholder
        preview_img = QLabel("📷  Hasil akhir akan ditampilkan di sini")
        preview_img.setAlignment(Qt.AlignCenter)
        preview_img.setFixedSize(800, 500)
        preview_img.setStyleSheet(
            "background-color: #0F172A; border-radius: 12px; "
            "border: 3px dashed #334155; font-size: 24px; color: #64748B;"
        )
        card_layout.addWidget(preview_img)

        # Session summary
        summary = QLabel("Ringkasan Sesi")
        summary.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(summary)

        summary_text = QLabel(
            "Paket: Default 2x6 Strip (Rp 25.000)\n"
            "Foto: 2  |  Retake: 3x  |  Frame: default\n"
            "Harga: Rp 25.000"
        )
        summary_text.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(summary_text)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        # Edit again
        edit_btn = QPushButton("Edit Lagi")
        edit_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        edit_btn.clicked.connect(self._on_edit)
        btn_row.addWidget(edit_btn)

        # Payment
        pay_btn = QPushButton("Lanjut ke Pembayaran →")
        pay_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 700; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        pay_btn.clicked.connect(self._on_payment)
        btn_row.addWidget(pay_btn)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)

    def _on_edit(self):
        """Go back to editor."""
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

    def _on_payment(self):
        """Go to payment."""
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
            main_win.show_screen("payment")
