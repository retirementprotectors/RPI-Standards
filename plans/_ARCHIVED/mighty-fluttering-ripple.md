# Plan: Activate The Machine's Immune System

## Context

The Immune System hook architecture was designed and built across 2 sprints (~Feb 15-16). The hookify plugin — a full Python enforcement engine — exists at `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/` with:
- 4 hook handlers (PreToolUse, PostToolUse, UserPromptSubmit, Stop)
- Rule engine with regex matching, block/warn support, LRU cache (314 lines)
- Config loader that reads `.local.md` YAML frontmatter rules from project `.claude/` dirs
- 16 Tier 1+2 rules already written and symlinked to all 18 projects

**The problem:** The plugin isn't enabled. `settings.json` has 3 plugins enabled (frontend-design, context7, playwright) but NOT hookify. The entire enforcement layer is built but unplugged.

**Additionally:** CLAUDE.md describes shell scripts (`enforce.sh`, `intent-router.sh`, etc.) that don't exist — the actual implementation is the Python hookify plugin. The docs are wrong. And intent-routing rules (session-start, #SendIt, quality gates) haven't been written yet.

---

## Phase 1: Enable Hookify Plugin

**File:** `~/.claude/settings.json`

Add `"hookify@claude-plugins-official": true` to `enabledPlugins`. This causes Claude Code to read `hooks/hooks.json` in the plugin directory and auto-register the 4 hook events (PreToolUse, PostToolUse, UserPromptSubmit, Stop).

**Requires restart** of Claude Code for plugin registration to take effect.

---

## Phase 2: Add Intent Routing Rules (New `.local.md` Files)

These go in `_RPI_STANDARDS/hookify/` and get symlinked to all projects via setup script.

### 2a. Session-Start Intent
**File:** `hookify.intent-session-start.local.md`
- event: `prompt`
- action: `warn` (injects system message, doesn't block)
- pattern: matches "session launch", "let's get started", "kick off", "new project", "get started"
- Message: Instructs Claude to run session-start protocol (hookify rule sync check, reference detection, project CLAUDE.md read)

### 2b. Deploy Intent (#SendIt)
**File:** `hookify.intent-sendit.local.md`
- event: `prompt`
- action: `warn`
- pattern: matches "#SendIt", "send it", "ship it"
- Message: Instructs Claude to run the 6-step deploy protocol

### 2c. Quality Gate: Post-Deploy Verify
**File:** `hookify.quality-gate-deploy-verify.local.md`
- event: `bash`
- action: `warn`
- pattern: matches `clasp deploy`
- Message: Reminds to VERIFY @version number matches

### 2d. Quality Gate: Commit Without Deploy
**File:** `hookify.quality-gate-commit-remind.local.md`
- event: `bash`
- action: `warn`
- pattern: matches `git commit` on `.gs` or `.html` files (GAS projects)
- Message: Reminds to also deploy (commit + deploy together rule)

---

## Phase 3: Update CLAUDE.md Immune System Section

**File:** `_RPI_STANDARDS/CLAUDE.md`

Replace the current section that references `enforce.sh`, `intent-router.sh`, `quality-gate.sh`, `session-end.sh` (which don't exist) with accurate documentation:

- Hook Events → hookify plugin Python handlers (not shell scripts)
- Tier 1 Rules = `.local.md` files with `action: block` (enforced by hookify rule engine)
- Tier 2 Rules = `.local.md` files with `action: warn`
- Intent Triggers = `.local.md` files with `event: prompt`
- Quality Gates = `.local.md` files with `event: bash` matching deploy/commit commands
- Remove references to `rules.json`, `intent-triggers.json` (not needed — rules are the `.local.md` files themselves)
- Keep Closed Loop description but note violation logging is future work

---

## Phase 4: Update claude-config Repo + Propagate

1. Commit updated `settings.json` (with hookify enabled) to claude-config repo
2. Push to GitHub so AIR machine gets it on next sync
3. Re-run `setup-hookify-symlinks.sh` to propagate new rules to all 18 projects

---

## Phase 5: Verify

1. JDM restarts Claude Code (required for plugin registration)
2. Test Tier 1 block: Try writing `alert('test')` to a `.gs` file — should be BLOCKED
3. Test Tier 2 warn: Try writing a function without `{ success, data }` return — should WARN
4. Test intent routing: JDM types "let's get started" — should inject session-start protocol
5. Test quality gate: Run `clasp deploy` — should remind to VERIFY

---

## Files Modified

| File | Action |
|------|--------|
| `~/.claude/settings.json` | Add hookify to enabledPlugins |
| `_RPI_STANDARDS/hookify/hookify.intent-session-start.local.md` | NEW |
| `_RPI_STANDARDS/hookify/hookify.intent-sendit.local.md` | NEW |
| `_RPI_STANDARDS/hookify/hookify.quality-gate-deploy-verify.local.md` | NEW |
| `_RPI_STANDARDS/hookify/hookify.quality-gate-commit-remind.local.md` | NEW |
| `_RPI_STANDARDS/CLAUDE.md` | Update Immune System section |
| `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` | Already updated (18 projects) |

## Post-Implementation

- `/export` before restart
- Restart Claude Code
- Run verification tests
- Commit + push _RPI_STANDARDS changes
