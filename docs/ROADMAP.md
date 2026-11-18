# Development Roadmap — Xinoobie Photobooth

**Version:** 1.0
**Date:** 2026-11-17

---

## Overview

Phased delivery from foundation to commercial release.

---

## Visual Roadmap Summary

```
PHASE 1 — FOUNDATION      PHASE 2 — CAMERA      PHASE 3 — PHOTO ENGINE
[PROJECT STRUCTURE]      [CAMERA DETECTION]    [PREVIEW + RETAKE]
  • Folder layout        [LIVE PREVIEW]        [FILTER FEATURES]
  • Database (SQLite)    [CONFIG PROFILES]     [LAYOUT COMPOSER]
  • Main app skeleton    [AUTO CAPTURE]        [FRAME MANAGEMENT]
  • Admin login          [SESSION MANAGEMENT]  [FINAL RENDERING]
  • Customer UI shell    [ERROR RECOVERY]
  • Logging system
  • Utils

PHASE 4 — PRINTING        PHASE 5 — DIGITAL     PHASE 6 — BUSINESS
[SYSTEM]                   DELIVERY              [BUSINESS]
  • Printer detection    • QR code generation   • Package CRUD
  • Print queue          • Digital gallery      • Transactions
  • Print preview        • Photo download       • Payment verification
  • Print history        • Cloud upload (optional) • Reports
  • Print error handling • Offline queue         • Analytics

PHASE 7 — COMMERCIAL      PHASE 7 — COMMERCIAL  PHASE 7 — COMMERCIAL
 [RELEASE]                [RELEASE]             [RELEASE]
   • Installer (NSIS)     • Auto-update          • Security audit
   • Backup/restore       • Performance           • Hardware badge
   • Multi-boot support   • Load testing          • Support docs
   • Multi-branch config  • Crash recovery        • Packaging
```

---

## Detailed Phase Plan

---

### PHASE 1 — FOUNDATION
**Goal:** A working skeleton that compiles, shows a customer screen, and has a persistent database.

#### 1.1 Deliverable Files
| File | Description |
|---|---|
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/requirements.txt` | Dependencies |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/README.md` | Project overview |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/docs/SRS.md` | Software requirements spec |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/docs/ARCHITECTURE.md` | System architecture |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/docs/UI_DESIGN.md` | UI/UX design system |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/docs/ROADMAP.md` | Phase roadmap |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/__init__.py` | Package init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/main.py` | App entry point |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/app_core/__init__.py` | App core init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/app_core/config.py` | Configuration loader |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/app_core/logging_config.py` | Logging setup |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/app_core/error_handler.py` | Central error handler |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/app_core/utils.py` | Utility functions |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/logging/__init__.py` | Logging init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/logging/logger.py` | Logger factory |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/database/__init__.py` | Database init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/database/database.py` | Async SQLite engine |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/database/models.py` | ORM models |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/database/schema.sql` | SQL schema |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/database/migrations.py` | Migration manager |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/__init__.py` | Customer UI init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/main_window.py` | Main window (kiosk) |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/base_screen.py` | Base screen class |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/__init__.py` | Screens registry |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/welcome_screen.py` | Welcome screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/language_screen.py` | Language screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/start_session_screen.py` | Start session screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/package_screen.py` | Package selection screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/layout_screen.py` | Layout selection screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/frame_screen.py` | Frame selection screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/filter_screen.py` | Filter selection screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/instructions_screen.py` | Instructions screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/live_preview_screen.py` | Live preview screen (shell) |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/countdown_screen.py` | Countdown screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/capture_screen.py` | Capture screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/photo_selection_screen.py` | Photo selection screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/retake_screen.py` | Retake screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/photo_editor_screen.py` | Photo editor screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/final_preview_screen.py` | Final preview screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/payment_screen.py` | Payment screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/printing_screen.py` | Printing screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/qr_download_screen.py` | QR download screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/src/customer_interface/screens/thank_you_screen.py` | Thank you screen |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/tests/__init__.py` | Test init |
| `D:/PERCODINGAN AI/Xinoobie-Photobooth/tests/conftest.py` | Test fixtures |

#### 1.2 Functional Summary
- Application launches with PySide6 main window
- Fullscreen kiosk mode
- 19 screens implemented as stacked widgets
- Welcome screen shows language picker
- Language screen switches language (en/id)
- Database schema initialized on first run
- Admin login form (UI placeholder, auth not yet implemented)
- Configuration stored in `%LOCALAPPDATA%\XinoobiePhotobooth`
- Logging writing to `logs/xinoobie_YYYYMMDD.log`

#### 1.3 Build & Run Commands
```bat
# Create venv & install
cd D:\PERCODINGAN AI\Xinoobie-Photobooth
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run
python src/main.py
```

#### 1.4 Test Command
```bat
venv\Scripts\python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

---

### PHASE 2 — CAMERA
**Goal:** Camera detection, live preview, capture, configuration.

#### 2.1 Deliverable Files
Add to `src/`:
- `camera_engine/__init__.py`
- `camera_engine/camera_manager.py`
- `camera_engine/camera_abstractions.py`
- `camera_engine/sony_camera.py`
- `camera_engine/mock_camera.py`
- `camera_engine/profiles.py`

#### 2.2 Functional Summary
- Camera enumeration (webcam + network)
- Live preview via QVideoWidget
- Auto-focus, manual focus (where supported)
- ISO, shutter speed, aperture control (conditional)
- White balance, exposure compensation
- Camera configuration profiles (save/restore)
- Auto capture (burst)
- Session state machine
- Camera error recovery (reconnect, fallback to mock)

---

### PHASE 3 — PHOTO ENGINE
**Goal:** Complete photo capture + editing + layout composition pipeline.

#### 3.1 Deliverable Files
Add to `src/`:
- `image_processing_engine/__init__.py`
- `image_processing_engine/processor.py`
- `image_processing_engine/editor.py`
- `image_processing_engine/filters.py`
- `image_processing_engine/layout_composer.py`
- `frame_engine/__init__.py`
- `frame_engine/frame_manager.py`
- `frame_engine/frame_templates.py`
- `layout_engine/__init__.py`
- `layout_engine/layout_manager.py`

#### 3.2 Functional Summary
- Live preview scaling
- Photo capture flow (burst, single)
- Photo selection (2+ for strip)
- Non-destructive editing stack (crop, rotate, brightness/contrast/saturation, temperature, filters)
- Custom filter support
- Overlay: stickers, text, logo, frame
- Layout composition (2x6 strip, 4x6, 4x4, 1:1, custom)
- Frame management (upload, delete, edit, preview, categorize, price, enable/disable, default)
- Template system (no code change)

---

### PHASE 4 — PRINTING
**Goal:** Automatic printing with error handling.

#### 4.1 Deliverable Files
Add to `src/`:
- `printing_engine/__init__.py`
- `printing_engine/printer_manager.py`
- `printing_engine/print_queue.py`
- `printing_engine/print_job.py`

#### 4.2 Functional Summary
- Printer detection (USB, network)
- Print preview
- Print queue with retry
- Print settings (paper size, resolution)
- Print history
- Print error logging

---

### PHASE 5 — DIGITAL DELIVERY
**Goal:** QR codes + digital gallery + downloads.

#### 5.1 Deliverable Files
Add to `src/`:
- `qr_engine/__init__.py`
- `qr_engine/qr_generator.py`
- `storage_engine/__init__.py`
- `storage_engine/storage_manager.py`
- `storage_engine/backup_manager.py`

#### 5.2 Functional Summary
- Automatic QR generation
- Digital gallery (webpage + photos)
- Download original + strip
- Share link with password
- Expiring download link
- Cloud upload (optional)
- Offline queue

---

### PHASE 6 — BUSINESS SYSTEM
**Goal:** Complete business features.

#### 6.1 Deliverable Files
Add to `src/`:
- `payment_engine/__init__.py`
- `payment_engine/payment_processor.py`
- `payment_engine/transaction.py`
- `api/__init__.py`
- `api/main.py`
- `api/routes/__init__.py`
- `api/routes/sessions.py`
- `api/routes/packages.py`
- `api/routes/transactions.py`
- `api/routes/printers.py`
- `api/routes/cameras.py`
- `api/websocket.py`

#### 6.2 Functional Summary
- Package CRUD (create, edit, delete, price, photo count, retake limit)
- Transaction history & management
- Payment: cash, QRIS manual, gateway, e-wallet
- Payment verification
- Voucher & discount
- Reports (daily, monthly)
- Analytics

---

### PHASE 7 — COMMERCIAL RELEASE
**Goal:** Production-ready installation.

#### 7.1 Deliverable Files
Add to `scripts/`:
- `build_app.py` — PyInstaller one-file/build
- `build_installer.py` — NSIS wizard
- `create_portable.bat` — Portable build script
- `generate_license.py` — License file generation

#### 7.2 Functional Summary
- Windows installer (NSIS)
- Portable mode
- Auto-update architecture
- Automated backup
- Recovery system
- Hardware compatibility testing
- Performance optimization
- Security testing

---

## Design Standards (All Phases)

### Code Style
- PEP 8 compliant
- Type hints on all public functions
- Docstrings on all modules
- 4-space indentation

### Commit Conventions
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code restructuring
- `test:` test addition/update

### Branching
- `main` — stable
- `develop` — integration
- Feature branches: `feat/phase2-camera`, `feat/phase3-editor`

---

## Implementation Notes

### Dependency Notes
- PySide6 only on Windows (Phase 1-7)
- macOS/Linux: note in README, separate builds

### Known Limitations (Phase 1)
- No camera integration yet (UI has placeholder)
- No real payment processing
- No printer integration
- No QR generation in Phase 1

### Next Steps After One Phase
- Document what was built
- Run tests
- Report code coverage
- Start next phase
