"""Live Preview Screen — camera feed placeholder.

Displays a live camera preview. In Phase 1, shows a placeholder with status.
Real camera integration in Phase 2.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressBar, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from .base_screen import BaseScreen
from app_core.config import Config
from app_core.logging_config import get_logger
from camera_engine import CameraManager, Camera

logger = get_logger("xinoobie.customer_interface.live_preview")

config = Config.instance()
_camera_mgr = CameraManager()


class LivePreviewScreen(BaseScreen):
    """Live preview screen — placeholder for Phase 1."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active_camera_id = None
        self._preview_timer = QTimer(self)
        self._preview_timer.timeout.connect(self._on_preview_tick)
        self._preview_running = False

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

        # Session info
        session_label = QLabel("Sesi: —")
        session_label.setStyleSheet(
            "font-size: 14px; color: #94A3B8; font-family: 'JetBrains Mono', monospace;"
        )
        top_layout.addWidget(session_label)

        layout.addWidget(top_bar)

        # Main preview area
        preview_area = QFrame(self)
        preview_area.setStyleSheet(
            "QFrame { background-color: #0F172A; border-radius: 16px; "
            "box-shadow: 0 8px 32px rgba(0,0,0,0.4); }"
        )
        preview_layout = QVBoxLayout(preview_area)
        preview_layout.setContentsMargins(20, 20, 20, 20)

        # Camera status indicator
        self._camera_indicator = QLabel("○")
        self._camera_indicator.setStyleSheet(
            "color: #94A3B8; font-size: 24px; font-family: 'Segoe UI', sans-serif;"
        )
        self._camera_status_label = QLabel("Tidak Terhubung")
        self._camera_status_label.setStyleSheet(
            "color: #EF4444; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
        )
        self._camera_status_label.setAlignment(Qt.AlignCenter)
        self._camera_connecting = False

        # Preview area
        self._preview_label = QLabel("Menunggu kamera...")
        self._preview_label.setAlignment(Qt.AlignCenter)
        self._preview_label.setStyleSheet(
            "background-color: #1E293B; border-radius: 12px;"
            " border: 3px dashed #334155; font-size: 18px;"
            " color: #64748B; font-family: 'Segoe UI', sans-serif;"
        )
        preview_layout.addWidget(self._preview_label)

        # Camera status row (replaces placeholder)
        status_row = QHBoxLayout()
        status_label = QLabel("Kamera:")
        status_label.setStyleSheet(
            "color: #94A3B8; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
        )
        status_row.addWidget(status_label)
        status_row.addWidget(self._camera_indicator)
        status_row.addWidget(self._camera_status_label)
        preview_layout.addLayout(status_row)

        # Countdown progress
        countdown_label = QLabel("Countdown: 3")
        countdown_label.setStyleSheet(
            "font-size: 20px; color: #3B82F6; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif;"
        )
        preview_layout.addWidget(countdown_label)

        # Progress bar for camera connection
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(45)
        progress.setStyleSheet(
            "QProgressBar { border: 2px solid #334155; border-radius: 8px; "
            "background-color: #0F172A; height: 8px; }"
            "QProgressBar::chunk { background-color: #3B82F6; border-radius: 4px; }"
        )
        preview_layout.addWidget(progress)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        # Retake button
        retake_btn = QPushButton("Retake")
        retake_btn.setMinimumSize(160, 60)
        retake_btn.setStyleSheet(
            "QPushButton { background-color: #334155; color: #94A3B8; "
            "border-radius: 12px; font-size: 18px; font-weight: 600; }"
            "QPushButton:hover { background-color: #475569; }"
        )
        retake_btn.clicked.connect(self._on_retake)
        btn_row.addWidget(retake_btn)

        # Start session button
        start_btn = QPushButton("Mulai Sesi")
        start_btn.setMinimumSize(200, 60)
        start_btn.setStyleSheet(
            "QPushButton { background-color: #10B981; color: white; "
            "border-radius: 12px; font-size: 22px; font-weight: 700; }"
            "QPushButton:hover { background-color: #059669; }"
        )
        start_btn.clicked.connect(self._on_start_session)
        btn_row.addWidget(start_btn)

        preview_layout.addLayout(btn_row)

        layout.addWidget(preview_area)

        # Timer for preview tick
        self._preview_timer.start(2000)  # 2 seconds

    def _on_preview_tick(self):
        """Update camera status and preview."""
        connected = _camera_mgr.is_camera_connected(self._active_camera_id)
        if connected != self._preview_running:
            self._preview_running = connected
            self._update_camera_status(connected)
            if connected:
                self._preview_label.setText("🔴 Kamera Aktif")
                self._camera_status_label.setText("Terhubung")
                self._camera_status_label.setStyleSheet(
                    "color: #10B981; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
                )
            else:
                self._preview_label.setText("📷 Kamera Tidak Aktif")
                self._camera_status_label.setText("Tidak Terhubung")
                self._camera_status_label.setStyleSheet(
                    "color: #EF4444; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
                )

    def _update_camera_status(self, connected: bool):
        """Update UI for camera connection state."""
        self._preview_running = connected
        if connected:
            self._camera_indicator.setText("⏺")
            self._camera_indicator.setStyleSheet(
                "color: #10B981; font-size: 48px; font-family: 'Segoe UI', sans-serif;"
            )
            self._camera_status_label.setText("Terhubung")
            self._camera_status_label.setStyleSheet(
                "color: #10B981; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
            )
        else:
            self._camera_indicator.setText("○")
            self._camera_indicator.setStyleSheet(
                "color: #94A3B8; font-size: 48px; font-family: 'Segoe UI', sans-serif;"
            )
            self._camera_status_label.setText("Tidak Terhubung")
            self._camera_status_label.setStyleSheet(
                "color: #EF4444; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
            )

    def _on_retake(self):
        """Handle retake button."""
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
            main_win.show_screen("retake")

    def _on_start_session(self):
        """Handle start session."""
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
            session_id = main_win.session_id or "S-UNKNOWN"
            self.logger.info("Start session triggered: %s", session_id)
            main_win.show_screen("countdown")

    def showEvent(self, event):
        """Handle screen show — initialize camera."""
        super().showEvent(event)
        self._connect_camera()

    def hideEvent(self, event):
        """Handle screen hide — disconnect camera."""
        self._disconnect_camera()
        super().hideEvent(event)

    def _connect_camera(self):
        """Connect to the active camera."""
        if _camera_mgr.list_cameras():
            self._active_camera_id = _camera_mgr.list_cameras()[0].device_id
            status = _camera_mgr.connect(self._active_camera_id)
            if status:
                self._connect_camera_success()

    def _connect_camera_success(self):
        self._camera_connecting = False
        self._preview_running = True
        self._preview_label.setText("🔴 Kamera Aktif")
        self._camera_status_label.setText("Terhubung")
        self._camera_status_label.setStyleSheet(
            "color: #10B981; font-family: 'Segoe UI', sans-serif; font-size: 16px;"
        )
        _camera_mgr.start_preview(self._active_camera_id)

    def _disconnect_camera(self):
        """Disconnect from the active camera."""
        if self._active_camera_id is not None:
            _camera_mgr.stop_preview(self._active_camera_id)
        self._preview_running = False
