---
name: intent-execute-plan
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#LetsRockIt|#letsrockit|let'?s\s+rock|rock\s+it|execute\s+the\s+plan|plan\s+approved|green\s+light|go\s+build)
---

**PLAN EXECUTION TRIGGERED (#LetsRockIt)**

Plan approved. Switching to MEDIUM thinking for execution.

1. Exit Plan Mode (ExitPlanMode)
2. Execute the approved plan file sequentially
3. Spawn parallel agents where phases are independent
4. Report results at each milestone
5. When complete: ask JDM if ready for #SendIt (deploy)

The plan already decided the *what*. Now execute the *how*.
