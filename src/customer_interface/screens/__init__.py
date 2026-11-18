"""Customer Interface — Screens registry and base classes."""

from __future__ import annotations

import log_utils
import logging
from typing import Protocol, Type

from PySide6.QtWidgets import QWidget

# Import all screen modules so their classes are registered
from .welcome_screen import WelcomeScreen
from .language_screen import LanguageScreen
from .start_session_screen import StartSessionScreen
from .package_screen import PackageScreen
from .layout_screen import LayoutScreen
from .frame_screen import FrameScreen
from .filter_screen import FilterScreen
from .instructions_screen import InstructionsScreen
from .live_preview_screen import LivePreviewScreen
from .countdown_screen import CountdownScreen, CountDownStageScreen
from .capture_screen import CaptureScreen, CaptureStageScreen
from .photo_selection_screen import PhotoSelectionScreen
from .retake_screen import RetakeScreen
from .photo_editor_screen import PhotoEditorScreen
from .final_preview_screen import FinalPreviewScreen
from .payment_screen import PaymentScreen
from .printing_screen import PrintingScreen
from .qr_download_screen import QRCodeDownloadScreen
from .thank_you_screen import ThankYouScreen


class ScreenId(str):
    """Identifier for a customer screen."""
    WELCOME = "welcome"
    LANGUAGE = "language"
    START = "start"
    PACKAGE = "package"
    LAYOUT = "layout"
    FRAME = "frame"
    FILTER = "filter"
    INSTRUCTIONS = "instructions"
    LIVE_PREVIEW = "live_preview"
    COUNTDOWN = "countdown"
    CAPTURE = "capture"
    PHOTO_SELECTION = "photo_selection"
    RETAKE = "retake"
    PHOTO_EDITOR = "photo_editor"
    FINAL_PREVIEW = "final_preview"
    PAYMENT = "payment"
    PRINTING = "printing"
    QR_DOWNLOAD = "qr_download"
    THANK_YOU = "thank_you"


class BaseScreen(QWidget):
    """Base class for all customer screens."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(
            f"xinoobie.customer_interface.screens.{self.__class__.__name__}"
        )

    def setup_ui(self):
        """Subclasses should build their UI here."""
        raise NotImplementedError

    def show_error(self, title: str, message: str):
        """Show an error to the user."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, title, message)


# Screen registry: name -> class
SCREEN_REGISTRY: dict[str, Type[BaseScreen]] = {
    "welcome": WelcomeScreen,
    "language": LanguageScreen,
    "start": StartSessionScreen,
    "package": PackageScreen,
    "layout": LayoutScreen,
    "frame": FrameScreen,
    "filter": FilterScreen,
    "instructions": InstructionsScreen,
    "live_preview": LivePreviewScreen,
    "countdown": CountdownScreen,
    "capture": CaptureScreen,
    "photo_selection": PhotoSelectionScreen,
    "retake": RetakeScreen,
    "photo_editor": PhotoEditorScreen,
    "final_preview": FinalPreviewScreen,
    "payment": PaymentScreen,
    "printing": PrintingScreen,
    "qr_download": QRCodeDownloadScreen,
    "thank_you": ThankYouScreen,
}


def get_screen(name: str) -> Type[BaseScreen] | None:
    """Get a screen class by name."""
    return SCREEN_REGISTRY.get(name)


def get_all_screens() -> dict[str, Type[BaseScreen]]:
    """Return the full screen registry."""
    return SCREEN_REGISTRY.copy()
