"""Printing Screen — print preview and queue management.

Displays print preview, quantity, and start print button.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QSpinBox, QMessageBox,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger

logger = get_logger("xinoobie.customer_interface.printing")

config = Config.instance()


class PrintingScreen(BaseScreen):
    """Printing screen with preview, quantity, and queue."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._print_queue = []
        self._printing = False

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

        # Print settings
        settings_label = QLabel("SETELAH PERCETAKAN")
        settings_label.setStyleSheet(
            "font-size: 20px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(settings_label)

        # Preview
        preview = QLabel("PRINTER PREVIEW")
        preview.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        preview.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(preview)

        # Preview image placeholder
        preview_img = QLabel("📷  Preview cetak akan muncul di sini")
        preview_img.setAlignment(Qt.AlignCenter)
        preview_img.setFixedSize(600, 400)
        preview_img.setStyleSheet(
            "background-color: #0F172A; border-radius: 12px; "
            "border: 3px dashed #334155; font-size: 24px; color: #64748B;"
        )
        card_layout.addWidget(preview_img)

        # Print settings row
        settings_row = QHBoxLayout()
        settings_row.setSpacing(16)

        # Quantity spinner
        qty_label = QLabel("Jumlah cetak:")
        qty_label.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        settings_row.addWidget(qty_label)

        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(5)
        self.qty_spin.setValue(1)
        self.qty_spin.setStyleSheet(
            "QSpinBox { border: 2px solid #334155; border-radius: 8px; "
            "padding: 6px; background-color: #0F172A; color: #F8FAFC; }"
        )
        settings_row.addWidget(self.qty_spin)

        # Paper size
        paper_label = QLabel("Ukuran Kertas: A6")
        paper_label.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        settings_row.addWidget(paper_label)

        # Print now button
        print_btn = QPushButton("Mulai Cetak")
        print_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
            "QPushButton:disabled { background-color: #4B5563; }"
        )
        print_btn.clicked.connect(self._on_print)
        settings_row.addWidget(print_btn)

        card_layout.addLayout(settings_row)

        # Print queue
        queue_label = QLabel("ANTREAN CEMPLAK")
        queue_label.setStyleSheet(
            "font-size: 20px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(queue_label)

        queue_list = QListWidget()
        queue_list.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 60px; padding: 10px; "
            "border-radius: 8px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        if self._print_queue:
            for job in self._print_queue:
                item = QListWidgetItem(queue_list)
                item.setData(Qt.UserRole, job)
                text = f"Akan dicetak: {job['quantity']}x {job['photo_index']}"
                item_text = QLabel(text)
                item_text.setStyleSheet(
                    "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
                )
                item.setSizeHint(item_text.sizeHint())

        queue_list.addItem("Belum ada antrian cetak")
        queue_list.setDisabled(True)
        card_layout.addWidget(queue_list)

        # Status
        status_label = QLabel("Status: Siap Cetak")
        status_label.setStyleSheet(
            "font-size: 18px; color: #10B981; font-weight: 600; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(status_label)

        layout.addWidget(card)

        # Simulation
        self._simulate_print()

    def _simulate_print(self):
        """Simulate print job (placeholder)."""
        import time
        for i in range(3):
            time.sleep(0.5)
            self.logger.info("Simulated print item %d", i)

    def _on_print(self):
        """Handle print start."""
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
            self._printing = True
            self.logger.info("Print started: %dx (qty=%d)",
                             self.sender(), self.qty_spin.value())
            main_win.show_screen("qr_download")
