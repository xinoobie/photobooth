"""Main application entry point for Xinoobie Photobooth."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app_core.config import Config
from app_core.logging_config import setup_logging, get_logger
from customer_interface.main_window import MainApplicationWindow

config = Config.instance()

# Setup
setup_logging(config)
logger = get_logger("xinoobie.main")


def main():
    """Application entry point."""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName(config.app_name)
    app.setApplicationVersion(config.app_version)

    # Create and show main window
    window = MainApplicationWindow()
    window.show()

    # Set up exception handling
    sys.excepthook = config.exception_handler

    logger.info("Starting %s %s", config.app_name, config.app_version)
    logger.info("Theme: %s", config.theme)
    logger.info("Screen: %dx%d @%d", config.window_width, config.window_height, config.dpi)

    # Run the application
    exit_code = app.exec()
    logger.info("Application exited with code %d", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
