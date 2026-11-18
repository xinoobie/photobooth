"""Package Selection Screen.

Display available packages (name, photo count, price, retake limit) for selection.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QListWidget, QListWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir

from database.models import Package, Base, User, Role
from database.database import Database

config = Config.instance()
db = Database(config.db_path)
logger = get_logger("xinoobie.customer_interface.packages")

# Load ORM models
from app_core import config as app_config  # noqa: F401


def _load_packages():
    """Load packages from database (async)."""
    try:
        loop = __import__("asyncio").get_event_loop()
        # Simpler: use a blocking approach for now
        # In a real app, this would use async
        # For Phase 1, return placeholder packages
        return {
            "Default 2x6 Strip": {"id": 1, "name": "Default 2x6 Strip",
                                   "photo_count": 2, "price": 25000,
                                   "retake_limit": 3},
            "Premium 2x6 Strip": {"id": 2, "name": "Premium 2x6 Strip",
                                   "photo_count": 2, "price": 35000,
                                   "retake_limit": 5},
            "4x6 Single Photo": {"id": 3, "name": "4x6 Single Photo",
                                  "photo_count": 1, "price": 15000,
                                  "retake_limit": 2},
            "1:1 Digital": {"id": 4, "name": "1:1 Digital Photo",
                            "photo_count": 1, "price": 12000,
                            "retake_limit": 1},
        }
    except Exception as exc:
        logger.warning("Error loading packages: %s", exc)
        return {}


class PackageScreen(BaseScreen):
    """Package selection screen."""

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)
        self._packages = _load_packages()
        self._selected_package = None

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

        title = QLabel("Pilih Paket")
        title.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        top_layout.addWidget(title)

        layout.addWidget(top_bar)

        # Main content
        content = QWidget(self)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.addWidget(QLabel("PILIH PAKET"))
        header.addStretch(1)
        content_layout.addLayout(header)

        # Scrollable package list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:vertical { width: 8px; background: #0F172A; "
            "border-radius: 4px; }"
            "QScrollBar::handle:vertical { background: #3B82F6; "
            "border-radius: 4px; min-height: 30px; }"
        )

        list_widget = QListWidget()
        list_widget.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 90px; padding: 12px; "
            "border-radius: 10px; margin: 6px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
            "QListWidget::item:selected:!active { background-color: #1D4ED8; }"
        )

        if not self._packages:
            empty = QLabel("Tidak ada paket tersedia")
            empty.setStyleSheet(
                "color: #94A3B8; font-size: 18px; padding: 40px; "
                "text-align: center;"
            )
            list_widget.addItem(empty)
        else:
            for pkg_name, pkg_data in self._packages.items():
                item = QListWidgetItem(list_widget)
                item.setData(Qt.UserRole, pkg_name)
                item.setSizeHint(
                    QWidget().sizeHint()  # placeholder
                )

                # Create a custom widget for the item
                pkg_widget = self._create_package_widget(pkg_name, pkg_data)
                list_widget.setItemWidget(item, pkg_widget)

        scroll.setWidget(list_widget)
        content_layout.addWidget(scroll)

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

        if self._packages:
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

    def _create_package_widget(self, pkg_name: str, pkg_data: dict) -> QWidget:
        """Create a package item widget."""
        container = QFrame()
        container.setStyleSheet(
            "QFrame { background-color: #0F172A; border-radius: 10px; "
            "padding: 12px; }"
            "QFrame:hover { background-color: #1E293B; }"
        )
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        # Package name
        name_label = QLabel(pkg_name)
        name_label.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #F8FAFC; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        layout.addWidget(name_label)

        # Price
        price_label = QLabel(f"Rp {pkg_data['price']:,.0f}")
        price_label.setStyleSheet(
            "font-size: 20px; font-weight: 700; color: #10B981; "
            "font-family: 'JetBrains Mono', monospace;"
        )
        layout.addWidget(price_label)

        # Features
        features = [
            f"{pkg_data['photo_count']} foto",
            f"Retake: {pkg_data['retake_limit']}x",
        ]
        features_label = QLabel(" | ".join(features))
        features_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        layout.addWidget(features_label)

        # Select button
        select_btn = QPushButton("Pilih")
        select_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 8px; font-size: 14px; font-weight: 600; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        select_btn.clicked.connect(
            lambda: self._on_select(pkg_name, pkg_data)
        )
        layout.addWidget(select_btn)

        return container

    def _on_select(self, pkg_name: str, pkg_data: dict):
        """Handle package selection."""
        self._selected_package = pkg_data
        self.logger.info("Package selected: %s (%s)", pkg_name, pkg_data["price"])
        # Highlight selected in list
        for i in range(self.findChild(QListWidget)):
            pass  # Not used in this approach
        # Emit signal or show confirmation
        self._show_selection_confirm(pkg_name, pkg_data)

    def _show_selection_confirm(self, pkg_name: str, pkg_data: dict):
        """Show confirmation that package is selected."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self, "Paket Terpilih",
            f"Paket '{pkg_name}' dipilih! Harga: Rp {pkg_data['price']:,.0f}\n"
            f"Foto: {pkg_data['photo_count']}  |  Retake: {pkg_data['retake_limit']}x",
        )

    def _on_next(self):
        """Handle next button."""
        if not self._selected_package:
            QMessageBox.warning(
                self, "Pilih Paket", "Silakan pilih paket terlebih dahulu."
            )
            return

        # Navigate to next screen
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
            main_win.package = self._selected_package
            main_win.show_screen("layout")
