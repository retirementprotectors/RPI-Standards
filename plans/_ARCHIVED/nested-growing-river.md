# Operation Virus Kill: Unified Org Data Architecture

## Context

7 parallel audit agents scanned every project across the platform and found org/hierarchy/permission data scattered in **6 hardcoded maps across 4 projects**, **3 conflicting data sources**, **wrong data in _USER_HIERARCHY**, and **UI bugs ignoring permissions**. JDM declared: "We need a SINGLE UI INPUT SOURCE and a SINGLE MATRIX SOURCE OF TRUTH. Everything else feeds off the MATRIX."

This plan eliminates ALL ambiguity by adding missing columns, building a universal resolver, killing every hardcoded map, and fixing wrong data.

---

## Phase 1: Schema + Data (Foundation)

### Step 1.1: Add columns to `_USER_HIERARCHY`

New columns added to the RIGHT of existing columns (no index shift):

| Column | Default | Populated From |
|--------|---------|---------------|
| `slack_id` | Populate from existing maps | Kills 5 hardcoded Slack maps |
| `phone` | blank | JDM to provide |
| `job_title` | Populate (CEO, COO, etc.) | From CLAUDE.md team list |
| `aliases` | JSON[] | From CC/MCP-Hub name variant maps |
| `personal_email` | blank | Known for some |
| `location` | blank | Future |
| `npn` | blank | Future |
| `hire_date` | blank | Future |
| `google_chat_id` | Populate from Workspace | For Google Chat DMs / RPI Messenger |

### Step 1.2: Fix wrong data in `_USER_HIERARCHY`

| User | Field | Current | Fix To |
|------|-------|---------|--------|
| Nikki | hierarchy_level | UNIT | DIVISION |
| Vinnie | hierarchy_level | UNIT | DIVISION |
| Aprille | hierarchy_level | UNIT | DIVISION |
| Vinnie | role_template_id | readonly | admin |
| Matt | role_template_id | readonly | admin |
| Susan | role_template_id | sales | service |

### Step 1.3: Add `slack_channel_id` to `_COMPANY_STRUCTURE`

| entity_id | slack_channel_id |
|-----------|-----------------|
| MEDICARE (SALES) | From SLACK_CHANNEL_MEDICARE_SALES Script Property |
| RETIREMENT (SALES) | From SLACK_CHANNEL_RETIREMENT_SALES |
| MEDICARE_SVC (SERVICE) | From SLACK_CHANNEL_MEDICARE_SERVICE |
| RETIREMENT_SVC (SERVICE) | From SLACK_CHANNEL_RETIREMENT_SERVICE |

### Step 1.4: Populate `_COMPANY_STRUCTURE.manager_email` for units

All units currently blank. Populate with division leaders.

### Step 1.5: Populate `employee_profile` enrichments

Add `roadmap_doc_id` and `team_folders` from MCP-Hub's hardcoded data for Matt, Nikki, Vinnie, Jason, Aprille.

**Method:** All via gdrive MCP sheet writes. No code deploys needed.

---

## Phase 2: RAPID_CORE — resolveUser() + Column Access

### Step 2.1: Add `resolveUser()` to CORE_Entitlements.gs

New function — universal name/alias resolver:
- Input: any string (email, first name, last name, alias, slack_id)
- Reads _USER_HIERARCHY (active rows only)
- Match priority: email > slack_id > first+last > aliases[] > first_name fuzzy
- Returns: full user row object or null

### Step 2.2: Update `getUserHierarchy()`

Return new columns: slack_id, phone, job_title, aliases, personal_email, location, npn, hire_date.

### Step 2.3: Update `getMyProfile()`

Include new columns in profile response.

### Step 2.4: Export new function

Add `resolveUser` to RAPID_CORE exports in Code.gs.

### Step 2.5: Deploy RAPID_CORE library

Push + version. All consuming projects auto-update (library reference).

**Files:** `RAPID_CORE/CORE_Entitlements.gs`, `RAPID_CORE/Code.gs`

---

## Phase 3: Kill Hardcoded Maps (6 projects)

### Step 3.1: RIIMO — Kill `RIIMO_SLACK_MAP`
**File:** `RIIMO/RIIMO_MyRPI.gs`
Replace hardcoded map lookup with slack_id from already-loaded UH row.

### Step 3.2: CC — Kill `SLACK_TEAM_MAP`
**File:** `RPI-Command-Center/CC_SlackDigest.gs`
Replace with `RAPID_CORE.resolveUser(ownerName).slack_id`.

### Step 3.3: CC — Kill `ROADMAP_OWNER_MAP` + `CC_ROADMAP_PEOPLE`
**File:** `RPI-Command-Center/CC_AutoRoute.gs`, `CC_Config.gs`
Replace with `RAPID_CORE.resolveUser(ownerName)` → `employee_profile.roadmap_doc_id`.

### Step 3.4: MCP-Hub — Kill `RPI_TEAM` + `TEAM_FOLDERS`
**File:** `MCP-Hub/rpi-business-mcp/src/meeting-tools.js`
Add `GET /team` endpoint to RAPID_API. MCP-Hub calls on startup, caches.
**Also:** `RAPID_API/API_User.gs` — add `listTeamRoster_()`.

### Step 3.5: IMPORT — Kill leader email Script Properties
**File:** `RAPID_IMPORT/IMPORT_Approval.gs`
`resolveLeaderEmail_()` reads `_COMPANY_STRUCTURE.manager_email` via RAPID_CORE.

### Step 3.6: IMPORT — Kill Slack channel Script Properties
**File:** `RAPID_IMPORT/IMPORT_Approval.gs`
`resolveRoutedSlackChannel_()` reads `_COMPANY_STRUCTURE.slack_channel_id`.

**Deploy order:** RAPID_CORE first (Phase 2), then all consumers in parallel (Phase 3).

---

## Phase 4: Fix RIIMO Sidebar Permissions

### Step 4.1: Dynamic sidebar respects entitlements
**File:** `RIIMO/Index.html` — `renderSidebar()`
Initial static HTML shows all modules. Fix: render only Dashboard + loading skeleton until dynamic JS replaces it based on user's actual entitlements.

### Step 4.2: LEADER+ profile switcher
MyRPI profile switcher already uses `validateScopedAdmin`. Ensure LEADER-level users see their unit members in the dropdown (not just EXECUTIVE+).

---

## Phase 5: CC _ACTION_ITEMS FK

### Step 5.1: Add `owner_email` column
Via gdrive MCP. Populate by resolving existing free-text `owner` names to emails.

### Step 5.2: Update CC_ActionItems.gs
Use `owner_email` for lookups. Keep `owner` display name for UI.

---

## Execution Order (Critical Path)

| # | Phase | Project(s) | Type | Depends On |
|---|-------|-----------|------|------------|
| 1 | Schema + data fixes (columns, wrong data, enrichments) | Sheets (gdrive) | Data | Nothing |
| 2 | resolveUser() + column access | RAPID_CORE | Code + library deploy | Phase 1 |
| 3 | Kill RIIMO_SLACK_MAP + fix sidebar | RIIMO | Code + deploy | Phase 2 |
| 4 | Kill CC maps + ACTION_ITEMS FK | CC | Code + deploy | Phase 2 |
| 5 | Add /team API endpoint + kill IMPORT maps | RAPID_API, RAPID_IMPORT | Code + deploy | Phase 2 |
| 6 | Booking pages (Calendly-style) | RIIMO | Code + deploy | Phase 3 |
| 7a | Kill MCP-Hub hardcoded maps | MCP-Hub | Code + npm restart | Phase 5 |
| 7b | Cascade verify: PRODASHX + SENTINEL | PRODASHX, sentinel-v2 | Verify + minor fixes | Phase 2 |
| 8 | Documentation sweep (ALL CLAUDE.md + MEMORY + Standards) | All projects | Docs | All above |

Phases 3, 4, 5, 7b can run in **parallel** after Phase 2.
Phase 6 after Phase 3. Phase 7a after Phase 5. Phase 8 is final.

**Total:** 6 GAS deploys + 1 MCP restart + 1 booking page feature + full docs sweep

---

## Verification

1. `RAPID_CORE.resolveUser("Shaner")` → returns Shane's full row with slack_id
2. `RAPID_CORE.resolveUser("U09BBHTN8F2")` → returns Josh's row
3. MyDropZone "Send to Slack" → uses slack_id from MATRIX
4. CC Slack Digest → routes DMs via resolveUser, no hardcoded map
5. CC AutoRoute → resolves roadmap owner via resolveUser + employee_profile
6. RIIMO sidebar → USER sees only Dashboard + assigned modules
7. RIIMO sidebar → LEADER sees profile switcher for unit members
8. IMPORT approval → routes to leader via _COMPANY_STRUCTURE.manager_email
9. MCP-Hub → loads team from RAPID_API /team endpoint

---

## Phase 6: Booking Pages (Calendly-Style)

### Step 6.1: Public booking endpoint in RIIMO
Add a lightweight public-facing page served by RIIMO's `doGet()` with a `?book=EMAIL` parameter.
- Reads user's `calendar_booking_types` + `meet_room.meet_link` from `_USER_HIERARCHY.employee_profile`
- Displays: person name, photo, booking type cards (name + duration)
- Each card opens Google Calendar pre-filled event URL with duration + meet link + person as attendee
- Clean, mobile-friendly design — this is the link team members share with clients/prospects
- URL format: `RIIMO_URL?book=vince@retireprotected.com` or `RIIMO_URL?book=Vinnie` (resolved via aliases)

### Step 6.2: Booking link in MyDropZone
Each user's MyDropZone section shows their booking page URL with a copy button.
The URL is auto-generated from their email: `https://[RIIMO_DEPLOY]/exec?book=EMAIL`

### Step 6.3: Google Calendar Appointment Schedules (future enhancement)
The booking page is step 1. When Google Calendar API supports programmatic Appointment Schedule creation, we can upgrade each booking type to a true availability-aware schedule. For now, the pre-filled Calendar links are the MVP.

---

## Phase 7: Permission Cascade (RIIMO → Portals → Apps/Modules)

### Step 7.1: RIIMO (B2E) — Source of Admin Truth
Already handles org admin. After Phases 1-5:
- Sidebar dynamically reflects entitlements
- Admin panel creates/manages users with all new fields
- MyRPI shows all profile data from MATRIX
- LEADER+ profile switcher works for unit scope

### Step 7.2: PRODASHX (B2C) — Cascade permissions
**File:** `PRODASHX/Code.gs`, `PRODASHX/Scripts.html`
- Sidebar already reads `RAPID_CORE.getEntitlementsForPlatform(email, 'PRODASH')`
- Verify new columns (slack_id, aliases, job_title) flow through `getMyProfile()`
- MyRPI in PRODASHX (when built) reads same MATRIX data
- Remove legacy `_PERMISSIONS` tab fallback in Code.gs (~line 825)

### Step 7.3: SENTINEL (B2B) — Cascade permissions
**File:** `sentinel-v2/SENTINEL_Permissions.gs`
- Already clean — delegates to `RAPID_CORE.getEntitlementsForPlatform(email, 'SENTINEL')`
- Verify new columns flow through
- No hardcoded maps to kill (already clean per audit)

### Step 7.4: Apps/Modules — Inherit from Portal
Apps embedded in Portals (Command Center, DEX, C3, DAVID-HUB) inherit the Portal's auth context. After CC maps are killed (Phase 3), CC reads from MATRIX via resolveUser. DEX and C3 already use RAPID_CORE entitlements. DAVID-HUB has `ADMIN_DOMAINS` — leave for now (domain-based auth is valid for external-facing B2B app).

---

## Phase 8: Documentation Sweep

### Step 8.1: Global CLAUDE.md
- Update Key Team table with job_title references
- Update Org Structure section to reference `_USER_HIERARCHY` as sole source
- Add `aliases` concept to terminology
- Remove any hardcoded team references that should point to MATRIX
- Add `resolveUser()` to Available MCP Tools / patterns section

### Step 8.2: Project CLAUDE.md files (all 6 deployed projects)
- **RAPID_CORE** — Document resolveUser(), new columns, export list
- **RIIMO** — Update key functions table, version, deployment ID
- **CC** — Update to reflect all maps killed, new data source patterns
- **RAPID_API** — Document new /team endpoint
- **RAPID_IMPORT** — Document leader/channel routing now from MATRIX
- **MCP-Hub** — Document team roster from API, remove hardcoded map references

### Step 8.3: _RPI_STANDARDS reference docs
- Update `STANDARDS.md` if org/permission rules changed
- Update `MONITORING.md` with new health checks for new columns
- Update `POSTURE.md` with new verification items

### Step 8.4: MEMORY.md
- Add resolveUser() pattern
- Add aliases column knowledge
- Add google_chat_id column knowledge
- Note the hardcoded map elimination pattern for future sessions

---

## Risk Mitigation

- **RAPID_CORE is a library** — deploy updates ALL consumers. Test resolveUser via execute_script before deploying.
- **Add columns to RIGHT** of existing columns — no index shifts, no breaking changes.
- **Phase 2 before Phase 3** — resolveUser exists and works before we delete any hardcoded maps.
- **MCP-Hub is Node.js** — requires npm restart, not GAS deploy.
