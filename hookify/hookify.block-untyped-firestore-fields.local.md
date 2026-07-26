---
name: block-untyped-firestore-fields
enabled: true
event: PreToolUse
action: block
conditions:
  - field: tool
    operator: equals
    value: Edit
  - field: content
    operator: regex_match
    pattern: \.(set|update|add)\s*\(\s*\{
  # GV2 WS-A conflict #3 (shinob1, 2026-07-08, STAGED — enforcement-changing, HIKARI verify-eye):
  # this rule had NO path scoping, so its blunt `.set/.update/.add({` match fired inside the EXACT
  # server-side paths block-direct-firestore-write deliberately authorizes (services/api/src/, mdj-agent/src/,
  # etc.) — the blunt rule shadowed the careful one. This file_path negative-lookahead MIRRORS
  # block-direct-firestore-write's authorized-path allowlist so the two rules stop contradicting.
  - field: file_path
    operator: regex_match
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

> **STAGED / GV2 WS-A #3 — enforcement-changing, for HIKARI's both-ends verify-eye + MEGAZORD (rule owner) at bless:**
> 1. This adds a `file_path` allowlist so the rule no longer shadows the authorized server-side write
>    paths (`services/api/src/`, `mdj-agent/src/`, …) — mirrors `block-direct-firestore-write`.
> 2. SEPARATE observation for the §2d schema-normalization: this rule declares `event: PreToolUse` +
>    `field: tool` (non-canonical vs the `event: file` / content+file_path majority). Flagged for the
>    consolidation's schema pass — the path-scoping fix here is correct regardless of that normalization.
