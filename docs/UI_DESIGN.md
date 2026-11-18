# User Interface & UX Design — Xinoobie Photobooth

**Version:** 1.0
**Date:** 2026-11-17

---

## 1. Design Philosophy

### Core Principles
- **Premium & Minimalist** — Clean surfaces, generous white space, subtle shadows
- **Customer-Facing** — The customer should not see dashboard elements
- **Touchscreen Optimized** — Large tap targets, no hover-dependent features
- **Korean Studio Aesthetic** — Balanced, precise, use of negative space
- **Consistent Visual Language** — Same color, typography, spacing across all screens

### Visual Identity
| Token | Value | Usage |
|---|---|---|
| Primary | `#3B82F6` (blue) | CTAs, active states |
| Primary Dark | `#1D4ED8` | Hover states |
| Accent | `#F59E0B` (amber) | Promotions, highlights |
| Success | `#10B981` (green) | Print/delivery success |
| Warning | `#F59E0B` (amber) | Reminder states |
| Error | `#EF4444` (red) | Errors, deletion |
| Background | `#0F172A` (slate-900) | Main surfaces |
| Surface | `#1E293B` (slate-800) | Card/elevated surfaces |
| Text | `#F8FAFC` (slate-50) | Primary text |
| Secondary Text | `#94A3B8` (slate-400) | Secondary/comments |
| Border | `#334155` (slate-700) | Dividers, inputs |

---

## 2. Typography

### Font Stack
```
- Headings: "Poppins" (from Google Fonts, fallback: "Segoe UI", sans-serif)
- Body: "Inter" (fallback: "Segoe UI", sans-serif)
- Numbers/captions: "JetBrains Mono" (fallback: monospace)
```

### Scale
| Size | Scale | Usage |
|---|---|---|
| Display | 48px | Welcome screen title |
| H1 | 36px | Section headers |
| H2 | 28px | Screen titles |
| H3 | 22px | Card titles |
| Body | 16px | Body text |
| Small | 14px | Captions, metadata |
| Tiny | 12px | Instruction text |

---

## 3. Color Schema (Dark Theme)

### Background Hierarchy
```
Surface 3 (deepest): #0B1220 — App background
Surface 2: #0F172A — Panel background
Surface 1: #1E293B — Card background
Surface 0: #334155 — Hover/reversed
```

### Accent Usage
- Primary buttons: filled `#3B82F6`
- Secondary buttons: border only, transparent fill
- Input focus: blue ring on border

### Status Colors
- Success: `#10B981` (green)
- Warning: `#F59E0B` (amber)
- Error: `#EF4444` (red)
- Info: `#3B82F6` (blue)

---

## 4. Spacing System

8px baseline grid:
```
1 → 4px, 2 → 8px, 3 → 12px, 4 → 16px, 5 → 24px, 6 → 32px, 8 → 48px
```

---

## 5. Customer Interface Screens — Design Specifications

### 5.1 Welcome Screen
```
Layout: Centered card with left-side logo/image
- Top: App logo (custom SVG, transparent PNG)
- Middle: Title "Xinoobie PHOTOBOOTH" (Display font, white)
- Subtitle: "Silakan pilih bahasa" (body, slate-400)
- Language chips: [🇮🇩 Indonesia] [🇺🇸 English]
- Bottom: "Mulai Sesi" primary button (full width)
- Background: subtle gradient (deep blue → slate)
- Touch targets: 72px min height
```

### 5.2 Start Session Screen
```
- Minimalistic: "Mulai Sesi" large centered button
- Subtle: "Siap? Tekan untuk mulai." (secondary text)
- No options, everything pre-selected
```

### 5.3 Language Screen
```
- Two large language cards side by side
- [🇮🇩 Indonesia] (primary selection, highlighted)
- [🇺🇸 English] (outline)
- Select one → proceed to package selection
```

### 5.4 Package Selection
```
- Horizontal scroll cards (2 per row on full screen)
- Card: Package name, photo count, price, retake limit, "Select" button
- Selected card: blue border + subtle scale (1.02)
- Empty state: "Tidak ada paket tersedia" (when database empty)
```

### 5.5 Layout Selection
```
- Grid of layout options (minimum 2x2 cards)
- Each card: thumbnail + label
- Selected: blue highlight, "Select" confirmation
- Thumbnails: placeholder image previews
```

### 5.6 Frame Selection
```
- Grid of frames (thumbnail images)
- Selected: blue ring
- "Preview" mode: click to see on a test image
- Bottom: "Lanjut" button
```

### 5.7 Filter Selection
```
- Vertical filter list with icons
- Each filter: name + description
- Selected: primary accent color
- "Apply" button at bottom
```

### 5.8 Instructions Screen
```
- Full-width image placeholder with icon
- "Posisi badan" + instruction text
- 2-3 bullet points
- "Lanjut" button
```

### 5.9 Live Preview Screen
```
- Fullscreen camera feed
- Top-left: Session badge (rounded, small)
- Bottom-left: "Siap" or camera status indicator
- Top-right: countdown indicator
- Bottom-right: "Terima Kasih" button
- If camera offline: red pulsing alert
```

### 5.10 Countdown Screen
```
- Fullscreen black background
- Big number: "3" → "2" → "1" (times 1 second each)
- "GET READY" sub-label
- Audio beep (optional, OS-dependent)
- Transition to capture via signal (no user interaction)
```

### 5.11 Capture Screen
```
- Shows captured photos in grid (2x2)
- "Retake" button (visible per photo)
- "Lanjut" button (if retake limit reached)
- Photo preview: full preview click to open editor
- Status: "Foto 1/2" (progress indicator)
```

### 5.12 Photo Selection
```
- Grid of all captured photos + selections
- Tap to select
- Selection state: checkmark overlay
- On 2x6 strip: 2 photos required, warning if less
- "Proses" button enables after all required selected
```

### 5.13 Retake Screen
```
- Shows last few photos
- Tap to select one
- "Retake Again" button
- "The Last" state: "No more retakes allowed" (if limit reached)
```

### 5.14 Photo Editor
```
- Left: original preview
- Right: edited preview
- Editable: crop, rotate, brightness slider, contrast slider, saturation slider
- Filter buttons (B/W, Vintage, Film, Warm)
- Overlays: sticker, text, logo
- "Apply" / "Revert" / "Kembali" buttons
```

### 5.15 Final Preview
```
- Shows full image with all overlays
- "Finish" button (primary, large)
- "Edit Again" button (secondary)
- Session summary: package, price, session ID
```

### 5.16 Payment Screen
```
- Package details card (name, price, payments)
- Payment method radio buttons:
  [💵 Tunai] [📱 QRIS Manual] [💳 E-wallet]
- Amount input field (when manual)
- "Pembayaran Selesai" button
- Success state: "Bayar diterima!" + transaction ID
- Failed state: retry button
```

### 5.17 Printing Screen
```
- "Print Preview" card: full layout preview
- Quantity selector: [-] 1 [+], default 1
- "Mulai Cetak" primary button
- "Print Queue" list
- Status: "Mencetak..." / "Selesai"
```

### 5.18 QR Code Download
```
- QR code displayed at center (large)
- "Klik untuk download" label
- Step-by-step guide: 1. Scan QR 2. Buka link 3. Download
- "Selesai" button
- QR regenerates on refresh
```

### 5.19 Thank You Screen
```
- "Terima Kasih!"
- Session summary (session ID, package, price, prints)
- Gallery link (if QR generated)
- "Mulai Sesi Baru" button
- "Lihat History" (next phase)
```

---

## 6. Admin Dashboard — Light Theme

### 6.1 Overall Layout
- Sidebar (240px, dark slate):
  - Logo "Xinoobie"
  - Navigation items with icons
  - "Logout" button
- Main content:
  - Header: title, date/time, user info
  - Content area: cards with tables/charts

### 6.2 Color Schema (Admin, Light)
```
Background: #F8FAFC (slate-50)
Surface: #FFFFFF
Primary: #3B82F6
Text: #0F172A (slate-900)
Secondary Text: #64748B (slate-500)
Border: #E2E8F0 (slate-200)
```

### 6.3 Navigation Menu
```
- Dashboard (Overview)
- Transaksi (Transactions)
- Sesi (Sessions)
- Paket (Packages)
- Template (Frames, Filters, Layouts)
- Perangkat (Hardware)
- Penyimpanan (Storage)
- Analitik (Analytics)
- Pengaturan (Settings)
```

---

## 7. Interaction Design

### 7.1 Transitions
- Screen change: fade (300ms, ease-in-out)
- Button press: scale 0.96 → 1.0 (400ms)
- Card hover: subtle lift (shadow increase, 150ms)
- Icon change: scale + opacity

### 7.2 Feedback
- Task in progress: loading spinner (16px, centered)
- Success: green check with brief flash
- Warning: amber alert banner (dismissible)
- Error: red alert banner with retry button
- Connection: indicator pulse (blue normal, red error)

### 7.3 Accessibility
- Minimum 44x44px touch targets
- Contrast ratio: text 4.5:1 minimum, 3:1 for large
- Focus visible: 2px blue ring
- Screen reader: accessible labels on all interactive elements

---

## 8. Screens Overview Table

| Screen ID | Customer View | Admin View | Transition |
|---|---|---|---|
| 01 | Welcome | N/A | → Language |
| 02 | Start Session | N/A | → Active Session |
| 03 | Language | N/A | → Package |
| 04 | Package | N/A | → Layout |
| 05 | Layout | N/A | → Frame |
| 06 | Frame | N/A | → Filter |
| 07 | Filter | N/A | → Instructions |
| 08 | Instructions | N/A | → Live Preview |
| 09 | Live Preview | Dashboard | → Countdown (auto) |
| 10 | Countdown | N/A | → Capture (auto) |
| 11 | Capture | Dashboard | → Selection |
| 12 | Photo Selection | Dashboard | → Editing (optional) |
| 13 | Retake | N/A | → Capture |
| 14 | Editor | N/A | → Final Preview |
| 15 | Final Preview | Dashboard | → Payment |
| 16 | Payment | Dashboard | → Printing |
| 17 | Printing | Dashboard | → QR |
| 18 | QR Download | N/A | → Thank You |
| 19 | Thank You | N/A | → Start (new session) |

---

## 9. Component Library

### Button Types
| Type | Appearance | Usage |
|---|---|---|
| Primary | Filled blue, white text | CTAs (proceed, start) |
| Secondary | Outline, transparent fill | Alternatives (edit, cancel) |
| Ghost | No border, text only | Destructive (delete), navigation |
| Icon | Circular icon button | Actions (camera, refresh) |

### Inputs
- Full-width text input (16px, 12px padding)
- Rounded corners: 8px
- Focus: blue border + ring

### Cards
- Border-radius: 12px
- Shadow: 0 4px 12px rgba(0,0,0,0.2)
- Padding: 16px
- Hover: 0 2px 8px rgba(0,0,0,0.3)

### Badges
- Small pill-shaped, rounded-full
- States: default, success, warning, error, neutral

---

## 10. Icons

| Icon | Usage |
|---|---|
| `camera` | Camera live preview |
| `camera-retake` | Retake action |
| `edit` | Edit photo |
| `print` | Print action |
| `qr-code` | QR screen |
| `check` | Selection, success |
| `arrow-right` | Navigation |
| `x` | Close, remove |
| `menu` | Hamburger menu |
| `settings` | Settings |
| `record` | Recording indicator |
| `hourglass` | Processing |
| `trash` | Delete |
| `plus` | Add |
| `minus` | Remove |
| `refresh` | Reconnect, retry |
