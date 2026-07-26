---
name: intent-plan-mode
enabled: true
# GV2 WS-B batch 2: a DRAFT skill exists at _RPI_STANDARDS/skills/plan-mode/.
# It is NOT WIRED. Skills load only via a manual symlink into ~/.claude/skills/;
# exactly one such symlink exists on the box today (case-drive-checklist).
# Until that symlink exists AND the skill is proven to load, THIS RULE IS THE ONLY
# ENFORCEMENT PATH. Do NOT set enabled:false on the strength of the draft alone --
# that removes enforcement and replaces it with a skill that never loads.
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#LetsPlanIt|#letsplanit|plan\s+(this|it|out|for)|build\s+a\s+plan|make\s+a\s+plan|let'?s\s+plan|need\s+a\s+plan|create\s+a\s+plan|EnterPlanMode|plan\s+mode)
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

**THINKING LEVEL: SWITCH TO HIGH**

You are entering Plan Mode. Plans require deep multi-step reasoning across files, dependencies, execution order, and risk.

**Before building the plan:**
- Switch to HIGH thinking (extended thinking max)
- This is where mistakes are expensive — think hard now, execute fast later

**After plan is approved and you exit Plan Mode:**
- Switch back to MEDIUM thinking (default)
- Execution is mechanical — the plan already decided the *what*

**MANDATORY: When presenting the plan for approval, end with this exact block:**
```
Ready for approval. When you say go, I switch to MEDIUM thinking and execute.
```
This ensures JDM sees confirmation that the thinking level shift is happening.

**The rule:**
| Phase | Thinking Level |
|-------|---------------|
| Planning / Architecture / "Figure out why" | HIGH |
| Execution / Building / Deploying | MEDIUM |
| Simple edits / Lookups / Quick fixes | LOW |

---

**PIPELINE AWARENESS:**

You are Phase II (Planner). Your plan will be consumed by:
- **Phase III (Executor)**: Needs unambiguous tasks with clear scope boundaries
- **Phase IV (Auditor)**: Needs Audit Methods — exact grep patterns, line checks, screenshots
- **Phase V (JDM)**: Needs CHECKPOINT markers where he reviews before next sub-phase

Your plan MUST contain:
1. **Acceptance Criteria** column for every task — what "done" looks like
2. **Audit Method** column for every task — how the Auditor verifies (grep patterns, line counts, Playwright screenshots)
3. **CHECKPOINT** markers between sub-phases
4. **Audit Instructions** section (tells Phase IV what to verify per sub-phase)
5. Sub-phase labels with bounded scope (e.g., "1A:", "1B:")

**Kill means DELETE the code entirely.** Not merge. Not hide. Not stub. Not rename. Not comment out. If a task says "kill X", the Acceptance Criteria must require ZERO references, and the Audit Method must specify the exact grep patterns to prove it.
