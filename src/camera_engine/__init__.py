"""Camera Engine - abstract camera management layer.

Provides abstraction so other camera brands can be added later.
Phase 1 is a placeholder; Phase 2 implements real camera control.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger

config = Config.instance()
logger = get_logger("xinoobie.camera_engine")


@dataclass
class CameraInfo:
    """Information about a connected camera."""
    device_id: str
    manufacturer: str
    model: str
    resolution_width: int
    resolution_height: int
    supported_features: list[str]
    connected: bool = False


class Camera(ABC):
    """Abstract base class for camera devices."""

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the camera."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the camera."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check connection status."""
        pass

    @abstractmethod
    def start_preview(self) -> bool:
        """Start live preview."""
        pass

    @abstractmethod
    def stop_preview(self) -> bool:
        """Stop live preview."""
        pass

    @abstractmethod
    def capture(self) -> Optional[str]:
        """Capture a photo and return path."""
        pass

    @abstractmethod
    def set_auto_focus(self, enabled: bool) -> bool:
        """Set auto focus."""
        pass

    @abstractmethod
    def set_iso(self, iso: int) -> bool:
        """Set ISO."""
        pass

    @abstractmethod
    def set_shutter_speed(self, speed: float) -> bool:
        """Set shutter speed."""
        pass

    @abstractmethod
    def set_exposure_compensation(self, ev: int) -> bool:
        """Set exposure compensation."""
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Get current camera status."""
        return {}


class CameraManager:
    """Manages camera devices."""

    def __init__(self):
        self._cameras: dict[str, Camera] = {}
        self._active_camera: Optional[Camera] = None

    def register(self, camera: Camera, device_id: str):
        """Register a camera device."""
        self._cameras[device_id] = camera
        logger.info("Camera registered: %s (id=%s)", type(camera).__name__, device_id)

    def deregister(self, device_id: str):
        """Deregister a camera device."""
        if device_id in self._cameras:
            del self._cameras[device_id]
            logger.info("Camera deregistered: %s", device_id)

    def set_active(self, device_id: str) -> bool:
        """Set active camera."""
        if device_id not in self._cameras:
            logger.warning("Camera not found: %s", device_id)
            return False
        self._active_camera = self._cameras[device_id]
        logger.info("Active camera set: %s", device_id)
        return True

    def connect(self, device_id: str | None = None) -> bool:
        """Connect a camera by ID and make it active."""
        if device_id is None:
            return False
        if not self.set_active(device_id):
            return False
        return bool(self._active_camera and self._active_camera.connect())

    def disconnect(self, device_id: str | None = None) -> bool:
        """Disconnect a camera by ID."""
        if device_id is None:
            return False
        camera = self._cameras.get(device_id)
        if camera is None:
            return False
        return bool(camera.disconnect())

    def is_camera_connected(self, device_id: str | None = None) -> bool:
        """Check whether a camera by ID is connected."""
        if device_id is None:
            return False
        camera = self._cameras.get(device_id)
        return bool(camera and camera.is_connected())

    def get_active(self) -> Optional[Camera]:
        """Get active camera."""
        return self._active_camera

    def list_cameras(self) -> list[CameraInfo]:
        """List all known cameras."""
        result = []
        for device_id, cam in self._cameras.items():
            # This would be filled by camera-specific implementations
            result.append(CameraInfo(
                device_id=device_id,
                manufacturer="Unknown",
                model="Unknown",
                resolution_width=1920,
                resolution_height=1080,
                supported_features=["capture", "preview"],
                connected=cam.is_connected(),
            ))
        return result

    def start_preview(self, device_id: str | None = None) -> bool:
        """Start preview on active camera."""
        if device_id is not None and not self.set_active(device_id):
            return False
        if self._active_camera is None:
            logger.warning("No active camera set")
            return False
        result = self._active_camera.start_preview()
        logger.info("Preview started: %s", result)
        return result

    def stop_preview(self, device_id: str | None = None) -> bool:
        """Stop preview on active camera."""
        if device_id is not None:
            camera = self._cameras.get(device_id)
            if camera is not None:
                return bool(camera.stop_preview())
        if self._active_camera is None:
            return False
        result = self._active_camera.stop_preview()
        logger.info("Preview stopped: %s", result)
        return result

    def capture(self) -> Optional[str]:
        """Capture photo on active camera."""
        if self._active_camera is None:
            logger.warning("No active camera set")
            return None
        return self._active_camera.capture()


# Placeholder camera for Phase 1 (simulates a camera)
class MockCamera(Camera):
    """Mock camera for testing/Phase 1."""

    def __init__(self):
        self._connected = False
        self._preview_running = False
        self._counter = 0

    def connect(self) -> bool:
        self._connected = True
        self._counter = 0
        logger.info("Mock camera connected")
        return True

    def disconnect(self) -> bool:
        self._connected = False
        self._preview_running = False
        logger.info("Mock camera disconnected")
        return True

    def is_connected(self) -> bool:
        return self._connected

    def start_preview(self) -> bool:
        if not self._connected:
            return False
        self._preview_running = True
        logger.info("Mock camera preview started")
        return True

    def stop_preview(self) -> bool:
        self._preview_running = False
        logger.info("Mock camera preview stopped")
        return True

    def capture(self) -> str:
        self._counter += 1
        import os
        from app_core.utils import ensure_dir
        save_dir = os.path.join(config.data_dir, "capture")
        ensure_dir(save_dir)
        filename = f"capture_{self._counter}.png"
        filepath = os.path.join(save_dir, filename)
        # Create a simple placeholder image
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (1920, 1080), (30, 41, 58))
        draw = ImageDraw.Draw(img)
        draw.text((960, 540), f"Capture {self._counter}", fill=(248, 250, 252))
        img.save(filepath)
        logger.info("Mock capture saved: %s", filepath)
        return filepath

    def get_status(self) -> dict:
        return {
            "connected": self._connected,
            "preview": self._preview_running,
            "capture_count": self._counter,
        }

    # Abstract method implementations
    def set_auto_focus(self, enabled: bool) -> bool:
        logger.info("Mock camera auto focus set to %s", enabled)
        return enabled

    def set_iso(self, iso: int) -> bool:
        logger.info("Mock camera ISO set to %s", iso)
        return True

    def set_shutter_speed(self, speed: float) -> bool:
        logger.info("Mock camera shutter speed set to %s", speed)
        return True

    def set_exposure_compensation(self, ev: int) -> bool:
        logger.info("Mock camera exposure compensation set to %s", ev)
        return True


# Configuration for camera profiles
@dataclass
class CameraProfile:
    """Camera configuration profile."""
    name: str
    iso: int = 100
    shutter_speed: float = 1/125
    aperture: str = "f/5.6"
    white_balance: str = "auto"
    exposure_compensation: int = 0
    auto_focus: bool = True


class CameraProfileManager:
    """Manage camera configuration profiles."""

    def __init__(self):
        self._profiles: dict[str, CameraProfile] = {}
        self._default_profile = "default"

    def add_profile(self, profile: CameraProfile):
        """Add a camera profile."""
        self._profiles[profile.name] = profile
        logger.info("Camera profile added: %s", profile.name)

    def remove_profile(self, name: str):
        """Remove a camera profile."""
        if name in self._profiles:
            del self._profiles[name]
            logger.info("Camera profile removed: %s", name)

    def get_profile(self, name: str) -> Optional[CameraProfile]:
        """Get a camera profile."""
        return self._profiles.get(name)

    def set_default(self, name: str):
        """Set default profile."""
        if name in self._profiles:
            self._default_profile = name
            logger.info("Default camera profile set: %s", name)
