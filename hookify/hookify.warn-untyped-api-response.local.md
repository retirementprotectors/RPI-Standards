---
name: warn-untyped-api-response
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: res\.json\(successResponse\(\{
  - field: path
    operator: regex_match
    pattern: services/api/src/routes/
exclude:
  - pattern: \.test\.(ts|js)
---

**WARNING: API Response Without Shared Type Contract**

You are returning an inline object from `successResponse({...})` in an API route without a shared type from `@tomachina/core`.

**Why this matters:**
- TypeScript cannot check types across HTTP boundaries
- The frontend may expect a different shape than what the API returns (arrays vs counts, different field names)
- This is the exact bug class that caused the ForgeAudit `audit-round` crash (2026-03-20): API returned `{ pending: NUMBER }`, frontend expected `{ pending: ARRAY[] }`

**Required pattern:**
```typescript
// In packages/core/src/api-types/sprints.ts
export interface AuditRoundResponse {
  current_round: number
  pending: TrackerItem[]
  // ...
}

// In services/api/src/routes/sprints.ts
import type { AuditRoundResponse } from '@tomachina/core'
res.json(successResponse<AuditRoundResponse>({...}))

// In packages/ui/src/modules/ForgeAudit.tsx
import type { AuditRoundResponse } from '@tomachina/core'
useState<AuditRoundResponse | null>(null)
```

**Three-layer protection:**
- **Layer 1 (this rule):** Warns when API routes return inline objects without shared DTOs
- **Layer 2 (TypeScript):** Shared DTOs in `@tomachina/core/api-types/` enforce types at compile-time
- **Layer 3 (Valibot):** `fetchValidated` validates response shapes at runtime in the browser — catches mismatches TypeScript can't see across HTTP boundaries

**Before writing any `res.json(successResponse({...}))`:**
- Read the frontend consumer that calls this endpoint
- Verify field names AND types match exactly
- Pay special attention to: arrays vs counts, nested objects vs flat values, field name differences
- Ensure the corresponding Valibot schema in `packages/core/src/schemas/` matches

See: toMachina CLAUDE.md -> Code Standards | IMMUNE_SYSTEM.md -> Three-Layer Enforcement Model
