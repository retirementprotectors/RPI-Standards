---
name: intent-execute-plan
enabled: false
# → migrated to skill execute-plan (GV2 WS-B batch 2, STAGED). See
#   _RPI_STANDARDS/skills/execute-plan/. Pattern + regex kept below as
#   historical reference and as the fallback if the skill conversion is
#   not ratified. Do NOT re-enable without SHINOB1 review.
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#LetsRockIt|#letsrockit|let'?s\s+rock|rock\s+it|execute\s+the\s+plan|plan\s+approved|green\s+light|go\s+build)
owner: shinob1
---

**PLAN EXECUTION TRIGGERED (#LetsRockIt)**

Plan approved. Switching to MEDIUM thinking for execution.

1. Exit Plan Mode (ExitPlanMode)
2. Execute the approved plan file sequentially
3. Spawn parallel agents where phases are independent
4. Report results at each milestone
5. When complete: ask JDM if ready for #SendIt (deploy)

The plan already decided the *what*. Now execute the *how*.
