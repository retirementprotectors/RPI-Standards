ARCHIVED: Consolidated into tomachina-epic-roadmap.md on 2026-03-13
# RIIMO Platform Roadmap

> Consolidated from 9 individual plans (4 active + 5 archived) + RPI Comms Integration plan.
> Last updated: 2026-03-08

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| v1.8.2 | ~Feb 14 | Solid scaffolding, dark theme, data models — but 9 fake metric functions, dead code, bugs |
| v1.9.0 | Feb 15 | Phase 0 — Security cleanup, deprecated code removal, honest returns, timezone fix |
| v2.0.0 | Feb 15 | Phase 1 — Foundation: real MATRIX health, dynamic sidebar, showToast, error feed, user hierarchy seed |
| v2.1.0 | Feb 15 | Phase 2 — Visibility dashboards: System Health, Data Pipeline, Data Quality, Error Feed, Commission, B2B Pipeline, B2C Client Health cards |
| v3.0 | ~Feb 19 | Entitlements v2 (per-module VIEW/EDIT/ADD), Onboarding + Task System (Pipeline > Stages > Tasks), Job Description Module, Dashboard Overhaul (Command Bar + Pipeline Snapshot + My Tasks + Module Launcher) |
| v3.6.0 | ~Feb 19 | My RPI UX pass: first name fix in top-right bar, auto-create employee Drive folder on onboarding, profile photos from Google Workspace, communication preferences section, Google Picker for document upload |
| v3.6.x | ~Feb 20 | Dashboard vs Intelligence restructure: Dashboard = progress/action (Command Bar, Pipeline Snapshot, My Tasks, Module Launcher), Intelligence = metrics/health/diagnostics (System Health, Platform Overview, Diagnostic Tools, AI Analytics, Ops Intelligence, Integration Hub) |

---

## Stream 1: Production Build Phases 0-4

**Status: PARTIAL — Phases 0-2 shipped, Phases 3-4 outstanding**
**Source plan:** `noble-skipping-plum.md`

### 1A: Phase 0 — Security + Cleanup (SHIPPED)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1A.1 | RIIMO `appsscript.json` → `DOMAIN` + `executionApi` + timezone fix | DONE | Was `ANYONE_ANONYMOUS` |
| 1A.2 | RAPID_API — leave as `ANYONE_ANONYMOUS` (SPARK exception), fix timezone, add API key to `/pipeline` route | DONE | Approved exception for Optum/SPARK webhooks |
| 1A.3 | RPI-Command-Center `ANYONE` → `DOMAIN` + timezone | DONE | |
| 1A.4 | Legacy SENTINEL `ANYONE` → `DOMAIN` + timezone | DONE | |
| 1A.5 | Remove 310 lines deprecated code in `RIIMO_MATRIX_Setup.gs` (lines 492-803) | DONE | Dead migration functions |
| 1A.6 | Remove duplicate `getMATRIX()` (line 886) | DONE | Keep only `RIIMO_Core.gs` version |
| 1A.7 | Replace 9 fake metric functions with honest "not_implemented" returns | DONE | `RIIMO_Pipelines.gs`, `RIIMO_Dashboard.gs` |
| 1A.8 | Fix `event.currentTarget` capture bug (Index.html line 1328) | DONE | Captured button ref BEFORE `await showConfirmation()` |
| 1A.9 | Add `.modal-overlay` CSS | DONE | Backdrop + centering for confirmation modals |
| 1A.10 | Fix default permissions — empty `_USER_HIERARCHY` → USER level (not OWNER) | DONE | Security fix |
| 1A.11 | Remove dead `include()` function from `Code.gs` | DONE | |
| 1A.12 | Add `executionApi: DOMAIN` to 7+ projects (DEX, C3, CAM, CEO-Dashboard, RPI-Command-Center, SENTINEL v2, DAVID-HUB) | DONE | Unblocks MCP execute_script for RIIMO |
| 1A.13 | Write healthcare-mcps setup doc | DONE | JDM deploying on second machine |

### 1B: Phase 1 — Foundation (SHIPPED)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1B.1 | GAS Project Registry (`_GAS_PROJECTS` tab in RAPID_MATRIX) | DONE | Tracks all 13+ projects: script ID, deploy version, RAPID_CORE version, GCP linked, access setting |
| 1B.2 | Real MATRIX health checks — actual `SpreadsheetApp.openById()` try/catch | DONE | Replaced hardcoded "Connected" |
| 1B.3 | Remove hardcoded MATRIX_IDS — use `RAPID_CORE.getMATRIX_IDS()` exclusively | DONE | |
| 1B.4 | Dynamic sidebar — render from `uiGetToolSuites()` respecting cascading permissions | DONE | |
| 1B.5 | `showToast()` component — success/error/info/warning, auto-dismiss | DONE | |
| 1B.6 | Module pages with real links — each module links to actual GAS web app URL + deploy health | DONE | |
| 1B.7 | Error feed card — read `_ERROR_LOG`, show last 24h grouped by source + severity | DONE | |
| 1B.8 | API caller utility — centralized `callRapidAPI()` | DONE | |
| 1B.9 | Populate `_USER_HIERARCHY` — JDM=OWNER, Behn=SUPER_ADMIN, Leaders assigned | DONE | |
| 1B.10 | Admin CRUD (Tier 1) — Behn can create admins, assign to RIIMO modules | DONE | |
| 1B.11 | Permission sync mechanism — RIIMO assignment pushes role to module's `_USER_HIERARCHY` via RAPID_API | DONE | |

### 1C: Phase 2 — Visibility Dashboards (SHIPPED)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1C.1 | System Health Panel — deploy versions, API pings, MATRIX connectivity | DONE | Green/yellow/red per dependency |
| 1C.2 | Data Pipeline Card — `_INTAKE_QUEUE` depth by status, oldest pending age | DONE | |
| 1C.3 | Data Quality Card — dupe count, orphan count, last reconciliation | DONE | |
| 1C.4 | Error Feed (enhanced) — severity chart, source breakdown | DONE | |
| 1C.5 | Commission/Revenue Card — pipeline value, FYC/REN counts | DONE | From CAM/RAPID_MATRIX comp grids |
| 1C.6 | B2B Pipeline Card — deal count, stage distribution, pipeline value | DONE | From SENTINEL_MATRIX |
| 1C.7 | B2C Client Health Card — client count, account totals, basic stats | DONE | From PRODASH_MATRIX |

### 1D: Phase 3 — Control (NOT STARTED)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1D.1 | One-click triggers: GHL Sync, Reconciliation, Config Audit, Cache Clear, Comp Cycle | P2 | Not started |
| 1D.2 | Reconciliation Queue UI — resolve client dupes | P2 | Not started |
| 1D.3 | Real Data Maintenance pipeline — actual cleanup + backup | P3 | Not started |
| 1D.4 | On-boarding/Off-boarding pipeline tracking | P2 | Not started |
| 1D.5 | Security pipeline connected to real audit tools | P3 | Not started |
| 1D.6 | Log viewer with filters | P3 | Not started |

### 1E: Phase 4 — Intelligence (NOT STARTED)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1E.1 | TDM Level scoring (Levels 0-5 per client) | P2 | Not started |
| 1E.2 | Data quality KPIs — orphans, dupes, normalization coverage | P2 | Not started |
| 1E.3 | Revenue + Pipeline analytics | P3 | Not started |
| 1E.4 | MDJ Instance dashboard | P3 | Not started |
| 1E.5 | Carrier intelligence | P3 | Not started |

**Files:** `RIIMO_Dashboard.gs`, `RIIMO_Pipelines.gs`, `RIIMO_Core.gs`, `RIIMO_MATRIX_Setup.gs`, `RIIMO_OrgAdmin.gs`, `RIIMO_Actions.gs`, `RIIMO_Intelligence.gs`, `Index.html`, `Code.gs`, `DashboardWidgets.html`
**Dependencies:** RAPID_CORE (library), RAPID_API (REST layer), all 3 MATRIX spreadsheets

---

## Stream 2: Unit-Based Auto-Assignment

**Status: OPEN**
**Source plan:** `warm-humming-riddle.md`

| # | Item | Priority | Status |
|---|------|----------|--------|
| 2.1 | **Fix unit dropdown** — populate from `UNIT_MODULE_DEFAULTS` (MEDICARE/RETIREMENT/LEGACY), not `_COMPANY_STRUCTURE` entity_ids | P1 | Not started |
| 2.2 | **Add `LEADER_DEFAULT_RAPID_TOOLS` constant** in `RAPID_CORE/CORE_Entitlements.gs` — `['C3', 'RAPID_IMPORT', 'DEX']` auto-granted to Leaders+ with VIEW/EDIT/ADD | P1 | Not started |
| 2.3 | **Update `computeModulePermissions()`** — Leaders+ get C3/RAPID_IMPORT/DEX automatically, CAM only for EXECUTIVE+, MCP_HUB individually assignable | P1 | Not started |
| 2.4 | **Add `onUnitChange()` handler** in `Index.html` — when unit changes + entitlements panel open: compute defaults, update all toggle chips, show toast | P2 | Not started |
| 2.5 | **Decouple unit from division** — unit dropdown should NOT reset when division changes (functional specialty independent of org hierarchy) | P2 | Not started |
| 2.6 | **Add `uiComputeDefaultPermissions(roleTemplateKey, unitId)`** endpoint in `Code.gs` | P1 | Not started |
| 2.7 | **Add `uiGetUnitModuleDefaults()`** endpoint in `Code.gs` | P1 | Not started |
| 2.8 | **Auto-compute on save** — `saveUser()` in `RIIMO_OrgAdmin.gs` auto-computes `module_permissions` when `unit_id` changes for new users | P2 | Not started |
| 2.9 | **Run `FIX_RecomputeAllPermissions()`** — one-time backfill existing Leaders with C3/RAPID_IMPORT/DEX (in `PRODASHX/PRODASH_Migration.gs`) | P2 | Not started |

**Files:** `RAPID_CORE/CORE_Entitlements.gs`, `RAPID_CORE/Code.gs`, `RIIMO/Code.gs`, `RIIMO/Index.html`, `RIIMO/RIIMO_OrgAdmin.gs`, `PRODASHX/PRODASH_Migration.gs`
**Dependencies:** Entitlements v2 (Stream 1, Phase 3 of v3.0 — SHIPPED). RAPID_CORE library push required first.

**Deploy Order:**
1. RAPID_CORE -> `clasp push` + version (library, no deploy needed)
2. RIIMO -> `clasp push` + version + deploy
3. Run `FIX_RecomputeAllPermissions()` in PRODASHX to backfill
4. Verify in RIIMO UI

---

## Stream 3: EP Onboarding Package

**Status: OPEN**
**Source plan:** `rustling-wibbling-babbage.md`

| # | Item | Priority | Status |
|---|------|----------|--------|
| 3.1 | **Create Google Sheet: "RPI x EP -- Carrier Inventory"** — 28 carriers across 3 entities (MFGAN, MFG, MFGA), pre-populated from Q4 2025 bank statement analysis. Columns: Carrier, Payment Frequency, Entity, Avg Monthly $, Agent/Writing #, Username, Password, 2FA Method | P1 | Not started |
| 3.2 | **Create Google Sheet: "RPI x EP -- Commission Structure"** — Tab 1: Rules (flow, formula, multipliers, tiers). Tab 2: Examples (3 worked calculations: MAPD AST-II, Life SPC-I, Annuity SPC-III) | P1 | Not started |
| 3.3 | **Share Signal Transactions Google Sheet** — `1GFCd72nuYw19HscUR58lDNkdkb_aUBeYCiEOELomuDg` (Jan 2023-Nov 2025) with Zane + Abhishek (viewer) | P1 | Not started |
| 3.4 | **Share 3 CoF statement PDFs** — CR5229-20251125, CR5229-20251028, CR5229-20250909 with Zane + Abhishek (viewer) | P1 | Not started |
| 3.5 | **Share Carrier Inventory** with Zane (editor) + Abhishek (editor) | P1 | Not started |
| 3.6 | **Share Commission Structure** with Zane (viewer) + Abhishek (viewer) | P1 | Not started |
| 3.7 | **Draft reply email** to Zane's ASA thread (messageId `19c3efbc0f2222dc`) — ASA info (5 items), links to 6 shared files, commission overview, carrier inventory overview, next steps | P1 | Not started |
| 3.8 | **JDM approval required** before send | BLOCKER | Waiting |

**Carrier inventory detail (28 carriers):**
- MFGAN (acct 5231): Signal ~$232k/mo, Aetna ~$11.4k, UHC ~$3.5k, Wellabe ~$2.4k, Humana ~$950, MMProtect ~$480, CoF ~$340, Ethos ~$367, Chubb ~$300, Ameritas ~$200, NGIS ~$255, Spark ~$162, ITS Alliance ~$667, Lumico ~$109, FGL ~$130, Manhattan Life ~$86, GTL ~$81, Elips ~$68, Mutual of Omaha ~$34, Cigna ~$30, NCD ~$29, Premier Senior ~$52, Lumeris ~$13, Kansas City Life varies
- MFG (acct 4829): GBL/BCBS ~$430, Pacific Life ~$63, Protective Life ~$0.09
- MFGA (acct 5190): Assurity Life ~$36

**Commission structure:**
- Formula: `Net = Gross Revenue x Product Mult x Source Mult x Tier %`
- Product: MAPD 2.0x, MedSupp 1.5x, PDP/Life/Annuity 1.0x
- Source: Merger 2.0x, Acquisition 1.5x, Partnership 1.0x
- B2C Tiers: COR-I 5% through SPC-III 30%
- B2B Tiers: Bronze 20% through Diamond 30%

**Files:** Google Sheets (new), Google Drive sharing, Gmail reply
**Dependencies:** JDM approval on email draft. Share recipients: `zane@ep-insuranceservices.com`, `a.kumar@epr-india.com`

---

## Stream 4: Playbook & Job Description Extraction

**Status: BLOCKED — requires Drive docs to be identified/accessible**
**Source plans:** `parsed-hugging-lerdorf.md` (Casework Workbench — PRODASHX, cross-references RIIMO job templates), `wise-gliding-stonebraker.md` (Phase 2B — Job Description Module)

### 4A: Job Description Module (from v3.0 plan, partially built)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 4A.1 | **`_JOB_TEMPLATES` MATRIX tab** — template_id, role_name, division_id, unit_id, team, status, weekly_schedule (JSON), pipeline_ownership (JSON), module_ownership (JSON), platform_ownership (JSON), minimum_expectations (JSON), goals (JSON), performance_metrics (JSON), rewards (JSON), description_html, metadata | P2 | Not started |
| 4A.2 | **`RIIMO_JobTemplates.gs`** — `getJobTemplates(filters)`, `getJobTemplate(id)`, `saveJobTemplate(data)`, `deleteJobTemplate(id)`, `generateJobDescription(id)`, `cloneJobTemplate(id)`, `linkTemplateToUser(templateId, userId)` | P2 | Not started |
| 4A.3 | **Code.gs endpoints** — `uiGetJobTemplates()`, `uiGetJobTemplate(id)`, `uiSaveJobTemplate(data)`, `uiDeleteJobTemplate(id)`, `uiGenerateJobDescription(id)`, `uiCloneJobTemplate(id)` | P2 | Not started |
| 4A.4 | **Job Templates admin module UI** — List view (table with Role Name, Division, Unit, Status, Last Updated, actions). Template Editor (multi-section form: Identity, Schedule grid, Ownership checklists, Expectations list builder, Goals list builder, Metrics scoreboard builder, Rewards/comp fields). Preview/Generate output with copy button. | P2 | Not started |
| 4A.5 | **Onboarding integration** — queue form optionally links to job template, auto-generates Job Description as first HR task, template's `module_ownership` auto-populates `assigned_modules` | P3 | Not started |

### 4B: Playbook Doc Extraction (BLOCKED)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 4B.1 | **Identify 8 Drive docs** containing existing playbook/job description content | P2 | BLOCKED — docs not yet identified |
| 4B.2 | **Read + parse docs** — extract structured role definitions, responsibilities, KPIs, schedules | P2 | BLOCKED on 4B.1 |
| 4B.3 | **Seed `_JOB_TEMPLATES`** from extracted data via `SETUP_SeedJobTemplates()` | P2 | BLOCKED on 4B.2 |
| 4B.4 | **Map to RIIMO module** — verify extracted data populates all Job Template Editor sections | P3 | BLOCKED on 4B.3 |

**Files:** `RIIMO_JobTemplates.gs` (NEW, ~300-400 lines), `RIIMO_MATRIX_Setup.gs`, `Code.gs`, `Index.html` (or `JobTemplates.html` include)
**Dependencies:** Drive doc identification (JDM to specify which 8 docs). Job Description Module from v3.0 plan. `_JOB_TEMPLATES` tab creation in MATRIX.

---

## Stream 5: Team Availability Dashboard

**Status: NOT STARTED**
**Source plan:** `wondrous-snuggling-phoenix.md` (RPI Communications Integration — Sprint 8)

| # | Item | Priority | Status |
|---|------|----------|--------|
| 5.1 | **Calendar free/busy card** — Query Google Calendar API for team members, show availability grid (free/busy/OOO) for today + next 2 days. Color-coded: green = free, yellow = tentative, red = busy, gray = OOO | P3 | Not started |
| 5.2 | **Chat presence indicator** — Query Google Chat API for team member online/offline/DND status. Show colored dot next to each team member name | P3 | Not started |
| 5.3 | **Team Availability dashboard card** — Combined widget showing both calendar availability + chat presence for all team members. Render in RIIMO Dashboard or Intelligence section | P3 | Not started |
| 5.4 | **Google Chat panel** — Embedded internal comms panel for quick team messages without leaving RIIMO. Read/send messages to Chat spaces | P4 | Not started |
| 5.5 | **"Schedule Meeting" quick action** — One-click to create Calendar event with Google Meet link for any team member who shows as free | P4 | Not started |

**Files:** `RIIMO_Dashboard.gs` or `RIIMO_Intelligence.gs`, `DashboardWidgets.html`, `Code.gs`
**Dependencies:** Google Calendar MCP (available), Google Chat tools in rpi-workspace MCP (available), Google Meet tools in rpi-workspace MCP (available). rpi-comms MCP for full comms integration (Sprint 8 of phoenix plan).

---

## Stream 6: Strategic Context

**Status: CONCEPT — long-term vision items, no active plans**

| # | Item | Priority | Status | Description |
|---|------|----------|--------|-------------|
| 6.1 | **TDM Levels (Team Decision Matrix)** | P2 | Concept | Scoring system Levels 0-5 per client measuring data completeness, engagement depth, product penetration, service quality. Feeds Intelligence dashboards. Drives automated outreach triggers via C3 campaigns. |
| 6.2 | **MDJ Instances (Multi-Dimensional Job descriptions)** | P3 | Concept | Each role has a living MDJ document auto-generated from `_JOB_TEMPLATES` + actual performance data. Shows expected vs actual: schedule adherence, pipeline ownership, module usage, KPI attainment. Self-updating via MATRIX data. |
| 6.3 | **AI Platform Control Plane** | P3 | Concept | RIIMO as the master control surface for all AI/MCP operations. Monitor MCP tool usage (HEM analytics already running), token consumption, model selection, cost tracking. Manage which team members can invoke which AI capabilities. |
| 6.4 | **Data Quality Pipeline** | P2 | Concept | Automated continuous data health monitoring: orphaned records (accounts without clients), duplicate detection (client dedup scoring), normalization coverage (how many fields meet schema standards), FK integrity checks (client_id references valid across all MATRIX tabs). Surfaces issues to Command Bar as actionable items. |
| 6.5 | **Cascading Permission Model (full implementation)** | P2 | Partially built | RIIMO is THE master permission source. Tier 1 (RIIMO): OWNER/SUPER_ADMIN assigns module admins. Tier 2 (Module UIs): Admins manage team access within PRODASH/SENTINEL/etc. Tier 3 (End Users): access determined by module admin. Foundation shipped in v3.0, full cascade + data isolation audit still needed. |
| 6.6 | **Data Isolation Enforcement** | P2 | Not started | Audit all downstream UIs (PRODASH, SENTINEL, CAM, etc.) for exposed MATRIX IDs in rendered HTML. Scrub any spreadsheet IDs, script IDs, deploy IDs, direct MATRIX links from non-RIIMO UIs. Only RIIMO admins should see actual infrastructure. |

**Dependencies:** Streams 1-4 provide the foundation. TDM Levels require client data normalization (MATRIX health). MDJ Instances require Job Description Module (Stream 4). AI Control Plane requires MCP analytics pipeline (already running via `com.rpi.mcp-analytics` launchd agent). Data Quality Pipeline requires RAPID_CORE reconciliation functions.

---

## Stream 7: Booking Engine (Phase 6+7)

**Status: NOT STARTED**
**Source plan:** `memoized-stirring-nova.md` (consolidated 2026-03-08)
**Absorbs:** `zazzy-meandering-flamingo.md` (Phase 6 Booking Pages — superseded)

Phase 6 delivered 19 booking pages on WordPress (12 individual + 7 team) with auto-sync, Google profile photos, schema-driven titles, and tiered directory. Phase 7 replaces Google Calendar pre-fill links with the full Calendly-killer: availability checking, contact collection, auto-booking, and automated comms.

### 7A: Phase 6 Cleanup (30 min)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7A.1 | Daily WP sync trigger | DONE | JDM verified active |
| 7A.2 | WP credentials in Script Props | DONE | Stored via execute_script |
| 7A.3 | Instant sync on profile save — hook `syncBookingPage()` into `saveUser()` and `updateMeetRoom()` | Not started | RIIMO_OrgAdmin.gs + RIIMO_MyRPI.gs |
| 7A.4 | On-boarding/off-boarding pipeline steps — auto-create/delete booking pages | Not started | Add to `_PIPELINE_CONFIG` |

### 7B: Phase 7a — Core Booking Engine (Session 1)

Architecture: RAPID_API iframe + WordPress shell. RAPID_API is the only public GAS app (`ANYONE_ANONYMOUS` — approved exception). WordPress pages embed `RAPID_API?page=booking&agent={slug}` as iframe.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7B.1 | `_BOOKING_LOG` tab schema in RAPID_CORE (17 columns: booking_id, agent_email, client_name/email/phone, guests, type, mode, start/end, duration, reason, status, calendar_event_id, meet_link, confirmation_sent, created_at) | Not started | TABLE_ROUTING + TAB_SCHEMAS |
| 7B.2 | `?page=booking` route in RAPID_API `doGet()` | Not started | Serves BOOKING_UI.html |
| 7B.3 | `API_Booking.gs` (NEW) — `getBookingConfig()`, `getAvailableSlots()`, `createBooking()`, `sendConfirmation()` | Not started | Uses CalendarApp for native Google Calendar read/write |
| 7B.4 | `BOOKING_UI.html` (NEW) — 4-step flow: meeting type cards > date/time picker > contact form > confirmation | Not started | Mobile-responsive, RPI-branded |
| 7B.5 | Update WordPress booking pages — replace Google Calendar links with iframe embed | Not started | Via WordPress MCP |
| 7B.6 | End-to-end test: book meeting > calendar event created > confirmations sent | Not started | |

### 7C: Phase 7b — Availability Management (Session 2)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7C.1 | `employee_profile.availability` schema — business_hours (per day), buffer_minutes, max_advance_days, allow_f2f, f2f_location | Not started | JSON field in _USER_HIERARCHY |
| 7C.2 | RIIMO MyRPI availability editor — editable by user (own profile) or LEADER+ (via profile switcher) | Not started | MyRPI.html section |
| 7C.3 | Seed default availability for all 12 team members | Not started | SETUP function |
| 7C.4 | Wire availability into `getAvailableSlots()` — real calendar + business hours | Not started | |
| 7C.5 | Mode selector in booking form (Call/Meet/F2F with gating) | Not started | F2F requires `allow_f2f=true` |

### 7D: Phase 7c — Communications + Polish (Session 3)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7D.1 | SendGrid email templates for booking confirmation + reminder | Not started | Via RAPID_COMMS |
| 7D.2 | Twilio SMS confirmation + reminder | Not started | Via RAPID_COMMS |
| 7D.3 | 24-hour reminder trigger (GAS time-driven) | Not started | JDM creates trigger |
| 7D.4 | Reschedule/cancel flow (link in confirmation email > updates event + log) | Not started | |
| 7D.5 | Slack DM to agent on booking | Not started | Via Slack MCP |

### Automated Communications (on booking)

- **To Client:** Email confirmation (meeting details, Meet link, reschedule link) + SMS ("Your [type] with [agent] is confirmed for [date]")
- **To Agent:** Slack DM + Google Calendar event (auto-appears as attendee)
- **24hr before:** Email + SMS reminder to client; agent gets native Calendar reminder

**New files:** `API_Booking.gs` (~300 lines), `BOOKING_UI.html` (~400 lines)
**Modified:** `RAPID_API/Code.gs` (doGet route), `CORE_Database.gs` (schema), `RIIMO_MyRPI.gs` (availability), `MyRPI.html` (availability editor)

---

## Recommended Execution Order

### Phase 1: Quick Wins + Unblock EP (Streams 2 + 3)

**Why first:** Stream 2 (Unit Auto-Assignment) is a small, focused change to RAPID_CORE + RIIMO that immediately improves the admin UX for all Leaders. Stream 3 (EP Onboarding) is time-sensitive -- Zane is waiting for data deliverables. Both are independent and can run in parallel.

- Stream 2: ~1 session (RAPID_CORE library push + RIIMO deploy + backfill)
- Stream 3: ~1 session (create sheets, share files, draft email, JDM approval)

### Phase 2: Job Description Module (Stream 4A)

**Why second:** Builds the `_JOB_TEMPLATES` infrastructure that feeds into onboarding, MDJ Instances, and team management. Once the module UI exists, Drive doc extraction (Stream 4B) can populate it whenever those docs are identified.

- Stream 4A: ~2-3 sessions (new GAS file, MATRIX tab, UI module)
- Stream 4B: unblocked once JDM identifies the 8 Drive docs

### Phase 3: Control Console (Stream 1D)

**Why third:** Phases 0-2 shipped the visibility layer. Phase 3 adds the ability to ACT on what you see -- trigger operations, resolve dupes, manage pipelines. This is what transforms RIIMO from a dashboard into a command center.

- Stream 1D: ~3-4 sessions (pipeline implementations, reconciliation UI, log viewer)

### Phase 4: Intelligence + Availability (Streams 1E + 5)

**Why fourth:** Intelligence (TDM scoring, cross-platform analytics) and Team Availability (calendar/chat presence) are valuable but not blocking anyone. They enhance RIIMO's value once the foundation (Streams 1-4) is solid.

- Stream 1E: ~2-3 sessions
- Stream 5: ~1-2 sessions (leverages existing MCP tools)

### Phase 5: Strategic Vision (Stream 6)

**Why last:** These are long-term architecture items that mature as the platform grows. Data Quality Pipeline is the most immediately useful. MDJ Instances and AI Control Plane require more foundation work. Data Isolation Enforcement should be a dedicated security audit.

---

## Source Plans (Archived Reference)

| Plan File | Stream | Status |
|-----------|--------|--------|
| `noble-skipping-plum.md` | Stream 1: Production Build Phases 0-4 | PARTIAL (Phases 0-2 shipped, 3-4 open) |
| `warm-humming-riddle.md` | Stream 2: Unit-Based Auto-Assignment | OPEN |
| `rustling-wibbling-babbage.md` | Stream 3: EP Onboarding Package | OPEN |
| `parsed-hugging-lerdorf.md` | Stream 4 (cross-ref): Casework Workbench is PRODASHX, but references RIIMO job templates | OPEN (PRODASHX stream) |
| `wondrous-snuggling-phoenix.md` | Stream 5: Team Availability (Sprint 8 of RPI Comms Integration) | NOT STARTED |
| `twinkling-tinkering-shell.md` | Stream 1: v1.9-2.1 (deprecated code removal, real MATRIX health, Cloud Run) | ARCHIVED — shipped |
| `wise-gliding-stonebraker.md` | Streams 1 + 4: v3.0 (Entitlements v2, Onboarding/Tasks, Job Descriptions, Dashboard Overhaul) | ARCHIVED — partially shipped |
| `linked-spinning-meerkat.md` | Stream 1: v3.6.0 (first name fix, Drive folder, profile photos, Google Picker) | ARCHIVED — shipped |
| `zany-snacking-petal.md` | Stream 1: v3.6.x (Dashboard vs Intelligence restructure) | ARCHIVED — shipped |
| `memoized-stirring-nova.md` | Stream 7: Booking Engine Phase 6+7 | CONSOLIDATED (2026-03-08) |
| `zazzy-meandering-flamingo.md` | Stream 7 (absorbed): Phase 6 Booking Pages | SUPERSEDED by memoized-stirring-nova |

---

## Key Architecture Notes

### Cascading Permission Model

```
Tier 1: RIIMO
├── OWNER (JDM) — all access, final authority
└── SUPER ADMIN (John Behn) — creates admins, assigns RIIMO modules
    └── Assigns Admin to modules → TWO things happen:
        1. Admin gets view/edit in RIIMO for those modules
        2. Admin gets ADMIN role inside that module's actual UI

Tier 2: Module UIs (PRODASH, SENTINEL, CAM, DEX, C3, etc.)
├── Admin (pushed from RIIMO assignment) — manages their team's access
└── Creates user entitlements: view-only, agent, service, etc.
    └── Controls which sub-modules their team sees + can edit

Tier 3: End Users (sales/service team)
└── Access determined by their admin in the module UI
```

### User Hierarchy (Current)

| Person | RIIMO Level | Platform Access |
|--------|-------------|-----------------|
| JDM (josh@retireprotected.com) | OWNER (0) | All |
| John Behn (john@retireprotected.com) | EXECUTIVE (1) | All |
| Matt McCormick | LEADER (2) | DAVID Tools + RAPID Tools |
| Vinnie Vazquez | LEADER (2) | RPI Tools + RAPID Tools |
| Nikki Gray | LEADER (2) | RPI Tools + RAPID Tools |
| Dr. Aprille Trupiano | LEADER (2) | RPI Tools + RAPID Tools |
| Shane Parmenter | NOT in RIIMO | N/A |
| Jason Moran | NOT in RIIMO | N/A |

### Data Isolation Rule (NON-NEGOTIABLE)

- NO spreadsheet IDs, script IDs, deploy IDs, or direct MATRIX links exposed in any UI except RIIMO
- Only RIIMO admins can see actual infrastructure (project registry, MATRIX connections, deploy status)
- Downstream UIs access data ONLY through API layers (RAPID_API, RAPID_CORE functions)
- No one touches actual code or data itself unless they are admins of RIIMO

### HTML Size Management

Index.html uses GAS HTML includes to stay manageable:
```html
<?!= include('DashboardWidgets') ?>
<?!= include('TaskManager') ?>
<?!= include('JobTemplates') ?>
<?!= include('MyRPI') ?>
```

### Dashboard vs Intelligence Split (v3.6.x)

**Dashboard** = "What's the progress on shit?" — Command Bar, Pipeline Snapshot, My Tasks, Module Launcher. 3 rows, 3 async loaders, fast.

**Intelligence** = metrics + health + diagnostics — System Health, Platform Overview (B2C/B2B tabs), Diagnostic Tools (5 action buttons), AI Analytics, Operations Intelligence, Integration Hub.
