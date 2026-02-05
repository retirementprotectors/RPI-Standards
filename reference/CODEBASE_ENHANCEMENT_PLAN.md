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

### 2.1 Split PRODASH/Index.html
- **Current:** 4,091 lines (CSS + HTML + JS mixed)
- **Target Structure:**
  ```
  PRODASH/
  ├── Index.html (~500 lines) - Structure + includes
  ├── Styles.html (~1,500 lines) - All CSS
  └── Scripts.html (~1,000 lines) - All JavaScript
  ```
- **Pattern:** Match QUE-Medicare's cleaner structure
- **Status:** [ ] Not Started

### 2.2 Split sentinel-v2 Index.html (if needed)
- **Current:** Review size after v1 exclusion
- **Action:** Assess whether v2 needs same treatment
- **Status:** [ ] Assess

### 2.3 Create Shared UI Component Library
- **Problem:** Modal, toast, loading, confirmation patterns copied everywhere
- **Target:** `_RPI_STANDARDS/components/gas-ui-lib.html`
  - `showToast(message, type)`
  - `showConfirmation(options)` → Promise
  - `showLoading()` / `hideLoading()`
  - Card, button, form group templates
- **Consumers:** All GAS web apps
- **Status:** [ ] Not Started

---

## Phase 3: Backend Consolidation

### 3.1 Split IMPORT_GHL.gs
- **Current:** 3,209 lines - largest RAPID_IMPORT module
- **Target Structure:**
  ```
  RAPID_IMPORT/
  ├── IMPORT_GHL_Sync.gs - Core sync logic
  ├── IMPORT_GHL_Mapping.gs - Field mapping
  └── IMPORT_GHL_Validation.gs - Data validation
  ```
- **Status:** [ ] Not Started

### 3.2 Standardize RAPID_CORE Return Values
- **Problem:** Library exports raw functions; consumers must handle errors
- **Option A:** Wrap all exports with `{ success, data/error }`
- **Option B:** Create parallel `*Safe()` versions
- **Decision:** [ ] TBD - discuss with JDM
- **Status:** [ ] Not Started

### 3.3 Migrate Remaining Imports to RAPID_API
- **Current:** Only IMPORT_Intake uses RAPID_API pattern
- **Target:** IMPORT_Agent, IMPORT_Account, IMPORT_Revenue all route through RAPID_API
- **Benefit:** Single source of truth, audit trail
- **Status:** [ ] Not Started

---

## Phase 4: Quality & Compliance

### 4.1 Add Error Handling to QUE-Medicare API Proxy ✅
- **Problem:** Functions don't check response codes, JSON parse can fail silently
- **Files:** `QUE-Medicare/Code.gs` (11 functions refactored)
- **Fix:** Refactored to use RAPID_CORE.callApi() - proper response codes + JSON handling
- **Status:** [x] **COMPLETE** (2026-02-04)
- **Delivered:** QUE-Medicare v1.1.0 - 100+ lines reduced to ~50 lines, all functions use callApi()

### 4.2 Extract Test Framework from Production
- **Current:** `SENTINEL_Testing.gs` (6,017 lines) lives in prod code
- **Target:** Move to `sentinel-v2/Docs/Testing/` or `_RPI_STANDARDS/testing/`
- **Status:** [ ] Not Started

### 4.3 Standardize Configuration Pattern
- **Problem:** Mix of hardcoded URLs vs Script Properties
- **Rule:** ALL API URLs, MATRIX IDs, secrets → Script Properties only
- **Audit:** PRODASH, QUE-Medicare, DAVID-HUB
- **Status:** [ ] Not Started

---

## Phase 5: DAVID-HUB Refinements

### 5.1 Create ActionRouter Pattern
- **Current:** `Code.gs` has long switch statement (17 action references)
- **Target:** Handler registry pattern for cleaner action dispatch
- **Status:** [ ] Not Started

### 5.2 Decouple Output Pipeline
- **Current:** `Output.gs` (931 lines) - PDF→Email→SMS→Slack→SENTINEL tightly coupled
- **Target:** Chain-of-responsibility or separate handler modules
- **Status:** [ ] Not Started

---

## Tracking

### Completion Checklist

| Phase | Item | Owner | Status | Completed |
|-------|------|-------|--------|-----------|
| 1.1 | Extract callApi() | GA | **DONE** | 2026-02-04 |
| 1.2 | Extract readMatrixSheet() | GA | **DONE** | 2026-02-04 |
| 1.3 | Add PHI masking utilities | GA | **DONE** | 2026-02-04 |
| 2.1 | Split PRODASH/Index.html | - | Not Started | |
| 2.2 | Assess sentinel-v2 HTML | - | Not Started | |
| 2.3 | Create shared UI library | - | Not Started | |
| 3.1 | Split IMPORT_GHL.gs | - | Not Started | |
| 3.2 | Standardize RAPID_CORE returns | - | Not Started | |
| 3.3 | Migrate imports to RAPID_API | - | Not Started | |
| 4.1 | QUE-Medicare error handling | GA | **DONE** | 2026-02-04 |
| 4.2 | Extract test framework | - | Not Started | |
| 4.3 | Standardize config pattern | - | Not Started | |
| 5.1 | DAVID-HUB ActionRouter | - | Not Started | |
| 5.2 | DAVID-HUB Output pipeline | - | Not Started | |

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
