"""Main application window (kiosk mode).

Creates the QApplication, sets up the main window, and manages screen transitions.
"""

from __future__ import annotations

import sys
import os
import logging
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout,
    QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
    QFrame,
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QFont, QGuiApplication, QScreen

from app_core.config import Config
from app_core.utils import generate_session_id
from app_core.logging_config import get_logger

logger = get_logger("xinoobie.customer_interface")

# Screens are imported in a later step for clarity
try:
    from .screens import get_screen, ScreenId
except ImportError:
    ScreenId = None
    get_screen = None


class BaseScreen(QWidget):
    """Base class for all customer screens."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(f"xinoobie.customer_interface.screens.{self.__class__.__name__}")

    def setup_ui(self):
        """Subclasses override this to build their UI."""
        raise NotImplementedError

    def show_error(self, title: str, message: str):
        """Show a standard error message to the user."""
        QMessageBox.critical(self, title, message)


class MainApplicationWindow(QMainWindow):
    """Main window: fullscreen kiosk, screen stack management."""

    def __init__(self):
        super().__init__()
        self.logger = get_logger("xinoobie.main_window")
        self.setWindowTitle("Xinoobie Photobooth")

        # Application state
        self.current_screen = None
        self.session_id = None
        self.current_language = Config.instance().language
        self.screens = {}

        # Central widget with stacked layout
        central = QWidget()
        self.setCentralWidget(central)
        self._stack = QStackedWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._stack)

        # Load screens after the stacked widget is available
        self._load_screens()

        # Set fullscreen
        self._enter_fullscreen()

        # Timer for periodic checks (camera status, session timer, etc.)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(1000)  # 1 second

        self.logger.info("Main window created")

    def _load_screens(self):
        """Instantiate and register all 19 screens."""
        screen_classes = {
            "welcome": self._import_screen("WelcomeScreen"),
            "language": self._import_screen("LanguageScreen"),
            "start": self._import_screen("StartSessionScreen"),
            "package": self._import_screen("PackageScreen"),
            "layout": self._import_screen("LayoutScreen"),
            "frame": self._import_screen("FrameScreen"),
            "filter": self._import_screen("FilterScreen"),
            "instructions": self._import_screen("InstructionsScreen"),
            "live_preview": self._import_screen("LivePreviewScreen"),
            "countdown": self._import_screen("CountdownScreen"),
            "capture": self._import_screen("CaptureScreen"),
            "photo_selection": self._import_screen("PhotoSelectionScreen"),
            "retake": self._import_screen("RetakeScreen"),
            "photo_editor": self._import_screen("PhotoEditorScreen"),
            "final_preview": self._import_screen("FinalPreviewScreen"),
            "payment": self._import_screen("PaymentScreen"),
            "printing": self._import_screen("PrintingScreen"),
            "qr_download": self._import_screen("QRCodeDownloadScreen"),
            "thank_you": self._import_screen("ThankYouScreen"),
        }

        for name, screen_class in screen_classes.items():
            if screen_class:
                screen = screen_class(self._stack)
                screen.setup_ui()
                self._stack.addWidget(screen)
                self.screens[name] = screen
        self.logger.info("All %d screens loaded", len(self.screens))

    def _import_screen(self, name: str):
        """Import a screen class by name. Returns the class or None."""
        try:
            from .screens import get_screen as _get_screen
            from .screens import SCREEN_REGISTRY

            screen_class = next(
                (
                    cls
                    for cls in SCREEN_REGISTRY.values()
                    if cls.__name__ == name
                ),
                None,
            )
            if screen_class is not None:
                return screen_class
        except Exception as exc:
            logger.warning("Could not import screen '%s': %s", name, exc)
        return None

    def _enter_fullscreen(self):
        """Enter kiosk fullscreen mode."""
        screen = QGuiApplication.primaryScreen()
        if screen:
            if Config.instance().fullscreen:
                self.showFullScreen()
            else:
                self.resize(
                    Config.instance().window_width,
                    Config.instance().window_height,
                )
            # Set minimum size to 1080p
            self.setMinimumSize(1920, 1080)

    def show_screen(self, screen_name: str):
        """Switch to the named screen."""
        if screen_name not in self.screens:
            self.logger.warning("Screen '%s' not found", screen_name)
            return
        self._stack.setCurrentWidget(self.screens[screen_name])
        self.current_screen = self.screens[screen_name]
        self.logger.debug("Showing screen: %s", screen_name)

    def get_screen(self, screen_name: str):
        """Get a screen widget by name."""
        return self.screens.get(screen_name)

    @Slot()
    def _on_timer(self):
        """Periodic timer events (test camera, session timer, etc.)."""
        # Placeholder for future periodic tasks
        pass

    def closeEvent(self, event):
        """Clean up on close."""
        self.logger.info("Application closing")
        # Clean temp dir on close
        try:
            import shutil
            temp_dir = Config.instance().temp_dir
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
                logger.debug("Temp dir cleaned: %s", temp_dir)
        except Exception as exc:
            logger.warning("Temp cleanup failed: %s", exc)
        event.accept()


def main():
    """Application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Xinoobie Photobooth")
    app.setStyle("Fusion")

    # Set application font
    font = QFont("Segoe UI", 12)
    app.setFont(font)

    # Create main window
    window = MainApplicationWindow()

    # Show welcome screen (language select) first
    window.show_screen("welcome")

    # Start the application
    logger.info("Application starting...")
    exit_code = app.exec()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
