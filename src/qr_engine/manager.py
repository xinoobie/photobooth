"""QR Engine - generate QR codes for digital delivery.

Features:
- QR code generation
- Digital gallery creation
- Link generation
- Expiry management
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional

try:
    import qrcode
    _HAVE_QRCODE = True
except ImportError:
    qrcode = None
    _HAVE_QRCODE = False

from PIL import Image

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir

config = Config.instance()
logger = get_logger("xinoobie.qr_engine")


@dataclass
class DigitalGallery:
    """A digital gallery for a session."""
    gallery_id: str
    session_id: str
    creator_id: str
    title: str
    description: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    password: Optional[str] = None
    is_public: bool = False
    photo_paths: list[str] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        """Check if gallery has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at


class QRManager:
    """Manages QR code generation and digital delivery."""

    def __init__(self):
        self._galleries: dict[str, DigitalGallery] = {}
        self._gallery_counter = 0

    def create_gallery(self, session_id: str, creator_id: str,
                       title: str, photo_paths: list[str],
                       days_to_expire: int = 7,
                       is_public: bool = False) -> DigitalGallery:
        """Create a digital gallery."""
        gallery_id = f"GAL-{uuid.uuid4().hex[:8].upper()}"
        gallery = DigitalGallery(
            gallery_id=gallery_id,
            session_id=session_id,
            creator_id=creator_id,
            title=title,
            description=f"Session {session_id} - {title}",
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=days_to_expire),
            is_public=is_public,
            photo_paths=photo_paths,
        )
        self._galleries[gallery_id] = gallery
        logger.info("Digital gallery created: %s (session=%s)", gallery_id, session_id)
        return gallery

    def get_gallery(self, gallery_id: str) -> Optional[DigitalGallery]:
        """Get a gallery by ID."""
        return self._galleries.get(gallery_id)

    def get_galleries_by_session(self, session_id: str) -> list[DigitalGallery]:
        """Get all galleries for a session."""
        return [g for g in self._galleries.values()
                if g.session_id == session_id]

    def get_public_galleries(self) -> list[DigitalGallery]:
        """Get all public galleries."""
        return [g for g in self._galleries.values() if g.is_public]

    def generate_qr_code(self, url: str, file_path: Optional[str] = None) -> str:
        """Generate a QR code and optionally save it."""
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#3B82F6", back_color="white")
        buf = os.path.join(config.data_dir, "qr_cache")
        ensure_dir(buf)

        if file_path:
            img.save(file_path)
            logger.info("QR code saved: %s", file_path)
            return file_path

        # Return as bytes
        import io
        buf = os.path.join(config.data_dir, "qr_cache")
        ensure_dir(buf)
        fname = f"qr_{uuid.uuid4().hex[:8]}.png"
        fpath = os.path.join(buf, fname)
        img.save(fpath)
        logger.info("QR code saved: %s", fpath)
        return fpath

    def generate_gallery_url(self, session_id: str) -> str:
        """Generate a gallery URL for a session."""
        return f"https://xinoobie.example/gallery/{session_id}"

    def check_gallery_access(self, gallery_id: str, password: Optional[str] = None) -> tuple[bool, str]:
        """Check if a gallery can be accessed."""
        gallery = self._galleries.get(gallery_id)
        if not gallery:
            return False, "Gallery not found"

        if gallery.is_expired:
            return False, "Gallery expired"

        # Check if password required
        if gallery.password and password != gallery.password:
            return False, "Incorrect password"

        return True, "Access granted"
