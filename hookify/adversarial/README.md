# Adversarial corpora — reviewer-authored, committed on purpose

`MZ-ADVERSARIAL-CORPUS-001` · megazord · 2026-07-26

These are **not** the builder's tests. They were written by a reviewer (HIKARI) who was
deliberately trying to break `warn-checkout-in-standards-tree`, against a frozen sha, without
seeing the builder's own corpus first. Three rounds, three real defects, none of which the
builder would have found.

They are committed because they lived in a session scratchpad that dies with the seat that
made them — the same *"it only exists in one place"* failure this repo has been closing all
week, pointed at the evidence itself.

## Provenance

| File here | Original | sha256 (first 16) | Author |
|---|---|---|---|
| `round3-hazard-shapes.py` | `adv.py` | `4846600848e2906b` | HIKARI |
| `round4-quote-spans.py` | `adv4.py` | `33e1b241b1ad8c62` | HIKARI |
| `round4b-nesting-matrix.py` | `mirror.py` | `b80cfe491b4caa2c` | HIKARI |

**Byte-identical to the originals**, with exactly one recorded exception below. Renamed for
clarity only; contents otherwise unmodified, verified with `cmp`. Do not "tidy" them — a
reconstruction of a reviewer's corpus is a builder's corpus with better marketing.

**Exception — `round4b-nesting-matrix.py`, `HIK-CORPUS-EXIT-001`, by HIKARI (its author).**
As committed in #77 it had **no `sys.exit`**, so it failed green: it printed its failures and
returned rc 0, and any runner reading the exit code saw a clean pass. One line added —
`sys.exit(1 if bad else 0)` — matching both siblings. Nothing else changed; no case, no
expectation, no pattern. sha256 in the table updated from `2d19d0fcc4bbff30` accordingly,
because a provenance table that still claimed byte-identity would be exactly the class of
defect this corpus exists to catch.

Proven both ways on a syntactically valid instrument (compile checked first, so the exit code
means something): unmodified vs the live rule → `4/4 pass`, **rc 0**; a copy with a single
expectation inverted → `3/4 pass` with the false negative reported, **rc 1**.

The builder deliberately did *not* fix this — it is the reviewer's file, and a builder tidying
a reviewer's corpus is how the arrangement stops meaning anything.

## What each one found

- **round3** — four **false negatives**: real branch ops going *silent* because a quote
  appeared earlier on the line (`cd "<tree>" && git <verb> main`). Byte-for-byte the incident
  shape the rule exists to catch. A false negative here is strictly worse than a false positive.
- **round4** — quote-span handling, including an apostrophe inside a double-quoted commit
  message, escaped inner quotes, command substitution, and a backslash line-continuation.
- **round4b** — the nesting matrix: each quote type nested inside each other type. Confirms the
  span clause is **order-independent** — the branches are keyed on the opening character, so
  they cannot compete at a given position.

## Running them

```
python3 hookify/adversarial/run-all.py <path-to-rule.md>                 # expect clean
python3 hookify/adversarial/run-all.py <path-to-rule.md> --expect-fail   # prove discrimination
```

`run-all.py` is the builder's, not the reviewer's. It exists because **`round4b` has no
`sys.exit`** — it prints its failures and returns 0 regardless. A committed test that cannot
fail loudly is worse than no test. The runner therefore reads each corpus's *output* and treats
any printed failure marker as a failure, ANDed with the exit code. It reports **per corpus,
never a total**, so a corpus that regresses to zero coverage cannot hide behind another that grew.

## ⚠️ These have a half-life. That is the running cost of the method, not a defect in it.

The moment a reviewer's corpus is committed, it becomes **builder-owned**: it is now part of
the inventory of failures the builder already knows about, and it can no longer surprise them.

> A builder's corpus is an inventory of the failures he already imagined.
> A reviewer who reuses their own last corpus has quietly become the builder.

So these files prove the rule survives **the attacks already made**. They do not and cannot
prove it survives the next one. **Round 5 requires new reviewer-chosen inputs**, and so does
every round after.

Read as permanent coverage, this directory becomes rehearsal wearing a test-suite badge — a
gate demonstrated only on inputs its own side constructed has established that it *can* fire,
never *when*. Budget for a fresh adversarial pass whenever the rule's matching clause changes.

## Discrimination status — measured, not assumed

Against the pre-fix revision (`51518ac`), `--expect-fail` behaviour:

| corpus | vs broken rule | discriminates? |
|---|---|---|
| round3 | 12/17, exit 1 | **yes** |
| round4 | 8/13, exit 1 | **yes** |
| round4b | 4/4, exit 0 | **no — and correctly so** |

`round4b` passing against the broken revision is **expected**: that revision had no quote guard
at all, so quoted hazards fired there for the wrong reason. It discriminates against a
hypothetical order-dependent implementation, which is a real risk if someone edits the
alternation, but is not the defect the earlier revision had. Recorded here so nobody reads its
green as evidence about the shipped fix, and nobody "fixes" it by deleting it.
