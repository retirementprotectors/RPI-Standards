# Portal Overhaul — Working Plan

> **Last updated**: 2026-03-08 (Phase 0.5 — Pipeline Enforcement Rules)
> **Source**: JDM_Portal_Feedback_Inventory.md (137 items)
> **Pipeline**: Intake → Planner → Executor → Auditor → JDM Review

---

## Phase 0.5: Pipeline Enforcement Rules

| Task | Action | Status | Acceptance Criteria | Audit Method |
|------|--------|--------|---------------------|--------------|
| 0.5-1 | Create `quality-gate-plan-format.local.md` | DONE | Rule blocks plan writes missing Acceptance Criteria, Audit Method, CHECKPOINT | `cat _RPI_STANDARDS/hookify/hookify.quality-gate-plan-format.local.md` — file exists with event: file, action: block |
| 0.5-2 | Create `quality-gate-phase-complete.local.md` | DONE | Rule blocks "phase complete" prompts until plan updated with evidence | `cat _RPI_STANDARDS/hookify/hookify.quality-gate-phase-complete.local.md` — file exists with event: prompt, action: block |
| 0.5-3 | Create `quality-gate-audit-verify.local.md` | DONE | Rule injects adversarial audit protocol on "audit"/"verify" | `cat _RPI_STANDARDS/hookify/hookify.quality-gate-audit-verify.local.md` — file exists with event: prompt, action: warn |
| 0.5-4 | Enhance `intent-plan-mode` with pipeline awareness | DONE | #LetsPlanIt injects Acceptance Criteria + Audit Method + CHECKPOINT requirements | `grep "PIPELINE AWARENESS" _RPI_STANDARDS/hookify/hookify.intent-plan-mode.local.md` — match found |
| 0.5-5 | Run `setup-hookify-symlinks.sh` to propagate | DONE | New rules symlinked to all 18+ projects | `ls -la .claude/hookify.quality-gate-plan-format.local.md` in any project — symlink exists |
| 0.5-6 | "Kill means DELETE" in `intent-plan-mode` | DONE | Rule defines Kill = delete entirely, not merge/hide/stub/rename/comment | `grep "Kill means DELETE" _RPI_STANDARDS/hookify/hookify.intent-plan-mode.local.md` — match found |

**CHECKPOINT: Phase 0.5 complete. JDM verifies rules are active.**

---

## Phase 0: Research & Answers

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 0-1 | 10, 11 | Title vs Level vs Role audit | RESOLVED | JDM decided: keep all three. No rename. | N/A — business decision, no code change |
| 0-2 | 45, 46, 47 | Org structure investigation | RESOLVED | Org Mgmt = RIIMO only, first admin tab. Kill from PRODASHX. Data from _COMPANY_STRUCTURE. | N/A — business decision |
| 0-3 | 64-66 | Task Templates investigation | PENDING | Confirm functional or identify bugs | Load RIIMO Admin → Task Templates → verify renders without spinning |
| 0-4 | 67 | Job Templates dual buttons | PENDING | Identify if "New Template" and "Create Template" are duplicate buttons | Read JobTemplates.html, grep for button labels |
| 0-5 | 68, 69 | Pipeline automation inventory | PENDING | Full list of executeStage() automations documented | Read RIIMO_Pipelines.gs, grep for executeStage/automation references |
| 0-6 | 97, 98 | Comms Hub investigation | RESOLVED | Comms Hub in Dashboard quick actions only. Backend exists. | N/A — confirmed during audit |
| 0-7 | 104 | C3 investigation | RESOLVED | C3 = embedded native module, marked isApp: true (wrong). Fix: reclassify. | N/A — confirmed during audit |
| 0-8 | 116, 117 | SENTINEL Deal Mgmt + Producers | PENDING | Document current structure, recommend changes | Read sentinel-v2 sidebar config + Deal Management code |
| 0-9 | 28 | Direct mail/voicemail roadmap | PENDING | Search for roadmap references | Grep for direct_mail, voicemail across codebase |
| 0-10 | 22, 23 | B2C vs B2B comparison table | PENDING | Table built from audit data | Document exists with both portal structures compared |

**CHECKPOINT: Phase 0 complete. All questions answered. JDM reviews before Phase 1.**

---

## Phase 1: RIIMO Cleanup

### 1A: Kill Dead Things

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 1A-1 | 60 | Verify Error Log still gone | PENDING | Not in admin tabs | Grep `Error.Log\|error-log\|ERROR_LOG` in RIIMO sidebar/admin config → 0 matches |
| 1A-2 | 61 | Verify On-Boarding still gone from admin | PENDING | Not in admin tabs (pipeline only) | Grep admin tab config for onboarding → 0 in admin, exists in pipelines |
| 1A-3 | 62 | Verify Off-Boarding still gone from admin | PENDING | Not in admin tabs (pipeline only) | Same pattern as 1A-2 |
| 1A-4 | 63 | Verify Job Templates still functional | PENDING | Tab exists and loads | Grep admin tab config for Job Templates → present |
| 1A-5 | 64-66 | Task Templates: per Phase 0-3 decision | PENDING | Per JDM decision | Per Phase 0-3 |
| 1A-6 | 56-58, 75 | KILL Data Maint / Tech Maint / Security from sidebar + pipeline config | PENDING | Zero references in sidebar AND pipeline data | `grep -r "DATA_MAINTENANCE\|TECH_MAINTENANCE\|SECURITY\|Data Maint\|Tech Maint" RIIMO/` → 0 matches in sidebar render code |
| 1A-7 | 70-72 | KILL RAPID Tools section entirely | PENDING | Section deleted from sidebar | `grep -r "RAPID Tools\|rapid-tools\|RAPID_TOOLS.*section\|Tool Suites" RIIMO/Index.html` → 0 matches |
| 1A-8 | 73 | KILL DAVID Tools section entirely | PENDING | Section deleted from sidebar | `grep -r "DAVID Tools\|david-tools\|DAVID Hub" RIIMO/Index.html RIIMO/RIIMO_Core.gs` → 0 matches in sidebar |
| 1A-9 | — | KILL RPI Tools section entirely | PENDING | Section deleted from sidebar | `grep -r "RPI Tools\|rpi-tools" RIIMO/Index.html` → 0 matches |
| 1A-10 | 25 | Remove CEO Dashboard from Apps | PENDING | Gone from Apps | `grep -r "CEO.Dashboard\|CEO_DASHBOARD\|ceo-dashboard" RIIMO/` → 0 in sidebar/apps config |
| 1A-11 | 76-77 | Final sidebar: Dashboard + Pipelines(2) + Apps(5) + Admin | PENDING | Exactly 4 sections, correct items | Count sections in sidebar render. Pipelines = On-Boarding + Off-Boarding only. Apps = Atlas, CAM, DEX, C3, Command Center. |
| 1A-12 | 80 | Onboarding above Offboarding | PENDING | Visual order correct | Read sidebar config array — On-Boarding index < Off-Boarding index |
| 1A-13 | 79 | Dashboard — leave as-is | ALREADY DONE | No changes | N/A |

**CHECKPOINT: Phase 1A complete. JDM reviews RIIMO sidebar kills. Auditor verifies before 1B.**

### 1B: Fix Broken / Wrong Things

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 1B-1 | 84 | Verify "build call index" error still fixed | PENDING | My RPI loads clean | Load in Playwright → no console errors on My RPI |
| 1B-2 | 14 | UNDO: Remove My Team from Profile (was merged, should be KILLED) | PENDING | `_myrpiRenderMyTeam` call removed from Profile. Zero My Team content. | `grep -r "_myrpiRenderMyTeam\|renderMyTeam\|My Team" RIIMO/` → 0 in MyRPI rendering |
| 1B-3 | 15 | UNDO: Remove Documents from Profile (was merged, should be KILLED) | PENDING | `_myrpiRenderDocuments` call removed. Zero Documents content. | `grep -r "_myrpiRenderDocuments\|renderDocuments" RIIMO/` → 0 in MyRPI rendering |
| 1B-4 | 43 | Portal access selection errors | PENDING | Portal Config saves without errors | Load Admin → Portal Config → attempt save → no console errors |
| 1B-5 | 38 | Reports To non-canonical names | PENDING | All names display as canonical full names | Verify resolveUser() wired to Team Mgmt display render |
| 1B-6 | 67 | Job Templates dual buttons | PENDING | One clear action button (per Phase 0-4) | Read JobTemplates.html → count CTA buttons → must be 1 |

**CHECKPOINT: Phase 1B complete. JDM reviews fixes. Auditor verifies before 1C.**

### 1C: Admin Rebuild

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 1C-1 | 48 | Org Management tab — first tab in Admin | PENDING | Standalone tab for divisions + units CRUD. First position. | Grep admin tab config → "Org Management" at index 0 |
| 1C-2 | 37 | Team Mgmt — add column sorting | PENDING | Click headers to sort | Grep for sort handler on table headers in Team Mgmt render |
| 1C-3 | 9 | Verify email column still removed | PENDING | 7 columns, no email | Grep Team Mgmt column headers → no "Email" |
| 1C-4 | 36 | Verify "User Management" subheader still killed | PENDING | No redundant titles | Grep for "User Management" in Team Mgmt render → 0 |
| 1C-6 | 33, 35 | Add User: Smart Lookup + fix @retireprotected.com | PENDING | Smart Lookup on name → auto-fill. Email styled. | `grep "buildSmartLookup" RIIMO/` in Add User modal code → match found |
| 1C-7 | 34 | Add User: new user triggers On-Boarding pipeline | PENDING | Toggle/auto-detect: match → existing; no match → new + onboarding | Grep for onboarding trigger in Add User flow |
| 1C-8 | 41, 42 | Rename "Module Config" → "Portal Config". Strip to portal access ONLY. | PENDING | Tab renamed. ONLY user x portal toggles. No org structure. | Grep for "Portal Config" in admin tab config → found. Grep for org structure render → 0 in Portal Config. |
| 1C-9 | 44 | Portal access defaults from MATRIX data | PENDING | Pre-populated with existing access data | Verify data fetch on Portal Config load |
| 1C-10 | 39 | Remove module permissions from Edit User | PENDING | Permissions gone from Edit User panel | Grep Edit User modal for permission/module toggles → 0 |
| 1C-11 | 49 | Permission categories → Apps, Modules, Pipelines | PENDING | Old categories replaced | Grep for new category names in Portal Config |
| 1C-12 | 6 | Admin tab order: Org Mgmt → Team Mgmt → Portal Config → Pipeline Config → Job Templates → Task Templates | PENDING | Exact order matches spec | Read tab definition array, verify indices match |
| 1C-13 | 52-54 | Pipeline Config: add pipeline + edit stage + edit pipeline | PENDING | All CRUD operations functional | Grep for add/edit/delete handlers in Pipeline Config |
| 1C-14 | 5 | Kill redundant screen titles | ALREADY DONE | No duplicate titles | Visual check |

**CHECKPOINT: Phase 1C complete. JDM reviews admin rebuild. Auditor verifies before 1D.**

### 1D: My RPI (RIIMO version)

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 1D-1 | 12 | Verify 3 tabs only | PENDING | 3 tabs, clean content | Count tabs in My RPI config |
| 1D-2 | 13 | Verify Permissions killed | PENDING | Gone | Grep for Permissions tab → 0 |
| 1D-3 | 14 | Verify My Team KILLED (not merged) | PENDING | Content DELETED | Covered by 1B-2 |
| 1D-4 | 15 | Verify Documents KILLED (not merged) | PENDING | Content DELETED | Covered by 1B-3 |
| 1D-5 | 16 | Profile matches ProDash gold standard | PENDING | Visual match confirmed | Side-by-side Playwright screenshots |
| 1D-6 | 17 | MyDropZone matches ProDash gold standard | PENDING | Functional | Verify match via Playwright |
| 1D-7 | 18 | Meetings matches Sentinel gold standard | PENDING | Meeting types + availability grid render | Playwright → Meetings tab → verify populated |
| 1D-8 | 20 | LEADER+ profile switcher | PENDING | Functional for leaders | Grep for profile switcher component |

**CHECKPOINT: Phase 1 complete. Full RIIMO audit before moving to Phase 2.**

---

## Phase 2: SENTINEL Cleanup

### 2A: Verify Already-Done Items

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 2A-1 | 111 | Verify Settings killed | PENDING | Gone from admin | Grep sentinel-v2 admin config → no Settings |
| 2A-2 | 112 | Verify Integrations killed | PENDING | Gone | Same pattern |
| 2A-3 | 113 | Verify Database killed | PENDING | Gone | Same pattern |
| 2A-4 | 8 | Verify Team Mgmt removed | PENDING | Not in admin or sidebar | Same pattern |
| 2A-5 | 114 | Verify version ghost fixed | PENDING | No version displayed in UI | Grep for version label render → 0 or hidden |

### 2B: Verify Fixes

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 2B-1 | 109 | Verify Pipeline Config loads | PENDING | Functional | Playwright → Admin → Pipeline Config → renders |
| 2B-2 | 110 | Verify Module Config loads | PENDING | Functional | Playwright → Admin → Module Config → renders |

### 2C: Admin

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 2C-1 | 89 | Module Config permission matrix | PENDING | VIEW/EDIT/ADD per module | Verify matrix renders with toggles |
| 2C-2 | 26 | Sales vs Service + Leader vs User permissions | PENDING | Permission model reflects both dimensions | Design review with JDM |
| 2C-3 | 6 | Admin tab order | PENDING | Module Config → Pipeline Config | Read tab array |
| 2C-4 | 5 | Kill redundant screen titles | PENDING | No duplicate titles | Visual check |
| 2C-5 | 52-54 | Pipeline Config CRUD | PENDING | All CRUD works | Test add/edit/delete |

### 2D: Sidebar + Apps

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 2D-1 | 120 | DEX in Apps — FUNCTIONAL (not stub) | PENDING | DEX loads when clicked | Playwright → click DEX → verify page loads |
| 2D-2 | 121 | ATLAS in Apps | PENDING | ATLAS app entry with working URL | Grep for ATLAS in apps config → found with URL |
| 2D-3 | 24 | CAM, C3, Command Center in Apps | PENDING | All 5 apps functional | Click each in Playwright → all load |
| 2D-4 | 25 | Verify CEO Dashboard absent | PENDING | Not listed | Grep → 0 |
| 2D-5 | 1, 2 | Sidebar indent match RIIMO | PENDING | Pixel-identical | Compare CSS values |

### 2E: My RPI

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 2E-1 | 12 | Verify 3 tabs | PENDING | Profile, MyDropZone, Meetings | Count tabs |
| 2E-2 | 123 | Profile matches ProDash | PENDING | Full ProDash-equivalent rendering | Side-by-side comparison |
| 2E-3 | 19, 126 | Meeting types populated | PENDING | Types display from employee_profile | Playwright → Meetings → verify list |
| 2E-4 | 127 | Profile switcher (LEADER+) | PENDING | Dropdown functional | Grep for switcher component |
| 2E-5 | 13-15 | Verify kills | PENDING | No remnants | Grep for Permissions/MyTeam/Documents → 0 |

**CHECKPOINT: Phase 2 complete. Full SENTINEL audit before Phase 3.**

---

## Phase 3: PRODASHX Cleanup

### 3A: Kill Dead Things (Reverse damage)

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 3A-1 | 88 | Verify Settings killed | PENDING | Gone | Grep → 0 |
| 3A-2 | 86 | Verify C3/BoB killed | PENDING | Gone | Grep → 0 |
| 3A-3 | 87 | KILL Org Structure tab | PENDING | Tab DELETED. Code removed. | `grep -r "Org.Structure\|org-structure\|ORG_STRUCTURE" PRODASHX/` in admin config → 0 |
| 3A-4 | 8 | KILL Team Management / Team Entitlements entirely | PENDING | Tab DELETED. All code removed. Zero admin user mgmt. | `grep -r "Team.Entitlements\|team-entitlements\|Team.Management\|TEAM_ENTITLEMENTS" PRODASHX/` → 0 |
| 3A-5 | 103 | Verify QUE-Medicare not duplicated | PENDING | Once in Sales Centers only | Count occurrences |
| 3A-6 | 97 | Verify Comms Hub removed from sidebar | PENDING | Only in Dashboard quick actions | Grep sidebar config |
| 3A-7 | — | Fix CAM broken link (points to nonexistent page) | PENDING | CAM loads when clicked | `page: 'cam'` has matching view OR external URL |
| 3A-8 | 104 | Fix C3 labeling (isApp: true but embedded) | PENDING | Correct classification | `isApp` set appropriately or moved to proper section |

### 3B: Fix Broken Things

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 3B-1 | 99 | Sales Centers Life/Annuity/Advisory NOT pointing to generic Pipelines | PENDING | Each loads its own view | `grep "page: 'pipelines'" PRODASHX/` in Sales Centers config → 0 for Life/Annuity/Advisory |
| 3B-2 | 85 | Pipeline Config quality | PENDING | CRUD works | Test in Playwright |

### 3C: Admin (Simplified)

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 3C-1 | 89 | Module Config permission matrix | PENDING | Functional after killing Team Entitlements | Matrix renders |
| 3C-2 | 26 | Sales/Service + Leader/User permissions | PENDING | Model reflects both dimensions | Design review |
| 3C-3 | 6 | Admin tab order: Module Config → Pipeline Config only | PENDING | Exactly 2 tabs | Count admin tabs → 2 |
| 3C-4 | 5 | Kill redundant titles | PENDING | Clean | Visual check |

### 3D: Sidebar + Apps

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 3D-1 | 24 | Apps: Atlas, CAM, DEX, C3, CC all working | PENDING | All 5 apps with WORKING links | Click each in Playwright |
| 3D-2 | 25 | Verify CEO Dashboard absent | PENDING | Not listed | Grep → 0 |
| 3D-3 | 1, 2 | Sidebar indent match RIIMO | PENDING | Arrows not cut off | Test at various zoom |

### 3E: My RPI

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 3E-1 | 12 | Verify 3 tabs | PENDING | Complete | Count tabs |
| 3E-2 | 13-15 | Verify kills | PENDING | No remnants | Grep → 0 |
| 3E-3 | 18 | Verify Meetings functional | PENDING | Types + availability | Playwright |
| 3E-4 | 20 | Verify profile switcher | PENDING | Working | Test |

**CHECKPOINT: Phase 3 complete. Full PRODASHX audit before Phase 4.**

---

## Phase 4: Cross-Portal Shared Backend

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 4-1 | 3, 4 | Verify all configs pull from RAPID_CORE | PENDING | No portal has its own config source | Grep each portal for config definitions not from RAPID_CORE |
| 4-2 | 3 | Shared CSS variable standardization | PENDING | --portal, --portal-glow, --portal-accent | Grep PortalStandard.html across all 3 |
| 4-3 | — | Extract shared My RPI into CORE_MyRPI.gs | PENDING | Single source of truth | One .gs file shared by all 3 portals |
| 4-4 | — | Extract shared RPI Connect into CORE_Connect.gs | PENDING | Single source | One .gs file |

**CHECKPOINT: Phase 4 complete. Cross-portal verification.**

---

## Phase 5: Sidebar Architecture (Requires Phase 0 answers + JDM decisions)

| Task | Feedback # | Action | Status | Acceptance Criteria | Audit Method |
|------|-----------|--------|--------|---------------------|--------------|
| 5-1 | 90-92 | PRODASHX sidebar restructure | PENDING | Sales Center + Sales Process with nested modules | Sidebar config matches 3-layer spec |
| 5-2 | 93 | Move My Cases into Sales Process | PENDING | Not standalone | Grep Workspace section for My Cases → 0 |
| 5-3 | 94 | Move Report Orders under Data Foundation | PENDING | Sub-feature, not standalone | Nested in Data Foundation |
| 5-4 | 101 | Service pipelines in Service Center | PENDING | Admin-configured | Service Center section has pipelines |
| 5-5 | 118 | SENTINEL Sales Process modules | PENDING | Business, MEC, PRP, SPH as Layer 2 | Sidebar config correct |
| 5-6 | 116 | Resolve Deal Management | PENDING | Per Phase 0-8 decision | Documented |
| 5-7 | 117 | Resolve Producers | PENDING | Per Phase 0-8 decision | Documented |
| 5-8 | 91 | Sales Process own admin config | PENDING | Separate from Pipeline Config | Distinct config section |
| 5-9 | 99 | Life/Annuity/Advisory routing fix | PENDING | Per JDM placeholder decision | Each loads correct view |
| 5-10 | 103 | QUE-Medicare: launches from Case Building | PENDING | Not in generic Apps | Single entry point in Case Building |

**CHECKPOINT: Phase 5 complete. Full platform audit.**

---

## Deferred

| Feedback # | Item | Why |
|-----------|------|-----|
| 27 | Direct mail + voicemail | Separate project |
| 29 | Comms Hub full build | Entire project scope |
| 81-83 | RPI Connect redesign | Own project later |
| 98 | Comms Hub placement | Depends on Comms build |
| 79 | Dashboard revisit | JDM said "fine for now" |

---

## Audit Instructions

See plan Phase descriptions above for per-task Audit Methods. General rules:
1. "Killed" = code GONE. Not commented, not flagged, not merged.
2. grep count = 0 is necessary but not sufficient — also visual check.
3. Deployed version must match code version.
4. One contradiction = task FAILS.
