> ARCHIVED: Superseded by polymorphic-twirling-hopper.md on 2026-03-08

# PLAN: Source of Truth Registry App

## Context

RPI has 80+ carriers, 6+ product lines, and dozens of data flows — but no single system tracks WHERE data comes from, HOW it gets here, WHO is responsible for manual pulls, and WHAT the gap is between current state (monthly CSV download) and target state (daily API feed). Today that knowledge lives in JDM's head, scattered CLAUDE.md docs, and tribal knowledge.

RAPID_IMPORT already tracks 13 automated integrations via `_INTEGRATION_STATUS`, but the 30-50+ manual data flows (carrier portal CSV downloads, BoB exports, commission sheets) have zero tracking. When JDM wants to delegate "pull the Wellmark MAPD BoB report," there's no system for assigning, scheduling, or verifying completion.

This App closes that gap: a live, granular, field-level registry of every data source across every carrier and product line — with calendar scheduling, task delegation, gap analysis, and automation scoring.

---

## Decision: New GAS Project (App Pattern)

Research confirms RPI Apps (Command Center, DEX, C3, CAM) are:
- **Separate GAS projects** with their own Script ID + Deploy ID
- **Registered in RAPID_CORE** `CORE_Entitlements.gs` (MODULES + TOOL_SUITES)
- **Registered in RIIMO** `RIIMO_Core.gs` (PROJECT_REGISTRY with deployId)
- **Opened via `window.open()`** from RIIMO sidebar
- **Use RAPID_CORE as library**, write through RAPID_API

RAPID_IMPORT is already 81K lines / 747 functions. This is a management/delegation tool, not a data ingestion function. It belongs as a peer App.

**Working name: ATLAS** (All-source Tracking, Ledger, Analytics & Scheduling)
- JDM may rename — suggest alternatives: NEXUS, PULSE, GRID, or keep SOT

---

## Architecture

```
ATLAS (New GAS Web App)
  |
  |-- Reads from:
  |     _INTEGRATION_STATUS (13 automated sources, updated every 30 min by RAPID_IMPORT)
  |     _CARRIER_MASTER (canonical carrier data from RAPID_CORE)
  |     _USER_HIERARCHY + _COMPANY_STRUCTURE (team/routing from RAPID_CORE)
  |
  |-- Owns (new RAPID_MATRIX tabs):
  |     _SOURCE_REGISTRY (carrier x product x domain — the master registry)
  |     _SOURCE_TASKS (recurring manual pull tasks + one-off migrations)
  |     _SOURCE_HISTORY (audit trail of all data pulls)
  |     _SOURCE_METRICS (aggregated analytics per period)
  |
  |-- Writes via:
  |     RAPID_API (all MATRIX writes, per standard)
  |
  |-- Integrates with:
  |     Google Calendar (task scheduling, shared "RPI Data Pulls" calendar)
  |     Slack (daily per-owner DMs, weekly JDM summary, overdue escalation)
  |     RAPID_IMPORT (consumes _INTEGRATION_STATUS, does NOT modify RAPID_IMPORT code)
```

---

## Data Model

### Tab 1: `_SOURCE_REGISTRY` (Master Registry)
One row per carrier x product line x data domain.

| Field | Type | Example |
|-------|------|---------|
| source_id | UUID PK | `SRC_a1b2c3` |
| carrier_name | String | `Wellmark` |
| carrier_id | FK _CARRIER_MASTER | (optional, null if carrier not in master) |
| product_line | Enum | `MAPD`, `MED_SUPP`, `FIA`, `MYGA`, `TERM_LIFE`, `WHOLE_LIFE`, `IUL`, `BDRIA` |
| product_category | Enum | `HEALTH`, `WEALTH`, `LEGACY` |
| data_domain | Enum | `ACCOUNTS`, `COMMISSIONS`, `DEMOGRAPHICS`, `CLAIMS`, `ENROLLMENT`, `LICENSING`, `VALIDATION` |
| current_source | String | `Carrier Portal CSV`, `Stateable API`, `SPARK Webhook`, `Manual Entry` |
| current_method | Enum | `MANUAL_CSV`, `API_FEED`, `WEBHOOK`, `MANUAL_ENTRY`, `SFTP`, `NOT_AVAILABLE` |
| current_frequency | Enum | `REALTIME`, `DAILY`, `WEEKLY`, `MONTHLY`, `QUARTERLY`, `ON_DEMAND`, `NONE` |
| current_owner_email | FK _USER_HIERARCHY | `nikki@retireprotected.com` |
| target_source | String | `DTCC I&RS`, `Blue Button FHIR`, `Carrier API` |
| target_method | Enum | (same as current_method) |
| target_frequency | Enum | (same as current_frequency) |
| gap_status | Enum | `GREEN` (automated), `YELLOW` (manual but working), `RED` (not flowing), `GRAY` (not needed) |
| automation_pct | Integer 0-100 | `85` |
| integration_id | FK _INTEGRATION_STATUS | (links to existing 13 integrations, null for manual) |
| portal | Enum | `B2C`, `B2B`, `B2E`, `ALL` |
| portal_url | String | Carrier portal URL for manual pulls |
| priority | Enum | `HIGH`, `MEDIUM`, `LOW` |
| notes | Text | Free text |
| last_pull_at | ISO timestamp | |
| next_pull_due | ISO timestamp | |
| status | Enum | `ACTIVE`, `PLANNED`, `DEPRECATED` |
| created_at / updated_at | ISO timestamps | |

### Tab 2: `_SOURCE_TASKS` (Manual Pull Calendar + Workflow)
One row per recurring task or one-off migration.

| Field | Type | Purpose |
|-------|------|---------|
| task_id | UUID PK | |
| source_id | FK _SOURCE_REGISTRY | Links to the data source |
| task_type | Enum | `RECURRING_PULL`, `MIGRATION`, `SETUP`, `VALIDATION`, `ONE_TIME` |
| title | String | "Download Wellmark MAPD BoB report" |
| description | Text | Step-by-step instructions (idiot-proof) |
| owner_email | FK _USER_HIERARCHY | Assigned to |
| delegate_email | FK _USER_HIERARCHY | Delegated to (optional) |
| recurrence | Enum | `DAILY`, `WEEKLY`, `BIWEEKLY`, `MONTHLY`, `QUARTERLY`, `ANNUAL`, `ONCE` |
| recurrence_day | String | `MON` or `15` (day of month) |
| due_date | ISO date | Next due |
| last_completed_at | ISO timestamp | |
| last_completed_by | String (email) | |
| task_status | Enum | `PENDING`, `IN_PROGRESS`, `COMPLETE`, `OVERDUE`, `SKIPPED`, `BLOCKED` |
| calendar_event_id | String | Google Calendar event ID |
| slack_reminder | Boolean | Send Slack reminders |
| notes | Text | |
| created_at / updated_at | ISO timestamps | |

### Tab 3: `_SOURCE_HISTORY` (Audit Trail)
One row per completed data pull or sync event.

| Field | Type | Purpose |
|-------|------|---------|
| history_id | UUID PK | |
| source_id | FK _SOURCE_REGISTRY | |
| task_id | FK _SOURCE_TASKS | Null for automated |
| action_type | Enum | `MANUAL_PULL`, `AUTO_SYNC`, `VALIDATION`, `MIGRATION`, `ERROR` |
| completed_by | String | Email or "SYSTEM" |
| completed_at | ISO timestamp | |
| records_affected | Integer | |
| duration_seconds | Integer | |
| error_message | Text | If action_type=ERROR |
| notes | Text | |
| created_at | ISO timestamp | |

### Tab 4: `_SOURCE_METRICS` (Aggregated Analytics)
One row per carrier x domain x period.

| Field | Type | Purpose |
|-------|------|---------|
| metric_id | UUID PK | |
| period | String | `2026-03` or `2026-W10` |
| carrier_name | String | |
| product_line | String | |
| data_domain | String | |
| total_pulls | Integer | Successful pulls in period |
| total_errors | Integer | Errors in period |
| records_imported | Integer | Total records |
| automation_score | Integer 0-100 | |
| gap_trend | Enum | `IMPROVING`, `STABLE`, `DEGRADING` |
| created_at | ISO timestamp | |

---

## Portal Views

| Portal | Who Sees It | What They See |
|--------|-------------|---------------|
| **RIIMO** | Leadership (EXECUTIVE+) | Full admin: registry CRUD, task delegation, gap analysis, analytics, team workload, calendar view |
| **ProDash** | Service team (LEADER+) | B2C filtered: Medicare/Life/Annuity carrier status cards, "My Tasks" for assigned pulls, read-only registry |
| **SENTINEL** | DAVID team (LEADER+) | B2B filtered: revenue/producer data status, deal due diligence view, acquisition data readiness |

Single web app, query param `?view=riimo|prodash|sentinel` controls filtering + CRUD access.
Entitlements via `RAPID_CORE.getUserEntitlements()` gate access.

---

## Calendar + Workflow + Slack

**Layer 1 — `_SOURCE_TASKS` is ground truth.** Recurrence rules, due dates, ownership all live here.

**Layer 2 — Google Calendar.** On task create/update, sync to shared "RPI Data Pulls" calendar. Team sees their obligations. Uses `mcp__google-calendar__create-event`.

**Layer 3 — Slack notifications.**
- Daily 7 AM: per-owner DM with today's due/overdue pulls
- Weekly Monday: JDM summary (U09BBHTN8F2) with team-wide gap status
- On overdue: escalation to owner's leader via `_COMPANY_STRUCTURE`
- On completion: brief confirmation to owner

**Layer 4 — Auto-completion.** For GREEN (automated) sources, the registry reads `_INTEGRATION_STATUS` and auto-marks corresponding tasks COMPLETE. Manual sources require user click.

---

## How This Fits the RAPID_IMPORT Roadmap

| Existing Stream | Impact |
|----------------|--------|
| **Stream 6A (Documentation)** | REPLACED. The live registry IS the documentation. Kill the planned static docs. |
| **Stream 6D (Integration Dashboard)** | SUBSUMED. RAPID_IMPORT's `INTEGRATION_DASHBOARD.html` stays as internal diagnostic. ATLAS becomes the authoritative cross-platform dashboard. |
| **Stream 7 (Validation APIs)** | TRACKED. Each validation service (PhoneValidator, NeverBounce, USPS) becomes a row in `_SOURCE_REGISTRY` with `data_domain: VALIDATION`. |
| **Stream 8 (Comms Intake)** | TRACKED. Each comm source (Twilio, SendGrid, Meet, Chat) is a row. Already GREEN via `_INTEGRATION_STATUS` link. |
| **Stream 6B (Comm Archives)** | TRACKED. Jira archive, GHL legacy become RED rows until imported, then YELLOW/GREEN. |
| **Stream 6C (Carrier Integrations)** | THE ROADMAP. DTCC, Schwab, Gradient, Blue Button start as RED `target_method: API_FEED` rows. As JDM completes vendor enrollments and we build integrations, they evolve to GREEN. The registry IS the carrier integration roadmap. |
| **Stream 5 (CoF)** | TRACKED. CoF policy details = RED row, blocked on CoF response. |

**Net effect: Streams 6A and 6D collapse into the ATLAS App. Streams 5, 6B, 6C, 7, 8 become rows in the registry rather than separate roadmap items.**

---

## Project Structure

```
~/Projects/RAPID_TOOLS/ATLAS/
  .clasp.json
  appsscript.json              -- DOMAIN access, RAPID_CORE library, executionApi
  Code.gs                      -- doGet(), include_(), ForUI wrappers, routing
  ATLAS_Config.gs              -- Constants, enums, tab names
  ATLAS_Registry.gs            -- _SOURCE_REGISTRY CRUD
  ATLAS_Tasks.gs               -- _SOURCE_TASKS management, recurrence engine, due dates
  ATLAS_History.gs             -- _SOURCE_HISTORY logging
  ATLAS_Analytics.gs           -- Metrics aggregation, gap analysis, automation scoring
  ATLAS_Triggers.gs            -- Scheduled: overdue check, metrics, Slack digests
  ATLAS_Calendar.gs            -- Google Calendar sync
  ATLAS_Slack.gs               -- Slack notifications
  ATLAS_DevTools.gs            -- DEBUG_Ping, SETUP_, TEST_, FIX_ functions
  Index.html                   -- Main UI (all views: RIIMO/ProDash/SENTINEL)
  _CSS_VARS.html               -- CSS variables (dark theme)
  _SHARED_UI.html              -- Shared UI components
  CLAUDE.md
  .claude/                     -- Hookify symlinks
```

---

## Changes to Other Projects

| Project | File | Change |
|---------|------|--------|
| **RAPID_CORE** | `CORE_Database.gs` | Add 4 tabs to TABLE_ROUTING + TAB_SCHEMAS |
| **RAPID_CORE** | `CORE_Entitlements.gs` | Register ATLAS module in MODULES + TOOL_SUITES |
| **RIIMO** | `RIIMO_Core.gs` | Add ATLAS to PROJECT_REGISTRY with deployId |
| **RAPID_API** | `API_SETUP.gs` | Add write routes for 4 new tabs |
| **_RPI_STANDARDS** | `setup-hookify-symlinks.sh` | Add ATLAS to project list |
| **_RPI_STANDARDS** | `MONITORING.md` / `POSTURE.md` | Add ATLAS to tracking |

RAPID_IMPORT: **NO CHANGES.** ATLAS reads `_INTEGRATION_STATUS` as-is.

---

## Seed Data Strategy

Initial registry population from existing codebase:

1. **13 automated integrations** from `IMPORT_IntegrationStatus.gs` INTEGRATIONS array -> GREEN rows
2. **230+ carrier aliases** from `CORE_Normalize.gs` CARRIER_ALIASES -> canonical carrier list
3. **4 commission grids** (MAPD, MedSup, Life, Annuity) -> carrier x product rows
4. **Known manual flows** (from RAPID_IMPORT CLAUDE.md + roadmap) -> YELLOW/RED rows
5. **Future integrations** (DTCC, Schwab, Gradient, Blue Button) -> RED rows with target state

Estimated: ~150-200 initial registry rows covering all known carrier x product x domain combinations.

---

## Implementation Phases

| Phase | What | Effort | Depends On |
|-------|------|--------|------------|
| **0: Foundation** | New GAS project, git, CLAUDE.md, .clasp.json, DEBUG_Ping | 1 hr | JDM: GCP link + first auth |
| **1: Data Model** | RAPID_CORE schemas + TABLE_ROUTING, SETUP functions, seed data | 1-2 hrs | Phase 0 |
| **2: Backend** | Registry CRUD, task management, history logging, analytics | 2-3 hrs | Phase 1 |
| **3: Frontend (RIIMO view)** | Full admin UI — registry grid, task board, gap dashboard, analytics | 3-4 hrs | Phase 2 |
| **4: Portal Views** | ProDash + SENTINEL filtered views, entitlements gating | 1-2 hrs | Phase 3 |
| **5: Calendar + Slack** | Google Calendar sync, daily/weekly Slack digests, overdue alerts | 1-2 hrs | Phase 2 |
| **6: Seed + Launch** | Populate all known sources, register in RIIMO, deploy | 1-2 hrs | Phases 3-5 |

**Total: ~10-16 hours across 3-4 sessions.**

---

## Verification

1. **Registry CRUD**: Create/edit/delete source entries via UI, verify in RAPID_MATRIX
2. **Task workflow**: Create recurring task, verify due date computation, mark complete, check history log
3. **Gap analysis**: Seed mix of GREEN/YELLOW/RED sources, verify dashboard renders correctly
4. **Portal filtering**: Access with `?view=prodash` vs `?view=riimo`, verify correct data scope
5. **Calendar sync**: Create task with recurrence, verify Google Calendar event appears
6. **Slack digest**: Run daily digest function, verify per-owner DMs arrive
7. **Auto-completion**: Verify GREEN sources with active `_INTEGRATION_STATUS` rows auto-mark complete
8. **Entitlements**: Verify LEADER+ sees ProDash/SENTINEL views, EXECUTIVE+ sees RIIMO admin
9. **Cross-project**: Verify RIIMO sidebar shows ATLAS, opens correct URL

---

## Hookify Rules

### #LetsPlanIt (ALREADY LIVE)
`hookify.intent-plan-mode.local.md` exists in `_RPI_STANDARDS/hookify/`. Triggers on `#LetsPlanIt` and plan-related phrases. Switches to HIGH thinking for architecture/planning work.

### #LetsRockIt (NEW — Plan Execution Trigger)
Create `hookify.intent-execute-plan.local.md` in `_RPI_STANDARDS/hookify/`:

**Catchphrase: `#LetsRockIt`** — signals "plan approved, go build"

Pairs with `#LetsPlanIt` (plan) and `#SendIt` (deploy):
- `#LetsPlanIt` = HIGH thinking, plan mode, architecture
- `#LetsRockIt` = MEDIUM thinking, exit plan mode, execute the approved plan
- `#SendIt` = deploy protocol (6-step)

Rule spec:
```yaml
name: intent-execute-plan
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#LetsRockIt|#letsrockit|let'?s\s+rock|rock\s+it|execute\s+the\s+plan|plan\s+approved|green\s+light|go\s+build)
```

Message:
```
**PLAN EXECUTION TRIGGERED (#LetsRockIt)**

Plan approved. Switching to MEDIUM thinking for execution.

1. Exit Plan Mode (ExitPlanMode)
2. Execute the approved plan file sequentially
3. Spawn parallel agents where phases are independent
4. Report results at each milestone
5. When complete: ask JDM if ready for #SendIt (deploy)

The plan already decided the *what*. Now execute the *how*.
```

**Also update:**
- `_RPI_STANDARDS/CLAUDE.md` Communication Style table — add `#LetsRockIt` row
- `~/.claude/CLAUDE.md` Communication Style table — add `#LetsRockIt` row
- `_RPI_STANDARDS/hookify/` symlinks propagated to all 18+ projects
- Intent Rules list in CLAUDE.md Operating System section — add `intent-execute-plan`
