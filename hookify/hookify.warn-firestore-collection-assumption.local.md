---
name: warn-firestore-collection-assumption
enabled: false
event: PreToolUse
action: warn
owner: megazord
# RETIRED 2026-07-08 (megazord · §2d dormant-cluster sweep · JDM + SHINOB1 + HIKARI call).
# Kept as a DORMANT DOCUMENTED REFERENCE (enabled:false), NOT deleted — deleting would lose the
# concept + the known-collections seed below. Renamed to the hookify.* prefix so it shows honestly
# on the rulebook surface as retired/dormant rather than vanishing.
#
# WHY RETIRED, NOT REVIVED (it was never a functioning rule):
#   1. FILENAME lacked the `hookify.` prefix → the engine globs `.claude/hookify.*.local.md`
#      (config_loader.py) → it was NEVER loaded, regardless of event.
#   2. NO MATCHER — the frontmatter carries no `pattern`/`conditions`; the "Pattern to Watch For"
#      lives in the body as prose, so even if loaded it could match nothing.
#   3. Non-canonical fields the engine ignores: `id` (engine reads `name`), `tier` (reads `action`),
#      `tools:[...]` (reads `tool_matcher`) — plus the dead `event: PreToolUse` value.
#   4. The concept resists a clean matcher: `db.collection('literal')` fires on EVERY legit access
#      = warn-spam, and a regex cannot tell whether the name was verified first (the actual intent).
#      Arming a stub into a noise generator is the opposite of the immune system's job.
#
# THE REAL VERSION of this idea = a from-scratch, ATLAS-registry-backed rule that flags only NEW
# collection literals absent from a known-collections registry (seeded by the list below). That is a
# design task on MEGAZORD's ATLAS lane, tracked SEPARATELY from this sweep — not a §2d event flip.
---

> **RETIRED — dormant documented reference (enabled:false).** This is not an active rule. See the
> banner above for why it was retired rather than revived, and the ATLAS-registry-backed successor.

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
