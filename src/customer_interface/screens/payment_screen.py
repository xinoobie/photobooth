"""Payment Screen.

Display package price and payment method selection.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QRadioButton, QButtonGroup,
    QLineEdit, QMessageBox,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger

logger = get_logger("xinoobie.customer_interface.payment")

config = Config.instance()


class PaymentScreen(BaseScreen):
    """Payment screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_method = None
        self._package = None
        self._amount = 0.0

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)
        self._package = self._get_selected_package()

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

        # Title
        title = QLabel("Pembayaran")
        title.setStyleSheet(
            "font-size: 32px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(title)

        # Package info
        if self._package:
            pkg_info = QLabel(
                f"Paket: {self._package.get('name', 'Unknown')}\n"
                f"Harga: Rp {self._package.get('price', 0):,.0f}\n"
                f"Foto: {self._package.get('photo_count', 0)}\n"
                f"Retake: {self._package.get('retake_limit', 0)}x"
            )
            pkg_info.setStyleSheet(
                "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
            )
            card_layout.addWidget(pkg_info)

        # Payment methods
        method_label = QLabel("Metode Pembayaran")
        method_label.setStyleSheet(
            "font-size: 22px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(method_label)

        # Radio buttons
        methods = [
            ("💵", "Tunai (Cash)"),
            ("📱", "QRIS Manual"),
            ("💳", "E-wallet"),
        ]

        self._radio_group = QButtonGroup(self)
        row = 0
        for icon, name in methods:
            radio = QRadioButton(f"{icon}  {name}")
            radio.setStyleSheet(
                "QPushButton { border: none; background: transparent; "
                "font-size: 20px; color: #94A3B8; font-family: 'Segoe UI', sans-serif; }"
            )
            radio.setStyleSheet(
                "QRadioButton { border: none; background: transparent; "
                "font-size: 20px; color: #94A3B8; font-family: 'Segoe UI', sans-serif; }"
                "QRadioButton::indicator { width: 32px; height: 32px; "
                "border: 3px solid #334155; border-radius: 10px; "
                "background-color: #0F172A; }"
                "QRadioButton::indicator:checked { background-color: #3B82F6; "
                "border-color: #3B82F6; }"
            )
            radio.setChecked(row == 0)
            self._radio_group.addButton(radio, row)
            radio.toggled.connect(self._on_method_changed)
            card_layout.addWidget(radio)
            row += 1

        # Amount input (for manual QRIS)
        self._amount_input = QLineEdit()
        self._amount_input.setPlaceholderText("Masukkan nominal uang tunai (jika manual)")
        self._amount_input.setStyleSheet(
            "background-color: #0F172A; color: #F8FAFC; "
            "border: 2px solid #334155; border-radius: 8px; "
            "font-size: 18px; padding: 10px;"
        )
        self._amount_input.setVisible(False)
        card_layout.addWidget(self._amount_input)

        # Payment button
        pay_btn = QPushButton("Lunas →")
        pay_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 24px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        pay_btn.clicked.connect(self._on_pay)
        card_layout.addWidget(pay_btn)

        layout.addWidget(card)

        # Auto-select first method
        if self._radio_group.buttons():
            self._radio_group.buttons()[0].setChecked(True)
            self._on_method_changed()

    def _get_selected_package(self):
        """Get the currently selected package from main window."""
        from ..main_window import MainApplicationWindow
        main_win = None
        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()
        return getattr(main_win, "package", None)

    def _on_method_changed(self):
        """Handle payment method change."""
        selected = self._radio_group.checkedButton()
        if selected:
            self._selected_method = selected.text().replace("💵 ", "").replace("📱 ", "").replace("💳 ", "")
            is_cash = "Tunai" in selected.text()
            is_qris = "QRIS" in selected.text()
            self._amount_input.setVisible(is_cash)
            if is_cash:
                self._amount_input.setText(str(self._package["price"]) if self._package else "")
            self.logger.info("Payment method selected: %s", self._selected_method)

    def _on_pay(self):
        """Handle payment confirmation."""
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
            amount = float(self._amount_input.text().replace(",", "")) if self._amount_input.text() else 0
            self._amount = amount
            self.logger.info("Payment confirmed: %s %s", self._selected_method, amount)
            main_win.show_screen("printing")
