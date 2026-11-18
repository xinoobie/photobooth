"""Countdown Screen.

Displays a configurable countdown timer (3-3-3 or 5-5-5).
Triggered automatically when session starts.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressBar,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger

logger = get_logger("xinoobie.customer_interface.countdown")


class CountdownScreen(BaseScreen):
    """Countdown screen for camera preparation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._countdown_tick)
        self._countdown_value = 3

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
        card_layout.setContentsMargins(60, 48, 60, 48)
        card_layout.setSpacing(24)

        # Big countdown number
        self.countdown_label = QLabel("3")
        self.countdown_label.setStyleSheet(
            "font-size: 200px; font-weight: 900; color: #F8FAFC; "
            "font-family: 'JetBrains Mono', monospace; "
            "text-align: center;"
        )
        self.countdown_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.countdown_label)

        # Label
        label = QLabel("GET READY")
        label.setStyleSheet(
            "font-size: 36px; color: #94A3B8; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label)

        # Progress bar
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(100)
        progress.setStyleSheet(
            "QProgressBar { border: 2px solid #334155; border-radius: 8px; "
            "background-color: #0F172A; height: 8px; }"
            "QProgressBar::chunk { background-color: #3B82F6; "
            "border-radius: 4px; }"
        )
        card_layout.addWidget(progress)

        # Audio indicator
        audio_label = QLabel("🔊  Bunyi berisik dalam 3 detik!")
        audio_label.setStyleSheet(
            "font-size: 16px; color: #94A3B8; font-family: 'Segoe UI', sans-serif;"
        )
        audio_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(audio_label)

        layout.addWidget(card)

        # Timer
        self._countdown_timer.start(1000)  # 1 second

    def _countdown_tick(self):
        """Decrement countdown every second."""
        self._countdown_value -= 1
        if self._countdown_value <= 0:
            self._countdown_value = 0
            # Count down complete - notify parent to trigger capture
            self._on_countdown_complete()
            return

        self.countdown_label.setText(str(self._countdown_value))
        self.logger.info("Countdown: %d", self._countdown_value)

    def _on_countdown_complete(self):
        """Handle countdown completion."""
        self._countdown_timer.stop()
        self.countdown_label.setText("0")
        self.logger.info("Countdown complete - trigger capture")
        self._transition_to_capture()

    def _transition_to_capture(self):
        """Move to capture screen."""
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
            main_win.show_screen("capture")


class CountDownStageScreen(BaseScreen):
    """Alternative: multi-stage countdown (3-3-3 style - get ready, smile, etc.).

    Simplified for Phase 1 to use the single countdown approach.
    """
    def setup_ui(self):
        self.setMinimumSize(1920, 1080)
        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._tick)
        self.stage = 2  # 2 -> 1
        self.countdown_labels = {}

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

        layout.addWidget(top_bar)

        # Main card
        card = QFrame(self)
        card.setStyleSheet(
            "QFrame { background-color: #1E293B; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(60, 48, 60, 48)
        card_layout.setSpacing(24)

        # Title
        title = QLabel("Get Ready!")
        title.setStyleSheet(
            "font-size: 48px; font-weight: 700; color: #F8FAFC; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(title)

        # Stage indicator
        stage_label = QLabel("Stage 2/3")
        stage_label.setStyleSheet(
            "font-size: 20px; color: #3B82F6; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        card_layout.addWidget(stage_label)

        # Progress bar
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(66)
        progress.setStyleSheet(
            "QProgressBar { border: 2px solid #334155; border-radius: 8px; "
            "background-color: #0F172A; height: 8px; }"
            "QProgressBar::chunk { background-color: #3B82F6; "
            "border-radius: 4px; }"
        )
        card_layout.addWidget(progress)

        # Countdown number (smaller)
        countdown = QLabel("2")
        countdown.setStyleSheet(
            "font-size: 120px; font-weight: 900; color: #F8FAFC; "
            "font-family: 'JetBrains Mono', monospace;"
        )
        countdown.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(countdown)

        # SMILE text
        smile = QLabel("SMILE!")
        smile.setStyleSheet(
            "font-size: 28px; font-weight: 700; color: #FBBF24; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        smile.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(smile)

        layout.addWidget(card)
        self._countdown_timer.start(1000)

    def _tick(self):
        self.stage -= 1
        if self.stage <= 0:
            self._on_countdown_complete()
            return
        self.countdown_labels.get("countdown", None)
