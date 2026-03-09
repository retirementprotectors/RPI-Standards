# Phase 3b Continuation — Builder Agent Execution Plan

## Context

Phase 3b data import is mid-stream. Previous session imported 317 records (151 Life + 64 Annuity + 102 BD/RIA) into PRODASHX MATRIX but left 153 orphans, 160 blank carriers, and skipped the dedup pass. Timeline is crunching.

**This plan covers 5 priorities:** P1 (AI3 Combined), P2 (Signal Revenue), P6 (Commission PDFs), P5 (Carrier XLSX files), P3 (Advisor client subfolders). P4 (RED API/infrastructure gaps) is deferred to a future workstream.

**Approach: Path C (Hybrid)** — Use FIX_ import pattern for speed, but register every new tool in ATLAS _TOOL_REGISTRY, log to _SOURCE_HISTORY, and run the full RAPID_CORE data quality pipeline on every write.

---

## THE MACHINE MAP — What Powers Each Step

This is the payoff from hundreds of hours of infrastructure. Every step below uses registered, battle-tested components:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THE MACHINE — DATA LAYER                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ATLAS (_SOURCE_REGISTRY)              ATLAS (_TOOL_REGISTRY)           │
│  ├─ 100+ sources scored RED/YELLOW/    ├─ 150+ tools across 6 categories│
│  │  GREEN with gap analysis            ├─ INTAKE_QUEUING scanners       │
│  ├─ Drives priority order (not guesswork)│ EXTRACTION classifiers       │
│  └─ _SOURCE_HISTORY logs every import  └─ MATCHING_DEDUP algorithms     │
│                                                                         │
│  RAPID_CORE (Library — used on EVERY write)                             │
│  ├─ normalizeCarrierName() — 1,000+ alias mappings                      │
│  ├─ deriveParentCarrier() — 50+ subsidiary→parent maps                  │
│  ├─ bulkInsert() — normalize + dedup + UUID + timestamps in one call    │
│  ├─ updateRow() — targeted field updates with normalization             │
│  ├─ matchClient/Account() — multi-index dedup scoring                   │
│  ├─ reconcileClients/Accounts() — full-tab duplicate scanning           │
│  ├─ fullAutoMerge() — automated merge execution (score >= 85)           │
│  ├─ normalizeExistingData() — retroactive cleanup (9 normalizer types)  │
│  ├─ TAB_SCHEMAS — enforces column order (prevents silent data loss)     │
│  └─ TABLE_ROUTING — routes tabs to correct MATRIX sheet automatically   │
│                                                                         │
│  RAPID_IMPORT (Data Ingestion)                                          │
│  ├─ bobBuildClientGHLLookup_() — GHL contact ID → client_id bridge     │
│  ├─ bobReadSheet_() — cached sheet reader with column indexing          │
│  ├─ FIX_CarrierInference — learn+fill carrier patterns cross-tab       │
│  ├─ FIX_Normalize* — retroactive normalization per product line        │
│  ├─ FIX_AutoMerge* — client + account dedup execution                  │
│  └─ IMPORT_BoBImport.gs — carrier-specific BoB configs (10 carriers)   │
│                                                                         │
│  Document Pipeline (watcher.js — launchd agent, always-on)              │
│  ├─ scanIntakeFolders → classify → Claude Vision extraction             │
│  ├─ _APPROVAL_QUEUE → human approval UI → MATRIX                       │
│  └─ Used for P6 commission PDFs (no custom code needed)                 │
│                                                                         │
│  MCP-Hub/drive-tools (Preprocessors)                                    │
│  ├─ fetch-sheet.js — reusable Google Sheets → JSON reader              │
│  ├─ preprocess-life.js, preprocess-annuity.js, etc. (proven patterns)  │
│  └─ All new preprocessors committed here                                │
│                                                                         │
│  Hookify (Immune System — 22 rules, real-time enforcement)              │
│  ├─ block-direct-matrix-write — prevents bypassing RAPID_CORE          │
│  ├─ block-phi-in-logs — prevents PHI in console output                 │
│  ├─ block-hardcoded-matrix-ids — forces getMATRIX_ID()                 │
│  └─ intent-atlas-consult — forces ATLAS check before data work         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Per-step Machine usage:**

| Step | ATLAS | RAPID_CORE | RAPID_IMPORT | Pipeline | Preprocessor |
|------|-------|------------|--------------|----------|-------------|
| 0 Housekeeping | Gap analysis baseline | normalizeExistingData, fullAutoMerge, inferCarriers | FIX_Normalize*, FIX_AutoMerge*, FIX_InferCarriers | — | — |
| 1-2 AI3 Import | SRC_2za0m3cf priority | bulkInsert (normalize+dedup+UUID), updateRow (orphans) | bobBuildClientGHLLookup_, new FIX_AI3Import.gs | — | NEW preprocess-ai3.js |
| 3-4 Signal Revenue | SRC_hm4xqs5i priority | bulkInsert (_REVENUE_MASTER) | new FIX_SignalRevenue.gs | — | NEW preprocess-signal-revenue.js |
| 5 Commission PDFs | P6 sources (KCL, Aetna, CoF, Humana, Wellcare, MMP) | insertRow (via approval pipeline) | scanIntakeFolders | watcher.js → Claude Vision → _APPROVAL_QUEUE → approval UI | **NONE** (existing pipeline) |
| 6-7 Carrier XLSX | Cross-ref vs MATRIX | bulkInsert | Extend IMPORT_BoBImport.gs carrier configs | — | NEW preprocess-carrier-xlsx.js |
| 8 Client Demographics | P3 advisor data | bulkInsert/updateRow on _CLIENT_MASTER | bobBuildClientGHLLookup_ | — | NEW preprocess-client-demo.js |
| 9 Quality Pass | _SOURCE_HISTORY update | normalize, infer, reconcile, merge | All FIX_ wrappers | — | — |
| 10 Verify + Ship | _SOURCE_HISTORY, _TOOL_REGISTRY | — | — | — | — |

---

## STEP 0: HOUSEKEEPING (Do First)

### 0A: Commit _RPI_STANDARDS
```bash
cd ~/Projects/_RPI_STANDARDS && git add -A && git commit -m "Add ATLAS briefing + intent-atlas-consult hookify rule" && git push
```

### 0B: Run overdue data quality on existing records
Execute via `execute_script` on RAPID_IMPORT (scriptId from `.clasp.json`), `devMode: true`:

1. `FIX_NormalizeLife` → `FIX_NormalizeAnnuity` → `FIX_NormalizeBDRIA` (IMPORT_BoBEnrich.gs)
2. `FIX_InferCarriers_All` (FIX_CarrierInference.gs) — run AFTER normalization
3. `FIX_AutoMergeAccountsDryRun` → review → `FIX_AutoMergeAccounts`

### 0C: Log baseline counts
Run `DEBUG_ActiveCounts` and record totals per tab. This is the "before" snapshot.

**Machine components used:** RAPID_CORE.normalizeExistingData, RAPID_CORE.fullAutoMerge, FIX_CarrierInference (learn+fill algorithm)

---

## STEP 1: AI3 COMBINED PREPROCESSOR (Node.js)

### Build: `~/Projects/RAPID_TOOLS/MCP-Hub/drive-tools/preprocess-ai3.js`

**Input:** Sheet `1NmTT8g554PT1xTLKJYgDLkmB8x21KovsvcPQQZaXeuc` (~3,972 rows x 330 cols)

**Algorithm — Unpivot the wide-format pivot table:**

1. Use `fetch-sheet.js` pattern to read all rows via Google Sheets API
2. Parse header row to discover slot positions:
   - `N - ANNUITY-` prefix (N=1..9, ~18 fields each)
   - `N - LIFE-` prefix (N=1..4, ~16 fields each)
   - `N - MEDICARE-` prefix (N=1..4, ~13 fields each)
3. For each row:
   - Extract `Contact Id` (col A) → `gid` (GHL contact ID)
   - Extract `First Name`, `Last Name` → `fn`, `ln`
   - Loop ANNUITY slots 1-9: if `Account #` non-empty → emit annuity record
   - Loop LIFE slots 1-4: if `Policy #` non-empty → emit life record
   - Loop MEDICARE slots 1-4: if `Policy #` non-empty → emit medicare record
4. Strip `$`, commas from numeric fields. Normalize dates to YYYY-MM-DD.
5. Output: `var AI3_ANNUITY_DATA = [...]`, `var AI3_LIFE_DATA = [...]`, `var AI3_MEDICARE_DATA = [...]`

**Key maps (Annuity):** gid→ghl_contact_id, an→account_number, cr→carrier_name, at→account_type, pd→product_name, st→status, id→issue_date, ts→tax_status, ao→as_of_date, av→account_value, sv→surrender_value, ib→income_benefit, bob→book_of_business

**Key maps (Life):** gid→ghl_contact_id, pn→policy_number, cr→carrier_name, pt→policy_type, pd→product_name, st→status, id→issue_date, pm→premium_mode, sp→scheduled_premium, av→cash_value, sv→surrender_value, ins→insured, db→death_benefit, bob→book_of_business

**Key maps (Medicare):** gid→ghl_contact_id, pn→policy_number, cr→carrier_name, pt→core_product_type, pd→plan_name, st→status, ed→effective_date, sp→planned_premium, pm→premium_mode, bob→book_of_business

**Verification:** Log record counts per product line. Expect most contacts have 0-2 accounts per line.

---

## STEP 2: AI3 GAS IMPORT + ORPHAN RESOLVER

### Build: `~/Projects/RAPID_TOOLS/RAPID_IMPORT/FIX_AI3Import.gs`

**Functions:**
```
FIX_ImportAI3Annuity_DryRun() / FIX_ImportAI3Annuity()
FIX_ImportAI3Life_DryRun() / FIX_ImportAI3Life()
FIX_ImportAI3Medicare_DryRun() / FIX_ImportAI3Medicare()
FIX_BackfillOrphansFromAI3_DryRun() / FIX_BackfillOrphansFromAI3()
```

**Import pattern (follows FIX_ImportLifeBob_ exactly):**
1. Build `ghl_contact_id → client_id` lookup from _CLIENT_MASTER (using `bobBuildClientGHLLookup_()`)
2. Build `FIRST|LAST → client_id` name index from _CLIENT_MASTER (fallback)
3. Build existing policy/account number index from target tab (dedup)
4. For each inline data record:
   - Skip if policy/account number already exists in MATRIX
   - Resolve client_id: try GHL lookup via `gid`, then name match via `fn|ln`
   - Build data object matching TAB_SCHEMA fields
   - Set `import_source = 'ai3_combined'`, timestamps = now
5. **Use `RAPID_CORE.bulkInsert(tabName, newRecords)`** — handles normalization, parent_carrier derivation, UUID gen, timestamps automatically
6. Chunk into batches of 200 if needed (6-min limit protection)

**CRITICAL: Use RAPID_CORE.bulkInsert(), NOT direct setValues().** Hook-enforced by `block-direct-matrix-write`.

**Orphan backfill (FIX_BackfillOrphansFromAI3):**
1. Build `ghl_contact_id → client_id` from _CLIENT_MASTER
2. For each account tab: find rows where client_id is blank
3. If ghl_contact_id resolves → call `RAPID_CORE.updateRow(tabName, recordId, { client_id: resolved })`
4. Also try name matching for records with no ghl_contact_id
5. **Target: reduce 153 orphans to < 30**

**Execution order:** clasp push → DryRun all three → Live all three → DryRun orphan backfill → Live → Log counts

---

## STEP 3: SIGNAL TRANSACTIONS PREPROCESSOR (Node.js)

### Build: `~/Projects/RAPID_TOOLS/MCP-Hub/drive-tools/preprocess-signal-revenue.js`

**Input:** Sheet `1GFCd72nuYw19HscUR58lDNkdkb_aUBeYCiEOELomuDg` (Jan 2023 - Nov 2025)

**Algorithm:**
1. Read all rows via `fetch-sheet.js` pattern
2. Map Signal `line_type` → MATRIX revenue `type`:
   - Standard Commission / Excess → FYC
   - True-Up Received → FYC
   - As Earned / Renewal / Trail → REN
   - Override / Bonus → OVR
3. Parse amounts, dates to YYYY-MM-DD
4. Output: `var SIGNAL_REVENUE_DATA = [...]`

**Key maps:** pn→policy_number, am→amount, ty→type, pd→payment_date, cr→carrier, an→advisor_name, cn→client_name, src→source

**Verification:** Row count, total amount sum, distribution by type (FYC/REN/OVR).

---

## STEP 4: SIGNAL REVENUE GAS IMPORT

### Build: `~/Projects/RAPID_TOOLS/RAPID_IMPORT/FIX_SignalRevenue.gs`

**Functions:** `FIX_ImportSignalRevenue_DryRun()` / `FIX_ImportSignalRevenue()`

**Algorithm:**
1. Build policy_number → account_id lookup from _ACCOUNT_LIFE + _ACCOUNT_ANNUITY
2. Build advisor_name → agent_id lookup from _AGENT_MASTER + _USER_HIERARCHY
3. For each record: resolve account_id + agent_id, build _REVENUE_MASTER row
4. Write via `RAPID_CORE.bulkInsert('_REVENUE_MASTER', records)` — no dedup on revenue (transactions always insert)
5. Chunk batches of 500 if > 1000 records

**Verification:** DryRun first. Account linkage >60%, agent linkage >80%.

---

## STEP 5: COMMISSION PDFs (P6) — EXISTING PIPELINE, NO NEW CODE

**This step uses the document pipeline that's already built and running.** No new preprocessors or GAS functions needed.

### What to do:
1. **Locate the commission PDFs** in Drive for these 6 carriers:
   - KCL (in Data Vault `CARRIER_DATA/LIFE/KCL/` — 27 files, mostly PDFs)
   - Aetna (MAPD commission statements)
   - CoF (Catholic Order of Foresters)
   - Humana (MAPD commission statements)
   - Wellcare (MAPD commission statements)
   - MMP (MAPD commission statements)

2. **Drop PDFs into `SPC_INTAKE` folder** (the monitored intake folder)
   - watcher.js (`com.rpi.document-watcher` launchd agent) picks them up automatically
   - Claude Vision extracts structured data
   - Records land in `_APPROVAL_QUEUE` for human review
   - After approval → MATRIX via RAPID_CORE.insertRow()

3. **Alternatively:** Forward commission emails to the monitored email inbox (for carriers that send statements via email)

**Machine components used:**
- `watcher.js` (always-on launchd agent) — scanIntakeFolders
- Claude Vision extraction — classifies and extracts structured data from PDFs
- `_APPROVAL_QUEUE` — human-in-the-loop before MATRIX write
- `RAPID_CORE.insertRow()` — called by approval pipeline, full normalization

**Why this is powerful:** Zero new code. The pipeline was built to handle exactly this. PDFs go in, structured data comes out, human approves, MATRIX updates. The Machine works.

**Verification:** After dropping PDFs, check `_APPROVAL_QUEUE` for new pending items. Verify extraction quality on first few before bulk-dropping.

---

## STEP 6: CARRIER XLSX RECONNAISSANCE (P5 — Phase 1: Discover)

Before importing anything from the 37 carrier subfolders, we need to know what's new vs what's already in MATRIX.

### What to do:
1. **Inventory the carrier subfolders:**
   - Annuity: 20 subfolders (AEL, AIG, ALZ, Americo, Athene, AXA, BHF, DEL, F&G, Global Atlantic, JH, JNL, KCL, LFG, MNL, NAC, NAS, NWF, PAC, PFG)
   - Life: 5 subfolders (Ameritas, F&G, JH, KCL, NAC)
   - BD/RIA: 12 subfolders (Advisory-Schwab, Advisory-Pershing, etc.)

2. **For each subfolder:** List XLSX/CSV files (skip PDFs — those go through P6 pipeline)

3. **Cross-reference:** For each XLSX, read the account/policy numbers and check against existing MATRIX records
   - Build a "delta report": New records not in MATRIX vs duplicates already imported
   - Only import the delta

### Build: `~/Projects/RAPID_TOOLS/MCP-Hub/drive-tools/preprocess-carrier-xlsx.js`

This preprocessor must handle multiple carriers with different column layouts. Design pattern:
- Carrier config map: `{ 'NAC': { accountCol: 'Policy Number', carrierName: 'North American', ... }, 'AEL': { ... } }`
- For each XLSX: detect carrier from folder name → apply config → emit normalized records
- Output: `var CARRIER_ANNUITY_DATA = [...]`, `var CARRIER_LIFE_DATA = [...]`, `var CARRIER_BDRIA_DATA = [...]`

**Note:** Many of these XLSX files are the SAME data that's already in the curated ProDash BoB sheets (just carrier-specific views). The cross-reference step is critical to avoid mass duplication.

---

## STEP 7: CARRIER XLSX IMPORT (P5 — Phase 2: Import Delta)

### Build: `~/Projects/RAPID_TOOLS/RAPID_IMPORT/FIX_CarrierXlsxImport.gs`

**Functions:**
```
FIX_ImportCarrierAnnuity_DryRun() / FIX_ImportCarrierAnnuity()
FIX_ImportCarrierLife_DryRun() / FIX_ImportCarrierLife()
FIX_ImportCarrierBDRIA_DryRun() / FIX_ImportCarrierBDRIA()
```

Same pattern as Step 2: inline data → client matching → dedup → `RAPID_CORE.bulkInsert()`

**import_source:** `'carrier_xlsx_{carrier}_{date}'` (e.g., `carrier_xlsx_nac_20250806`)

**Verification:** DryRun counts should be SMALL (mostly duplicates filtered out). If DryRun shows hundreds of new records for a single carrier, investigate — likely a schema mismatch, not truly new data.

---

## STEP 8: ADVISOR CLIENT SUBFOLDERS (P3)

### What to do:
1. **Read CoF Clients sheet** (`1dQ_1AsN90rKit495W7K3suvfd_OJPREaymrv818R3F4`)
2. **Scan Client Data Hub subfolders** (folder `1SdvvD7RAQZmKadBtG13nyorVWHp8KzWW`): ALEX, ARCH, Christa, DEX, MFG
3. These contain **client demographics** — names, addresses, DOBs, contact info
4. Target: `_CLIENT_MASTER` enrichment (fill blanks on existing records) + new client creation for unmatched

### Build: `~/Projects/RAPID_TOOLS/MCP-Hub/drive-tools/preprocess-client-demo.js`
### Build: `~/Projects/RAPID_TOOLS/RAPID_IMPORT/FIX_ClientDemoImport.gs`

**Pattern:**
- For existing clients (matched by name or ghl_contact_id): `RAPID_CORE.updateRow()` to fill blanks only (never overwrite)
- For new clients: `RAPID_CORE.bulkInsert('_CLIENT_MASTER', newClients)`
- **import_source:** `'advisor_client_{subfolder}'`

**This is the orphan GAP FILLER** — after AI3 resolves the GHL-linked orphans (Step 2), these advisor files fill the remaining gaps where clients exist in carrier data but not in our CRM.

---

## STEP 9: FINAL DATA QUALITY PASS

Run in sequence via `execute_script` after ALL imports complete:

| # | Function | Purpose |
|---|----------|---------|
| 9A | FIX_NormalizeLife/Annuity/BDRIA/Medicare | Normalize all records including new imports |
| 9B | FIX_InferCarriers_All | Fill remaining blank carriers (max patterns available now) |
| 9C | FIX_AutoMergeClientsDryRun → Live | Client dedup (score >= 85) |
| 9D | FIX_AutoMergeAccountsDryRun → Live | Account dedup (score >= 85) |

**Machine components:** Every normalizer, inference engine, and dedup algorithm running on the full dataset.

**Targets:**
- Orphans: Life < 20, Annuity < 10, BD/RIA < 5
- Blank carriers: Life < 30, Annuity < 5
- Zero duplicate accounts above score 85

---

## STEP 10: VERIFY + COMMIT + ATLAS UPDATE + TOOL REGISTRATION

### 10A: Final verification
- `DEBUG_ActiveCounts` vs Step 0 baseline → delta report
- `FIX_ScanClientDuplicates` + `FIX_ScanAccountDuplicates` → confirm clean

### 10B: Update ATLAS _SOURCE_HISTORY
Log all imports with source ID, date, record counts, target tabs:
- SRC_2za0m3cf (AI3 Combined)
- SRC_hm4xqs5i (Signal Transactions)
- P6 carriers (KCL, Aetna, CoF, Humana, Wellcare, MMP) — log intake queue submissions
- P5 carrier XLSX sources
- P3 advisor client sources

### 10C: Register new tools in ATLAS _TOOL_REGISTRY
Every new preprocessor and GAS function gets registered:
- `preprocess-ai3.js` → INTAKE_QUEUING category
- `preprocess-signal-revenue.js` → INTAKE_QUEUING
- `preprocess-carrier-xlsx.js` → INTAKE_QUEUING
- `preprocess-client-demo.js` → INTAKE_QUEUING
- `FIX_AI3Import.gs` → BULK_OPERATIONS
- `FIX_SignalRevenue.gs` → BULK_OPERATIONS
- `FIX_CarrierXlsxImport.gs` → BULK_OPERATIONS
- `FIX_ClientDemoImport.gs` → BULK_OPERATIONS

### 10D: Commit + Deploy
```bash
# RAPID_IMPORT
cd ~/Projects/RAPID_TOOLS/RAPID_IMPORT
clasp push --force
git add -A && git commit -m "Phase 3b: AI3 + Signal revenue + carrier XLSX + client demo imports" && git push

# MCP-Hub
cd ~/Projects/RAPID_TOOLS/MCP-Hub
git add -A && git commit -m "Phase 3b: 4 new preprocessors (ai3, signal-revenue, carrier-xlsx, client-demo)" && git push
```

### 10E: Build audit report on Shared Drive
Google Doc with final numbers, delta report, audit trail.

---

## AUDIT AGENT CHECKLIST

| Check | Pass Criteria |
|-------|---------------|
| All MATRIX writes via RAPID_CORE | bulkInsert/insertRow/updateRow only. No direct setValues(). |
| Every record has `import_source` | Zero blanks from this session |
| Carrier normalization | Zero raw names that have a known alias |
| parent_carrier derived | All carrier records have parent_carrier where applicable |
| Dedup pass executed | FIX_AutoMerge ran on both clients AND accounts |
| Orphan reduction | 153 → target < 30 |
| Blank carrier reduction | 160 → target < 35 |
| Revenue linkage | >60% of Signal transactions linked to account_id |
| Commission PDFs in pipeline | PDFs submitted to SPC_INTAKE, items visible in _APPROVAL_QUEUE |
| Carrier XLSX cross-referenced | Delta report shows only truly-new records imported |
| ATLAS _SOURCE_HISTORY | All imports logged with counts + dates |
| ATLAS _TOOL_REGISTRY | All 8 new tools registered |
| Git committed | RAPID_IMPORT + MCP-Hub + _RPI_STANDARDS all committed |
| No PHI in logs | Zero PHI patterns in console.log/Logger.log |
| No hardcoded MATRIX IDs | All use getMATRIX_ID() or TABLE_ROUTING |

---

## Critical Files Reference

| File | Role |
|------|------|
| `RAPID_IMPORT/FIX_LifeBob.gs` | **Pattern to follow** for all new import functions |
| `RAPID_IMPORT/IMPORT_BoBEnrich.gs` | Shared helpers + normalization/dedup/inference wrappers |
| `RAPID_IMPORT/FIX_CarrierInference.gs` | Post-import carrier gap filling |
| `RAPID_IMPORT/IMPORT_Revenue.gs` | Revenue config + Stateable patterns (reference for Signal) |
| `RAPID_IMPORT/IMPORT_BoBImport.gs` | Carrier-specific tab configs (extend for P5) |
| `RAPID_CORE/CORE_Database.gs` | bulkInsert, insertRow, updateRow, TAB_SCHEMAS, TABLE_ROUTING |
| `RAPID_CORE/CORE_Normalize.gs` | normalizeCarrierName, deriveParentCarrier, CARRIER_ALIASES |
| `MCP-Hub/drive-tools/fetch-sheet.js` | Reusable Sheets reader |
| `MCP-Hub/drive-tools/preprocess-life.js` | **Pattern to follow** for preprocessor structure |

---

## Parallel Execution Opportunities

| Can Run In Parallel | Why |
|--------------------|----|
| Step 0A (git commit) + Step 1 (AI3 preprocessor) | Independent |
| Step 1 (AI3 preprocessor) + Step 3 (Signal preprocessor) | Independent Node.js scripts |
| Step 2 Annuity/Life/Medicare imports | Independent tabs |
| Step 5 (PDF drop) can start during Steps 1-4 | Separate pipeline entirely |
| Step 6 (XLSX recon) can start during Steps 3-4 | Independent research |
| Steps 9A-9B (normalize + infer) must be sequential | Inference learns from normalization |
| Steps 9C-9D (client + account dedup) must be sequential | Client merges affect account orphans |

---

## New Files Created by This Plan

| File | Location | Type |
|------|----------|------|
| `preprocess-ai3.js` | MCP-Hub/drive-tools/ | Node.js preprocessor |
| `preprocess-signal-revenue.js` | MCP-Hub/drive-tools/ | Node.js preprocessor |
| `preprocess-carrier-xlsx.js` | MCP-Hub/drive-tools/ | Node.js preprocessor |
| `preprocess-client-demo.js` | MCP-Hub/drive-tools/ | Node.js preprocessor |
| `FIX_AI3Import.gs` | RAPID_IMPORT/ | GAS import + orphan resolver |
| `FIX_SignalRevenue.gs` | RAPID_IMPORT/ | GAS revenue import |
| `FIX_CarrierXlsxImport.gs` | RAPID_IMPORT/ | GAS carrier XLSX import |
| `FIX_ClientDemoImport.gs` | RAPID_IMPORT/ | GAS client demo import |
