# The Data Operating System — Permanent Data Quality Governance

## Context

After cleaning ~700 records across 5 PRODASH_MATRIX tabs (product name typos, epoch dates, garbage fields, status inconsistencies, etc.), JDM asked the right question: "Are we compiling a rules base so when we ingest data from M&A sources we're not re-learning all this shit?"

The answer: **build a Data Operating System** — the same 5-pillar governance framework as the Security OS (`_RPI_STANDARDS/reference/os/`), but applied to data quality. Every manual FIX_ correction becomes a permanent rule. Every rule becomes an automated normalizer. Every normalizer becomes a defense layer for the next M&A import.

JDM's directive: *"The Operating System. Standards / Posture / Enforcement / Monitoring / Operations. THIS is what we need for our Data."*

Additional insight: Google Drive files (policy PDFs, statements, applications) are a "monster resource" for enrichment. Both RPI's existing files and any files from future acquisitions should feed back into MATRIX to fill gaps.

---

## What Already Exists

| Layer | Current State |
|-------|---------------|
| **Normalizers** | 14 types in `normalizeData_()`, 90+ fields mapped in `FIELD_NORMALIZERS`. Fires on every `insertRow()`/`updateRow()`/`bulkInsert()` |
| **Dedup** | Phase 2 pre-write dedup in `dedupCheck_()` — scores incoming vs existing, auto-merge at 100 |
| **Reconciliation** | Phase 3 in `CORE_Reconcile.gs` — batch client/account/agent dedup scans |
| **FIX_ functions** | 22 families (44 entry points) in `IMPORT_BoBEnrich.gs` — ad-hoc corrections with DryRun pattern |
| **DEBUG_ functions** | 16 diagnostic tools — distinct values, orphan scan, field quality, numeric scan |
| **Validation APIs** | 6 functions in `CORE_Validation_API.gs` — phone (phonevalidator.com), email (NeverBounce), address (USPS v3), city/state (USPS), bank routing, composite score. All built + keyed. **Never called automatically — standalone batch functions only** |
| **Docs** | `reference/data/` has 3 files (carrier integration only). No field registry, no normalizer catalog, no M&A playbook |

**Key gaps found:**
- `product_name` and `plan_name` are NOT in `FIELD_NORMALIZERS` — pass through completely untouched
- `normalizeProductName()` and `normalizePlanName()` don't exist in `CORE_Normalize.gs`
- `imo` type wired in switch but no fields mapped to `'imo'` — normalizer exists, never fires
- No garbage-string filter (epoch dates, CMS plan IDs in name fields, `®` symbols)
- No pre-import quality gate — bad data gets in, then we clean it
- Validation APIs exist but are never applied — 17k+ records have never been validated against phone/email/address APIs
- No documentation of what canonical values ARE or what corrections have been made

---

## The 5 Pillars

### Pillar 1: DATA_STANDARDS (What the Rules Are)

**File:** `_RPI_STANDARDS/reference/data/DATA_STANDARDS.md`

Contents:
- **Field Registry** — every field across all MATRIX tabs, its normalizer type, canonical format, and allowed values
- **Canonical Value Lists** — carrier names, product types, product names, plan names, statuses, BoB names (the "blessed" values)
- **Garbage Patterns** — known bad patterns with the correction rule (epoch dates in premium fields, CMS plan IDs in name fields, `®`/trademark symbols, double spaces, trailing underscores)
- **Correction Log** — every FIX_ correction ever made, what it fixed, how many records, date (audit trail for M&A)

### Pillar 2: DATA_POSTURE (Current State of Data Quality)

**File:** `_RPI_STANDARDS/reference/data/DATA_POSTURE.md`

Contents:
- **Tab-level health metrics** — record counts, orphan %, blank field %, distinct carrier/product counts per tab
- **Last normalization sweep** — date + results for each tab
- **Known issues** — remaining problems not yet addressed (CoF blocked on response, etc.)
- **M&A data import log** — source, date, record counts, quality score, issues found

### Pillar 3: DATA_IMMUNE_SYSTEM (Enforcement + Learning Loop)

**Implementation:** New normalizers + quality gate in RAPID_CORE

#### 3A: Add `normalizeProductName()` to CORE_Normalize.gs

New function with `PRODUCT_NAME_ALIASES` map built from ALL corrections made in `FIX_FixProductNames_`:
- Annuity: 24 corrections (VersaChoice, Synergy, ApexAdvantage, Income Pay Pro, etc.)
- Life: 26 corrections (Whole Life, SuperNOVA, EquiFlex, Compass Elite, etc.)
- Combined into one alias map, keyed lowercase → canonical

#### 3B: Add `normalizePlanName()` to CORE_Normalize.gs

New function with `PLAN_NAME_ALIASES` map built from Medicare corrections:
- 97 + 42 = 139 corrections (Heathcare→Healthcare, PLATNIUM→PLATINUM, Aetna paren fixes, Wellcare standardization, AARPMODMEDSUP, truncated LTC names, etc.)
- Plus regex rules for systematic patterns (the "Heathcare" typo affected 59+ records)

#### 3C: Wire into FIELD_NORMALIZERS (CORE_Database.gs)

Add to FIELD_NORMALIZERS:
```
product_name: 'product_name'    → new type, dispatches to normalizeProductName()
plan_name: 'plan_name'          → new type, dispatches to normalizePlanName()
imo_name: 'imo'                 → wire existing normalizeIMOName() (currently unwired)
```

Add cases to `normalizeData_()` switch:
```
case 'product_name': → normalizeProductName(val)
case 'plan_name':    → normalizePlanName(val)
```

#### 3D: Add garbage filters to `normalizeAmount()`

Guard against epoch dates in numeric fields:
- If value is a Date object with year <= 1901 → return '' (clear it)
- If value is a string containing "1899" + "GMT" and is not a valid number → return ''

#### 3E: Import Quality Gate — `assessDataQuality()` in CORE_Database.gs

New function called optionally before bulk imports. Scans an array of records and returns:
```javascript
{
  score: 'A'|'B'|'C'|'D'|'F',
  total: N,
  issues: { missing_required: N, garbage_detected: N, non_canonical: N, orphan_risk: N },
  samples: [...first 20 issues with field + value + suggested fix],
  recommendation: 'PROCEED' | 'REVIEW_FIRST' | 'REJECT'
}
```

This runs BEFORE data hits MATRIX. M&A imports get a quality report card before any records are written.

#### 3F: Validation Layer (External API Enrichment)

**Existing functions in `CORE_Validation_API.gs`** — already built, API keys configured:

| Function | API | What It Does |
|----------|-----|-------------|
| `validatePhoneAPI(phone, type)` | phonevalidator.com | Line type (cell/landline/VoIP), carrier, fake detection |
| `validateEmailAPI(email)` | NeverBounce | Deliverability (valid/invalid/disposable/catchall) |
| `validateAddressAPI(address)` | USPS Addresses v3 | CASS-certified standardization, deliverability |
| `lookupCityStateAPI(zipCode)` | USPS | City/state by ZIP (backfill blanks) |
| `lookupRoutingNumberAPI(routing)` | bankrouting.io | Bank name/location |
| `scoreContactQuality(contact)` | All above | Composite A-F grade |

**When they fire (3 touchpoints):**

1. **Import Quality Gate (Phase C)**: `assessDataQuality()` optionally calls `scoreContactQuality()` on a sample of incoming records to estimate batch quality. Flag: `{ validateContacts: true }`. Cost-controlled — samples 10% or max 50 records.

2. **Post-Import Enrichment Batch**: New `FIX_ValidateContacts_()` function in IMPORT_BoBEnrich.gs. Runs `scoreContactQuality()` on all records missing a `contact_quality_score` field. Writes results back (grade, phone_valid, email_valid, address_standardized). DryRun pattern. Chunked to respect API rate limits (50 records/batch with 2-sec delay).

3. **Periodic Maintenance**: Monthly batch re-validation on records older than 6 months (contact info goes stale — people move, change phones, abandon emails). Updates `contact_quality_score` and `last_validated_date`.

**NOT on every insertRow()** — these are external API calls with per-call costs. They fire as batch operations, not inline.

**New fields needed in TAB_SCHEMAS** (for _CLIENT_MASTER):
- `contact_quality_score` (A-F grade)
- `phone_valid` (valid/invalid/unknown)
- `email_valid` (valid/invalid/disposable/unknown)
- `address_standardized` (true/false)
- `last_validated_date` (YYYY-MM-DD)

#### 3G: Closed Loop

Same pattern as the Security Immune System:
1. Manual FIX_ correction identifies a pattern
2. Document the pattern in DATA_STANDARDS.md (Correction Log)
3. Promote the correction into a RAPID_CORE normalizer (alias map entry)
4. Next import auto-catches the pattern — no re-learning

### Pillar 4: DATA_MONITORING (Watchdogs + Health Checks)

**File:** `_RPI_STANDARDS/reference/data/DATA_MONITORING.md`

#### 4A: `DEBUG_DataHealthCheck()` in IMPORT_BoBEnrich.gs

Monthly diagnostic that runs all quality scans and returns a summary:
- Distinct carrier names per tab (flags any new non-canonical values)
- Distinct product names/plan names (drift detection)
- Orphan account count
- Blank field percentages for key fields
- Records with garbage patterns
- **Contact quality distribution** — % of clients at each grade (A/B/C/D/F), % never validated, % stale (>6 months since last validation)

#### 4B: Scheduled trigger (future)

Monthly time-driven trigger running normalization sweep + health check. Reports results to JDM via Slack DM. (Not in this sprint — document the design, implement when JDM wants it.)

### Pillar 5: DATA_OPERATIONS (Playbooks + Procedures)

**File:** `_RPI_STANDARDS/reference/data/DATA_OPERATIONS.md`

Four playbooks:

1. **M&A Data Ingestion Playbook**
   - Step 1: Receive CRM export (CSV/Excel)
   - Step 2: Run Python preprocessor (field mapping → inline JS)
   - Step 3: Run `assessDataQuality()` with `{ validateContacts: true }` → quality report card + contact validity sample
   - Step 4: If score B or better → import via `FIX_Import*()` with DryRun → review → execute
   - Step 5: If score C or worse → run targeted FIX_ corrections first, then re-score
   - Step 6: Run normalization sweep on imported data
   - Step 7: Run orphan linker
   - Step 8: Run `FIX_ValidateContacts_()` on imported records → phone/email/address validation
   - Step 9: Update DATA_POSTURE.md with import log entry + contact quality metrics

2. **Drive-Based Enrichment Playbook** (future sprint)
   - Use DEX intake pipeline in "enrichment mode"
   - Claude Vision extracts structured data from policy PDFs, statements, applications
   - Matched to existing MATRIX records by policy number, client name, or carrier+product
   - Fills blank fields (effective_date, face_amount, premium, etc.)
   - Both RPI's existing Drive files and M&A partner files

3. **Periodic Maintenance Playbook**
   - Monthly: Run `DEBUG_DataHealthCheck()` → review drift + contact quality distribution
   - Monthly: Run normalization sweep on all 5 tabs (catches Sheets-induced regressions like ZIP zero-pad stripping)
   - Monthly: Run `FIX_ValidateContacts_()` on records missing `contact_quality_score` (new clients since last run)
   - Quarterly: Run full reconciliation (dedup scan + orphan check)
   - Quarterly: Re-validate records with `last_validated_date` > 6 months (contact info goes stale)

4. **Correction → Permanent Rule Playbook**
   - Identify garbage pattern via DEBUG_ function
   - Build FIX_ correction with DryRun
   - Execute correction
   - Add alias entry to RAPID_CORE normalizer
   - Document in DATA_STANDARDS.md Correction Log
   - Deploy RAPID_CORE → pattern is now auto-caught on future imports

---

## Implementation Phases

### Phase A: Promote Corrections into RAPID_CORE Normalizers
**Files:** `CORE_Normalize.gs`, `CORE_Database.gs`

1. Create `normalizeProductName()` with PRODUCT_NAME_ALIASES (50+ entries from FIX_FixProductNames_)
2. Create `normalizePlanName()` with PLAN_NAME_ALIASES (139+ entries from FIX_FixProductNames_)
3. Add `product_name`, `plan_name` to FIELD_NORMALIZERS + switch cases
4. Wire `imo_name: 'imo'` in FIELD_NORMALIZERS (fix the gap)
5. Add epoch date guard to `normalizeAmount()`
6. Deploy RAPID_CORE (clasp push + version + git commit)

### Phase B: Write Data OS Documentation
**Files:** 4 new docs in `_RPI_STANDARDS/reference/data/`

1. `DATA_STANDARDS.md` — Field Registry + Canonical Value Lists + Garbage Patterns + Correction Log
2. `DATA_POSTURE.md` — Current metrics + M&A log template
3. `DATA_MONITORING.md` — Health check design + scheduled trigger spec
4. `DATA_OPERATIONS.md` — 4 playbooks

### Phase C: Build Import Quality Gate
**File:** `CORE_Database.gs`

1. Create `assessDataQuality(records, tabName, options)` function
2. Checks: required fields present, values match canonical lists, garbage pattern detection, client_id validity
3. If `options.validateContacts === true` → sample 10% (max 50) through `scoreContactQuality()` for phone/email/address validation
4. Returns quality score + detailed issue report + contact quality sample
5. Export in CORE_Database namespace

### Phase D: Build Health Check + Contact Validation
**Files:** `IMPORT_BoBEnrich.gs`, `CORE_Database.gs`

1. Create `DEBUG_DataHealthCheck()` — aggregates all quality metrics into single report
2. Distinct value drift detection (compares current distinct values against canonical lists)
3. Contact quality distribution (A/B/C/D/F breakdown, % never validated, % stale)
4. Returns summary suitable for Slack DM formatting
5. Create `FIX_ValidateContacts_()` in IMPORT_BoBEnrich.gs — batch contact validation via `scoreContactQuality()`
   - Processes records missing `contact_quality_score` (never validated)
   - Chunked: 50 records/batch with 2-sec delay between batches (API rate limits)
   - Writes back: `contact_quality_score`, `phone_valid`, `email_valid`, `address_standardized`, `last_validated_date`
   - DryRun variant for preview
6. Add new fields to TAB_SCHEMAS for `_CLIENT_MASTER`: `contact_quality_score`, `phone_valid`, `email_valid`, `address_standardized`, `last_validated_date`

### Phase E: Remaining Data Fixes (Deferred from Prior Plan)
**File:** `IMPORT_BoBEnrich.gs`

1. Run orphan diagnostic (`DEBUG_OrphanDiagnostic` — already exists at line 1370)
2. Execute enhanced orphan linking (`FIX_LinkOrphanAccountsV2` — already exists at line 1421)
3. Import GHL opportunities (`FIX_ImportGHLOpportunities` — already exists at line 1524)
4. Run post-fix normalization sweep
5. Run `FIX_ValidateContacts_()` on all existing client records (first full validation pass)

### Phase F: Drive-Based Enrichment (Future Sprint)
- Design enrichment mode for DEX intake pipeline
- Claude Vision extraction from policy PDFs → structured MATRIX fields
- Not in this implementation — document the design in DATA_OPERATIONS.md only

---

## Execution Order

```
Phase A: Promote corrections into RAPID_CORE normalizers
  → Deploy RAPID_CORE
    ↓
Phase B: Write Data OS documentation (parallel with Phase C)
Phase C: Build import quality gate + wire validation APIs in CORE_Database.gs
  → Deploy RAPID_CORE
    ↓
Phase D: Build health check + contact validation batch in IMPORT_BoBEnrich.gs
  → Push RAPID_IMPORT
    ↓
Phase E: Execute remaining data fixes (orphans + opportunities + first contact validation pass)
  → Run via execute_script with DryRun → JDM approves → Execute
    ↓
Phase F: Drive enrichment (future sprint — document only)
```

---

## Critical Files

| File | Project | Changes |
|------|---------|---------|
| `CORE_Normalize.gs` | RAPID_CORE | New `normalizeProductName()` + `normalizePlanName()` + epoch guard in `normalizeAmount()` |
| `CORE_Database.gs` | RAPID_CORE | Wire `product_name`, `plan_name`, `imo_name` in FIELD_NORMALIZERS + switch. Add `assessDataQuality()` |
| `CORE_Validation_API.gs` | RAPID_CORE | No changes — reuse existing `scoreContactQuality()`, `validatePhoneAPI()`, etc. |
| `IMPORT_BoBEnrich.gs` | RAPID_IMPORT | Add `DEBUG_DataHealthCheck()` + `FIX_ValidateContacts_()` |
| `DATA_STANDARDS.md` | _RPI_STANDARDS | NEW — field registry + canonical values + correction log |
| `DATA_POSTURE.md` | _RPI_STANDARDS | NEW — current metrics + M&A log |
| `DATA_MONITORING.md` | _RPI_STANDARDS | NEW — health check + monitoring design |
| `DATA_OPERATIONS.md` | _RPI_STANDARDS | NEW — 4 operational playbooks |

## Existing Functions to Reuse

| Function | Location | Purpose |
|----------|----------|---------|
| `normalizeData_()` | CORE_Database.gs:1166 | Dispatch loop — add new cases here |
| `FIELD_NORMALIZERS` | CORE_Database.gs:1073 | Field→type mapping — add new fields here |
| `normalizeAmount()` | CORE_Normalize.gs:760 | Add epoch date guard here |
| `FIX_FixProductNames_()` | IMPORT_BoBEnrich.gs:2962 | Source of correction maps to promote |
| `DEBUG_DistinctValues()` | IMPORT_BoBEnrich.gs:1172 | Reuse for drift detection in health check |
| `DEBUG_OrphanDiagnostic()` | IMPORT_BoBEnrich.gs:1370 | Already built, ready to run |
| `FIX_LinkOrphanAccountsV2()` | IMPORT_BoBEnrich.gs:1421 | Already built, ready to run |
| `FIX_ImportGHLOpportunities()` | IMPORT_BoBEnrich.gs:1524 | Already built, ready to run |
| `normalizeExistingData()` | CORE_Reconcile.gs:60 | Retro-normalization sweep |
| `FIX_NormalizeClients/Medicare/Life/Annuity/BDRIA` | IMPORT_BoBEnrich.gs:499-512 | Thin wrappers for normalization sweep |
| `scoreContactQuality()` | CORE_Validation_API.gs | Composite A-F contact quality grade (wraps phone + email + address APIs) |
| `validatePhoneAPI()` | CORE_Validation_API.gs | Phone line type, carrier, fake detection |
| `validateEmailAPI()` | CORE_Validation_API.gs | Email deliverability check |
| `validateAddressAPI()` | CORE_Validation_API.gs | USPS CASS-certified address standardization |

## Verification

1. After Phase A deploy: Run `FIX_NormalizeMedicareDryRun()` — should show 0 changes (corrections already applied; new normalizers should produce same results)
2. After Phase C: Test `assessDataQuality()` against a sample batch of known-bad records (with + without `validateContacts` flag)
3. After Phase D: Run `DEBUG_DataHealthCheck()` — verify it returns comprehensive metrics including contact quality distribution
4. After Phase D: Run `FIX_ValidateContactsDryRun()` on a small batch — verify API calls succeed and results look correct
5. After Phase E: Run `DEBUG_OrphanDiagnostic()` — confirm orphan count reduced
6. After Phase E: Run `FIX_ValidateContacts()` on full client base — first complete contact quality pass
7. Spot-check: `DEBUG_DistinctValues` on carrier_name, product_name, plan_name — all values should be canonical
