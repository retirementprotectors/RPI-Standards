---
name: block-scope-build-before-confirm
enabled: false
event: file
action: warn
owner: shinob1
introduced: 2026-07-07
status: DESIGNED_NOT_ARMED — SHINOB1 recommends DEFER (see FP simulation below). Do not flip enabled:true without re-running the simulation in this file and getting a clean pass.
conditions:
  - field: tool
    operator: equals
    pattern: Write
  - field: file_path
    operator: regex_match
    pattern: ^(apps|packages|services)/.*\.(ts|tsx|js|jsx)$
  - field: file_path
    operator: not_contains
    pattern: .test.
  - field: file_path
    operator: not_contains
    pattern: .spec.
  - field: file_path
    operator: not_contains
    pattern: __mocks__
  - field: content
    operator: not_contains
    pattern: Scope-Ref:
  - field: content
    operator: not_contains
    pattern: scope_confirmed:
  - field: content
    operator: not_contains
    pattern: build_contract:
---

WARN (dormant — `enabled: false`, do not arm): This file is being built inside
`apps/`, `packages/`, or `services/` with no `Scope-Ref:` / `scope_confirmed:` /
`build_contract:` marker anywhere in it — i.e. no trace back to a confirmed
scope. Run `/scope-confirm` against the governing ticket/brief first, or add a
`Scope-Ref: <TICKET-ID>` comment citing the confirmed scope, before continuing
the build.

## Why this is the missing WS-B rule, and why it ships DISABLED

This is `block-scope-build-before-confirm` from the original GV2 disco
(`docs/strategy/disco-verification-layer-and-doctrine-consolidation.md`,
WS-B/B2): "fires if a warrior's first build action lands before a scope-read
confirmation." Per `OB1-GV2-REBASELINE-001` (the 2026-07-06 gap ledger), this
rule had **no file, no commit, anywhere** — this closes that gap by landing a
fully-designed v1. It ships `enabled: false` (never fires) because the honest
FP simulation below says arming it today — even as WARN — is not safe.

## The FP-safety brief, worked

The build-SPC instruction for this ticket was explicit: find the tightest,
lowest-FP trigger, simulate it against the LIVE toMachina repo, report the
false-positive count, and if it would fire on legitimate existing code,
tighten it, WARN-only it, or recommend deferring outright rather than forcing
a high-FP rule onto every warrior's edits. Two things ruled out a clean v1:

**1. The literal intent is a sequence check, not a content check.** "First
build action lands before a scope-read confirmation" is about *order of
operations within a session* (was a confirm step logged before the first
Write?). The generic hookify `event: file` engine (the one `warn-early-
conclusion` and `block-done-without-live-verify` run on) only ever sees ONE
isolated tool call's `content` + `file_path` + `tool` — it has zero visibility
into session history, prior tool calls, or "was this the first Write." That
kind of session-sequence awareness only exists today in the scope-bound
event lane (`event: pre-write` + a custom `check_<event>.sh` script reading
the per-session tmux ledger at `/tmp/scope-prior-art-<session>.jsonl`) — and
even there, `enforce.sh` currently logs `mcp__*` tool calls and `__ship__`
git-push tags into that ledger, **never** Read/Write/Edit. There is no
"first build action" signal available anywhere in the fleet today without
first extending the dispatcher itself — a materially bigger change than a
single hookify rule file, and out of scope for this ticket.

**2. There is no positive "confirmed" signal to check against — by design,
not by oversight.** The original disco scoped `/scope-confirm` (WS-C: "read
ticket → confirm understanding → emit build contract") as the thing that
would PRODUCE the confirmation artifact this gate checks for. Per the same
rebaseline: "missing WS-C — `/scope-confirm`, `/arch-route`, `/pr-land`
skills. None exist." WS-B was always downstream of WS-C in the original
disco's own architecture — the gate was never meant to ship before its own
evidence producer.

## The simulation (live toMachina repo, 2026-07-07)

Ran the tightest content-based proxy available without session state: does
the new/changed file carry ANY marker that a `/scope-confirm`-style skill
would plausibly emit (`Scope-Ref:`, `scope_confirmed:`, `build_contract:`)?

```
find apps packages services -type f \( -name "*.ts" -o -name "*.tsx" \
  -o -name "*.js" -o -name "*.jsx" \) | grep -v node_modules \
  | xargs grep -lE 'Scope-Ref:|scope_confirmed:|build_contract:' | wc -l
# → 0

find apps packages services -type f \( -name "*.ts" -o -name "*.tsx" \
  -o -name "*.js" -o -name "*.jsx" \) | grep -v node_modules \
  | grep -v '\.d\.ts$' | wc -l
# → 2524
```

**0 / 2524 existing implementation files (0%) carry the marker.** That is
not a tuning problem — it means the condition as designed would fire on
essentially 100% of legitimate Writes to `apps/`, `packages/`, `services/`,
forever, because nothing in the fleet has ever produced the signal it's
looking for. (A looser proxy — "no ticket-ID-shaped token anywhere in the
file" — was tried first and simulated even worse: 1,479 / 2,048 existing
`.ts`/`.tsx` files, 72%, carry no such token, since ticket IDs live in commit
messages and PR titles, not inline in source. Tightening further doesn't
help; the problem isn't the pattern, it's that the thing being checked for
doesn't exist yet.)

## SHINOB1 recommendation: DEFER, don't arm

This ships DISABLED (`enabled: false`) with `action: warn` reserved for when
it's safe — never `block`, matching the fleet-wide rule for a first-run
governance gate. **Do not flip `enabled: true`** until:

1. `/scope-confirm` (WS-C) ships and actually emits a `Scope-Ref:` /
   `scope_confirmed:` marker warriors are expected to carry into their build,
   AND
2. This exact simulation is re-run and shows a non-trivial pass rate on live
   code (i.e. real warriors are actually emitting the marker in practice, not
   0/2524), AND
3. Ideally, this graduates to a proper scope-bound `pre-write` rule with a
   `check_scope_build_confirm.sh` script reading the per-session ledger
   (requires extending `enforce.sh`'s ledger to log Write/Edit + a confirm
   event) rather than the blunt content-regex form here — the same
   architecture already proven by `block-disco-write-from-non-sub-session`.

## Companion tickets this depends on

- `OB1-GV2-P3-SKILLS` (re-issued in `OB1-GV2-REBASELINE-001`) — ships
  `/scope-confirm`. This rule cannot safely arm before that lands.
- A future ledger-extension ticket to log Write/Edit + confirm events into
  `/tmp/scope-prior-art-<session>.jsonl` (currently `mcp__*` + `__ship__`
  only) — needed for the scope-bound sequence-aware version.

See: `docs/strategy/disco-verification-layer-and-doctrine-consolidation.md`
(WS-B/B2, original ask) · `docs/discoveries/ob1-gv2-rebaseline-001-
governance-v2-rebaseline-v1.0.html` (gap ledger that flagged this missing) ·
`_RPI_STANDARDS/hookify/scope-bound/block-disco-write-from-non-sub-session.
local.md` (the sequence-aware architecture pattern to copy once the ledger
signal exists).
