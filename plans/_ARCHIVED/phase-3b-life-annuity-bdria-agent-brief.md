ARCHIVED: Consolidated into tomachina-epic-roadmap.md on 2026-03-13
# Phase 3b Agent Brief — Life, Annuity, BD/RIA Import

> **Delegate to:** Builder Agent (either machine)
> **Parent plan:** `_RPI_STANDARDS/plans/drifting-snuggling-crystal.md` (Operation Data Foundation)
> **Prerequisites:** Phases 1-2 COMPLETE, 3b-Medicare COMPLETE
> **Scope:** Import Life, Annuity, and BD/RIA account data into PRODASHX MATRIX

---

## What You're Doing

Importing structured account data from Google Sheets and Drive files into `_ACCOUNT_LIFE`, `_ACCOUNT_ANNUITY`, and `_ACCOUNT_BDRIA` tabs in PRODASHX MATRIX. Follow the proven pattern from 3b-Medicare.

---

## Before You Start

1. Read the parent plan: `_RPI_STANDARDS/plans/drifting-snuggling-crystal.md`
2. Read `RAPID_IMPORT/CLAUDE.md` for the BoB Import/Enrichment workflow
3. Read `RAPID_CORE/CLAUDE.md` for MATRIX schemas + normalizeData_() behavior
4. Run `DEBUG_ActiveCounts` via execute_script on RAPID_IMPORT to get current baseline
5. Run `DEBUG_Ping` on RAPID_CORE to verify connectivity

---

## Priority Order

### 1. LIFE (Priority — existing data is 80% CoF, needs carrier diversity)

**Current state:** 4,937 records (4,699 active). 80% from cof_members, 19% from GHL_BULK.

**Sources to import (in this order):**

**A. RPI+ProDash Life BoB (Google Sheet — PRIMARY)**
- Sheet ID: `1AdyI3zekCuToEStRVv3lzuJx-cxP3LD5DfJovRtjXf0`
- Fields: Policy #, Policy Owner, ACF Link, Carrier, Product Name, Type, Issue Date, Status, Book of Business, Market, Insured, As-Of Date, Cash Value, Data Source, Loan Principal, Dividend Option-1, Scheduled Premium, Premium Mode, Preferred Draft Date, ANNUALIZED Premium, DB Option, MEC, Underwriting Status, Dividend Option-2, NET Cash Surrender Value, Joint Owner
- Read ALL rows. This is curated data with carrier + product already populated.
- Import into `_ACCOUNT_LIFE` via the BoB import pattern.

**B. Signal Life Export (Google Sheet)**
- Sheet ID: `1Kz2sSAzq8oxeYxkWlnqbrZD7qhIntmHCBK0rguBR2OI`
- Fields: Policy Number, Client Name, Carrier, Product, Issue Date, Advisor, Premium, Values
- 96 records. Cross-reference with ProDash Life BoB to avoid duplicates.
- NOTE: CONFIRMED — Signal Life Export and Signal Annuity Export share identical schemas and both contain annuity carriers (NAC, Sentinel Security Life). These are likely a single combined Life+Annuity dataset. During import, inspect carrier/product values row-by-row to route to correct MATRIX tab.

**C. Data Vault Life files (uploaded from local disk)**
- Location: Data Vault `CARRIER_DATA/LIFE/` subfolders
- KCL (27 files — mix of XLSX BoB exports + PDF statements), ALIC (16 — 1 CSV BoB + 15 PDF statements), F&G (12 PDF statements), CoF (2 files), JH (1 XLSX BoB), Lincoln (1 PDF), NAC (2 — 1 XLSX BoB + 1 PDF)
- **Key XLSX files to process:** `!KCL In-Force Policies 4.3.24.xlsx`, `!22 ALIC UL BoB.csv`, `!JH- Inforce Policies_08.26.2024.xlsx`, `!Alex NAC BoB.xlsx`
- PDF statements are individual client docs — lower priority, may not need bulk import.

**D. Account/BoB Hub Life subfolders (pre-existing Drive)**
- Parent: https://drive.google.com/drive/folders/1ceb5gvi-6S32cdEu5jrWpLjY36EzUGc-
- 5 carrier subfolders: Ameritas, F&G, JH, KCL, NAC
- Check for additional XLSX/CSV BoB exports not already in the Data Vault.

### 2. ANNUITY (most new data available — currently 92% GHL)

**Current state:** 904 records (794 active). 92% from GHL_BULK.

**Sources to import (in this order):**

**A. RPI+ProDash Annuity BoB (Google Sheet — PRIMARY)**
- Sheet ID: `1gqQgclh0mIDFDJGJOnVn-lQhy-j1vCocNeWw8sndwPo`
- Fields: Account #, Account Owner, ACF Link, Carrier, Type, Product Name, Issue Date, Status, Market, Book of Business, Tax Status, Payment Amount, Underwriting Status, Payment Mode, Account Value, Annuitant, MYGA Rate, Payment Frequency, Joint Owner, Surrender Value, MYGA Guarantee Period, Net Deposits, Return % (Cumulative), Return % (Annualized), Death Benefit, Income Benefit
- Read ALL rows. Curated data.

**B. BookOfBusiness_20250806 — NAC (Google Sheet)**
- Sheet ID: `1QZyxBmHrg78ohMdVDpkp-TqxcoajYIG8xH7QTIMoWrI`
- 111+ records, ALL North American Company FIAs
- Fields: Policy Number, Status, Product Type/Name, Tax Status, Account Value, Issue Age/State, Owner Name, Writing Agent
- Rich data — has account values, issue state, tax status.

**C. Signal Annuity Export (Google Sheet)**
- Sheet ID: `11F07R5OFIoCy-PbzivYE8qj0E6oLlJ3Uh01OSv-bkyc`
- 96 records with valuations + advisor assignments
- Cross-reference with ProDash Annuity BoB to avoid duplicates.

**D. Account/BoB Hub Annuity subfolders (pre-existing Drive — LARGEST SOURCE)**
- Parent: https://drive.google.com/drive/folders/11039yU6hrvpPyKfxyiT2_ieaOLHQpzSx
- **20 carrier subfolders:** AEL, AIG, ALZ, Americo, Athene, AXA, BHF (Met), DEL (SLF), F&G, Global Atlantic, JH, JNL, KCL, LFG, MNL, NAC, NAS, NWF, PAC, PFG
- Check each for XLSX/CSV BoB exports. Many will be PDF statements (lower priority).
- Also contains: `BookOfBusiness_20250806` (3 copies), `Signal Annuities Export.xlsx`, `BoB_Signal_Export_2025-08-15 Annuity`

### 3. BD/RIA (needs custodian data — currently 75% GHL)

**Current state:** 325 records (251 active). 75% from GHL_BULK.

**Sources to import:**

**A. Account/BoB Hub BD/RIA subfolders (pre-existing Drive — ONLY SOURCE)**
- Parent: https://drive.google.com/drive/folders/1ieTiAd0h_d9wwpCecs98uE0_WznPLLoO
- 12 subfolders: Advisory-Schwab (SIGNAL), Advisory-Pershing/SIS (WFS), Advisory-TDAI (Ameritas), Brokerage-NFS (Advisor Group), Brokerage-Pershing (WFS), Direct-401k, Direct-ALTS.MULT (WFS), Direct-Mutual Funds.MULT, Direct-TAMP.Curian (SFS), Direct-TAMP.SEI (SFS), Christa-Schwab Statements, ARCHIVE-AIC.WFS.SFS Business
- Key files: `!Archer-Accounts.xlsx`, `*Balances_Firm_BROOKSTONE...csv`, Schwab statements, Pershing SIS reports
- Also: `ProDash Dowload- BD:RIA` (Google Sheet ID: `1wDfpqNhUnAomVuIi3io1XYcl0qKgk2JEwBTxpzFYNwA`)
  - NOTE: GHL pipeline export — multi-account-per-row format (columns prefixed `1 - BD/RIA-*`, `2 - BD/RIA-*`, etc.). **Needs unpivoting** during preprocessing to normalize to one-account-per-row.
- Also: `Profile_Firm_SIGNAL_ADVISORS_WEALTH_LLC...` (Google Sheet ID: `11VOanoznqNIEd48demNrOki9otUN4CMZfUgzgIJne-I`)
  - NOTE: Report-style export — metadata in rows 1-2 ("104 Records exported", firm profile summary). **Data headers start on row 3+.** Needs row-offset handling during preprocessing.

---

## Import Pattern (proven in 3b-Medicare)

For each source:

1. **Read the Google Sheet** via `mcp__gdrive__getGoogleSheetContent` to understand schema + record count
2. **Download/extract data** — for Sheets, read all rows; for XLSX on Drive, download and parse
3. **Preprocess** — build Node.js script (like `preprocess-medicare.js`) that converts to compact inline JS objects
4. **Build GAS function** — `FIX_Import{Product}Bob.gs` with inline data + import logic
5. **Client matching** — match by `FIRST|LAST` uppercase against `_CLIENT_MASTER`. Handle ambiguous names.
6. **Carrier normalization** — use `RAPID_CORE.normalizeCarrierName()`. The NAIC auto-population is wired in.
7. **DryRun first** — always preview before writing
8. **Execute** — batch write via `setValues()` for speed (same pattern as Medicare fast-batch)
9. **Post-import:** Run `FIX_Normalize{Product}` to backfill naic_code + parent_carrier
10. **Dedup:** Run `FIX_AutoMergeAccounts` (85+ score threshold)
11. **Verify:** Run `DEBUG_ActiveCounts` and compare before/after

---

## Key Rules

- **ALL writes eventually go through RAPID_CORE normalization** — carrier_name, parent_carrier, naic_code auto-populated
- **Dedup AFTER each import batch** — don't let dupes accumulate
- **Source tracking** — set `import_source` on every record (e.g., `prodash_life_bob`, `signal_export_20250815`, `nac_bob_20250806`)
- **Don't import PDF statements** — those are individual client documents, not bulk data. Only import structured XLSX/CSV/Google Sheet data.
- **Cross-reference between sources** — the ProDash BoB sheets, Signal exports, and carrier-specific exports will overlap. Use policy_number as the primary dedup key.
- **Commit preprocess scripts to git** — the Medicare audit flagged this. Every preprocessing script goes into `MCP-Hub/drive-tools/`

---

## MATRIX Tab Schemas (for reference)

> **WARNING:** These are key fields only. The actual schemas have 50+ fields each.
> **ALWAYS read `RAPID_CORE/CORE_Database.gs` TAB_SCHEMAS before building import functions.**

**_ACCOUNT_LIFE** key fields: `life_id`, `account_id`, `ghl_object_id`, `ghl_contact_id`, `client_id`, `policy_number`, `carrier_name`, `parent_carrier`, `naic_code`, `product_name`, `product_code`, `policy_type`, `status`, `issue_date`, `as_of_date`, `face_amount`, `cash_value`, `net_cash_surrender_value`, `scheduled_premium`, `annual_premium`, `premium_mode`, `premium_frequency`, `death_benefit_option`, `book_of_business`, `import_source`
- NOTE: No `effective_date` — uses `issue_date` + `as_of_date` separately
- NOTE: No single `premium` — uses `scheduled_premium`, `annual_premium`, `premium_mode`, `premium_frequency`
- NOTE: No `product_type` — uses `product_code`

**_ACCOUNT_ANNUITY** key fields: `annuity_id`, `account_id`, `ghl_object_id`, `ghl_contact_id`, `client_id`, `account_number`, `carrier_name`, `parent_carrier`, `naic_code`, `product_name`, `product_code`, `status`, `issue_date`, `maturity_date`, `as_of_date`, `surrender_period_end`, `account_value`, `surrender_value`, `net_deposits`, `tax_status`, `death_benefit`, `income_benefit_base`, `book_of_business`, `import_source`
- NOTE: Uses `account_number`, NOT `policy_number`
- NOTE: No `effective_date` — uses `issue_date`, `maturity_date`, `as_of_date`, `surrender_period_end`
- NOTE: No `premium` field — annuities track `account_value`, `net_deposits` instead
- NOTE: No `product_type` — uses `product_code`

**_ACCOUNT_BDRIA** key fields: `bdria_id`, `account_id`, `ghl_object_id`, `ghl_contact_id`, `client_id`, `account_number`, `custodian`, `bd_ria_firm`, `advisor_of_record`, `fund_family`, `account_type`, `status`, `opened_date`, `as_of_date`, `account_value`, `advisory_fee`, `book_of_business`, `import_source`
- NOTE: BDRIA does NOT use `carrier_name`/`parent_carrier`/`product_name`/`product_type` — it uses `custodian`, `bd_ria_firm`, `fund_family` instead
- NOTE: No `effective_date` — uses `opened_date` + `as_of_date`
- NOTE: BDRIA schema is fundamentally different from Life/Annuity — it's brokerage/advisory, not insurance

---

## Deliverables

For each product line, provide:
1. Record counts: imported, matched to clients, deduped, final active
2. Carrier distribution of imported records
3. Deploy report (clasp push, version, deploy, verify, git commit, git push)
4. Any preprocessing scripts committed to `MCP-Hub/drive-tools/`
5. Update the parent plan tracker (`drifting-snuggling-crystal.md`) with completion status

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Life active records | Significantly more than current 4,699 (add carrier-specific data beyond CoF/GHL) |
| Annuity active records | Significantly more than current 794 (add 20-carrier diversity) |
| BD/RIA active records | Increase from current 251 (add custodian-specific data) |
| All records have carrier_name | >95% |
| All records with carrier have naic_code | 100% (auto-populated) |
| All records with carrier have parent_carrier | 100% where applicable |
| Zero errors on import | 0 |
| Dedup pass after each import | Required |
| Preprocess scripts committed | Required |
