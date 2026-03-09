---
name: block-direct-matrix-write
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (FIX_|IMPORT_).*\.(gs|js)$
  - field: file_path
    operator: not_contains
    pattern: RAPID_CORE
  - field: file_path
    operator: not_contains
    pattern: RAPID_API
  - field: content
    operator: regex_match
    pattern: (sheet|tab|sh)\s*\.\s*getRange\s*\([^)]*\)\s*\.\s*setValues\s*\(|(sheet|tab|sh)\s*\.\s*appendRow\s*\(
---

**BLOCKED: Direct MATRIX Write in Import/Fix Function**

You are writing directly to a MATRIX sheet using `setValues()` or `appendRow()` inside a FIX_ or IMPORT_ function.

**Why this is blocked:**
- RAPID_API / RAPID_CORE.insertRow() is the single source of truth for ALL MATRIX writes
- Direct writes bypass: normalization (carrier names, NAIC codes, parent carriers), dedup checks, validation hooks, and audit trail logging
- This exact pattern caused 5,016 duplicate Medicare records in February 2026 and required retroactive normalization of 12,232+ records across 4 account tabs in March 2026

**What was missed both times:**
- NAIC code auto-population (carrier_name → _CARRIER_MASTER lookup)
- Parent carrier derivation
- Status field normalization
- Audit trail (who/when/what)

**Fix — use RAPID_CORE bulk operations:**
```javascript
// WRONG — direct sheet write
var rows = buildRows(data);
sheet.getRange(startRow, 1, rows.length, headers.length).setValues(rows);

// CORRECT — route through RAPID_CORE
for (var i = 0; i < records.length; i++) {
  RAPID_CORE.insertRow(tabName, records[i]);
}

// CORRECT — bulk with dedup
var result = RAPID_CORE.bulkInsert(tabName, records, { dedup: true });
```

**If you MUST bypass for performance (500+ records):**
1. Get explicit approval from JDM first
2. Add a comment: `// BYPASS: Direct write approved by JDM [date] — reason`
3. IMMEDIATELY run `FIX_Normalize[Tab]()` after the import to backfill normalization
4. Run `FIX_AutoMergeAccounts()` to catch duplicates

**The pipeline exists for a reason. Use it.**
