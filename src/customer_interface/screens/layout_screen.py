"""Layout Selection Screen.

Display available photo layouts (2x6 strip, 4x6, 4x4, 1:1, custom).
User selects one before proceeding to frame selection.
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


class LayoutScreen(BaseScreen):
    """Layout selection screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_layout = None
        self._layouts = self._load_layouts()

    def setup_ui(self):
        self.setMinimumSize(1920, 1080)
        self._layouts = self._load_layouts()

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

        title = QLabel("Pilih Layout Foto")
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
        header.addWidget(QLabel("PILIH TIPE LAYOUT"))
        header.addStretch(1)
        content_layout.addLayout(header)

        # Scrollable layout list
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
            "QListWidget::item { height: 120px; padding: 12px; "
            "border-radius: 10px; margin: 6px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )

        if not self._layouts:
            empty = QLabel("Tidak ada layout tersedia")
            empty.setStyleSheet(
                "color: #94A3B8; font-size: 18px; padding: 40px; "
                "text-align: center;"
            )
            list_widget.addItem(empty)
        else:
            for layout_name, layout_data in self._layouts.items():
                item = QListWidgetItem(list_widget)
                item.setData(Qt.UserRole, layout_name)

                # Thumbnail placeholder
                thumb = QLabel(layout_name[:8])
                thumb.setStyleSheet(
                    "background-color: #334155; color: #64748B; "
                    "border-radius: 6px; display: flex; align-items: center; "
                    "justify-content: center; font-size: 12px; "
                    "font-weight: 600;"
                )
                thumb.setFixedSize(100, 100)

                # Layout info
                info = QLabel(f"{layout_data['name']} — {layout_data['description']}")
                info.setStyleSheet(
                    "font-size: 14px; color: #F8FAFC; margin-top: 6px;"
                )

                # Select button
                select_btn = QPushButton("Pilih")
                select_btn.setStyleSheet(
                    "QPushButton { background-color: #3B82F6; color: white; "
                    "border-radius: 8px; font-size: 14px; font-weight: 600; }"
                    "QPushButton:hover { background-color: #1D4ED8; }"
                )
                select_btn.clicked.connect(
                    lambda _, name=layout_name: self._on_select(name)
                )

                row = QVBoxLayout()
                row.addWidget(thumb)
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

    def _load_layouts(self) -> dict:
        """Load available layouts (from database in future versions)."""
        return {
            "Strip 2x6": {
                "name": "Strip 2x6",
                "description": "2 foto dalam strip",
                "photo_count": 2,
                "width": 320,
                "height": 100,
            },
            "Single 4x6": {
                "name": "Single 4x6",
                "description": "1 foto ukuran 4x6 inch",
                "photo_count": 1,
                "width": 600,
                "height": 400,
            },
            "Square 1:1": {
                "name": "Square 1:1",
                "description": "1 foto format persegi",
                "photo_count": 1,
                "width": 500,
                "height": 500,
            },
            "Custom": {
                "name": "Custom",
                "description": "Ukuran khusus",
                "photo_count": 1,
                "width": 1920,
                "height": 1080,
            },
        }

    def _on_select(self, layout_name: str):
        """Handle layout selection."""
        self._selected_layout = self._layouts[layout_name]
        self.logger.info("Layout selected: %s", layout_name)
        QMessageBox.information(
            self, "Layout Terpilih",
            f"Layout '{layout_name}' dipilih!\n"
            f"Foto: {self._selected_layout['photo_count']} "
            f"dengan ukuran {self._selected_layout['width']}x{self._selected_layout['height']}",
        )

    def _on_next(self):
        """Handle next button."""
        if not self._selected_layout:
            QMessageBox.warning(
                self, "Pilih Layout", "Silakan pilih layout terlebih dahulu."
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
            main_win.selected_layout = self._selected_layout
            main_win.show_screen("frame")
