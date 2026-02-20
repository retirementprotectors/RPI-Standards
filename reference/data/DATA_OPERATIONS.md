# DATA_OPERATIONS — Playbooks & Procedures

> Pillar 5 of the Data Operating System. Step-by-step operational playbooks for data management.

## Playbook 1: M&A Data Ingestion

When RPI acquires a book of business or partners with an agency, their CRM data must be imported into PRODASH_MATRIX. This playbook ensures consistent quality.

### Prerequisites
- CRM export file (CSV or Excel) from the M&A partner
- Field mapping document (which source fields map to which MATRIX fields)
- Book of Business entry created in `_BOB_MASTER` (or will be created during import)

### Steps

**Step 1: Receive & Inventory**
- Get CRM export from partner
- Count total records, identify available fields
- Note: source system (GHL, Salesforce, AgencyBloc, etc.), export format, date range

**Step 2: Field Mapping**
- Map source fields to MATRIX schema fields (use `TAB_SCHEMAS` in CORE_Database.gs as reference)
- Identify unmappable fields (partner-specific data that doesn't fit our schema)
- Document mapping in the import function (e.g., `IMPORT_GHL.gs` pattern)

**Step 3: Quality Assessment**
```javascript
// Run pre-import quality gate
var report = RAPID_CORE.assessDataQuality(records, '_CLIENT_MASTER', {
  validateContacts: true  // Optional: sample 10% through phone/email/address APIs
});
// Returns: { score: 'A'|'B'|'C'|'D'|'F', issues: {...}, recommendation: 'PROCEED'|'REVIEW_FIRST'|'REJECT' }
```

**Step 4: Import Decision**
- Score A or B → Proceed to import with DryRun
- Score C → Run targeted FIX_ corrections first, re-score, then import
- Score D or F → REJECT — data needs significant cleanup at source before import

**Step 5: Import with DryRun**
```javascript
// Preview what will happen
FIX_Import[Source]_({ dryRun: true });
// Review log output, verify record counts, check dedup behavior
```

**Step 6: Execute Import**
```javascript
// JDM approves → execute live
FIX_Import[Source]_({ dryRun: false });
```

**Step 7: Post-Import Normalization**
```javascript
// Run normalization sweep on all imported records
RAPID_CORE.normalizeExistingData('_CLIENT_MASTER', { source: 'M&A import' });
RAPID_CORE.normalizeExistingData('_ACCOUNT_MEDICARE', { source: 'M&A import' });
// ... etc for each tab that received data
```

**Step 8: Orphan Linking**
```javascript
// Link any accounts that couldn't auto-match to clients
FIX_LinkOrphanAccountsV2({ dryRun: true });  // Preview
FIX_LinkOrphanAccountsV2({ dryRun: false }); // Execute (after JDM approval)
```

**Step 9: Contact Validation**
```javascript
// Validate phone/email/address on imported records
FIX_ValidateContacts_({ dryRun: true });   // Preview
FIX_ValidateContacts_({ dryRun: false });  // Execute
```

**Step 10: Update DATA_POSTURE.md**
- Add entry to M&A Data Import Log
- Update tab record counts
- Note any remaining issues

## Playbook 2: Drive-Based Enrichment (Future Sprint)

**Status: Design only — not yet implemented.**

### Concept
Use DEX intake pipeline in "enrichment mode" to extract structured data from policy PDFs, statements, and applications stored in Google Drive. Match extracted data to existing MATRIX records and fill blank fields.

### Data Sources
- RPI's existing Drive files (client folders, policy documents)
- M&A partner files (imported during acquisition)
- Carrier statements and correspondence

### Extraction Targets
| Document Type | Fields to Extract |
|--------------|-------------------|
| Policy PDF | policy_number, effective_date, face_amount, premium, carrier_name, product_name |
| Annual Statement | account_value, surrender_value, death_benefit, as_of_date |
| Application | dob, ssn, address, beneficiaries, health_conditions |
| Carrier Correspondence | status changes, rate actions, rider details |

### Matching Strategy
1. Match by policy_number (highest confidence)
2. Match by client name + carrier + product type
3. Match by client name + effective date range
4. Unmatched → flag for manual review

### Implementation Notes
- Claude Vision API for PDF extraction
- DEX already has intake queue infrastructure
- Add "enrichment mode" flag to DEX watcher
- Results written via RAPID_API (not direct sheet writes)

## Playbook 3: Periodic Maintenance

### Monthly Tasks
1. **Run `DEBUG_DataHealthCheck()`** — review drift detection results, contact quality distribution
2. **Normalization sweep** — `normalizeExistingData()` on all 5 PRODASH_MATRIX tabs
   - Why monthly: Sheets can introduce regressions (ZIP zero-pad stripping, date format changes)
3. **New client validation** — `FIX_ValidateContacts_()` on records missing `contact_quality_score`
4. **Review DATA_POSTURE.md** — update metrics, note any new issues

### Quarterly Tasks
1. **Full reconciliation** — `reconcileClients({ dryRun: true })` + `reconcileAccounts({ dryRun: true })`
2. **Contact re-validation** — `FIX_ValidateContacts_()` on records with `last_validated_date` > 6 months
   - Contact info goes stale: people move, change phones, abandon email addresses
3. **Dedup review** — Check for REVIEW_NEEDED records from dedup queue
4. **Schema audit** — Verify all TAB_SCHEMAS match actual sheet columns

### Annual Tasks
1. **Full data quality audit** — Run all DEBUG_ diagnostics, compile report
2. **Normalizer review** — Check if any canonical values need updating (carrier mergers, product discontinuations)
3. **API key rotation** — Verify all validation API keys are current

## Playbook 4: Correction → Permanent Rule

When a new data quality issue is discovered:

### Step 1: Identify
```javascript
// Use DEBUG functions to find the problem
DEBUG_DistinctValues('_ACCOUNT_ANNUITY', 'product_name');
// Look for non-canonical values in the output
```

### Step 2: Build FIX_ Correction
```javascript
// Create a FIX_ function with DryRun pattern
function FIX_FixNewIssue_(options) {
  var dryRun = options && options.dryRun !== false;
  // ... correction logic
}
function FIX_FixNewIssueDryRun() { return FIX_FixNewIssue_({ dryRun: true }); }
function FIX_FixNewIssue() { return FIX_FixNewIssue_({ dryRun: false }); }
```

### Step 3: Execute Correction
```javascript
// DryRun first → JDM reviews → Execute live
FIX_FixNewIssueDryRun();  // Preview
FIX_FixNewIssue();        // Execute (after approval)
```

### Step 4: Promote to Normalizer
- Add alias entries to the appropriate map in `CORE_Normalize.gs`:
  - `PRODUCT_NAME_ALIASES` for product names
  - `PLAN_NAME_ALIASES` for plan names
  - `CARRIER_ALIASES` for carrier names
  - `STATUS_MAP` for status values
  - `BOB_ALIASES` for book of business names
- Wire new fields into `FIELD_NORMALIZERS` if not already mapped
- Add new cases to `normalizeData_()` switch if needed

### Step 5: Deploy
```bash
# RAPID_CORE 6-step deploy
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - Add [correction] normalizer"
git add -A && git commit -m "vX.X - Add [correction] normalizer"
git push
```

### Step 6: Document
- Add entry to DATA_STANDARDS.md Correction Log
- Update DATA_POSTURE.md if metrics changed

### Step 7: Verify
- The pattern is now auto-caught on all future imports
- Next M&A data import will never contain this issue
- No re-learning required

---

*Part of the Data Operating System. See also: DATA_STANDARDS.md, DATA_POSTURE.md, DATA_MONITORING.md*
