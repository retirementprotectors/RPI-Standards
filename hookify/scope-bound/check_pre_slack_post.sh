#!/usr/bin/env bash
# check_pre_slack_post.sh — ENF-007 (SCOPE-005)
#
# Sibling check script for block-parent-cxo-disco-without-spawn.local.md.
# Invoked by _RPI_STANDARDS/hookify/enforce.sh dispatcher when the tool call
# is `mcp__slack__slack_post_message` and any scope-bound rule declares
# `event: pre-slack-post`.
#
# Inputs (read from environment):
#   $INPUT — the full PreToolUse JSON envelope (tool_name + tool_input).
#
# Behavior:
#   1. Extract `tool_input.channel` and `tool_input.text`.
#   2. If channel ∈ {5 parent bilateral channel IDs}
#      AND text matches the scope/disco claim regex
#      AND NO active `<warrior>-disco-sub-*` session exists in
#          ForgeRunState with `spawn_ts >= now - 3600s`
#      → exit 1 with the rule's block message on stderr.
#   3. Otherwise exit 0 (allow the post).
#
# Allow-through cases:
#   - Channel is not a parent bilateral.
#   - Message body does not match scope/disco claim regex.
#   - Active sub-warrior found for the inferred parent.
#   - Message is the death-gate ACK itself (contains "ACK" + "-disco-sub-" + PR URL).
#   - Message is the sub-warrior's own completion post (auto-allowed via
#     sentinel footer [session:<name>]).
#
# Dependencies: jq, node (for ENF-006 CLI).
#
# ZRD-SCOPE-005-001 v1.0 · Section A · ENF-007

set -euo pipefail

# Allow override of the ENF-006 CLI location for tests.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT_GUESS="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
FORGE_STATE_LOAD="${FORGE_STATE_LOAD:-${REPO_ROOT_GUESS}/scripts/forge-state-load.mjs}"

# 5 parent bilateral channel IDs (verbatim per disco + CLAUDE.md).
declare -A PARENT_BY_CHANNEL=(
  ["C0AS0LETSBW"]="shinob1"
  ["C0ARFBHSKNK"]="musashi"
  ["C0ARWQMMUMQ"]="megazord"
  ["C0ARUP0HM1C"]="voltron"
  ["C0ASE72K458"]="taiko"
)

INPUT_JSON="${INPUT:-$(cat)}"
# SCOPE-005-1-P: MCP slack tool uses `channel_id`, not `channel`. Accept either,
# and fail-open if neither is present (bash associative array subscript with
# empty key throws "bad array subscript" — non-fatal but spams stderr).
CHANNEL=$(echo "$INPUT_JSON" | jq -r '.tool_input.channel_id // .tool_input.channel // empty' 2>/dev/null)
TEXT=$(echo "$INPUT_JSON" | jq -r '.tool_input.text // empty' 2>/dev/null)
[[ -z "$CHANNEL" ]] && exit 0

# ─────────────────────────────────────────────────────────────────────────────
# SCOPE-005-1-F: First-5-tool-call audit for *-disco-sub-* sessions.
# When called from a sub-CXO session, require that all 4 universal MCP
# registry tools (plus the parent-specific tool when shipped) have been
# invoked at least once BEFORE the first scope/disco-claim Slack post.
#
# Ledger is appended by enforce.sh at /tmp/scope-prior-art-<session>.jsonl
# (each line: {"ts":"...","tool":"mcp__xxx__yyy"}). We read it, build the
# set of invoked tools, compare against the required set for this parent.
#
# Allow-through cases (don't audit):
#   - Not in a *-disco-sub-* session (only sub-warriors are audited)
#   - Text doesn't match disco/scope claim regex (the existing check below)
# ─────────────────────────────────────────────────────────────────────────────
TMUX_SESSION="$(tmux display-message -p '#S' 2>/dev/null || true)"
if [[ "$TMUX_SESSION" =~ ^([a-zA-Z0-9_]+)-disco-sub-[^[:space:]]+$ ]]; then
  PARENT_FROM_SESSION="${BASH_REMATCH[1]}"
  LEDGER="/tmp/scope-prior-art-${TMUX_SESSION}.jsonl"

  # Required tools per parent
  REQUIRED_UNIVERSAL=(
    "mcp__shinob1__grep_discoveries"
    "mcp__shinob1__grep_codebase"
    "mcp__shinob1__gh_search_prs"
    "mcp__shinob1__firestore_collections_list"
  )
  REQUIRED_PARENT=""
  case "$PARENT_FROM_SESSION" in
    shinob1)  REQUIRED_PARENT="mcp__shinob1__architecture_search" ;;
    musashi)  REQUIRED_PARENT="mcp__musashi__cmo_registry_search" ;;
    megazord) REQUIRED_PARENT="mcp__megazord__atlas_registry_search" ;;
    voltron)  REQUIRED_PARENT="mcp__voltron__que_registry_search" ;;
    taiko)    REQUIRED_PARENT="mcp__taiko__pipes_registry_search" ;;
    ronin)    REQUIRED_PARENT="mcp__ronin__sprint_history_search" ;;
  esac

  # Build the invoked-tools set from the ledger (if present)
  INVOKED_SET=""
  if [[ -f "$LEDGER" ]]; then
    INVOKED_SET=$(jq -r '.tool' "$LEDGER" 2>/dev/null | sort -u)
  fi

  # Detect disco/scope claim (same regex as the channel-allowlist check below,
  # repeated here for the audit branch — only audit when the post is disco-shape)
  shopt -s nocasematch
  AUDIT_MATCH=0
  if [[ "$TEXT" =~ (disco|discovery|disco[[:space:]]+doc|discovery[[:space:]]+doc) ]]; then AUDIT_MATCH=1; fi
  if [[ "$TEXT" =~ scope.*\b(writing|drafting|authoring|completing)\b ]]; then AUDIT_MATCH=1; fi
  if [[ "$TEXT" =~ ZRD-[A-Za-z0-9_-]+ ]]; then AUDIT_MATCH=1; fi
  if [[ "$TEXT" =~ 8[-[:space:]]?tab ]]; then AUDIT_MATCH=1; fi
  shopt -u nocasematch

  # Allow-through: not a disco-shape post → skip audit
  if [[ $AUDIT_MATCH -eq 1 ]]; then
    # Allow-through: completion-receipt drum (carries [session:<name>] sentinel)
    if ! [[ "$TEXT" =~ \[session:[a-zA-Z0-9_-]+\] ]]; then
      MISSING_TOOLS=()
      for tool in "${REQUIRED_UNIVERSAL[@]}"; do
        if ! grep -qFx "$tool" <<<"$INVOKED_SET"; then
          MISSING_TOOLS+=("$tool")
        fi
      done
      if [[ -n "$REQUIRED_PARENT" ]] && ! grep -qFx "$REQUIRED_PARENT" <<<"$INVOKED_SET"; then
        MISSING_TOOLS+=("$REQUIRED_PARENT")
      fi

      if [[ ${#MISSING_TOOLS[@]} -gt 0 ]]; then
        cat >&2 <<EOF
ENFORCE [first-5-tool-call audit] — SCOPE-005-1-F
Sub-CXO session: ${TMUX_SESSION}
Parent CXO:      ${PARENT_FROM_SESSION}

Disco-shape Slack post BLOCKED — first-5-tool-call audit incomplete.

Missing required registry queries (must each be invoked at least once
BEFORE the first scope/disco-claim post):
$(printf '  - %s\n' "${MISSING_TOOLS[@]}")

The audit ensures every disco is grounded in a verified multi-registry
prior-art check. Re-run the missing tools, then re-attempt the post.

Ledger:  ${LEDGER}
Invoked: $(echo "${INVOKED_SET}" | tr '\n' ',' | sed 's/,$//')

ZRD-SCOPE-005-1 v1.1 · SCOPE-005-1-F
EOF
        exit 1
      fi
    fi
  fi
fi

# Channel not a parent bilateral → allow.
PARENT_LOWER="${PARENT_BY_CHANNEL[$CHANNEL]:-}"
[[ -z "$PARENT_LOWER" ]] && exit 0

# Scope/disco claim regex (per rule body lines 24-29 of
# block-parent-cxo-disco-without-spawn.local.md).
# - "disco" or "discovery" (case-insensitive)
# - "scope" + ("writing" | "drafting" | "authoring" | "completing")
# - "ZRD-" followed by anything
# - "8-tab" or "8 tab"
# - "discovery doc" or "disco doc"
shopt -s nocasematch
MATCH=0
if [[ "$TEXT" =~ (disco|discovery|disco[[:space:]]+doc|discovery[[:space:]]+doc) ]]; then MATCH=1; fi
if [[ "$TEXT" =~ scope.*\b(writing|drafting|authoring|completing)\b ]]; then MATCH=1; fi
if [[ "$TEXT" =~ ZRD-[A-Za-z0-9_-]+ ]]; then MATCH=1; fi
if [[ "$TEXT" =~ 8[-[:space:]]?tab ]]; then MATCH=1; fi
shopt -u nocasematch

# Death-gate ACK allow-through: message contains "ACK" + "-disco-sub-" + a URL.
if [[ "$TEXT" =~ ACK && "$TEXT" =~ -disco-sub- && "$TEXT" =~ https?:// ]]; then
  exit 0
fi

# Sub-warrior completion post allow-through: carries [session:<name>] sentinel.
if [[ "$TEXT" =~ \[session:[a-zA-Z0-9_-]+\] ]]; then
  exit 0
fi

# No scope/disco claim → allow.
[[ $MATCH -eq 0 ]] && exit 0

# Scope/disco claim in parent bilateral channel — must have active sub-warrior.
# Iterate Firestore for active <parent>-disco-sub-* within the last 3600s.
NOW_EPOCH=$(date -u +%s)
WINDOW_SEC="${HOOKIFY_SPAWN_WINDOW_SEC:-3600}"

# ENF-006 CLI gives us a single doc by name; we don't have a list endpoint
# baked in. Strategy: shellout to gcloud firestore query if available, else
# fall back to a deterministic doc-name probe. The disco's spec leaves the
# query mechanism to the implementation; ENF-006 is the canonical bridge.
#
# Minimal viable check: try the ENF-006 CLI with a `<parent>-disco-sub-*`
# wildcard via the `--list` invocation. If the CLI doesn't support listing,
# we fall back to "no active sub" → block.

ACTIVE_FOUND=0
if command -v node >/dev/null 2>&1 && [[ -f "$FORGE_STATE_LOAD" ]]; then
  # Query the dispatcher-level helper (ENF-006). The CLI as specified takes a
  # specific session name; for the list-probe variant we accept a wildcard via
  # an opt-in env (HOOKIFY_FORGE_STATE_LIST) the deployment can wire up later.
  # Until then we conservatively assume no active sub — the wall holds, which
  # is the doctrine choice per Q5 (hard-block day 1).
  if [[ -n "${HOOKIFY_FORGE_STATE_LIST:-}" ]] && [[ -x "$HOOKIFY_FORGE_STATE_LIST" ]]; then
    LIST_OUTPUT=$("$HOOKIFY_FORGE_STATE_LIST" --parent "$PARENT_LOWER" --window-sec "$WINDOW_SEC" 2>/dev/null || true)
    if [[ -n "$LIST_OUTPUT" ]] && [[ "$LIST_OUTPUT" != "[]" ]]; then
      ACTIVE_FOUND=1
    fi
  fi
fi

if [[ $ACTIVE_FOUND -eq 1 ]]; then
  exit 0
fi

cat >&2 <<EOF
BLOCKED: scope/disco claim without active sub-warrior spawn.

Parent CXOs cannot write discovery docs in-session.
Exclusive path: spawn a sub-CXO first.

  scripts/spawn-subcxo-disco.sh \\
    --parent ${PARENT_LOWER^^} \\
    --scope-id <scope-id> \\
    --brief <path/to/brief.md>

Sub-warrior writes the disco. Parent reviews + ACKs. Death-gate closes.
No exceptions. ZRD-SCOPE-005-001 / TRK-14757.
EOF
exit 1
