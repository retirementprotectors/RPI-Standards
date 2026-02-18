# The Machine's Immune System — Hookify

> Complete reference for RPI's code enforcement, session protocol, and learning loop system.
> Last updated: 2026-02-18

---

## Overview

Hookify is a Python-based enforcement engine that intercepts Claude Code at three points in the tool execution lifecycle. It reads `.local.md` rule files, evaluates them against tool input using regex matching with LRU cache, and either **blocks** operations (code never reaches disk) or **warns** (injects guidance while allowing the operation).

**20 rules** live in `_RPI_STANDARDS/hookify/` and are symlinked to all 18 RPI projects via `setup-hookify-symlinks.sh`.

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
├─ Count rules in source: _RPI_STANDARDS/hookify/ → Expected: 20 rules
├─ Spot-check symlinks across key projects
├─ If missing → Run: setup-hookify-symlinks.sh
└─ Report: "20 rules verified across 18 projects"

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

### Tier 1 — Block Rules (10 rules)

PreToolUse file events. `action: block`. Code never reaches disk.

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

### Quality Gates (2 rules)

PreToolUse bash events. `action: block`. Commands are blocked before execution.

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

### Intent Triggers (2 rules)

UserPromptSubmit events. `action: warn`. Injects protocol instructions.

#### 13. `intent-session-start`
- **Triggers:** "let's get started", "session launch", "kick off", "SKODEN"
- **Fires:** Full session-start protocol (hookify check, project CLAUDE.md, reference detection, ecosystem survey)

#### 14. `intent-sendit`
- **Triggers:** "#SendIt", "send it", "ship it"
- **Fires:** Full 6-step deploy protocol

---

### Tier 2 — Warn Rules (6 rules)

PreToolUse file events. `action: warn`. Warns but allows the operation.

#### 15. `warn-date-return-no-serialize`
- **Files:** `.gs`
- **Pattern:** `return\s+.*new\s+Date\s*\(`
- **Warns:** Returning `new Date()` objects that may become NULL on the client
- **Fix:** Wrap with `JSON.parse(JSON.stringify())` in ForUI functions

#### 16. `warn-inline-pii-data`
- **Files:** All
- **Pattern:** Object literals containing PII field names (`dob`, `ssn`, `phone`, `email`, `address`)
- **Warns:** PII embedded directly in source code (committed to git permanently)
- **Fix:** Store bulk data in Drive, load at runtime

#### 17. `warn-missing-structured-response`
- **Files:** `.gs`
- **Pattern:** Functions with `return` but no `success:` field
- **Warns:** Functions not following `{ success: true/false, data/error }` pattern
- **Fix:** Wrap returns in structured response

#### 18. `warn-modal-no-flexbox`
- **Files:** `.html`
- **Pattern:** `.modal-content` without `display: flex`
- **Warns:** Modal buttons may scroll out of view
- **Fix:** Use flexbox scroll pattern (flex column, scrollable body, fixed header/footer)

#### 19. `warn-phi-in-error-message`
- **Files:** All
- **Pattern:** Catch blocks that return/throw/log `error.message` or `error.stack` directly
- **Warns:** Error messages may contain PHI from database queries
- **Fix:** Log server-side, return generic message to client

#### 20. `warn-plain-person-select`
- **Files:** `.html`
- **Pattern:** `<select>` with IDs containing person keywords (`agent`, `owner`, `producer`, `client`, etc.)
- **Warns:** Known-entity person fields should use Smart Lookup type-ahead, not plain dropdowns
- **Fix:** Replace with `buildSmartLookup()`

---

## The Full Deploy Protocol (#SendIt)

**Trigger:** JDM says "#SendIt", "send it", "ship it"
**Enforced by:** `quality-gate-deploy-verify` + `quality-gate-commit-remind`

```
┌──────────────────────────────────────────────────────────────┐
│               DEPLOY PROTOCOL (#SendIt)                       │
│          Triggered by: intent-sendit rule                     │
│          Enforced by: quality-gate-deploy-verify              │
│                        quality-gate-commit-remind             │
└──────────────────────────────────────────────────────────────┘

STEP 1: PRE-FLIGHT CHECK
├─ git status                    → Any uncommitted changes?
├─ git remote -v                 → Correct remote?
└─ If anything wrong → FIX before proceeding. Do NOT deploy dirty.


STEP 2: PUSH CODE TO GAS
├─ NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
├─ Verify output: "Pushed N files"
└─ If error → STOP. Fix the issue. Do not continue.


STEP 3: CREATE VERSION
├─ NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - description"
├─ Note the VERSION NUMBER returned (e.g., "Created version 111")
└─ This number is critical for Step 4


STEP 4: DEPLOY + VERIFY (Atomic — enforced by quality gate)
│
│  ┌─────────────────────────────────────────────────────────┐
│  │  QUALITY GATE: quality-gate-deploy-verify               │
│  │  BLOCKS: clasp deploy without clasp deployments         │
│  │  These MUST be chained in one command                   │
│  └─────────────────────────────────────────────────────────┘
│
├─ NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X" \
│    && NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deployments | grep "@[VERSION]"
│
├─ VERIFY OUTPUT: The @VERSION number MUST match what you just deployed
│   ├─ "@111" appears → Deploy confirmed
│   └─ Old number appears → Deploy FAILED. Fix -V flag. Redeploy.
│
└─ WHY: On 2026-02-14, RAPID_API was stuck at @33 while code was v108.


STEP 5: GIT COMMIT + PUSH
│
│  ┌─────────────────────────────────────────────────────────┐
│  │  QUALITY GATE: quality-gate-commit-remind               │
│  │  BLOCKS: git commit with .gs/.html/.json without        │
│  │  clasp push in the same command chain                   │
│  └─────────────────────────────────────────────────────────┘
│
├─ git add [specific files]
├─ git commit -m "vX.X - description"
└─ git push


STEP 6: DEPLOY REPORT
└─ Output EVERY time:

   | Step              | Result                        |
   |-------------------|-------------------------------|
   | clasp push        | pass/fail                     |
   | clasp version     | vN                            |
   | clasp deploy      | pass/fail                     |
   | VERIFY: @version  | @N confirmed / MISMATCH       |
   | git commit        | [hash]                        |
   | git push          | pass/fail                     |
   | Access: Org only  | pass/fail                     |


THE ENFORCEMENT CHAIN:
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ intent-sendit│────▶│ deploy-verify   │────▶│ commit-remind    │
│ (triggers    │     │ (blocks deploy  │     │ (blocks commit   │
│  protocol)   │     │  without verify)│     │  without deploy) │
└─────────────┘     └─────────────────┘     └──────────────────┘
     INTENT              GATE 1                   GATE 2

Three rules, working together:
- The intent STARTS the protocol
- Gate 1 ENFORCES verification
- Gate 2 ENFORCES deploy-before-commit ordering
```

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
4. When a mistake repeats, JDM says `/hookify` — a new rule is born, symlinked to all 18 projects instantly

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
20 RULES in _RPI_STANDARDS/hookify/
     │
     │ symlinked via setup-hookify-symlinks.sh
     │
     ├──▶ 18 PROJECTS (.claude/ directories)
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
│  (JDM's words)        2 intent rules             │
│                                                  │
│  PreToolUse ──────▶ pretooluse.py               │
│  (before execution)   10 block + 6 warn + 2 gate │
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
~/Projects/_RPI_STANDARDS/hookify/hookify.*.local.md   (20 rules)

# Propagation script
~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh

# Targets (18 projects)
~/Projects/RAPID_TOOLS/{RAPID_CORE,RAPID_IMPORT,RAPID_API,...}/.claude/
~/Projects/PRODASHX_TOOLS/{PRODASHX,QUE-Medicare}/.claude/
~/Projects/SENTINEL_TOOLS/{sentinel,sentinel-v2,DAVID-HUB}/.claude/
~/Projects/_RPI_STANDARDS/.claude/
~/.claude/   (global rules)
```

Edit once in `_RPI_STANDARDS/hookify/`, symlinks propagate instantly to all projects.

---

## Key Technical Decisions (2026-02-18)

1. **Quality gates use PreToolUse block, not PostToolUse warn** — PostToolUse `systemMessage` from plugin hooks doesn't surface in Claude Code. PreToolUse `permissionDecision: deny` is a proven, reliable enforcement mechanism.

2. **Deploy + verify are atomic** — The quality gate forces `clasp deploy` and `clasp deployments` to be chained in a single command. You physically cannot deploy without verifying.

3. **Session-start uses execute_script, not clasp auth** — GAS connectivity is verified via `execute_script` (MCP), not by checking clasp login status. Clasp is only needed for code deployment operations.

4. **All rules use regex with LRU cache** — Compiled regex patterns are cached (max 128) for performance across multiple rule evaluations per tool call.
