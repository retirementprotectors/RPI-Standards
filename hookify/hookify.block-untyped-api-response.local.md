---
name: block-untyped-api-response
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: res\.json\(successResponse\(\{
  - field: path
    operator: regex_match
    pattern: services/api/src/routes/
exclude:
  - pattern: \.test\.(ts|js)
owner: shinob1
---

🛑 **BLOCKED: API response without shared type contract**

You are returning an inline object from `successResponse({...})` in an API route without a shared type from `@tomachina/core`.

**Why this matters:**
- TypeScript cannot check types across HTTP boundaries
- The frontend may expect a different shape than what the API returns (arrays vs counts, different field names)
- This is the exact bug class that caused the ForgeAudit `audit-round` crash (2026-03-20): API returned `{ pending: NUMBER }`, frontend expected `{ pending: ARRAY[] }`

**Canonical pattern:**

```typescript
// In packages/core/src/api-types/sprints.ts
export interface AuditRoundResponse {
  current_round: number
  pending: TrackerItem[]
}

// In services/api/src/routes/sprints.ts
import type { AuditRoundResponse } from '@tomachina/core'
res.json(successResponse<AuditRoundResponse>({ current_round, pending }))

// In packages/ui/src/modules/ForgeAudit.tsx
import type { AuditRoundResponse } from '@tomachina/core'
useState<AuditRoundResponse | null>(null)
```

**Three-layer protection:**
- **Layer 1 (this BLOCK):** prevents inline objects in API routes
- **Layer 2 (TypeScript):** shared DTOs in `@tomachina/core/api-types/` enforce types at compile-time
- **Layer 3 (Valibot):** `fetchValidated` validates response shapes at runtime in the browser

**Override (rare — temporary scaffolding, not for production):**
- WIP route under active development: rename the call site so it doesn't match (e.g. `res.json(successResponse(payload))` where `payload` is a typed variable) — that's actually the correct pattern anyway, since the type lives on the variable.
- The regex specifically matches `successResponse(\{` — passing a typed variable bypasses it cleanly.

**Why BLOCK, not WARN:** the WARN was invisible. The ForgeAudit crash class has shipped before. BLOCK forces shared DTOs or explicit-variable typing.

See: toMachina CLAUDE.md → Code Standards | IMMUNE_SYSTEM.md → Three-Layer Enforcement Model
