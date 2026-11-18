"""Photo Session Engine - manage a photo shooting session.

Handles:
- Session lifecycle (create, start, pause, resume, cancel, complete)
- Counting
- Capture scheduling
- Photo storage
- Session recovery
- Session history
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir, generate_session_id
import os

config = Config.instance()
logger = get_logger("xinoobie.photo_session_engine")


class SessionState:
    """Session state machine states."""
    CREATED = "created"
    READY = "ready"
    COUNTDOWN = "countdown"
    CAPTURING = "capturing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RECOVERED = "recovered"


@dataclass
class SessionPhoto:
    """A single photo in a session."""
    photo_id: str
    file_path: str
    captures: int
    plate_number: str
    capture_time: datetime
    order: int


@dataclass
class PhotoSession:
    """A photo session."""
    session_id: str
    user_id: str
    package: dict
    layout: str
    frame: str
    filter: str
    state: str = SessionState.CREATED
    photos: list[SessionPhoto] = field(default_factory=list)
    retakes: int = 0
    max_retakes: int = 3
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cancelled: bool = False
    auto_recover: bool = True

    @property
    def photo_count(self) -> int:
        return len(self.photos)

    @property
    def is_active(self) -> bool:
        return self.state not in (SessionState.COMPLETED, SessionState.CANCELLED)

    def add_photo(self, file_path: str, plate_number: str = "", order: int = 0):
        """Add a photo to the session."""
        photo = SessionPhoto(
            photo_id=str(uuid4()),
            file_path=file_path,
            captures=1,
            plate_number=plate_number,
            capture_time=datetime.now(timezone.utc),
            order=order,
        )
        self.photos.append(photo)
        logger.info("Photo added to session %s: %s", self.session_id, file_path)
        return photo


class SessionManager:
    """Manages photo sessions."""

    def __init__(self):
        self._sessions: dict[str, PhotoSession] = {}
        self._session_counter = 0

    def create_session(self, user_id: str, package: dict,
                       layout: str, frame: str, filter: str) -> PhotoSession:
        """Create a new session."""
        session_id = generate_session_id("S")
        session = PhotoSession(
            session_id=session_id,
            user_id=user_id,
            package=package,
            layout=layout,
            frame=frame,
            filter=filter,
            state=SessionState.READY,
            max_retakes=int(config.session_defaults.get("max_retakes", 3)),
            start_time=datetime.now(timezone.utc),
        )
        self._sessions[session_id] = session
        logger.info("Session created: %s (user=%s)", session_id, user_id)
        return session

    def get_session(self, session_id: str) -> Optional[PhotoSession]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def update_session(self, session_id: str, **kwargs):
        """Update session fields."""
        session = self._sessions.get(session_id)
        if session:
            for key, value in kwargs.items():
                setattr(session, key, value)
            logger.info("Session updated: %s", session_id)

    def complete_session(self, session_id: str):
        """Mark a session as completed."""
        session = self._sessions.get(session_id)
        if session:
            session.end_time = datetime.now(timezone.utc)
            session.state = SessionState.COMPLETED
            logger.info("Session completed: %s", session_id)

    def cancel_session(self, session_id: str):
        """Cancel a session."""
        session = self._sessions.get(session_id)
        if session:
            session.cancelled = True
            session.state = SessionState.CANCELLED
            logger.info("Session cancelled: %s", session_id)

    def get_active_sessions(self) -> list[PhotoSession]:
        """Get all active sessions."""
        return [s for s in self._sessions.values() if s.is_active]

    def get_session_history(self) -> list[PhotoSession]:
        """Get all completed sessions."""
        return [s for s in self._sessions.values() if not s.is_active]
