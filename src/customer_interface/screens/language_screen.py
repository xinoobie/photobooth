"""Language Selection Screen.

Customer chooses between Indonesian (id) and English (en).
Sets preferred language in config and moves to package selection.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QButtonGroup,
)
from PySide6.QtCore import Qt

from .base_screen import BaseScreen
from app_core.config import Config

config = Config.instance()


class LanguageScreen(BaseScreen):
    """Language selection screen."""

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

        title = QLabel("Pilih Bahasa")
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

        # Instruction
        instruction = QLabel("Pilih bahasa yang Anda inginkan")
        instruction.setStyleSheet(
            "font-size: 18px; color: #94A3B8; text-align: center;"
        )
        card_layout.addWidget(instruction)

        # Language list
        lang_list = QVBoxLayout()
        lang_list.setSpacing(16)

        lang_id = QPushButton("🇮🇩  Bahasa Indonesia")
        lang_id.setMinimumHeight(72)
        lang_id.setStyleSheet(
            "QPushButton { background-color: #3B82F6; color: white; "
            "border-radius: 12px; font-size: 20px; font-weight: 600; "
            "border: 3px solid #3B82F6; }"
            "QPushButton:hover { background-color: #1D4ED8; }"
            "QPushButton:checked { background-color: #0B1220; }"
        )
        lang_id.setCheckable(True)
        lang_id.setChecked(True)  # Default Indonesian
        lang_list.addWidget(lang_id)

        lang_en = QPushButton("🇺🇸  English")
        lang_en.setMinimumHeight(72)
        lang_en.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 20px; font-weight: 600; "
            "border: 3px solid #334155; }"
            "QPushButton:hover { background-color: #475569; }"
            "QPushButton:checked { background-color: #0B1220; "
            "border: 3px solid #3B82F6; }"
        )
        lang_en.setCheckable(True)
        lang_list.addWidget(lang_en)

        card_layout.addLayout(lang_list)

        # Proceed button
        proceed = QPushButton("Lanjut")
        proceed.setMinimumSize(400, 72)
        proceed.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        proceed.clicked.connect(self._on_proceed)
        card_layout.addWidget(proceed)

        layout.addWidget(card)

    def _on_proceed(self):
        """Handle proceed to package selection."""
        # Determine which radio is checked
        from .screens import get_screen
        from ..main_window import MainApplicationWindow

        w = self.parent()
        while w:
            from ..main_window import MainApplicationWindow
            if isinstance(w, MainApplicationWindow):
                main_win = w
                break
            w = w.parent()

        if main_win:
            # Set language in config
            is_id = self.findChild(QPushButton, "lang_id")
            is_en = self.findChild(QPushButton, "lang_en")
            selected_lang = "id" if is_id and is_id.isChecked() else "en"
            Config.instance()._data["language"] = selected_lang
            Config.instance()._data["language"] = selected_lang

            # Save to config file
            try:
                config_path = Config.instance().data_dir / "config.json"
                # Simple save - just the language setting
                import json
                save_data = {"language": selected_lang}
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.write_text(
                    json.dumps(save_data, indent=2), encoding="utf-8"
                )
                self.logger.info("Language set to: %s", selected_lang)
            except Exception as exc:
                self.logger.warning("Could not save language config: %s", exc)

            main_win.show_screen("package")
