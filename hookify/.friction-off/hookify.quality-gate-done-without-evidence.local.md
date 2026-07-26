---
name: quality-gate-done-without-evidence
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (all.*(?:built|done|complete|pass|shipped|audited)|(?:built|done|complete|pass|shipped|audited).*all|everything.*(?:done|built|pass)|PASS.*audit|audit.*PASS)
owner: shinob1
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

**EVIDENCE GATE: Cannot report completion without verification**

Before reporting work as complete, verify:
1. `git status` — working tree clean? All changes committed?
2. `npm run build` — passes all workspaces?
3. `git log --oneline -1` — commit exists?

Learned 2026-03-19: Wave 1 was reported as "PASS, audited" with 61 files uncommitted. Builder prompts were reported as "updated" when they were not.
