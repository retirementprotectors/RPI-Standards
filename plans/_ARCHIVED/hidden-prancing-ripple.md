# Portal Standardization Phase 6 — Portal Overhaul

## Context

JDM did a comprehensive walkthrough of all 3 portals and identified ~50 items across admin panels, sidebars, and My RPI. Phase 5 (just shipped) fixed shared admin functions, pinned admin to sidebar bottom, and added PRODASHX nav items. Phase 6 is the cleanup + rebuild that brings everything to production quality.

This is broken into 4 sub-phases: A (cleanup), B (admin rebuild), C (My RPI), D (sidebar architecture). A-C are executable now. D requires business decisions first.

---

## Phase 6A: Quick Wins + Cleanup

> Kill dead code, fix broken things, align spacing. Pure cleanup, no new features.

### 6A-1: Kill Dead Admin Tabs

| Portal | Tab to Kill | Why |
|--------|-----------|-----|
| RIIMO | Error Log | Broken, irrelevant |
| RIIMO | On-Boarding | It's a pipeline module, not admin config |
| RIIMO | Off-Boarding | Same |
| SENTINEL | Settings | Useless |
| SENTINEL | Integrations | Useless |
| SENTINEL | Database | Useless |
| SENTINEL | Team Mgmt | RIIMO-only (leaders have RIIMO access) |
| PRODASHX | Settings | Useless |
| PRODASHX | C3/BOB Assignments | Broken/obsolete |
| PRODASHX | Org Structure | Useless in PRODASHX |
| PRODASHX | Team Mgmt | RIIMO-only |

**Files:**
- `RIIMO/Index.html` — Remove admin tab definitions + content panels for Error Log, On-Boarding, Off-Boarding
- `SENTINEL/Index.html` — Remove Settings, Integrations, Database, Team Mgmt tabs + content
- `PRODASHX/Index.html` + `Scripts.html` — Remove Settings, C3/BOB, Org Structure, Team Mgmt tabs + content
- `SENTINEL/SENTINEL_OrgAdmin.gs` — Remove/stub Team Mgmt ForUI functions
- `PRODASHX/PRODASH_OrgAdmin.gs` — Remove/stub Team Mgmt ForUI functions

### 6A-2: Kill Dead Sidebar Items

| Portal | Item to Kill | Why |
|--------|-------------|-----|
| RIIMO | Data Maintenance pipeline | Replaced by ATLAS |
| RIIMO | Security pipeline | Replaced by Operating System |
| RIIMO | Tech Maintenance pipeline | Replaced by OS/ATLAS |
| PRODASHX | QUE-Medicare from Apps section | It's already in Sales Centers as a module. The Apps listing is a duplicate pointing to the same internal page. |
| PRODASHX | Comms Hub from Workspace | Kill frontend for now, backend stays. Tag as Next Phase. |

**Additions:**
| Portal | Item to Add | Where |
|--------|-----------|-------|
| RIIMO | ATLAS | Apps section |
| SENTINEL | DEX | Apps section |
| SENTINEL | ATLAS | Apps section |
| PRODASHX | ATLAS | Apps section |

**Files:**
- `RIIMO/Index.html` — renderSidebar() pipeline filtering + apps array
- `SENTINEL/Index.html` — renderSentinelSidebar() apps array
- `PRODASHX/Scripts.html` — renderSidebar() items arrays
- Confirm ATLAS/DEX/OS coverage before removing pipelines (grep _PIPELINE_CONFIG)

### 6A-3: Fix Broken Things

| Issue | Portal | Fix |
|-------|--------|-----|
| My RPI error "build call index is not defined" | RIIMO | Debug and fix the JS error |
| Version footer ghost reappears in admin | SENTINEL | Hunt second render path — likely in loadAdminView() or switchAdminTab() |
| Pipeline Config not loading | SENTINEL | Debug — likely missing RAPID_CORE functions (now deployed in Phase 5) |
| Module Config not loading | SENTINEL | Same root cause |

**Files:**
- `RIIMO/Index.html` — Find and fix buildCallIndex reference
- `SENTINEL/Index.html` — Grep for version render outside sidebar, kill it

### 6A-4: Cosmetic Alignment

| Issue | Scope | Fix |
|-------|-------|-----|
| Sidebar left indent inconsistent | All 3 | RIIMO is gold standard. Check padding/margin on `.sidebar-section`, `.nav-item`, `.sidebar-section-header` across all 3. Likely PRODASHX has extra padding in Styles.html. |
| Kill redundant screen titles | All 3 | Remove `<h2>` headers inside admin tab content panels that repeat the tab name |
| Kill "User Management" subheader | RIIMO | Remove from Team Mgmt tab content |
| Kill email column from Team Mgmt | RIIMO | Remove from table header + row render |
| Reorder admin tabs | All 3 | Order: Module Config (2nd) → Pipeline Config (3rd). Currently Pipeline is before Module. |

**Files:**
- `PRODASHX/Styles.html` — Check for sidebar padding overrides
- All 3 `Index.html` + `Scripts.html` — Admin tab order + redundant titles

---

## Phase 6B: Admin Panel Rebuild

> Rebuild Module Config, improve Pipeline Config, fix Add User.

### 6B-1: Module Config Tab — Rebuild from Scratch

**Kill** existing content on all portals. Replace with shared design:

**RIIMO version = "Portal Config":**
- Which portals does each user have access to (PRODASHX, SENTINEL, RIIMO)
- Simple toggle matrix: users (rows) x portals (columns)

**SENTINEL/PRODASHX version = "Module Config":**
- Sections: Modules, Apps, Pipelines (matching the sidebar taxonomy)
- Per-user permission matrix: VIEW / EDIT / ADD per item
- Reads from `_USER_HIERARCHY.module_permissions` (RAPID_CORE)
- Writes via `RAPID_CORE.updateUserModulePermissions()`

**Shared backend:** Already exists in RAPID_CORE (Phase 5 shipped `updateUserModulePermissions`).

### 6B-2: Pipeline Config Improvements (RIIMO)

| Feature | Current | Target |
|---------|---------|--------|
| Add Pipeline | Missing | Green button on far right of pipeline tab bar |
| Edit Stage | Missing | Click stage row → inline edit or modal |
| Delete Stage | Exists (soft-delete) | Keep |
| Reorder Stages | Exists (drag) | Keep |

### 6B-3: Add User Modal Improvements (RIIMO)

| Feature | Current | Target |
|---------|---------|--------|
| @retireprotected.com suffix | Ugly, inconsistent styling | Fix to match form design |
| Smart Lookup (existing users) | Manual entry only | When user exists in Google Workspace, Smart Lookup by name → auto-fill email, first, last |
| Create new (triggers onboarding) | Manual entry | Keep manual entry path, optionally trigger On-Boarding pipeline |
| Both flows | Not supported | Toggle or auto-detect: Smart Lookup finds match → existing user path; no match → new user path |

### 6B-4: Move Module Permissions out of Edit User

Currently module permissions show at bottom of Edit User panel in RIIMO. Move to Module Config tab instead. Remove from Edit User panel.

---

## Phase 6C: My RPI Standardization

> One shared implementation, 3 tabs, same on all portals.

### Target: 3 Tabs Only

| Tab | Gold Standard | Content |
|-----|--------------|---------|
| **Profile** | PRODASHX | Name, email, level, division, unit, reports-to, comm prefs, quick links |
| **MyDropZone** | PRODASHX | Meet link, intake folder, booking page, calendar |
| **Meetings** | SENTINEL | Meeting type picker + per-type availability grid |

### Kill from My RPI (all portals)
- Permissions tab
- My Team tab
- Documents tab

### Features Required on All 3
- LEADER+ profile switcher (view/manage team members' profiles)
- Meeting types pre-populated from existing `employee_profile` data
- Availability grid per meeting type

### Current State (NOT shared — needs unification)

| Component | RIIMO | SENTINEL | PRODASHX | Shared? |
|-----------|-------|----------|----------|---------|
| My RPI backend | `RIIMO_MyRPI.gs` (1,587 lines) | `SENTINEL_MyRPI.gs` (179 lines) | `PRODASH_Profile.gs` (451 lines) | NO |
| Admin backend | Delegates to RAPID_CORE | Calls RAPID_CORE | Calls RAPID_CORE | PARTIAL (RAPID_CORE shared, ForUI per portal) |
| RPI Connect HTML | `RPI_Connect.html` | `RPI_Connect.html` | `RPI_Connect.html` | YES (identical) |
| RPI Connect backend | `RIIMO_Messenger.gs` (295) | `SENTINEL_Messenger.gs` (294) | `PRODASH_Messenger.gs` (243) | YES (near-identical) |

### Implementation — Shared Backend Architecture

All cross-portal features follow the same pattern established in Phase 5 (OrgAdmin):

```
RAPID_CORE (shared backend — one source of truth)
├── CORE_OrgAdmin.gs    ← Phase 5 (DONE)
├── CORE_MyRPI.gs       ← Phase 6C: Extract from RIIMO_MyRPI.gs (1,587 lines)
├── CORE_Connect.gs     ← Phase 6C: Formalize from *_Messenger.gs (already near-identical)
└── (future) Comms wrapper ← Next Phase: RAPID_COMMS library already exists
```

Per-portal pattern (same as OrgAdmin):
- Backend: ~20-line delegate file calling RAPID_CORE shared functions
- Frontend: Shared HTML partial copied to each portal, styled by CSS variables

**CORE_MyRPI.gs** (new, extract from RIIMO):
- Profile read/write, meeting type CRUD, availability CRUD, drop zone config
- Profile switcher (LEADER+ can view team members)
- SENTINEL_MyRPI.gs + PRODASH_Profile.gs become thin delegates

**CORE_Connect.gs** (new, formalize from Messenger files):
- Already near-identical across all 3 portals
- Extract shared logic, each portal gets a 1-line delegate

**Shared HTML partials** in `_RPI_STANDARDS/reference/portal/`:
- `MyRPI.html` — Profile, MyDropZone, Meetings tabs
- `RPI_Connect.html` — already shared (identical across all 3)
- Portal-specific styling via CSS variables (--portal, --portal-glow, --portal-accent)

### Fix RIIMO My RPI
- Debug "build call index is not defined" error before standardizing

---

## Phase 6D: Sidebar Architecture (Requires Business Decisions)

> Deferred — needs B2C vs B2B mapping table + JDM alignment on Sales Process structure.

### RIIMO Sidebar Simplification
Current: Pipelines, RAPID Tools, Tool Suites, Apps, Admin
Target: **Pipelines** (On-Boarding, Off-Boarding + future), **Apps** (ATLAS, CAM, DEX, C3, CEO Dashboard, Command Center), **Admin**

Kill RAPID Tools + Tool Suites sections entirely. Everything that's a separate project goes in Apps.

### PRODASHX Information Architecture
This is the big one. Current sidebar doesn't reflect the actual 3-layer Sales Process:
- Layer 1: Sales Center (Prospecting, Sales Process) / Service Center (RMD, Beni)
- Layer 2: Sales Process stages (Discovery, Data Foundation, Case Building, Close)
- Layer 3: Tools within stages (QUE-Medicare, QUE-Life, QUE-Annuity, QUE-Advisory)

My Cases + Report Orders belong in the Sales Process flow, not standalone.
Sales Process stages need their own admin config (not traditional pipeline config).

### SENTINEL Parallel Structure
- Pipelines: Prospecting, Sales Process, Transition (correct, keep)
- Need to map Deal Management, Analysis, Market Intel against the B2B version of the 3-layer model
- Producers — investigate what it is

### B2C vs B2B Comparison Table (build this first)
| Layer | PRODASHX (B2C) | SENTINEL (B2B) |
|-------|---------------|----------------|
| Pipelines | Prospecting, Sales Process | Prospecting, Sales Process, Transition |
| Sales Process stages | Discovery, Data Foundation, Case Building, Close | Business, MEC, PRP, SPH |
| Tools within stages | QUE-Medicare/Life/Annuity/Advisory | DAVID Hub, Proposal Maker |

---

## Refined Taxonomy (from JDM walkthrough)

Understanding the 3-layer architecture precisely:

| Layer | What It Is | Classification | Example |
|-------|-----------|----------------|---------|
| **Layer 1: Pipelines** | High-level workflow stages (Kanban) | Configurable in Admin | Prospecting, Sales Process, Transition |
| **Layer 2: Sales Process Stages** | Deep multi-tab workflow modules within Sales Process | **Modules** (native .gs files in portal) | Discovery, Data Foundation, Case Building, Close (B2C); Business, MEC, PRP, SPH (B2B) |
| **Layer 3: QUE Tools / Apps** | Massive domain-specific applications used within stages | **Apps** (separate projects, integrated in frontend) | QUE-Medicare, QUE-Life, QUE-Annuity, QUE-Advisory (B2C); DAVID Hub, Proposal Maker (B2B) |

**Key distinction:**
- **Module** = native code within the portal project. Significant but not a separate project.
- **App** = separate GAS project with its own backend/frontend, exposed and integrated in the portal.
- **Tool** = backend-only, no frontend exposure (RAPID_CORE, RAPID_API, etc.)

**QUE-Medicare current state:** Embedded as a module within PRODASHX (1,420 lines across 3 .gs files). The standalone QUE-Medicare project is an empty shell. It's duplicated in the sidebar — listed as both a module in Sales Centers AND an app in Apps (both point to the same internal page). The Apps listing is incorrect and should be removed. Eventually QUE-Medicare becomes its own project/app as it grows with CSG, Carrier Connect, Blue Button integrations.

**Layer 3 apps don't live in the generic "Apps" sidebar section.** They attach to their parent Sales Process modules (Layer 2). For example, QUE-Medicare launches from within the Case Building module, not from the sidebar.

---

## Deferred / Next Phase

| Item | Reason |
|------|--------|
| Comms Hub full build | Complete project — backend ready, frontend needs design. All 3 portals. |
| Direct mail + voicemail integration | Requires permissions/setup JDM already provided. Roadmap item. |
| PRODASHX Sales/Service Center restructure | Phase 6D — needs business decisions |
| SENTINEL Deal Mgmt / Analysis restructure | Phase 6D — needs business decisions |
| QUE extraction to standalone apps | Future — when Medicare/Life/Annuity/Advisory grow large enough to warrant separate projects |

---

## Deploy Sequence

Phase 6A deploys first (cleanup). Then 6B and 6C can parallelize.

| Phase | Projects Touched | Blocking? |
|-------|-----------------|-----------|
| 6A | All 3 portals + _RPI_STANDARDS | No dependencies |
| 6B | RIIMO (primary), RAPID_CORE (minor) | Depends on 6A |
| 6C | All 3 portals + _RPI_STANDARDS | Depends on 6A (RIIMO My RPI fix) |
| 6D | All 3 portals | Requires business decisions first |

---

## Verification

### Phase 6A
- [ ] Dead admin tabs gone on all 3 portals
- [ ] Dead sidebar items gone, ATLAS/DEX added to Apps
- [ ] RIIMO My RPI loads without error
- [ ] SENTINEL version footer completely gone
- [ ] SENTINEL Pipeline Config + Module Config load
- [ ] Sidebar indent consistent across all 3
- [ ] No redundant titles in admin panels
- [ ] Admin tab order: Team Mgmt → Module Config → Pipeline Config

### Phase 6B
- [ ] Module Config shows proper permission matrix
- [ ] Pipeline Config: can add new pipeline + edit existing stages
- [ ] Add User: Smart Lookup works for existing Workspace users
- [ ] Add User: @retireprotected.com styled correctly
- [ ] Module permissions removed from Edit User panel

### Phase 6C
- [ ] My RPI identical on all 3 portals (3 tabs only)
- [ ] Profile switcher works for LEADER+ on all 3
- [ ] Meetings tab pre-populated with existing data
- [ ] Availability grid functional
