# RPI Codebase Enhancement Plan

> **Created:** 2026-02-04
> **Status:** Active
> **Scope:** All platforms except sentinel v1 (scheduled for full rebuild)

---

## Executive Summary

Consolidate duplicated patterns into RAPID_CORE, modularize monolithic files, and standardize compliance utilities across all RPI projects.

**Excluded:** `sentinel/` (v1) - Full frame-up remodel in progress separately.

---

## Phase 1: RAPID_CORE Extractions (Foundation)

*These unblock everything else - do first.*

### 1.1 Extract Unified API Caller ✅
- **Source:** `PRODASH/PRODASH_Clients.gs` → `callRapidAPI()` (45 lines)
- **Problem:** Duplicated in 3+ PRODASH modules, reimplemented 8x in QUE-Medicare
- **Target:** `RAPID_CORE/CORE_Api.gs` → `callApi()`
- **Consumers:** PRODASH, QUE-Medicare, future projects
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Delivered:** RAPID_CORE v1.1.0 - `callApi()`, `apiGet()`, `apiPost()`

### 1.2 Extract Sheet Reading Utility ✅
- **Source:** `PRODASH/PRODASH_Clients.gs` + `PRODASH_Accounts.gs` (110+ lines combined)
- **Problem:** Identical caching/header normalization logic duplicated
- **Target:** `RAPID_CORE/CORE_Database.gs` → `readMatrixSheet()`
- **Consumers:** PRODASH, any project reading MATRIX sheets directly
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Delivered:** RAPID_CORE v1.2.0 - `readMatrixSheet()`, `clearSheetCache()`, `getSheetCacheStats()`

### 1.3 Add PHI Masking Utilities ✅
- **Problem:** QUE-Medicare displays full SSN/DOB - violates CLAUDE.md PHI rules
- **Target:** `RAPID_CORE/CORE_Compliance.gs` (new module)
  - `maskSSN(ssn)` → `***-**-1234`
  - `maskDOB(dob, showAge)` → age or masked date
  - `sanitizeForLog(obj, sensitiveFields)` → safe logging
- **Consumers:** PRODASH, QUE-Medicare, DEX, any PHI-handling project
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Delivered:** RAPID_CORE v1.1.0 - `maskSSN()`, `maskDOB()`, `maskPhone()`, `maskMBI()`, `calculateAge()`, `sanitizeForLog()`, `safeLog()`

---

## Phase 2: Frontend Modularization

### 2.1 Split PRODASH/Index.html ✅
- **Before:** 4,091 lines (CSS + HTML + JS mixed)
- **After:**
  ```
  PRODASH/
  ├── Index.html (1,160 lines) - Structure + includes
  ├── Styles.html (1,179 lines) - All CSS
  └── Scripts.html (1,759 lines) - All JavaScript
  ```
- **Pattern:** Matches QUE-Medicare's cleaner structure
- **Status:** [x] **COMPLETE** (2026-02-04)

### 2.2 Split sentinel-v2 Index.html (if needed) ✅
- **Current:** 1,887 lines (CSS: 771, HTML: 471, JS: 641)
- **Assessment:** Manageable size. Split is "nice to have" but not critical.
- **Status:** [x] **ASSESSED** - No immediate action needed
- **Recommendation:** Split when next working on sentinel-v2 frontend

### 2.3 Create Shared UI Component Library ✅
- **Problem:** Modal, toast, loading, confirmation patterns copied everywhere
- **Finding:** `UI_DESIGN_GUIDELINES.md` exists in `reference/archive/legacy-setup/` with full spec
- **Reality:** GAS architecture can't share HTML/JS via libraries - only `.gs` code
- **Current State:**
  - PRODASH, DAVID-HUB, QUE-Medicare each implement `showToast()` following the spec
  - Patterns are consistent across projects
  - Guideline doc ensures consistency
- **Status:** [x] **ASSESSED** - Pattern documented; no shared HTML lib possible in GAS (2026-02-04)
- **Recommendation:** Move UI_DESIGN_GUIDELINES.md from archive to active reference

---

## Phase 3: Backend Consolidation

### 3.1 Split IMPORT_GHL.gs ⏸️
- **Current:** 3,171 lines - largest RAPID_IMPORT module
- **Target Structure:**
  ```
  RAPID_IMPORT/
  ├── IMPORT_GHL_Sync.gs - Core sync logic
  ├── IMPORT_GHL_Mapping.gs - Field mapping
  └── IMPORT_GHL_Validation.gs - Data validation
  ```
- **Status:** [ ] **DEFERRED** - Heavy function interdependencies; requires careful testing of GHL sync
- **Note:** 60+ functions with cross-references. Recommend tackling when GHL sync needs maintenance work.

### 3.2 Standardize RAPID_CORE Return Values ✅
- **Original Concern:** Library exports raw functions; consumers must handle errors
- **Assessment:** Current pattern is **correct and appropriate**:
  - Simple utilities (normalize, mask, calculate) → return raw values directly
  - Operations that can fail (API calls, DB writes) → return `{ success, data/error }`
  - RAPID_CORE already follows this correctly (e.g., `callApi()` returns structured, `maskSSN()` returns string)
- **Status:** [x] **ASSESSED** - No change needed (2026-02-04)

### 3.3 Migrate Remaining Imports to RAPID_API ✅
- **Target:** All web import functions route through RAPID_API
- **Migrated Functions (Code.gs):**
  - `importAgentsFromWeb_()` → `importAgentsViaAPI()` ✅
  - `importClientsFromWeb_()` → `importClientsViaAPI()` ✅
  - `importAccountsFromWeb_()` → `importAccountsViaAPI()` ✅
- **Benefit:** Single source of truth, audit trail
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Note:** Base functions in IMPORT_*.gs have direct writes but are called BY RAPID_API as library (correct pattern)

---

## Phase 4: Quality & Compliance

### 4.1 Add Error Handling to QUE-Medicare API Proxy ✅
- **Problem:** Functions don't check response codes, JSON parse can fail silently
- **Files:** `QUE-Medicare/Code.gs` (11 functions refactored)
- **Fix:** Refactored to use RAPID_CORE.callApi() - proper response codes + JSON handling
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Delivered:** QUE-Medicare v1.1.0 - 100+ lines reduced to ~50 lines, all functions use callApi()

### 4.2 Extract Test Framework from Production ✅
- **Context:** `SENTINEL_Testing.gs` (6,017 lines) is in sentinel v1 (excluded from plan)
- **Other Projects:**
  - IMPORT_Testing.gs (1,158 lines) - Appropriate size
  - PRODASH_Testing.gs (545 lines) - Appropriate size
- **Assessment:** No action needed for in-scope projects. Testing files are reasonable sizes.
- **Status:** [x] **ASSESSED** - N/A for in-scope projects (2026-02-04)

### 4.3 Standardize Configuration Pattern ✅
- **Problem:** Mix of hardcoded URLs vs Script Properties
- **Rule:** ALL API URLs, MATRIX IDs, secrets → Script Properties only
- **Audit Results:**
  - **PRODASH:** Fixed - 8 hardcoded MATRIX_IDs replaced with `RAPID_CORE.getMATRIX_ID('PRODASH')`
    - PRODASH_Clients.gs: New `getProdashMatrixId_()` lazy-loaded getter
    - PRODASH_Accounts.gs: Uses shared getter
    - PRODASH_CLIENT360.gs: Uses shared getter
    - DEBUG_API.gs: 5 instances fixed
  - **QUE-Medicare:** ✅ Already compliant (uses Script Properties for QUE_API_URL)
  - **DAVID-HUB:** ✅ No hardcoded IDs found
- **Status:** [x] **COMPLETE** (2026-02-04)

---

## Phase 5: DAVID-HUB Refinements

### 5.1 Create ActionRouter Pattern ✅
- **Current:** `Code.gs` has switch statement with 15 cases in organized sections
- **Assessment:** Current structure is clean and readable. Cases are grouped by function (HYPO, User/Admin, QUAL Flow, MEC, SPH). ActionRouter pattern would be over-engineering.
- **Status:** [x] **ASSESSED** - No action needed (2026-02-04)

### 5.2 Decouple Output Pipeline ✅
- **Current:** `Output.gs` (931 lines) - PDF→MATRIX→SENTINEL→Email→SMS→Slack pipeline
- **Assessment:** Code is well-structured with clear sequential steps. Pipeline pattern is appropriate for this use case. Chain-of-responsibility would add complexity without benefit.
- **Status:** [x] **ASSESSED** - No action needed (2026-02-04)

---

## Tracking

### Completion Checklist

| Phase | Item | Owner | Status | Completed |
|-------|------|-------|--------|-----------|
| 1.1 | Extract callApi() | GA | **DONE** | 2026-02-04 |
| 1.2 | Extract readMatrixSheet() | GA | **DONE** | 2026-02-04 |
| 1.3 | Add PHI masking utilities | GA | **DONE** | 2026-02-04 |
| 2.1 | Split PRODASH/Index.html | GA | **DONE** | 2026-02-04 |
| 2.2 | Assess sentinel-v2 HTML | GA | **ASSESSED** | 2026-02-04 |
| 2.3 | Create shared UI library | GA | **ASSESSED** | 2026-02-04 |
| 3.1 | Split IMPORT_GHL.gs | - | **DEFERRED** | |
| 3.2 | Standardize RAPID_CORE returns | GA | **ASSESSED** | 2026-02-04 |
| 3.3 | Migrate imports to RAPID_API | GA | **DONE** | 2026-02-04 |
| 4.1 | QUE-Medicare error handling | GA | **DONE** | 2026-02-04 |
| 4.2 | Extract test framework | GA | **ASSESSED** | 2026-02-04 |
| 4.3 | Standardize config pattern | GA | **DONE** | 2026-02-04 |
| 5.1 | DAVID-HUB ActionRouter | GA | **ASSESSED** | 2026-02-04 |
| 5.2 | DAVID-HUB Output pipeline | GA | **ASSESSED** | 2026-02-04 |

### Priority Order (Recommended)

1. **Phase 1** (RAPID_CORE) - Unblocks everything, highest ROI
2. **Phase 4.1** (QUE error handling) - Quick win, prevents silent failures
3. **Phase 2.1** (PRODASH HTML) - High pain point, moderate effort
4. **Phase 3.1** (GHL split) - Maintainability win
5. **Phases 2.3, 5.x** - Nice-to-haves, do as time permits

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-04 | v2.0 | Completed 3.3 (RAPID_API migration) - All web imports now route through API |
| 2026-02-04 | v1.9 | Assessed 3.2 (Return values) - Current pattern is correct; no change needed |
| 2026-02-04 | v1.8 | Assessed 2.3 (UI library) - UI_DESIGN_GUIDELINES.md exists; GAS can't share HTML |
| 2026-02-04 | v1.7 | Assessed 4.2 (Test framework) - N/A for in-scope projects |
| 2026-02-04 | v1.6 | Assessed 5.1 + 5.2 (DAVID-HUB) - Current architecture is clean, no changes needed |
| 2026-02-04 | v1.5 | Completed 4.3 (Config standardization) - PRODASH hardcoded IDs → RAPID_CORE.getMATRIX_ID() |
| 2026-02-04 | v1.4 | Completed 2.1 (PRODASH HTML split) - 4,091 lines → 3 modular files |
| 2026-02-04 | v1.3 | Completed 4.1 (QUE-Medicare error handling) - QUE v1.1.0 |
| 2026-02-04 | v1.2 | Completed 1.2 (readMatrixSheet) - RAPID_CORE v1.2.0. **Phase 1 COMPLETE!** |
| 2026-02-04 | v1.1 | Completed 1.1 (callApi) and 1.3 (PHI masking) - RAPID_CORE v1.1.0 |
| 2026-02-04 | v1.0 | Initial plan created |

---

## Notes

- **sentinel v1:** Excluded from this plan. Full rebuild in progress.
- **RAPID_CORE changes:** Require version bump + library update in all consumers
- **HTML splits:** Test thoroughly - GAS include() can have quirks

---

*Last updated: 2026-02-04*
