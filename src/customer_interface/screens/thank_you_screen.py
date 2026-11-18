"""Thank You Screen — end of session.

Shows session summary and "Start New Session" button.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.utils import generate_session_id
from app_core.logging_config import get_logger

logger = get_logger("xinoobie.customer_interface.thank_you")

config = Config.instance()


class ThankYouScreen(BaseScreen):
    """Thank you screen at the end of session."""

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

        title = QLabel("Terima Kasih!")
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
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(20)

        # Thank you message
        message = QLabel("Terima kasih sudah menggunakan Xinoobie Photobooth!")
        message.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        message.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(message)

        # Session summary
        summary = QLabel("RINGKASAN SESI")
        summary.setStyleSheet(
            "font-size: 18px; color: #3B82F6; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(summary)

        summary_text = QLabel(
            f"Sesi ID: {self._session_id}\n"
            f"Paket: Default 2x6 Strip\n"
            f"Harga: Rp 25.000\n"
            f"Foto: 2  |  Cetak: 1x  |  QR Download: ✔"
        )
        summary_text.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
            " background-color: #0F172A; padding: 16px; border-radius: 8px;"
        )
        card_layout.addWidget(summary_text)

        # Gallery link
        gallery_label = QLabel("Galeri Digital:")
        gallery_label.setStyleSheet(
            "font-size: 16px; color: #10B981; font-weight: 600; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(gallery_label)

        gallery_link = QLabel("https://xinoobie.example/gallery/S-12345678")
        gallery_link.setStyleSheet(
            "font-size: 14px; color: #3B82F6; font-family: 'JetBrains Mono', monospace;"
            " word-break: break-all;"
        )
        card_layout.addWidget(gallery_link)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        # Back
        back_btn = QPushButton("← Mulai Sesi Baru")
        back_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        back_btn.clicked.connect(self._on_new_session)
        btn_row.addWidget(back_btn)

        # Exit
        exit_btn = QPushButton("Keluar Aplikasi")
        exit_btn.setStyleSheet(
            "QPushButton { background-color: #EF4444; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 700; }"
            "QPushButton:hover { background-color: #DC2626; }"
        )
        exit_btn.clicked.connect(self._on_exit)
        btn_row.addWidget(exit_btn)

        card_layout.addLayout(btn_row)

        layout.addWidget(card)

    @property
    def _session_id(self):
        """Get the session ID from main window."""
        from ..main_window import MainApplicationWindow
        main_win = None
        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()
        return getattr(main_win, "session_id", "S-UNKNOWN")

    def _on_new_session(self):
        """Start a new session."""
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
            # Generate fresh session ID
            main_win.session_id = generate_session_id("S")
            logger.info("New session started: %s", main_win.session_id)
            main_win.show_screen("start")

    def _on_exit(self):
        """Exit the application."""
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
            from PySide6.QtWidgets import QApplication
            import sys
            QApplication.quit()
            sys.exit(0)
