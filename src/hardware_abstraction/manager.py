"""Hardware Abstraction Layer - abstract hardware interfaces.

Provides a common interface for hardware devices.
Phase 1 is a stub; Phase 2 will implement real hardware interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app_core.logging_config import get_logger

logger = get_logger("xinoobie.hardware_abstraction")


class CameraInterface(ABC):
    """Abstract camera interface."""
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def start_preview(self) -> bool:
        pass

    @abstractmethod
    def stop_preview(self) -> bool:
        pass

    @abstractmethod
    def capture(self) -> str:
        pass


class PrinterInterface(ABC):
    """Abstract printer interface."""
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def print(self, file_path: str, quantity: int) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> dict:
        pass


class TouchscreenInterface(ABC):
    """Abstract touchscreen interface."""
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def get_display_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_brightness(self, level: int) -> bool:
        pass


class HardwareManager:
    """Manages hardware devices."""
    def __init__(self):
        self._cameras: list[CameraInterface] = []
        self._printers: list[PrinterInterface] = []
        self._touchscreens: list[TouchscreenInterface] = []

    def register_camera(self, cam: CameraInterface):
        """Register a camera."""
        self._cameras.append(cam)

    def register_printer(self, printer: PrinterInterface):
        """Register a printer."""
        self._printers.append(printer)

    def register_touchscreen(self, screen: TouchscreenInterface):
        """Register a touchscreen."""
        self._touchscreens.append(screen)

    def get_cameras(self) -> list[CameraInterface]:
        """Get all registered cameras."""
        return self._cameras

    def get_printers(self) -> list[PrinterInterface]:
        """Get all registered printers."""
        return self._printers

    def get_touchscreens(self) -> list[TouchscreenInterface]:
        """Get all registered touchscreens."""
        return self._touchscreens
