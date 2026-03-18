ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# SERFF Closed Block → BigQuery → PSM-RATE Pipeline

> **Status: EXECUTED — 2026-03-09**
> Built, tested, deployed. Waiting for next monthly data drop with Iowa carriers.

## Context

RPI subscribes to CSG Actuarial's SERFF rate filing data — monthly drops covering Med Supp rates across 61 carriers, 48 states, 13 plan types (~1.18M rows). The data includes both **current rates** and **pending future rate actions** (25 carriers with increases effective Apr-Oct 2026). This is the engine that powers the proactive service model: detect upcoming rate increases BEFORE they hit clients, trigger the PSM-RATE campaign, convert rate anxiety into appointments.

**What was built (2026-03-09):**
- BigQuery dataset `SERFF_MedSupp` with 1.18M rows across 5 tables
- Node.js CSV→BigQuery loader (`MCP-Hub/serff-loader/`) — reads from Shared Drive
- GAS rate detection engine (`RAPID_IMPORT/IMPORT_RateDetection.gs`) — 19 functions
- 90+ SERFF carrier aliases in RAPID_CORE + `_RATE_ACTIONS` schema
- MCP OAuth extended with BigQuery scope (33 total)

**Source data location:** `SERFF_Rate_Data` folder on Shared Drive (inside Mail Intake)
- Drive folder ID: `1PV5nwIuXzKiM6_QAW3zyESe5OE5LdtZQ`
- JDM drops CSVs here → tells Claude "new SERFF drop" → pipeline runs

**CSG API status:** Brien Welch (bwelch@csgactuarial.com) owes API key + SERFF data feed endpoints. As of Mar 8, the documented APIs on Apiary (https://csgapi.docs.apiary.io/) are quoting tools only — no SERFF data feed endpoints published yet. Build against CSV files now; API integration is a future enhancement when endpoints are available.

**GCP Project:** `claude-mcp-484718` (same project as SENTINEL BigQuery CSG agent data)

## Execution Notes (2026-03-09)

**Versions deployed:** RAPID_CORE v1.17.0 (@97) | RAPID_IMPORT v3.31.1 (@192)

**Bugs found and fixed during testing:**
1. **Med Supp filter** — `core_product_type` used exact string match (`!== 'med_supp'`) instead of `indexOf('med supp')`. Real Med Supp records were being skipped; blank-type records leaked through.
2. **Plan letter metadata** — `plan_letter` field contained parenthetical metadata like `"F (T65 <1.1.20)"`. Added normalization to strip everything after the letter during matching.
3. **BigQuery free tier** — DML `DELETE` and streaming inserts not available. Switched to `WRITE_TRUNCATE` disposition on load jobs and NDJSON file loads for snapshots.

**First dry run results:** 0 affected clients (correct). Only 2 carriers have rate increases (Royal Arcanum in DE/MD, Heartland National in IL). RPI has no active Med Supp clients with those carriers in those states.

**Operational flow:**
1. JDM drops CSVs in `SERFF_Rate_Data` on Shared Drive
2. Claude runs `npm run serff:load` (downloads from Drive → BigQuery)
3. Claude runs `FIX_DetectRateActionsDryRun()` → shows impact
4. JDM reviews, says #SendIt
5. Claude runs `FIX_DetectRateActions()` → updates fields, enrolls PSM-RATE, Slack summary

**Next sprint:** Wire document watcher to auto-detect new CSVs in the Drive folder (eliminates manual "new SERFF drop" trigger).

---

## Data Inventory

| File | Rows | Size | Content |
|------|------|------|---------|
| `rates_supp_current.csv` | 577,936 | 110MB | Current rates: 61 carriers, 48 states, Plans A-N + HDG |
| `rates_supp_future.csv` | 102,442 | 20MB | Pending increases: 25 carriers, 35 states, eff Apr-Oct 2026 |
| `rates_supp_current_ma_mn_wi.csv` | 46,620 | 9MB | MA/MN/WI current (community-rated states, unique plan codes) |
| `rates_supp_future_ma_mn_wi.csv` | 2,072 | 400KB | MA/MN/WI future |
| `zip_codes_supp.csv` | 452,299 | 21MB | ZIP lookup → State/County/City/ZIP-3/ZIP-5 |
| `rates_sel_current.csv` | 288 | 53KB | Medicare Select current |
| `zip_codes_sel.csv` | 165 | 8KB | Select ZIP mapping |
| **TOTAL** | **~1.18M** | **~161MB** | Semicolon-delimited, quoted fields |

**Schema (22 columns):** Company, Company_Old, NAIC, Plan, State, Area, Zip_Lookup_Code, Gender, T/NT, Couple_Fac, Eff_Date, Rate_Type, Age_For_Sorting, Lowest_Rate?, Highest_Rate?, Age, Monthly_Rate, Quarterly_Rate, Semi-Annual_Rate, Annual_Rate, Policy Fee, Household Discount

---

## Architecture Decisions

| Decision | Answer | Rationale |
|----------|--------|-----------|
| **Where does BigQuery code live?** | SENTINEL (query patterns) + MCP-Hub Node.js (CSV loading) + RAPID_IMPORT (detection) | SENTINEL already has BQ enabled; 110MB CSV requires Node.js; detection is a data import operation |
| **How to load 110MB CSV?** | Node.js in `MCP-Hub/serff-loader/` using `@google-cloud/bigquery` `table.load()` | GAS has 6-min limit and ~50MB URL fetch cap. Node.js streams the file directly. No GCS staging needed. |
| **Rate change detection?** | New `IMPORT_RateDetection.gs` in RAPID_IMPORT with BigQuery queries | RAPID_IMPORT already has RAPID_CORE (carrier normalization), MATRIX access, RAPID_API writes |
| **Carrier matching?** | NAIC code as primary key, carrier name normalization as fallback | SERFF includes NAIC codes (universal insurance identifiers). More reliable than fuzzy name matching. |
| **Dedicated rate actions tab?** | Yes — `_RATE_ACTIONS` in RAPID_MATRIX | Tracks carrier-level rate actions (reference data) separate from client-level `_ACCOUNT_MEDICARE` updates |

---

## Phase 1: BigQuery Infrastructure + Data Load

### 1A. Create BigQuery Dataset + Tables

**Dataset:** `claude-mcp-484718.SERFF_MedSupp`

**Tables:**

```sql
-- rates_current: All current supplement + select + MA/MN/WI rates
CREATE TABLE SERFF_MedSupp.rates_current (
  company STRING, company_old STRING, naic INT64,
  plan STRING, state STRING, area INT64, zip_lookup_code INT64,
  gender STRING, tobacco_status STRING, couple_factor STRING,
  eff_date DATE, rate_type STRING,
  age_for_sorting INT64, is_lowest_rate BOOL, is_highest_rate BOOL, age STRING,
  monthly_rate FLOAT64, quarterly_rate FLOAT64, semi_annual_rate FLOAT64, annual_rate FLOAT64,
  policy_fee FLOAT64, household_discount STRING,
  is_community_rated_state BOOL, data_source STRING, load_date DATE, load_batch STRING
);

-- rates_future: Same schema (pending rate actions)
CREATE TABLE SERFF_MedSupp.rates_future ( /* identical columns */ );

-- zip_lookup: ZIP code → geography mapping
CREATE TABLE SERFF_MedSupp.zip_lookup (
  zip_lookup_code INT64, state STRING, county STRING, city STRING,
  zip_3 STRING, zip_5 STRING, data_source STRING, load_date DATE
);

-- carrier_mapping: SERFF carrier name → RPI _CARRIER_MASTER linkage
CREATE TABLE SERFF_MedSupp.carrier_mapping (
  serff_company STRING, serff_naic INT64,
  rpi_carrier_name STRING, rpi_carrier_id STRING,
  match_method STRING, verified BOOL, updated_at TIMESTAMP
);

-- rate_snapshots: Monthly load tracking
CREATE TABLE SERFF_MedSupp.rate_snapshots (
  snapshot_month STRING, table_name STRING, row_count INT64,
  carrier_count INT64, state_count INT64, loaded_at TIMESTAMP
);
```

### 1B. Build Node.js CSV Loader

**New directory:** `MCP-Hub/serff-loader/`
- `load-serff.js` — main loader script
- `package.json` — deps: `@google-cloud/bigquery`, `csv-parse`

**What it does:**
1. Reads semicolon-delimited CSVs from local `!AAA_Closed_Block/` directory
2. Parses with transformations:
   - `Eff_Date` "2/1/2025 0:00:00" → `2025-02-01`
   - `NAIC` "63444.00" → `63444`
   - `Lowest_Rate?` "Y"/"N" → `true`/`false`
   - `Policy Fee` "$25" → `25.00`
   - `T/NT` → `tobacco_status` ("Tobacco"/"Non-Tobacco")
3. Loads via `@google-cloud/bigquery` `table.load()` with readable stream
4. MA/MN/WI files → `is_community_rated_state = true`
5. Select files → `data_source = 'select'`

**Commands:**
```bash
cd ~/Projects/RAPID_TOOLS/MCP-Hub
npm run serff:load          # Full load (all 7 files)
npm run serff:load:future   # Future rates only (quick, for monthly refresh)
npm run serff:status        # Row counts + snapshot history
```

### 1C. Load + Verify

Expected row counts after load:
- `rates_current`: ~624,844 (577,936 + 46,620 + 288)
- `rates_future`: ~104,514 (102,442 + 2,072)
- `zip_lookup`: ~452,464 (452,299 + 165)

---

## Phase 2: Rate Change Detection

### 2A. Add BigQuery to RAPID_IMPORT

Modify `appsscript.json`:
- Add BigQuery Advanced Service (`bigquery v2`)
- Add scope `https://www.googleapis.com/auth/bigquery`
- **JDM one-time:** Re-authorize from GAS editor after `clasp push`

### 2B. Create `IMPORT_RateDetection.gs`

**Core functions:**

```javascript
// Configuration
var RATE_CONFIG = {
  projectId: 'claude-mcp-484718',
  dataset: 'SERFF_MedSupp',
  tables: { current: '`...rates_current`', future: '`...rates_future`', ... }
};

// BigQuery helper (same pattern as SENTINEL runBigQuery_)
function runRateBQ_(sql, params) { ... }

// Step 1: Map SERFF carriers to _CARRIER_MASTER via NAIC + name normalization
function buildCarrierMapping_() { ... }

// Step 2: Query rate increases (future > current for same carrier/plan/state/age/gender)
function queryRateIncreases_() { ... }

// Step 3: Cross-reference with _ACCOUNT_MEDICARE to find affected RPI clients
function detectClientRateActions_() { ... }

// Step 4: Write updates to _ACCOUNT_MEDICARE via RAPID_API + insert _RATE_ACTIONS
function executeRateActionUpdates_(dryRun) { ... }

// Step 5: Enroll affected clients in PSM-RATE campaign
function enrollAffectedClients_(clientIds) { ... }

// Step 6: Slack summary to JDM (U09BBHTN8F2)
function sendRateActionSummary_(results) { ... }

// Orchestrator
function detectAndUpdate_(dryRun) {
  buildCarrierMapping_();
  var increases = queryRateIncreases_();
  var affected = detectClientRateActions_(increases);
  var results = executeRateActionUpdates_(affected, dryRun);
  if (!dryRun) {
    enrollAffectedClients_(results.clientIds);
    sendRateActionSummary_(results);
  }
  return results;
}

// Entry points
function FIX_DetectRateActionsDryRun() { return detectAndUpdate_(true); }
function FIX_DetectRateActions()       { return detectAndUpdate_(false); }
function rateDetection_trigger()       { return detectAndUpdate_(false); }
```

**Rate increase detection SQL:**
```sql
SELECT f.company, f.naic, f.plan, f.state, f.gender, f.tobacco_status, f.age,
       f.eff_date AS new_eff_date,
       c.monthly_rate AS current_rate, f.monthly_rate AS future_rate,
       ROUND((f.monthly_rate - c.monthly_rate) / NULLIF(c.monthly_rate, 0) * 100, 2) AS pct_increase,
       f.monthly_rate - c.monthly_rate AS rate_delta
FROM rates_future f
JOIN rates_current c
  ON f.naic = c.naic AND f.plan = c.plan AND f.state = c.state
  AND f.area = c.area AND f.gender = c.gender
  AND f.tobacco_status = c.tobacco_status AND f.age = c.age
WHERE f.monthly_rate > c.monthly_rate
ORDER BY pct_increase DESC
```

**Client matching logic:**
For each `_ACCOUNT_MEDICARE` record → resolve carrier NAIC, plan letter, client state, age, gender → look up in rate increase results → if match found → compute new rate action fields.

### 2C. Add `_RATE_ACTIONS` Schema

In `RAPID_CORE/CORE_Database.gs`:

**TABLE_ROUTING:** `'_RATE_ACTIONS': 'RAPID'`

**TAB_SCHEMAS:**
```javascript
'_RATE_ACTIONS': [
  'rate_action_id', 'serff_company', 'naic', 'rpi_carrier_name',
  'plan', 'state', 'rate_type',
  'current_monthly_rate', 'future_monthly_rate', 'pct_increase', 'rate_delta',
  'effective_date', 'affected_client_count', 'status',
  'detected_at', 'load_batch', 'created_at', 'updated_at'
]
```

### 2D. Add `naic_code` to `_CARRIER_MASTER`

Add column to schema. Populate for known SERFF carriers using NAIC from the CSV data.

---

## Phase 3: Client Impact + Campaign Trigger

### 3A. Update `_ACCOUNT_MEDICARE` Fields

For each matched client, via RAPID_API:
- `rate_action_premium` = future monthly rate
- `annual_rate_increase` = percentage increase
- `cumulative_rate_increase` = existing cumulative + new increase
- `rate_action_date` = effective date

### 3B. Trigger PSM-RATE Campaign

Call existing `enrollContacts(psmRateCampaignId, clientIds, null, 'SERFF_RATE_DETECTION')` from `API_CampaignSend.gs`. The fully-built enrollment → queue → send pipeline handles the rest.

### 3C. Slack Notification

Post to JDM DM (`U09BBHTN8F2`):
- Carriers with pending increases, states affected, date range
- RPI clients affected count, campaign enrollments created
- Top 5 impacted carriers by client count

---

## Phase 4: Monthly Refresh

1. JDM receives monthly CSG data drop → places in `!AAA_Closed_Block/`
2. Run `npm run serff:load` (truncate + reload — full refresh)
3. Run `FIX_DetectRateActions()` — re-runs client matching
4. New rate actions detected, clients enrolled, Slack summary sent

**Optional automation:** GAS time-driven trigger on `rateDetection_trigger()` (monthly on 5th at 8am).

---

## Files to Create/Modify

### New Files
| File | Project | Purpose |
|------|---------|---------|
| `serff-loader/load-serff.js` | MCP-Hub | Node.js CSV → BigQuery loader |
| `serff-loader/package.json` | MCP-Hub | Dependencies |
| `IMPORT_RateDetection.gs` | RAPID_IMPORT | Detection + client matching + campaign trigger |

### Modified Files
| File | Project | Change |
|------|---------|--------|
| `CORE_Database.gs` | RAPID_CORE | Add `_RATE_ACTIONS` schema + `naic_code` to `_CARRIER_MASTER` |
| `CORE_Normalize.gs` | RAPID_CORE | Add ~62 SERFF carrier names to `CARRIER_ALIASES` |
| `appsscript.json` | RAPID_IMPORT | Add BigQuery Advanced Service + scope |
| `package.json` | MCP-Hub | Add `serff:*` script commands |

### No Changes Needed
| Component | Why |
|-----------|-----|
| PRODASHX | Rate action fields + UI already exist |
| API_CampaignSend.gs | `enrollContacts()` already works |
| C3 | PSM-RATE campaign already defined |
| SENTINEL | Pattern reference only, not modified |

---

## Execution Order

1. **RAPID_CORE** — schema additions (`_RATE_ACTIONS`, `naic_code`, carrier aliases). Deploy library.
2. **MCP-Hub** — build `serff-loader/`. Test with small CSV, then full load.
3. **BigQuery** — create dataset + tables. Run full load. Verify counts.
4. **RAPID_IMPORT** — add BigQuery service. JDM re-auth. Create `IMPORT_RateDetection.gs`. Push.
5. **Dry run** — `FIX_DetectRateActionsDryRun()` — review matched clients, verify no false positives.
6. **Live run** — `FIX_DetectRateActions()` — updates + campaign enrollments + Slack summary.

---

## JDM Actions Required

| Action | When | How |
|--------|------|-----|
| Re-authorize RAPID_IMPORT | After Phase 4 `clasp push` | Open GAS editor, prompted automatically |
| Review carrier mapping report | After first dry run | Unmatched carriers list, verify/add manual mappings |
| Verify PSM-RATE campaign exists in `_CAMPAIGNS` | Before Phase 6 | Check via PRODASHX or direct MATRIX lookup |

---

## Verification

1. `serff:status` shows correct row counts matching source CSVs
2. `FIX_DetectRateActionsDryRun()` returns structured summary with affected client count
3. `_RATE_ACTIONS` tab populated with carrier-level rate increase records
4. `_ACCOUNT_MEDICARE` rate action fields updated for affected clients
5. CLIENT360 "Deductibles & Rate Actions" card shows new values
6. `_CAMPAIGN_ENROLLMENTS` has new PSM-RATE enrollments
7. Slack DM to JDM with impact summary
8. Spot-check 5 client records in PRODASHX UI
