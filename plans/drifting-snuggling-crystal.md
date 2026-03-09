# Operation Data Foundation — Bottom-Up Data Quality Blitz

## Execution Tracker

> **Last updated:** 2026-03-09 — Build Session 1 complete (Phases 1-2 full + 3a + 3b-Medicare)
> **Status:** IN PROGRESS — Foundation + Medicare import complete
> **Plan file:** `_RPI_STANDARDS/plans/drifting-snuggling-crystal.md`
> **Origin session:** ATLAS audit Q&A → discovered fragmented data → bottom-up plan

| Phase | Status | Started | Completed | Blocker | Notes |
|-------|--------|---------|-----------|---------|-------|
| **1a** Create Drive structure | COMPLETE | 2026-03-09 | 2026-03-09 | — | 58 folders on Shared Drive |
| **1b** Upload local data | COMPLETE | 2026-03-09 | 2026-03-09 | — | 153 files / 88.5 MB uploaded via drive-tools/upload.js, 0 errors |
| **1c** Dedup + garbage removal | COMPLETE | 2026-03-09 | 2026-03-09 | — | 3 dupes deleted, 13 superseded archived, IMPORT_EXCLUSIONS.md created |
| **2a** Populate _CARRIER_MASTER | COMPLETE | 2026-03-09 | 2026-03-09 | — | 134 carriers seeded |
| **2b** Populate _PRODUCT_MASTER | COMPLETE | 2026-03-09 | 2026-03-09 | — | 283 carrier x product combos |
| **2c** Verify CARRIER_ALIASES | COMPLETE | 2026-03-09 | 2026-03-09 | — | 53 new aliases added, 24 new carriers seeded, 8 normalization failures fixed. Totals: 158 carriers, 325 products |
| **3a** Audit PRODASHX MATRIX current state | COMPLETE | 2026-03-09 | 2026-03-09 | — | 18,415 records audited, gaps documented |
| **3b-Medicare** Import Medicare data | COMPLETE | 2026-03-09 | 2026-03-09 | — | 4,638 records: 233 inserted w/dedup, 267 merged, 4,138 batch appended. 87.3% client matched. |
| **3b-Life** Import Life data | NOT STARTED | — | — | Needs 1+2 | Priority 2 |
| **3b-Annuity** Import Annuity data | NOT STARTED | — | — | Needs 1+2 | Priority 3 |
| **3b-BDRIA** Import BD/RIA data | NOT STARTED | — | — | Needs 1+2 | Priority 4 |
| **3b-Commissions** Import commission data | NOT STARTED | — | — | Needs 1+2 | Priority 5 |
| **3d** Commission stream mapping | NOT STARTED | — | — | Needs 1 | Answers ATLAS Audit Finding #2 |
| **4a** Enrichment sweep | NOT STARTED | — | — | Needs 3 | WhitePages, NeverBounce, USPS |
| **4b** Reconciliation | NOT STARTED | — | — | Needs 4a | Dedup + orphan linking |
| **4c** Final verification | NOT STARTED | — | — | Needs 4b | Record count validation |
| **5a** ATLAS SOURCES rewire | UNBLOCKED | — | — | — | Can start now (Phase 2 complete) |
| **5b** ATLAS OPS review | NOT STARTED | — | — | Needs 5a | — |
| **5c** Answer Q&A from data | NOT STARTED | — | — | Needs 3d+5a | — |
| **6** Launch ready | NOT STARTED | — | — | Needs 4c+5c | Team + campaigns |

### Dependency Graph
```
Phase 1a ──→ 1b ──→ 1c ──┐
                          ├──→ Phase 3 (all imports) ──→ Phase 4 ──→ Phase 6
Phase 2a ──→ 2b ──→ 2c ──┘        │                                    ↑
                    │              └── 3d (commission mapping) ──────────┤
                    └──→ Phase 5a ──→ 5b ──→ 5c ───────────────────────┘
```

### Data Locations (discovered 2026-03-09)
| Location | Size | Content | Backed Up? |
|----------|------|---------|------------|
| `RAPID_IMPORT/BoB Data Dump/+Life + Annuity- CARRIER DATA/` | 73MB | KCL, JH, NAC, Athene, F&G, ALIC, CoF, Global Atlantic, Lincoln | NO |
| `RAPID_IMPORT/BoB Data Dump/` (other folders) | 10MB | GHL exports, Aris commissions, Spark, Eastern IA M&A | NO |
| `~/Medicare BoB Formatting/` | 130MB | Aetna, UHC, BCBS, Humana, Wellmark + consolidated Medicare BoB | NO |
| `SENTINEL/sentinel/signal_*.xlsx + .json` | ~270KB | Signal life/annuity grids | NO |
| `~/Downloads/` | scattered | AFLAC BoB, CoF MFGAN, Wellmark premium | NO |
| Drive: `1BJkow8...` (EBSSR folder) | ? | Midwest Medigap/Mutual of Omaha EBSSR only | YES (partial) |
| Drive: `1nzdAWT...` (Account/BoB Hub) | ? | 20 annuity, 5 life, Medicare, BD/RIA carrier folders | YES |
| Drive: `1SdvvD7...` (Client Data Hub) | ? | ALEX, ARCH, Christa, DEX, MFG client data | YES |
| Drive: `12Y6vck...` (MFG Migration) | ? | Migration scripts, dedup docs | YES |

### Session Handoff Protocol
When resuming this plan in a new session:
1. Read this plan file FIRST
2. Check the Execution Tracker table for current status
3. Check the Blocker column — resolve blockers before starting dependent phases
4. Update Status/Started columns when beginning work
5. Update Completed column + Notes when done
6. If a phase fails or changes scope, update Notes with what happened

---

## Context

RPI has 213MB+ of carrier data scattered across local disk (unprotected), multiple Drive folders, and Downloads — representing the ENTIRETY of the business's revenue streams across Medicare, Life, Annuity, and BD/RIA. This data was never properly consolidated or imported into PRODASHX MATRIX. Meanwhile, ATLAS (the visibility layer) has been maintaining its own parallel carrier/product list instead of inheriting from RAPID_CORE.

**The problem:** PRODASHX can't launch campaigns without quality data. The data exists but is fragmented, unorganized, and unimported. ATLAS has blind spots because it's not reading from the infrastructure.

**The goal:** Get ALL carrier/account/commission data organized, imported through the existing RAPID_CORE/IMPORT/API pipeline into PRODASHX MATRIX, enriched, and verified — then rewire ATLAS to simply reflect reality.

---

## Phase 1: Secure & Organize Raw Data
**Priority: IMMEDIATE — data on local disk is unprotected**

### 1a. Create clean Shared Drive structure

```
📁 RPI Data Vault/
├── 📁 CARRIER_DATA/
│   ├── 📁 MEDICARE/
│   │   ├── 📁 Aetna/
│   │   ├── 📁 BCBS-Wellmark/
│   │   ├── 📁 Devoted/
│   │   ├── 📁 Humana/
│   │   ├── 📁 Mutual-of-Omaha/
│   │   ├── 📁 UnitedHealthcare/
│   │   └── 📁 _Consolidated/        ← merged/cleaned master files
│   ├── 📁 LIFE/
│   │   ├── 📁 Ameritas/
│   │   ├── 📁 CoF/
│   │   ├── 📁 F&G/
│   │   ├── 📁 John-Hancock/
│   │   ├── 📁 KCL/
│   │   ├── 📁 NAC/
│   │   └── 📁 _Consolidated/
│   ├── 📁 ANNUITY/
│   │   ├── 📁 Athene/
│   │   ├── 📁 F&G/
│   │   ├── 📁 Global-Atlantic/
│   │   ├── 📁 KCL/
│   │   ├── 📁 Midland-National/
│   │   ├── 📁 NAC/
│   │   └── 📁 (+ other carriers as found)/
│   ├── 📁 BDRIA/
│   │   ├── 📁 Schwab/
│   │   ├── 📁 Pershing/
│   │   ├── 📁 DST-Vision/
│   │   └── 📁 (custodian subfolders)/
│   └── 📁 COMMISSIONS/
│       ├── 📁 Stateable-EBSSR/
│       ├── 📁 Aris/
│       ├── 📁 Signal-Grids/
│       └── 📁 Direct-Carrier/
├── 📁 CLIENT_DATA/
│   ├── 📁 GHL-Exports/
│   ├── 📁 Spark-Data/
│   └── 📁 CoF-Members/
├── 📁 MFG_MIGRATION/               ← existing migration docs (preserve)
└── 📁 _ARCHIVE/                    ← anything superseded
```

**Principle:** Organized by PRODUCT LINE → CARRIER. One carrier, one folder. No advisor names, no "New Folder With Items", no date-stamped duplicates in the name.

### 1b. Move local data to Drive

| Source | Destination | Action |
|--------|-------------|--------|
| `RAPID_IMPORT/BoB Data Dump/+Life + Annuity- CARRIER DATA/` (73MB, 68 files) | Sort into `CARRIER_DATA/LIFE/` and `CARRIER_DATA/ANNUITY/` by carrier | Upload + sort |
| `~/Medicare BoB Formatting/` (130MB) | `CARRIER_DATA/MEDICARE/` by carrier + `_Consolidated/` for master files | Upload + sort |
| `SENTINEL/sentinel/signal_*.xlsx + .json` | `CARRIER_DATA/COMMISSIONS/Signal-Grids/` | Upload |
| `RAPID_IMPORT/BoB Data Dump/SPARK/` | `CLIENT_DATA/Spark-Data/` | Upload |
| `RAPID_IMPORT/BoB Data Dump/New Folder With Items*/` | `CLIENT_DATA/GHL-Exports/` | Upload |
| `RAPID_IMPORT/BoB Data Dump/aris_commissions_1/` | `CARRIER_DATA/COMMISSIONS/Aris/` | Upload |
| `RAPID_IMPORT/BoB Data Dump/+Eastern IA Agency*` | `_ARCHIVE/` (M&A historical) | Upload |
| `~/Downloads/AFLAC MFGAN- BoB.xlsx` | `CARRIER_DATA/LIFE/Aflac/` or appropriate | Upload |
| Drive: existing [BRAND][ADVISOR] BoB folders | Merge into new structure, archive originals | Reorganize |
| Drive: EBSSR folder (`1BJkow8...`) | `CARRIER_DATA/COMMISSIONS/Stateable-EBSSR/` | Move/link |

### 1c. Dedup and garbage removal
- Identify duplicate files across local + Drive (same content, different names)
- Remove superseded consolidated files (keep only the latest FINAL version)
- Flag anything that's clearly test data vs production data

**Critical files to read:**
- `~/Medicare BoB Formatting/CONSOLIDATED_Medicare_BoB_FINAL_20250621_175008.csv` — latest Medicare consolidated
- `RAPID_IMPORT/BoB Data Dump/+Life + Annuity- CARRIER DATA/*.xlsx` — carrier BoB exports
- `SENTINEL/sentinel/signal_life_grid_data.json` — Signal life grid
- `SENTINEL/sentinel/josh-book-internal.csv` — 2,239 Medicare policies

---

## Phase 2: Complete RAPID_CORE Knowledge
**Foundation — source of truth must be right before anything else**

### 2a. Populate `_CARRIER_MASTER`

`_CARRIER_MASTER` schema exists in RAPID_CORE but needs to be populated with every carrier discovered from the data. For each carrier:
- `name`: canonical name (from CARRIER_ALIASES)
- `aliases`: JSON array of all known variations
- `product_types`: JSON array of product types they offer
- `domain`: HEALTH, WEALTH, or BOTH
- `carrier_type`: INSURANCE, CUSTODIAN, BD_RIA, IMO
- `status`: ACTIVE or INACTIVE

**Source:** Cross-reference CARRIER_ALIASES (86 carriers) + actual data files found in Phase 1. Any carrier in the data that's not in CARRIER_ALIASES gets added.

### 2b. Populate `_PRODUCT_MASTER`

Schema exists but is EMPTY. Populate with every product type from `PRODUCT_TYPES` constant:
- Link each product to the carriers that offer it
- Set domain/category
- Mark which require custodian vs carrier

### 2c. Verify CARRIER_ALIASES completeness

From the data we found, ensure these carriers have aliases:
- Medicare: Aetna, UHC, Humana, BCBS, Wellmark, Devoted, Mutual of Omaha, GTL, Wellabe/Medico, Aflac
- Life: KCL, John Hancock, CoF, F&G, NAC, Ameritas, ALIC (Accordia)
- Annuity: Athene, NAC, F&G, Global Atlantic, KCL, Midland National, AEL, AIG, ALZ, Americo, AXA, BHF, JH, JNL, LFG, NAS, NWF, PAC, PFG, DEL/SLF
- BD/RIA: Schwab, Pershing, DST Vision, Brookstone, SEI, Curian, NFS/Advisor Group

**Key file:** `RAPID_CORE/CORE_Normalize.gs` (CARRIER_ALIASES constant, lines 31-250)
**Key file:** `RAPID_CORE/CORE_Carriers.gs` (all carrier CRUD functions)
**Key file:** `RAPID_CORE/CORE_Database.gs` (TABLE_ROUTING, TAB_SCHEMAS)

---

## Phase 3: Import Through RAPID_IMPORT
**Use the proven BoB Import/Enrichment workflow**

### 3a. Inventory what's already in PRODASHX MATRIX

Before importing anything, audit current state:
- `_CLIENT_MASTER` — how many records, how many with complete data
- `_ACCOUNT_MEDICARE` — how many, which carriers represented
- `_ACCOUNT_LIFE` — how many, which carriers
- `_ACCOUNT_ANNUITY` — how many, which carriers
- `_ACCOUNT_BDRIA` — how many, which custodians
- `_REVENUE_MASTER` (SENTINEL) — commission records

### 3b. Import priority order

| Priority | Product Line | Source Data | Import Method |
|----------|-------------|-------------|---------------|
| 1 | **MEDICARE** | Consolidated BoB FINAL + individual carrier BoBs + josh-book-internal | BoB Import (bulk) |
| 2 | **LIFE** | KCL, JH, NAC, CoF, F&G carrier exports + Signal Life Export | BoB Import (bulk) |
| 3 | **ANNUITY** | 20 carrier folders + Signal Annuity Export + BookOfBusiness_20250806 | BoB Import (bulk) |
| 4 | **BD/RIA** | Schwab, Pershing, DST Vision, custodian statements | BoB Import (bulk) |
| 5 | **COMMISSIONS** | Stateable EBSSR + Aris + Signal grids + direct carrier | Revenue Import |

### 3c. For each import batch

Follow the proven pattern from `RAPID_IMPORT/CLAUDE.md`:
1. Python preprocessing → compact inline JS objects
2. GAS FIX_ function with inline data (function-scoped var)
3. clasp push → DryRun → review → Execute
4. Reconciliation pass for new duplicates

**Key file:** `RAPID_IMPORT/IMPORT_BoBImport.gs` — bulk carrier BoB import
**Key file:** `RAPID_IMPORT/IMPORT_BoBEnrich.gs` — enrichment helpers
**Key file:** `RAPID_IMPORT/IMPORT_Revenue.gs` — commission/revenue import

### 3d. Commission data stream mapping

For each carrier, document:
- How commissions currently arrive (Stateable, direct PDF, Gradient, carrier portal)
- Frequency (weekly, monthly, quarterly)
- Whether automation exists or is possible (API, SFTP, manual)
- Who on the team is responsible for pulling it

This answers ATLAS Audit Finding #2 (commission gap) directly.

---

## Phase 4: Enrichment & Verification
**Blast PRODASHX MATRIX with all backend tools**

### 4a. Full enrichment sweep
- `FIX_NormalizeClients` + all account normalizers (RAPID_CORE normalization)
- `FIX_BackfillClientStatus` + `FIX_BackfillState` (fill gaps)
- WhitePages Pro (phone + address enrichment)
- NeverBounce (email validation)
- USPS address standardization
- NPI validation (for agent records)

### 4b. Reconciliation
- `FIX_ScanClientDuplicates` → review + merge
- Account-level dedup across tabs
- Orphan linking (accounts without client_id)

### 4c. Final verification
- `FIX_FinalVerification` — full quality audit
- Spot-check carrier coverage vs actual BoB files
- Compare record counts: source files vs MATRIX

**Key file:** `RAPID_IMPORT/IMPORT_BulkValidation.gs` — validation framework
**Key file:** `RAPID_IMPORT/IMPORT_Reconcile.gs` — dedup/reconciliation

---

## Phase 5: Rewire ATLAS
**ATLAS becomes a read-only window into RAPID_CORE reality**

### 5a. SOURCES section — inherit from RAPID_CORE

**Current:** `_SOURCE_REGISTRY` manually maintains carrier/product list
**Target:** ATLAS reads carrier/product universe from `_CARRIER_MASTER` + `_PRODUCT_MASTER`

Changes to `ATLAS_Audit.gs`:
- `getAuditReport()` reads `_CARRIER_MASTER` instead of just `getKnownCarrierNames()`
- Coverage matrix auto-generates from `_CARRIER_MASTER.product_types` × data domains
- Gap status computed from: does data exist in PRODASHX MATRIX for this carrier × product?

`_SOURCE_REGISTRY` retains ONLY flow metadata:
- `current_method` (API, CSV, manual)
- `current_frequency` (daily, weekly, monthly)
- `gap_status` (flowing/partial/not flowing)
- `current_owner_email`
- `last_pull_at` / `next_pull_due`

### 5b. OPS section — dynamic where possible

- Tool Registry: Consider auto-discovery from codebase vs manual seed (future sprint)
- Automation Registry: Already reads heartbeats dynamically (keep as-is)
- Wires: Keep static definitions but add wires for newly discovered data flows
- Pipeline: Already reads from live data (keep as-is)

### 5c. Answer Q&A from actual data

Replace the 54 static questions with **actual answers** derived from:
- Carrier inventory from `_CARRIER_MASTER`
- Data flow documentation from Phase 3d
- Commission stream mapping from Phase 3d
- Automation status from `_AUTOMATION_REGISTRY`

---

## Phase 6: Launch Ready
**Team migration + campaigns**

With solid data in PRODASHX MATRIX:
1. Team can see real client/account data in PRODASHX
2. C3 campaign engine has valid targets with enriched contact info
3. Service Centers (RMD, Beni) have complete account data
4. Sales Centers (QUE-Medicare, etc.) have current carrier/plan info

---

## Execution Strategy

**Parallel where possible:**
- Phase 1 (backup/organize) can start immediately — no code changes needed
- Phase 2a-2c (RAPID_CORE knowledge) can run in parallel with Phase 1
- Phase 3 (imports) depends on Phase 1 (organized data) + Phase 2 (carrier knowledge)
- Phase 4 (enrichment) depends on Phase 3 (imported data)
- Phase 5 (ATLAS rewire) can start after Phase 2 (doesn't depend on imports)

**Estimated scope:**
- Phase 1: File organization + upload (1 session)
- Phase 2: RAPID_CORE carrier/product population (1 session)
- Phase 3: Import batches by product line (2-3 sessions, parallelizable)
- Phase 4: Enrichment + verification (1 session)
- Phase 5: ATLAS code changes (1 session)
- Phase 6: Launch prep (team + campaigns)

---

## Verification

After each phase:
- **Phase 1:** All local files backed up to Shared Drive. Zero data on local disk only. `du -sh` confirms.
- **Phase 2:** `RAPID_CORE.getAllCarriers()` returns complete carrier list. `_PRODUCT_MASTER` populated.
- **Phase 3:** PRODASHX MATRIX record counts match source file record counts per carrier/product.
- **Phase 4:** Enrichment completion rates >90%. Duplicate count <50 (from thousands). Zero orphans.
- **Phase 5:** ATLAS audit report shows zero "missing carriers". Coverage matrix reflects reality.
- **Phase 6:** ProDashX loads with complete data. C3 campaign targeting returns valid recipients.
