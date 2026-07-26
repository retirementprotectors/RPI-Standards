---
name: intent-immune-system-check
enabled: true
# GV2 WS-B batch 2: a DRAFT skill exists at _RPI_STANDARDS/skills/immune-system-check/.
# It is NOT WIRED. Skills load only via a manual symlink into ~/.claude/skills/;
# exactly one such symlink exists on the box today (case-drive-checklist).
# Until that symlink exists AND the skill is proven to load, THIS RULE IS THE ONLY
# ENFORCEMENT PATH. Do NOT set enabled:false on the strength of the draft alone --
# that removes enforcement and replaces it with a skill that never loads.
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (immune\s+system|knowledge\s+report|knowledge\s+pipeline|what\s+happened\s+overnight|morning\s+briefing|overnight\s+report|compliance\s+(status|check))
owner: shinob1
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

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
