---
name: plan-mode
description: Enter Plan Mode correctly (#LetsPlanIt) — switch to HIGH thinking for the plan, build a plan with Acceptance Criteria + Audit Method columns and CHECKPOINT markers per the FORGE pipeline shape, and confirm the thinking-level switch back to MEDIUM on approval.
version: 0.1.0-draft
---

# Plan Mode

You have been invoked as the Plan Mode skill — entering Plan Mode (#LetsPlanIt).

**THINKING LEVEL: SWITCH TO HIGH.** Plans require deep multi-step reasoning across files, dependencies, execution order, and risk.

## Before building the plan

- Switch to HIGH thinking (extended thinking max).
- This is where mistakes are expensive — think hard now, execute fast later.

## After the plan is approved and you exit Plan Mode

- Switch back to MEDIUM thinking (default).
- Execution is mechanical — the plan already decided the *what*.

**MANDATORY:** when presenting the plan for approval, end with this exact block so JDM sees confirmation of the thinking-level shift:

```
Ready for approval. When you say go, I switch to MEDIUM thinking and execute.
```

## Thinking-level rule

| Phase | Thinking Level |
|-------|---------------|
| Planning / Architecture / "Figure out why" | HIGH |
| Execution / Building / Deploying | MEDIUM |
| Simple edits / Lookups / Quick fixes | LOW |

## Pipeline Awareness

You are Phase II (Planner). Your plan will be consumed by:

- **Phase III (Executor)** — needs unambiguous tasks with clear scope boundaries.
- **Phase IV (Auditor)** — needs Audit Methods: exact grep patterns, line checks, screenshots.
- **Phase V (JDM)** — needs CHECKPOINT markers where he reviews before the next sub-phase.

Your plan MUST contain:

1. **Acceptance Criteria** column for every task — what "done" looks like.
2. **Audit Method** column for every task — how the Auditor verifies (grep patterns, line counts, Playwright screenshots).
3. **CHECKPOINT** markers between sub-phases.
4. **Audit Instructions** section (tells Phase IV what to verify per sub-phase).
5. Sub-phase labels with bounded scope (e.g., "1A:", "1B:").

**Kill means DELETE the code entirely.** Not merge. Not hide. Not stub. Not rename. Not comment out. If a task says "kill X", the Acceptance Criteria must require ZERO references, and the Audit Method must specify the exact grep patterns to prove it.

When execution starts, hand off to the `/execute-plan` skill.

---

*SHINOB1, CTO · plan-mode · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-plan-mode` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
