---
name: warn-shinob1-session-end-no-heartbeat
enabled: true
event: stop
action: warn
severity: WARN
scope: SHINOB1-HEARTBEAT-001
introduced: 2026-05-18
implementation: social-contract + session-end shell hook
---

# warn-shinob1-session-end-no-heartbeat

Warns SHINOB1 to post a closing heartbeat to `#shinob1` (C0AS0LETSBW) before the Claude Code session terminates.

## Heartbeat cadence (from SHINOB1 WORKFLOW.md)

SHINOB1 operates on a **session-boundary heartbeat cadence**:
- **Session open:** Post ACK within 30s of receiving the first task or context drop.
- **Session close:** Post a closing heartbeat summarizing work completed, PRs opened/merged, and any open threads before the session ends.
- **Heads-down stretches:** Heartbeat every 2–3 minutes during Write/Bash execution blocks.

The session-close heartbeat is the most commonly missed. This rule exists to close that gap.

## What the heartbeat must contain

Minimum session-close heartbeat to `#shinob1`:

```
🥷 SESSION CLOSE — <date> <time>
Completed: <bullet list of what shipped>
PRs: <#num links or "none">
Open threads: <any unresolved questions needing JDM>
Next: <what the next SHINOB1 session should pick up>

🥷 — SHINOB1 (OG)
```

## Implementation status

**Current state: SOCIAL CONTRACT + SESSION-END SHELL HOOK STUB**

The hookify plugin's frontmatter `event:` system natively supports `file`, `bash`, and `intent` events dispatched through `enforce.sh` (PreToolUse). It does NOT currently dispatch on Claude Code's `Stop` lifecycle event.

Claude Code's `Stop` hook IS wired in `~/.claude/settings.json`:

```json
"Stop": [{
  "matcher": "",
  "hooks": [{ "type": "command", "command": "...session-end.sh" }]
}]
```

To make this rule machine-enforced, SHINOB1 must:

1. Author `~/Projects/_RPI_STANDARDS/hookify/check_shinob1_session_end_heartbeat.sh`
   — reads the per-session Slack ledger at `/tmp/scope-prior-art-<tmux-session>.jsonl`
   — checks if any `mcp__slack__slack_post_message` call targeted `C0AS0LETSBW` during this session
   — exits 0 (heartbeat posted, allow) or prints a WARN and exits 0 (never block Stop)

2. Register it in `~/.claude/settings.json` Stop hooks block:
   ```json
   {
     "type": "command",
     "command": "/home/jdm/.claude/hooks/check_shinob1_session_end_heartbeat.sh"
   }
   ```

3. Add the registration to `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh`'s Stop-hook section (or create one if missing).

Until step 2 lands, this rule is enforced by SHINOB1's own discipline and session protocol. The hookify `.local.md` file exists to document the intent and provide the spec for the shell script when wired.

## Why WARN not BLOCK

Stop hooks **cannot block** in Claude Code's lifecycle — the session is terminating regardless. A Stop hook can only print a reminder. This is correct behavior: we want the reminder, not an error.

Even if the heartbeat is missed, the session ends cleanly. The goal is habit formation, not hard enforcement.

## Companion rules

- `hookify.intent-session-start.local.md` — enforces the ACK-within-30s at session open
- `enforce.sh` scope-bound ledger at `/tmp/scope-prior-art-<session>.jsonl` — already tracks every `mcp__slack__*` call; the session-end check script reads this ledger

## Reference

- SHINOB1 WORKFLOW.md § "Heartbeat Cadence" — the authoritative cadence spec
- `~/.claude/hooks/session-end.sh` — existing Stop hook (stats + brain export)
- MEMORY.md feedback `[ACK FIRST in bilateral]` — bilateral ACK protocol
- MEMORY.md feedback `[Heartbeat during heads-down]` — heads-down heartbeat protocol
- ZRD ticket for wiring: SCOPE-STOP-HOOK-001 (to be filed by SHINOB1 when picking this up)
