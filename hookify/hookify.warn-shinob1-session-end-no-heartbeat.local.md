---
name: warn-shinob1-session-end-no-heartbeat
enabled: true
event: stop
action: warn
severity: WARN
scope: SHINOB1-HEARTBEAT-001
introduced: 2026-05-18
implementation: stop-event shell hook via check_shinob1_session_end_heartbeat.sh
status: enforced
wired_in: session-end-brain-export.sh (Stop hook registered in ~/.claude/settings.json)
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

**Current state: ENFORCED via Stop-event shell hook**

SHINOB1-STOP-HOOK-001 (2026-05-18) wired the check script into the active Stop hook.

**Wiring path:**
```
~/.claude/settings.json Stop hook
  → toMachina/services/learning-loop/deploy/hooks/session-end-brain-export.sh
    → _RPI_STANDARDS/hookify/check_shinob1_session_end_heartbeat.sh
```

**Check script** (`check_shinob1_session_end_heartbeat.sh`):
- Reads `/tmp/scope-prior-art-<tmux-session>.jsonl` (per-session ledger from enforce.sh)
- Scoped to SHINOB1/shinob1 sessions only (regex: `^[Ss][Hh][Ii][Nn][Oo][Bb]1`)
- Counts `mcp__slack__slack_post_message` entries in the ledger
- If count < 1 → prints WARN with heartbeat template to stderr
- Always exits 0 (Stop hooks cannot block)

**Why any slack_post_message = bilateral proxy:**
SHINOB1 is blocked from posting to team channels by `block-team-channels.py`. Therefore any
`slack_post_message` that succeeded during the session must have been a bilateral or warrior-channel post.
Zero slack posts = zero heartbeat of any kind = WARN fires.

**Note on ledger channel granularity:**
The enforce.sh ledger currently stores tool name only (not channel_id). A future enhancement
(adding `"channel"` to the Slack ledger entries) would enable filtering specifically to
`C0AS0LETSBW` posts. The current any-slack-post proxy is correct for WARN purposes.

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
