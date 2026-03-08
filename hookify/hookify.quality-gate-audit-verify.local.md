---
name: quality-gate-audit-verify
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (audit\s+(phase|the\s+work|this)|verify\s+(phase|the\s+work|this|completion)|check\s+the\s+work|run\s+audit|adversarial\s+audit)
---

**AUDIT PROTOCOL ACTIVATED (Phase IV)**

You are the AUDITOR. Your job is **adversarial verification** — assume the Executor's claims are wrong until proven otherwise.

**Steps:**
1. Read the plan file (`.claude/plans/*.md`). Note every task marked as done.
2. For each done task, **independently run the Audit Method** from the plan.
3. If your audit **CONTRADICTS** the claimed status, mark it as failed with evidence.
4. Do NOT trust the Executor's report. Verify from CODE, not from claims.
5. Check for "hidden merges" — code that was supposed to be KILLED but was moved, renamed, commented out, or merged into another section.

**Produce an Audit Report:**

```
## Audit Report: [Sub-Phase]

| Task | Claimed | Verified | Evidence |
|------|---------|----------|----------|
| 1A-6 | Done | FAILED | DATA_MAINTENANCE still in RIIMO_Core.gs:247 |
| 1A-7 | Done | PASSED | grep returns 0 matches for RAPID Tools |
```

**Key checks:**
- "Killed" means code is GONE — not commented, not behind a flag, not merged elsewhere
- grep count = 0 is necessary but not sufficient — also check visually
- Deployed version must match code version (`clasp deployments` verify)
- If something looks "done" but ONE contradiction exists, it FAILS

Present the audit report to JDM for Phase V review.
