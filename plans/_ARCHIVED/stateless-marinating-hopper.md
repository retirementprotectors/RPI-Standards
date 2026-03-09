# PRODASH_MATRIX Data Quality & Normalization Cleanup Plan

## Context

After the CoF Members import (1,111 clients + 3,960 policies), PRODASH_MATRIX has ~5,200 clients and ~7,000+ accounts across 4 tabs. A `DEBUG_InventoryProdash` audit revealed 6 categories of data quality issues that need systematic cleanup. Additionally, RAPID_CORE's normalization engine has gaps (no status normalizer, incomplete carrier aliases) that let bad data slip through. The goal is to fix RAPID_CORE first, then run all existing data through normalization, then clean up specific issues, and finally prepare for Janet's policy detail data.

---

## Phase 0: Expand RAPID_CORE Normalizers

**Files:** `/Users/joshd.millang/Projects/RAPID_TOOLS/RAPID_CORE/CORE_Normalize.gs`, `CORE_Database.gs`

### 0A. Add `normalizeStatus()` function
- New function in `CORE_Normalize.gs` (~line 510)
- STATUS_MAP handles known variants: `"acive"→"Active"`, `"a"→"Active"`, `"i"→"Inactive"`, `"active- internal"→"Active- INTERNAL"`, `"active- external"→"Active- EXTERNAL"`, empty→leave blank (don't default)
- Preserves compound statuses like "Active- INTERNAL" with proper casing

### 0B. Add status to FIELD_NORMALIZERS
- In `CORE_Database.gs` (line ~986), add `status: 'status'`, `client_status: 'status'`
- In `normalizeData_()` switch statement (~line 1020), add case for `'status'`

### 0C. Expand CARRIER_ALIASES
- Currently 21 entries — add missing carriers found in PRODASH data:
  - `'catholic order of foresters'` → `'Catholic Order of Foresters'`
  - `'cof'` → `'Catholic Order of Foresters'`
  - `'kansas city life'` / `'kcl'` → `'Kansas City Life'`
  - `'north american company'` / `'nac'` → `'North American Company'`
  - `'national western'` / `'nwl'` → `'National Western Life'`
  - `'great western'` → `'Great Western Insurance'`
  - `'american equity'` → `'American Equity'`
  - `'athene'` → `'Athene'`
  - `'global atlantic'` → `'Global Atlantic'`
  - Any others discovered during normalization DryRun

### 0D. Add date guard for day-of-week strings
- `normalizeDate()` currently doesn't handle inputs like `"Monday"` or `"Wed"` — should return `''` (blank) for non-date strings
- Add early return at top of function: if input matches day-of-week pattern, return `''`

### 0E. Push RAPID_CORE changes
- `clasp push --force` to RAPID_CORE (library, no deploy needed)
- All downstream projects (RAPID_IMPORT, RAPID_API, PRODASH, SENTINEL) auto-inherit via library binding

**Verification:** Run existing unit tests in RAPID_CORE if available, or manual spot-check of each normalizer with edge cases.

---

## Phase 1: Normalize All Existing Data

**Tool:** `RAPID_CORE.normalizeExistingData(tabName, options)` — already exists at `CORE_Reconcile.gs:60-168`

Run on all 6 PRODASH_MATRIX tabs in order:

| Order | Tab | Est. Rows | Why This Order |
|-------|-----|-----------|----------------|
| 1 | `_CLIENT_MASTER` | ~5,200 | Clients first — name/phone/email normalization |
| 2 | `_ACCOUNT_MEDICARE` | ~5,100 | Largest account tab |
| 3 | `_ACCOUNT_LIFE` | ~4,900 | Second largest (includes CoF) |
| 4 | `_ACCOUNT_ANNUITY` | ~850 | |
| 5 | `_ACCOUNT_BDRIA` | ~250 | |
| 6 | `_PRODUCER_MASTER` | ~50 | SENTINEL tab, small |

**Process per tab:**
1. DryRun: `normalizeExistingData('_TAB_NAME', { dryRun: true })` — review change log
2. If changes look correct, Live: `normalizeExistingData('_TAB_NAME', { dryRun: false })`
3. Status fields will now normalize via the new `normalizeStatus()` from Phase 0

**Timeout risk:** `normalizeExistingData()` writes cell-by-cell. For 5,000+ row tabs with many changes, may need batching. If timeout occurs, run with `{ dryRun: false, batchSize: 25 }` or split by row range.

---

## Phase 2: Targeted Backfills

**File:** `/Users/joshd.millang/Projects/RAPID_TOOLS/RAPID_IMPORT/IMPORT_BoBEnrich.gs` (new FIX_ functions)

### 2A. Client Status Backfill
- ~4,790 clients with blank `client_status`
- New function `FIX_BackfillClientStatus_()` with DryRun/Live pattern
- Logic: If `client_status` is blank AND client has at least one linked active account → set `"Active- INTERNAL"`
- Clients with no linked accounts → leave blank for manual review

### 2B. Client State Backfill
- ~885 clients with blank `state`
- Logic: If `state` is blank AND `zip` is filled → resolve state from zip via lookup table
- If `mailing_state` is filled → copy to `state`

### 2C. Medicare Date Cleanup
- Fix `effective_date` and `term_date` fields containing day-of-week strings ("Monday", "Tuesday")
- After Phase 0D adds the guard, run `normalizeExistingData('_ACCOUNT_MEDICARE')` again — it will blank out the garbage dates
- Or write a targeted FIX_ function if there are many

---

## Phase 3: Orphan Resolution

**Existing tools available:**
- `FIX_BackfillOrphanClientIds()` in `IMPORT_GHL.gs:3472` — links via `ghl_contact_id`
- `FIX_OrphanCleanup()` in `IMPORT_Approval.gs:19025` — auto-link by policy#, soft-delete empty orphans

### 3A. Run GHL orphan linker first
- `FIX_BackfillOrphanClientIds()` — DryRun then Live
- This links accounts that have `ghl_contact_id` but missing `client_id`

### 3B. Run general orphan cleanup
- `FIX_OrphanCleanup()` — DryRun then Live
- Links orphans by matching `policy_number` to already-linked accounts
- Soft-deletes orphans with no policy number at all
- Remaining orphans logged for manual review

### 3C. Run CoF-specific orphan linking
- New CoF members may have orphaned accounts from earlier imports
- Check if any `_ACCOUNT_LIFE` records with carrier "Catholic Order of Foresters" lack `client_id`
- Match by `policy_number` against CoF client data

---

## Phase 4: Reconciliation Pass

**Existing tools:** `RAPID_CORE.reconcileClients(options)`, `RAPID_CORE.reconcileAccounts(options)`

### 4A. Client Dedup
- `reconcileClients({ dryRun: true, scoreThreshold: 70 })` — get duplicate pair report
- Review pairs: auto-merge 85+ (high confidence), manual review 70-84
- The CoF import created 160 matched clients — some may now be duplicates with better data

### 4B. Account Dedup
- `reconcileAccounts({ dryRun: true })` — get duplicate + orphan report
- Focus on cross-tab duplicates (same policy in `_ACCOUNT_LIFE` and `_ACCOUNT_ANNUITY`)

### 4C. Review via Reconcile UI
- Use the web app reconciliation page: `?page=reconcile`
- Side-by-side comparison for medium-confidence pairs

---

## Phase 5: CoF Enrichment P1

**Existing function:** `FIX_EnrichClientsFromCoFContacts()` in `IMPORT_BoBEnrich.gs:302-305`

- 699 CoF contact records with DOB, phone, address, Medicare number
- Now that 1,111 CoF clients exist in `_CLIENT_MASTER`, this enrichment should have many more matches
- DryRun first to verify match rate, then Live

---

## Phase 6: Janet's Policy Detail Data (Blocked — Waiting for Dataset)

**Prerequisite:** JDM provides the CoF policy detail dataset with product types, product names, policy types

### 6A. Python Preprocessing
- Convert to inline JS (same pattern as CoF member import)
- Key = `cof_member_id` or `policy_number`

### 6B. GAS Enrichment Function
- New `FIX_EnrichCoFPolicyDetails_()` in `IMPORT_BoBEnrich.gs`
- Match by `policy_number` against `_ACCOUNT_LIFE` records
- Fill: `product_type`, `product_name`, `policy_type`
- Move annuity policies to `_ACCOUNT_ANNUITY` if product_type resolves to annuity

### 6C. Post-Enrichment Normalization
- Run `normalizeExistingData('_ACCOUNT_LIFE')` and `normalizeExistingData('_ACCOUNT_ANNUITY')` to normalize new values

---

## Phase 7: Final Verification

- Re-run `DEBUG_InventoryProdash()` — compare against pre-cleanup baseline
- Confirm 0 orphaned accounts, 0 blank client statuses (on linked clients), carrier names standardized
- Run `reconcileClients()` and `reconcileAccounts()` one final time — confirm no new duplicates
- Spot-check 10 random CoF clients: verify `cof_member_id`, linked policies, data completeness

---

## Execution Summary

| Phase | Effort | Dependencies | Risk |
|-------|--------|--------------|------|
| 0 — RAPID_CORE expansion | Medium | None | Low (library, auto-inherited) |
| 1 — Normalize all data | Low | Phase 0 | Medium (timeout on large tabs) |
| 2 — Targeted backfills | Medium | Phase 1 | Low |
| 3 — Orphan resolution | Low | Phase 2 | Low (existing tools) |
| 4 — Reconciliation | Medium | Phase 3 | Medium (manual review needed) |
| 5 — CoF enrichment P1 | Low | Phases 1-3 | Low (existing function) |
| 6 — Janet's policy data | Medium | JDM provides dataset | Blocked |
| 7 — Final verification | Low | All above | None |

**Key files to modify:**
- `RAPID_CORE/CORE_Normalize.gs` — new `normalizeStatus()`, expanded aliases, date guard
- `RAPID_CORE/CORE_Database.gs` — add status to FIELD_NORMALIZERS + normalizeData_() switch
- `RAPID_IMPORT/IMPORT_BoBEnrich.gs` — new FIX_ backfill functions (status, state, CoF enrichment)
- `RAPID_IMPORT/IMPORT_BoBImport.gs` — Phase 6 CoF policy detail import (when data arrives)

**Deploy notes:**
- RAPID_CORE: `clasp push --force` only (library, no version/deploy needed)
- RAPID_IMPORT: `clasp push --force` only for FIX_ functions (editor-only, no web app deploy)
