# RPI Ecosystem Documentation Inventory

**Audit Date:** 2026-01-25  
**Purpose:** Identify documentation across all projects for potential consolidation/indexing in RPI-Standards

---

## Summary

| Project | Total Docs | Agent Docs | Technical | Strategic | Notes |
|---------|------------|------------|-----------|-----------|-------|
| MCP-Hub | 22 | 0 | 18 | 4 | Well-organized subfolders |
| DAVID-HUB | 8 | 8 | 0 | 0 | Standard agent structure |
| CAM | 10 | 9 | 1 | 0 | Has SENTINEL migration doc |
| RAPID_API | 13 | 4 | 9 | 0 | Heavy on setup guides |
| sentinel | 20+ | 8 | 9 | 3 | Some 'x' prefixed (deprecated?) |
| RAPID_IMPORT | 10 | 10 | 0 | 0 | Standard agent structure |
| RAPID_CORE | 27 | 9 | 18 | 0 | Most scattered (root level) |
| PRODASH | 10 | 9 | 1 | 0 | Standard agent structure |
| CEO Dashboard | 20 | 8 | 4 | 8 | **Has team playbooks** |
| RPI Content Manager | 4 | 2 | 2 | 0 | Minimal docs |
| DIMS | 2 | 0 | 2 | 0 | Minimal docs |
| **TOTAL** | **~146** | **~67** | **~64** | **~15** | |

---

## Detailed Inventory by Project

### 1. MCP-Hub (22 files)

**Location:** `/Users/joshd.millang/Projects/MCP-Hub/`

| Path | File | Category | Action? |
|------|------|----------|---------|
| `docs/` | HANDOFF-Meeting-Intelligence-System.md | Technical | Keep |
| `docs/` | current-config.md | Technical | Keep |
| `docs/` | Quick-Reference.md | Technical | **INDEX in Standards** |
| `docs/` | Implementation-Guide.md | Technical | Keep |
| `docs/` | integration-mcps.md | Technical | Keep |
| `docs/` | credentials.md | Technical | Keep (sensitive) |
| `docs/` | roadmap.md | Strategic | **INDEX in Standards** |
| `docs/` | SENTINEL-HANDOFF-BoB-Analysis-Pipeline.md | Technical | Keep |
| `docs/` | google-meet-recordings-setup.md | Technical | Keep |
| `docs/` | setup-new-machine.md | Technical | **INDEX in Standards** |
| `commission-intelligence/docs/` | MATRIX-MEDSUP-COMP-GRID-SPEC.md | Technical | Keep |
| `commission-intelligence/docs/` | MATRIX-ANC-COMP-GRID-SPEC.md | Technical | Keep |
| `commission-intelligence/docs/` | COMMISSION_ANALYSIS.md | Technical | Keep |
| `commission-intelligence/docs/` | SOURCE-PDFS-INDEX.md | Technical | Keep |
| `commission-intelligence/docs/` | Midwest_Medigap_Executive_Summary.md | Output | Archive? |
| `commission-intelligence/docs/` | HANDOFF-2026-01-23-Midwest-Medigap-Analysis.md | Handoff | Archive? |
| Root | README.md | Overview | Keep |
| `healthcare-mcps/` | README.md | Technical | Keep |
| `commission-intelligence/` | README.md | Technical | Keep |
| `rpi-meeting-processor/` | README.md | Technical | Keep |

**Recommendation:** Index `roadmap.md`, `Quick-Reference.md`, `setup-new-machine.md` in Standards

---

### 2. DAVID-HUB (8 files)

**Location:** `/Users/joshd.millang/Projects/DAVID-HUB/Docs/`

| File | Category |
|------|----------|
| 0-SESSION_HANDOFF.md | Agent/Handoff |
| 1-AGENT_BRIEFING.md | Agent |
| 2.1-AGENT_SCOPE_GENERAL.md | Agent |
| 2.2-AGENT_SCOPE_OPS.md | Agent |
| 3.1-AGENT_SCOPE_SPC1_UI.md | Agent |
| 3.2-AGENT_SCOPE_SPC2_QUAL.md | Agent |
| 3.3-AGENT_SCOPE_SPC3_MEC.md | Agent |
| 3.4-AGENT_SCOPE_SPC4_SPH.md | Agent |

**Recommendation:** Standard structure, keep in project

---

### 3. CAM (10 files)

**Location:** `/Users/joshd.millang/Projects/CAM/Docs/`

| File | Category | Action? |
|------|----------|---------|
| 0-SESSION_HANDOFF.md | Agent/Handoff | Keep |
| 1-AGENT_BRIEFING.md | Agent | Keep |
| 2.1-AGENT_SCOPE_GENERAL.md | Agent | Keep |
| 2.2-AGENT_SCOPE_OPS.md | Agent | Keep |
| 3.1-AGENT_SCOPE_SPC1_UI.md | Agent | Keep |
| 3.2-AGENT_SCOPE_SPC2_PIPELINE.md | Agent | Keep |
| 3.3-AGENT_SCOPE_SPC3_REVENUE.md | Agent | Keep |
| 3.4-AGENT_SCOPE_SPC4_COMMISSION.md | Agent | Keep |
| 3.5-AGENT_SCOPE_SPC5_ANALYTICS.md | Agent | Keep |
| SENTINEL_MIGRATION_PLAN.md | Technical | Review/Archive? |

**Recommendation:** Standard structure, keep in project

---

### 4. RAPID_API (13 files)

**Location:** `/Users/joshd.millang/Projects/RAPID_API/`

| File | Category | Action? |
|------|----------|---------|
| README.md | Overview | Keep |
| SETUP_INSTRUCTIONS.md | Technical | Keep |
| LIBRARY_SETUP.md | Technical | Consolidate? |
| LIBRARY_TROUBLESHOOTING.md | Technical | Consolidate? |
| QUICK_FIX.md | Technical | Archive? |
| QUICK_FIX_LIBRARY.md | Technical | Archive? |
| API_TESTING_GUIDE.md | Technical | Keep |
| README_UI.md | Technical | Keep |
| README_GIT.md | Technical | Keep |
| `Docs/0-SESSION_HANDOFF.md` | Agent | Keep |
| `Docs/1-AGENT_BRIEFING.md` | Agent | Keep |
| `Docs/2.1-AGENT_SCOPE_GENERAL.md` | Agent | Keep |
| `Docs/2.2-AGENT_SCOPE_OPS.md` | Agent | Keep |

**Recommendation:** Consolidate LIBRARY_*.md files, archive QUICK_FIX_*.md

---

### 5. sentinel (20+ files)

**Location:** `/Users/joshd.millang/Projects/sentinel/`

| File | Category | Action? |
|------|----------|---------|
| xREADME.md | Overview | **Deprecated (x prefix)** |
| xARCHITECTURE_VISION.md | Strategic | Review if current |
| xCODE_ALIGNMENT_CHANGES.md | Technical | Review |
| xDEPLOYMENT_SUMMARY.md | Technical | Review |
| xQUICK_START.md | Technical | Review |
| xSETUP_COMPLETE.md | Technical | Review |
| xPROJECT_MASTER.md | Strategic | Review |
| RAPID_CORE_SETUP.md | Technical | Keep |
| RAPID_CORE_SETUP_EXECUTE.md | Technical | Keep |
| REVENUE_MEDSUP_ANCILLARY.md | Technical | Keep |
| TASK_IMO_RATES_PHASE_BUILD.md | Technical | Keep |
| `Docs/0-SESSION_HANDOFF.md` | Agent | Keep |
| `Docs/1-AGENT_BRIEFING.md` | Agent | Keep |
| `Docs/2.1-AGENT_SCOPE_GENERAL.md` | Agent | Keep |
| `Docs/2.2-AGENT_SCOPE_OPS.md` | Agent | Keep |
| `Docs/3.1-AGENT_SCOPE_SPC1_UI.md` | Agent | Keep |
| `Docs/3.2-AGENT_SCOPE_SPC2_MEDICARE.md` | Agent | Keep |
| `Docs/3.3-AGENT_SCOPE_SPC3_DATABASE.md` | Agent | Keep |
| `Docs/3.4-AGENT_SCOPE_SPC4_FINANCIAL.md` | Agent | Keep |
| `Docs/4-AGENT_SCOPE_BOB_ANALYSIS.md` | Agent | Keep |

**Recommendation:** Delete or archive 'x' prefixed files (7 files)

---

### 6. RAPID_IMPORT (10 files)

**Location:** `/Users/joshd.millang/Projects/RAPID_IMPORT/Docs/`

| File | Category |
|------|----------|
| 0-SESSION_HANDOFF.md | Agent/Handoff |
| 1-AGENT_BRIEFING.md | Agent |
| 2.1-AGENT_SCOPE_GENERAL.md | Agent |
| 2.2-AGENT_SCOPE_OPS.md | Agent |
| 3.1-AGENT_SCOPE_SPC1_AGENT_IMPORT.md | Agent |
| 3.2-AGENT_SCOPE_SPC2_CLIENT_IMPORT.md | Agent |
| 3.3-AGENT_SCOPE_SPC3_ACCOUNT_IMPORT.md | Agent |
| 3.4-AGENT_SCOPE_SPC4_REVENUE_IMPORT.md | Agent |
| 3.5-AGENT_SCOPE_SPC5_VALIDATION.md | Agent |
| 3.6-AGENT_SCOPE_SPC6_TESTING.md | Agent |

**Recommendation:** Standard structure, keep in project

---

### 7. RAPID_CORE (27 files) - **NEEDS CLEANUP**

**Location:** `/Users/joshd.millang/Projects/RAPID_CORE/` (root level, no Docs folder!)

**Agent Docs:**
- 0-SESSION_HANDOFF.md
- 1-AGENT_BRIEFING.md
- 2.1-AGENT_SCOPE_GENERAL.md
- 2.2-AGENT_SCOPE_OPS.md
- 3.1-AGENT_SCOPE_SPC1_DATABASE.md
- 3.2-AGENT_SCOPE_SPC2_NORMALIZE.md
- 3.3-AGENT_SCOPE_SPC3_MATCH.md
- 3.4-AGENT_SCOPE_SPC4_DRIVE.md
- 3.5-AGENT_SCOPE_SPC5_CARRIERS.md
- 3.6-AGENT_SCOPE_SPC6_FINANCIAL.md

**Technical Docs:**
- PROJECT_PLAN.md
- PROJECT_STANDARDS.md
- STATUS.md
- TASK_BREAKDOWN.md
- INTEGRATION_TEST_PLAN.md
- DEPLOYMENT_REPORT.md
- GA_REVIEW_REPORT.md
- CHECK_VERSION.md
- FIX_VERSION_UNDEFINED.md
- TEST_RAPID_IMPORT.md
- CREATE_MATRIX_SPREADSHEET.md
- SETUP_MATRIX_INSTRUCTIONS.md
- SETUP_DRIVE_INSTRUCTIONS.md
- ADD_LIBRARY_TO_RAPID_IMPORT.md
- LIBRARY_TROUBLESHOOTING.md
- MANUAL_VERIFICATION_STEPS.md
- AGENT_INSTRUCTIONS.md

**Recommendation:** 
1. Move agent docs to `Docs/` folder
2. Archive task-specific docs (FIX_*, CHECK_*, TEST_*)
3. Keep: PROJECT_STANDARDS.md, STATUS.md, INTEGRATION_TEST_PLAN.md

---

### 8. PRODASH (10 files)

**Location:** `/Users/joshd.millang/Projects/PRODASH/` (root level, no Docs folder)

| File | Category |
|------|----------|
| 1-AGENT_BRIEFING.md | Agent |
| 2.1-AGENT_SCOPE_GENERAL.md | Agent |
| 2.2-AGENT_SCOPE_OPS.md | Agent |
| 3.1-AGENT_SCOPE_SPC1_CLIENTS.md | Agent |
| 3.2-AGENT_SCOPE_SPC2_ACCOUNTS.md | Agent |
| 3.3-AGENT_SCOPE_SPC3_CLIENT360.md | Agent |
| 3.4-AGENT_SCOPE_SPC4_RMD_CENTER.md | Agent |
| 3.5-AGENT_SCOPE_SPC5_UI.md | Agent |
| 3.6-AGENT_SCOPE_SPC6_TESTING.md | Agent |
| PROJECT_STANDARDS.md | Technical |

**Recommendation:** Move to `Docs/` folder for consistency

---

### 9. CEO Dashboard (20 files) - **HAS TEAM PLAYBOOKS**

**Location:** `/Users/joshd.millang/Projects/CEO Dashboard/Docs/`

**Agent Docs:**
- 0-SESSION_HANDOFF.md
- 1- AGENT_BRIEFING.md
- 2.1- AGENT_SCOPE_GENERAL.md
- 2.2- AGENT_SCOPE_OPS.md
- 3.1- AGENT_SCOPE_SPC1_AI.md
- 3.2- AGENT_SCOPE_SPC2_INTEGRATIONS.md
- 3.3- AGENT_SCOPE_SPC3_DATABASE.md
- 3.4- AGENT_SCOPE_SPC4_FRONTEND.md

**Playbooks (IMPORTANT!):**
- RPI- Leadership Team Playbook.md
- RPI Sales Team- Playbook.md
- RPI Service Team- Playbook.md
- RPI Support Team- Playbook.md
- Sales Leader Play Book.md
- ProDash 101.md

**Strategic:**
- rpi-data-division-strategy.md
- CLAUDE_MEMORY_DIGEST.md

**Technical:**
- README.md
- HANDOFF.md
- AGENT_HANDOFF.md
- QUICKSTART_FOR_AGENT.md

**Recommendation:** 
1. **MOVE Playbooks to RPI-Standards** (team-wide reference)
2. **MOVE ProDash 101 to RPI-Standards** (universal training)
3. **MOVE rpi-data-division-strategy.md to RPI-Standards** (strategic)

---

### 10. RPI Content Manager (4 files)

**Location:** `/Users/joshd.millang/Projects/RPI Content Manager/`

| File | Category |
|------|----------|
| README.md | Overview |
| HANDOFF.md | Handoff |
| `docs/1-AGENT_BRIEFING.md` | Agent |
| `docs/2.2-AGENT_SCOPE_OPS.md` | Agent |

**Recommendation:** Standard structure, keep in project

---

### 11. DIMS (2 files)

**Location:** `/Users/joshd.millang/Projects/DIMS/`

| File | Category |
|------|----------|
| DEPLOYMENT_GUIDE.md | Technical |
| ENHANCED_CONTENT_DATE_EXTRACTION.md | Technical |

**Recommendation:** Keep in project (minimal, specific)

---

## Recommended Actions

### HIGH PRIORITY - Move to RPI-Standards

| Source | File | Reason |
|--------|------|--------|
| CEO Dashboard | RPI- Leadership Team Playbook.md | Universal team reference |
| CEO Dashboard | RPI Sales Team- Playbook.md | Universal team reference |
| CEO Dashboard | RPI Service Team- Playbook.md | Universal team reference |
| CEO Dashboard | RPI Support Team- Playbook.md | Universal team reference |
| CEO Dashboard | ProDash 101.md | Universal training doc |
| CEO Dashboard | rpi-data-division-strategy.md | Strategic planning |
| MCP-Hub | setup-new-machine.md | Onboarding reference |

### MEDIUM PRIORITY - Index Reference in RPI-Standards

| Source | File | Index As |
|--------|------|----------|
| MCP-Hub | roadmap.md | Tech Roadmap |
| MCP-Hub | Quick-Reference.md | MCP Quick Reference |

### CLEANUP - Archive/Delete

| Project | Files | Action |
|---------|-------|--------|
| sentinel | x*.md (7 files) | Delete deprecated |
| RAPID_API | QUICK_FIX*.md | Archive |
| RAPID_CORE | FIX_*, CHECK_*, TEST_*.md | Archive |

### STRUCTURAL - Reorganize

| Project | Current | Change To |
|---------|---------|-----------|
| RAPID_CORE | Docs in root | Create `Docs/` folder |
| PRODASH | Docs in root | Create `Docs/` folder |

---

## Proposed RPI-Standards Structure (After Consolidation)

```
RPI-Standards/
├── README.md                           # Main index
├── +0- [CORE STANDARDS]               # Existing
├── +1- [TASK TEMPLATES]               # Existing
├── Plans/                              # Existing (10 plans)
├── Playbooks/                          # NEW
│   ├── RPI-Leadership-Team-Playbook.md
│   ├── RPI-Sales-Team-Playbook.md
│   ├── RPI-Service-Team-Playbook.md
│   ├── RPI-Support-Team-Playbook.md
│   └── ProDash-101.md
├── Strategic/                          # NEW
│   └── rpi-data-division-strategy.md
└── Onboarding/                         # NEW
    └── setup-new-machine.md
```
