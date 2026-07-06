---
name: warn-policy-logic-in-firestore
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: \.(set|update|add)\s*\(
  - field: content
    operator: regex_match
    pattern: (ROADMAP_PERMISSIONS|RoadmapSurfacePolicy|permission_matrix|permissions_matrix|role_permissions|permitted_actions|can_perform|Record<[^>]*Role[^>]*,\s*[^>]*(allow|permission|can_|Action))
owner: shinob1
---

**WARNING: Permission POLICY may be leaking into DATA (Firestore).**

This file both (a) performs a Firestore write (`.set(` / `.update(` / `.add(`) and (b) carries **permission-MATRIX** vocabulary — the shape of a *decision rule*, not a stored value. That's the L2 gate for **The Data/Policy Line** (canonical doctrine in `docs/warriors/shared/toMachina-engineering-doctrine.md`).

**Why this is the escalation hole:**
A permission **matrix / ruleset** stored as a Firestore document is editable from a console — **anyone with console access can grant themselves access or bypass a gate.** POLICY (the gate logic — band enums, the roadmap/RPM permission matrix, the "may this actor do this action" decision function) must live in **code** (`.ts`), PR-gated and immutable at runtime. That is WHY `packages/core/src/auth/roadmap-matrix.ts` is code and stays code.

**The one-question test:** *"If someone edited this row in a Firestore console, could they escalate access or bypass a gate?"*
- **YES ⇒ it's POLICY ⇒ move it to code** (a `.ts` matrix, PR-gated). Don't write it to Firestore.
- **NO** — it's just *what-exists / who's-on* data that policy READS ⇒ it's **DATA ⇒ Firestore is correct.**

**Values vs enforcement (the opt-out — this is DATA, ignore the warning):**
Storing permission *values* is fine and expected in Firestore:
- a catalog/grant row carrying `permitted_bands` **values** as an eligibility ceiling,
- entitlement **booleans**, per-tenant on/off toggles, per-user grants + Assigned-By.

Those are DATA that a code-side matrix *enforces*. This warning targets the **matrix/decision shape** (a `permission_matrix` / `role_permissions` / `can_perform` / `Record<Role, …allow…>`), **not** value fields — if you're writing values, this is a false positive; proceed.

**If POLICY:** move the decision logic into a code matrix (e.g. `packages/core/src/auth/*-matrix.ts`), have Firestore carry only the values it reads. Belt (data in Firestore) + suspenders (policy in code) — never policy-in-a-console.

Doctrine: `docs/warriors/shared/toMachina-engineering-doctrine.md` → "THE DATA/POLICY LINE". L3 backstop: the CI `death-gate` on auth/entitlements/rules PRs.
