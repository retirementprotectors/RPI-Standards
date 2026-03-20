---
name: block-direct-matrix-write
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: spreadsheets\.values\.(update|append|batchUpdate)
  - field: file_path
    operator: not_contains
    pattern: RAPID_CORE
---

**BLOCKED: Direct MATRIX Write**

Do not write directly to MATRIX spreadsheets outside RAPID_CORE. Use RAPID_CORE write functions or the Bridge service.
