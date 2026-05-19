---
name: block-unvalidated-fetch
enabled: true
event: file
action: block
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
owner: shinob1
---

🛑 **BLOCKED: Raw `fetchWithAuth` import in a UI module — use `fetchValidated`**

All JSON API calls in `packages/ui/` MUST use `fetchValidated` from `./fetchValidated` (or `../fetchValidated`).

**Why:**
- `fetchValidated` validates response shapes at runtime using Valibot schemas (Layer 3 enforcement)
- `fetchWithAuth` returns raw `Response` — caller must manually parse JSON and check `success`, error-prone
- The ForgeAudit crash (2026-03-20) happened because `fetchWithAuth` gave no protection against unexpected response shapes

**Canonical:**
```typescript
import { fetchValidated } from './fetchValidated'
const result = await fetchValidated<MyType[]>('/api/endpoint')
if (result.success) doSomething(result.data)
```

**Override (rare — non-JSON endpoints):**
- HTML, plain-text, binary, or streaming responses are legitimately raw `fetchWithAuth` use
- Add comment on the import line: `import { fetchWithAuth } from './fetchWithAuth' // non-json-exempt: <reason>`
- The block matches the literal import string — a different import style (e.g. importing both from a barrel) won't match.

**Why BLOCK, not WARN:** the WARN was invisible. The 2026-03-20 crash class still happens when raw fetchWithAuth slips through. BLOCK forces validated fetch unless explicitly exempted.

See: IMMUNE_SYSTEM.md → Three-Layer Enforcement Model
