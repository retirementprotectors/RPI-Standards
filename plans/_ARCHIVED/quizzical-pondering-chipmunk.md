# The Machine's Immune System — _RPI_STANDARDS

## Context

**Problem:** RPI's enforcement system is belt-and-belt, not belt-and-suspenders. 10 of 16 hookify rules duplicate CLAUDE.md content — both are instruction-based markdown the AI reads and hopefully follows (~90% compliance). For compliance-critical rules (PHI, secrets, security access), 90% is not enough. Meanwhile, JDM's intent signals ("ship it", "weekly check", project names) go unrouted, deploys go unverified, and outbound messages go unscanned for PHI.

**Solution:** Graduate The Machine from instruction-based enforcement to a code-enforced immune system using Claude Code hooks across all available event types. One config-driven engine, deterministic enforcement, closed-loop learning.

**What exists today:**
- `~/.claude/hooks/memory-router.sh` — UserPromptSubmit hook (created this session)
- `~/.claude/settings.json` — Hook registration (UserPromptSubmit only)
- `~/.claude/knowledge-promote.js` (1091 lines) — Knowledge pipeline with compliance sweep
- `~/.claude/knowledge-tracker.json` — 86 entries promoted, tracks confidence
- `~/.claude/knowledge-manifest.json` — Routes promotions to correct CLAUDE.md files
- `~/.claude/compliance-sweep.md` — 244 violations across 16 projects
- `~/Projects/_RPI_STANDARDS/hookify/` — 16 .local.md rule files (YAML frontmatter + regex)
- `~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` — Deploys rules to 18 projects
- 4 launchd agents (knowledge-promote 4am, cleanup Sun 3am, analytics 3:30am, mcp-analytics Mon 8am)

---

## The Hierarchy (After Implementation)

```
LAYER 0: HOOKS (settings.json)      <- Code-level. AI cannot ignore.
LAYER 1: CLAUDE.md                   <- The Constitution. Context + why.
LAYER 2: MEMORY.md                   <- The Holding Pen. Auto-captured.
LAYER 3: Knowledge Pipeline          <- Graduates memory -> instructions.
LAYER 4: _RPI_STANDARDS              <- The Library. Procedures + configs.
LAYER 5: Project CLAUDE.md           <- Local rules per project.
LAYER 6: Project Code                <- Where it all gets applied.
```

Knowledge flows UP (sessions -> memory -> CLAUDE.md). Rules flow DOWN (CLAUDE.md -> projects -> code). Hooks enforce ACROSS — intercepting every interaction at the code level.

---

## The 5-Event Architecture

### EVENT 1: UserPromptSubmit — Intent Router

**Script:** `~/.claude/hooks/intent-router.sh`
*(Merges and replaces existing `memory-router.sh` — one script, all routing)*

**Trigger library loaded from:** `~/.claude/hooks/intent-triggers.json` (not hardcoded in bash)

#### TIER 0: Full Workflow Scripts (inject entire multi-step protocols)

| Trigger | Full Workflow Injected |
|---------|----------------------|
| **"session launch"** / **"let's get started"** / **"kick off"** | 1. Review the [project] CLAUDE.md + code/docs. 2. Cleanup recommendations. 3. SOAP analysis (Subjective/Objective/Assessment/Plan) of most valuable next steps with reasoning. 4. Copy plan to Google Doc in default Drive folder (1FwTJ3Id2X88wK20N9g_J3idTI9PL0Zw7). |
| **"post-deployment"** / **"debrief"** / **"wrap it up"** | 1. Review deployment report, make corrections. 2. Full debrief: what we did, where, why, implications, benefits, next steps. 3. Create 3 docs in designated Drive folder (18pzEZmjUVovFGeL4QGX4B8Zrr-p9TU5H): (a) Detailed debrief + what's next, (b) Delegation Guide per team member (Vinnie=Sales ALL, Lucas+Lacy=Medicare, Shaner/Matty/Alex/Arch=Retirement), (c) Testing Guide per format. 4. Confirm documents are available. |

#### TIER 1: Single-Purpose Triggers (inject one directive)

| Category | Triggers | Injects |
|----------|----------|---------|
| **Memory** | "remember this" / "pin it" / "lock it" / "from now on" / "moving forward" / "going forward" / "note this" / "write this down" | Route to CLAUDE.md |
| **Deploy** | "ship it" / "deploy" | Full 6-step deploy protocol + VERIFY |
| **Maintenance** | "weekly check" / "health check" | Full maintenance checklist |
| **Audit** | "audit" / "security audit" / "security check" | Audit protocol |
| **Project** | RIIMO, PRODASH, CAM, C3, DEX, DAVID-HUB, sentinel, QUE, RAPID_API, etc. | "Read that project's CLAUDE.md at [path]" |
| **Outbound** | "slack" / "email" / "message" / "send" | PHI scan reminder |
| **Status** | "status" / "what's going on" | Git status across active projects |
| **Onboard** | "new project" / "setting up" | New project setup protocol |
| **Catchup** | "catch me up" / "what changed" | Git log across recent projects |
| **Emergency** | "hot fix" / "emergency" | Fast-track deploy (still VERIFY) |
| **Cleanup** | "clean up" / "tidy up" | Compliance sweep + fix protocol |
| **Testing** | "test it" / "verify" | DEBUG_ functions + endpoint checks |
| **Revert** | "roll back" / "revert" | Safe revert protocol |
| **Report** | "show me the numbers" / "compliance report" | Latest compliance-sweep.md summary |
| **Domain: CAM** | "commission" / "CAM work" | CAM CLAUDE.md + commission context |
| **Domain: C3** | "campaign" / "C3 work" | C3 CLAUDE.md + CAMPAIGN_MASTER_INDEX.md |
| **Domain: QUE** | "medicare" / "quoting" | QUE-Medicare CLAUDE.md + healthcare tools |
| **Domain: DAVID** | "DAVID" / "B2B" / "partnership" | sentinel-v2 CLAUDE.md + DAVID-HUB |
| **Architecture** | "blueprint" / "architecture" | Project + _RPI_STANDARDS ecosystem context |
| **Meta: New Trigger** | "create a trigger" / "make that a trigger" / "that should be a trigger" / "add a trigger" | Ask JDM: what phrase + what protocol. Write to intent-triggers.json. Confirm saved. Active next session. |

**How it works:**
1. Reads `tool_input.prompt` from stdin JSON
2. Loads `intent-triggers.json` (config-driven, not hardcoded)
3. Pattern-matches against all trigger categories (case-insensitive)
4. For project detection: uses `knowledge-manifest.json` projectKeywords
5. Outputs `additionalContext` with the appropriate directive
6. Multiple triggers can fire on the same prompt (memory + project, etc.)

**Updating the library over time:**
- Add entries to `intent-triggers.json` — no bash code changes needed
- File syncs between machines via git (lives in `~/.claude/hooks/`)
- knowledge-promote.js can SUGGEST new triggers based on session patterns

### EVENT 2: PreToolUse — Compliance Firewall

**Scripts:**
- `~/.claude/hooks/enforce.sh` — Single engine, multi-subsystem
- `~/.claude/hooks/rules.json` — Tier 1 rule definitions

**Matchers:** Two PreToolUse entries in settings.json:
1. `Write|Edit|Bash` — file writes + git/clasp commands
2. `Slack|Gmail|slack_post_message|slack_send_message|send_email|draft_email` — outbound comms via MCP

#### Sub-system A: File Write Enforcement (Write|Edit tools)
Fires on every Write/Edit tool call. Reads `tool_input` (file_path + content/new_string).

| Rule | Action | Exception |
|------|--------|-----------|
| `block-hardcoded-secrets` | BLOCK | None |
| `block-credentials-in-config` | BLOCK | None |
| `block-phi-in-logs` | BLOCK | None |
| `block-anyone-anonymous-access` | BLOCK | RAPID_API appsscript.json (SPARK webhook) |
| `block-hardcoded-matrix-ids` | BLOCK | RAPID_CORE files (definition source) |
| `block-alert-confirm-prompt` | WARN | Comments (lookbehind for `//` or `*`) |

#### Sub-system B: Outbound PHI Scan (MCP tools + Bash)
**Primary:** Fires on MCP Slack/Gmail tool calls (slack_post_message, slack_send_message, send_email, draft_email). Scans `tool_input` (message text, body, etc.) for PHI patterns (SSN, DOB, Medicare ID, beneficiary_id). BLOCKS if found.
**Secondary:** Also fires on Bash commands containing curl/webhook sends with PHI patterns.

#### Sub-system C: Git Push Credential Scan (Bash tool)
Fires on `git push` commands. Quick scan of recent staged changes for credential patterns (API keys, tokens, passwords). WARNS if suspicious.

#### Sub-system D: Clasp Deploy VERIFY Injection (Bash tool)
Fires on `clasp deploy` commands. Injects additionalContext: "After this deploy completes, you MUST run `clasp deployments` and verify the @VERSION number matches."

**Engine mechanics:**
1. Reads JSON from stdin (`tool_name`, `tool_input`)
2. Routes to sub-system based on tool_name + command content
3. Uses `perl` for regex (built into macOS, supports lookbehinds)
4. Logs ALL matches to `~/.claude/hooks/violation-log.jsonl`
5. BLOCK match: `exit 2` + stderr message (tool call prevented)
6. WARN match: `exit 0` + additionalContext JSON on stdout
7. No match: `exit 0` silent
8. Target: <500ms execution

### EVENT 3: PostToolUse — Quality Gates

**Script:** `~/.claude/hooks/quality-gate.sh`
**Matcher:** `Bash|Write|Edit`

| After Tool | Check | Action |
|-----------|-------|--------|
| Bash containing `clasp deploy` | Scan stdout for version confirmation | WARN if output doesn't contain expected @VERSION |
| Bash containing `git commit` in GAS project dir | Check if `.clasp.json` exists in project | WARN: "GAS project — commit + deploy together" |
Quality gates always exit 0 — they warn, never block. Information flows to the AI as additionalContext.

**Dropped from V1:** ForUI serialization check (multi-line function body analysis too complex for bash regex — Tier 2 .local.md handles this adequately).

### EVENT 4: SessionStart (Handled by CLAUDE.md Protocol — No Hook Event)

Claude Code doesn't expose a SessionStart hook event. This layer is already covered by:
- **CLAUDE.md Session Protocol** — read project CLAUDE.md, survey ecosystem, reference detection
- **`~/.claude/setup.sh`** — bootstrap for new machines
- **Intent Router** — detects project names in first prompt and routes accordingly

No new code needed. The instruction-based approach works here because session start is a one-time setup, not a repeated enforcement point.

### EVENT 5: Stop — Knowledge Capture

**Script:** `~/.claude/hooks/session-end.sh`

| Action | What It Does |
|--------|-------------|
| Diff MEMORY.md | Log new entries since session start to `~/.claude/session-capture.log` |
| Detect [LOCKED] entries | Flag entries marked for immediate promotion |
| Log session stats | Append to `~/.claude/session-stats.jsonl` (violations blocked, rules fired, session duration) |

**Session duration tracking:** `enforce.sh` writes a `.session-start` timestamp file on first invocation per session. `session-end.sh` reads it to calculate duration. No SessionStart hook needed.

`knowledge-promote.js` reads `session-stats.jsonl` during daily 4am run to enrich compliance reports with real-time enforcement data.

---

## Tier Classification: All 16 Hookify Rules

### TIER 1 — Code-Enforced (6 rules -> enforce.sh via rules.json)

Criteria: **Failure = compliance violation, security exposure, or data loss**

| Rule | Action | Regex Pattern (from .local.md frontmatter) |
|------|--------|---------------------------------------------|
| `block-hardcoded-secrets` | BLOCK | `(api_key\|apiKey\|API_KEY\|token\|TOKEN\|password\|PASSWORD\|secret\|SECRET\|access_key\|ACCESS_KEY)\s*[:=]\s*['"][A-Za-z0-9_\-]{20,}['"]` |
| `block-credentials-in-config` | BLOCK | `(xoxb-\|xoxp-\|sk-[a-zA-Z0-9]{20,}\|GOCSPX-\|ya29\.)` |
| `block-phi-in-logs` | BLOCK | `(console\.log\|Logger\.log\|console\.error\|console\.warn).*(\bssn\b\|\bSSN\b\|social_security\|socialSecurity\|\bdob\b\|\bDOB\b\|date_of_birth\|dateOfBirth\|medicare_id\|medicareId\|beneficiary_id)` |
| `block-anyone-anonymous-access` | BLOCK | `"access"\s*:\s*"(ANYONE_ANONYMOUS\|ANYONE)"` (file_path must match `appsscript\.json$`) |
| `block-hardcoded-matrix-ids` | BLOCK | Hardcoded spreadsheet ID patterns outside RAPID_CORE |
| `block-alert-confirm-prompt` | WARN | `(?<!\/\/.*)\b(alert\|confirm\|prompt)\s*\(` with comment-awareness |

### TIER 2 — Instruction-Based (10 rules -> stay as .local.md)

Criteria: **Failure = tech debt or code quality issue, not disaster**

| Rule | Why Tier 2 |
|------|-----------|
| `block-drive-url-external` | Produces visible runtime errors (self-correcting) |
| `block-forui-no-json-serialize` | Client-side bugs, debuggable |
| `block-hardcoded-colors` | Theming concern, high false positives |
| `block-let-module-caching` | GAS-specific, not compliance |
| `warn-date-return-no-serialize` | GAS gotcha, not compliance |
| `warn-missing-structured-response` | Pattern consistency |
| `warn-modal-no-flexbox` | UX quality |
| `warn-phi-in-error-message` | Borderline — violation tracker will collect data for future graduation |
| `warn-plain-person-select` | UX quality |
| `warn-inline-pii-data` | Data management practice |

---

## The Closed Loop

```
Session -> AI writes code -> enforce.sh checks it -> violation logged
    -> knowledge-promote reads violations -> compliance report updated
    -> frequently-violated rules get graduated or emphasized
    -> CLAUDE.md adjusted -> next session is smarter
```

Data flows:
1. `enforce.sh` writes to `~/.claude/hooks/violation-log.jsonl` (every blocked/warned action)
2. `session-end.sh` writes to `~/.claude/session-stats.jsonl` (session summary)
3. `knowledge-promote.js` (4am daily) reads both, enriches `compliance-sweep.md`
4. Compliance sweep already scans all 16 projects against all hookify rules
5. **NEW:** "Hot Rules" section surfaces Tier 2 rules with >10 real-time violations/week -> graduation candidates (V1: RECOMMEND only, V2: auto-promote)
6. **NEW:** "Hot Projects" section surfaces projects with >20 violations/week -> audit targets

---

## Files to Create/Modify

### NEW FILES (5)

| File | Purpose |
|------|---------|
| `~/.claude/hooks/rules.json` | Tier 1 rule definitions (6 rules, JSON config with patterns + exceptions) |
| `~/.claude/hooks/intent-triggers.json` | Intent Router trigger library (config-driven, 19 categories, easily updatable) |
| `~/.claude/hooks/enforce.sh` | PreToolUse engine: file write enforcement + PHI scan + credential scan + deploy injection |
| `~/.claude/hooks/quality-gate.sh` | PostToolUse engine: deploy verification + commit/deploy reminder + GAS gotcha detection |
| `~/.claude/hooks/session-end.sh` | Stop hook: MEMORY.md diff + [LOCKED] detection + session stats |

### MODIFIED FILES (5)

| File | Change |
|------|--------|
| `~/.claude/hooks/memory-router.sh` -> `intent-router.sh` | Merge memory routing + add deploy/audit/project triggers |
| `~/.claude/settings.json` | Register all 4 hook events (UserPromptSubmit, PreToolUse, PostToolUse, Stop) |
| `~/.claude/knowledge-promote.js` | Phase 7b: read violation-log.jsonl + session-stats.jsonl, add Hot Rules/Projects. Phase 9: compile + send daily Slack DM report to JDM personal channel |
| `~/Projects/_RPI_STANDARDS/CLAUDE.md` | Add "Enforced by hook" annotations, remove redundant enforcement language |
| `~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` | Add Tier 1/2 headers, mark code-enforced rules |

### settings.json (Final State)

```json
{
  "permissions": { "defaultMode": "bypassPermissions" },
  "skipDangerousModePermissionPrompt": true,
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/intent-router.sh", "timeout": 5 }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/enforce.sh", "timeout": 10 }
        ]
      },
      {
        "matcher": "mcp__slack__slack_post_message|mcp__slack__slack_reply_to_thread|mcp__claude_ai_Slack__slack_send_message|mcp__claude_ai_Slack__slack_send_message_draft|mcp__gmail__send_email|mcp__gmail__draft_email",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/enforce.sh", "timeout": 10 }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/quality-gate.sh", "timeout": 5 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/session-end.sh", "timeout": 10 }
        ]
      }
    ]
  }
}
```

---

## Daily Morning Report (Slack DM to JDM)

**CRITICAL: Send to JDM personal DM, NOT JDM CEO.** JDM CEO is a team-wide memo channel. JDM is the personal DM.

**When:** After knowledge-promote.js completes its 4am daily run (Phase 9, new)
**Where:** Slack DM to JDM personal channel
**How:** knowledge-promote.js sends via Slack Bot Token (same `SLACK_BOT_TOKEN` used by existing mcp-analytics agent in `~/.claude/analytics/`). Falls back to console output if token unavailable.

**Report contents (executive summary):**
1. **What happened overnight** — entries processed, rules scanned, sessions analyzed
2. **What moved UP** — entries promoted to CLAUDE.md (with destinations)
3. **What didn't move** — entries still in holding (with confidence scores)
4. **What got pushed DOWN** — where promoted entries were routed (which project CLAUDE.md, which reference doc)
5. **What got deleted** — stale entries removed (>21 days, never confirmed)
6. **Hot Rules** — which enforcement rules fired most (Tier 2 graduation candidates)
7. **Hot Projects** — which projects had most violations (audit candidates)
8. **Violations blocked** — count of real-time blocks from enforce.sh
9. **Session stats** — sessions captured, total tool calls intercepted

**Format:** Clean, scannable Slack message. Numbers up top, details below. JDM should be able to read it in 60 seconds and know exactly what The Machine did while he slept.

**Future:** Monthly rollup summary (once the daily cadence is dialed in and JDM is confident the system is doing what he wants).

---

## Machine-to-Machine Sync

All hook scripts live in `~/.claude/hooks/`. That directory is inside `~/.claude/`, which is already git-tracked and syncs between machines.

| What | Syncs? | How |
|------|--------|-----|
| `settings.json` | Yes | Git push/pull (existing ~/.claude sync) |
| `rules.json` | Yes | Git push/pull |
| `intent-triggers.json` | Yes | Git push/pull |
| `enforce.sh`, `intent-router.sh`, etc. | Yes | Git push/pull |
| `violation-log.jsonl` | No | Local/ephemeral — each machine has its own |
| `session-stats.jsonl` | No | Local/ephemeral — processed by 4am knowledge-promote |

`setup.sh` gets updated to: create `hooks/` dir if missing, `chmod +x` all `.sh` files in it.

## Session-to-Session Persistence

Hooks are files on disk + settings.json registration. Claude Code reads settings.json fresh on every launch.

- Every new session automatically has all hooks active — zero setup
- `violation-log.jsonl` accumulates across sessions (not wiped between sessions)
- `session-stats.jsonl` accumulates across sessions (one entry per session end)
- `knowledge-promote.js` at 4am processes both logs, truncates processed entries
- `cleanup.sh` (Sunday 3am) prunes old log entries (>7 days)

---

## Build Order

| Phase | What | Files | Parallel? |
|-------|------|-------|-----------|
| 1A | rules.json | `~/.claude/hooks/rules.json` | Yes (with 2A, 2B, 2C) |
| 1B | enforce.sh | `~/.claude/hooks/enforce.sh` | After 1A |
| 2A | intent-router.sh | `~/.claude/hooks/intent-router.sh` | Yes (with 1A, 2B, 2C) |
| 2B | quality-gate.sh | `~/.claude/hooks/quality-gate.sh` | Yes (with 1A, 2A, 2C) |
| 2C | session-end.sh | `~/.claude/hooks/session-end.sh` | Yes (with 1A, 2A, 2B) |
| 3 | settings.json | `~/.claude/settings.json` | After 1B, 2A, 2B, 2C |
| 4 | Verification tests | Synthetic JSON inputs | After 3 |
| 5 | knowledge-promote.js | `~/.claude/knowledge-promote.js` | After 4 (verified) |
| 6 | CLAUDE.md cleanup | `_RPI_STANDARDS/CLAUDE.md` | After 4 (verified) |
| 7 | Hookify .local.md updates | `_RPI_STANDARDS/hookify/*.local.md` | After 4 (verified) |

**Phases 1A + 2A + 2B + 2C build in parallel** (4 agents).
**Phases 6 and 7 happen LAST** — do not remove instruction-based enforcement until code-based enforcement is verified working.

---

## Verification Plan

### enforce.sh Tests (pipe synthetic JSON to stdin)
1. Write with hardcoded secret -> BLOCKED, logged to violation-log.jsonl
2. Write with PHI in console.log -> BLOCKED
3. Write with ANYONE_ANONYMOUS in appsscript.json -> BLOCKED
4. Write with ANYONE_ANONYMOUS in RAPID_API appsscript.json -> PASSES (exception)
5. Write with MATRIX ID outside RAPID_CORE -> BLOCKED
6. Write with MATRIX ID inside RAPID_CORE -> PASSES (exception)
7. Write with alert() in code -> WARNED (not blocked)
8. Write with "alert" in comment -> PASSES (lookbehind)
9. Clean code write -> SILENT PASS
10. All blocked/warned matches -> verify violation-log.jsonl has entries
11. Bash with `git push` + credential in diff -> WARNED
12. Bash with `clasp deploy` -> additionalContext with VERIFY reminder

### intent-router.sh Tests
13. Prompt "remember this for later" -> additionalContext routes to CLAUDE.md
14. Prompt "ship it" -> additionalContext injects deploy protocol
15. Prompt "working on RIIMO today" -> additionalContext injects RIIMO CLAUDE.md path
16. Prompt "security audit" -> additionalContext injects audit protocol
17. Prompt "fix this bug" -> NO output (normal prompt, no routing)

### quality-gate.sh Tests
18. PostToolUse after `clasp deploy` -> WARN about verification
19. PostToolUse after `git commit` in GAS project dir -> WARN about deploy

### session-end.sh Tests
20. Stop event -> session-stats.jsonl gets an entry

### Live Integration Test
21. Restart Claude Code -> write a file with a violation -> confirm block
22. Say "ship it" -> confirm deploy protocol injection
23. End session -> confirm session-stats.jsonl entry

---

## Emergency Escape Hatch

If hooks cause problems mid-session:
- **Quick disable one:** Rename `enforce.sh` to `enforce.sh.disabled`
- **Full disable all:** Remove `hooks` section from `~/.claude/settings.json`
- **Surgical disable:** Comment out specific hook entries in settings.json

Tier 2 .local.md rules continue working independently — they don't depend on settings.json hooks.

---

## What This Does NOT Change

- **CLAUDE.md content stays.** Hooks enforce; CLAUDE.md teaches. Both are needed.
- **Hookify .local.md files stay.** Tier 2 rules remain instruction-based. Tier 1 originals stay as reference.
- **Knowledge pipeline stays.** Adds new data source (violation-log.jsonl) but doesn't change promotion logic.
- **Launchd agents stay.** No new agents needed. knowledge-promote.js gets enhanced, not replaced.
- **Setup/cleanup scripts stay.** setup.sh may get a line to create hooks/ dir if missing.
