"""Async SQLite database engine for Xinoobie Photobooth.

Uses SQLAlchemy 2.0 with aiosqlite backend.

Connection URL: sqlite+aiosqlite:///path/to/db
"""

from __future__ import annotations

import asyncio
import logging
import log_utils
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app_core.config import Config

_config = Config.instance()
logger = logging.getLogger("xinoobie.database")


class Database:
    """Async SQLite database manager.

    Handles connection, session creation, schema initialization, and
    (future) migration management. Designed to be swappable with PostgreSQL
    later via connection URL change only.
    """

    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path or _config.db_path
        self._engine = None
        self._session_factory = None
        self._initialized = False
        # Prevent concurrent init from multiple threads
        self._init_lock = asyncio.Lock()

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_async_engine(
                f"sqlite+aiosqlite:///{self._db_path}",
                echo=False,
                future=True,
                connect_args={"check_same_thread": False},
            )
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                self.engine, expire_on_commit=False
            )
        return self._session_factory

    async def init_db(self, create_tables: bool = True) -> None:
        """Initialize the database: create directory, tables, and seed data."""
        async with self._init_lock:
            if self._initialized:
                return

            # Ensure data directory exists
            self._db_path.parent.mkdir(parents=True, exist_ok=True)

            if create_tables:
                async with self.engine.begin() as conn:
                    # Read and execute schema
                    schema_path = Path(__file__).parent / "schema.sql"
                    if schema_path.exists():
                        sql = schema_path.read_text(encoding="utf-8")
                        await conn.exec_driver_sql(sql)
                    else:
                        logger.warning(
                            "Schema file not found; skipping table creation"
                        )

                    # Seed default system settings (only if not exists)
                    seed_queries = [
                        "INSERT OR IGNORE INTO system_settings "
                        "(key, value, description, updated_at) VALUES "
                        "('default_language', 'id', 'Default interface language', "
                        "'2026-11-17T00:00:00Z'), "
                        "('default_language_timezone', 'Asia/Jakarta', "
                        "'Application timezone', '2026-11-17T00:00:00Z'), "
                        "('retention_days', '90', 'Session photo retention in days', "
                        "'2026-11-17T00:00:00Z'), "
                        "('kiosk_mode', 'false', 'Kiosk fullscreen mode', "
                        "'2026-11-17T00:00:00Z'), "
                        "('auto_start', 'false', 'Auto-start on boot', "
                        "'2026-11-17T00:00:00Z'), "
                        "('max_retake_limit', '3', 'Maximum retake count per session', "
                        "'2026-11-17T00:00:00Z');"
                    ]
                    for query in seed_queries:
                        await conn.exec_driver_sql(query)

            self._initialized = True
            logger.info("Database initialized at %s", self._db_path)

    async def get_session(self) -> AsyncSession:
        """Get a new async session."""
        async with self.session_factory() as session:
            yield session

    async def query(self, stmt) -> list[Any]:
        """Execute a select statement and return results."""
        async with self.session_factory() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def execute(self, stmt) -> Any:
        """Execute a non-select statement (insert/update/delete)."""
        async with self.session_factory() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result

    async def close(self) -> None:
        """Close all connections."""
        if self._engine is not None:
            await self.engine.dispose()
            logger.info("Database connections closed")


# Module-level singleton (created lazily)
_db_instance: Database | None = None


def get_db() -> Database:
    """Get the database singleton."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(_config.db_path)
    return _db_instance
