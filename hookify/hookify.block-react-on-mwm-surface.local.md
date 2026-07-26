---
name: block-react-on-mwm-surface
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (?:from|require\s*\()\s*['"][^'"]*(?:OpportunityBoard|OpportunityCard|CapstoneProfile)[^'"]*['"]|<\s*(?:OpportunityCard|CapstoneProfile)\b|\bexport\s+(?:default\s+)?(?:async\s+)?(?:function|const|let|var|class|interface|type|enum)\s+(?:OpportunityCard|CapstoneProfile)|\bexport\s*\{[^}]*(?:OpportunityCard|CapstoneProfile)
  - field: file_path
    operator: regex_match
    pattern: \.(?:tsx|jsx|ts|mts|cts)$
  - field: file_path
    operator: not_contains
    pattern: registry/app-registry-def.ts
owner: shinob1
---

🛑 **BLOCKED: React is being re-introduced onto an MWM surface.**

The DIPSET / Opportunity Board React module (`packages/ui/src/modules/OpportunityBoard/`) is **retired, not parked**. This write either re-creates one of its components or imports one into another file.

**The ruling this enforces (JDM, 2026-07-23 — authoritative):**
> "KILL the React fork — we do NOT put React on MWM surfaces. Consolidate on the HTML board. The unwired React module IS the drift — retire it, do not wire it."

**Why it is absolute:**
Two forks of one product existed. Nine DIPSET tickets were reported **done** while rendering on **zero** live surfaces — they compiled, so they looked finished. The board users actually see is `docs/dipset/dipset-board.html`. Wiring the React fork instead of deleting it would have created a dual surface to keep in sync forever and repeated the exact BUILT-BUT-DARK failure. The audit's tentative "lean WIRE" was explicitly overridden.

**The canonical surface:**
```
docs/dipset/dipset-board.html      # tab-pipeline · tab-validation · tab-taxonomy · tab-opportunity
```

**Fix — build it on the HTML board:**
- **Capstone profile?** A drawer off an Opportunity Board row-click **in the HTML board** — not a React `CapstoneProfile`, and not a 5th tab (D2).
- **Card reshape / tier badge / multi-evidence corroboration?** On the HTML board (D4).
- **Evidence redaction?** Redaction is enforced on the **registry row** (`is_phi: true` + a `partner_midwest_medigap` entity tenancy segment), not only in client-side JS. A UI-only redaction dies with the surface that carries it.
- **Registry row?** `dipset_opportunity_board` points at the HTML board surface. It must never point at a React component — `registry-conformance` (L3) asserts exactly that.

**3-Layer enforcement of this invariant (G-L3A):**
- **L1 (source):** the JDM ruling above + the DIPSET Surfaces scope-contract (doctrine).
- **L2 (this rule):** blocks the re-creation or import at write time.
- **L3 (merge backstop):** `registry-conformance` CI asserts no DIPSET registry row points at a React component.

**THE DATA/POLICY LINE:** deleting the module and repointing the registry row are **PR-gated CODE changes** — never a Firestore console edit.

**Scope of this rule (v1 — 2026-07-25, OB1-DIPSET-09):**
- **Matches CODE SHAPE, never the bare identifier.** Four arms: a module-specifier `import` / `export … from` / `require` naming the fork; a JSX element opening one of its components; an `export function|const|class|interface|type` declaring one; or a named re-export block. A file that merely *mentions* `OpportunityCard` in prose or a comment does **not** trip it.
- **That distinction is load-bearing, measured not assumed.** The naive `\b(OpportunityCard|CapstoneProfile|OpportunityBoard)\b` matcher hits **8 files**; the code-shape matcher hits **4** — exactly the fork, nothing else. The 4 the naive version would have falsely blocked are all comment-only references: `packages/core/src/registry/app-registry-def.ts` (**which would have blocked the very ticket that repoints the row off React**), `packages/ui/src/components/surface/Sheet.tsx`, and both `.github/scripts/death-gate-matcher*.js`. A literal-substring gate trips comments and identifiers as readily as real calls — the same trap that has cost this fleet whole sessions of blind bisection.
- **`app-registry-def.ts` is additionally excluded by an explicit `not_contains` condition** — belt and suspenders, so this gate can never block a registry repoint even if the comment text there changes.
- **Not matched structurally:** `.css`, `.md`, `.html`, discovery docs, and `/inbox/` artifacts — the file-extension condition confines this rule to React/TS source.
- **Deletion is not a write.** Removing the module (OB1-DIPSET-01) and stripping its imports do not trip this rule: a delete never reaches the file hook, and an `Edit` that removes an import carries the *post*-edit text, which no longer names the fork.
- **POSTURE: BLOCK.** This is a new rule and a hard stop from day one, deliberately — the invariant is an absolute JDM ruling rather than a tunable convention, and the measured false-positive surface is zero. It is the direct enforcement of the ruling the whole DIPSET Surfaces scope executes.
- **Residual gap, stated rather than papered over:** a brand-new `.tsx` under a DIPSET path that references none of the retired components and imports nothing from the module would not trip L2. L3 `registry-conformance` (OB1-DIPSET-10) is the backstop, and the module directory being deleted makes any file there a visible re-creation in the PR diff.

**Extending:** if another React component is ever added to the retired set, append it to the alternation — and measure the new identifier against the live tree first, comment-only references included. Coordinate with SHINOB1 (immune-system stewardship).

Doctrine: `docs/warriors/shared/toMachina-engineering-doctrine.md` → "3-LAYER ENFORCEMENT" + "THE DATA/POLICY LINE". Scope-contract: DIPSET Surfaces — Kill the React Fork, Consolidate the HTML Board (v1.0, 2026-07-23), gate G-L3A.
