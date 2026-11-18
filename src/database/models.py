"""ORM models for Xinoobie Photobooth — SQLAlchemy 2.0 declarative base."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import(
    Boolean,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    LargeBinary,
    Index,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    pin_hash: Mapped[str] = mapped_column(String(128), nullable=False)  # PIN (hashed)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    role: Mapped["Role"] = relationship(
        "Role", back_populates="users", lazy="selectin"
    )
    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )
    activity_logs: Mapped[list["ActivityLog"]] = relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan"
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    can_manage: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="role", cascade="all, delete-orphan"
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    package_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("packages.id")
    )
    language: Mapped[str] = mapped_column(
        String(8), nullable=False, default="id"
    )
    booth_id: Mapped[Optional[str]] = mapped_column(String(32))
    branch_id: Mapped[Optional[str]] = mapped_column(String(32))
    payment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("transactions.id")
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # active, complete, cancelled, recovered
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=utcnow
    )
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    total_photos: Mapped[int] = mapped_column(Integer, default=0)
    total_prints: Mapped[int] = mapped_column(Integer, default=0)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    # Images
    photos: Mapped[list["SessionPhoto"]] = relationship(
        "SessionPhoto", back_populates="session",
        cascade="all, delete-orphan",
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    package: Mapped[Optional["Package"]] = relationship(
        "Package", back_populates="sessions"
    )
    # The payment transaction (FK: sessions.payment_id -> transactions.id)
    payment: Mapped[Optional["Transaction"]] = relationship(
        "Transaction", foreign_keys=[payment_id]
    )

    # Print jobs created for this session
    print_jobs: Mapped[list["PrintJob"]] = relationship(
        "PrintJob", back_populates="session", cascade="all, delete-orphan"
    )


Index("idx_sessions_user_started", "user_id", "started_at.desc()")
Index("idx_sessions_status", "status")
Index("idx_sessions_package", "package_id")


class SessionPhoto(Base):
    __tablename__ = "session_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"), index=True, nullable=False
    )
    photo_index: Mapped[int] = mapped_column(Integer, nullable=False)
    original_path: Mapped[Optional[str]] = mapped_column(Text)
    processed_path: Mapped[Optional[str]] = mapped_column(Text)
    layout_path: Mapped[Optional[str]] = mapped_column(Text)
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    is_selected: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    session: Mapped["Session"] = relationship(
        "Session", back_populates="photos"
    )

    # Print jobs created from this photo
    print_jobs: Mapped[list["PrintJob"]] = relationship(
        "PrintJob", back_populates="photo", cascade="all, delete-orphan"
    )


Index("idx_session_photos_session", "session_id", "photo_index")
Index("idx_session_photos_processed", "processed_path")


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    retake_limit: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3
    )
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    category: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="package", cascade="all, delete-orphan"
    )

Index("idx_packages_enabled", "is_enabled")
Index("idx_packages_price", "price")


class Frame(Base):
    __tablename__ = "frames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_path: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(64))
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    price: Mapped[Optional[float]] = mapped_column(Float)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    Index("idx_frames_enabled", "is_enabled")
    Index("idx_frames_category", "category")


class Filter(Base):
    __tablename__ = "filters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    parameters: Mapped[Optional[dict]] = mapped_column(Text)  # JSON
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    order_index: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    Index("idx_filters_enabled", "is_enabled")


class Layout(Base):
    __tablename__ = "layouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    config: Mapped[Optional[dict]] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    Index("idx_layouts_enabled", "is_enabled")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"), index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    package_id: Mapped[int] = mapped_column(
        ForeignKey("packages.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(32), nullable=False)
    method_reference: Mapped[Optional[str]] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # pending, completed, failed, refunded
    refunded_amount: Mapped[float] = mapped_column(Float, default=0.0)
    voucher_code: Mapped[Optional[str]] = mapped_column(String(64))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    # Asymmetric relationship: Transaction.session_id -> sessions.id
    session: Mapped[Optional["Session"]] = relationship(
        "Session", foreign_keys=[session_id]
    )
    user: Mapped["User"] = relationship("User", back_populates="transactions")
    package: Mapped["Package"] = relationship("Package", back_populates="sessions")

Index("idx_transactions_session", "session_id")
Index("idx_transactions_user", "user_id", "created_at.desc()")
Index("idx_transactions_status", "status")
Index("idx_transactions_created", "created_at.desc()")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )


class Printer(Base):
    __tablename__ = "printers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    device_name: Mapped[str] = mapped_column(String(256), nullable=False)
    connection_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=utcnow
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    # Print jobs sent to this printer
    print_jobs: Mapped[list["PrintJob"]] = relationship(
        "PrintJob", back_populates="printer", cascade="all, delete-orphan"
    )


class PrintJob(Base):
    __tablename__ = "print_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"), index=True, nullable=False
    )
    photo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("session_photos.id")
    )
    printer_id: Mapped[int] = mapped_column(
        ForeignKey("printers.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    paper_size: Mapped[str] = mapped_column(String(32), nullable=False)
    resolution_dpi: Mapped[int] = mapped_column(
        Integer, nullable=False, default=300
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # pending, printing, completed, failed, cancelled
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    session: Mapped["Session"] = relationship("Session", back_populates="print_jobs")
    photo: Mapped[Optional["SessionPhoto"]] = relationship(
        "SessionPhoto", back_populates="print_jobs"
    )
    printer: Mapped["Printer"] = relationship("Printer", back_populates="print_jobs")

Index("idx_print_jobs_session", "session_id")
Index("idx_print_jobs_status", "status")
Index("idx_print_jobs_printer", "printer_id")


class DigitalGallery(Base):
    __tablename__ = "digital_galleries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"), unique=True, nullable=False, index=True
    )
    qr_code_path: Mapped[Optional[str]] = mapped_column(Text)
    password_hash: Mapped[Optional[str]] = mapped_column(Text)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    cloud_url: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )

    session: Mapped["Session"] = relationship(
        "Session", back_populates="gallery"
    )


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow, onupdate=utcnow
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    target_type: Mapped[Optional[str]] = mapped_column(String(64))
    target_id: Mapped[Optional[int]] = mapped_column(Integer)
    details: Mapped[Optional[dict]] = mapped_column(Text)  # JSON
    ip_address: Mapped[Optional[str]] = mapped_column(String(48))
    user_agent: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="activity_logs")

Index("idx_activity_logs_created", "created_at.desc()")
