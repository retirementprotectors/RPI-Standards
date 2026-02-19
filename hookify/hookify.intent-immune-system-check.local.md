---
name: intent-immune-system-check
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (immune\s+system|knowledge\s+report|knowledge\s+pipeline|what\s+happened\s+overnight|morning\s+briefing|overnight\s+report|compliance\s+(status|check))
---

## Immune System Check — Deliver Structured Briefing

**When this intent fires, read these data sources and deliver a structured briefing:**

### Data Sources (read in parallel)
1. `~/.claude/knowledge-promote.log` — last 50 lines (latest run output)
2. `~/.claude/knowledge-tracker.json` — current entry states (holding, promoted, deleted counts)
3. `~/.claude/compliance-sweep.md` — latest sweep report
4. `~/.claude/compliance-history.json` — violation trend data (last 30 runs)
5. `~/.claude/projects/-Users-joshd-millang/memory/MEMORY.md` — current MEMORY.md contents

### Briefing Format

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
