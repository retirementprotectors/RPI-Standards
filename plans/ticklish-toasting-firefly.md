# Plan: Fix Pipeline Studio — Seed NBX_SECURITIES Full 5-Layer Data

## Context

Pipeline Studio loads 14 pipelines and 7 stages for NBX_SECURITIES, but shows **0 steps / 0 tasks** with 14 console errors. Two root causes identified:

1. **Missing Firestore composite indexes** — The step and task queries require composite indexes that don't exist, causing 500 errors
2. **Seed script never run** — The TypeScript config has all 14 steps + 40 tasks, but they were never written to Firestore

## Root Cause Detail

### Missing Indexes

`firestore.indexes.json` has an index for `flow_stages` (pipeline_key + stage_order) — that's why stages load. But NO indexes exist for:

**Step query** (`flow-admin.ts:489-493`):
```
flow_steps → .where('pipeline_key').where('stage_id').orderBy('step_order')
```
Needs: `(pipeline_key ASC, stage_id ASC, step_order ASC)`

**Task query** (`flow-admin.ts:638-642`):
```
flow_task_templates → .where('pipeline_key').where('stage_id').where('step_id').orderBy('task_order')
```
Needs: `(pipeline_key ASC, stage_id ASC, step_id ASC, task_order ASC)`

### No Seed Data

The seed script (`services/api/src/scripts/seed-pipelines.ts`) exists and the config is complete, but it was never executed. The `flow_steps` and `flow_task_templates` collections are empty.

## Plan (3 Steps)

### Step 1: Add Missing Composite Indexes

**File:** `firestore.indexes.json`

Add 2 new index entries:
```json
{
  "collectionGroup": "flow_steps",
  "queryScope": "COLLECTION",
  "fields": [
    { "fieldPath": "pipeline_key", "order": "ASCENDING" },
    { "fieldPath": "stage_id", "order": "ASCENDING" },
    { "fieldPath": "step_order", "order": "ASCENDING" }
  ]
},
{
  "collectionGroup": "flow_task_templates",
  "queryScope": "COLLECTION",
  "fields": [
    { "fieldPath": "pipeline_key", "order": "ASCENDING" },
    { "fieldPath": "stage_id", "order": "ASCENDING" },
    { "fieldPath": "step_id", "order": "ASCENDING" },
    { "fieldPath": "task_order", "order": "ASCENDING" }
  ]
}
```

Then deploy: `firebase deploy --only firestore:indexes`

**Note:** Index build takes 1-5 minutes. Can seed data in parallel since writes don't need indexes.

### Step 2: Run Seed Script

```bash
cd ~/Projects/toMachina
npx tsx services/api/src/scripts/seed-pipelines.ts --pipeline=NBX_SECURITIES
```

This writes to Firestore:
- 1 pipeline doc (overwrites existing)
- 7 stage docs (overwrites existing)
- 7 workflow docs
- 14 step docs (NEW — currently missing)
- 40 task template docs (NEW — currently missing)

Total: 69 documents

### Step 3: Verify in Pipeline Studio

1. Navigate to `http://localhost:3001/modules/pipeline-studio`
2. Click Edit on NBX - Securities & Advisory
3. Confirm: **7 stages / 14 steps / 40 tasks**
4. Click into Suitability stage — verify 3 steps (Client Profile, Product Suitability, Documentation) with 10 tasks including system checks (FIELD_PRESENT, LNW_LIMIT, BI_UNIQUE)
5. Click into QC Review — verify 4 steps with 11 tasks including CORRECT_CUSTODIAN and FIELD_NOT_CONTAINS checks

## Files Modified

- `firestore.indexes.json` — Add 2 composite indexes
- No code changes needed — the API routes and seed script are correct as-is

## Risk

- Zero risk to production. Indexes are additive (don't affect existing queries). Seed script uses `batch.set()` which overwrites existing docs idempotently.
