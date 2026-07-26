# registry-check — Gates

> Hookify enforcement map for this skill. Rules are referenced BY NAME only —
> never duplicated here. Hookify (`_RPI_STANDARDS/hookify/`) is the SSOT for
> all literal patterns and enforcement logic.

## No code-level enforcement — this is a context-injector, not a violation-detector

`intent-no-create-without-registry-check`, the hookify rule this skill was converted from, was never a
BLOCK/WARN rule that catches a bad action — it fired on `event: prompt` purely
to *inject* this guidance into context whenever a prompt matched its regex. It
detected no violation and enforced no invariant. That is exactly the GV2 WS-B
class this batch converts: dumb context-injectors riding the hot-path
prompt-event matcher, removed from the hot path and made invocable instead.

**Enforcing hookify rules:** none. This skill carries no `hooks_enforcing`
entries because it enforces nothing at the code level — it is operator/agent
guidance, invoked deliberately (`/registry-check`) instead of fired unconditionally
on every matching prompt.

**Source rule status:** `intent-no-create-without-registry-check` is set to `enabled: false` (or
already was) with a migration-pointer note in this same PR. It is NOT deleted
— the pattern + regex stay on disk as historical reference and as the
fallback if this skill conversion is not ratified.

---

> **If a future revision of this skill needs code-level enforcement**, author
> that rule in `_RPI_STANDARDS/hookify/` per the hookify process (requires
> SHINOB1 review), then add a row here. Never define rule patterns in this file.
