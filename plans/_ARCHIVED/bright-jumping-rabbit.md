# Plan: Knowledge Machine v2 — Full Cascade + Compliance Sweep

## Context

v1 of the Knowledge Machine is LIVE and working (sessions → MEMORY.md → CLAUDE.md promotion). The bootstrap proved the concept but exposed 5 gaps:

1. **EOF append** — entries got dumped at bottom of files with `<!-- Promoted -->` comments instead of integrated into proper sections. Required manual cleanup of 9 files.
2. **No reference doc routing** — manifest has `globalProcedures` map to 5 reference docs but v1 never uses it. Everything goes to CLAUDE.md or project CLAUDE.md.
3. **No compliance sweep** — new rules protect future code but don't retroactively find violations in existing codebases.
4. **Misroutes + duplicates** — C3 got a .gitignore fact, temporal data got promoted, entries duplicated within files.
5. **Wrong schedule** — 11:15pm runs in the MIDDLE of JDM's typical work shift.

**The full knowledge cascade v2 enables:**
```
Sessions (both machines)
  → MEMORY.md (auto-memory captures)
    → CLAUDE.md (rules promoted, section-aware)
      → _RPI_STANDARDS/reference/ (procedures routed correctly)
        → Project CLAUDE.md (project-specific rules)
          → Compliance sweep report (violations found in existing code)
```

---

## What Changes

### File: `~/.claude/knowledge-promote.js` (~674 → ~985 lines)

**6 surgical changes, no architecture rewrite:**

### Change 1: Fix AI JSON Parsing (root cause of all v1 failures)

Haiku wraps JSON in markdown fences (` ```json...``` `). v1 does raw `JSON.parse()` which fails. Add `stripMarkdownFences()` before parsing.

```javascript
function stripMarkdownFences(text) {
  if (!text) return text;
  const fenceMatch = text.match(/```(?:json)?\s*\n?([\s\S]*?)```/);
  return fenceMatch ? fenceMatch[1].trim() : text.trim();
}
```

Wire into `callHaiku()` return path. This unblocks ALL AI features.

### Change 2: Fix Duplicate Detection

Replace 50-char prefix check with normalized full-text comparison + Jaccard word-set similarity (>60% overlap). Also check tracker's `promotedTo` field to prevent re-promoting.

```javascript
function normalizeForComparison(text) {
  return text.replace(/\*\*/g, '').replace(/`/g, '')
    .replace(/[^a-zA-Z0-9\s]/g, '').toLowerCase()
    .replace(/\s+/g, ' ').trim();
}
```

### Change 3: Add Temporal Data Filter

Prevent version numbers, status snapshots, and dated entries from being promoted:

```javascript
const temporalPatterns = [
  /^(RAPID_CORE|RAPID_API|RIIMO|...):\s*v\d+/i,
  /Phase \d.*COMPLETE/i,
  /\d+ (client )?dupes/i,
  /NOT YET SYNCED/i
];
```

Entries matching → `status: 'temporal-skipped'` in tracker, never promoted.

### Change 4: AI-Powered Section-Aware Insertion

Replace the v1 write path (regex section finder + EOF fallback) with:

1. Extract section headers from destination file as table of contents
2. Send to Haiku: "Here are the sections, here's the entry — which section, what line, what format?"
3. AI returns: `{ insertAfterLine, formattedContent, sectionName }`
4. Sanity checks: valid line number, not inside code block
5. Fallback to v1 logic (without `<!-- Promoted -->` comments) if AI fails

**AI system prompt** tells Haiku to match the formatting style of the target section (bullets, tables, etc.) and insert among similar entries.

### Change 5: Reference Doc Routing

Enhanced `classifyWithAI()` prompt includes `procedureCategory` field:
- `compliance` → COMPLIANCE_STANDARDS.md
- `security` → SECURITY_COMPLIANCE.md
- `integrations` → GHL_INTEGRATION.md
- `patterns` → SMART_LOOKUP.md
- `maintenance` → WEEKLY_HEALTH_CHECK.md

Enhanced `resolveFilePath()` uses the category to pick the right reference doc from `manifest.globalProcedures`.

### Change 6: Compliance Sweep (NEW)

After promoting rule entries, for each newly promoted RULE:

1. **AI generates a grep pattern** from the rule text (e.g., "empty string indexOf" → `\.indexOf\(\s*\)`)
2. **Scan projects** — global rules scan all 16 projects; project-specific rules scan only that project
3. **Report** written to `~/.claude/compliance-sweep.md` with violation table (file, line, content)

Also adds `--sweep-only` mode that loads all 16 hookify rules and scans all projects without running the promotion pipeline. Useful for on-demand compliance checking.

**Does NOT auto-fix** — too risky for unattended nightly run. Reports violations for next session to address.

---

### Schedule Change: `com.rpi.knowledge-promote` plist

Move from 11:15pm → **4:00am daily**.

Rationale: 11:15pm is mid-shift for JDM. 4am is after sessions end, before new ones start. The cleanup already runs at 3am Sunday — 4am daily fits the same "off-hours maintenance" window.

Also move `com.rpi.analytics-push` from 11pm → **3:30am daily** (same reasoning — analytics should aggregate after the work day, not during it).

**Update on BOTH machines** (Air + Pro plist files in ~/Library/LaunchAgents/).

---

## What v2 Does NOT Do (and why)

**Auto-cascade writes** (copying rules from CLAUDE.md into every project CLAUDE.md): Not appropriate for unattended nightly automation. When a rule goes into global CLAUDE.md, every session on every project already reads it. Project CLAUDE.md files only need project-SPECIFIC rules, which the promotion engine already handles via its routing logic.

**Auto-fix violations**: The compliance sweep REPORTS violations but does not modify code. Fixing code in an unattended nightly job without review is too risky. The sweep report feeds the next session — Claude Code reads it and can fix violations when JDM is present.

---

## Implementation Sequence

| Step | What | Lines |
|------|------|-------|
| 1 | `stripMarkdownFences()` + wire into `callHaiku()` | +6 |
| 2 | `normalizeForComparison()` + replace `findTrackerMatch()` | +15 |
| 3 | `isTemporalData()` + wire into `classifyEntry()` | +15 |
| 4 | Enhanced `classifyWithAI()` prompt (procedure categories, no fences instruction) | +15 |
| 5 | Enhanced `resolveFilePath()` for reference doc routing | +8 |
| 6 | `applyPromotionV2()` + AI insertion prompt + fallback function | +80 |
| 7 | `extractScanPattern()` + `scanProjectForPattern()` + `runComplianceSweep()` + `writeSweepReport()` | +135 |
| 8 | `loadHookifyRules()` + `--sweep-only` mode + wire into main() | +55 |
| 9 | Update launchd schedules (both machines) | plist edits |
| 10 | Test: `--dry-run`, `--sweep-only`, controlled `--apply` | verification |
| 11 | Commit + push | git |

**Estimated total: ~985 lines (under 1000-line target)**
**AI calls per daily run: 2-7 (well under $0.05/day)**

---

## Verification

```bash
# 1. Dry run — check temporal filter, AI parsing, routing
node ~/.claude/knowledge-promote.js --dry-run

# 2. Sweep-only — scan all 16 projects against all 16 hookify rules
node ~/.claude/knowledge-promote.js --sweep-only
cat ~/.claude/compliance-sweep.md

# 3. Controlled apply — add test entry to MEMORY.md with 3+ sessions, run
node ~/.claude/knowledge-promote.js --apply
# Verify: entry lands in correct section, no EOF append, no duplicates

# 4. launchd verification
launchctl list | grep rpi
# Confirm knowledge-promote shows next fire at 4:00am
```

---

## Critical Files

| File | Action |
|------|--------|
| `~/.claude/knowledge-promote.js` | All code changes (Steps 1-8) |
| `~/.claude/compliance-sweep.md` | NEW — generated sweep report |
| `~/Library/LaunchAgents/com.rpi.knowledge-promote.plist` | Schedule → 4:00am |
| `~/Library/LaunchAgents/com.rpi.analytics-push.plist` | Schedule → 3:30am |
| `~/.claude/launchd/com.rpi.knowledge-promote.plist` | Template updated |
| `~/.claude/launchd/com.rpi.analytics-push.plist` | Template updated |
| `~/.claude/knowledge-manifest.json` | Read-only (already has globalProcedures) |
| `~/.claude/knowledge-tracker.json` | Compatible — new `temporal-skipped` status added |
| `_RPI_STANDARDS/hookify/*.local.md` | Read-only (loaded by --sweep-only) |
