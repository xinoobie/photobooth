"""Admin Dashboard - FastAPI backend for admin operations.

Features:
- Admin authentication
- Session management
- Transaction management
- Package management
- Template management
- Hardware management
- Storage management
- Analytics
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Xinoobie Photobooth Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ──────────────────────────────────────────────────────────
class AdminLogin(BaseModel):
    username: str
    password: str


class PackageCreate(BaseModel):
    name: str
    price: float
    photo_count: int
    retake_limit: int = 3
    is_enabled: bool = True


class SessionCreate(BaseModel):
    user_id: str
    package_name: str
    layout: str
    frame: str
    filter: str


# ── Routes ──────────────────────────────────────────────────────────
@app.post("/admin/login")
def admin_login(payload: AdminLogin):
    """Admin login endpoint."""
    # TODO: Real authentication
    if payload.username == "admin" and payload.password == "password":
        return {"success": True, "token": "admin-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/admin/overview")
def admin_overview():
    """Get dashboard overview."""
    return {
        "total_sessions": 0,
        "daily_revenue": 0.0,
        "monthly_revenue": 0.0,
        "total_prints": 0,
        "active_booths": 1,
        "device_status": "ready",
    }


@app.get("/admin/sessions")
def get_sessions():
    """Get all sessions."""
    return []


@app.get("/admin/packages")
def get_packages():
    """Get all packages."""
    return [
        {
            "id": "pkg_1",
            "name": "Default 2x6 Strip",
            "price": 25000,
            "photo_count": 2,
            "retake_limit": 3,
        }
    ]


@app.post("/admin/packages")
def create_package(payload: PackageCreate):
    """Create a new package."""
    return {"id": f"pkg_{uuid.uuid4().hex[:8]}", **payload.dict()}


@app.get("/admin/hardware")
def get_hardware():
    """Get hardware status."""
    return {
        "cameras": [],
        "printers": [],
        "touchscreens": [],
    }
