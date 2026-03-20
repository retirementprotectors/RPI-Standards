---
name: quality-gate-done-without-evidence
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (all.*(?:built|done|complete|pass|shipped|audited)|(?:built|done|complete|pass|shipped|audited).*all|everything.*(?:done|built|pass)|PASS.*audit|audit.*PASS)
---

**EVIDENCE GATE: Cannot report completion without verification**

Before reporting work as complete, verify:
1. `git status` — working tree clean? All changes committed?
2. `npm run build` — passes all workspaces?
3. `git log --oneline -1` — commit exists?

Learned 2026-03-19: Wave 1 was reported as "PASS, audited" with 61 files uncommitted. Builder prompts were reported as "updated" when they were not.
