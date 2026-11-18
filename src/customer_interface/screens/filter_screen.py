"""Filter Selection Screen.

Display available filters for photo editing.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QListWidget, QListWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config


class FilterScreen(BaseScreen):
    """Filter selection screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_filter = None
        self._filters = self._load_filters()

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

        title = QLabel("Filter Foto")
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

        # Header
        header = QHBoxLayout()
        header.addWidget(QLabel("PILIH FILTER"))
        header.addStretch(1)
        content_layout.addLayout(header)

        # Filter list
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
            "QListWidget::item { height: 100px; padding: 12px; "
            "border-radius: 10px; margin: 6px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        if not self._filters:
            empty = QLabel("Tidak ada filter tersedia")
            empty.setStyleSheet(
                "color: #94A3B8; font-size: 18px; padding: 40px; "
                "text-align: center;"
            )
            list_widget.addItem(empty)
        else:
            for filter_name in self._filters:
                item = QListWidgetItem(list_widget)
                item.setData(Qt.UserRole, filter_name)

                # Filter icon placeholder
                icon = QLabel(filter_name[0])
                icon.setStyleSheet(
                    "background-color: #334155; color: #94A3B8; "
                    "border-radius: 12px; display: flex; align-items: center; "
                    "justify-content: center; font-size: 28px; "
                    "font-weight: 600;"
                )
                icon.setFixedSize(56, 56)

                # Filter info
                info = QLabel(filter_name)
                info.setStyleSheet(
                    "font-size: 16px; color: #F8FAFC; margin-top: 4px; "
                    "font-weight: 500;"
                )

                # Select button
                select_btn = QPushButton("Terapkan")
                select_btn.setStyleSheet(
                    "QPushButton { background-color: #3B82F6; color: white; "
                    "border-radius: 8px; font-size: 14px; font-weight: 600; }"
                    "QPushButton:hover { background-color: #1D4ED8; }"
                )
                select_btn.clicked.connect(
                    lambda _, name=filter_name: self._on_select(name)
                )

                row = QVBoxLayout()
                row.addWidget(icon)
                row.addWidget(info)
                row.addWidget(select_btn)

                row_widget = QWidget()
                row_widget.setLayout(row)
                list_widget.addItem(item)
                list_widget.setItemWidget(item, row_widget)

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

    def _load_filters(self) -> list[str]:
        """Load available filters (from database in future versions)."""
        return [
            "Default",
            "Black & White",
            "Vintage",
            "Film",
            "Warm",
            "Contrast",
            "Brightness",
            "Saturation",
            "Color Temperature",
        ]

    def _on_select(self, filter_name: str):
        """Handle filter selection."""
        self._selected_filter = filter_name
        self.logger.info("Filter selected: %s", filter_name)
        QMessageBox.information(
            self, "Filter Terpilih",
            f"Filter '{filter_name}' dipilih. Hasil akan terlihat setelah capture."
        )

    def _on_next(self):
        """Handle next button."""
        if not self._selected_filter:
            QMessageBox.warning(
                self, "Pilih Filter", "Silakan pilih filter terlebih dahulu."
            )
            return

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
            main_win.selected_filter = self._selected_filter
            main_win.show_screen("instructions")
