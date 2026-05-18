#!/usr/bin/env bash
# check_shinob1_session_end_heartbeat.sh — Stop-event check for warn-shinob1-session-end-no-heartbeat
#
# Fires at session end (called from session-end-brain-export.sh, the registered
# Stop hook). Scoped exclusively to SHINOB1 sessions (tmux session name matches
# SHINOB1* or shinob1*). Non-SHINOB1 sessions exit 0 immediately.
#
# Inspects /tmp/scope-prior-art-<session>.jsonl — the per-session tool ledger
# maintained by enforce.sh (PreToolUse) — for at least one
# mcp__slack__slack_post_message call during this session.
#
# Since SHINOB1 is blocked from posting to team channels (block-team-channels.py),
# any slack_post_message that made it through IS a bilateral/warrior-channel post.
# Zero posts = no heartbeat of any kind → WARN fires.
#
# Exit semantics:
#   exit 0  — always. Stop hooks cannot block. This is WARN-only.
#
# SHINOB1-STOP-HOOK-001 · 2026-05-18
# Rule: warn-shinob1-session-end-no-heartbeat

set -uo pipefail

SHINOB1_CHANNEL="C0AS0LETSBW"
TMUX_SESSION="${TMUX_SESSION:-$(tmux display-message -p '#S' 2>/dev/null || echo '')}"

# ── Scope gate: SHINOB1 sessions only ────────────────────────────────────────
# Matches: SHINOB1, SHINOB1-anything, shinob1, shinob1-anything
if [[ -z "$TMUX_SESSION" ]]; then
  exit 0
fi

if [[ ! "$TMUX_SESSION" =~ ^[Ss][Hh][Ii][Nn][Oo][Bb]1 ]]; then
  exit 0
fi

# ── Ledger check ─────────────────────────────────────────────────────────────
LEDGER="/tmp/scope-prior-art-${TMUX_SESSION}.jsonl"

# If ledger doesn't exist, no MCP calls happened — no Slack possible.
# Treat as no heartbeat only if we can confirm this is a real working session
# (not a bare test shell). Heuristic: if ledger is absent, WARN anyway —
# a true session should have left some trace.
if [[ ! -f "$LEDGER" ]]; then
  cat >&2 <<'MSG'
::warn-shinob1-session-end-no-heartbeat::
SHINOB1 session ending — no Slack activity ledger found (no MCP calls recorded).
If work was done, post a closing heartbeat to #shinob1 before exiting.

Minimum close heartbeat:
  🥷 SESSION CLOSE — <date> <time>
  Completed: <bullet list>
  PRs: <links or "none">
  Open threads: <any>
  Next: <pickup context>
  🥷 — SHINOB1 (OG)

This is a WARN — session proceeds normally.
MSG
  exit 0
fi

# Count any slack_post_message calls in this session
slack_count=$(grep -F '"mcp__slack__slack_post_message"' "$LEDGER" 2>/dev/null | wc -l || echo 0)
# Trim whitespace from wc -l output
slack_count="${slack_count//[[:space:]]/}"

if [[ "$slack_count" -lt 1 ]]; then
  cat >&2 <<MSG
::warn-shinob1-session-end-no-heartbeat::
SHINOB1 session ending without a #shinob1 heartbeat post.

Per WORKFLOW.md heartbeat doctrine:
  • Session open:   ACK within 30s
  • Session close:  Closing heartbeat to #shinob1 (C0AS0LETSBW)
  • Heads-down:     Post every 2-3 min during Write/Bash execution blocks

No mcp__slack__slack_post_message calls found in this session's ledger:
  ${LEDGER}

Post a brief session-close heartbeat to #shinob1 before exiting:

  🥷 SESSION CLOSE — $(date -u +"%Y-%m-%d %H:%M UTC")
  Completed: <bullet list of what shipped>
  PRs: <#num links or "none">
  Open threads: <any unresolved questions needing JDM>
  Next: <what the next SHINOB1 session should pick up>
  🥷 — SHINOB1 (OG)

This is a WARN-only — session can still close.
MSG
fi

exit 0
