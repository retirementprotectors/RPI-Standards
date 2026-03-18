ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# PRODASHX BigQuery Migration — The Leap

## Context

v3.25.0 exhausted every GAS-level optimization: serialized call queue, batched init/dashboard/accounts, CacheService output caching, reduced chat polling, eliminated HTTP round-trips. **Result: data-heavy functions still take 30-56s** because `getDataRange().getValues()` on 4,895 clients × 102 columns through the GAS web app execution context is irreducibly slow.

The same functions run in ~5s via `execute_script` (API execution). The bottleneck is the GAS web app execution layer itself — not the code, not the data volume, not contention. This is a **platform ceiling**.

**The fix**: Move PRODASHX reads from Google Sheets to BigQuery via Cloud Run. BQ queries on this data volume return in <200ms. Combined with the existing call queue, dashboard goes from 30-56s to ~3-5s (Phase 1) or <1s (Phase 2).

---

## Architecture

### Current (Slow)
```
Browser → google.script.run → GAS Web App → Sheets getDataRange() [30-56s] → Browser
```

### Phase 1: GAS → Cloud Run → BQ (Quick Win)
```
Browser → google.script.run → GAS → UrlFetchApp.fetch(Cloud Run) → BQ [~200ms] → Browser
Total: ~3-5s (GAS overhead + BQ)
```

### Phase 2: Browser → Cloud Run → BQ (Full Speed)
```
Browser → fetch(Cloud Run) with identity token → BQ [~200ms] → Browser
Total: <1s
```

---

## Phase 0: BQ Dataset + Sync Loader

**Goal**: Get PRODASHX data into BigQuery and keep it fresh.

### 0A: Create BQ Dataset + Tables

**Dataset**: `claude-mcp-484718.PRODASH_Data` (alongside existing `SERFF_MedSupp`)

**Tables** (one per MATRIX tab, priority order):

| BQ Table | Source Sheet | ~Rows | ~Cols | Priority |
|----------|-------------|-------|-------|----------|
| `clients` | `_CLIENT_MASTER` | 4,895 | 102 | P0 — critical |
| `accounts_annuity` | `_ACCOUNT_ANNUITY` | 2,300 | 74 | P0 |
| `accounts_life` | `_ACCOUNT_LIFE` | 1,800 | 60 | P0 |
| `accounts_medicare` | `_ACCOUNT_MEDICARE` | 2,100 | 47 | P0 |
| `accounts_bdria` | `_ACCOUNT_BDRIA` | 1,500 | 65 | P0 |
| `accounts_banking` | `_ACCOUNT_BANKING` | 1,590 | 24 | P0 |
| `activity_log` | `_ACTIVITY_LOG` | 50K+ | 9 | P0 |
| `opportunities` | `_OPPORTUNITIES` | 1,200 | 13 | P1 |
| `case_tasks` | `_CASE_TASKS` | 500 | 13 | P1 |
| `pipelines` | `_PIPELINES` | 12 | 8 | P1 |
| `relationships` | `_RELATIONSHIPS` | 800 | 7 | P1 |
| `permissions` | `_PERMISSIONS` | 30 | 7 | P2 |

**Schema source**: `TAB_SCHEMAS` in `RAPID_CORE/CORE_Database.gs` (lines 271-670). Each schema field maps to a BQ column. Default type STRING except known numeric/date fields get proper BQ types (`FLOAT64`, `DATE`, `BOOL`). Every row gets `_load_date DATE` and `_load_batch STRING` for audit.

### 0B: Build Sync Loader

**Location**: `~/Projects/RAPID_TOOLS/MCP-Hub/prodash-loader/`

**Pattern**: Follow `serff-loader/load-serff.js` exactly:
- `@google-cloud/bigquery@^7.9.0` + `googleapis@^144.0.0` (same deps)
- ES modules (`"type": "module"`)
- Auth: Drive OAuth from `~/.config/rpi-mcp/gcp-oauth.keys.json` + `~/.config/google-drive-mcp/tokens.json`, BQ via ADC
- **Read MATRIX via Sheets API** (`googleapis` npm, NOT SpreadsheetApp) — reads the PRODASH_MATRIX spreadsheet by ID from `RAPID_CORE.getMATRIX_ID('PRODASH')` (ID stored in GAS Script Properties, also readable via Sheets API)
- Transform rows to NDJSON, BQ load job with `WRITE_TRUNCATE` (full refresh)
- Total data is ~70K rows — full refresh takes <30 seconds

**Scripts**:
```json
{
  "scripts": {
    "sync": "node load-prodash.js",
    "sync:status": "node load-prodash.js --status",
    "sync:table": "node load-prodash.js --table clients"
  }
}
```

### 0C: BQ Views (Materialize Dedup/Join Logic)

Replace the `PRODASH_MatrixCache.gs` transformation logic with BQ views:

**`v_clients_deduped`** — Replicates `_ensureClients()` logic (MatrixCache.gs lines 78-152):
```sql
WITH ranked AS (
  SELECT *,
    CASE LOWER(TRIM(COALESCE(client_status, status, '')))
      WHEN 'active - internal' THEN 10
      WHEN 'active - external' THEN 9
      WHEN 'active' THEN 8
      WHEN 'prospect' THEN 3
      WHEN 'inactive' THEN 1
      ELSE 2
    END AS _status_priority,
    ROW_NUMBER() OVER (
      PARTITION BY LOWER(TRIM(first_name)) || '|' || LOWER(TRIM(last_name)) || '|' || REGEXP_REPLACE(COALESCE(phone, cell_phone, ''), r'[^0-9]', '')
      ORDER BY CASE LOWER(TRIM(COALESCE(client_status, status, '')))
        WHEN 'active - internal' THEN 10 WHEN 'active - external' THEN 9 WHEN 'active' THEN 8 ELSE 2 END DESC
    ) AS _dedup_rank
  FROM `claude-mcp-484718.PRODASH_Data.clients`
  WHERE LOWER(TRIM(COALESCE(status, ''))) != 'deleted'
    AND LOWER(TRIM(COALESCE(client_status, ''))) != 'inactive - merged'
)
SELECT * EXCEPT(_status_priority, _dedup_rank) FROM ranked WHERE _dedup_rank = 1
```

**`v_accounts_all`** — Union of all 5 account tables with type discriminator:
```sql
SELECT *, 'annuity' AS account_type FROM accounts_annuity WHERE LOWER(COALESCE(status,'')) != 'deleted'
UNION ALL
SELECT *, 'life' AS account_type FROM accounts_life WHERE LOWER(COALESCE(status,'')) != 'deleted'
UNION ALL ...
```

**`v_dashboard_stats`** — Pre-aggregated stats:
```sql
SELECT
  (SELECT COUNT(*) FROM v_clients_deduped) AS client_count,
  (SELECT COUNT(*) FROM v_accounts_all WHERE LOWER(COALESCE(status,'')) = 'active') AS account_count,
  (SELECT COALESCE(SUM(SAFE_CAST(account_value AS FLOAT64)), 0) FROM v_accounts_all) AS total_aum,
  (SELECT COUNT(*) FROM v_accounts_all WHERE SAFE_CAST(rmd_remaining AS FLOAT64) > 0) AS rmds_due
```

### 0D: Schedule Sync

**Launchd agent**: `com.rpi.prodash-sync` — runs `npm run sync` every 5 minutes.
- Plist template in `~/.claude/launchd/`
- Installed at `~/Library/LaunchAgents/`
- Logs: `prodash-loader/sync-out.log`

**Why 5 minutes**: Writes happen sporadically via RAPID_API. 5-minute eventual consistency is acceptable — users don't refresh-on-write repeatedly.

### 0E: Validation

Compare BQ data against Sheets:
1. Row counts per table must match (within 5-min sync window)
2. Spot-check 50 random client records — field values must match
3. Run `v_clients_deduped` and compare count against PRODASHX's `getAllClients_().length`
4. Run `v_dashboard_stats` and compare against `uiGetDashboardStats()` output

---

## Phase 1: Cloud Run API + GAS Proxy

**Goal**: Replace all Sheets reads with Cloud Run → BQ. Users see 30-56s drop to ~3-5s.

### 1A: Build PRODASH API (Cloud Run)

**Location**: `~/Projects/RAPID_TOOLS/MCP-Hub/prodash-api/`

**Structure** (mirrors healthcare-mcps pattern):
```
prodash-api/
├── api/
│   └── server.js          # Express.js endpoints
├── Dockerfile             # node:20-slim, npm ci, expose 3456
├── cloudbuild.yaml        # Build → Artifact Registry → Cloud Run
├── package.json           # express, @google-cloud/bigquery, cors
└── .gcloudignore
```

**Cloud Run config**:
```yaml
Memory: 512Mi          # BQ queries, not in-memory data
CPU: 1
Min Instances: 0       # Cost savings — cold start (~2s) hidden by GAS overhead
Max Instances: 3
Region: us-central1
Allow-unauthenticated: true  # Auth via identity token in header
```

**Express.js endpoints** (`api/server.js`):

```
GET  /api/prodash/health                    → { status: 'ok', dataset: 'PRODASH_Data' }
GET  /api/prodash/dashboard                 → Stats + priority queue + recent activity
GET  /api/prodash/clients?filters&page&limit → Paginated, filtered, deduped clients
GET  /api/prodash/clients/:id               → Single client with all fields
GET  /api/prodash/clients/:id/accounts      → Accounts for client (all types or filtered)
GET  /api/prodash/clients/:id/activities    → Activities for client (sorted DESC, limited)
GET  /api/prodash/clients/:id/relationships → Relationships for client
GET  /api/prodash/accounts?filters&page&limit → Paginated, filtered accounts
GET  /api/prodash/accounts/stats            → Per-type aggregated stats
GET  /api/prodash/carriers                  → DISTINCT carrier names
GET  /api/prodash/opportunities?stage_id    → Filtered opportunities
GET  /api/prodash/tasks?opportunity_id      → Case tasks
GET  /api/prodash/pipelines                 → All pipelines with stages
```

All endpoints query BQ views. Auth: verify `Authorization: Bearer <token>` header (Google identity token from GAS). Response format: `{ success: true, data }` or `{ success: false, error }`.

### 1B: GAS Bridge (`PRODASH_BQ_API.gs`)

New file in PRODASHX, modeled on `PRODASH_MEDICARE_API.gs`:

```javascript
var PRODASH_API_URL_ = PropertiesService.getScriptProperties()
  .getProperty('PRODASH_API_URL') || '';

function callProdashAPI_(endpoint, params) {
  if (!PRODASH_API_URL_) return null;  // Fallback to Sheets
  var url = PRODASH_API_URL_ + endpoint;
  if (params) {
    var qs = Object.keys(params).filter(function(k) { return params[k] != null; })
      .map(function(k) { return k + '=' + encodeURIComponent(params[k]); }).join('&');
    if (qs) url += '?' + qs;
  }
  var response = UrlFetchApp.fetch(url, {
    headers: { 'Authorization': 'Bearer ' + ScriptApp.getIdentityToken() },
    muteHttpExceptions: true, connectTimeout: 10000, timeout: 15000
  });
  if (response.getResponseCode() !== 200) return null;
  return JSON.parse(response.getContentText());
}
```

### 1C: Swap Data Source in MatrixCache

Modify `PRODASH_MatrixCache.gs` — each `_ensure*()` function tries BQ first, falls back to Sheets:

```javascript
function _ensureClients() {
  if (_mcClients) return _mcClients;

  // Try BQ (fast path)
  var bqResult = callProdashAPI_('/api/prodash/clients', { limit: 10000 });
  if (bqResult && bqResult.success && bqResult.data) {
    // Build same structure from already-deduped BQ data
    var clientsById = {};
    var list = bqResult.data.clients || bqResult.data;
    for (var i = 0; i < list.length; i++) {
      var c = list[i];
      var cid = c.client_id || c.id;
      var ghl = c.ghl_contact_id;
      if (cid) clientsById[cid] = c;
      if (ghl && ghl !== cid) clientsById[ghl] = c;
    }
    _mcClients = { clientsById: clientsById, clientsList: list, deletedById: {} };
    return _mcClients;
  }

  // Fallback: existing Sheets code (unchanged)
  var allClientRows = _parseSheet('_CLIENT_MASTER');
  // ... existing dedup logic ...
}
```

Same pattern for `_ensureAccounts()` and `_ensureActivities()`.

**Key**: The `ui*` functions (`uiGetClients`, `uiGetDashboardPage`, etc.) change ZERO. They still call `getAllClients_()` → `_ensureClients()`. The data source swap is invisible to the UI layer.

### 1D: Dedicated BQ Endpoints for Batched Functions

For the batched functions that currently compose multiple data reads, create dedicated BQ endpoints:

- `GET /api/prodash/dashboard` replaces the logic in `uiGetDashboardPage()` — returns stats + priority queue + activity in one BQ query
- `GET /api/prodash/accounts/page?filters&page&limit` replaces `uiGetAccountsPage()` — returns accounts + stats + carriers in one response
- `GET /api/prodash/clients/:id/360` replaces `uiGetClient360Page()` — returns client + accounts + activities + relationships in one BQ join

The GAS batched functions (`uiGetDashboardPage`, `uiGetAccountsPage`, `uiGetClient360Page`) become thin wrappers:

```javascript
function uiGetDashboardPage() {
  var result = callProdashAPI_('/api/prodash/dashboard');
  if (result && result.success) return result;
  // Fallback to existing Sheets-based logic
  return withOutputCache_('prodash_dashboard', 120, function() { ... });
}
```

### Deployment

1. JDM sets Script Property `PRODASH_API_URL` to the Cloud Run URL
2. Deploy PRODASHX with new `PRODASH_BQ_API.gs` + modified MatrixCache
3. If Cloud Run is down or `PRODASH_API_URL` is empty, all reads fall back to Sheets automatically
4. Zero-risk rollback: delete the Script Property → instant revert to Sheets

---

## Phase 2: Browser-Direct to Cloud Run (Optional — if 3-5s isn't fast enough)

**Goal**: Eliminate `google.script.run` entirely for reads. Browser calls Cloud Run directly.

### Auth Token Handoff

`doGet()` in Code.gs injects an identity token into the HTML template:

```javascript
template.prodashApiUrl = PropertiesService.getScriptProperties().getProperty('PRODASH_API_URL') || '';
template.bqToken = ScriptApp.getIdentityToken();  // OIDC token, ~1h TTL
```

Browser JavaScript stores and uses the token:

```javascript
var PRODASH_API = '<?= prodashApiUrl ?>';
var BQ_TOKEN = '<?= bqToken ?>';

async function callBQ(path, params) {
  var url = new URL(PRODASH_API + path);
  Object.entries(params || {}).forEach(function([k,v]) { url.searchParams.set(k, v); });
  var resp = await fetch(url, { headers: { 'Authorization': 'Bearer ' + BQ_TOKEN } });
  return resp.json();
}
```

### Gradual Migration via Route Map

Extend the existing `callServer()` queue with a BQ route map:

```javascript
var BQ_ROUTES = {
  'uiGetDashboardPage': '/api/prodash/dashboard',
  'uiGetClients': '/api/prodash/clients',
  'uiGetAccountsPage': '/api/prodash/accounts/page',
  'uiGetClient360Page': '/api/prodash/clients/{id}/360'
};

function callServer(functionName) {
  // Check BQ route
  if (PRODASH_API && BQ_TOKEN && BQ_ROUTES[functionName]) {
    return callBQ(BQ_ROUTES[functionName], ...args);
  }
  // Fall back to google.script.run queue
  ...
}
```

Adding a route = one line. No GAS changes, no backend changes.

### Token Refresh

When BQ_TOKEN expires (~1h), browser calls `google.script.run.getRefreshToken()` — a single fast GAS call (no data, just token). Refresh runs via `callServerBg` (background priority, never blocks user actions).

---

## Write → Read Consistency

Writes stay unchanged: `google.script.run` → `callRapidAPI()` → RAPID_API → `RAPID_CORE.insertRow()` → MATRIX sheet.

After a write, next sync (<=5 min) picks up the change. For immediate read-after-write:
- After any write, `invalidateMatrixCache_()` clears the module-level cache
- The next read tries BQ (may still have old data within sync window)
- **Option A (simple)**: GAS-side reads fall back to Sheets for the next read after a write (set a `_lastWriteAt` timestamp, if <5 min ago, skip BQ). This guarantees consistency with zero additional infrastructure.
- **Option B (later)**: Add a `/api/prodash/sync-trigger` endpoint that does an immediate BQ refresh of the affected table (~2s). Wire into `invalidateMatrixCache_()`.

**Recommended**: Option A for launch. Upgrade to Option B if users notice stale data.

---

## Cost

| Component | Monthly Cost |
|-----------|-------------|
| BigQuery storage (~70K rows) | **$0** (free tier: 10GB) |
| BigQuery queries (~100/day, <1GB each) | **$0** (free tier: 1TB/month) |
| Cloud Run (min 0 instances, 512Mi) | **~$5-10** (pay per request, scales to 0 when idle) |
| Sync loader (launchd, runs on JDM's machine) | **$0** |
| **Total** | **~$5-10/month** |

---

## Execution Order

```
Phase 0A-0B (BQ setup + loader)      ← Foundation. Data in BQ.
Phase 0C (BQ views)                   ← Dedup/join logic in SQL.
Phase 0D-0E (Schedule + validate)     ← Sync running, data verified.
    ↓
Phase 1A (Cloud Run API)              ← Express.js endpoints.
Phase 1B-1C (GAS bridge + swap)      ← PRODASHX reads from BQ. 30-56s → 3-5s.
Phase 1D (Dedicated BQ endpoints)     ← Optimized single-query paths.
    ↓
Phase 2 (Browser-direct) [OPTIONAL]   ← 3-5s → <1s. Only if needed.
```

---

## Expected Performance

| Scenario | Current (v3.25.0) | After Phase 1 | After Phase 2 |
|----------|-------------------|---------------|---------------|
| Dashboard | 30-56s | **~3-5s** | **<1s** |
| Clients list | 36s | **~3-5s** | **<500ms** |
| Client360 | 44-56s | **~3-5s** | **<1s** |
| Accounts page | 32-36s | **~3-5s** | **<500ms** |
| MyCases | 5-7s (already fixed) | **~3s** | **<500ms** |
| Return visit (SPA cache) | <100ms | **<100ms** | **<100ms** |

---

## Rollback

Every phase has instant rollback:
- **Phase 0**: BQ data exists but nothing reads it. No impact.
- **Phase 1**: Delete `PRODASH_API_URL` Script Property → all reads revert to Sheets. One-line change, no deploy needed.
- **Phase 2**: Remove `BQ_ROUTES` entries → all reads revert to `google.script.run`. One deploy.

---

## Critical Files

### New Files
| File | Phase | Purpose |
|------|-------|---------|
| `MCP-Hub/prodash-loader/load-prodash.js` | 0 | Sheets → BQ sync loader |
| `MCP-Hub/prodash-loader/package.json` | 0 | Dependencies |
| `MCP-Hub/prodash-api/api/server.js` | 1 | Express.js Cloud Run API |
| `MCP-Hub/prodash-api/Dockerfile` | 1 | Container def |
| `MCP-Hub/prodash-api/cloudbuild.yaml` | 1 | CI/CD |
| `MCP-Hub/prodash-api/package.json` | 1 | Dependencies |
| `PRODASHX/PRODASH_BQ_API.gs` | 1 | GAS → Cloud Run bridge |

### Modified Files
| File | Phase | Changes |
|------|-------|---------|
| `PRODASHX/PRODASH_MatrixCache.gs` | 1 | `_ensure*()` functions try BQ first, fall back to Sheets |
| `PRODASHX/Code.gs` | 1 | `uiGetDashboardPage()` tries BQ endpoint |
| `PRODASHX/PRODASH_Accounts.gs` | 1 | `uiGetAccountsPage()` tries BQ endpoint |
| `PRODASHX/PRODASH_CLIENT360.gs` | 1 | `uiGetClient360Page()` tries BQ endpoint |
| `PRODASHX/Scripts.html` | 2 | `callBQ()` + `BQ_ROUTES` + token handoff |
| `PRODASHX/Code.gs` (doGet) | 2 | Inject `prodashApiUrl` + `bqToken` into template |

### Reference Files (Read, Don't Modify)
| File | Why |
|------|-----|
| `MCP-Hub/serff-loader/load-serff.js` | Loader pattern: Drive OAuth, NDJSON, BQ load jobs |
| `MCP-Hub/healthcare-mcps/cloudbuild.yaml` | Cloud Run deployment pattern |
| `MCP-Hub/healthcare-mcps/Dockerfile` | Container pattern |
| `PRODASHX/PRODASH_MEDICARE_API.gs` | GAS → Cloud Run bridge pattern (`callHealthcareMcps_`) |
| `RAPID_CORE/CORE_Database.gs` | `TAB_SCHEMAS` (BQ schema source), `TABLE_ROUTING` (tab→platform map) |

---

## Verification

### After Phase 0:
1. `npm run sync` completes without errors
2. BQ Console shows all tables in `PRODASH_Data` dataset with correct row counts
3. `SELECT COUNT(*) FROM v_clients_deduped` matches PRODASHX client count (~4,895)
4. `SELECT * FROM v_dashboard_stats` matches `uiGetDashboardStats()` output
5. Spot-check: `SELECT * FROM clients WHERE client_id = 'D8Kn8bQx4IKfSEgTpbRz'` returns correct record

### After Phase 1:
1. Set `PRODASH_API_URL` in PRODASHX Script Properties
2. Deploy PRODASHX
3. Open PRODASHX → dashboard loads in ~3-5s (check execution log)
4. Navigate to Clients → loads in ~3-5s
5. Open Client360 → loads in ~3-5s
6. Check execution log: `uiGetDashboardPage` = ~3-5s (was 30-56s)
7. Delete `PRODASH_API_URL` → verify Sheets fallback works (loads slower but works)

### After Phase 2:
1. Open PRODASHX → dashboard loads in <1s
2. No `google.script.run` calls in execution log for read operations
3. Only writes still use `google.script.run`
