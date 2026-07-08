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
owner: ronin
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

### Required Tabs (the CANONICAL 8 — non-negotiable)

A Discovery Doc MUST include all 8 canonical tab panels, in order. This matches the hard gate
`block-disco-missing-canonical-tabs` (checks for the 8 `id="panel-*"` markers) — authoring to a
smaller set gets the doc HARD-BLOCKED at write time. Reconciled 2026-07-08 (GV2 WS-A conflict #2):
this spec used to require only 4 tabs, which the 8-tab gate rejected.

| # | Tab | `id="panel-*"` | Carries |
|---|-----|----------------|---------|
| 1 | **Pain** | `panel-pain` | Why this exists, the problem, what "done" looks like (the old "Vision") |
| 2 | **Build** | `panel-build` | What gets built — scope, the shape of the solution |
| 3 | **Architecture** | `panel-arch` | How it works; diagrams |
| 4 | **Decisions** | `panel-decisions` | Key calls + trade-offs (the record JDM/warriors sign off on) |
| 5 | **Phases** | `panel-phases` | Sequenced phases / milestones |
| 6 | **Tickets** | `panel-tickets` | **MOST CRITICAL — RONIN seeds from this.** The TRK ticket table (format below) |
| 7 | **Files** | `panel-files` | Files created/modified |
| 8 | **Gates** | `panel-gates` | Acceptance / verification gates — how each ticket proves done |

Start from the canonical template so all 8 panel IDs are present:
`cp docs/templates/discovery-doc-template.html docs/discoveries/<sprint-name>.html`
(format guide: `docs/templates/DISCOVERY_DOC_FORMAT.md`). The FORGE **Tickets** tab uses the exact
TRK table format specified below; RONIN's seeder reads it.

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

The canonical structure is `docs/templates/discovery-doc-template.html` (all 8 panel IDs).
For a worked example, read a recent doc under `docs/discoveries/` in the repo directly
(the `github.io` public URL convention is retired — Pages 404s since the 2026-06-27 lockdown).
Use the canonical dark-theme template, the 8-tab structure, and the TRK table format.

---

### Checklist Before Handing to RONIN

- [ ] `data-cwd` set on `<html>` tag
- [ ] Sprint Plan tab exists with ticket table
- [ ] Every ticket has exact file path
- [ ] Every ticket has acceptance criteria (not just a title)
- [ ] TRK IDs follow `TRK-S[NN]-NNN` format
- [ ] Doc lives at `docs/discoveries/<name>.html` in the repo (NOT a public `github.io` URL — that convention is retired). For `POST /forge/sprint`, pass the repo path / an auth-reachable URL, not `github.io`.
- [ ] Sprint name matches what you'll use in POST /forge/sprint

When ready: `POST /forge/sprint { name: "Sprint Name", discovery_doc: "https://URL" }`
