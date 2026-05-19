---
name: warn-missing-structured-response
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: function\s+\w+\s*\([^)]*\)\s*\{[\s\S]*?return\s+(?!.*success)
  - field: file_path
    operator: regex_match
    pattern: \.(gs|ts|js)$
owner: shinob1
---

**WARNING: Missing Structured Response**

Functions should return `{ success: true/false, data/error }` pattern for consistent error handling.

---

**📌 TODO — regex tightening required before BLOCK upgrade** (flagged 2026-05-19, SHINOB1-HOOKIFY-WARN-TO-BLOCK-AUDIT)

This rule was audited alongside 8 others (all upgraded to BLOCK) in the 2026-05-19 WARN→BLOCK bundle. It was deliberately held back because **the current regex is too broad to BLOCK safely**:

```
function\s+\w+\s*\([^)]*\)\s*\{[\s\S]*?return\s+(?!.*success)
```

Fires on ANY function returning a value not containing "success" — including legitimate cases:

- Helper functions returning primitives (numbers, strings, booleans)
- Internal transforms returning arrays, objects, undefined
- Pure utility functions where structured responses are inappropriate
- TypeScript getters / arrow functions / async-without-return

As BLOCK, this would prevent far more legitimate work than it enforces. The right fix is a **regex tightening pass** scoping the rule to specific surfaces:

1. **API handlers only** — functions exported as Express routes (`router.get(...)`, `router.post(...)`)
2. **GAS ForUI handlers** — functions named `forUi*` or registered in a routing manifest
3. **Top-level handlers** — functions matched against an explicit allow-list of "must-return-structured" surfaces

Once the regex is tight enough that BLOCK has zero false positives on the codebase as of audit-date, this rule becomes BLOCK in a follow-up.

**Until then:** stays WARN. See `block-untyped-api-response` for the canonical pattern for API routes (already BLOCK and effective).
