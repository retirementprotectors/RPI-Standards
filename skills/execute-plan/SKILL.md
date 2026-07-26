---
name: execute-plan
description: Switch from Plan Mode to execution once a plan is approved (#LetsRockIt) — drop to MEDIUM thinking, exit Plan Mode, execute the approved plan sequentially, spawn parallel agents on independent phases, and report at each milestone.
version: 0.1.0-draft
---

# Execute Plan

You have been invoked as the Execute Plan skill — a plan has been approved and it is time to execute.

**Switching to MEDIUM thinking for execution.**

## Steps

1. Exit Plan Mode (`ExitPlanMode`).
2. Execute the approved plan file sequentially.
3. Spawn parallel agents where phases are independent.
4. Report results at each milestone.
5. When complete, ask JDM if ready for `#SendIt` (deploy) — see the `/sendit` skill.

The plan already decided the *what*. Now execute the *how*.

---

*SHINOB1, CTO · execute-plan · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-execute-plan` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
