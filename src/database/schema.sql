-- ============================================================================
-- Xinoobie Photobooth — SQLite Database Schema
-- Database: SQLite 3 (async, SQLAlchemy)
-- Version: 1.0
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    role_id       INTEGER NOT NULL,
    pin           TEXT NOT NULL,  -- Hashed PIN (e.g., PBKDF2)
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT users_role_fk FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS roles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT,
    can_manage  INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL UNIQUE,       -- Human-readable unique ID
    user_id         INTEGER NOT NULL,
    package_id      INTEGER,
    language        TEXT NOT NULL DEFAULT 'id',
    booth_id        TEXT,
    branch_id       TEXT,
    payment_id      INTEGER,
    status          TEXT NOT NULL,              -- active, complete, cancelled, recovered
    started_at      TEXT NOT NULL,
    completed_at    TEXT,
    duration_seconds INTEGER,
    total_photos    INTEGER,
    total_prints    INTEGER,
    total_revenue   REAL,
    notes           TEXT,
    CONSTRAINT sessions_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT sessions_package_fk FOREIGN KEY (package_id) REFERENCES packages(id),
    CONSTRAINT sessions_payment_fk FOREIGN KEY (payment_id) REFERENCES transactions(id)
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_started
    ON sessions(user_id, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_sessions_status
    ON sessions(status);

CREATE INDEX IF NOT EXISTS idx_sessions_package
    ON sessions(package_id);

CREATE TABLE IF NOT EXISTS session_photos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    photo_index     INTEGER NOT NULL,
    original_path   TEXT,
    processed_path  TEXT,
    layout_path     TEXT,
    width           INTEGER,
    height          INTEGER,
    created_at      TEXT NOT NULL,
    is_selected     INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT session_photos_session_fk FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_session_photos_session
    ON session_photos(session_id, photo_index);

CREATE INDEX IF NOT EXISTS idx_session_photos_processed
    ON session_photos(processed_path);

CREATE TABLE IF NOT EXISTS packages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    description     TEXT,
    photo_count     INTEGER NOT NULL,
    price           REAL NOT NULL,
    retake_limit    INTEGER NOT NULL DEFAULT 3,
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    category        TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_packages_enabled
    ON packages(is_enabled);

CREATE INDEX IF NOT EXISTS idx_packages_price
    ON packages(price);

CREATE TABLE IF NOT EXISTS frames (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    description     TEXT,
    image_path      TEXT NOT NULL,
    category        TEXT,
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    price           REAL,                       -- Optional additional price
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_frames_enabled
    ON frames(is_enabled);

CREATE INDEX IF NOT EXISTS idx_frames_category
    ON frames(category);

CREATE TABLE IF NOT EXISTS filters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    description     TEXT,
    key             TEXT NOT NULL,
    parameters      TEXT,                       -- JSON
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    order_index     INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_filters_enabled
    ON filters(is_enabled);

CREATE TABLE IF NOT EXISTS layouts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    description     TEXT,
    type            TEXT NOT NULL,              -- strip, single, custom
    width           INTEGER NOT NULL,           -- in pixels
    height          INTEGER NOT NULL,
    photo_count     INTEGER NOT NULL,
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    config          TEXT,                       -- JSON layout configuration
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_layouts_enabled
    ON layouts(is_enabled);

CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    package_id      INTEGER NOT NULL,
    amount          REAL NOT NULL,
    payment_method  TEXT NOT NULL,
    method_reference TEXT,
    status          TEXT NOT NULL,              -- pending, completed, failed, refunded
    refunded_amount REAL DEFAULT 0,
    voucher_code    TEXT,
    notes           TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    CONSTRAINT transactions_session_fk FOREIGN KEY (session_id) REFERENCES sessions(id),
    CONSTRAINT transactions_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT transactions_package_fk FOREIGN KEY (package_id) REFERENCES packages(id)
);

CREATE INDEX IF NOT EXISTS idx_transactions_session
    ON transactions(session_id);

CREATE INDEX IF NOT EXISTS idx_transactions_user
    ON transactions(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_transactions_status
    ON transactions(status);

CREATE INDEX IF NOT EXISTS idx_transactions_created
    ON transactions(created_at DESC);

CREATE TABLE IF NOT EXISTS payment_methods (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    code            TEXT NOT NULL UNIQUE,
    description     TEXT,
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS printers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    device_name     TEXT NOT NULL,
    connection_type TEXT NOT NULL,              -- usb, network
    is_enabled      INTEGER NOT NULL DEFAULT 1,
    last_used_at    TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS print_jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    photo_id        INTEGER,
    printer_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL DEFAULT 1,
    paper_size      TEXT NOT NULL,
    resolution_dpi  INTEGER NOT NULL DEFAULT 300,
    status          TEXT NOT NULL,              -- pending, printing, completed, failed, cancelled
    error_message   TEXT,
    retry_count     INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL,
    started_at      TEXT,
    completed_at    TEXT,
    CONSTRAINT print_jobs_session_fk FOREIGN KEY (session_id) REFERENCES sessions(id),
    CONSTRAINT print_jobs_photo_fk FOREIGN KEY (photo_id) REFERENCES session_photos(id),
    CONSTRAINT print_jobs_printer_fk FOREIGN KEY (printer_id) REFERENCES printers(id)
);

CREATE INDEX IF NOT EXISTS idx_print_jobs_session
    ON print_jobs(session_id);

CREATE INDEX IF NOT EXISTS idx_print_jobs_status
    ON print_jobs(status);

CREATE INDEX IF NOT EXISTS idx_print_jobs_printer
    ON print_jobs(printer_id);

CREATE TABLE IF NOT EXISTS digital_galleries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL UNIQUE,
    qr_code_path    TEXT,
    password_hash   TEXT,                       -- Encrypted/hashed
    expires_at      TEXT,
    cloud_url       TEXT,
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    CONSTRAINT digital_galleries_session_fk FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS system_settings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    key             TEXT NOT NULL UNIQUE,
    value           TEXT NOT NULL,
    description     TEXT,
    updated_at      TEXT NOT NULL,
    CONSTRAINT system_settings_key_uq UNIQUE (key)
);

-- Default settings
INSERT OR IGNORE INTO system_settings (key, value, description, updated_at) VALUES
    ('default_language', 'id', 'Default interface language', '2026-11-17T00:00:00Z'),
    ('default_language_timezone', 'Asia/Jakarta', 'Application timezone', '2026-11-17T00:00:00Z'),
    ('retention_days', '90', 'Session photo retention in days', '2026-11-17T00:00:00Z'),
    ('kiosk_mode', 'false', 'Kiosk fullscreen mode', '2026-11-17T00:00:00Z'),
    ('auto_start', 'false', 'Auto-start on boot', '2026-11-17T00:00:00Z'),
    ('max_retake_limit', '3', 'Maximum retake count per session', '2026-11-17T00:00:00Z');

CREATE TABLE IF NOT EXISTS activity_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER,
    action          TEXT NOT NULL,
    target_type     TEXT,
    target_id       INTEGER,
    details         TEXT,                       -- JSON
    ip_address      TEXT,
    user_agent      TEXT,
    created_at      TEXT NOT NULL,
    CONSTRAINT activity_logs_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_activity_logs_created
    ON activity_logs(created_at DESC);
