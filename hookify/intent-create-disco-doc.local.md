---
name: intent-create-disco-doc
description: Fires when JDM wants to create a FORGE Discovery Document — injects full spec and template requirements
event: UserPromptSubmit
action: warn
conditions:
  prompt_contains:
    - "#LetsCreateTheDiscoDoc"
    - "#LetsCreateADiscoDoc"
    - "create the disco doc"
    - "write the disco doc"
    - "create a discovery doc"
    - "write a discovery document"
---

## FORGE Discovery Document — Creation Spec

You are creating a FORGE Discovery Document. This is the contract RONIN executes against. Get it right — RONIN can only build what you specify here.

---

### Required HTML Structure

```html
<!DOCTYPE html>
<html lang="en" data-cwd="/path/to/working/directory">
<head>
  <title>Sprint [NUMBER]: [Sprint Name]</title>
</head>
```

**`data-cwd` is mandatory.** It tells RONIN which directory to work in.
- toMachina features: `data-cwd="/home/jdm/Projects/toMachina"`
- mdj-agent changes: `data-cwd="/home/jdm/mdj-agent"`
- GAS maintenance: `data-cwd="/home/jdm/Projects/gas/[project]"`

---

### Required Tabs (in order)

1. **Vision** — Why this sprint exists, what problem it solves, what done looks like
2. **Current State** — What exists today, what's broken, what's missing
3. **Architecture** — How the solution works, diagrams if needed
4. **Sprint Plan** ← **MOST CRITICAL — RONIN seeds from this**

Additional tabs as needed (Auth, Data Model, API Spec, etc.)

---

### Sprint Plan Tab — EXACT FORMAT REQUIRED

RONIN's seeder reads this table. Every row becomes a Firestore tracker item.

```
| TRK | Title | Type | Description / Acceptance Criteria |
|-----|-------|------|-----------------------------------|
| TRK-S[NN]-001 | [Short title] | feat/fix/enhancement/docs/test | [File path] + [What to build] + [How to verify it's done] |
```

**Rules for the ticket table:**
- TRK IDs: `TRK-S[SPRINT_NUMBER]-001` through `TRK-S[SPRINT_NUMBER]-NNN`
- Type: `feat` | `fix` | `enhancement` | `docs` | `test`
- Description MUST include:
  - **File path** — exact file(s) to create or modify
  - **What to build** — specific function/component/change
  - **Acceptance criteria** — how RONIN knows it's done (tsc passes, endpoint returns X, UI shows Y)
- The description is what RONIN's builder agents read — if it's vague, the build will be wrong

**Test it:** Could a junior developer who just joined today execute this ticket correctly with no other context? If yes, it's good. If no, add more detail.

---

### The 9-Stage FORGE Lifecycle (for context)

| Stage | Name | Agent | Status |
|-------|------|-------|--------|
| 000 | Discovery (Write) | JDM + GA | You are here |
| 1 | Discovery (Seed) | Sonnet | RONIN extracts tickets → seeded |
| 2 | Discovery (Audit) | Haiku | Disco ↔ tickets aligned? → disc_audited |
| 3 | Plan (Write) | Opus | Implementation plan → planned |
| 4 | Plan (Audit) | Haiku | Plan ↔ tickets aligned? → plan_audited |
| 5 | Build (Code) | Sonnet | Parallel builders → built |
| 6 | Build (Audit) | Haiku | Build ↔ plan? → audited |
| 7 | Confirm (Deploy) | RONIN | #SendIt → CI → live |
| 8 | Confirm (UX) | JDM/Team | ⭐ ONLY REAL GATE → confirmed |
| 9 | Complete | — | #LandedIt!!! |

---

### Reference Template

The cleanest example to follow: `sprint-005-ronin-autonomy-discovery.html`
Live at: `https://retirementprotectors.github.io/toMachina/sprint-005-ronin-autonomy-discovery.html`

Use the same dark theme CSS, same tab structure, same Sprint Plan table format.

---

### Checklist Before Handing to RONIN

- [ ] `data-cwd` set on `<html>` tag
- [ ] Sprint Plan tab exists with ticket table
- [ ] Every ticket has exact file path
- [ ] Every ticket has acceptance criteria (not just a title)
- [ ] TRK IDs follow `TRK-S[NN]-NNN` format
- [ ] Doc is publicly accessible via URL (GitHub Pages or similar)
- [ ] Sprint name matches what you'll use in POST /forge/sprint

When ready: `POST /forge/sprint { name: "Sprint Name", discovery_doc: "https://URL" }`
