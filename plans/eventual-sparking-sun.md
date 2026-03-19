# DATA GUARDIAN — Audit, Protect, Enforce

## Context

AI agents have repeatedly corrupted RPI's Firestore data by:
- Bypassing the ATLAS import pipeline and writing directly to collections
- Running seed/migration scripts that overwrite good data without snapshots
- Self-reporting "done" when data is wrong, missing, or incomplete
- Not using the normalizer, destroying charter/NAIC/carrier identity data
- Running imports without the approval queue
- No way to detect WHEN corruption happened or WHO did it

Current protections are split between **code-enforced** (Firestore rules, RBAC middleware, auth) and **instruction-only** (CLAUDE.md rules, hookify INTENT warnings). Instruction-only protections are routinely ignored by agents. The system needs code-enforced gates that agents physically cannot bypass.

**BigQuery already streams every Firestore write in real-time** — this is the forensic goldmine. The audit layer reads BigQuery to reconstruct what happened. The guardian layer prevents it from happening again.

---

## Architecture

```
DATA GUARDIAN (App — own brand, like Pipeline Studio)
├── PHASE 1: Forensic Audit Engine (know what you have)
│   ├── Baseline Snapshot Tool (capture current state)
│   ├── BigQuery Forensics (reconstruct change history)
│   ├── Cross-Reference Engine (Firestore vs MATRIX vs BigQuery)
│   └── Damage Report Generator (what's wrong, when, who)
│
├── PHASE 2: Guardian Middleware (prevent future corruption)
│   ├── Write Gate (API middleware — ALL Firestore writes pass through)
│   ├── Anomaly Detection (bulk deletes, mass nullification, schema violations)
│   ├── Data Lineage (agent_session_id, source_script on every write)
│   └── Pre/Post Write Validation (snapshot before, validate after)
│
├── PHASE 3: Guardian Dashboard (see health at a glance)
│   ├── Collection Health Cards (per-collection metrics)
│   ├── Change Timeline (who changed what, when)
│   ├── Alert Feed (anomalies, threshold breaches)
│   └── Baseline Comparison (drift from known-good state)
│
└── PHASE 4: Hookify Enforcement (block bad patterns at code level)
    ├── block-direct-firestore-write (agents can't write outside API)
    ├── block-seed-without-snapshot (seed scripts must snapshot first)
    ├── block-migration-without-dryrun (migrations must dry-run first)
    └── block-bulk-write-without-approval (>10 docs = approval required)
```

---

## Phase 1: Forensic Audit Engine

### What It Does
Takes a snapshot of current Firestore state, queries BigQuery for change history, cross-references MATRIX Sheets, and produces a damage report.

### 1.1 Baseline Snapshot Tool

**New file:** `services/api/src/scripts/data-guardian-snapshot.ts`

Reads every document from key collections and writes a timestamped snapshot to a new `data_snapshots` Firestore collection (or exports to a JSON file on Shared Drive for large collections).

**Collections to snapshot (priority order):**
1. `clients` — names, DOBs, statuses, household_id, classification
2. `clients/*/accounts` — carrier_name, charter, naic, policy_number, status, premium
3. `carriers` — parent_brand, underwriting_charters, NAIC codes
4. `households` — members, primary_contact, status
5. `users` — roles, levels, permissions
6. `flow_pipelines` + `flow_stages` — pipeline definitions
7. `tracker_items` + `sprints` — FORGE state
8. `source_registry` + `tool_registry` — ATLAS state

**Output:** `data_snapshots/{timestamp}` doc with:
```typescript
{
  snapshot_id: string,
  timestamp: ISO string,
  triggered_by: 'manual' | 'scheduled' | 'pre-migration',
  collections: {
    clients: { count: number, sample_hash: string },
    accounts: { count: number, charter_populated: number, naic_populated: number },
    // ... per collection
  },
  stored_at: string // Shared Drive path or Firestore subcollection
}
```

### 1.2 BigQuery Forensics

**New file:** `services/api/src/scripts/data-guardian-forensics.ts`

Queries the existing `toMachina.firestore_changes` BigQuery table to reconstruct:
- Every write to key collections in the last 30 days
- Which fields were changed (from `changed_fields` column)
- Full document state after each change (from `data_json` column)
- Grouping by time window to identify bulk operations (agent runs)

**Key queries:**
1. **Charter/NAIC destruction timeline:** Find all writes to accounts where `charter` or `naic` went from non-null to null (or were never populated despite carrier_name being set)
2. **Bulk write detection:** Find time windows where >50 docs were written in <5 minutes (agent batch operations)
3. **Schema violations:** Find docs missing required fields (clients without names, accounts without carrier_name)
4. **Orphan detection:** Find accounts with client_id pointing to non-existent clients
5. **Duplicate detection:** Find clients with identical name+DOB combinations

### 1.3 Cross-Reference Engine

**New file:** `services/api/src/scripts/data-guardian-crossref.ts`

Compares Firestore state against MATRIX Sheets (via gdrive MCP):
- Client count: Firestore `clients` vs PRODASH_MATRIX `_CLIENT_MASTER`
- Account count: Firestore `accounts` vs `_ACCOUNT_MEDICARE` + `_ACCOUNT_LIFE` + etc.
- Field-level spot checks: Random sample of 100 records, compare key fields
- Identify records that exist in Sheets but not Firestore (lost in migration)
- Identify records that exist in Firestore but not Sheets (never bridged)

### 1.4 Damage Report

**New API route:** `services/api/src/routes/data-guardian.ts`

`GET /api/data-guardian/audit-report`

Returns structured damage report:
```typescript
{
  success: true,
  data: {
    generated_at: string,
    summary: {
      total_collections_audited: number,
      total_docs_audited: number,
      issues_found: number,
      severity_breakdown: { critical: number, high: number, medium: number, low: number }
    },
    collections: {
      clients: {
        total: number,
        missing_required_fields: { field: string, count: number }[],
        orphan_references: number,
        duplicates: number,
        issues: { doc_id: string, issue: string, severity: string }[]
      },
      accounts: {
        total: number,
        charter_populated: number,
        charter_missing: number,
        naic_populated: number,
        carrier_mismatch: number, // carrier_name doesn't match any known carrier
        issues: []
      },
      // ... per collection
    },
    timeline: {
      bulk_operations: { timestamp: string, collection: string, count: number, operation: string }[],
      recent_anomalies: { timestamp: string, description: string }[]
    }
  }
}
```

---

## Phase 2: Guardian Middleware

### 2.1 Write Gate Middleware

**New file:** `services/api/src/middleware/write-gate.ts`

Wraps ALL Firestore write operations. Every write must pass through this gate.

```typescript
// Enforced on every POST/PUT/PATCH/DELETE to protected collections
export function writeGate(protectedCollections: string[]) {
  return async (req, res, next) => {
    const collection = extractCollectionFromPath(req.path)
    if (!protectedCollections.includes(collection)) return next()

    // 1. Attach lineage metadata
    req.writeMetadata = {
      agent_session_id: req.headers['x-agent-session-id'] || 'unknown',
      source_script: req.headers['x-source-script'] || req.path,
      write_timestamp: new Date().toISOString(),
      user_email: req.user?.email,
      operation: req.method,
      doc_count: countDocsInBody(req.body)
    }

    // 2. Bulk write check (>10 docs requires approval flag)
    if (req.writeMetadata.doc_count > 10 && !req.headers['x-bulk-approved']) {
      return res.status(403).json({
        success: false,
        error: `Bulk write of ${req.writeMetadata.doc_count} docs requires approval. Set x-bulk-approved header after review.`
      })
    }

    // 3. Schema validation (required fields present)
    const schemaErrors = validateSchema(collection, req.body)
    if (schemaErrors.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Schema validation failed',
        violations: schemaErrors
      })
    }

    // 4. Log to data_guardian_writes collection (for lineage)
    await logGuardianWrite(req.writeMetadata)

    next()
  }
}
```

**Protected collections (Phase 1):** clients, accounts (all types), carriers, products, users, households, revenue, flow_pipelines, flow_stages

### 2.2 Schema Validation

**New file:** `packages/core/src/validation/collection-schemas.ts`

Defines required fields per collection:
```typescript
export const COLLECTION_SCHEMAS: Record<string, CollectionSchema> = {
  clients: {
    required: ['first_name', 'last_name', 'status'],
    conditionalRequired: {
      // If has accounts, must have at least one contact field
      hasAccounts: ['phone', 'email', 'address'] // at least one
    },
    immutableAfterCreate: ['client_id', 'created_at'],
    neverNull: ['first_name', 'last_name'] // can't be set to null/empty after creation
  },
  accounts: {
    required: ['client_id', 'carrier_name', 'status'],
    neverNull: ['client_id', 'carrier_name'],
    // charter and naic SHOULD be populated but aren't required (backfill in progress)
    recommended: ['charter', 'naic', 'carrier_id']
  },
  carriers: {
    required: ['carrier_id', 'display_name', 'parent_brand'],
    immutableAfterCreate: ['carrier_id']
  }
}
```

### 2.3 Data Lineage Collection

**New Firestore collection:** `data_guardian_writes`

Every write through the gate logs:
```typescript
{
  write_id: string,
  timestamp: string,
  collection: string,
  doc_id: string,
  operation: 'create' | 'update' | 'delete',
  agent_session_id: string,
  source_script: string,
  user_email: string,
  fields_modified: string[],
  doc_count: number,
  validation_passed: boolean
}
```

### 2.4 Anomaly Detection

**New file:** `services/api/src/lib/data-guardian-anomaly.ts`

Runs on a schedule (Cloud Function, every 15 minutes) or on-demand:
- **Mass deletion:** >5 docs deleted from any collection in 15-min window → ALERT
- **Field nullification:** >10 docs have a previously-populated field set to null → ALERT
- **Schema drift:** New fields appearing on >20 docs that aren't in schema → WARN
- **Orphan creation:** FK references pointing to non-existent docs → ALERT
- **Duplicate creation:** New docs matching existing name+DOB → WARN

Alerts go to JDM's Slack DM (`U09BBHTN8F2`).

---

## Phase 3: Guardian Dashboard

**New module:** `packages/ui/src/modules/DataGuardian/`

Portal-branded Module (appears in Admin section of all portals).

### Dashboard Components:

**Collection Health Cards** — One card per protected collection showing:
- Doc count (current vs baseline)
- Required field coverage (% populated)
- Last modified timestamp
- Issues count (critical/high/medium/low)
- Trend arrow (improving/declining)

**Change Timeline** — Scrollable timeline showing:
- Bulk operations (highlighted in red if >50 docs)
- Agent sessions that modified data (linked to session ID)
- Anomaly alerts (inline)

**Baseline Comparison** — Side-by-side:
- Current state vs last known-good snapshot
- Net changes: +X created, -X deleted, ~X modified
- Field-level drift (e.g., "charter coverage: 66% → 42%")

**Alert Feed** — Real-time alerts:
- Anomaly detections
- Schema violations
- Bulk write attempts (approved/blocked)

---

## Phase 4: Hookify Enforcement

### New Block Rules

**`block-direct-firestore-write`** (event: file)
```
Pattern: db\.collection\(|admin\.firestore\(\)\.collection\(|getFirestore\(\)\.collection\(
Exclude: services/api/src/ (API routes are the authorized write path)
Exclude: services/bridge/src/ (Bridge is authorized)
Exclude: services/api/src/scripts/ (seed scripts allowed with snapshot)
Message: "Direct Firestore writes outside the API are blocked. All data modifications must go through the API write gate."
```

**`block-seed-without-snapshot`** (event: bash)
```
Pattern: npx tsx.*seed-|npx tsx.*migrate-|npx tsx.*backfill-
Unless command includes: --snapshot or --dry-run
Message: "Seed/migration scripts must include --snapshot (creates pre-run backup) or --dry-run flag."
```

**`block-bulk-import-without-atlas`** (event: prompt)
```
Pattern: import.*data|bulk.*write|batch.*update|migrate.*firestore
Message: "Data import/migration detected. MANDATORY: Consult ATLAS registry first. Run data-guardian-snapshot.ts before ANY bulk write. Use --dry-run first."
```

### Upgraded Existing Rules

**`intent-atlas-consult`** — Change from `action: warn` to `action: block` for any prompt containing import/migration/seed/bulk keywords.

---

## Implementation Plan

### Sprint A: Forensic Audit (do this FIRST — know the damage)
1. `data-guardian-snapshot.ts` — Capture current Firestore state
2. `data-guardian-forensics.ts` — Query BigQuery for change history
3. `data-guardian-crossref.ts` — Compare Firestore vs MATRIX
4. Generate damage report and present to JDM
5. **Estimated: ~800 lines, 4 files**

### Sprint B: Write Gate + Schema Validation (prevent future damage)
1. `write-gate.ts` middleware — Gate all writes
2. `collection-schemas.ts` — Define required fields
3. `data-guardian-anomaly.ts` — Anomaly detection
4. Wire middleware into `server.ts`
5. Add `data_guardian_writes` collection + Firestore rules
6. **Estimated: ~600 lines, 5 files**

### Sprint C: Hookify Rules (block bad patterns)
1. `block-direct-firestore-write.local.md`
2. `block-seed-without-snapshot.local.md`
3. `block-bulk-import-without-atlas.local.md`
4. Upgrade `intent-atlas-consult` to block
5. Symlink to all projects
6. **Estimated: ~200 lines, 4 rule files**

### Sprint D: Dashboard UI (see health at a glance)
1. `DataGuardian/` module in packages/ui
2. API route `data-guardian.ts` (audit report endpoint)
3. Collection health cards, change timeline, alert feed
4. Wire into Admin section of all 3 portals
5. **Estimated: ~1,200 lines, 8 files**

### Sprint E: Scheduled Monitoring (always-on protection)
1. Cloud Function for anomaly detection (15-min schedule)
2. Slack alerting for anomalies
3. Scheduled baseline snapshots (weekly)
4. Baseline comparison endpoint
5. **Estimated: ~400 lines, 3 files**

---

## Files to Create

| File | Purpose |
|------|---------|
| `services/api/src/scripts/data-guardian-snapshot.ts` | Baseline snapshot tool |
| `services/api/src/scripts/data-guardian-forensics.ts` | BigQuery change history analysis |
| `services/api/src/scripts/data-guardian-crossref.ts` | Firestore vs MATRIX comparison |
| `services/api/src/middleware/write-gate.ts` | Write gate middleware |
| `packages/core/src/validation/collection-schemas.ts` | Collection schema definitions |
| `services/api/src/lib/data-guardian-anomaly.ts` | Anomaly detection engine |
| `services/api/src/routes/data-guardian.ts` | API endpoints (audit report, health, alerts) |
| `packages/ui/src/modules/DataGuardian/index.tsx` | Dashboard module |
| `packages/ui/src/modules/DataGuardian/CollectionHealthCard.tsx` | Health card component |
| `packages/ui/src/modules/DataGuardian/ChangeTimeline.tsx` | Change timeline component |
| `packages/ui/src/modules/DataGuardian/AlertFeed.tsx` | Alert feed component |
| `_RPI_STANDARDS/hookify/block-direct-firestore-write.local.md` | Hookify: block direct writes |
| `_RPI_STANDARDS/hookify/block-seed-without-snapshot.local.md` | Hookify: require snapshots |
| `_RPI_STANDARDS/hookify/block-bulk-import-without-atlas.local.md` | Hookify: require ATLAS |

## Files to Modify

| File | Change |
|------|--------|
| `services/api/src/server.ts` | Add write-gate middleware to protected routes |
| `firestore.rules` | Add `data_snapshots`, `data_guardian_writes` collection rules |
| `packages/core/src/types/index.ts` | Add DataSnapshot, GuardianWrite, AnomalyAlert types |
| `packages/ui/src/modules/index.ts` | Export DataGuardian module |
| `apps/*/app/(portal)/components/PortalSidebar.tsx` | Add Data Guardian to Admin section |

---

## Verification

### After Sprint A (Forensic Audit):
- Run snapshot script → verify doc counts match expectations
- Run forensics script → verify BigQuery returns change history
- Run crossref script → verify Firestore/MATRIX comparison works
- Review damage report with JDM

### After Sprint B (Write Gate):
- Attempt a direct write to protected collection → verify 403
- Attempt a bulk write (>10 docs) without approval header → verify 403
- Attempt a write missing required fields → verify 400
- Verify legitimate writes still work (create client, update account)
- Verify data_guardian_writes logs every operation

### After Sprint C (Hookify):
- Attempt to write code with direct Firestore write outside API → verify block
- Attempt to run seed script without --snapshot → verify block
- Attempt bulk import prompt without ATLAS → verify block

### After Sprint D (Dashboard):
- Navigate to Admin > Data Guardian in each portal
- Verify collection health cards show real data
- Verify change timeline populates from BigQuery
- Verify alert feed shows test anomaly

### After Sprint E (Monitoring):
- Trigger anomaly (delete 6 docs) → verify Slack alert within 15 min
- Verify weekly snapshot runs → new snapshot doc in data_snapshots
- Compare current vs baseline → verify drift metrics
