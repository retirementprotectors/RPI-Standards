---
name: quality-gate-phase-complete
enabled: true
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (phase\s+complete|sub-?phase\s+(done|complete)|ready\s+for\s+review|checkpoint\s+(reached|done|complete)|all\s+tasks\s+(done|complete)|deployed\s+and\s+verified)
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

**BLOCKED: Cannot report phase complete without evidence**

Before reporting a phase/sub-phase as complete, you MUST:

1. **Read the plan file** (`.claude/plans/*.md`)
2. **For EVERY task in the current sub-phase:**
   - Update status to done or not done with evidence
   - If done: include the audit evidence (grep result, line number, screenshot)
   - If not done: explain what's still needed
3. **Run the Audit Method** for each task (from the plan's Audit Method column)
4. **Update the plan file** with results BEFORE reporting
5. Only report complete when ALL tasks show evidence

The Phase 6 portal overhaul had a 21% success rate because the executor self-reported without evidence. This gate prevents that from happening again.

**After updating the plan file, report to JDM with:**
- Summary of what was done
- Any tasks that failed with reasons
- Link to updated plan file
