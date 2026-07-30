---
name: warn-policy-logic-in-firestore
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: \.(?:set|update|add)\s*\(\s*(?:[\w$.\[\]'"]+\s*,\s*)?\{?[^;{}]{0,300}?(?:ROADMAP_PERMISSIONS|RoadmapSurfacePolicy|permission_matrix|permissions_matrix|role_permissions|permitted_actions|can_perform)
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

---

## Why this rule is ONE condition and not two (TRK-HOOK-212a, ronin, 2026-07-30)

This rule used to carry two positive `content` conditions — "a `.set(`/`.update(`/`.add(` call
exists" AND "permission-matrix vocabulary exists" — ANDed across the whole file. That is
**CROSS-CONDITION CONFLATION**: the two conditions are meant to describe **one construct** (a
Firestore write *whose payload is* a permission matrix), but they were evaluated over a string
that let them describe two unrelated things in the same file.

**The axis test that decided it — SYNTACTIC, not LINKAGE.** The distinction matters because the
opposite fix is a regression on a linkage detector (PHI and money gates are compounds whose whole
point is that independent facts CO-OCCUR; narrowing one breaks it). The discriminator used here,
which generalises:

> **If the rule's own prescribed-correct architecture satisfies both conditions, the compound
> cannot be a LINKAGE.** A linkage compound's co-occurrence must be hazardous in *every* instance.

It is not, here, and that was measured rather than argued: `services/api/src/middleware/rbac.ts`
is the exemplar this doctrine points people toward — it *reads* the matrix from code and enforces
in code — and the old rule fired on it. Its two "writes" were `profileCache.set(...)` and
`partnerLevelCache.set(...)`, in-memory `Map`s that touch no database, and its matrix vocabulary
was a **comment** describing the correct pattern. Two unrelated parts of one file, satisfying one
condition each. Under a linkage reading that is a true positive; under the syntactic reading it is
the defect. The correct architecture tripping the gate settles the axis.

**A second, independent defect fixed in the same pass:** the old first condition did not describe
a Firestore write at all. `\.(set|update|add)\s*\(` matches `Map.set`, `Set.add`, and any
`.update(` on any object — 938 of 4198 tracked files in toMachina, 22% of the repo. Requiring the
matrix vocabulary to sit inside the write's own argument list is what makes the call Firestore-
shaped in practice.

`Record<…Role…, …allow|permission|can_|Action…>` was dropped from the vocabulary: it is a
TypeScript **type declaration**, so it cannot appear inside a Firestore write payload, and a
code-side matrix type is the location this doctrine *prescribes*. It could only ever produce a
false positive here.

**WHAT THIS NOW REFUSES THAT IT DID NOT BEFORE: nothing, provably.** Any content matching the new
pattern necessarily contains a `.set|update|add(` call and a vocabulary term, so it satisfied both
old conditions too. The new rule is a strict subset of the old one — asserted over the corpus in
the case file below, not merely asserted here.

**WHAT THIS NOW PERMITS — the declared limits.** Each is asserted as a MISS in
`hookify/warn-policy-logic-in-firestore.cases.py`, so if a future widening starts catching one,
that test fails loudly and sends the reader back to this section instead of letting the change
land silently:

1. **Indirection through a variable** — `const m = { permission_matrix: … }; await ref.set(m);`
   is the real defect and is now missed. A single `regex_match` over `content` cannot follow a
   binding.
2. **A nested object before the vocabulary** — `set({ meta: { … }, permission_matrix: … })`.
   `[^;{}]` stops at the inner brace.
3. **A payload longer than 300 characters** before the vocabulary term.

These are accepted deliberately. This is a `warn` with an L3 backstop (the CI `death-gate` on
auth/entitlements PRs), so the cost of a miss is a warning nobody saw, while the cost of the old
behaviour was a warning on the file that models the correct answer — which is how a gate trains
people to ignore it. Closing (1) needs binding resolution, i.e. an L3 that parses, not an L2
regex; do not attempt it by widening the quantifier here.
