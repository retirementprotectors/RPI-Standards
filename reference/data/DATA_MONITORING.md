# DATA_MONITORING — Watchdogs & Health Checks

> Pillar 4 of the Data Operating System. Defines how we detect data quality drift and maintain visibility.

## DEBUG_DataHealthCheck()

**Location:** `RAPID_IMPORT/IMPORT_BoBEnrich.gs`
**Purpose:** Monthly diagnostic that aggregates all quality metrics into a single report.

### What It Checks

1. **Distinct Value Drift** — Compares current distinct values for key fields (carrier_name, product_name, plan_name, product_type, status) against canonical lists in RAPID_CORE normalizer maps. Any value NOT in the canonical list = drift.

2. **Orphan Accounts** — Accounts with no matching client_id in _CLIENT_MASTER. Uses DEBUG_OrphanDiagnostic logic.

3. **Blank Field Analysis** — Percentage of blank/null values for critical fields per tab:
   - _CLIENT_MASTER: email, phone, dob, address, state, zip
   - _ACCOUNT_MEDICARE: carrier_name, plan_name, effective_date
   - _ACCOUNT_LIFE: carrier_name, product_name, face_amount
   - _ACCOUNT_ANNUITY: carrier_name, product_name, account_value
   - _ACCOUNT_BDRIA: carrier_name, product_name, market_value

4. **Garbage Pattern Detection** — Scans for known garbage patterns:
   - Epoch dates in amount fields (1899/1900 patterns)
   - CMS plan IDs in name fields (H1234-567 patterns)
   - Trademark symbols (®) in product/plan names
   - Truncated strings (ending mid-word)

5. **Contact Quality Distribution** — For _CLIENT_MASTER records with contact_quality_score:
   - Grade distribution (A/B/C/D/F counts and percentages)
   - % never validated (no contact_quality_score)
   - % stale (last_validated_date > 6 months ago)

6. **Record Counts** — Total records per tab, growth since last check.

### Output Format

Returns a structured object suitable for Slack DM formatting:
```javascript
{
  success: true,
  data: {
    timestamp: '2026-02-20T12:00:00Z',
    tabs: {
      _CLIENT_MASTER: { count: N, blanks: {...}, drift: [...] },
      _ACCOUNT_MEDICARE: { count: N, blanks: {...}, drift: [...] },
      // ... etc
    },
    orphans: { total: N, by_tab: {...} },
    garbage: { total: N, samples: [...] },
    contact_quality: { A: N, B: N, C: N, D: N, F: N, never_validated: N, stale: N },
    overall_score: 'B',
    recommendation: 'Run normalization sweep on _ACCOUNT_MEDICARE (3 non-canonical carrier names detected)'
  }
}
```

## Scheduled Trigger (Future)

**Not yet implemented — design documented here for future activation.**

### Monthly Health Check Trigger
- **When:** 1st of each month, 6:00 AM CT
- **Function:** `TRIGGER_MonthlyHealthCheck()` in RAPID_IMPORT
- **Actions:**
  1. Run `DEBUG_DataHealthCheck()`
  2. Run `normalizeExistingData()` on all 5 PRODASH_MATRIX tabs (catches Sheets-induced regressions)
  3. Format results as Slack message
  4. Send to JDM's DM (`U09BBHTN8F2`) via Slack API
- **Setup:** Time-driven trigger in RAPID_IMPORT GAS editor (requires editor auth — JDM one-time setup)

### Quarterly Full Reconciliation Trigger
- **When:** 1st of Jan/Apr/Jul/Oct, 6:00 AM CT
- **Function:** `TRIGGER_QuarterlyReconciliation()` in RAPID_IMPORT
- **Actions:**
  1. Run monthly health check (above)
  2. Run `reconcileClients({ dryRun: true })` — find new duplicate pairs
  3. Run `reconcileAccounts({ dryRun: true })` — find orphans + dup policies
  4. Run `FIX_ValidateContacts_({ dryRun: true })` on records with last_validated_date > 6 months
  5. Report findings to JDM via Slack DM
  6. Actual merges/fixes require JDM approval (DryRun only)

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Non-canonical carrier names | >5 new values | >20 new values |
| Non-canonical product names | >10 new values | >50 new values |
| Orphan accounts | >50 | >200 |
| Blank email % (_CLIENT_MASTER) | >15% | >30% |
| Blank phone % (_CLIENT_MASTER) | >10% | >25% |
| Contact quality: % grade D/F | >20% | >40% |
| Contact quality: % never validated | >50% | >80% |

## Drift Detection

When `DEBUG_DataHealthCheck()` finds values NOT in canonical lists, it means either:
1. **New legitimate value** — Add to normalizer alias map in RAPID_CORE, deploy
2. **Typo/garbage** — Build FIX_ correction, execute, then add to alias map
3. **Import regression** — Re-run normalization sweep on affected tab

The correction flow follows the Closed Loop described in DATA_STANDARDS.md.

---

*Part of the Data Operating System. See also: DATA_STANDARDS.md, DATA_POSTURE.md, DATA_OPERATIONS.md*
