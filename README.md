# Xinoobie Photobooth

## Overview

**Xinoobie Photobooth** — Professional desktop photobooth software for:
- Korean-style photobooth events
- Self photo studio
- Event photobooth
- Professional photography studio

Offline-first desktop application with modular architecture. Designed for future multi-booth and multi-branch deployment.

**Product Lead**: Muhammad Nur Wahid (xinoobie)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                 CUSTOMER INTERFACE                    │
│         Touchscreen fullscreen (PySide6)              │
│  Welcome → Start → Language → Package → ... → Thank You │
└─────────────────────────────────────────────────────┘
                              ▲
                              │ Qt Signals / Local events
┌─────────────────────────────────────────────────────┐
│                 APP CORE                            │
│  Config · Logging · Utils · Error Handling          │
└─────────────────────────────────────────────────────┘
        │          │          │          │          │
┌───────┴──┐ ┌─────┴────┐ ┌───┴──────┐ ┌────┴──────┐ ┌─────┴──────┐
│ Camera   │ │ Photo     │ │ Frame    │ │ Print     │ │ Payment    │
│ Engine   │ │ Session   │ │ Engine   │ │ Engine    │ │ Engine     │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └────────────┘
        │          │          │          │          │
        └──────────┴──────────┴──────────┴──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌───────▼──────┐  ┌──────▼──────┐
│  Database    │  │   API (API)  │  │  Hardware    │
│  (SQLite/PSQL)│  │  REST + WS   │  │  Abstraction │
└──────────────┘  └──────────────┘  └─────────────┘
```

---

## Directory Structure

```
D:\PERCODINGAN AI\Xinoobie-Photobooth
├── README.md
├── requirements.txt
├── setup.py
├── docs/
│   ├── SRS.md
│   ├── ARCHITECTURE.md
│   ├── UI_DESIGN.md
│   └── ROADMAP.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── app_core/
│   ├── customer_interface/
│   ├── admin_dashboard/
│   ├── camera_engine/
│   ├── photo_session_engine/
│   ├── image_processing_engine/
│   ├── frame_engine/
│   ├── layout_engine/
│   ├── printing_engine/
│   ├── payment_engine/
│   ├── qr_engine/
│   ├── storage_engine/
│   ├── database/
│   ├── api/
│   ├── hardware_abstraction/
│   ├── logging/
│   └── testing/
├── tests/
├── scripts/
└── assets/
    ├── frames/
    ├── filters/
    ├── layouts/
    └── photos/
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Desktop GUI | PySide6 (Qt 6) |
| Image Processing | OpenCV, Pillow, NumPy |
| Camera (Primary) | Sony ZV-E10 via Sony Camera Remote SDK (Phase 2) |
| Camera (Alternative) | OpenCV USB webcam (fallback) |
| Database | SQLite (local) → PostgreSQL (future) |
| Backend API | FastAPI + WebSocket |
| QR Code | qrcode library |
| Installer | PyInstaller → NSIS Windows installer |
| Portable Mode | Created via build script |

---

## Development Phases

- **Phase 1 — Foundation** (this document's scope):
  Project structure, database, main application, customer interface shell, admin login.
- **Phase 2 — Camera**
- **Phase 3 — Photo Engine**
- **Phase 4 — Printing**
- **Phase 5 — Digital Delivery**
- **Phase 6 — Business System**
- **Phase 7 — Commercial Release**

---

## License & Copyright

Copyright © 2026 Muhammad Nur Wahid. All rights reserved.
