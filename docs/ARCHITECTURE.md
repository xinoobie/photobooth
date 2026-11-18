# System Architecture — Xinoobie Photobooth

**Version:** 1.0
**Date:** 2026-11-17

---

## 1. Architectural Style

**Modular Monolith with Clean Architecture boundaries.**

- All modules are self-contained Python packages
- Core business logic is independent of GUI and DB frameworks
- Dependency rule: outer layers (UI, API) depend on inner layers (engines, domain)
- Each module has an `__init__.py` that exposes a clean public API

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────────────┐    ┌──────────────────────────┐     │
│  │ Customer Interface  │    │ Admin Dashboard (React)  │     │
│  │  (PySide6)          │    │  (Web, future)           │     │
│  └─────────────────────┘    └──────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐   │
│  │ API      │ │ Payment  │ │ QR       │ │ Auth (core)    │   │
│  │ (FastAPI)│ │ Engine   │ │ Engine   │ │                │   │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    DOMAIN / CORE LAYER                       │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────────┐    │
│  │ Photo Session│ │ Camera       │ │ Image Processing  │    │
│  │ Engine       │ │ Engine       │ │ Engine            │    │
│  └──────────────┘ └──────────────┘ └───────────────────┘    │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────────┐    │
│  │ Frame        │ │ Layout       │ │ Storage           │    │
│  │ Engine       │ │ Engine       │ │ Engine            │    │
│  └──────────────┘ └──────────────┘ └───────────────────┘    │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────────┐    │
│  │ Printing     │ │ Database     │ │ Logging           │    │
│  │ Engine       │ │ Abstraction  │ │                   │    │
│  └──────────────┘ └──────────────┘ └───────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Module Dependency Graph

```
app_core
  ├── database
  │     (SQLAlchemy, async SQLite)
  ├── storage_engine
  │     (File I/O, atomic save, backup)
  ├── logging
  │     (Structured logging)
  ├── hardware_abstraction
  │     (Camera & printer abstract interfaces)
  │     ├── camera_engine
  │     │     (Camera detection, capture, profiles)
  │     ├── printing_engine
  │     │     (Printer detection, print queue)
  │     └── qr_engine
  │           (QR code generation)
  ├── photo_session_engine
  │     (Session management, state machine, recovery)
  ├── image_processing_engine
  │     (OpenCV + Pillow pipeline)
  ├── frame_engine
  │     (Frame management, templates)
  ├── layout_engine
  │     (Photo layout composition)
  ├── payment_engine
  │     (Payment method abstraction)
  └── api
        (FastAPI REST + WebSocket, optional in Phase 1)
```

**FX:** `customer_interface` → `app_core` → all engines
**CX:** `admin_dashboard` → `api` → `app_core` → engines

---

## 4. Component Design

### 4.1 app_core

Entry point and shared services.

**Files:**
- `config.py` — Configuration loader (JSON/TOML), environment variables
- `logging_config.py` — Structured logging setup
- `error_handler.py` — Central exception handling
- `utils.py` — Common utilities (atomic file save, path resolution)

**Responsibilities:** Application lifecycle, configuration, logging, cross-cutting concerns.

### 4.2 database

DB access layer.

**Files:**
- `database.py` — Async SQLite engine, session factory
- `models.py` — SQLAlchemy ORM models (60+ tables)
- `migrations.py` — Alembic-style migration management
- `schema.sql` — Initial schema

**Responsibilities:** Data persistence, schema migration, query abstractions.

**Future:** PostgreSQL adapter without application changes (via DB URL config).

### 4.3 storage_engine

File storage management.

**Files:**
- `storage_manager.py` — Path resolution, session photo directory management
- `backup_manager.py` — Automatic backup on shutdown, restore
- `file_utils.py` — Image file operations

**Responsibilities:** Session photo storage, atomic writes, backup/restore.

### 4.4 logging

Structured logging.

```
logs/
└── xinoobie_2026-11-17.log
```

**Responsibilities:** Capture application events, errors, camera events.

### 4.5 hardware_abstraction

**`camera_abstractions.py`** — Abstract base class for cameras.
**`printer_abstractions.py`** — Abstract base class for printers.

All hardware engines implement these interfaces, allowing vendor-specific implementations.

### 4.6 camera_engine

**`camera_manager.py`** — Camera lifecycle, device enumeration, reconnection.
**`sony_camera.py`** — Sony ZV-E10 implementation.
**`mock_camera.py`** — Mock for testing.

**Responsibilities:** Detection, live preview, capture triggering, settings management, error recovery.

### 4.7 photo_session_engine

**`session.py`** — Session state machine.
**`session_manager.py` — Global session coordination.**

**Responsibilities:** Session lifecycle, state persistence/recovery, photo capture scheduling, session history.

### 4.8 image_processing_engine

**`processor.py`** — Core pipeline (load → process → save).
**`editor.py`** — Non-destructive editing stack.
**`filters.py`** — Filter registry.
**`layout_composer.py`** — Strip/layout composition.

**Responsibilities:** Photo capture processing, edit application, layout composition.

### 4.9 frame_engine

**`frame_manager.py` — Frame CRUD, categorization.**
**`frame_template.py` — Default frame templates.**

**Responsibilities:** Frame management, template loading.

### 4.10 layout_engine

**`layout_manager.py` — Layout definitions, composition.**
**`design_templates.py` — Default layouts (2x6 strip, 4x6, 1:1, custom).**

**Responsibilities:** Layout orchestration, photo placement.

### 4.11 printing_engine

**`printer_manager.py` — Printer detection, status.**
**`print_queue.py` — Print queue with retry.**
**`print_job.py` — Single print job.**

**Responsibilities:** Print pipeline, error handling, history.

### 4.12 payment_engine

**`payment_processor.py`** — Payment method abstraction.
**`transaction.py`** — Transaction record.

**Responsibilities:** Payment processing, status tracking.

### 4.13 qr_engine

**`qr_generator.py`** — QR generation for digital delivery.

**Responsibilities:** QR code generation, linking.

### 4.14 api

**`main.py`** — FastAPI app initialization.
**`routes/`** — API route modules.
**`websocket.py`** — WebSocket endpoints.

**Responsibilities:** Admin-facing API for session management, hardware status.

### 4.15 customer_interface (Phase 1 shell)

**`main_window.py`** — Main QApplication, window setup, kiosk mode.
**`screens/__init__.py`** — Screen registry.
**`screens/welcome_screen.py`** — Welcome screen shell.
**`screens/base_screen.py`** — Common screen base class.

**Responsibilities:** Customer-facing touchscreen UI shell.

---

## 5. Data Flow

### Session Flow
```
User selects package → Build session → Camera prepares → 
  Countdown → Burst capture → Photo selection → 
  Edit (optional) → Payment → Print &
  QR generation → Thank you → Save session → 
  Log (analytics)
```

### Hardware Flow
```
App starts → Detect hardware → Save config → 
  On enable: Test connection, create profile → 
  Each session: Use profile → 
  On disconnect: Auto-reconnect attempt 
  → Log error → Notify user
```

### Storage Flow
```
Capture → Save temp (RAM/temp dir) → Process → 
  Atomic save to session dir → Update DB → 
  Return path to UI → 
  Optional: Delete originals after retention policy
```

### Print Flow
```
User prints → Create print job → Send to printer → 
  Success → Log → Update DB → 
  Fail → Retry (3x) → Log → Notify
```

---

## 6. Key Design Decisions

| Decision | Rationale |
|---|---|
| Modular monolith, not microservices | Single executable, easier distribution, lower complexity |
| SQLite first | Zero-config for local version |
| Abstract hardware | Enables multi-vendor and future multi-booth |
| Offline-first | Photobooth is often in areas with no/internet |
| Non-destructive editing | Re-edit sessions later, customer satisfaction |
| Atomic file saves | Crash-resilient photos |
| Configuration in JSON → YAML/TOML | Easy to edit, programmatic structure |
| FastAPI + WebSocket | Admin dashboard future-ready, session push events |

---

## 7. Configuration Structure

```json
{
  "app": {
    "name": "Xinoobie Photobooth",
    "version": "0.1.0",
    "language": "id",
    "kiosk_mode": false,
    "auto_start": false,
    "data_dir": "%LOCALAPPDATA%\\XinoobiePhotobooth"
  },
  "camera": {
    "default_profile": "default",
    "profiles": {
      "default": {
        "device_index": 0,
        "width": 1920,
        "height": 1080,
        "fps": 30
      }
    },
    "sony_zv_e10": {
      "sdk_path": "",
      "device_mac": ""
    }
  },
  "printer": {
    "default_profile": "default",
    "profiles": {}
  },
  "session": {
    "default_photo_count": 2,
    "default_retake_limit": 3,
    "default_countdown": [3, 3, 3],
    "retention_days": 90
  },
  "payment": {
    "manual_qris_enabled": true,
    "gateways": {
      "midtrans": { "enabled": false, "api_key": "" }
    }
  }
}
```

---

## 8. UI Architecture

### 8.1 Customer Interface

- Single fullscreen QMainWindow (kiosk-like)
- QStackedWidget for screen navigation
- Screens inherit `BaseScreen` with common transitions
- Theme: Dark minimal, Korean-inspired design

**Monitored screens (19 total):**
1. `WelcomeScreen`
2. `StartSessionScreen`
3. `LanguageScreen`
4. `PackageScreen`
5. `LayoutScreen`
6. `FrameScreen`
7. `FilterScreen`
8. `InstructionsScreen`
9. `LivePreviewScreen`
10. `CountdownScreen`
11. `CaptureScreen`
12. `PhotoSelectionScreen`
13. `RetakeScreen`
14. `PhotoEditorScreen`
15. `FinalPreviewScreen`
16. `PaymentScreen`
17. `PrintingScreen`
18. `QRCodeDownloadScreen`
19. `ThankYouScreen`

### 8.2 Admin Dashboard

React + TypeScript + Vite frontend.
Backend: FastAPI.

**Pages:**
- Overview dashboard
- Transaction management
- Session management
- Package management
- Template (frame, filter, layout) management
- Hardware settings
- Storage management
- Analytics

---

## 9. Testing Architecture

- **Unit tests** — `pytest` with `responses` for HTTP, `freezegun` for time
- **Integration tests** — Camera manager with mock camera
- **UI tests** — QApplication with mocked QWidgets (headless)
- **Coverage target** — 70% on core engines
- **Mocking** — `mock_camera`, `mock_printer` for all hardware

---

## 10. Roadmap Summary

| Phase | Focus | Deliverables |
|---|---|---|
| 1 | Foundation | Project structure, DB, main app, customer UI shell, admin login |
| 2 | Camera | Detection, live preview, capture, profiles |
| 3 | Photo Engine | Preview, retake, filters, layout, frames, final render |
| 4 | Printing | Detection, print queue, print preview |
| 5 | Digital Delivery | QR, gallery, download |
| 6 | Business System | Packages, transactions, payments, reports |
| 7 | Commercial Release | Installer, backup, recovery, hardware compatibility |

Full details in `docs/ROADMAP.md`.
