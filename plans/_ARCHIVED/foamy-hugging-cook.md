# Portal Standardization — Implementation Plan

## Context

All 3 RPI portals (PRODASHX, SENTINEL, RIIMO) have divergent UI/UX — different sidebar structures, inconsistent admin panels, My RPI in wrong locations, and PRODASHX still on light mode. JDM approved a whiteboard spec (`_RPI_STANDARDS/whiteboard/portal-standardization.html`) that defines the target: dark mode everywhere, spinning-icon sidebar, standardized admin tabs, and consistent My RPI with a new Meetings tab. This plan executes that vision.

**Gold standard:** RIIMO's admin (8 tabs, full team/pipeline/module CRUD) + the whiteboard's sidebar design (spinning icons, collapsible sections, module vs app distinction).

---

## Phase 0: Foundation (Shared Assets + Docs)

**Goal:** Build the shared CSS design system and reference docs BEFORE touching any portal.

### 0A: Shared CSS — `PortalStandard.html`

Create master file at `_RPI_STANDARDS/reference/portal/PortalStandard.html`, then copy into each GAS project (GAS has no cross-project includes).

Contents:
- Dark mode base: `--bg-deepest`, `--bg-dark`, `--bg-card`, `--bg-surface`, `--text-primary`, `--text-secondary`, `--border-subtle`
- Portal accent override pattern: each portal sets `--portal`, `--portal-glow`, `--portal-accent`
- Sidebar styles: `.sidebar`, `.sidebar-section`, `.section-icon-btn`, spinning icon keyframes, `.nav-item`, `.pipeline-item`, `.module-item`, `.app-item`, `.admin-item`
- Admin tab bar: `.admin-tabs`, `.admin-tab`, `.admin-tab.active`, `.admin-content`
- My RPI panel: `.myrpi-tabs`, profile card, section styles
- Standard components: cards, tables, forms, buttons, modals (dark variants)

### 0B: Documentation — `reference/portal/`

Create:
- `reference/portal/PORTAL_STANDARDIZATION.md` — The spec: sidebar order, admin tab rules, My RPI tab rules, color system, module vs app distinction
- `reference/portal/NAVIGATION_ARCHITECTURE.md` — Section types (Pipeline/Module/App/Admin), routing, icon conventions, collapse behavior

### 0C: Backend Pattern Doc

Document the standard `*_OrgAdmin.gs` wrapper pattern (based on RIIMO_OrgAdmin.gs) that PRODASHX and SENTINEL will implement.

**Files created:** ~3 new files in `_RPI_STANDARDS`, 0 portal changes
**Parallelizable:** All 3 workstreams independent

---

## Phase 1: RIIMO (Validate Pattern)

**Goal:** Apply the standard to the gold standard portal first. Smallest risk, proves the pattern.

### 1A: Sidebar Restructure
- **File:** `RIIMO/Index.html` (sidebar rendering ~lines 1240-1310)
- Logo click = Dashboard (remove Dashboard nav item)
- Reorder: Pipelines FIRST, then RAPID Tools + Tool Suites (module sections), then Apps section (CAM, DEX, C3, CEO Dashboard, Command Center with orange/dashed/external-icon treatment)
- Admin pinned bottom (flat button, already correct)
- All sections default collapsed + spinning icon animation
- Include `PortalStandard.html` via `<?!= include('PortalStandard') ?>`

### 1B: Admin Tab Reorder
- Already has all 8 tabs — just reorder first 3 to match standard:
  - Tab 1: Team Management (current PERMISSIONS tab)
  - Tab 2: Pipeline Config (current PIPELINE_CONFIG tab)
  - Tab 3: Module Config (extract module permissions from PERMISSIONS into own tab, or keep combined)
  - Tab 4-8: Portal-specific (On-Boarding, Off-Boarding, Job Templates, Task Templates, Error Log)

### 1C: My RPI — Add Tabs + Meetings
- **File:** `RIIMO/MyRPI.html`
- Convert from scrolling sections to tabbed UI
- Standard tabs: Profile | MyDropZone | Meetings (NEW) | Permissions
- Portal-specific tabs: Onboarding | Job Description
- Build Meetings tab: meeting type CRUD + availability grid (store in `employee_profile` JSON)

**Deploy:** 6-step for RIIMO
**Files modified:** ~3 files (Index.html, MyRPI.html, + new PortalStandard.html)

---

## Phase 2: SENTINEL v2 (Port Pattern)

**Goal:** Bring SENTINEL up from the most behind to standardized.

### 2A: Sidebar Restructure
- **File:** `sentinel-v2/Index.html` (lines 4811-4892)
- Rewrite `renderSentinelSidebar()`:
  - Logo click = Dashboard
  - Pipelines FIRST (already first — good)
  - Deal Management + Analysis + Market Intel = Module sections (purple icons)
  - Apps section: DAVID-HUB, CAM, Proposal Maker (orange/dashed/external)
  - REMOVE "Personal > My RPI" from sidebar (moves to top-right)
  - Admin pinned bottom
  - All collapsed + spinning icons
- Include `PortalStandard.html`
- Set `--portal: #3CB371` (DAVID green)

### 2B: Admin Section Overhaul
- **New file:** `SENTINEL_OrgAdmin.gs` — thin wrapper around RAPID_CORE (pattern from RIIMO_OrgAdmin.gs)
  - `getAllUsers()`, `saveUser()`, `deleteUser()`, `updateUserModulePermissions()` — all filtered to SENTINEL platform
- **File:** `sentinel-v2/Index.html` admin section (lines 2144-2268)
- Rewrite from 3 tabs to 6 tabs:
  - Tab 1: Team Management (NEW — port from RIIMO)
  - Tab 2: Pipeline Config (NEW — port from RIIMO, SENTINEL pipelines only)
  - Tab 3: Module Config (NEW — port from RIIMO, SENTINEL modules only)
  - Tab 4: Settings (existing)
  - Tab 5: Integrations (existing)
  - Tab 6: Database (existing)

### 2C: My RPI — Move + Enhance
- Move from sidebar to top-right avatar + name
- Add top user bar (port from RIIMO pattern)
- **New file:** `SENTINEL_MyRPI.html` include
- Tabs: Profile | MyDropZone | Meetings | Permissions

**Deploy:** 6-step for sentinel-v2
**Files modified:** ~4 existing + 2 new (SENTINEL_OrgAdmin.gs, SENTINEL_MyRPI.html, PortalStandard.html copy)

---

## Phase 3: PRODASHX (Dark Mode + Restructure)

**Goal:** Convert the largest portal from light to dark + apply all standards. Highest effort.

### 3A: Dark Mode Conversion (BLOCKING — do first)
- **File:** `PRODASHX/Styles.html` (4,093 lines) — convert all CSS variables from light to dark
- **File:** `PRODASHX/Index.html` — fix any inline light-mode styles
- **File:** `PRODASHX/Scripts.html` — grep for hardcoded colors (#fff, #000, rgb, background-color, etc.)
- Include `PortalStandard.html`, set `--portal: #3d8a8f` (ProDashX teal)
- Key conversions: body bg white→dark, cards white→card-dark, text dark→light, borders gray→subtle

### 3B: Sidebar Rewrite (after 3A)
- **File:** `PRODASHX/Scripts.html` (renderSidebar at line 7337)
- Logo click = Dashboard (REMOVE Dashboard nav item)
- Pipelines FIRST (extract from Workspace section)
- Workspace (Clients, Accounts, Comms Hub) = Module section
- Sales Centers = Module section
- Service Centers = Module section
- C3 section = Module section
- Apps section: QUE-Medicare, CAM, C3 (orange/dashed/external)
- Admin pinned bottom
- All collapsed + spinning icons

### 3C: Admin Section Overhaul (parallel with 3B)
- **New file:** `PRODASH_OrgAdmin.gs` — thin wrapper around RAPID_CORE
- **File:** `PRODASHX/Index.html` (admin section lines 3447-3683)
- Convert from card layout to tabbed UI:
  - Tab 1: Team Management (refactor existing `loadTeamEntitlements()`)
  - Tab 2: Pipeline Config (refactor existing pipeline admin)
  - Tab 3: Module Config (refactor existing entitlements)
  - Tab 4: Settings (existing system status)
  - Tab 5: C3/BOB Matrix (existing PRODASHX-specific)

### 3D: My RPI Enhancement
- Already in correct position (top-right) — keep
- Convert from scrolling cards to tabbed UI
- **New file:** `PRODASH_MyRPI.html` (extract from Scripts.html lines 13750+)
- Tabs: Profile | MyDropZone | Meetings | Permissions | My Team | Documents

**Deploy:** 6-step for PRODASHX
**Files modified:** ~5 existing + 2 new (PRODASH_OrgAdmin.gs, PRODASH_MyRPI.html, PortalStandard.html copy)

---

## Phase 4: Meetings Tab (Cross-Portal)

**Goal:** Build the new Meetings feature once, deploy to all 3.

### Data Model (in `employee_profile` JSON, `_USER_HIERARCHY`)
```
meeting_types: [{ id, name, duration_minutes, location_type, description }]
availability: { [meeting_type_id]: { monday: [{start,end}], tuesday: [...], ... } }
```

### Backend
- Add `updateMeetingTypes(userId, types)` + `updateAvailability(userId, availability)` to each portal's `*_MyRPI.gs`
- These write to the `employee_profile` JSON merge pattern (already exists in RIIMO)

### Frontend
- Meeting type CRUD cards (add/edit/delete types)
- Availability grid: 7-day x time-slot toggles per meeting type
- Day selector: Mon-Sun with time slot chips (9a, 10a, 11a, 12p, 1p, 2p, 3p, 4p, 5p)
- Build in RIIMO first, port pattern to SENTINEL + PRODASHX

**Deploy:** All 3 portals

---

## Phase 5: Polish + Documentation

- Cross-portal screenshot audit (visual consistency check)
- Verify all admin functions work (add user, edit user, pipeline config, module config)
- Verify My RPI tabs work across all 3
- Verify sidebar collapse/expand + navigation in all 3
- Verify entitlements gating (USER sees no admin, LEADER sees scoped admin, OWNER sees all)
- Update `reference/portal/` docs with final state
- Update each portal's CLAUDE.md with new file references
- Update whiteboard HTML if any design decisions changed during build

---

## Execution Order + Dependencies

```
Phase 0 (Foundation)     ← No dependencies, do first
    |
Phase 1 (RIIMO)          ← Depends on Phase 0 (needs PortalStandard.html)
    |
Phase 2 (SENTINEL)       ← Depends on Phase 0 (can run parallel with Phase 1 if needed)
    |
Phase 3 (PRODASHX)       ← Depends on Phase 0. 3A (dark mode) blocks 3B/3C/3D
    |
Phase 4 (Meetings)       ← Depends on Phase 1 My RPI tabs being done. Can start after Phase 1
    |
Phase 5 (Polish)         ← After all phases complete
```

**Parallelization within phases:** Each phase's workstreams (A/B/C) are parallelizable via sub-agents unless noted as blocking.

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Shared CSS delivery | Copy per project, master in `_RPI_STANDARDS` | GAS has no cross-project include |
| Admin UI style | **Whiteboard mockup style** (clean dark cards + checkmarks) | JDM chose this over replicating RIIMO's current UI verbatim |
| Admin backend | Portal-specific `*_OrgAdmin.gs` wrapping RAPID_CORE | ui* wrappers need project-local Session, portal-specific tabs need local code |
| Meeting types storage | `employee_profile` JSON in `_USER_HIERARCHY` | User-scoped data, RIIMO already has this pattern, no new MATRIX tab needed |
| Sidebar rendering | Portal-specific functions, shared CSS classes | Different content per portal, same visual structure |
| Dark mode approach | PortalStandard.html base + portal override | Cascade: shared dark base, portal accents on top |
| Admin tab order | Team Mgmt > Pipeline Config > Module Config > portal-specific | Standardized first 3, flexibility after |
| App vs Module classification | Apps = separate GAS projects (QUE, CAM, C3, DAVID-HUB, etc.) / Modules = native .gs files in that portal | JDM confirmed: if it has its own backend+frontend GAS project, it's an App |
| Deploy strategy | Deploy per phase, autonomously | RIIMO after Phase 1, SENTINEL after Phase 2, PRODASHX after Phase 3 |

## Pre-Flight Status (Verified 2026-03-06)

| Portal | Git | Clasp | Deploy ID | Current Version |
|--------|-----|-------|-----------|-----------------|
| RIIMO | Clean | Valid | `AKfycbw47EuRk5pba7ejwQ1CysSUteRIPefPIesRYDxgwWVlsBXX1mqNqnC05j30NbF90Mo` | v3.10.1 @85 |
| SENTINEL | Clean | Valid | `AKfycbzLXgIoIda9X7IKGk89D3-nD_bf1APt7W6W5muq7dZXXCUKQU0w3erbKJ9P5WAxgIcl` | v3.9.1 @34 |
| PRODASHX | Clean | Valid | `AKfycbxL_QG4K3odZdikeuLQ8pZv8zZZVhKRXCyTUS3ic01I7fUq6QoXEkcRc08zEsUlLbDBsQ` | v3.5 @171 |
| _RPI_STANDARDS | 1 untracked (whiteboard/) | N/A | N/A | N/A |

---

## Verification

After each phase deploy:
1. Open portal in incognito → verify dark mode renders correctly
2. Click logo → verify Dashboard loads
3. Click each sidebar section → verify spinning icon + expand/collapse
4. Check Admin → verify all 3 standard tabs load data
5. Check My RPI → verify tabbed UI with correct tabs
6. Test as OWNER, LEADER, USER → verify entitlement gating
7. `clasp deployments | grep @VERSION` → verify deploy version matches
