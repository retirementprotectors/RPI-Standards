#!/usr/bin/env bash
# check_pre_tmux_kill.sh — ENF-008 (SCOPE-005)
#
# Sibling check script for block-tmux-kill-without-exit-gate.local.md.
# Invoked by _RPI_STANDARDS/hookify/enforce.sh dispatcher when the tool call
# is `Bash` and `tool_input.command` matches `tmux kill-session [-t] <name>`.
#
# Inputs:
#   $1     — tmux session name extracted by the dispatcher.
#   $INPUT — the full PreToolUse JSON envelope (read but not required).
#
# Behavior:
#   1. If session name does NOT match `^(\w+)-disco-sub-(\S+)$` → exit 0
#      (non-sub-CXO tmux kills pass through).
#   2. Load ForgeRunState for that session via ENF-006 CLI:
#         node scripts/forge-state-load.mjs <session_name>
#      - exit 1 + `{}` from the CLI → session doesn't exist in Firestore →
#        exit 0 (the kill is not gated by exit-gate state).
#      - exit 0 + JSON doc from the CLI → parse exit_gate fields.
#   3. exit_gate.disco_pr_merged === true AND exit_gate.parent_ack === true
#      → exit 0 (kill allowed).
#   4. Otherwise → exit 1 with the rule's block message on stderr.
#
# Dependencies: jq, node (for ENF-006 CLI).
#
# ZRD-SCOPE-005-001 v1.0 · Section A · ENF-008

set -euo pipefail

SESSION_NAME="${1:-}"
[[ -z "$SESSION_NAME" ]] && exit 0  # no session name extracted → not our concern

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT_GUESS="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
FORGE_STATE_LOAD="${FORGE_STATE_LOAD:-${REPO_ROOT_GUESS}/scripts/forge-state-load.mjs}"

# Sub-CXO session-name pattern.
if ! [[ "$SESSION_NAME" =~ ^([a-zA-Z0-9_]+)-disco-sub-([A-Za-z0-9_.-]+)$ ]]; then
  exit 0
fi

# Load ForgeRunState.
if ! command -v node >/dev/null 2>&1; then
  # No node → cannot enforce; allow rather than hard-block on tooling gap.
  exit 0
fi
if [[ ! -f "$FORGE_STATE_LOAD" ]]; then
  exit 0
fi

set +e
STATE_JSON=$(node "$FORGE_STATE_LOAD" "$SESSION_NAME" 2>/dev/null)
CLI_RC=$?
set -e

# CLI exit 1 + `{}` means "no Firestore doc for this session" — non-sub-CXO
# tmux kills pass through.
if [[ $CLI_RC -ne 0 ]]; then
  # Distinguish "doc missing" from "error". Both result in `{}` to stdout.
  # If the doc is genuinely missing, the kill is allowed (per spec).
  exit 0
fi

# Parse exit_gate fields.
PR_MERGED=$(echo "$STATE_JSON" | jq -r '.exit_gate.disco_pr_merged // false' 2>/dev/null)
PARENT_ACK=$(echo "$STATE_JSON" | jq -r '.exit_gate.parent_ack // false' 2>/dev/null)

if [[ "$PR_MERGED" == "true" && "$PARENT_ACK" == "true" ]]; then
  exit 0
fi

cat >&2 <<EOF
BLOCKED: tmux kill-session requires exit gate to be fully open.

Current gate state for ${SESSION_NAME}:
  disco_pr_merged: ${PR_MERGED}
  parent_ack:      ${PARENT_ACK}

To open the gate:
  1. PR must be merged to main (GitHub webhook auto-flips disco_pr_merged
     via POST /api/forge/exit-gate)
  2. Parent CXO must ✅-react to your completion post in bilateral channel
     (Slack reaction_added listener auto-flips parent_ack
     via /api/events/slack)

Do NOT kill this session until both are true.
ZRD-SCOPE-005-001 / TRK-14758 Death-Gate Protocol.
EOF
exit 1
