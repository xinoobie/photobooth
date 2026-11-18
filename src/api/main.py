"""API - FastAPI HTTP API for the application.

Phase 1: Basic API structure for future admin dashboard integration.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from app_core.config import Config

config = Config.instance()
app = FastAPI(title="Xinoobie Photobooth API")

# ── Models ──────────────────────────────────────────────────────────
class Package(BaseModel):
    id: str
    name: str
    price: float
    photo_count: int
    retake_limit: int


class SessionCreate(BaseModel):
    user_id: str
    package_id: str
    layout: str
    frame: str
    filter: str


# ── In-memory store (placeholder for real database) ─────────────────
_packages = [
    Package(id="pkg_1", name="Default 2x6 Strip", price=25000, photo_count=2, retake_limit=3),
]
_sessions = []
_next_id = 1


# ── Routes ──────────────────────────────────────────────────────────
@app.get("/api/packages")
def list_packages():
    """List all packages."""
    return _packages


@app.post("/api/sessions")
def create_session(payload: SessionCreate):
    """Create a new session."""
    global _next_id
    session = {
        "id": f"S-{_next_id:06d}",
        "user_id": payload.user_id,
        "package_id": payload.package_id,
        "layout": payload.layout,
        "frame": payload.frame,
        "filter": payload.filter,
        "created_at": "2026-11-17T00:00:00Z",
    }
    _sessions.append(session)
    _next_id += 1
    return session


@app.get("/api/sessions")
def list_sessions():
    """List all sessions."""
    return _sessions


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "database": "connected"}
