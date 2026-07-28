---
name: block-blanket-rpi-on-phi-surface
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (?:permitted_tenancy:\s*\[(?:\s*\.\.\.(?:RPI_ONLY|PARTNER)\s*|\s*(?:'(?:rpi|partner_agent|partner_admin|superadmin)'\s*,?\s*)+)\][^\n]*is_phi:\s*true)|(?:is_phi:\s*true[^\n]*permitted_tenancy:\s*\[(?:\s*\.\.\.(?:RPI_ONLY|PARTNER)\s*|\s*(?:'(?:rpi|partner_agent|partner_admin|superadmin)'\s*,?\s*)+)\])
  - field: file_path
    operator: regex_match
    pattern: registry/app-registry-def\.ts$
owner: hikari-mwm-dipset
---

🛑 **BLOCKED: a PHI-bearing registry row is gated only by GENERIC role rails.**

This write sets `is_phi: true` on an `app_registry` row whose `permitted_tenancy` contains
only generic rails (`rpi`, `partner_agent`, `partner_admin`, `superadmin`, or the
`[...RPI_ONLY]` / `[...PARTNER]` spreads). **That is not an entity gate.**

**Why it is blocked (G-L3C):**
Generic rails say what ROLE an actor holds. They never say WHICH partner's book that actor
may see. A PHI surface gated only by them is readable by **any** partner agent — which is
the blanket-tenancy hole this layer exists to seal. The row would *read* as gated to a human
reviewer while gating nothing.

**Fix — add an ENTITY SEGMENT to `permitted_tenancy`:**
```ts
// before — is_phi:true with no entity segment
permitted_tenancy: [...RPI_ONLY],  is_phi: true

// after — 'rpi' retained for RPI staff, entity segment added
const MWM_PHI: readonly Tenancy[] = ['rpi', 'partner_midwest_medigap']
permitted_tenancy: [...MWM_PHI],   is_phi: true
```
An entity segment is any `Tenancy` value OUTSIDE `{rpi, partner_agent, partner_admin,
superadmin}` — today `partner_midwest_medigap`, declared in
`packages/core/src/types/index.ts`.

**Do NOT resolve this by flipping `is_phi` to false.** The flag is a statement about the
data, not a gate setting; a PHI surface that claims it is not PHI dodges this rule and every
layer above it. If the row genuinely does not carry PHI, that is a contract change, not an
edit.

**⚠ THIS IS A SINGLE-LINE BELT. READ THIS BEFORE CONCLUDING A ROW IS COVERED.**

If you are reading this because you were BLOCKED, the block is correct — fix the row. But if you
are reading this to decide whether some OTHER row is safe, the answer is: **this rule not firing
is NOT evidence of compliance.**

- **Multi-line rows are NOT matched.** The content pattern joins `permitted_tenancy` and
  `is_phi` with `[^\n]*`, so both must sit on ONE physical line. A row that declares the
  blanket rail on one line and `is_phi: true` two lines below sails straight through. One such
  row exists in the registry today. Reformatting an object literal silently disarms this gate
  and nothing reports it.
- **L3 does not backstop that gap.** L3 examines only the **6 DIPSET registry rows**. This rule
  is not DIPSET-scoped. The two layers have DIFFERENT SETS and neither covers the union — a
  multi-line, non-DIPSET, `is_phi: true` row with a blanket rail is caught by NEITHER.
- **Why it was not "fixed" with a multi-line pattern:** a regex spanning lines inside an object
  literal cannot tell where a row ends, so it marries `permitted_tenancy` from one row to an
  `is_phi: true` two rows below. On a BLOCK-action PHI gate a false positive is worse than a
  false negative — it blocks correct work, and that is how you manufacture demand for a
  carve-out. The real fix is a structural import-time assert over `HUB_SURFACE_DEF`, scoped
  separately.

Declared 2026-07-28 after review refusal: nobody had watched this rule FAIL, only pass.

**3-LAYER ENFORCEMENT of this invariant:**
- **L1 (source):** the DIPSET Surfaces scope-contract G-L3C + JDM's ruling to build the lock
  rather than accept the exception for Midwest (2026-07-26).
- **L2 (this rule):** blocks the blanket-gated PHI row at write time.
- **L3 (merge backstop):** `scripts/check-dipset-registry-conformance.mjs` R3
  [blanket-tenancy-on-phi-row] fails the PR — it filters `permitted_tenancy` against
  `GENERIC_RAILS` and requires at least one segment outside it.

**A NOTE ON WHY THIS RULE IS ANCHORED THE WAY IT IS.** It matches a row DECLARATION — the
two fields co-occurring on one registry line — not a MENTION of `is_phi` or a tenancy value
in prose. Doc comments, contracts and this very file discuss those tokens constantly; an
unanchored rule would fire on all of them, and a guard that cries wolf trains seats to skim
the self-check preamble, which is the only thing standing between a phrase match and a
fabricated directive. The `file_path` condition additionally scopes it to the registry
source file, so this cannot fire fleet-wide on unrelated TypeScript.

**THE DATA/POLICY LINE:** `permitted_tenancy` and `is_phi` are **PR-gated CODE** in the typed
seed — never a Firestore console edit. The live `app_registry` rows are seeded FROM this file.
