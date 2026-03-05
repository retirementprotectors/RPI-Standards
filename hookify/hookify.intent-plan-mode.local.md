---
name: intent-plan-mode
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#LetsPlanIt|#letsplanit|plan\s+(this|it|out|for)|build\s+a\s+plan|make\s+a\s+plan|let'?s\s+plan|need\s+a\s+plan|create\s+a\s+plan|EnterPlanMode|plan\s+mode)
---

**THINKING LEVEL: SWITCH TO HIGH**

You are entering Plan Mode. Plans require deep multi-step reasoning across files, dependencies, execution order, and risk.

**Before building the plan:**
- Switch to HIGH thinking (extended thinking max)
- This is where mistakes are expensive — think hard now, execute fast later

**After plan is approved and you exit Plan Mode:**
- Switch back to MEDIUM thinking (default)
- Execution is mechanical — the plan already decided the *what*

**The rule:**
| Phase | Thinking Level |
|-------|---------------|
| Planning / Architecture / "Figure out why" | HIGH |
| Execution / Building / Deploying | MEDIUM |
| Simple edits / Lookups / Quick fixes | LOW |
