#!/usr/bin/env bash
# check_respond_where_received.sh — Stop-event check enforcing RULE #1
# ("RESPOND WHERE YOU RECEIVE"). Cross-warrior.
#
# Called from session-end-brain-export.sh (the registered Stop hook) with the
# full transcript piped on stdin. Detects the ONE violation class: a directive
# arrived from JDM in the bilateral (dispatcher-injected user message tagged
# "Incoming from U09BBHTN8F2") AND no slack_post_message went out in the
# response → the warrior answered console-only instead of back in the bilateral.
#
# Cross-warrior tmux coordination is INVISIBLE to this check — it only looks at
# JDM directives, never warrior-to-warrior traffic, so it never pushes tmux
# chatter into the team-facing bilateral channels (per JDM 2026-06-12).
#
# Exit semantics: exit 0 always (WARN-only v1, matching the proven heartbeat
# Stop-hook pattern). A hard `{"decision":"block"}` upgrade is a tested
# follow-up — a misfiring Stop-block can loop a warrior, so v1 is loud-but-safe.
#
# SHINOB1-RULE1-ENFORCE-001 · owner: shinob1 · 2026-06-12
set -uo pipefail

_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_PY="${_DIR}/check_respond_where_received.py"
[ -f "$_PY" ] || exit 0

TRANSCRIPT="$(cat 2>/dev/null || true)"
[ -z "$TRANSCRIPT" ] && exit 0

VERDICT="$(printf '%s' "$TRANSCRIPT" | python3 "$_PY" 2>/dev/null)"

if [[ "$VERDICT" == VIOLATION* ]]; then
  SNIP="${VERDICT#VIOLATION$'\t'}"
  cat >&2 <<MSG
::warn-respond-where-you-receive::
🛑 RULE #1 VIOLATION — "RESPOND WHERE YOU RECEIVE."

JDM sent you a directive and you did NOT post your response back to your
bilateral channel — you answered console-only. That makes JDM chase your
response to another surface, which is the #1 non-negotiable rule.

  Directive: ${SNIP}

FIX IT NOW, before you stop: post your Acknowledge | Execute | Report to your
own bilateral Slack channel (mcp__slack__slack_post_message). Every JDM
directive gets its ACK, its progress, AND its final report IN that bilateral.

(Cross-warrior tmux coordination is exempt — this only fires on JDM directives,
never warrior-to-warrior traffic.)

WARN v1 — session still proceeds; hard-block upgrade pending.
MSG
fi
exit 0
