# `reference/hookify-parked-rules/` — parked hookify rules, dormancy STRUCTURAL

**OB1-FRICTION-OFF-UNDECLARED-001** · owner: SHINOB1 (hookify) · cut 2026-08-02

Every rule in this directory is **OFF**. This file is the single place that says why,
what actually keeps them off, and — the part that matters — **what does not**.

## Why this repo, and not only `dojo-warriors`

The sibling change parked the same 31 rules in `dojo-warriors`
(`docs/hookify-parked-rules/`). **It was correct and incomplete**, and MEGAZORD's
cross-lane review named the half that was missing:

> *"Identical set. Same 31 rules, same 17/14 split, both places. This PR parks the
> `dojo-warriors` copy and leaves the `_RPI_STANDARDS` copy exactly as it was — and
> `_RPI_STANDARDS/hookify` is the directory the live dispatcher's `RULES_DIR` actually
> points at."*

**This is the repo that loads.** Leaving the misreading here and fixing it only in the
other repo would have closed the defect everywhere except where a reader is most likely
to look — the one directory a person inspecting live enforcement actually opens.

## What was wrong

31 rules sat in `hookify/.friction-off/` — **17 `action: block`, 14 `action: warn`**,
including `block-gh-pr-merge-admin-bypass` and
`block-canonical-doctrine-write-outside-ssot`. **30 of the 31 carried
`enabled: true`.**

They read as live guards and enforced nothing.

## What actually keeps them off

**The LOCATION and the EXTENSION — never the `enabled` field.** Every file here carries a
`.parked` suffix and sits outside every rule root, so three independent barriers apply and
**any one of them alone is sufficient**:

| barrier | why it holds |
|---|---|
| wrong directory | the live dispatcher's `RULES_DIR` is `hookify/`; this is `reference/` |
| glob is non-recursive | `hookify.*.local.md` cannot reach a subdirectory in any case |
| `.parked` suffix | breaks the `.local.md` anchor, so no loader glob and no merge gate sees a rule at all |

`enforce.sh` reads `hookify/scope-bound/*.local.md` — a different directory again.

## Measured, with the controls that make the zero mean something

Run with the dispatchers' own glob expressions, before and after the move:

```
                                        BEFORE   AFTER
hookify/hookify.*.local.md                 106     106    <- positive control
hookify/scope-bound/*.local.md               6       6    <- positive control
.friction-off files on disk                 31       0
parked files reachable by either glob        0       0
*.local.md anywhere under reference/         -       0
```

**The two controls are the point.** They return non-zero on the live directories through
the same code path, so the `0` on the parked set is a finding rather than a broken filter.
They are also **unchanged across the move**, which is the proof that nothing live was
disarmed: not one rule went from loaded to unloaded.

**Nothing is armed by this change either.** No rule moves OFF → ON. Arming 17 `block`
rules is a blast-radius decision and is not what a dormancy declaration is for.

## A correction worth carrying — the old state was not a coincidence

The `dojo-warriors` README said the previous dormancy *"rested on glob flatness — a
coincidence."* **That is wrong, and MEGAZORD's review corrected it:** the glob is
non-recursive **by construction**, and `dojov3/bin/hookify-l2-bypass.mjs` documents this
exact case as GAP 2 — *"was governed, never loads."*

So this change does not make dormancy real. **It makes dormancy LEGIBLE** — which is a
smaller claim than the original one, and the true one. The defect being fixed is that a
reader could not tell an inert rule from a live one, not that an inert rule might fire.

## To un-park a rule

Do not edit `enabled` here — nothing reads it at this path. Move the file back to
`hookify/hookify.<name>.local.md`, drop the `.parked` suffix, and treat it as **arming a
rule**: state the blast radius. For a `block` rule that means naming what it will start
refusing, and for whom.
