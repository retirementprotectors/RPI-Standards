> ARCHIVED: Consolidated into prodashx-platform-roadmap.md (Stream 8: Performance - Unified Matrix Cache) on 2026-03-08

# PRODASHX Performance Refactor: Unified Matrix Cache

## Context

PRODASHX loads slowly because every UI function independently opens the PRODASHX_MATRIX spreadsheet and reads full sheets. A single CLIENT360 view triggers 5 `SpreadsheetApp.openById()` calls and up to 16 `getDataRange().getValues()` reads. Dashboard triggers 4 opens and 8 reads. The data volume is small (~3K rows / 200K cells) — the problem is redundant reads, not data size. BigQuery is not needed.

**Goal:** Consolidate all MATRIX reads into a single cached scanner. One spreadsheet open, 7 sheet reads, cached for 60 seconds. All consumers use the cache instead of independent reads.

---

## Phase 1: Create `PRODASH_MatrixCache.gs` (NEW FILE)

**The core of the refactor.** One file, one scanner, all indexes.

### What it provides:
- `getMatrixId_()` — unified MATRIX ID getter (replaces both `getProdashxMatrixId_()` and `getProdashMatrixId_()`)
- `scanMatrix_()` — opens PRODASHX_MATRIX ONCE, reads all 7 sheets, builds all indexes, caches 60s
- `getClient_(id)` — O(1) lookup by client_id OR ghl_contact_id (replaces linear scans)
- `getAllClients_()` — returns deduplicated client array (replaces `readClientsFromMatrix_()`)
- `getAllAccounts_(type)` — returns accounts by type or all (replaces `readAccountsFromMatrix_()`)
- `getAccountsForClient_(clientId, type)` — indexed lookup (replaces full-sheet-then-filter)
- `getAccountTypesMap_()` — client badge flags (replaces `getAccountTypesByClient_()`)
- `getActivitiesForClient_(clientId, limit)` — indexed activity lookup (replaces `getClientActivitiesFromLog_()`)
- `getRecentActivities_(limit)` — for dashboard activity feed
- `getScanDataForServiceCenters_()` — backwards-compatible wrapper for RMD/BENI consumers
- `getScanDataForSalesCenters_(options)` — backwards-compatible wrapper for Sales Center consumers
- `invalidateMatrixCache_()` — called after writes to bust cache

### Cache structure:
```
{
  clientsById: { [id]: clientObj },     // dual-key: client_id + ghl_contact_id
  clientsList: [ clientObj, ... ],       // deduplicated array
  accounts: { annuity: [], life: [], medicare: [], bdria: [], banking: [] },
  accountsByClient: { [id]: { annuity: [], life: [], ... } },
  accountTypesByClient: { [id]: { annuity: true, life: false, ... } },
  activitiesByClient: { [id]: [ activityObj, ... ] },
  activitiesList: [ ... ]               // sorted desc, capped at 100
}
```

### Key patterns preserved:
- Client dedup by person-identity (name+phone+status priority) from `readClientsFromMatrix_()`
- Dual-key indexing (client_id + ghl_contact_id) from `scanSalesCenterData_()`
- Date formatting via `Utilities.formatDate()` from Sales/Service scanners
- Status filtering (skip deleted) from all existing scanners
- `var` (not `let`) for module-level caching (GAS requirement)

---

## Phase 2: Refactor Consumers (Modify 8 files)

All existing function SIGNATURES stay identical. Only internal implementation changes.

### `PRODASH_Clients.gs`
- `readClientsFromMatrix_()` → delegate to `getAllClients_()`
- `getAccountTypesByClient_()` → delegate to `getAccountTypesMap_()`
- `getMatrix_()` → remove (no longer needed)
- Remove local cache vars (`_clientMatrixCache`, `_clientMatrixCacheTime`, `_accountTypesCache`)
- `clearClientCache()` → calls `invalidateMatrixCache_()`
- Keep `getProdashxMatrixId_()` as thin wrapper → `getMatrixId_()` (backward compat)

### `PRODASH_Accounts.gs`
- `readAccountsFromMatrix_(type)` → delegate to `getAllAccounts_(type)` with type name mapping (`'annuities'`→`'annuity'`, `'bd_ria'`→`'bdria'`)
- `uiGetAccountForEdit(accountId, type)` (line 614) → use `getAllAccounts_(type)` + find by ID (no more SS open)
- `uiSearchClientsForLink()` (line 1066) → use `getAllClients_()` instead of independent SS open
- Remove local cache vars (`_accountMatrixCache`, `_accountMatrixCacheTime`)
- `clearAccountCache()` → calls `invalidateMatrixCache_()`

### `Code.gs`
- `uiGetDashboardStats()` (line 110) → use `getAllClients_()` + `getAllAccounts_()`. Remove the 3 separate `readAccountsFromMatrix_()` calls for annuities/bdria — filter the 'all' result in memory instead.
- `uiGetPriorityQueue()` (line 173) → use `getAllAccounts_('annuity')` + `getAllAccounts_('bdria')` + `getAllClients_()` (all hit cache)
- `uiGetRecentActivity()` (line 247) → use `getRecentActivities_(20)`
- `uiLogActivity()` → keep write logic, add `invalidateMatrixCache_()` after write

### `PRODASH_CLIENT360.gs`
- `uiGetClient360()` (line 290) → use `getClient_(clientId)` for O(1) lookup instead of full sheet scan (lines 305-356 replaced)
- `uiGetClient360Accounts()` (line 661) → use `getAccountsForClient_(clientId)` instead of 5 separate sheet reads (lines 665-727 replaced)
- `getClientActivitiesFromLog_()` (line 605) → use `getActivitiesForClient_(clientId, limit)` (lines 608-651 replaced)
- `getClientAccountsFromMatrix_()` (line 556) → use `getAccountsForClient_(clientId)`
- `uiGetContactSummary()` (line 1782) → use `getClient_(clientId)` + `getAccountsForClient_(clientId)`
- `uiGenerateAi3ForUI()` (line 1242) → use cache for client + account reads

### `PRODASH_SALES_CENTERS.gs`
- `scanSalesCenterData_(options)` → 1-line delegation to `getScanDataForSalesCenters_(options)`
- `getClientAccountsFromScan_()` — unchanged (already works with scan data shape)
- All downstream consumers (QUE_MEDICARE, etc.) — unchanged

### `PRODASH_SERVICE_CENTERS.gs`
- `scanServiceCenterData_()` → 1-line delegation to `getScanDataForServiceCenters_()`
- All downstream consumers (RMD_CENTER, BENI_CENTER, buildAi3*) — unchanged

### `PRODASH_CASE_CENTRAL.gs`
- Line 84 and 907: replace `SpreadsheetApp.openById()` client lookups with `getClient_(clientId)` + `getAccountsForClient_(clientId)`

### `PRODASH_MEDICARE_REC.gs`
- Line 74: replace `SpreadsheetApp.openById()` client lookup with `getClient_(clientId)`

### NOT modified (out of scope):
- `PRODASH_Migration.gs` — one-time migration utility, not hot path
- `DEBUG_API.gs` — diagnostic functions, leave as-is
- `PRODASH_DISCOVERY_KIT.gs` — only the `getProdashMatrixId_()` function at line 1031 becomes a thin wrapper
- `PRODASH_MEDICARE_API.gs` — writes to MATRIX, not reads (uses its own matrixId param)
- `Code.gs` pipeline/opportunity functions (lines 254-1317) — these use `_PIPELINES` and `_OPPORTUNITIES` sheets which are tiny and already fast. Out of scope.

---

## Phase 3: Cache Invalidation on Writes

Any function that WRITES to PRODASHX_MATRIX must call `invalidateMatrixCache_()` after the write:

- `Code.gs`: `uiLogActivity()`, `uiSaveClient()`, `uiSavePipeline()`, `uiSaveOpportunity()`
- `PRODASH_Accounts.gs`: `uiSaveAccount()`, `uiLinkAccountToClient()`
- `PRODASH_CLIENT360.gs`: `uiSaveClient360Field()`, `uiSaveNotes()`
- `PRODASH_CASEWORK.gs`: any case write functions

---

## Performance Impact

| Scenario | Before (opens/reads) | After (opens/reads) |
|----------|---------------------|---------------------|
| Dashboard load | 4 opens, 8 reads | 1 open, 7 reads (cold) OR 0/0 (cached) |
| CLIENT360 view | 5 opens, 16 reads | 0/0 (cached from dashboard) OR 1/7 (cold) |
| Accounts page | 1 open, 5 reads | 0/0 (cached) |
| Account stats | 5 opens, 5 reads | 0/0 (cached) |
| Service alerts | 2 opens, 9 reads | 0/0 (cached) |
| **Worst case (cold)** | — | **1 open, 7 reads (~2-3s)** |
| **Best case (warm)** | — | **0 opens, 0 reads (<50ms)** |

---

## Implementation Order

1. Create `PRODASH_MatrixCache.gs` with scanner + all accessors
2. Wire `PRODASH_SERVICE_CENTERS.gs` scanner (1-line swap, safest test)
3. Wire `PRODASH_SALES_CENTERS.gs` scanner (1-line swap)
4. Wire `PRODASH_Clients.gs` (delegate + remove local caches)
5. Wire `PRODASH_Accounts.gs` (delegate + remove local caches)
6. Wire `Code.gs` dashboard functions
7. Wire `PRODASH_CLIENT360.gs` (biggest win — 16 reads → 0)
8. Wire `PRODASH_CASE_CENTRAL.gs` + `PRODASH_MEDICARE_REC.gs`
9. Add `invalidateMatrixCache_()` calls to all write functions
10. Unify MATRIX ID getters (thin wrapper redirects)

---

## Verification

1. **Pre-deploy testing**: Run `DEBUG_Ping` via execute_script to confirm GAS connectivity
2. **Functional test**: Navigate PRODASHX — Dashboard → Clients → CLIENT360 → Accounts tab → Activity tab → RMD Center → back to Dashboard. Confirm all data loads correctly.
3. **Performance test**: Use browser DevTools Network tab to measure `google.script.run` call durations before and after. Target: Dashboard < 3s cold, < 500ms warm. CLIENT360 < 2s cold, < 500ms warm.
4. **Cache invalidation test**: Edit a client field, navigate away, navigate back — confirm the edit persists.
5. **Edge cases**: Client with only ghl_contact_id (no client_id), client with duplicate rows, new client with no accounts.

---

## Files Modified

| File | Action | Lines Changed (est.) |
|------|--------|---------------------|
| `PRODASH_MatrixCache.gs` | **NEW** | ~250 new |
| `PRODASH_Clients.gs` | Delegate to cache | ~80 simplified |
| `PRODASH_Accounts.gs` | Delegate to cache | ~60 simplified |
| `Code.gs` | Wire dashboard funcs | ~40 simplified |
| `PRODASH_CLIENT360.gs` | Indexed lookups | ~100 simplified |
| `PRODASH_SALES_CENTERS.gs` | 1-line scanner swap | ~55 removed |
| `PRODASH_SERVICE_CENTERS.gs` | 1-line scanner swap | ~55 removed |
| `PRODASH_CASE_CENTRAL.gs` | Use cache lookups | ~20 simplified |
| `PRODASH_MEDICARE_REC.gs` | Use cache lookup | ~10 simplified |
| `PRODASH_DISCOVERY_KIT.gs` | Thin wrapper redirect | ~5 changed |

**Net result:** ~250 new lines (cache), ~425 lines simplified/removed. SpreadsheetApp.openById() calls in hot paths: 44 → 1 (per 60s window).
