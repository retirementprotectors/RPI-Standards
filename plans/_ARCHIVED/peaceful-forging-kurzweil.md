# The Machine's Operating System: Hooks as Layer 0

## Context

RPI has built a layered system for enforcing standards, capturing knowledge, and maintaining code quality across 16+ GAS projects. But there's a gap: **everything below Layer 0 is instruction-based** — it works because the AI reads rules and follows them. Hooks are the first layer that's **code-level and deterministic**. The AI doesn't get a choice.

This plan upgrades "hookify" from markdown instructions into real Claude Code hooks, and establishes the complete hierarchy of tools — from the most powerful (hooks) down to the least (project code).

---

## The Hierarchy (Top = Most Powerful)

```
LAYER 0: HOOKS — Code-level. Deterministic. Cannot be ignored.
    │
    │  settings.json hooks fire on events:
    │  UserPromptSubmit, PreToolUse, PostToolUse,
    │  SessionStart, SessionEnd, Stop
    │
    │  Three hook types available:
    │  • command (shell script) — fast, deterministic
    │  • prompt (Haiku yes/no) — AI judgment, cheap
    │  • agent (subagent with tools) — full verification
    │
LAYER 1: GLOBAL CLAUDE.md — The Constitution
    │
    │  ~/.claude/CLAUDE.md → _RPI_STANDARDS/CLAUDE.md
    │  Loaded every session. Business context, golden rules,
    │  process, architecture. NO code enforcement (moved to L0).
    │
LAYER 2: MEMORY.md — The Holding Pen
    │
    │  Auto-captured session knowledge.
    │  [LOCKED] entries fast-tracked.
    │  Feeds into knowledge pipeline.
    │
LAYER 3: KNOWLEDGE PIPELINE — The Graduation System
    │
    │  knowledge-promote.js (daily 4am)
    │  3-session threshold (auto) / immediate ([LOCKED])
    │  Routes entries → appropriate CLAUDE.md or reference doc
    │
LAYER 4: _RPI_STANDARDS — The Library
    │
    │  reference/ (procedures), scripts/ (automation)
    │  hookify/ → becomes hook engine configs (not .local.md)
    │  Central source of truth for all standards
    │
LAYER 5: PROJECT CLAUDE.md — Local Rules
    │
    │  Project-specific context, deploy IDs, gotchas.
    │  Can declare project-specific hook overrides.
    │
LAYER 6: PROJECT CODE — Where Rules Get Applied
```

**Key principle:** Each layer is MORE powerful than the one below it. Hooks override instructions. Instructions override memory. The pipeline graduates memory into instructions. It's a closed loop.

---

## What Changes

### Hookify Rules: Markdown → Real Hooks

**Current (instruction-based, ~90% reliable):**
```
_RPI_STANDARDS/hookify/hookify.block-phi-in-logs.local.md
  → symlinked to each project's .claude/
  → AI reads it and (hopefully) follows it
```

**New (code-level, 100% reliable):**
```
_RPI_STANDARDS/hookify/rules/block-phi-in-logs.json
  → loaded by hook engine script
  → fires on PreToolUse for Write|Edit
  → pattern-matches file content
  → BLOCKS the tool call (exit 2) before write happens
```

### CLAUDE.md: Remove Duplicate Enforcement

The 10+ code enforcement rules currently duplicated in CLAUDE.md get REMOVED from CLAUDE.md once they're real hooks. CLAUDE.md goes back to being context, process, and architecture — not enforcement.

### New Hooks (Beyond Existing 16)

| Hook | Event | Type | What It Does |
|------|-------|------|---|
| **Memory Router** | UserPromptSubmit | command | Detects "remember/memory/moving forward/from now on" → injects "write to CLAUDE.md, not MEMORY.md" |
| **Ship It Protocol** | UserPromptSubmit | command | Detects "ship it" → injects full 6-step deploy checklist |
| **Project Context Loader** | UserPromptSubmit | command | Detects project names → injects "read that project's CLAUDE.md" |
| **PHI Outbound Firewall** | PreToolUse | command | On Slack/Email sends → scans for SSN/DOB/Medicare ID patterns → BLOCKS |
| **Deploy Verifier** | PostToolUse | command | After `clasp deploy` → auto-checks version number matches |
| **Commit+Deploy Gate** | PostToolUse | prompt | After git commit on GAS project → Haiku asks "did you also deploy?" |
| **Destructive Action Gate** | PreToolUse | command | On `git push --force`, `rm -rf` → BLOCKS with warning |
| **Compact Context Reinject** | SessionStart (compact) | command | After context compaction → reinjects critical rules |

---

## Hook Engine Architecture

### Single Entry Point

One shell script handles ALL PreToolUse enforcement:

```
~/.claude/hooks/hook-engine.sh
```

This script:
1. Reads tool input from stdin (JSON)
2. Determines which tool is being called (Write, Edit, Bash, Slack, etc.)
3. Loads applicable rules from the config directory
4. Pattern-matches content against each rule
5. Returns block/warn/allow

### Config-Driven Rules

Each rule is a JSON file in:

```
_RPI_STANDARDS/hookify/rules/
├── block-alert-confirm-prompt.json
├── block-phi-in-logs.json
├── block-anyone-anonymous-access.json
├── ... (16 existing + new rules)
└── warn-plain-person-select.json
```

Example rule format:
```json
{
  "id": "block-phi-in-logs",
  "action": "block",
  "description": "PHI fields in console/Logger statements",
  "fileTypes": [".gs", ".js"],
  "pattern": "(console\\.log|Logger\\.log).*\\b(ssn|SSN|dob|DOB|medicare_id)\\b",
  "message": "BLOCKED: PHI detected in log statement. Use masked values or record IDs."
}
```

### settings.json Structure

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/sync.sh pull" }] },
      { "matcher": "compact",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/reinject-context.sh" }] }
    ],
    "SessionEnd": [
      { "hooks": [{ "type": "command", "command": "bash $HOME/.claude/sync.sh push" }] }
    ],
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/intent-router.sh" }] }
    ],
    "PreToolUse": [
      { "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/hook-engine.sh" }] },
      { "matcher": "mcp__slack__.*|mcp__gmail__.*|mcp__claude_ai_Slack__.*",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/phi-firewall.sh" }] },
      { "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/destructive-gate.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "bash $HOME/.claude/hooks/deploy-verifier.sh" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "prompt", "prompt": "Check if the agent completed all requested tasks. If there are uncommitted changes on a GAS project, remind to deploy." }] }
    ]
  }
}
```

---

## Implementation Phases

### Phase 1: Hook Engine Core (Day 1)
- Build `hook-engine.sh` — reads rules from JSON, pattern-matches, blocks/warns
- Convert all 16 hookify `.local.md` rules to `.json` format
- Test with 2-3 critical rules (PHI in logs, alert/confirm, hardcoded secrets)
- Wire into settings.json as PreToolUse on Write|Edit

### Phase 2: Intent Router (Day 1)
- Build `intent-router.sh` — UserPromptSubmit hook
- Detect: "remember/memory/moving forward/from now on" → inject CLAUDE.md redirect
- Detect: "ship it" → inject deploy protocol
- Detect: project names → inject context reminder
- Update knowledge-promote.js to recognize [LOCKED] entries (threshold=0)

### Phase 3: Compliance Firewall (Day 1-2)
- Build `phi-firewall.sh` — PreToolUse on Slack/Email MCP tools
- Scan outbound message content for PHI patterns (SSN, DOB, Medicare ID)
- Block with clear error message if detected
- Build `destructive-gate.sh` — blocks force-push, rm -rf, etc.

### Phase 4: Quality Gates (Day 2)
- Build `deploy-verifier.sh` — PostToolUse on Bash
- Detect clasp deploy commands → verify version number in output
- Build Stop hook — Haiku checks for uncommitted work
- Build compact reinject hook — critical context survives compaction

### Phase 5: Cleanup (Day 2)
- Remove duplicate enforcement rules from CLAUDE.md (10+ items)
- Remove .local.md symlinks from all projects (replaced by real hooks)
- Update setup-hookify-symlinks.sh for new JSON format
- Update CLAUDE.md hierarchy documentation
- Update _RPI_STANDARDS reference docs

---

## File Locations

```
~/.claude/
├── settings.json          (hook event registration)
├── hooks/                 (NEW — hook scripts)
│   ├── hook-engine.sh     (PreToolUse: code enforcement engine)
│   ├── intent-router.sh   (UserPromptSubmit: memory/deploy/context routing)
│   ├── phi-firewall.sh    (PreToolUse: outbound PHI scanning)
│   ├── destructive-gate.sh (PreToolUse: dangerous command blocking)
│   ├── deploy-verifier.sh (PostToolUse: version verification)
│   └── reinject-context.sh (SessionStart compact: context preservation)
├── sync.sh                (existing — SessionStart/End sync)
├── knowledge-promote.js   (existing — updated for [LOCKED])
└── knowledge-tracker.json (existing)

~/Projects/_RPI_STANDARDS/
├── hookify/
│   ├── rules/             (NEW — JSON rule configs)
│   │   ├── block-alert-confirm-prompt.json
│   │   ├── block-phi-in-logs.json
│   │   └── ... (16+ rules)
│   └── *.local.md         (DEPRECATED — removed after migration)
├── CLAUDE.md              (slimmed down — enforcement removed)
└── reference/             (unchanged)
```

---

## Verification

1. **Hook engine test:** Write a file containing `alert('test')` → should be BLOCKED
2. **PHI firewall test:** Try sending a Slack message with "SSN: 123-45-6789" → should be BLOCKED
3. **Memory router test:** Type "remember that we always use bun" → agent should write to CLAUDE.md, not MEMORY.md
4. **Ship it test:** Type "ship it" → agent should receive full deploy protocol injection
5. **Deploy verifier test:** Run clasp deploy → should auto-verify version number
6. **Destructive gate test:** Try `git push --force` → should be BLOCKED
7. **Compact reinject test:** Trigger compaction → critical rules should be re-injected
8. **Backward compatibility:** Remove all .local.md symlinks → rules still enforced via hooks
9. **Run compliance sweep:** `node knowledge-promote.js --sweep-only` → should still detect violations

---

## What This Means for The Machine

Before: 6 layers of instructions hoping the AI follows them.
After: A code-level immune system that fires before the AI even processes, with 6 layers of context underneath.

The AI can ignore a CLAUDE.md rule. It cannot ignore a hook that blocks the tool call.

This is Layer 0. The foundation everything else stands on.
