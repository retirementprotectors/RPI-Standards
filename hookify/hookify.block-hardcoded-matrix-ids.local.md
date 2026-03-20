---
name: block-hardcoded-matrix-ids
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w|1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU|1[a-zA-Z0-9_-]{42,44})
---

**BLOCKED: Hardcoded MATRIX Spreadsheet ID**

Never hardcode MATRIX IDs. Use `RAPID_CORE.getMATRIX_ID()` or environment variables.
