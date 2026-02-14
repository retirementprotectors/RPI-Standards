---
name: block-hardcoded-matrix-ids
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: not_contains
    pattern: RAPID_CORE
  - field: content
    operator: regex_match
    pattern: (1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU|1K_DLb-txoI4F1dLrUyoFOuFc0xwsH1iW5eff3pQ_o6E|1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w)
---

**BLOCKED: Hardcoded MATRIX ID Outside RAPID_CORE**

You are hardcoding a MATRIX spreadsheet ID directly in code.

**Detected IDs:**
- `1nnSY-J3n...` = RAPID_MATRIX
- `1K_DLb-tx...` = SENTINEL_MATRIX
- `1byyXMJD...` = PRODASHX_MATRIX

**Why this is blocked:**
- MATRIX IDs should come from RAPID_CORE (single source of truth)
- Hardcoded IDs create maintenance nightmares
- If we ever migrate MATRIXes, hardcoded IDs will break

**Fix:**
```javascript
// WRONG
const MATRIX_ID = '1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w';

// CORRECT
const MATRIX_ID = RAPID_CORE.getMATRIX_ID('PRODASHX');

// Or via Script Properties fallback
const MATRIX_ID = PropertiesService.getScriptProperties().getProperty('PRODASHX_MATRIX_ID');
```

See: `_RPI_STANDARDS/reference/integrations/MATRIX_CONFIG.md`
