---
name: quality-gate-done-without-evidence
enabled: true
event: stop
action: warn
conditions:
  - field: last_assistant_message
    operator: regex_match
    pattern: (all (built|done|complete|shipped|audited)|everything('?s)? (done|built|shipped|complete)|(it'?s|its|we'?re) (done|complete|shipped|built|good to go)|(done|shipped|complete) (and|&|[+]) (verified|shipped|tested)|build (passes|is green|green)|type.?check (pass|passes|green)|[0-9]+/[0-9]+ pass|PASS,? *audit)
  # Exclusion (OB1-STOP-EVIDENCE-METACLAIM-001, 2026-07-19): don't re-fire on a turn that makes NO NEW
  # completion claim — a re-statement, a translation, or a reply ABOUT the gate itself. These meta-markers
  # essentially never appear in a genuine first-time "done" report, so the original hole (a bare
  # "PASS, audited" with nothing behind it) still fires.
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (false positive|gate (fired|misfired|fires|nagged)|fired (again|on (a|this|the|my|another)|last turn)|no new (done )?claim|no new work|nothing (new )?to (re-?)?verify|already (verified|ran (the )?(evidence )?(check|gate|checks))|(one|a) turn ago|(previous|last|prior) turn|re-?state|translat|in (plain )?english)
owner: shinob1
---

**EVIDENCE GATE: Cannot report completion without verification**

Before reporting work as complete, verify:
1. `git status` — working tree clean? All changes committed?
2. `npm run build` — passes all workspaces?
3. `git log --oneline -1` — commit exists?

Learned 2026-03-19: Wave 1 was reported as "PASS, audited" with 61 files uncommitted. Builder prompts were reported as "updated" when they were not.
