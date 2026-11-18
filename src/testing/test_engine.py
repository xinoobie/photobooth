"""Testing - unit tests for Xinoobie Photobooth.

Phase 1: Basic test structure and mock-based tests.
"""

from __future__ import annotations

import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app_core.utils import generate_session_id
from app_core.config import Config
from database.database import DatabaseManager


class TestUtils:
    """Test utility functions."""

    def test_generate_session_id(self):
        """Test session ID generation."""
        sid = generate_session_id("S")
        assert sid.startswith("S-")
        assert len(sid) > 5


class TestConfig:
    """Test configuration loading."""

    def test_config_instance(self):
        """Test config singleton."""
        config = Config.instance()
        assert config is not None
        assert config.app_name == "Xinoobie Photobooth"


class TestDatabase:
    """Test database operations."""

    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connection."""
        config = Config.instance()
        db = DatabaseManager(config.db_path)
        # Test connection without actually connecting
        assert db.engine is not None
        assert db.session_factory is not None


class TestCameraEngine:
    """Test camera engine."""

    @pytest.mark.asyncio
    async def test_mock_camera_capture(self):
        """Test mock camera capture."""
        from camera_engine import MockCamera

        mock = MockCamera()
        assert mock.connect() is True
        assert mock.is_connected() is True

        path = mock.capture()
        assert path is not None
        assert os.path.exists(path)

        mock.disconnect()
        assert mock.is_connected() is False


class TestPhotoSessionEngine:
    """Test photo session engine."""

    def test_session_creation(self):
        """Test session creation."""
        from photo_session_engine import SessionManager, PhotoSession

        manager = SessionManager()
        session = manager.create_session(
            user_id="test_user",
            package={"name": "Default", "price": 25000},
            layout="2x6",
            frame="default",
            filter="none",
        )
        assert session is not None
        assert session.session_id.startswith("S-")
        assert session.state == "ready"


class TestFrameEngine:
    """Test frame engine."""

    def test_frame_manager(self):
        """Test frame manager."""
        from frame_engine import FrameManager

        # Create temp frame dir
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            fm = FrameManager(tmpdir)
            frames = fm.get_all()
            # Should have at least the default frame
            assert len(frames) >= 1


class TestQRCode:
    """Test QR code generation."""

    def test_qr_generator(self):
        """Test QR code generation."""
        from qr_engine import QRManager

        qr = QRManager()
        url = qr.generate_gallery_url("S-123456")
        assert url.startswith("https://xinoobie.example/gallery/")
