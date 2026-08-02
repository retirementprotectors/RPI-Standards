---
name: block-subcxo-brief-without-5surface-section
enabled: true
event: bash
action: block
# 2026-05-31 (SHINOB1): Authored from JDM directive "MEMORY.md is a fucking
# joke — how can we ENFORCE so subs aren't building unnecessary shit or going
# into a new project un-equipped?"
#
# Companion to dojo-warriors/scripts/validate-subcxo-brief.sh (hard gate at
# script entry) — this rule blocks the spawn at the bash-tool level so
# operators can't bypass by skipping the validator.
conditions:
  # Trigger: any spawn-subcxo-(disco|mesh).sh invocation with --brief flag
  - field: command
    operator: regex_match
    pattern: spawn-subcxo-(disco|mesh)\.sh.*--brief
  # Opt-out: command must include the validator immediately before spawn
  # (operator pattern: `validate-subcxo-brief.sh <brief> && spawn-subcxo-*.sh ...`)
  - field: command
    operator: not_contains
    pattern: validate-subcxo-brief.sh
owner: shinob1
---

**BLOCKED: sub-CXO spawn without brief validation**

Per JDM directive 2026-05-31 + VOLTRON v2.0 lock with SHINOB1: every sub-CXO
brief passed to `spawn-subcxo-(disco|mesh).sh --brief <path>` must contain
the canonical 5-section + 6-gap-surface structure.

**Why this is blocked:**
- Sub-CXOs that boot without inherited 5-surface sweep context re-sweep from scratch
- Re-sweeping wastes spawn-context burn + misses gaps the parent already mapped
- Missing watch-items = sub repeats class-of-bug already banked in memory
- The "ENFORCE" layer here closes the gap MEMORY.md alone cannot
- Per `feedback-voltron-subcxo-brief-5-section-6-gap` — peer composes WHAT (5 sections), SHINOB1 owns HOW (this gate)

**To proceed (the canonical pattern):**

```bash
cp /home/jdm/Projects/dojo-warriors/scripts/templates/sub-brief-skeleton.md \
   /tmp/<warrior>-<scope>-brief.md
# Hydrate every section + at least 4 of 5 gap surfaces (a)(b)(c)(d)(f)
/home/jdm/Projects/dojo-warriors/scripts/validate-subcxo-brief.sh /tmp/<warrior>-<scope>-brief.md \
  && /home/jdm/Projects/dojo-warriors/scripts/spawn-subcxo-mesh.sh \
       --parent <PARENT> --sub-type <TYPE> --scope-id <scope> \
       --brief /tmp/<warrior>-<scope>-brief.md
```

The validator exits 0 if the brief passes; the `&&` then fires spawn.
If validation fails, spawn never runs + STDERR lists the missing sections.

**Canonical references:**
- Skeleton: `dojo-warriors/scripts/templates/sub-brief-skeleton.md`
- Validator: `dojo-warriors/scripts/validate-subcxo-brief.sh`
- VOLTRON reference template: `warriors/voltron/sub-cxo-brief-template.md` (v2.0)
- Doctrine memory: `feedback-voltron-subcxo-brief-5-section-6-gap`
- Doctrine memory: `feedback-parent-5-surface-sweep-in-sub-brief`

**Exemptions:** none. If a brief legitimately omits a section, mark it
explicitly with `## Section N — N/A (reason: ...)` — the validator accepts
both fully-populated and explicitly-N/A'd sections.
