---
id: warn-firestore-collection-assumption
tier: warn
event: PreToolUse
action: warn
tools: [Write, Edit, Bash]
enabled: true
---

# Warn: Firestore Collection Assumption

## What This Catches

Writing to a Firestore collection using a hardcoded string literal without verifying the collection exists first.

The RONIN `forge_runs` vs `mdj_forge_runs` bug was caused by this exact pattern — assuming a collection name from memory instead of verifying via `db.listCollections()`.

## Pattern to Watch For

```typescript
// ❌ TRIGGERS THIS WARN — hardcoded collection name, no prior verification
db.collection('forge_runs')
db.collection('my_collection')
firestore.collection('some_name')
```

## Required Practice

```typescript
// ✅ Verify first, then write
const collections = await db.listCollections();
const names = collections.map(c => c.id);
// Confirm your target collection appears in `names` before proceeding
```

## Warning Message

⚠️ FIRESTORE COLLECTION ASSUMPTION DETECTED

You are writing to a hardcoded Firestore collection name. Before proceeding:
1. Run `db.listCollections()` to get the verified list of existing collections
2. Confirm your target collection is in that list
3. If it is NOT — STOP and ask JDM. Do not silently create a new collection.

Known collections: mdj_forge_runs, sprints, tracker_items, clients, accounts, users, carriers, products, campaigns, templates, content_blocks, communications, opportunities, revenue, flow_pipelines, flow_stages, flow_workflows, flow_instances

Reference: FORGE_STANDARDS.md → "Firestore Collection Verification"
