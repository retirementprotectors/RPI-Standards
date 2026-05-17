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
