# ATLAS Consult — Gates

> Hookify enforcement map for this skill. Rules are referenced BY NAME only —
> never duplicated here. Hookify (`_RPI_STANDARDS/hookify/`) is the SSOT for
> all literal patterns and enforcement logic.

## No code-level enforcement — this is a context-injector, not a violation-detector

`intent-atlas-consult`, the hookify rule this skill was converted from, was never a
BLOCK/WARN rule that catches a bad action — it fired on `event: prompt` /
`action: block` purely to *inject* the ATLAS-consultation runbook into context
whenever a prompt matched its data-work regex. It detected no violation and
enforced no invariant; it was a dumb context-injector riding the hot-path
prompt-event matcher. That is exactly the GV2 WS-B class this pilot converts:
9 `intent-*` rules doing injection, not detection, removed from the hot path
and made invocable instead.

**Enforcing hookify rules:** none. This skill carries no `hooks_enforcing`
entries because it enforces nothing at the code level — it is operator/agent
guidance, invoked deliberately (`/atlas-consult`) instead of fired
unconditionally on every matching prompt.

**Source rule status:** `intent-atlas-consult` is being set to `enabled: false`
in this same PR, with a body note pointing here. It is NOT deleted — the
pattern + regex stay on disk as historical reference and as the fallback if
this skill conversion is not ratified.

---

> **If a future revision of this skill needs code-level enforcement** (e.g. a
> hard block on data-import work that skips ATLAS entirely), author that rule
> in `_RPI_STANDARDS/hookify/` per the hookify process (requires SHINOB1
> review), then add a row here. Never define rule patterns in this file.
