---
name: warn-unvalidated-fetch
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: from\s+['"]\.\./fetchWithAuth['"]|from\s+['"]\.\/fetchWithAuth['"]
  - field: path
    operator: regex_match
    pattern: packages/ui/src/(modules|components)/
exclude:
  - pattern: fetchValidated\.ts$
  - pattern: \.test\.(ts|js)
---

**WARNING: Raw fetchWithAuth — use fetchValidated instead**

You are importing `fetchWithAuth` directly in a UI module. All JSON API calls in `packages/ui/` should use `fetchValidated` from `./fetchValidated` (or `../fetchValidated`).

**Why this matters:**
- `fetchValidated` validates response shapes at runtime using Valibot schemas (Layer 3 enforcement)
- `fetchWithAuth` returns raw `Response` — caller must manually parse JSON and check `success`, which is error-prone
- The ForgeAudit crash (2026-03-20) happened because `fetchWithAuth` gave no protection against unexpected response shapes

**Required pattern:**
```typescript
// Use fetchValidated (validates envelope + optional schema)
import { fetchValidated } from './fetchValidated'
const result = await fetchValidated<MyType[]>('/api/endpoint')
if (result.success) doSomething(result.data)
```

**Exception:** Non-JSON endpoints (e.g., HTML responses) may use `fetchWithAuth` directly with a comment:
```typescript
import { fetchWithAuth } from './fetchWithAuth' // HTML endpoint — not JSON
```

See: IMMUNE_SYSTEM.md -> Three-Layer Enforcement Model
