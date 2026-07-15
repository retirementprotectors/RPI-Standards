---
name: immune-system-check
description: Deliver a structured Immune System briefing — pipeline health, compliance sweep trend, attention items, and MEMORY.md status — by reading the knowledge-promote log, tracker, compliance sweep + history, and MEMORY.md.
version: 0.1.0-draft
---

# Immune System Check

You have been invoked as the Immune System Check skill. Read the data sources below (in parallel) and deliver the structured briefing.

## Data Sources (read in parallel)

1. `~/.claude/knowledge-promote.log` — last 50 lines (latest run output)
2. `~/.claude/knowledge-tracker.json` — current entry states (holding, promoted, deleted counts)
3. `~/.claude/compliance-sweep.md` — latest sweep report
4. `~/.claude/compliance-history.json` — violation trend data (last 30 runs)
5. `~/.claude/projects/-Users-joshd-millang/memory/MEMORY.md` — current MEMORY.md contents

## Briefing Format

```
## Immune System Report — [date]

### Pipeline Health
- Last run: [timestamp] — Mode: [apply/sweep-only/dry-run]
- Entries promoted: [N] | Deleted: [N] | Holding: [N]
- Adaptive cap: [N]/run (backlog: [N] ready)
- All-time: [N] promoted, [N] deleted

### Compliance Sweep
- Total violations: [N] (delta: +/-N from previous)
- Top 3 rules: [rule]: [count], ...
- Trend: [improving/worsening/stable] over last [N] runs

### Attention Items
- [Any entries stuck in holding with 6+ sessions]
- [Any new violations appearing]
- [Any errors in last run (API key, git, Slack)]

### MEMORY.md Status
- Current entries: [N]
- Sections: [list]
```

> **Note (2026-07-08, WS-B conversion):** `~/.claude/projects/-Users-joshd-millang/memory/MEMORY.md` names a macOS-style path (`-Users-joshd-millang`) from before the fleet moved to the live Scroll shared streams (see `operating-rules.md` / MEMORY_DISCIPLINE.md). Verify this path still resolves on the box you're running from before citing it — if MEMORY.md has since been retired in favor of the Scroll, report that instead of a stale read.

---

*SHINOB1, CTO · immune-system-check · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-immune-system-check` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
