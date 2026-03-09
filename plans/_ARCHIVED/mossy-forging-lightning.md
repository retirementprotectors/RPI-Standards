# Plan: Migrate PRODASHX from ghl_contact_id to client_id

## Context

PRODASHX uses `ghl_contact_id` (GoHighLevel legacy ID) as the primary foreign key for linking accounts to clients. GHL is being phased out — new accounts (like the Sprenger BD/RIA imports) use `client_id` (UUID) instead. The codebase has 107 GHL references across 15 files, and account lookups fail for any record that doesn't have `ghl_contact_id` set. This migration makes `client_id` the sole primary key.

## Current State

- **`_CLIENT_MASTER`**: Has both `client_id` (UUID) and `ghl_contact_id` (legacy). `client_id` is the authoritative key.
- **Account sheets** (`_ACCOUNT_ANNUITY`, `_ACCOUNT_LIFE`, `_ACCOUNT_MEDICARE`, `_ACCOUNT_BDRIA`): Schema defines both `client_id` and `ghl_contact_id` columns. Legacy rows only have `ghl_contact_id` populated. New rows (Sprenger) only have `client_id`.
- **Frontend**: Uses `sessionStorage.setItem('selectedClientId', ...)` — already passes whatever ID the server returns as `id`. The server currently returns `client_id || id` as the primary ID (PRODASH_Clients.gs:539,554).
- **Account lookups**: Multiple functions match `ghl_contact_id` first, `client_id` as fallback.

## Plan

### Phase 1: Backfill `client_id` on all account rows (data fix)

Write a `FIX_BackfillAccountClientIds()` function in `DEBUG_API.gs`:
1. Read `_CLIENT_MASTER` → build map: `ghl_contact_id → client_id`
2. For each account sheet (`_ACCOUNT_ANNUITY`, `_ACCOUNT_LIFE`, `_ACCOUNT_MEDICARE`, `_ACCOUNT_BDRIA`, `_ACCOUNT_BANKING`):
   - Find `client_id` and `ghl_contact_id` column indexes
   - For every row where `client_id` is empty but `ghl_contact_id` exists: look up the UUID from the map and write it
3. Return counts: `{ sheet: rows_updated }`

**Files**: `DEBUG_API.gs` (new function, one-time)

### Phase 2: Swap lookup order in all server functions (code change)

Change every `ghl_contact_id || client_id` pattern to `client_id || ghl_contact_id`. This is safe because after Phase 1, all rows will have `client_id` populated. The GHL fallback stays for safety.

**Files to modify** (13 files, ~40 line changes):

| File | Changes |
|------|---------|
| `PRODASH_Clients.gs` | Lines 489,496,540: swap FK resolution order. Line 568: keep `ghlContactId` in response but deprioritize. Lines 688,721: swap match order. |
| `PRODASH_CLIENT360.gs` | Lines 338-341: already dual-keyed (no change needed). Lines 575-583,682-697: already fixed in this session. Line 704: swap `account_id || ghl_object_id` order (already correct). |
| `Code.gs` | Lines 1542,1724,1776-1806,2206,2254,2275: swap all fallback patterns |
| `PRODASH_Accounts.gs` | Lines 372-373,577,627-637: swap FK and account ID resolution |
| `PRODASH_RMD_CENTER.gs` | Lines 40,80-81: swap patterns |
| `PRODASH_SERVICE_CENTERS.gs` | Lines 36,246,321: swap patterns |
| `PRODASH_SALES_CENTERS.gs` | Lines 41,97: swap patterns |
| `PRODASH_BENI_CENTER.gs` | Lines 31,45: swap patterns |
| `PRODASH_QUE_MEDICARE.gs` | Lines 44,154: swap patterns |
| `PRODASH_MEDICARE_REC.gs` | Lines 84,450,485,514: swap patterns |
| `PRODASH_DISCOVERY_PDF.gs` | Line 394: swap pattern |
| `Scripts.html` | Lines 105,916,2307-2308: swap to prefer `client_id` |

### Phase 3: Remove `ghl_contact_id` from CLIENT360 response contract

Update `uiGetClients()` and `uiGetClientById()` responses:
- Keep `ghlContactId` field for now (backward compat) but ensure `id` always returns `client_id`
- Update outdated JSDoc comments (lines 552, 601 in CLIENT360)

**Files**: `PRODASH_Clients.gs`, `PRODASH_CLIENT360.gs`

### Phase 4: Clean up RAPID_CORE schemas (future, not this session)

Eventually remove `ghl_contact_id` and `ghl_object_id` from account schemas entirely. Not doing this now — the columns stay as historical data, they just stop being the lookup key.

## Execution Order

1. Run Phase 1 (backfill data) — must complete before Phase 2
2. Phase 2 + 3 together (code changes) — single deploy
3. Verify via CLIENT360 for multiple clients (GHL-imported + UUID-imported)
4. Delete one-time FIX function
5. Deploy + commit

## Verification

1. After Phase 1: Run a DEBUG function to confirm 0 account rows have empty `client_id`
2. After Phase 2+3: Pull up CLIENT360 for:
   - Randy Sprenger (has both GHL + UUID accounts)
   - Margo Sprenger (same)
   - A legacy-only client (GHL accounts only, no UUID accounts)
3. Confirm all accounts appear in all three cases
4. Test pipeline/casework views still work
