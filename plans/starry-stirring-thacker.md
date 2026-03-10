# PRODASHX Performance Fix v2 — Eliminate GAS Contention

## Context

v3.24.0 batched dashboard and client360 calls, but execution log shows functions STILL taking 30-130s. Root cause: **GAS web app per-user execution throttling**. When multiple `google.script.run` calls compete, a 5s function takes 60s+. The batching reduced call count but didn't prevent concurrent calls from competing.

Evidence: `uiGetDashboardPage` = 60s via web app vs 5s via execute_script (solo). `uiGetUnreadCounts` (a Chat API call with zero sheet reads) hit 130s once from pure contention.

Two interacting problems:
1. `callServer()` fires every call immediately — no queue, no throttle
2. Chat badge polling (60s) + message polling (30s) create persistent background contention

---

## Phase 1: Call Queue (HIGHEST IMPACT — Do First)

**What**: Replace `callServer()` with a serialized queue. Max 1 concurrent `google.script.run` at a time. Priority levels ensure user actions always run before background polling.

**Why this works**: Solo execution times are 2-5s. ALL the 30-130s overhead is GAS contention. Eliminating concurrency eliminates the overhead.

**File**: `Scripts.html` (lines 460-467)

Replace current `callServer`:
```javascript
function callServer(functionName, ...args) {
  return new Promise((resolve, reject) => {
    google.script.run.withSuccessHandler(resolve).withFailureHandler(reject)[functionName](...args);
  });
}
```

With queue implementation:
- Queue array: `{ fn, args, resolve, reject, priority }`
- `_queueRunning` boolean flag
- `_processQueue()`: if running, return; else sort by priority, shift, execute, set running=true; in success/failure handlers: set running=false, call _processQueue again
- Priority: `0` = user-initiated (default), `1` = init, `2` = background/polling
- New `callServerBg(functionName, ...args)` — same but inserts at priority 2

**CRITICAL**: `RPI_Connect.html` has **13 direct `google.script.run` calls** that bypass `callServer()`. ALL must be routed through the queue:
- Polling calls (`_fetchUnreadCounts` line 1380, `_loadMessages` polling path line 769, `_loadActiveMeets` line 1068) → use `callServerBg()`
- User-initiated calls (send message, create DM, mark read, load spaces, load favorites, search) → use `callServer()`

**Expected**: ALL functions drop from 30-130s → 2-8s (solo speed). Background polling never blocks user actions.

---

## Phase 2: Batch Init (4 calls → 1)

**What**: Create `uiGetAppInit()` server function that returns userInfo + permissions + entitlements + integrationURLs in one call.

**Why**: On DOMContentLoaded, 5 calls fire concurrently: `uiGetCurrentUserInfo`, `uiGetUserPermissions`, `uiGetUserEntitlements`, `uiGetDashboardPage`, `uiGetIFrameURLs`. With Phase 1's queue, the first 4 would serialize to 4 round-trips (~12s). Batching them into 1 call = ~3s.

**Server-side** (`Code.gs`):
```javascript
function uiGetAppInit() {
  var userInfo = uiGetCurrentUserInfo();
  var permissions = uiGetUserPermissions();
  var entitlements = uiGetUserEntitlements();
  var iframeURLs = uiGetIFrameURLs();
  return JSON.parse(JSON.stringify({
    success: true,
    data: { userInfo, permissions, entitlements, iframeURLs }
  }));
}
```
All four share one execution context → `RAPID_CORE.getUserHierarchy()` cache hits after first call.

**Client-side** (`Scripts.html`):
- Modify DOMContentLoaded handler to `await callServer('uiGetAppInit')` FIRST
- Apply userInfo, permissions, entitlements, URLs from single response
- THEN call `navigateTo(currentPage)` (dashboard call becomes next queue item)
- Remove standalone `loadIntegrationURLs()` call at line ~7238
- Remove `loadUserPermissions()` call from `initializeUser()`

**Expected**: Startup = 3s (init batch) + 5s (dashboard) = **~8s total** (was 60-130s)

---

## Phase 3: Batch Accounts Page (3 calls → 1)

**What**: Create `uiGetAccountsPage()` that returns accounts + stats + carriers in one call.

**Why**: Accounts page fires 3 concurrent calls (`uiGetAccounts` + `uiGetAccountStats` + `uiGetUniqueCarriers`), each reading the same 5 account sheets independently = 15 sheet reads. Within one execution, `_ensureAccounts()` caches after first read = 5 sheet reads total.

**Server-side** (`PRODASH_Accounts.gs`):
```javascript
function uiGetAccountsPage(filters, pagination) {
  var accountsResult = uiGetAccounts(filters, pagination);
  var statsResult = uiGetAccountStats();
  var carriersResult = uiGetUniqueCarriers();
  return JSON.parse(JSON.stringify({
    success: true,
    data: { accounts: accountsResult.data, stats: statsResult.data, carriers: carriersResult.data }
  }));
}
```

**Client-side** (`Scripts.html`):
- Modify `loadAccounts()` to call `uiGetAccountsPage` and render all three sections from response
- Extract rendering into `renderAccountStats_(data)` and `renderCarrierFilter_(data)`
- Remove standalone `loadCarriersFilter()` call from `navigateTo` accounts branch
- Remove `loadAccountStats()` from enhanced navigateTo wrapper for accounts

**Expected**: Accounts page = **~7-10s** (was 45-180s)

---

## Phase 4: Fix MyCases HTTP Storm (4 HTTP → 1 sheet read)

**What**: Replace 4 sequential `callRapidAPI('task', {status})` calls with 1 `RAPID_CORE.getTabData('_CASE_TASKS')`.

**Why**: `scanCaseworkData_()` (`PRODASH_CASEWORK.gs:64-98`) makes 4 HTTP round-trips to RAPID_API — which itself reads `_CASE_TASKS` from PRODASH_MATRIX. Cut out the middleman.

**Verified**: `_CASE_TASKS` is in `TABLE_ROUTING` as `'PRODASH'` (`CORE_Database.gs:68`), so `RAPID_CORE.getTabData('_CASE_TASKS')` works directly.

**File**: `PRODASH_CASEWORK.gs`

Replace lines 81-91:
```javascript
// OLD: 4 HTTP round-trips
var tasksResp = callRapidAPI('task', { status: 'open' }, 'GET');
// ... 3 more

// NEW: 1 direct MATRIX read
var allTasks = RAPID_CORE.getTabData('_CASE_TASKS') || [];
allTasks = allTasks.filter(function(t) { return t.status && t.status !== 'deleted'; });
```

Also fix `getCaseDetail_()` (line ~230) — same pattern, replace `callRapidAPI('task', { opportunity_id })` with MATRIX filter.

**Expected**: MyCases = **~5-7s** (was 74-101s)

---

## Phase 5: Reduce Chat Polling

**What**: Reduce polling frequency and delay initial badge check.

**File**: `RPI_Connect.html`

| Timer | Current | New |
|-------|---------|-----|
| Badge polling (`_initBadge`, line 1376) | 60s | 300s (5 min) |
| Message polling (`_startPolling`, line 1121) | 30s | 60s |
| Initial badge delay (line 1429) | 5s | 15s |

**Expected**: Background calls drop from ~3/30s to ~1/60s. With Phase 1's priority queue, these never block user actions anyway. Reduces GAS quota usage.

---

## Phase 6: Function Output CacheService (Optional Polish)

**What**: Cache small function outputs in `CacheService.getScriptCache()` with 2-5 min TTL.

**Why**: Each `google.script.run` is an independent execution — module-level `var` caches don't persist between calls. CacheService persists across executions AND across users.

**Constraint**: 100KB per key limit. Raw sheet data (5-10MB) can't be cached. But function OUTPUTS are small.

**Helper** (in `Code.gs` or `PRODASH_MatrixCache.gs`):
```javascript
function withOutputCache_(key, ttlSeconds, fn) {
  var cache = CacheService.getScriptCache();
  var cached = cache.get(key);
  if (cached) { try { return JSON.parse(cached); } catch(e) {} }
  var result = fn();
  try {
    var json = JSON.stringify(result);
    if (json.length < 95000) cache.put(key, json, ttlSeconds);
  } catch(e) {}
  return result;
}
```

**Apply to**: `uiGetDashboardPage` (2min TTL), `uiGetAccountStats` (5min), `uiGetUniqueCarriers` (10min)

**Invalidation**: Wire into `invalidateMatrixCache_()` — add `CacheService.getScriptCache().removeAll([keys])`.

**Expected**: Repeat visits within TTL = **<100ms** (no sheet reads at all)

---

## Execution Order

```
Phase 1 (Call Queue)      ← DO FIRST. Foundation. 60-130s → 5-8s.
Phase 4 (Fix MyCases)     ← PARALLEL with Phase 1. Independent server-side fix.
    ↓
Phase 2 (Batch Init)      ← After Phase 1. 5 round-trips → 1.
Phase 3 (Batch Accounts)  ← After Phase 1. 3 round-trips → 1.
Phase 5 (Chat Polling)    ← After Phase 1. Uses callServerBg.
    ↓
Phase 6 (CacheService)    ← Last. Polish. Repeat visits instant.
```

---

## Expected Performance

| Scenario | Current | After Phase 1 | After All Phases |
|----------|---------|---------------|-----------------|
| App startup → dashboard | 60-130s | ~15-20s | **~8s** |
| Accounts page | 45-180s | ~20s | **~7-10s** |
| MyCases / Yellow Stage | 74-101s | ~20-30s | **~5-7s** |
| Client360 | 47-71s | ~8-12s | **~8s** |
| Orange/Green Stage | 45-124s | ~5-8s | **~5-7s** |
| Return visit (cached) | Same | Same | **<100ms** |
| Background poll impact | Blocks everything | Zero | Zero |

---

## Critical Files

| File | Phases | Changes |
|------|--------|---------|
| `Scripts.html` | 1, 2, 3 | Call queue, init flow, accounts batching |
| `RPI_Connect.html` | 1, 5 | Route 13 `google.script.run` calls through queue, reduce polling |
| `Code.gs` | 2, 6 | `uiGetAppInit()`, `withOutputCache_()` |
| `PRODASH_Accounts.gs` | 3, 6 | `uiGetAccountsPage()`, CacheService wrappers |
| `PRODASH_CASEWORK.gs` | 4 | Replace 4 HTTP calls with `RAPID_CORE.getTabData('_CASE_TASKS')` |
| `PRODASH_MatrixCache.gs` | 6 | CacheService invalidation in `invalidateMatrixCache_()` |

---

## Verification

### After Phase 1:
1. Open PRODASHX in incognito
2. Check GAS execution log — functions should NEVER overlap (serial execution)
3. Each function should complete in 2-8s (solo speed)
4. Open RPI_Connect panel — badge/message polls should not delay page loads

### After Phase 2:
1. On fresh load, execution log shows `uiGetAppInit` as first call (~3s)
2. `uiGetDashboardPage` fires next (~5s)
3. Total startup: ~8s

### After Phase 3:
1. Navigate to Accounts — one `uiGetAccountsPage` call in log (~8s)
2. Stats cards, carrier filter, and account table all populate from single response

### After Phase 4:
1. Navigate to My Cases — `uiGetMyCases` in log at ~5-7s (no `callRapidAPI` HTTP calls)
2. Run `execute_script` on `uiGetMyCases` — should match web app timing

### After Phase 6:
1. Navigate Dashboard → Accounts → Dashboard — second dashboard load should show `withOutputCache_` hit in <1s
