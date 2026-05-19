---
name: warn-arch-write-without-adr
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+commit\b
exclude:
  - pattern: git\s+commit\s+.*--allow-empty
  - pattern: git\s+commit\s+.*\[no-adr\]
  - pattern: git\s+commit\s+.*\[no-ticket\]
---

**COMMIT GATE: Architecture files staged — does this decision have an ADR?**

You are committing changes to architecture-significant files. Before this commit lands,
verify that a meaningful architectural decision captured here already has an ADR — or
that one is in flight.

**Architecture-significant path patterns (verify with `git diff --cached --name-only`):**

```
docs/warriors/*/ORCHESTRATION.md     — mesh + fork policy
docs/warriors/*/TAXONOMY.md          — sub-type classification
docs/warriors/*/RESPONSIBILITIES.md  — accountability surface
docs/adr/                            — ADR docs themselves (always OK, skip check)
packages/core/src/**/flow/           — Flow Engine kernel
packages/core/src/**/architecture/   — any explicit architecture layer
services/api/src/routes/             — API contract surface (new routes = arch decision)
dojo-warriors/                       — warrior runtime / boot infrastructure
```

If your staged diff touches any of these paths:

1. **Is there an ADR for this decision?** Check `docs/adr/` — the sequence is global across all warriors.
2. **If yes** — add an ADR reference to your commit message:
   ```
   shinob1(SHINOB1-ARCH-001): restructure ORCHESTRATION mesh roster

   Closes: ADR-0003
   ```
   OR in the PR body:
   ```
   Closes: ADR-0003
   ```
3. **If no ADR exists yet:**
   - For a *new* architectural decision: author `docs/adr/NNNN-short-kebab-title.md` (copy TEMPLATE.md) and land it in the same PR or a preceding one.
   - For an *implementation* of a previously-decided ADR: reference it with `Contributes-to: ADR-NNNN`.
   - For a *trivial edit* (typo, cross-ref update, status bump) that is NOT introducing a new decision: use the escape hatch below.

**ADR reference formats (any of these suppress this warning):**

```
Closes: ADR-NNNN
Contributes-to: ADR-NNNN
Implements: ADR-NNNN
Supersedes: ADR-NNNN
```

The pattern hookify checks for in the commit message: `(Closes|Contributes-to|Implements|Supersedes):\s+ADR-\d{4}`

**Escape hatch — non-decision edits:**

If your commit is a typo fix, formatting pass, cross-ref update, or status bump that
introduces NO new architectural decision, add `[no-adr]` to suppress:

```
shinob1(SHINOB1-ADR-001): fix typo in ADR-0001 context section [no-adr]
```

**Why this gate exists:**

Audit item **3.10** (ADR mechanism). The scaffold exists; the enforcement doesn't — until now.
ADRs capture *why* a decision was made, not just *what* was built. Without a commit-time gate,
the gap between "decision made" and "ADR written" widens silently. The *why* vanishes.

Architectural decisions have compounding blast radius: one decision constrains all future warriors
in that lane. If the reasoning isn't captured at decision time, the next warrior re-litigates
the same trade-offs from scratch — or worse, reverses a decision whose cost they couldn't see.

**Status:** WARN. Upgrades to BLOCK once ADR coverage on existing architecture files reaches ≥80%
(tracked as follow-up audit item). The goal is behavior change, not immediate hard-blocking during
the bootstrapping window.

**Reference:** `docs/adr/README.md` — when to write an ADR, filename convention, template.

See: `toMachina-shinob1/docs/warriors/shinob1/ORCHESTRATION.md` § Mesh — Sub-Warrior Orchestration
(the `SHINOB1-ARCH-REVIEW` sub-type produces ADR drafts as its primary output).
