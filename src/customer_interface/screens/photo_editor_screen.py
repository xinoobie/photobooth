"""Photo Editor Screen.

Basic photo editor with crop, rotate, brightness, contrast, saturation,
color temperature, and filter options.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSlider, QFileDialog, QMessageBox,
    QGridLayout, QListWidget,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.utils import ensure_dir
from PIL import Image
import numpy as np
import os

config = Config.instance()


class PhotoEditorScreen(BaseScreen):
    """Photo editor screen with basic controls."""

    edited_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_image = None
        self._current_image = None
        self._edits = {
            "crop": None,
            "rotate": 0,
            "brightness": 1.0,
            "contrast": 1.0,
            "saturation": 1.0,
            "color_temp": 0,
        }

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

        title = QLabel("Edit Foto")
        title.setStyleSheet(
            "font-size: 28px; color: #F8FAFC; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        top_layout.addWidget(title)

        layout.addWidget(top_bar)

        # Main content
        content = QWidget(self)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(16)

        # Editor area
        editor_area = QFrame(self)
        editor_area.setStyleSheet(
            "QFrame { background-color: #0F172A; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        editor_layout = QVBoxLayout(editor_area)
        editor_layout.setContentsMargins(20, 20, 20, 20)

        # Image display
        self.image_label = QLabel("Tidak ada foto untuk diedit")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(
            "background-color: #1E293B; border-radius: 12px; "
            "border: 2px dashed #334155; font-size: 20px; color: #64748B;"
        )
        editor_layout.addWidget(self.image_label)

        # Controls grid
        controls = QGridLayout()
        controls.setSpacing(12)

        # Rotation slider
        rotate_label = QLabel("Putar")
        rotate_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        controls.addWidget(rotate_label, 0, 0)

        self.rotate_slider = QSlider(Qt.Horizontal)
        self.rotate_slider.setMinimum(0)
        self.rotate_slider.setMaximum(359)
        self.rotate_slider.setValue(0)
        self.rotate_slider.valueChanged.connect(self._on_rotate)
        controls.addWidget(self.rotate_slider, 0, 1)

        rotate_value = QLabel("0°")
        rotate_value.setStyleSheet(
            "font-size: 14px; color: #64748B; font-family: 'JetBrains Mono', monospace;"
        )
        controls.addWidget(rotate_value, 0, 2)

        # Brightness slider
        bright_label = QLabel("Bright")
        bright_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        controls.addWidget(bright_label, 1, 0)

        self.bright_slider = QSlider(Qt.Horizontal)
        self.bright_slider.setMinimum(-100)
        self.bright_slider.setMaximum(100)
        self.bright_slider.setValue(0)
        self.bright_slider.valueChanged.connect(self._on_brightness)
        controls.addWidget(self.bright_slider, 1, 1)

        bright_value = QLabel("1.0x")
        bright_value.setStyleSheet(
            "font-size: 14px; color: #64748B; font-family: 'JetBrains Mono', monospace;"
        )
        controls.addWidget(bright_value, 1, 2)

        # Contrast slider
        contrast_label = QLabel("Contrast")
        contrast_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        controls.addWidget(contrast_label, 2, 0)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(50)
        self.contrast_slider.setMaximum(150)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self._on_contrast)
        controls.addWidget(self.contrast_slider, 2, 1)

        contrast_value = QLabel("1.0x")
        contrast_value.setStyleSheet(
            "font-size: 14px; color: #64748B; font-family: 'JetBrains Mono', monospace;"
        )
        controls.addWidget(contrast_value, 2, 2)

        # Saturation slider
        sat_label = QLabel("Saturation")
        sat_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        controls.addWidget(sat_label, 3, 0)

        self.sat_slider = QSlider(Qt.Horizontal)
        self.sat_slider.setMinimum(0)
        self.sat_slider.setMaximum(200)
        self.sat_slider.setValue(100)
        self.sat_slider.valueChanged.connect(self._on_saturation)
        controls.addWidget(self.sat_slider, 3, 1)

        sat_value = QLabel("1.0x")
        sat_value.setStyleSheet(
            "font-size: 14px; color: #64748B; font-family: 'JetBrains Mono', monospace;"
        )
        controls.addWidget(sat_value, 3, 2)

        # Color temperature
        temp_label = QLabel("Temp")
        temp_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        controls.addWidget(temp_label, 4, 0)

        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(-100)
        self.temp_slider.setMaximum(100)
        self.temp_slider.setValue(0)
        self.temp_slider.valueChanged.connect(self._on_temp)
        controls.addWidget(self.temp_slider, 4, 1)

        temp_value = QLabel("5500K")
        temp_value.setStyleSheet(
            "font-size: 14px; color: #64748B; font-family: 'JetBrains Mono', monospace;"
        )
        controls.addWidget(temp_value, 4, 2)

        editor_layout.addLayout(controls)

        # Action buttons
        action_buttons = QHBoxLayout()
        action_buttons.setSpacing(12)

        # Revert
        revert_btn = QPushButton("Batal")
        revert_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 16px; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        revert_btn.clicked.connect(self._on_revert)
        action_buttons.addWidget(revert_btn)

        # Apply
        apply_btn = QPushButton("Terapkan")
        apply_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 16px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        apply_btn.clicked.connect(self._on_apply)
        action_buttons.addWidget(apply_btn)

        # Done (next)
        done_btn = QPushButton("Selesai →")
        done_btn.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 18px; font-weight: 700; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
        )
        done_btn.clicked.connect(self._on_done)
        action_buttons.addWidget(done_btn)

        editor_layout.addLayout(action_buttons)

        content_layout.addWidget(editor_area)

        # Filter preview area (optional)
        filter_area = QFrame(self)
        filter_area.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        filter_layout = QVBoxLayout(filter_area)
        filter_layout.setContentsMargins(20, 20, 20, 20)

        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet(
            "font-size: 18px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        filter_layout.addWidget(filter_label)

        filters = QListWidget()
        filters.setStyleSheet(
            "QListWidget { background: transparent; border: none; "
            "outline: none; }"
            "QListWidget::item { height: 50px; padding: 8px; "
            "border-radius: 8px; }"
            "QListWidget::item:selected { background-color: #3B82F6; "
            "color: white; }"
        )
        filters.addItem("Black & White")
        filters.addItem("Vintage")
        filters.addItem("Film")
        filters.addItem("Warm")
        filters.addItem("Contrast")
        filters.addItem("Brightness")
        filters.addItem("Saturation")
        filters.addItem("Color Temperature")

        filter_layout.addWidget(filters)
        content_layout.addWidget(filter_area)

        # Load image placeholder
        self._load_image_placeholder()

    def _load_image_placeholder(self):
        """Load a placeholder image for demo."""
        # In a real app, this would load the actual captured photo
        self.image_label.setText("📷  Foto akan muncul di sini")
        self.image_label.setStyleSheet(
            "background-color: #1E293B; border-radius: 12px; "
            "border: 2px dashed #334155; font-size: 20px; color: #64748B;"
        )

    def _on_rotate(self, value):
        """Handle rotation slider."""
        self._edits["rotate"] = value
        self._update_display()

    def _on_brightness(self, value):
        """Handle brightness slider."""
        self._edits["brightness"] = (value + 100) / 100.0
        self._update_display()

    def _on_contrast(self, value):
        """Handle contrast slider."""
        self._edits["contrast"] = value / 100.0
        self._update_display()

    def _on_saturation(self, value):
        """Handle saturation slider."""
        self._edits["saturation"] = value / 100.0
        self._update_display()

    def _on_temp(self, value):
        """Handle color temperature slider."""
        self._edits["color_temp"] = value
        self._update_display()

    def _update_display(self):
        """Update the displayed image based on current edits."""
        self.image_label.setText(
            f"Rotasi: {self._edits['rotate']}° | "
            f"Bright: {self._edits['brightness']:.2f} | "
            f"Contrast: {self._edits['contrast']:.2f} | "
            f"Sat: {self._edits['saturation']:.2f} | "
            f"Temp: {self._edits['color_temp']}"
        )

    def _on_revert(self):
        """Revert changes."""
        self._edits = {
            "crop": None,
            "rotate": 0,
            "brightness": 1.0,
            "contrast": 1.0,
            "saturation": 1.0,
            "color_temp": 0,
        }
        self._update_display()
        self.logger.info("Edits reverted")

    def _on_apply(self):
        """Apply edits and save."""
        self._edits["rotate"] = 0
        self._edits["brightness"] = 1.0
        self._edits["contrast"] = 1.0
        self._edits["saturation"] = 1.0
        self._edits["color_temp"] = 0
        self._update_display()
        self.logger.info("Edits applied")

    def _on_done(self):
        """Handle done button."""
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
            main_win.show_screen("final_preview")
