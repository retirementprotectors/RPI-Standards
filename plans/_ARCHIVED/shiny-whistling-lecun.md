# RAPID_IMPORT Comprehensive Upgrade Plan

## Context

RAPID_IMPORT is a 69,500-line GAS data import + approval platform with 169 functions across 15 files. A deep dive revealed compliance gaps (SSN exposure, missing confirmations), backend capabilities with no frontend exposure, and an opportunity to add API-powered data validation. JDM also asked about integrating WhitePages (already subscribed), Google Places autocomplete, address verification, phone type detection, and email validation.

This plan addresses all findings in execution priority order.

---

## Open Questions for JDM (4 from Deep Dive)

These decisions don't block Phase 1-2 work but need answers before Phase 3+:

| # | Question | Recommendation | Impact |
|---|----------|---------------|--------|
| Q1 | Should BoB raw data dump files stay in git? (~13K lines inline in FIX_ functions) | **Archive to Drive folder**, remove from git. Git history preserves them. | Cuts IMPORT_Approval.gs from 20K→7K lines |
| Q2 | Should executed FIX_ functions be archived out of active code? | **Yes** — move to `IMPORT_Archive.gs` (keep in project, just separate file) | Cleaner active codebase |
| Q3 | Should RAPID_API boundary include operational tabs (_CASE_TASKS, _INTAKE_QUEUE)? | **Yes** — RAPID_API should route ALL MATRIX writes, including operational tabs | Consistency, single source of truth |
| Q4 | Keep `developmentMode: true` on RAPID_CORE or pin to version? | **Pin to version for production stability**, use HEAD only during active RAPID_CORE development | Prevents accidental regressions |

**Q5 (NEW)**: Does your WhitePages Pro subscription include **API access** (developer key)? Or is it just the web portal for manual lookups? Check your account settings for an API key. This determines Phase 4 scope.

---

## Phase 1: Compliance & Security Fixes (P0)

**Zero risk tolerance. Fix before anything else.**

### 1.1 SSN Masking in APPROVAL_UI.html
- **File**: `APPROVAL_UI.html`
- **Problem**: SSN values visible in `current_value` column — PHI violation risk
- **Fix**: Add client-side masking function. When field name contains `ssn`, display `***-**-XXXX` (last 4 only). Already have `maskSsn_()` in `IMPORT_Client.gs` — replicate pattern in frontend JS.
- **Pattern**: `if (fieldName.toLowerCase().includes('ssn')) value = '***-**-' + value.slice(-4);`

### 1.2 SSN Masking in RECONCILE_UI.html
- **File**: `RECONCILE_UI.html`
- **Problem**: Full SSN visible in merge comparison field grid
- **Fix**: Same masking pattern as 1.1 applied to field comparison renderer

### 1.3 Confirmation Dialog Before "DONE - Execute Writes"
- **File**: `APPROVAL_UI.html`
- **Problem**: No confirmation before writing to production MATRIX. Accidental click = bad data in production.
- **Fix**: Add `showConfirmation()` modal (per RPI code standards — NOT `confirm()`) before `executeApprovedBatchFromUI()`. Show summary: X fields approved, Y edited, Z killed.

### 1.4 Confirmation Dialogs in RECONCILE_UI.html
- **File**: `RECONCILE_UI.html`
- **Problem**: Delete and Bulk Auto-Merge have NO confirmation
- **Fix**: Add `showConfirmation()` modal before `deleteRecordFromUI()` and `fullAutoMergeForUI()`. Show: "This will merge X records. This cannot be undone."

### 1.5 DEBUG_DumpScriptProperties Secret Exposure
- **File**: `IMPORT_Approval.gs` (or wherever this function lives)
- **Problem**: Dumps ALL Script Properties including API keys and tokens to Logger
- **Fix**: Filter output to exclude keys containing `token`, `key`, `secret`, `password`, `api`. Or remove function entirely.

### 1.6 SECURITY_COMPLIANCE.md Tracker Update
- **File**: `_RPI_STANDARDS/reference/compliance/SECURITY_COMPLIANCE.md`
- **Problem**: RAPID_IMPORT listed as "Not verified" in org-only access table
- **Fix**: Verify `appsscript.json` has `"access": "DOMAIN"`, update tracker with date

### 1.7 appsscript.json Source File Audit
- **File**: `RAPID_IMPORT/appsscript.json`
- **Problem**: Need to verify source file matches GAS editor setting (per GAS Gotcha #11)
- **Fix**: Read file, confirm `"webapp": { "access": "DOMAIN" }`. If wrong, fix source file.

---

## Phase 2: Code Quality & Bug Fixes (P1)

### 2.1 ZIP Zero-Pad Fix (RAPID_CORE + RAPID_IMPORT)
- **Files**: `RAPID_CORE/CORE_Normalize.gs` → `normalizeZip()`, `RAPID_IMPORT/IMPORT_Validation.gs` → `validateZip_()`
- **Problem**: 4-digit zips (VT: 05819, NH, etc.) don't get zero-padded. Fall through as raw `5819`.
- **Fix in CORE_Normalize.gs**:
  ```javascript
  if (digits.length === 4) return '0' + digits;  // Zero-pad 4-digit zips
  ```
- **Fix in IMPORT_Validation.gs**: Same pattern in `validateZip_()`
- **Deploy**: RAPID_CORE clasp push + new version. Then RAPID_IMPORT clasp push.

### 2.2 DryRun for FIX_ImportBoBData
- **File**: `IMPORT_Approval.gs`
- **Problem**: BoB import functions execute live writes with no preview option
- **Fix**: Add `dryRun` parameter (default `true`) to FIX_ImportBoBData functions. When `dryRun=true`, return `{ wouldInsert: N, wouldUpdate: N, sample: [...] }` without writing.

### 2.3 Home Page "Loading Status" Fix
- **File**: `Code.gs` → `createHomePage_()`
- **Problem**: Reconciliation and Drive Hygiene status cards show "Loading status..." but never load async data
- **Fix**: Add `google.script.run` calls on page load to fetch `getLastReconciliationTimeForUI()` and `getLastDriveHygieneTimeForUI()`, populate cards with actual timestamps

### 2.4 Queue Depth on Home Page
- **File**: `Code.gs` → `createHomePage_()`
- **Problem**: No indication of pending work (approval queue depth, intake queue counts)
- **Fix**: Add async calls to `getApprovalQueueCountForUI()` and `getIntakeQueueCountsForUI()` on page load. Display badge counts on relevant cards.

### 2.5 Stale CLAUDE.md References
- **File**: `RAPID_IMPORT/CLAUDE.md`
- **Problem**: May reference old paths, outdated version numbers, or missing module descriptions
- **Fix**: Update to reflect current state (v3.20.2, all 15 files, 169 functions, current deploy ID)

---

## Phase 3: Frontend/Backend Gap Closure (P2)

### What the Backend Has That the Frontend Doesn't Expose

| Backend Capability | Missing From | Proposed Fix |
|-------------------|-------------|-------------|
| `getApprovalQueueCountForUI()` | Home page | Add badge count to Approval card |
| `getIntakeQueueCountsForUI()` | Home page | Add per-channel queue counts |
| `getQueueStatusDetailForUI()` | Anywhere | Add to home page status panel |
| `searchApprovalBatchesForUI()` | Approval page | Add search bar at top of approval page |
| `bulkOrphanLinkFromUI()` | Reconcile page | Add multi-select + "Link All" button |
| `getEmailInboxConfigForUI()` | Home page | Add Email Config card or link |
| Confidence scores | Approval/Training | Show extraction confidence % per field |

### 3.1 Approval Batch Search
- **File**: `APPROVAL_UI.html`
- **Fix**: Add search input that calls `searchApprovalBatchesForUI(query)`. Display results as clickable batch cards. Currently users need the exact batch_id URL.

### 3.2 Bulk Orphan Linking
- **File**: `RECONCILE_UI.html`
- **Fix**: Add multi-select checkboxes to orphan cards. "Link All Selected to Client" button that calls `bulkOrphanLinkFromUI()` with array of orphan IDs.

### 3.3 Orphan Search Pagination
- **File**: `RECONCILE_UI.html`
- **Fix**: Add pagination to `searchClientsForUI()` results. Currently maxes at 220px height with no scroll indicator. Add "Load More" or proper pagination.

### 3.4 Merge Summary Before Execute
- **File**: `RECONCILE_UI.html`
- **Fix**: Before final "Merge" button, show summary modal: "Keeper: [Name], Loser: [Name], Fields from keeper: X, Fields from loser: Y". Requires building preview from field selections.

### 3.5 Email Inbox Configuration Link
- **File**: `Code.gs` → `createHomePage_()`
- **Fix**: Add card or link to email inbox configuration. Backend has `getEmailInboxConfigForUI()` but no UI exposes it.

---

## Phase 4: API Integration Architecture

### The Answer: Layered Architecture

```
LAYER 1: Frontend HTML (ProDashX, Sentinel, RIIMO forms)
  └── Google Places Autocomplete widget (client-side JS)

LAYER 2: RAPID_CORE (shared GAS library)
  └── New file: CORE_Validation_API.gs
      - validateAddress_viaAPI(address)
      - validatePhone_viaAPI(phone)
      - validateEmail_viaAPI(email)
      - enrichContact_viaAPI(name, phone, email, address)
      - API keys in Script Properties (NOT in RAPID_CORE code)

LAYER 3: RAPID_IMPORT (bulk orchestration)
  └── New file: IMPORT_BulkValidation.gs
      - FIX_BulkValidatePhones(dryRun)
      - FIX_BulkValidateEmails(dryRun)
      - FIX_BulkValidateAddresses(dryRun)
      - Rate limiting, batching, result storage

LAYER 4: MCP-Hub (future, lower priority)
  └── validate_contact, enrich_contact tools
```

### Why This Layering

| API | Where It Lives | Why |
|-----|---------------|-----|
| **Google Places Autocomplete** | Frontend HTML templates | Client-side widget, must be in browser |
| **WhitePages Pro wrappers** | RAPID_CORE | Every project needs validation — shared library |
| **Bulk validation** | RAPID_IMPORT | Import is where bulk data enters the system |
| **MCP tools** | MCP-Hub (future) | Nice-to-have for Claude-assisted workflows |

### What's NOT in RAPID_IMPORT or RAPID_CORE

Google Places Autocomplete goes into **ProDashX** and **Sentinel** frontend HTML only. It's a UX widget, not a data pipeline component. RAPID_IMPORT doesn't have data entry forms — it processes data that's already been entered elsewhere.

### Services & Costs

| Service | What For | One-Time (3,500 records) | Monthly Ongoing |
|---------|----------|------------------------|-----------------|
| WhitePages Pro | Phone type + address + email + identity | Included in subscription | Included |
| Google Places Autocomplete | Frontend address widget | FREE | FREE (under 10K/mo) |
| NeverBounce | Deep email hygiene | ~$28 | ~$0.50-1.00 |
| Google Address Validation | CASS-certified standardization | ~$60 | ~$2 |
| **Total** | | **~$88** | **~$3/month** |

### Implementation Steps (Phase 4)

1. **JDM confirms**: WhitePages Pro API key access (not just web portal)
2. **JDM enables**: Google Places API + Maps JS API in GCP project `90741179392`
3. **Build**: `CORE_Validation_API.gs` in RAPID_CORE — WhitePages Pro wrappers
4. **Build**: `IMPORT_BulkValidation.gs` in RAPID_IMPORT — batch runner with DryRun
5. **Build**: Google Places Autocomplete in ProDashX + Sentinel HTML templates
6. **Run**: NeverBounce bulk email clean ($28) + bulk phone type detection
7. **Run**: Google Address Validation bulk clean ($60) if physical mail is needed

---

## Phase 5: Maintainability & Architecture (P3)

### 5.1 Archive Executed FIX_ Functions (if Q1/Q2 approved)
- Move executed BoB import functions + inline data to `IMPORT_Archive.gs`
- Keep in project for reference but out of active code path
- Reduces `IMPORT_Approval.gs` from ~20K to ~7K lines

### 5.2 Pin RAPID_CORE Library Version (if Q4 approved)
- Change `developmentMode: true` to `false` in RAPID_IMPORT's library reference
- Pin to current RAPID_CORE version (v51)
- Switch to HEAD only during active RAPID_CORE development sessions

### 5.3 Update RAPID_IMPORT CLAUDE.md
- Reflect current state: v3.20.2, 15 files, 169 functions
- Document all ForUI functions and which page exposes them
- Add API integration architecture once built
- Reference all current deploy IDs

### 5.4 Add callRapidAPI_ Timeout
- **File**: Wherever `callRapidAPI_()` is defined
- **Problem**: No timeout — can hang indefinitely
- **Fix**: Add `muteHttpExceptions: true` and timeout parameter to `UrlFetchApp.fetch()` options

---

## Backend Inventory Summary (169 Functions)

| Category | Count | Key Functions |
|----------|-------|--------------|
| Intake & Scanning | 16 | `scanIntakeQueue()`, `scanMeetingQueue()`, `scanMailQueue()`, `scanEmailQueue()` |
| Extraction & Parsing | 12 | `extractFieldsFromDocument_()`, `parseAgentNIPR()`, `parseCRMExport()` |
| Approval Workflow | 18 | `createApprovalBatch()`, `executeApprovedBatch()`, `bulkUpdateApprovalBatch()` |
| GHL Integration | 35 | `fetchGHLContacts()`, `mapGHLContactToClient()`, `importGHLAccounts()` |
| BoB Enrichment | 14 | `FIX_ImportBoBData()`, `FIX_EnrichFromHumanaBoB()`, `FIX_LinkOrphanAccounts()` |
| Validation | 12 | `validateClient()`, `validateAccount()`, `validateAgent()`, `validateRevenue()` |
| Client/Account/Agent/Revenue CRUD | 22 | `importClient()`, `importAccount()`, `importAgent()`, `importRevenue()` |
| Reconciliation UI | 10 | `bulkAutoMergeDryRunForUI()`, `fullAutoMergeForUI()`, `mergeDuplicateFromUI()` |
| Case Tasks | 6 | `getCaseTasksForUI()`, `updateCaseTaskFromUI()` |
| Drive Hygiene | 5 | `driveDedup()`, `getDriveDuplicatesForUI()`, `trashDriveFileFromUI()` |
| Testing | 18 | `TEST_All()`, `TEST_AgentOnly()`, `TEST_ValidationOnly()`, entity tests |
| AI3 Document Gen | 11 | `generateAi3()`, `buildAi3ServiceCenters_()`, `buildAi3TotalPicture_()` |

### Identified Gaps
- No approval audit trail (who approved what, when)
- No approval SLA tracking
- No API error recovery / retry logic
- No batch splitting for large approval batches (6MB GAS limit)
- No two-way GHL sync (changes in MATRIX don't sync back to GHL)

### Identified Redundancies
- `getMatrixSpreadsheet_()` defined in 3 different files (Code.gs, IMPORT_Client.gs) — should consolidate
- `findExistingAgent()` in both IMPORT_Agent.gs and IMPORT_Client.gs — should use single source
- `generateUUID()` and `generateGHLUUID_()` appear to do the same thing

---

## Execution Order

```
Phase 1 (Compliance)     → Immediate. ~2-3 hours. Deploy same day.
Phase 2 (Code Quality)   → Next session. ~3-4 hours. RAPID_CORE + RAPID_IMPORT deploys.
Phase 3 (Frontend Gaps)  → Following session. ~4-6 hours. RAPID_IMPORT deploy only.
Phase 4 (API Integration) → After JDM confirms WhitePages API + enables Google Places.
                            RAPID_CORE + RAPID_IMPORT + ProDashX + Sentinel deploys.
Phase 5 (Maintainability) → After Q1-Q4 decisions. Can parallel with Phase 3-4.
```

---

## Verification Plan

### Phase 1 Verification
- [ ] Open APPROVAL_UI, confirm SSN shows `***-**-XXXX` not full value
- [ ] Open RECONCILE_UI, confirm SSN masked in merge comparison
- [ ] Click "DONE - Execute Writes" → confirmation modal appears (not direct execute)
- [ ] Click "Merge All" in Reconcile → confirmation modal appears
- [ ] Run `DEBUG_DumpScriptProperties` → verify no tokens/keys in output
- [ ] Check `appsscript.json` → `"access": "DOMAIN"` confirmed

### Phase 2 Verification
- [ ] Import a 4-digit zip (e.g., `5819`) → verify it becomes `05819`
- [ ] Run FIX_ImportBoBData with dryRun=true → verify no writes, get preview
- [ ] Load home page → reconciliation status shows actual timestamp (not "Loading...")
- [ ] Load home page → approval queue count badge visible

### Phase 3 Verification
- [ ] Search for approval batch by client name → results appear
- [ ] Select 3 orphans → "Link All" → all linked to selected client
- [ ] Merge two records → summary modal shows before final execute

### Phase 4 Verification
- [ ] Type address in ProDashX form → Google Places dropdown appears
- [ ] Run `FIX_BulkValidatePhones(true)` → dry run shows phone types found
- [ ] Run `FIX_BulkValidateEmails(true)` → dry run shows valid/invalid counts
