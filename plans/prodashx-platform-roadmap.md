# ProDashX Platform Roadmap

> Consolidated from 11 individual plans + active v3.11.1 session + JDM's Team Comms vision.
> Last updated: 2026-03-08

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| v3.6 @172 | Feb 15 | Discovery Kit shipped |
| v166 | Feb 15 | QUE-Medicare rename + AI3 template |
| v167 | Feb 15 | Banking product type formalized |
| v168 | Feb 15 | Medicare Rec backend engine |
| v3.9 @191 | Feb 24 | FK Migration (ghl_contact_id -> client_id) |
| v3.11 | Mar 3 | Latest deploy (current) |

---

## Stream 1: Bug Fixes & Stability (v3.11.1)

**Status: ACTIVE — in progress**
**Source plan:** `dynamic-sniffing-starlight.md`

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1.1 | **Dead screen on new tab** — "View Full Detail" uses iframe URL, not exec URL. `execUrl` template var needed. | P1 BLOCKER | Not started |
| 1.2 | **Client global search broken** — "ojeda" returns nothing in Clients mode. Variable scoping issue in `executeGlobalSearch`. | P2 | Not started |
| 1.3 | **MyRPI layout mismatch** — Doesn't match RIIMO's polished format. Port RIIMO `MyRPI.html` layout. | P3 | Not started |
| 1.4 | **Quick Intake custom fields** — "Add Field" should be select-then-input, not text prompt. Beneficiary needs structured sub-fields. | P4 | Not started |
| 1.5 | **Quick Intake screenshot paste** — Accept `image/png`, `image/jpeg` from clipboard. OCR via Gemini Vision. | P5 | Not started |
| 1.6 | **Team Comms UX** — See Stream 6 below (elevated to its own stream). | P6 | Redesigned |

**Ship as:** v3.11.1 (items 1.1-1.5)
**Files:** Code.gs, Index.html, Scripts.html, Styles.html

---

## Stream 2: Sales Pipeline Architecture

**Status: PARTIAL — Phase 1 shipped, Phases 2-7 outstanding**
**Source plans:** `rosy-shimmying-riddle.md`, `parsed-hugging-lerdorf.md`

### 2A: Stage-Based Navigation

The pipeline flows Orange > Blue > Yellow > Green. Sales Center nav mirrors that.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2A.1 | Generalize stage scanner (`scanStageOpportunities_(stageId)`) | Not started | ~30 lines in PRODASH_SALES_CENTERS.gs |
| 2A.2 | Blue Stage rename (Discovery Kit -> "Blue: Data Foundation") | Not started | Nav + all `dk-*` CSS/JS references |
| 2A.3 | Yellow Stage backend (`PRODASH_YELLOW_STAGE.gs`) | Not started | Scanner, dashboard, Case Central routing, QUE module status |
| 2A.4 | Yellow Stage UI — Dashboard + Internal Reports + QUE Modules + Case Central | Not started | Index.html sub-tabs + Scripts.html loaders |
| 2A.5 | Orange + Green stubs (`PRODASH_STAGE_STUBS.gs`) | Not started | ~150 lines, placeholder dashboards |
| 2A.6 | Nav refactor — 4 stage items replace old Sales Centers nav | Not started | QUE-Medicare moves under Yellow as sub-item |

**New files:** PRODASH_REPORT_ORDER.gs (~400), PRODASH_YELLOW_STAGE.gs (~350), PRODASH_STAGE_STUBS.gs (~150)
**~2,000 total new/changed lines across 7 files**

### 2B: Report Order System

Embedded within Blue Stage as a 5th sub-tab.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2B.1 | Report inventory constant (24 reports with metadata) | Not started | `REPORT_INVENTORY_` in PRODASH_REPORT_ORDER.gs |
| 2B.2 | Recommender engine — auto-suggest reports based on client accounts | Not started | Rules: annuity -> COMRA, BD/RIA -> Portfolio Pilot, etc. |
| 2B.3 | Report Order UI — card grid with select/deselect + source badges | Not started | Blue Stage sub-tab |
| 2B.4 | Routing sheet generator — "idiot-proof" instructions for ops team | Not started | Per-opp checklist: what to order from Gradient, what to upload |

### 2C: Casework Workbench (Yellow Stage)

Turns Yellow Stage from a read-only scoreboard into a real workbench.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2C.1 | `_CASE_TASKS` schema in RAPID_CORE + TABLE_ROUTING | Not started | 13-column task model |
| 2C.2 | `API_Task.gs` in RAPID_API — full CRUD + bulk create | Not started | ~200 lines, follows API_Opportunity.gs pattern |
| 2C.3 | `PRODASH_CASEWORK.gs` — scan, detail, readiness, notes, templates | Not started | ~350 lines, Layer 2/3 |
| 2C.4 | **My Cases** tab — stat cards, filter bar, case table sorted by staleness | Not started | Default Yellow Stage landing |
| 2C.5 | **Case Detail** tab — product line readiness strip + 4 sections (Tasks, Reports, QUE Modules, Notes) | Not started | Checkbox task completion, Smart Lookup assignment |
| 2C.6 | Task templates — auto-generate tasks per product line (medicare: 3, annuity: 4, life: 4, bdria: 4, general: 3) | Not started | `TASK_TEMPLATES_` constant + Apply Templates button |
| 2C.7 | Stage movement — [<- Blue] [Green ->] buttons on case detail header | Not started | |

**Dependency chain:** 2A.1 + 2A.3 must ship before 2C can be wired into Yellow Stage.

---

## Stream 3: Medicare Pipeline

**Status: PARTIAL — backend complete, UI integration outstanding**
**Source plans:** `floating-percolating-babbage.md`, `radiant-yawning-toucan.md`

| # | Item | Status | Notes |
|---|------|--------|-------|
| 3.1 | QUE-Medicare rename (68 refs, 13 files) | DONE (v166) | |
| 3.2 | AI3 template SETUP (Medicare merge field) | DONE (v166) | |
| 3.3 | Banking product type formalization | DONE (v167) | |
| 3.4 | Medicare Rec backend engine (`PRODASH_MEDICARE_REC.gs`) | DONE (v168) | Copies template, populates, exports PDF to ACF |
| 3.5 | **Medicare Rec UI — 7th QUE-Medicare tab** | Not started | Preset buttons (Full/Quick/Drug Focus), client search, plan selector, data summary chips, Generate button |
| 3.6 | **Comparison tab fix** — collects plan IDs but never calls `uiComparePlans()` | Not started | Wire comparison rendering + cache results in `medicareState.comparisonResults` |

**Files (3.5-3.6):** Index.html (~tab button + content div), Scripts.html (~rec state + functions + comparison render), Styles.html (2 CSS rules)
**Backend (3.4) already done — this is frontend-only work.**

---

## Stream 4: Client Output Engine (Case Central)

**Status: NOT STARTED**
**Source plan:** `humming-exploring-mochi.md` (consolidated 2026-03-08)

### 4A: Case Central Package Module

| # | Item | Status | Notes |
|---|------|--------|-------|
| 4A.1 | `PRODASH_CASE_CENTRAL.gs` — PDF package generator (~500 lines) | Not started | Follows PRODASH_MEDICARE_REC.gs pattern: copy template > populate merge fields > insert tables > clean sections > export PDF > save to ACF |
| 4A.2 | Google Doc template (11 sections: cover, demographics, accounts, holdings, risk, medicare, life, strategy, discovery, report manifest, disclosure) | Not started | Created via `SETUP_CreateCaseCentralTemplate()` |
| 4A.3 | 3 presets: `full` (11 sections), `gradient_handoff` (9 sections), `quick_summary` (6 sections) | Not started | Defined in `CASE_CENTRAL_PRESETS_` constant |
| 4A.4 | Household support — merge multiple clients into one package | Not started | Cover shows "Sprenger Household", accounts merge, Owner column in holdings |
| 4A.5 | UI buttons in Yellow Stage Case Central tab | Not started | "Generate Case Package" + "Gradient Handoff" buttons in Scripts.html |
| 4A.6 | ACF folder resolution — `resolveCasesFolder_()` targeting "B4 Cases" subfolder | Not started | Mirrors `resolveRecFolder_()` from PRODASH_MEDICARE_REC.gs |
| 4A.7 | Report order status update — mark `case_central_package` as `complete` after generation | Not started | Updates `type_fields.report_order.reports` |

### 4B: Data Flow

```
_CLIENT_MASTER → demographics, address, spouse, agent
_ACCOUNT_* (all 5 types) → account summary + holdings tables
opportunity.type_fields.discovery_kit → COMRA score, form status
opportunity.type_fields.report_order → report manifest
opportunity.type_fields.casework → strategy notes
          |
PRODASH_CASE_CENTRAL.gs :: generateCaseCentralPackage_()
          |
Google Doc template (copy > merge > clean sections > PDF)
          |
ACF "B4 Cases" folder + report_order status updated
```

**New files:** `PRODASH_CASE_CENTRAL.gs` (~500 lines)
**Modified:** `Scripts.html` (~40 lines), `PRODASH_REPORT_ORDER.gs` (1 line — mark shipped)
**Dependency:** Yellow Stage (2A.3-2A.4) should be built first, but Case Central backend can be built independently.
**Triggered by:** Sprenger household Gradient transition (4-6 week timeline from Feb 25).

---

## Stream 5: Client Communications

**Status: PARTIAL — RAPID_COMMS library live, PRODASHX integration not started**
**Source plan:** `velvety-hatching-sun.md`

### 5A: CLIENT360 Integration (wire existing buttons)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5A.1 | Wire `uiSendClientEmail` -> RAPID_COMMS.sendEmail() + real SendGrid message ID | Not started | Modify PRODASH_CLIENT360.gs:762-815 |
| 5A.2 | Wire `uiSendClientSMS` -> RAPID_COMMS.sendSMS() + Twilio SID | Not started | Pending A2P 10DLC verification |
| 5A.3 | New `uiInitiateClientCall` -> RAPID_COMMS.initiateCall() with recording | Not started | Add Call button to Index.html |

**Prereq:** JDM adds RAPID_COMMS library to PRODASH (one-time, GAS editor)

### 5B: Standalone Communications Module

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5B.1 | New `PRODASH_Communications.gs` — server functions | Not started | uiGetCommsInbox, uiSendComm, uiSearchContacts |
| 5B.2 | "Communications" top-level nav item + inbox UI | Not started | Smart Lookup contact search across clients + team + carriers |
| 5B.3 | Quick actions: Email, Text, Call for any contact | Not started | Reuses RAPID_COMMS |
| 5B.4 | Activity log — all channels, all contacts, recent history | Not started | Reads from `_COMMUNICATION_LOG` |

### 5C: Recording Pipeline (future)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5C.1 | Auto-download call recordings from Twilio to Google Drive | Not started | ~$0.024/min transcription |
| 5C.2 | Google Speech-to-Text transcription | Not started | Requires GCP API enablement |
| 5C.3 | Voicemail capture + transcription for inbound calls | Not started | TwiML greeting + record + webhook |

---

## Stream 6: Team Communications Platform (NEW)

**Status: CONCEPT — JDM's vision for Slack replacement**
**Source: JDM directive (Mar 3) + elevated from v3.11.1 Priority 6**

### The Vision

> "Active Threads / Channels... We're actively working on replacing Slack. Maybe a new concept should be considered for the TEAM Communications idea? This is going to be something that we deploy across the Platforms eventually (RIIMO / ProDash / SENTINEL) — like we've done with the MyRPI Section."

### Concept: RPI Messenger — Cross-Platform Shared Component

Like MyRPI (shared module across all 3 platforms), Team Comms becomes a **shared drawer/panel** that lives in every RPI platform. Backed by Google Chat APIs (we already have full read/write via rpi-workspace MCP).

**Form factor: Left Drawer** (DECIDED 2026-03-03)

```
┌──────┬────────────┬─────────────────────────┐
│  D   │ Messenger  │                         │
│  C   │ ────────── │      Main Content       │
│  A   │ # general  │                         │
│  S   │ # sales    │   (stays full-width     │
│      │ # service  │    when drawer closed)   │
│      │ # david    │                         │
│  [M] │ __________ │                         │
│  ^^^ │ Message... │                         │
│trigger└────────────┘                         │
└──────┴──────────────────────────────────────┘
```

**Why left drawer:**
- Trigger (M icon) is in the left sidebar — drawer opens where you clicked
- Matches Slack mental model exactly (channels on left)
- Main content stays anchored to right edge (better for data tables)
- Feels like the sidebar "expanding" — one fluid motion
- Code: `left: 52px` + `translateX(-100%)` toggle. No z-index battles.

### Architecture

```
Shared Component: RPI_MESSENGER
├── Module file: shared across RIIMO / PRODASHX / SENTINEL (like MyRPI)
├── Backend: Google Chat API (spaces, messages, threads)
│   ├── list_spaces → channels/DMs
│   ├── list_messages → thread feed
│   ├── send_message → compose
│   └── reply_to_thread → thread replies
├── Real-time: Polling or Chat webhook → RAPID_API
└── UI: Drawer/Panel component with:
    ├── Channel list (Google Chat spaces)
    ├── Active threads (recent messages per space)
    ├── DM list (1:1 conversations)
    ├── Compose (send to space or DM)
    ├── Thread view (replies within a message)
    └── Unread badge count on launcher icon
```

### What This Replaces

| Slack Feature | RPI Messenger | Powered By |
|---------------|---------------|------------|
| #channels | **Channels** | Google Chat Spaces |
| @mentions | @mentions | Google Chat |
| Threads | **Threads** | Google Chat thread replies |
| DMs | **Chat** | Google Chat DMs |
| Huddles | **Meet** | Google Meet (one-click, no calendar needed) |
| File sharing | Drive links in messages | Google Drive |
| Notifications | Badge count on RPI Shield icon | Native |
| Bots/Integrations | RAPID_API webhooks | Already built |

**Branding rule:** Respect Google's ecosystem. Chat = Chat. Meet = Meet. No rebranding their products.

### Implementation Phases

| # | Item | Scope | Notes |
|---|------|-------|-------|
| 6.1 | **Design the shared module pattern** — establish how cross-platform components work (following MyRPI precedent) | Architecture | Define: shared .gs file, shared HTML partial, per-platform CSS theming |
| 6.2 | **Channels + Chat list** — all Google Chat Spaces + DMs with unread indicators | MVP | list_spaces + list_messages (last message per space) |
| 6.3 | **Thread feed** — click a channel, see messages with thread indicators | MVP | list_messages for a space |
| 6.4 | **Compose + Reply** — send messages and reply to threads inline | MVP | send_message + reply_to_thread |
| 6.5 | **Unread tracking** — badge count on RPI Shield icon, per-channel unread counts | MVP | Requires tracking last-read timestamp per user per space |
| 6.6 | **Left drawer UI** — slides out from sidebar, collapsible, persists across nav | MVP | CSS translateX + flex child, theme-aware per platform |
| 6.7 | **Meet integration** — "Start Meet" button in compose area, creates Meet link, posts in channel, live indicator bar | MVP | meet_create_meeting + send_message |
| 6.8 | **RPI Shield trigger** — branded shield icon at sidebar bottom with notification badge | MVP | Asset: RPI-3.svg from WordPress media |
| 6.9 | **Deploy to PRODASHX first** — prove the pattern | MVP | Then RIIMO + SENTINEL follow |
| 6.10 | **Polling / real-time** — auto-refresh messages on interval or webhook push | Post-MVP | GAS time-based trigger or RAPID_API webhook from Chat |
| 6.11 | **Deploy to RIIMO + SENTINEL** — same component, different theme | Post-MVP | |

### Decisions Made

- **Form factor:** Left drawer — slides out from sidebar (DECIDED 2026-03-03)
- **MVP scope:** TBD — Channels + threads + compose, or just DMs first?
- **Migration:** TBD — Hard cutoff from Slack, or parallel run?

---

## Stream 7: Communications Wiring

**Status: NOT STARTED**
**Source plan:** `declarative-crunching-rainbow.md` (consolidated 2026-03-08)

PRODASHX communications are ~70% done. CLIENT360 + Comms Hub already send email/SMS/voice via RAPID_COMMS, log to `_COMMUNICATION_LOG`, and display history. This stream wires the remaining 30%: campaign sends, enrollment/queue system, DND enforcement, and delivery status display.

### 7A: Wave 1 — Foundation (parallel, ~1 session)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7A.1 | RAPID_CORE — Add `_CAMPAIGN_ENROLLMENTS` + `_QUEUED_SENDS` schemas to TABLE_ROUTING + TAB_SCHEMAS | Not started | 16 + 16 columns |
| 7A.2 | RAPID_API — Wire 3 campaign send stubs to RAPID_COMMS (email, SMS, VM drop) with DND checks + external_id capture | Not started | Replace stubs in API_CampaignSend.gs |
| 7A.3 | PRODASHX — Add DND enforcement to CLIENT360 send functions (uiSendClientEmail/SMS/Call) | Not started | Check `dnd_email/sms/phone/all` flags before send |
| 7A.4 | RAPID_API — Set `WEBHOOK_BASE_URL` Script Property (JDM one-time) | Not started | Points to RAPID_API Primary deployment URL |

### 7B: Wave 2 — Enrollment Engine (~2 sessions)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7B.1 | RAPID_API — `enrollContacts_()` endpoint: load campaign, compute touchpoint schedule, create enrollment + queued send records | Not started | New routes: POST /campaign/enroll, GET /campaign/enrollments, GET /campaign/queue |
| 7B.2 | PRODASHX — `PRODASH_Campaigns.gs` (NEW): campaign list, detail, target preview, enrollment, send history, stats | Not started | ~300 lines |
| 7B.3 | PRODASHX — "Campaigns" section UI: campaign grid, detail view, sequence timeline, target preview, enrollment modal | Not started | Index.html + Scripts.html |

### 7C: Wave 3 — Automation + Status UI (~1 session)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7C.1 | RAPID_API — `processQueuedSends_trigger()`: pick up due sends (50/run), route by channel, update enrollment progress | Not started | JDM creates 15-min trigger after deploy |
| 7C.2 | PRODASHX — Delivery status badges in CLIENT360 comms timeline (sent/delivered/opened/bounced/failed) | Not started | Channel icons + campaign name badges |

**New files:** `PRODASH_Campaigns.gs` (~300 lines)
**Modified:** `CORE_Database.gs` (schemas), `API_CampaignSend.gs` (3 stubs + enrollment + queue processor), `PRODASH_CLIENT360.gs` (DND), `PRODASH_Communications.gs` (DND), `Index.html`, `Scripts.html`
**JDM actions:** Set WEBHOOK_BASE_URL, create queue trigger

---

## Stream 8: Performance (Unified Matrix Cache)

**Status: NOT STARTED**
**Source plan:** `hidden-juggling-dahl.md` (consolidated 2026-03-08)

PRODASHX loads slowly because every UI function independently opens PRODASHX_MATRIX and reads full sheets. A single CLIENT360 view triggers 5 `SpreadsheetApp.openById()` calls and up to 16 reads. The fix: one cached scanner — one spreadsheet open, 7 sheet reads, cached for 60 seconds.

### 8A: Create PRODASH_MatrixCache.gs (NEW)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 8A.1 | `scanMatrix_()` — opens PRODASHX_MATRIX once, reads all 7 sheets, builds all indexes, caches 60s | Not started | `var` for module-level cache (GAS requirement) |
| 8A.2 | `getClient_(id)` — O(1) lookup by client_id OR ghl_contact_id (dual-key) | Not started | Replaces linear scans |
| 8A.3 | `getAllClients_()` — deduplicated client array | Not started | Replaces `readClientsFromMatrix_()` |
| 8A.4 | `getAllAccounts_(type)` — accounts by type or all | Not started | Replaces `readAccountsFromMatrix_()` |
| 8A.5 | `getAccountsForClient_(clientId, type)` — indexed account lookup | Not started | Replaces full-sheet-then-filter |
| 8A.6 | `invalidateMatrixCache_()` — cache buster called after writes | Not started | |

### 8B: Refactor Consumers (8 files)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 8B.1 | `PRODASH_Clients.gs` — delegate to cache, remove local cache vars | Not started | ~80 lines simplified |
| 8B.2 | `PRODASH_Accounts.gs` — delegate to cache, remove local cache vars | Not started | ~60 lines simplified |
| 8B.3 | `Code.gs` — wire dashboard stats/priority queue/activity to cache | Not started | ~40 lines simplified |
| 8B.4 | `PRODASH_CLIENT360.gs` — indexed lookups (biggest win: 16 reads -> 0) | Not started | ~100 lines simplified |
| 8B.5 | `PRODASH_SALES_CENTERS.gs` — 1-line scanner swap | Not started | |
| 8B.6 | `PRODASH_SERVICE_CENTERS.gs` — 1-line scanner swap | Not started | |
| 8B.7 | `PRODASH_CASE_CENTRAL.gs` + `PRODASH_MEDICARE_REC.gs` — cache lookups | Not started | ~30 lines simplified |
| 8B.8 | Add `invalidateMatrixCache_()` to all write functions | Not started | Code.gs, Accounts, CLIENT360, CASEWORK |

### Performance Impact

| Scenario | Before | After (cold/warm) |
|----------|--------|-------------------|
| Dashboard load | 4 opens, 8 reads | 1 open, 7 reads / 0, 0 |
| CLIENT360 view | 5 opens, 16 reads | 0, 0 (cached) |
| Accounts page | 1 open, 5 reads | 0, 0 (cached) |
| **Worst case (cold)** | -- | 1 open, 7 reads (~2-3s) |
| **Best case (warm)** | -- | 0 opens, 0 reads (<50ms) |

**New files:** `PRODASH_MatrixCache.gs` (~250 lines)
**Net result:** ~250 new lines, ~425 lines simplified/removed. SpreadsheetApp.openById() calls in hot paths: 44 -> 1 per 60s window.

---

## Recommended Execution Order

Based on dependencies, urgency, and value:

### Phase 1: Stabilize (v3.11.1)
**Stream 1** — Fix the production blockers.
- Dead screen fix (1.1)
- Client search fix (1.2)
- MyRPI layout (1.3)
- Quick Intake improvements (1.4-1.5)

### Phase 2: Wire What's Built
**Streams 3 + 5A** — UI for backends that already exist.
- Medicare Rec UI tab (3.5) + Comparison fix (3.6)
- CLIENT360 comms buttons (5A.1-5A.3)

Both are frontend-only work connecting to finished backends. High ROI.

### Phase 3: Sales Pipeline Foundation
**Stream 2A** — Stage architecture + Report Order.
- Stage scanner generalization (2A.1)
- Blue Stage rename + Report Order sub-tab (2A.2, 2B.1-2B.4)
- Yellow Stage backend + UI (2A.3-2A.4)
- Orange/Green stubs + nav refactor (2A.5-2A.6)

This unlocks the workbench (Phase 4) and Case Central (Stream 4).

### Phase 4: Casework Workbench
**Stream 2C** — The team's daily driver.
- Task schema + API (2C.1-2C.2)
- Casework backend + My Cases + Case Detail (2C.3-2C.7)

### Phase 5: Client Outputs
**Stream 4** — Case Central Package module.
- PDF generator + templates + presets (4.1-4.5)

Can be pulled forward if Sprenger/Gradient timeline demands it.

### Phase 6: Communications Platform
**Stream 5B + 5C** — Standalone comms module + recording pipeline.
- Comms module nav + inbox (5B.1-5B.4)
- Recording download + transcription (5C.1-5C.3)

### Phase 7: Team Comms (Slack Replacement)
**Stream 6** — Cross-platform RPI Messenger.
- Design shared module pattern (6.1)
- MVP: channels, threads, compose, drawer UI (6.2-6.7)
- Deploy to PRODASHX first, then RIIMO + SENTINEL (6.7, 6.10)

---

## Files Inventory (All Streams)

### New Files
| File | Stream | Lines Est. |
|------|--------|-----------|
| `PRODASH_REPORT_ORDER.gs` | 2B | ~400 |
| `PRODASH_YELLOW_STAGE.gs` | 2A | ~350 |
| `PRODASH_STAGE_STUBS.gs` | 2A | ~150 |
| `PRODASH_CASEWORK.gs` | 2C | ~350 |
| `PRODASH_CASE_CENTRAL.gs` | 4 | ~500 |
| `PRODASH_Communications.gs` | 5B | ~300 |
| `PRODASH_MESSENGER.gs` (or shared) | 6 | ~400 |
| `RAPID_API/API_Task.gs` | 2C | ~200 |

### Modified Files (all streams touch these)
- `Code.gs` — exec URL, new module wrappers
- `Index.html` — nav restructure, new views, drawer/panel
- `Scripts.html` — all new client-side logic
- `Styles.html` — stage colors, comms, messenger themes
- `PRODASH_SALES_CENTERS.gs` — scanner generalization
- `PRODASH_DISCOVERY_KIT.gs` — Blue Stage rename
- `PRODASH_CLIENT360.gs` — comms wiring
- `RAPID_CORE/CORE_Database.gs` — `_CASE_TASKS` schema

---

## Source Plans (Archived Reference)

| Plan File | Stream | Status |
|-----------|--------|--------|
| `mossy-forging-lightning.md` | FK Migration | DONE |
| `floating-percolating-babbage.md` | Medicare Pipeline | DONE (v166-168) |
| `dynamic-sniffing-starlight.md` | Bug Fixes (v3.11.1) | ACTIVE |
| `rosy-shimmying-riddle.md` | Stage Architecture (2A, 2B) | PARTIAL (Phase 1 only) |
| `radiant-yawning-toucan.md` | Medicare Rec UI (3) | NOT STARTED |
| `velvety-hatching-sun.md` | Communications (5) | PARTIAL (library only) |
| `parsed-hugging-lerdorf.md` | Casework Workbench (2C) | NOT STARTED |
| `humming-exploring-mochi.md` | Case Central Package (4) | CONSOLIDATED into Stream 4 (2026-03-08) |
| `declarative-crunching-rainbow.md` | Comms Wiring (7) | CONSOLIDATED into Stream 7 (2026-03-08) |
| `hidden-juggling-dahl.md` | Performance Refactor (8) | CONSOLIDATED into Stream 8 (2026-03-08) |

---

## Absorbed: wondrous-snuggling-phoenix (Feb 15) — RPI Comms Integration
**Decomposed 2026-03-03. Pieces distributed to:**
- PRODASHX Stream 5 — CLIENT360 comms wiring (already covered by velvety-hatching-sun)
- C3 — GHL code removal (~1,860 lines of push functions + settings panels)
- RIIMO — Team availability dashboard (Calendar free/busy + Chat presence)
- SENTINEL — Deal-scoped comms (covered by glimmering-baking-clarke Phase 7)
- RAPID_IMPORT — Comms intake sync (Twilio messages, SendGrid activity, Meet recordings, GHL migration)
- rpi-comms-mcp + Meet tools — DONE (already built and live)
