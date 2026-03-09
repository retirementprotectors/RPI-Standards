# SPARK Schema Expansion + Enrichment Pass 3

## Context

Q&A module complete — JDM decided on 8 unmapped SPARK fields. 5 need new schema columns on `_ACCOUNT_MEDICARE`, 1 new column on `_CLIENT_MASTER`, 1 existing field repurpose (`policy_number` gets `member_id`), 1 skip (`enrollment_code`).

Data for 6 of 7 target fields already exists in ACCOUNT_DATA from the initial Python converter. Only `agent_writing_number` needs a new Python extraction. `county_fips` comes from enrollment file only (8 FIPS codes).

---

## Step 1: RAPID_CORE Schema Changes

**File:** `~/Projects/RAPID_TOOLS/RAPID_CORE/CORE_Database.gs`

### `_ACCOUNT_MEDICARE` — Add 5 fields after line 540 (enrollment section)

Insert new section between `'prior_plan',` (line 540) and `// === Classification ===` (line 542):

```javascript
// === Application & Termination ===
'submitted_date', 'termination_reason',
'carrier_application_status', 'carrier_sales_type',
'agent_writing_number',
```

### `_CLIENT_MASTER` — Add `county_fips` after `county` on line 310

```javascript
'address', 'address_2', 'city', 'state', 'zip', 'county', 'county_fips', 'country',
```

### `FIELD_NORMALIZERS` — Add `submitted_date` as `'date'` type

Other new fields are codes/text — pass through unchanged.

### Push RAPID_CORE

```bash
cd ~/Projects/RAPID_TOOLS/RAPID_CORE
clasp push --force
# Library — no version/deploy needed, consuming projects use HEAD
```

---

## Step 2: Add Column Headers to PRODASH_MATRIX

Write `SETUP_SparkSchemaColumns()` in `IMPORT_BoBImport.gs`:
- Read existing headers from `_ACCOUNT_MEDICARE` and `_CLIENT_MASTER`
- Append missing column headers (only if not already present)
- 5 new on Medicare: `submitted_date`, `termination_reason`, `carrier_application_status`, `carrier_sales_type`, `agent_writing_number`
- 1 new on Client: `county_fips`

Run via `execute_script`.

---

## Step 3: Generate Enrichment Data

Write `/tmp/spark_enrich3_convert.py` — reads both SPARK CSVs, outputs:
- `/tmp/spark_enrich3_accounts.js` — 486 records keyed by muri with:
  - `sd` = submitted_date
  - `tr` = termination_reason
  - `cas` = carrier_application_status
  - `cst` = carrier_sales_type
  - `awn` = agent_writing_number
  - `mid` = member_id (for policy_number swap)
- `/tmp/spark_enrich3_clients.js` — ~8 records keyed by FIRST|LAST|DOB with:
  - `fp` = county_fips (from enrollment file only)

---

## Step 4: GAS Enrichment Function

**File:** `RAPID_IMPORT/IMPORT_BoBImport.gs`

### `FIX_EnrichSparkAccounts3_(dryRun)`

**Sub-pass A — Account enrichment:**
1. `bobReadSheet_('_ACCOUNT_MEDICARE')`
2. Index SPARK records by `policy_number` (stores muri)
3. Fill blanks: `submitted_date`, `termination_reason`, `carrier_application_status`, `carrier_sales_type`, `agent_writing_number`
4. **Replace** `policy_number` value with `member_id` (when non-empty)
5. `bobWriteEnrichment_`

**Sub-pass B — Client FIPS enrichment:**
1. `bobReadSheet_('_CLIENT_MASTER')`
2. Build name+DOB index (reuse cKey/nKey pattern from initial import)
3. Fill blank `county_fips` for matching clients
4. `bobWriteEnrichment_`

### Existing helpers reused:
- `bobReadSheet_()` — `IMPORT_BoBEnrich.gs`
- `bobWriteEnrichment_()` — `IMPORT_BoBEnrich.gs`
- `bobLogSummary_()` — `IMPORT_BoBEnrich.gs`

---

## Step 5: Push + Execute

```bash
cd ~/Projects/RAPID_TOOLS/RAPID_IMPORT
clasp push --force
```

1. `SETUP_SparkSchemaColumns` — add column headers
2. `FIX_EnrichSparkAccounts3DryRun` — verify counts
3. `FIX_EnrichSparkAccounts3` — live write

---

## Files Modified

| File | Change |
|------|--------|
| `RAPID_CORE/CORE_Database.gs` | +6 schema fields, +1 normalizer |
| `RAPID_IMPORT/IMPORT_BoBImport.gs` | +`SETUP_SparkSchemaColumns`, +`FIX_EnrichSparkAccounts3_` |
| `/tmp/spark_enrich3_convert.py` | New Python script |

---

## Verification

1. DryRun: ~309+ accounts enriched (matching pass 2 SPARK set)
2. Spot-check: `submitted_date`, `termination_reason`, `carrier_application_status` populated
3. `policy_number` now has `member_id` (e.g., `9860919001`) instead of muri hash
4. `county_fips` on ~8 clients from enrollment data
