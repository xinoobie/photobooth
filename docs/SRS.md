# Software Requirements Specification (SRS)
## Xinoobie Photobooth

**Version:** 1.0
**Date:** 2026-11-17
**Author:** Muhammad Nur Wahid

---

## 1. Introduction

### 1.1 Purpose

This document specifies the complete functional and non-functional requirements for Xinoobie Photobooth — a professional desktop photobooth application for Korean-style photobooths, self photo studios, event photobooths, and professional photo studios.

### 1.2 Scope

The system is a standalone desktop application that:
- Operates fully offline for main features
- Captures photos via camera
- Provides photo editing and layout composition
- Prints photos via connected printer
- Generates QR code for digital delivery
- Stores data locally in SQLite (migratable to PostgreSQL)
- Provides an admin web dashboard for management

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|---|---|
| Booth | Physical photobooth session space |
| Branch | Deployment location/server group |
| Session | Single customer session with the photobooth |
| Sheet/Stripe | Group of 2 or 4 photos arranged in a layout |
| Frame | Photo border/decoration (PNG with transparency) |
| Log | Structured record for debugging and error tracking |
| Admin | Authorized user managing system settings via dashboard |

---

## 2. Overall Description

### 2.1 Product Perspective

Xinoobie Photobooth is a modular desktop application with the following major components:
1. **Customer Interface** (PySide6) — Touchscreen fullscreen UI for customers
2. **Admin Dashboard** (React + TypeScript) — Web-based management console
3. **Backend API** (FastAPI) — REST + WebSocket communication layer
4. **Core Engines** — Camera, Photo Session, Image Processing, Frame, Layout, Printing, Payment, QR, Storage
5. **Database** — SQLite (local) with migration path to PostgreSQL

### 2.2 Operating Environment

- **OS**: Windows 10/11 (primary), macOS (future), Linux (experimental)
- **Runtime**: Python 3.9+ (desktop), Node 18+ (admin dashboard — future)
- **Display**: 1080p or higher (touchscreen recommended)
- **Camera**: USB webcam (fallback) or Sony ZV-E10 (primary target)
- **Printer**: Dye-sublimation or photo thermal printer (USB/WiFi)

### 2.3 Assumptions and Dependencies

- Customer interface must operate fully offline (no internet required)
- Camera is connected via USB or network
- Printer is connected via USB or network
- Admin dashboard requires network access to the backend API
- Sony ZV-E10 support is primary (Phase 2), with fallback to standard webcam

### 2.4 UI Usage

The customer interface is designed for use by customers without operator assistance:
- All screens are touch-optimized
- Navigation uses large, clearly labeled buttons/links
- Language selection is available on the welcome screen
- The session flow is guided step-by-step
- Error messages are displayed in a friendly, understandable way

---

## 3. Functional Requirements

### 3.1 Welcome Screen
- Displays application logo/title
- "Start Session" button (prominent)
- Multi-language selector (Indonesian, English)
- Auto-start option (Kiosk mode)

### 3.2 Start Session
- New session ID generation
- Session timer initialization
- Session state: `active`, `paused`, `complete`, `cancelled`, `recovered`

### 3.3 Language Selection
- Choose between Indonesian and English
- Applies throughout the session

### 3.4 Package Selection
- Display available packages with photo count, price, retake limit
- Select one package

### 3.5 Photo Layout Selection
- 2x6 inch strip (2 photos)
- 4x6 inch (1 photo)
- 4x4 inch (1 photo)
- 1:1 digital (1 photo)
- Custom canvas size

### 3.6 Frame Selection
- Select one frame from available
- Preview frame applied to test photo

### 3.7 Filter Selection
- Brightness
- Contrast
- Saturation
- Color Temperature
- Black & White
- Vintage
- Film
- Warm
- Custom (user-defined)

### 3.8 Photo Instructions
- Display camera instructions (position, gaze direction)
- Optional text instructions

### 3.9 Live Camera Preview
- Shows live camera feed
- Resize proportional to window
- Overlay information (session ID, countdown)

### 3.10 Countdown Screen
- Configurable countdown (default 3-3-3 or 5-5-5)
- "Get Ready" screen
- "Smile" screen
- Count is visual and audio

### 3.11 Photo Capture Screen
- Automatic capture per configured interval
- Individual photo preview immediately after capture
- Retake option (within limit)
- Burst capture option (multiple frames for 1 photo)

### 3.12 Photo Selection
- Select final photo from taken photos
- Multi-select for strip/layout

### 3.13 Retake Screen
- Select photo for retake
- Re-capture
- Maximum retake limit enforcement

### 3.14 Photo Editing
- Crop
- Rotate
- Brightness, Contrast, Saturation
- Color Temperature
- B/W, Vintage, Film, Warm filters
- Custom filter
- Sticker overlay
- Text overlay
- Logo overlay
- Frame overlay
- Non-destructive edit stack

### 3.15 Final Preview
- Full-size preview with all edits
- Layout preview with all selected elements

### 3.16 Payment Screen
- Package price display
- Payment method selection (Cash, Manual QRIS, E-wallet, Payment Gateway)
- Amount input (if manual)
- Payment verification
- Transaction history

### 3.17 Printing Screen
- Print preview with all frames/layouts
- Select quantity
- Select paper size
- Start printing
- Print queue management
- Print error handling

### 3.18 QR Code Download Screen
- QR code display
- Download gallery link
- Step-by-step guide

### 3.19 Thank You Screen
- Session summary
- Session ID
- Gallery link (if generated)
- "Start New Session" button

### 3.20 Session Recovery
- On application restart, list incomplete/abnormal sessions
- Recovery options: resume, abandon
- Session recovery log

### 3.21 Session History
- List of past sessions with date/time
- Session detail: photos taken, payment, prints

---

## 4. Non-Functional Requirements

### 4.1 Usability
- Touchscreen-friendly: minimum 44x44 px touch targets
- Clear typography with high contrast
- Smooth transitions between screens (300ms ease-in-out)
- Consistent spacing (8px grid system)

### 4.2 Performance
- Live preview: 30 fps minimum when available
- Image processing under 2 seconds per operation
- Session capture: < 3 seconds per photo
- Startup time: < 5 seconds (cold start)
- Memory usage < 2 GB during normal operation

### 4.3 Reliability
- Graceful handling of camera disconnection
- Graceful handling of printer disconnection
- Photo files protected during application crash (atomic save + backup)
- Session history preserves state across restarts

### 4.4 Portability
- Runs on Windows 10/11
- Portable mode: no installation required, single exe or folder
- Config stored in: `%LOCALAPPDATA%\XinoobiePhotobooth`

### 4.5 Security
- No plaintext passwords
- PIN-based admin access (6-digit)
- Session photos encrypted at rest (optional)
- Admin API: token-based authentication
- Role-Based Access Control (RBAC)

### 4.6 Maintainability
- Modular architecture (15 top-level modules)
- No single file contains all functionality
- Code documented with docstrings
- Test coverage target: 70%+ per module

---

## 5. Hardware Integration Requirements

### 5.1 Camera (Sony ZV-E10)
- Primary target hardware
- Support via Sony Camera Remote SDK
- Fallback: USB webcam via OpenCV
- Auto-detection and reconnection
- Manual focus, ISO, shutter speed, aperture where supported (conditional)
- Camera configuration profiles save/restore

### 5.2 Printer
- Dye-sublimation printer (common in photobooths)
- Photo thermal printer (alternative)
- Auto-detection via USB/WiFi
- Print queue with retry
- Print error logging

### 5.3 Storage
- Local USB or internal storage
- Secondary storage (NAS) for backup
- Automatic cleanup of old sessions (configurable retention)

---

## 6. Database Requirements

### 6.1 Storage
- SQLite (local version)
- PostgreSQL (future cloud/multi-branch)

### 6.2 Core Tables
See `database/schema.sql` for full DDL.

### 6.3 Indexing Strategy
- `sessions(user_id, created_at, status)` — Date range queries
- `transactions(user_id, created_at, status)` — Revenue reports
- `session_photos(session_id, created_at)` — Photo lookup
- `frames(is_enabled, category)` — Frame library queries
- `packages(price)` — Filtering and sorting

---

## 7. API Requirements

### 7.1 Base URL
- `http://localhost:8000` (local)
- `https://api.xinoobie.example` (future cloud)

### 7.2 Endpoints (Phase 6+)
- `POST /auth/login` — Admin authentication
- `GET /sessions` — Session list
- `GET /sessions/{id}` — Session detail
- `GET /sessions/{id}/photos` — All photos in session
- `GET /packages` — Package list
- `POST /payments/verify` — Payment verification
- `GET /printer/status` — Printer status
- `GET /camera/status` — Camera status

### 7.3 WebSocket Events
- `session.start` — New session initiated
- `session.capture` — New photo captured
- `session.complete` — Session finished
- `print.job.started` — Print job started
- `print.job.completed` — Print job completed

---

## 8. Risk Register

### 7.1 Sony ZV-E10 Integration
| Risk | Impact | Mitigation |
|---|---|---|
| SDK requires macOS | Medium | Provide webcam fallback + future support |
| SDK protocol undocumented | High | Evaluate, document in Phase 2 |
| Camera settings unavailable | Medium | Graceful degrade, log notification |
| Camera firmware update releases | Low | Keep SDK version flexible |

### 7.2 Printer Integration
| Risk | Impact | Mitigation |
|---|---|---|
| Proprietary driver | High | Provide test plan in Phase 4 |
| Paper tray sensor | Medium | Fallback manual check |
| Network printer conflict | Low | Use local detection first |

---

## 9. Acceptance Criteria

- [ ] Customer can run a complete session end-to-end without operator
- [ ] Application survives camera disconnection and recovers
- [ ] Photos are saved and displayed after session
- [ ] Admin can see session in dashboard
- [ ] QR code is generated and downloadable
- [ ] App can print via detected printer
- [ ] Database migration path to PostgreSQL coded (not fully implemented)
- [ ] Unit tests cover critical modules (70%+ target)
