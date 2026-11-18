"""Migration manager for Xinoobie Photobooth database.

Using a simple versioned migration approach (alembic-style simplified).
"""

from __future__ import annotations

import hashlib
import log_utils
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy import text

from .database import Database
from .models import Base

logger = logging.getLogger("xinoobie.database.migrations")

# Directory for migration scripts
MIGRATIONS_DIR = Path(__file__).parent / "migrations"


class Migration:
    """Represents a single database migration."""

    def __init__(self, version: str, description: str, up_sql: str, down_sql: Optional[str] = None):
        self.version = version
        self.description = description
        self.up_sql = up_sql
        self.down_sql = down_sql

    def __lt__(self, other: "Migration") -> bool:
        return self.version < other.version


class MigrationManager:
    """Handles database schema migrations."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._applied: list[Migration] = []
        self._versions_table = "schema_versions"

    async def _ensure_versions_table(self) -> None:
        """Create the schema_versions table if it doesn't exist."""
        async with self._db.engine.begin() as conn:
            await conn.exec_driver_sql(f"""
                CREATE TABLE IF NOT EXISTS {self._versions_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT NOT NULL UNIQUE,
                    description TEXT,
                    applied_at TEXT NOT NULL
                )
            """)

    async def _get_applied_versions(self) -> list[str]:
        """Return list of applied version strings (sorted)."""
        async with self._db.engine.begin() as conn:
            result = await conn.execute(text(f"SELECT version FROM {self._versions_table} ORDER BY id"))
            rows = result.fetchall()
            return [row[0] for row in rows]

    async def _record_migration(self, migration: Migration) -> None:
        """Record a migration as applied."""
        now = datetime.now(timezone.utc).isoformat()
        async with self._db.engine.begin() as conn:
            await conn.exec_driver_sql(f"""
                INSERT INTO {self._versions_table} (version, description, applied_at)
                VALUES (:version, :description, :applied_at)
            """, {"version": migration.version, "description": migration.description, "applied_at": now})

    async def _get_all_migrations(self) -> list[Migration]:
        """Load all migration files from the migrations directory."""
        migrations = []

        # Load from migrations directory
        if MIGRATIONS_DIR.exists():
            for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
                version = migration_file.stem
                # Parse description from SQL header comments
                sql = migration_file.read_text(encoding="utf-8")
                description = ""
                for line in sql.splitlines():
                    if line.strip().startswith("-- MIGRATION:"):
                        description = line.split(":", 1)[1].strip()
                        break

                # Also support .py migration files
                migration_py = migration_file.with_suffix(".py")
                if migration_py.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        f"migration_{version}", migration_py
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "migration"):
                        module_migration = module.migration
                        if isinstance(module_migration, Migration):
                            migrations.append(module_migration)

        # Also scan for .sql files directly
        for sql_file in MIGRATIONS_DIR.glob("*.sql"):
            version = sql_file.stem
            sql = sql_file.read_text(encoding="utf-8")
            description = ""
            for line in sql.splitlines():
                if line.strip().startswith("-- MIGRATION:"):
                    description = line.split(":", 1)[1].strip()
                    break
            migrations.append(Migration(version, description, sql))

        # Sort by version
        migrations.sort(key=lambda m: m.version)
        return migrations

    async def migrate(self) -> list[str]:
        """Run all pending migrations. Returns list of applied version strings."""
        await self._ensure_versions_table()
        applied = await self._get_applied_versions()

        migrations = await self._get_all_migrations()
        pending = [m for m in migrations if m.version not in applied]

        logger.info("Current schema versions applied: %s", applied)
        logger.info("Pending migrations: %s", [m.version for m in pending])

        applied_versions: list[str] = []
        for migration in pending:
            logger.info("Applying migration %s: %s", migration.version, migration.description)
            try:
                async with self._db.engine.begin() as conn:
                    await conn.exec_driver_sql(migration.up_sql)
                await self._record_migration(migration)
                applied_versions.append(migration.version)
                logger.info("Migration %s applied successfully", migration.version)
            except Exception as exc:
                logger.error("Migration %s failed: %s", migration.version, exc)
                raise

        return applied_versions


# Module-level singleton
_migration_manager: MigrationManager | None = None


def get_migration_manager(db: Optional[Database] = None) -> MigrationManager:
    global _migration_manager
    if _migration_manager is None:
        if db is None:
            from .database import get_db
            db = get_db()
        _migration_manager = MigrationManager(db)
    return _migration_manager
