> **Part of The Operating System** — the governance layer of The Machine.
> See [OS.md](OS.md) for the full architecture.
> The Immune System enforces standards in real-time and learns from every session.

# The Machine's Immune System — Hookify

> Complete reference for RPI's code enforcement, session protocol, and learning loop system.
> Last updated: 2026-03-19 (OS Audit — toMachina migration refresh)

---

## Overview

Hookify is a Python-based enforcement engine that intercepts Claude Code at three points in the tool execution lifecycle. It reads `.local.md` rule files, evaluates them against tool input using regex matching with LRU cache, and either **blocks** operations (code never reaches disk) or **warns** (injects guidance while allowing the operation).

**34 rules** live in `_RPI_STANDARDS/hookify/` and are symlinked to 8 active projects + `~/.claude/` (global) via `setup-hookify-symlinks.sh`.

**Enforcement hierarchy:** Hookify rules (code-level) > CLAUDE.md (instruction-level) > MEMORY.md > Knowledge Pipeline

---

## The Three-Direction Data Flow

```
USER PROMPT                          TOOL EXECUTION                        TOOL COMPLETION
     │                                    │                                      │
     ▼                                    ▼                                      ▼
┌─────────────────┐              ┌─────────────────┐                ┌─────────────────┐
│ UserPromptSubmit │              │   PreToolUse     │                │  PostToolUse     │
│                  │              │                  │                │                  │
│ "What did JDM    │              │ "What is Claude  │                │ "What did Claude │
│  just say?"      │              │  about to do?"   │                │  just do?"       │
│                  │              │                  │                │                  │
│ Intent detection │              │ Code enforcement │                │ Post-execution   │
│ Session triggers │              │ Pattern blocking │                │ analysis         │
│                  │              │ Security gates   │                │ (future use)     │
│                  │              │ Quality gates    │                │                  │
└────────┬────────┘              └────────┬────────┘                └────────┬────────┘
         │                                │                                  │
         ▼                                ▼                                  ▼
    WARN: Inject                   BLOCK: Deny tool                   WARN: Inject
    system message                 WARN: Inject msg                   system message
    (guide behavior)               (enforce standards)                (future use)
```

**Direction 1 — Inbound (UserPromptSubmit):** Catches JDM's intent before Claude starts working. Pattern-matches phrases like "let's get started" or "#SendIt" and injects protocol instructions.

**Direction 2 — Pre-Execution (PreToolUse):** Intercepts every Write, Edit, and Bash call BEFORE it executes. This is the primary enforcement layer — it blocks bad code from ever hitting disk. All Tier 1 block rules, Tier 2 warn rules, and quality gates live here.

**Direction 3 — Post-Execution (PostToolUse):** Available for future use. Note: PostToolUse `systemMessage` from plugin hooks does not surface as visible system-reminders in Claude Code (discovered 2026-02-18). Quality gates were moved to PreToolUse as blocks for this reason.

---

## The Big Two Session Triggers

Two intent rules fire on JDM's words, not Claude's actions:

### 1. `intent-session-start`

**Triggers on:** "let's get started", "session launch", "kick off", "new project", "SKODEN"

**What it fires:**

```
PHASE 1: HOOKIFY VERIFICATION
├─ Count rules in source: _RPI_STANDARDS/hookify/ → Expected: 34 rules
├─ Spot-check symlinks across key projects
├─ If missing → Run: setup-hookify-symlinks.sh
└─ Report: "34 rules verified across 8 projects + global"

PHASE 2: PROJECT CONTEXT
├─ Read project CLAUDE.md (if exists in CWD)
├─ Check for "## Required References" section → Read listed docs
└─ If GAS project → Verify execute_script connectivity via MCP
    (NEVER ask JDM to check clasp auth — use execute_script yourself)

PHASE 3: REFERENCE DETECTION (Belt & Suspenders)
├─ THE BELT (auto-detection via grep):
│   ├─ MATRIX patterns?      → Read RAPID_CORE/CORE_Database.gs
│   ├─ PHI/HIPAA patterns?   → Read COMPLIANCE_STANDARDS.md
│   ├─ Healthcare API refs?  → Confirm MCP tools loaded
│   └─ Campaign patterns?    → Read CAMPAIGN_MASTER_INDEX.md
├─ THE SUSPENDERS (project declarations):
│   └─ Read docs listed in project CLAUDE.md "Required References"
└─ Report what docs were loaded

PHASE 4: ECOSYSTEM SURVEY
├─ Check parent directory for sibling projects
├─ Inventory loaded MCP tools
└─ Note shared dependencies and available infrastructure

PHASE 5: EXECUTE
└─ Begin work. Report completion, not progress.
```

### 2. `intent-sendit`

**Triggers on:** "#SendIt", "send it", "ship it"

**What it fires:** The full 6-step deploy protocol (see Deploy Protocol section below).

---

## The Trigger Library: Code Enforcement

### Tier 1 — Block Rules (16 rules)

PreToolUse file/prompt/bash events. `action: block`. Code never reaches disk or operation is denied.

#### 1. `block-alert-confirm-prompt`
- **Files:** `.gs`, `.html`
- **Pattern:** `(alert|confirm|prompt)\s*\(`
- **Catches:** `alert()`, `confirm()`, `prompt()` calls
- **Fix:** Use `showToast()` for notifications, `showConfirmation()` for confirmations

#### 2. `block-anyone-anonymous-access`
- **Files:** `appsscript.json`
- **Pattern:** `"access"\s*:\s*"(ANYONE_ANONYMOUS|ANYONE)"`
- **Catches:** Public web app access settings
- **Fix:** Set `"access": "DOMAIN"` for organization-only access

#### 3. `block-credentials-in-config`
- **Files:** `.gs`, `.json`, `.js`
- **Pattern:** Slack tokens (`xoxb-`, `xoxp-`), webhook URLs, API keys (`sk-*`)
- **Catches:** Plaintext credentials in source files
- **Fix:** Use Script Properties (`PropertiesService.getScriptProperties()`) or environment variables

#### 4. `block-drive-url-external`
- **Files:** All
- **Pattern:** `(UrlFetchApp\.fetch|fetch\s*\(|axios|request).*drive\.google\.com`
- **Catches:** Google Drive URLs passed to external services/fetch calls
- **Fix:** Fetch with Apps Script auth, send as base64

#### 5. `block-forui-no-json-serialize`
- **Files:** `.gs`
- **Pattern:** `function\s+\w+ForUI\s*\(` without `JSON.parse(JSON.stringify`
- **Catches:** `*ForUI()` functions missing serialization
- **Fix:** Wrap return value with `JSON.parse(JSON.stringify(result))`

#### 6. `block-hardcoded-colors`
- **Files:** `.gs`, `.html`
- **Pattern:** Hex codes (`#FF0000`), `rgb()`, `rgba()` not inside CSS variables
- **Catches:** Inline color values
- **Fix:** Use CSS variables (`var(--color-primary)`) or utility classes (`bg-primary`)

#### 7. `block-hardcoded-matrix-ids`
- **Files:** All except RAPID_CORE
- **Pattern:** Known MATRIX spreadsheet IDs (RAPID, SENTINEL, PRODASHX)
- **Catches:** Hardcoded spreadsheet IDs outside the single source of truth
- **Fix:** Use `RAPID_CORE.getMATRIX_ID('PRODASHX')` or Script Properties fallback

#### 8. `block-hardcoded-secrets`
- **Files:** All
- **Pattern:** `(api_key|apiKey|token|password|secret|access_key)\s*[:=]\s*['"][A-Za-z0-9_\-]{20,}['"]`
- **Catches:** Hardcoded API keys, tokens, passwords, secrets (20+ character strings)
- **Fix:** Use Script Properties

#### 9. `block-let-module-caching`
- **Files:** `.gs`
- **Pattern:** `(let|const)\s+_\w*(cache|Cache|data|Data|config|Config)\w*\s*=`
- **Catches:** `let`/`const` for module-level cache variables
- **Fix:** Use `var` — `let`/`const` don't persist between GAS function calls

#### 10. `block-phi-in-logs`
- **Files:** All
- **Pattern:** `(console\.log|Logger\.log)` combined with PHI fields (`ssn`, `dob`, `medicare_id`, etc.)
- **Catches:** Protected Health Information in log statements
- **Fix:** Remove PHI from logs. Use masked values for debugging.

---

### Quality Gates (6 rules)

PreToolUse bash/prompt events. `action: block` or `action: warn`. Enforce process discipline.

#### 11. `quality-gate-deploy-verify`
- **Blocks:** `clasp deploy -[args]` WITHOUT `clasp deployments` in the same command
- **Requires:** Deploy and verify as one atomic operation
- **Why:** On 2026-02-14, RAPID_API was stuck at @33 while code was at v108 — nobody verified

```bash
# BLOCKED — deploy without verify
clasp deploy -i [ID] -V [VERSION] -d "vX.X"

# ALLOWED — deploy with chained verify
clasp deploy -i [ID] -V [VERSION] -d "vX.X" && clasp deployments | grep "@[VERSION]"
```

#### 12. `quality-gate-commit-remind`
- **Blocks:** `git commit` with GAS file extensions (`.gs`, `.html`, `.json`) WITHOUT `clasp push` in the command chain
- **Requires:** Deploy before commit
- **Why:** Never commit without deploying. Never deploy without committing.

---

### Intent Triggers (6 rules)

UserPromptSubmit events. `action: warn`. Injects protocol instructions.

#### 13. `intent-session-start`
- **Triggers:** "let's get started", "session launch", "kick off", "SKODEN"
- **Fires:** Full session-start protocol (hookify check, project CLAUDE.md, reference detection, ecosystem survey)

#### 14. `intent-sendit`
- **Triggers:** "#SendIt", "send it", "ship it"
- **Fires:** Full 6-step deploy protocol

#### 15. `intent-immune-system-check`
- **Triggers:** "check the immune system", "immune system", "compliance check"
- **Fires:** Structured Immune System briefing (pipeline + compliance + trends)

---

### Tier 2 — Warn Rules (6 rules)

PreToolUse file events. `action: warn`. Warns but allows the operation.

> Note: 6 additional rules exist that are not listed individually below (block-generated-logos, block-bulk-import-without-atlas, block-direct-firestore-write, block-seed-without-snapshot, quality-gate-plan-format, quality-gate-audit-verify). See `_RPI_STANDARDS/hookify/` for the complete set. Total: 34 rules.

#### 16. `warn-date-return-no-serialize`
- **Files:** `.gs`
- **Pattern:** `return\s+.*new\s+Date\s*\(`
- **Warns:** Returning `new Date()` objects that may become NULL on the client
- **Fix:** Wrap with `JSON.parse(JSON.stringify())` in ForUI functions

#### 17. `warn-inline-pii-data`
- **Files:** All
- **Pattern:** Object literals containing PII field names (`dob`, `ssn`, `phone`, `email`, `address`)
- **Warns:** PII embedded directly in source code (committed to git permanently)
- **Fix:** Store bulk data in Drive, load at runtime

#### 18. `warn-missing-structured-response`
- **Files:** `.gs`
- **Pattern:** Functions with `return` but no `success:` field
- **Warns:** Functions not following `{ success: true/false, data/error }` pattern
- **Fix:** Wrap returns in structured response

#### 19. `warn-modal-no-flexbox`
- **Files:** `.html`
- **Pattern:** `.modal-content` without `display: flex`
- **Warns:** Modal buttons may scroll out of view
- **Fix:** Use flexbox scroll pattern (flex column, scrollable body, fixed header/footer)

#### 20. `warn-phi-in-error-message`
- **Files:** All
- **Pattern:** Catch blocks that return/throw/log `error.message` or `error.stack` directly
- **Warns:** Error messages may contain PHI from database queries
- **Fix:** Log server-side, return generic message to client

#### 21. `warn-plain-person-select`
- **Files:** `.html`
- **Pattern:** `<select>` with IDs containing person keywords (`agent`, `owner`, `producer`, `client`, etc.)
- **Warns:** Known-entity person fields should use Smart Lookup type-ahead, not plain dropdowns
- **Fix:** Replace with `buildSmartLookup()`

---

## The Full Deploy Protocol (#SendIt)

**Trigger:** JDM says "#SendIt", "send it", "ship it"
**Enforced by:** `intent-sendit` + `quality-gate-deploy-verify` + `quality-gate-commit-remind` + `quality-gate-build-verify`

### toMachina Deploy (Primary)

```
┌──────────────────────────────────────────────────────────────┐
│               DEPLOY PROTOCOL (#SendIt)                       │
│          Triggered by: intent-sendit rule                     │
│          Enforced by: quality-gate-deploy-verify              │
│                        quality-gate-commit-remind             │
│                        quality-gate-build-verify              │
└──────────────────────────────────────────────────────────────┘

STEP 1: PRE-FLIGHT CHECK
├─ git status                    → Working tree clean?
├─ npm run build                 → All workspaces pass? (NOT just type-check)
└─ If anything wrong → FIX before proceeding. Do NOT deploy dirty.


STEP 2: GIT COMMIT
├─ git add [specific files]
├─ git commit -m "description"
└─ Do NOT push yet — verify build first


STEP 3: BRANCH + PR (Branch protection is ON — direct push to main is blocked)
├─ git push origin [branch-name]
├─ gh pr create --title "description" --body "summary"
└─ This triggers CI / check job on the PR


STEP 4: CI GATE (Required — cannot merge without green)
├─ CI / check job: type-check + build (MUST pass to merge)
├─ Watch: gh pr checks [PR-NUMBER] --repo retirementprotectors/toMachina
└─ If failed → fix, push to same branch, CI re-runs automatically


STEP 5: MERGE + DEPLOY
├─ gh pr merge --squash (merges to main)
├─ Merge triggers: CI / deploy-api (Docker + Cloud Run) + Firebase App Hosting (portals)
└─ Watch: gh run list --repo retirementprotectors/toMachina --limit 1


STEP 6: DEPLOY REPORT
└─ Output EVERY time:

   | Step              | Result                        |
   |-------------------|-------------------------------|
   | npm run build     | pass/fail                     |
   | git commit        | [hash]                        |
   | PR created        | [URL]                         |
   | CI / check        | pass/fail (must pass to merge) |
   | PR merged         | [merge hash]                  |
   | CI / deploy-api   | pass/fail                     |
   | Firebase Hosting  | auto-deploy (portals)         |


THE ENFORCEMENT CHAIN:
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ intent-sendit│────▶│ build-verify    │────▶│ deploy-verify    │────▶│ commit-remind    │
│ (triggers    │     │ (blocks without │     │ (warns before    │     │ (warns before    │
│  protocol)   │     │  npm run build) │     │  git push)       │     │  git commit)     │
└─────────────┘     └─────────────────┘     └──────────────────┘     └──────────────────┘
     INTENT              GATE 1                   GATE 2                   GATE 3
```

### GAS Deploy (Maintenance Only — 3 remaining engines)

For rare GAS maintenance deploys (RAPID_CORE, RAPID_IMPORT, DEX):
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
git add -A && git commit -m "description"
git push
```
GAS projects no longer need version/deploy steps unless the web app endpoint changes.

---

## Knowledge Capture

The system captures institutional knowledge at multiple levels:

```
HOOKIFY RULES        → Code-level enforcement (blocks bad patterns in real-time)
     ↑
CLAUDE.md            → Instruction-level guidance (session context, standards, protocols)
     ↑
MEMORY.md            → Experience-level learning (patterns confirmed across sessions)
     ↑
SESSION TRANSCRIPTS  → Raw signal (everything that happened)
```

**Enforcement hierarchy:** Hookify rules > CLAUDE.md > MEMORY.md > Session transcripts

When something goes wrong in a session, the fix flows upward:
1. **Immediate:** Fix the code, fix the data
2. **Session:** Note it in MEMORY.md if it's a pattern
3. **Permanent:** If it keeps happening, write a hookify rule to prevent it forever

---

## The Learning Loop

The closed-loop system that makes The Machine smarter over time:

```
SESSION                                                          NEXT SESSION
  │                                                                   ▲
  │  Claude makes mistakes                                            │
  │  Hookify catches violations                                       │
  │  JDM corrects behaviors                                           │
  ▼                                                                   │
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐     │
│   Session     │───▶│  knowledge-      │───▶│  CLAUDE.md /     │─────┘
│   Transcript  │    │  promote.js      │    │  MEMORY.md       │
│               │    │  (daily 4:00am)  │    │  updated         │
└──────────────┘    └──────────────────┘    └──────────────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Slack DM to JDM │
                    │  (weekly report) │
                    └──────────────────┘
```

**How it works:**
1. Sessions generate transcripts (violations, corrections, patterns)
2. `knowledge-promote.js` runs daily at 4:00am — scans for promotable learnings, routes to MEMORY.md or CLAUDE.md with section-aware insertion
3. `mcp-analytics` runs Monday 8am — weekly Slack report to JDM on system health
4. When a mistake repeats, JDM says `/hookify` — a new rule is born, symlinked to all 8 projects + global instantly

**The flywheel:**
```
Mistake happens → Gets caught → Rule written → Mistake impossible
                                                      │
                                    Next mistake  ◀────┘
                                    (different one)
```

Every session makes the immune system stronger. Every rule eliminates an entire category of error permanently. The system doesn't just remember — it **enforces**.

---

## System Architecture

```
34 RULES in _RPI_STANDARDS/hookify/
     │
     │ symlinked via setup-hookify-symlinks.sh
     │
     ├──▶ 8 PROJECTS (.claude/ directories)
     │    + ~/.claude/ (global rules)
     │         │
     │         │ loaded at runtime by config_loader.py
     │         │
     │         ▼
     │    ┌─────────────────────────────────┐
     │    │         RULE ENGINE             │
     │    │   (rule_engine.py + LRU cache)  │
     │    └──────────┬──────────────────────┘
     │               │
     │    ┌──────────┴──────────────────────┐
     │    │                                 │
     │    ▼                                 ▼
     │  BLOCK                             WARN
     │  permissionDecision: deny          systemMessage injection
     │  (hard stop — code blocked)        (guidance — operation allowed)
     │
     ▼
┌─────────────────────────────────────────────────┐
│               HOOK ENTRY POINTS                  │
│                                                  │
│  UserPromptSubmit ──▶ userpromptsubmit.py       │
│  (JDM's words)        6 intent rules             │
│                                                  │
│  PreToolUse ──────▶ pretooluse.py               │
│  (before execution)   16 block + 6 warn + 6 gate │
│                                                  │
│  PostToolUse ─────▶ posttooluse.py              │
│  (after execution)    available for future use    │
│                                                  │
│  Stop ────────────▶ stop.py                     │
│  (session end)        future: violation summary   │
└─────────────────────────────────────────────────┘
```

---

## Rule File Format

Every rule is a single `.local.md` file:

```markdown
---
name: rule-name
enabled: true
event: file|bash|prompt
action: block|warn
conditions:
  - field: command|content|file_path|user_prompt
    operator: regex_match|contains|not_contains|equals
    pattern: your-regex-here
---

**Message shown when rule triggers**

Explanation, fix instructions, context.
```

One file to read, one file to edit, one file to disable. No compilation, no build step — change the file, it's live next tool call.

---

## Emergency Escape Hatch

- **Disable all hookify:** Remove `"hookify@claude-plugins-official": true` from `~/.claude/settings.json`
- **Disable one rule:** Set `enabled: false` in the rule's YAML frontmatter, or delete the symlink
- **Rules only apply** in projects where `.claude/hookify.*.local.md` symlinks exist

---

## Rule Propagation

Rules are centrally managed and propagated:

```bash
# Source of truth
~/Projects/_RPI_STANDARDS/hookify/hookify.*.local.md   (34 rules)

# Propagation script
~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh

# Targets (8 projects + global)
~/Projects/toMachina/.claude/                    # THE PLATFORM (monorepo)
~/Projects/gas/RAPID_CORE/.claude/               # GAS — Sheets adapter
~/Projects/gas/RAPID_IMPORT/.claude/             # GAS — Data ingestion
~/Projects/gas/DEX/.claude/                      # GAS — PDF/Drive ops
~/Projects/services/MCP-Hub/.claude/             # MCP intelligence layer
~/Projects/services/PDF_SERVICE/.claude/         # PDF processing
~/Projects/services/Marketing-Hub/.claude/       # Marketing automation
~/Projects/_RPI_STANDARDS/.claude/               # Standards + governance
~/.claude/   (global rules — always active)
```

Edit once in `_RPI_STANDARDS/hookify/`, symlinks propagate instantly to all projects.

---

## Key Technical Decisions (2026-02-18)

1. **Quality gates use PreToolUse block, not PostToolUse warn** — PostToolUse `systemMessage` from plugin hooks doesn't surface in Claude Code. PreToolUse `permissionDecision: deny` is a proven, reliable enforcement mechanism.

2. **Deploy + verify are atomic** — The quality gate forces `clasp deploy` and `clasp deployments` to be chained in a single command. You physically cannot deploy without verifying.

3. **Session-start uses execute_script, not clasp auth** — GAS connectivity is verified via `execute_script` (MCP), not by checking clasp login status. Clasp is only needed for code deployment operations.

4. **All rules use regex with LRU cache** — Compiled regex patterns are cached (max 128) for performance across multiple rule evaluations per tool call.

---

## Related OS Documents

| Document | Relationship |
|----------|-------------|
| [OS.md](OS.md) | Master architecture — how all 5 subsystems connect |
| [STANDARDS.md](STANDARDS.md) | The rules this system enforces |
| [POSTURE.md](POSTURE.md) | Access control state verified by compliance triggers |
| [MONITORING.md](MONITORING.md) | Scheduled checks that complement real-time enforcement |
| [OPERATIONS.md](OPERATIONS.md) | Human processes triggered by enforcement findings |
