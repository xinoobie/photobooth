"""Base Screen class for all customer screens.

Exports BaseScreen and ScreenId for use by screen modules.
"""

from __future__ import annotations

import logging

from PySide6.QtWidgets import QWidget

__all__ = ["BaseScreen", "ScreenId"]


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
