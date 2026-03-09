# Close the Immune System Loop

## Context

The Immune System has two halves: **enforcement** (hookify, real-time) and **learning** (knowledge-promote, nightly). The learning half runs, promotes entries, and scans for compliance violations — but the results go into a dead-end file (`compliance-sweep.md`) that nothing reads. No Slack notifications. No trend tracking. The "closed loop" described in CLAUDE.md is open.

Additionally:
- **ANTHROPIC_API_KEY is commented out** in `MCP-Hub/.env` — AI-powered section routing has **never worked** in production. Every promotion has used heuristic fallback (end-of-file insertion).
- **27 entries with 6+ sessions** are stuck in holding because MAX_PROMOTIONS = 5/day creates a multi-day backlog.
- **No SLACK_BOT_TOKEN** in `.env` — Slack integration doesn't exist yet.
- **Log lines appear twice** — launchd redirects stdout to the log file, AND the `log()` function appends to the same file.

## Changes

### 1. Fix `.env` — Unblock AI Classification + Enable Slack
**File:** `/Users/joshd.millang/Projects/RAPID_TOOLS/MCP-Hub/.env`
- Uncomment + set `ANTHROPIC_API_KEY` (key provided by JDM)
- Add `SLACK_BOT_TOKEN=<redacted — use Script Properties>`

### 2. Add Slack Daily Digest to knowledge-promote.js
**File:** `~/.claude/knowledge-promote.js`

Add three functions after existing `loadApiKey()` (~line 116):
- `loadSlackToken()` — same pattern as `loadApiKey()`, reads from env then `.env` file
- `buildSlackBlocks(digest)` — constructs Slack Block Kit payload (reuse pattern from `MCP-Hub/analytics/weekly-report.js` lines 147-201)
- `postSlackDigest(digest)` — posts to `C09UNESEYMU` (#jdmceo) with Bearer auth via native `fetch`

Digest includes: promotions (count + list), deletions, holding count, approaching-threshold count, compliance violations + delta from last run, top 3 violation rules, pipeline health stats, any errors.

Graceful failure: if no token, log warning, skip — never block the pipeline.

### 3. Add Compliance History Tracking
**File:** `~/.claude/knowledge-promote.js`

New path constant: `COMPLIANCE_HISTORY_PATH = ~/.claude/compliance-history.json`

Three new functions:
- `loadComplianceHistory()` — load JSON, return `{ runs: [] }` on error
- `saveComplianceHistory(history)` — write JSON, keep last 30 runs
- `recordComplianceRun(violations)` — append current run, calculate delta from previous

Structure:
```json
{ "runs": [{ "date": "2026-02-19", "totalViolations": 256, "byRule": { "block-alert-confirm-prompt": 78 } }] }
```

### 4. Wire Slack + History Into Main Pipeline
**File:** `~/.claude/knowledge-promote.js`

- **`--sweep-only` mode**: After writing sweep report, call `recordComplianceRun()` + `postSlackDigest()` with sweep-only metrics
- **`--apply` mode**: Change compliance sweep to run on EVERY apply (not just when rules promoted). After sweep, call `recordComplianceRun()`, build full digest object, call `postSlackDigest()`. Slack post happens before git commits (Phase 8) so commit failures don't block notification.

### 5. Adaptive MAX_PROMOTIONS
**File:** `~/.claude/knowledge-promote.js`

Replace `MAX_PROMOTIONS = 5` with adaptive logic:
- Base: 5/day
- +1 per 3 backlog items above base
- Ceiling: 15/day
- Current backlog of 29 → promotes ~13/run → clears in 2-3 runs instead of 6

### 6. Fix Duplicate Log Lines
**File:** `~/.claude/knowledge-promote.js`

In `log()` function: only call `console.log()` when `process.stdout.isTTY` is true. The `fs.appendFileSync` to LOG_PATH stays unconditional. This prevents double-writes when launchd also redirects stdout to the same file.

### 7. Create Hookify Intent Rule
**New file:** `/Users/joshd.millang/Projects/_RPI_STANDARDS/hookify/hookify.intent-immune-system-check.local.md`

```yaml
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
```

Message body: instructions to read log, tracker, sweep report, compliance history, and MEMORY.md, then deliver structured briefing format.

After creating: run `setup-hookify-symlinks.sh` to propagate to all 18 projects.

### 8. Update CLAUDE.md Immune System Section
**File:** `~/.claude/CLAUDE.md` + `/Users/joshd.millang/Projects/_RPI_STANDARDS/CLAUDE.md`

- Add "check the immune system" to Communication Style signals table
- Update the "Closed Loop (Future)" line to reflect it's now LIVE
- Add `intent-immune-system-check` to the Intent Rules list

## Implementation Order

1. Fix `.env` (unblocks AI classification — ask JDM for ANTHROPIC_API_KEY)
2. Fix duplicate logging (quick, improves readability for testing)
3. Add `loadSlackToken()` + `buildSlackBlocks()` + `postSlackDigest()` (self-contained additions)
4. Add compliance history functions (self-contained additions)
5. Wire into main pipeline (modifies existing Phase 7 region + sweep-only block)
6. Adaptive MAX_PROMOTIONS (constant change + cap logic)
7. Create hookify intent rule + symlink propagation
8. Update CLAUDE.md

## Verification

1. `node ~/.claude/knowledge-promote.js --dry-run` — verify no errors, check adaptive promotion count
2. `node ~/.claude/knowledge-promote.js --sweep-only` — verify compliance-history.json created + Slack message posted to #jdmceo
3. `node ~/.claude/knowledge-promote.js --apply` — verify full pipeline + Slack digest + no duplicate logs
4. Say "check the immune system" in a new session context — verify hookify intent fires
5. Git commit both repos (`~/.claude` + `_RPI_STANDARDS`)

## Files Modified

| File | Change |
|------|--------|
| `~/Projects/RAPID_TOOLS/MCP-Hub/.env` | Add SLACK_BOT_TOKEN, uncomment ANTHROPIC_API_KEY |
| `~/.claude/knowledge-promote.js` | Slack digest, compliance history, adaptive cap, log fix |
| `~/.claude/compliance-history.json` | New file (auto-created by script) |
| `~/Projects/_RPI_STANDARDS/hookify/hookify.intent-immune-system-check.local.md` | New hookify intent rule |
| `~/.claude/CLAUDE.md` | Update Immune System section |
| `~/Projects/_RPI_STANDARDS/CLAUDE.md` | Same updates |
