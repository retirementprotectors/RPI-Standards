---
name: block-untyped-firestore-fields
enabled: true
# REVIVAL (megazord, §2d normalization, 2026-07-08 — HELD FOR JDM BLESS, TIER 2 / arms a blocker):
# event PreToolUse→file. The engine computes event from tool_name (Edit/Write/MultiEdit→file) and
# config_loader skips any rule whose event≠'all'≠computed — so 'PreToolUse' never matched and this
# rule was DEAD since authored (phantom-field writes uncaught everywhere). Flip to event:file arms
# it. Mirrors the proven live sibling block-direct-firestore-write: NO `tool` condition (event:file
# already scopes to Edit/Write/MultiEdit; the old `tool: equals Edit` also wrongly dropped Write).
# NOT live until bless-merge to main + setup-hookify-symlinks.sh (atomic flip).
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    # Object-literal Firestore write: .set({ / .update({ / .add({. The \{ keeps it write-shaped
    # (does NOT match Map.set(k,v)/Set.add(x)/setState) — verified 0 non-Firestore hits in packages/ui.
    pattern: \.(set|update|add)\s*\(\s*\{
  - field: file_path
    operator: regex_match
    # FULL sibling allowlist (mirrors block-direct-firestore-write EXACTLY — the two Firestore rules
    # must share one exemption surface so they never shadow/contradict). Exempts the legit direct-write
    # server layer + the Firebase-web-SDK prototype lanes (docs/*.html, inbox/*.html) + test/spec/md.
    # COVERAGE NOTE (megazord re-decision 2026-07-08): this exempts services/api/src, where some raw
    # untyped .set({...}) scripts (backfill-geo/whitepages/seed-domain) live — accepted deliberately:
    # block-untyped is a REMINDER guard, not a type-checker; the DURABLE field-schema fix for server
    # scripts is a typed Firestore client (packages/db converter), tracked separately, not this regex.
    pattern: ^(?!.*(services/api/src/|services/bridge/src/|services/intake/|services/bigquery-stream/|services/learning-loop/|mdj-agent/src/|services/approval-signer/|docs/.*\.html|inbox/.*\.html|\.(test|spec)\.(ts|js)|\.(md|txt)$)).*
owner: megazord
---

**BLOCKED: Firestore Write — Verify Fields Against Schema**

You are writing code that sets or updates Firestore document fields.

**BEFORE YOU PROCEED, YOU MUST:**

1. **READ the TypeScript interface** for the collection you're writing to
   - Clients: `packages/core/src/types/index.ts` → `Client` interface
   - Accounts: `packages/core/src/types/index.ts` → `Account` interface
   - All types: grep the `packages/core/src/types/` directory

2. **VERIFY every field name** in your `.set()`, `.update()`, or `.add()` call exists in that interface

3. **If a field doesn't exist in the type:**
   - STOP. You cannot invent fields.
   - Search for the CORRECT field name. There is probably one that does what you need.
   - Example: "poa_name" is NOT a field. But "estate_contact_name" or "beneficiary_name" might be.
   - If genuinely no field exists: ask JDM or MEGAZORD to add it to the schema FIRST.

4. **If all fields match the type:** Proceed. You're good.

**Why this exists:**
Warriors were inventing custom fields (poa_name, estate_planning_status, etc.) that don't exist in the schema. These phantom fields sit in Firestore invisibly, pollute the data, confuse other warriors who read the records, and are nearly impossible to find after the fact.

**The rule: You cannot write a field that doesn't exist in the TypeScript type. Find the right field. If it doesn't exist, escalate — don't invent.**

MEGAZORD owns the data schema. MEGAZORD IS ATLAS.
