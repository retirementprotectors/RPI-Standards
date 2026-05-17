#!/usr/bin/env bash
# enforce.sh — PreToolUse hook: Tier 1 enforcement dispatcher.
#
# Canonical source for ~/.claude/hooks/enforce.sh. Deployed via
# ~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh (or
# a one-time `cp _RPI_STANDARDS/hookify/enforce.sh ~/.claude/hooks/enforce.sh`).
#
# Two dispatcher layers:
#   1. File-content rules (Write/Edit) — Tier 1 belt-and-suspenders alongside hookify.
#   2. Scope-bound event rules (SCOPE-005 / ENF-004 + ENF-005):
#        - pre-slack-post   — fires on mcp__slack__slack_post_message
#        - pre-tmux-kill    — fires on `tmux kill-session` Bash invocations
#      Both walk _RPI_STANDARDS/hookify/scope-bound/*.local.md files whose
#      frontmatter declares `event: <category>`, then invoke each rule's
#      sibling `check_<event_underscored>.sh` script. Non-zero exit blocks
#      the tool call; every fire is appended to the violation log.
#
# Exit semantics:
#   exit 0  → allow
#   exit 2  → block (the hookify convention is exit 2 = block)
#   exit 1  → reserved for ENF-007/008 check scripts; the dispatcher
#             translates a non-zero rule exit into its own exit 2 with the
#             rule-supplied stderr passed through.
#
# Target: <500ms per invocation.
# ZRD-SCOPE-005-001 v1.0 · Section A · ENF-004 + ENF-005

set -euo pipefail

# Fail-open on missing required deps so a tooling gap on a single machine
# never silently blocks every Slack post or tmux kill across the team.
if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

# ── Portable paths ────────────────────────────────────────────────────────────
HOME_DIR="${HOME:-/home/jdm}"
VIOLATION_LOG="${HOOKIFY_VIOLATION_LOG:-${HOME_DIR}/.claude/hooks/violation-log.jsonl}"

# Canonical scope-bound rule directory (repo SSOT). Override with
# HOOKIFY_SCOPE_BOUND_DIR for tests or alternate deployments.
#
# SHINOB1-DISPATCHER-CANONICAL-PRIORITY-001 (2026-05-17):
# Resolution priority — canonical sibling first, then the toMachina mirror
# fallback for fresh-checkout environments. Previously the order was
# inverted: the toMachina mirror was the primary default, which meant every
# canonical-repo edit needed a hand-mirror commit into toMachina or it
# never took effect in production. This was exactly the failure mode that
# blocked 5+ legitimate Slack posts after Opt-B "merged" earlier this
# session — the change landed in _RPI_STANDARDS but the dispatcher read
# from the stale mirror copy in toMachina.
#
# New order:
#   1. HOOKIFY_SCOPE_BOUND_DIR env override (tests, alternate deployments)
#   2. Canonical _RPI_STANDARDS path (the dispatcher's own sibling, resolved
#      via readlink -f so the ~/.claude/hooks/enforce.sh symlink resolves
#      to its real location at _RPI_STANDARDS/hookify/enforce.sh)
#   3. toMachina mirror at toMachina/_RPI_STANDARDS/hookify/scope-bound/
#      (fallback for environments without a separate _RPI_STANDARDS clone)
SCOPE_BOUND_DIR="${HOOKIFY_SCOPE_BOUND_DIR:-}"
if [[ -z "$SCOPE_BOUND_DIR" || ! -d "$SCOPE_BOUND_DIR" ]]; then
  # Step 1: try canonical (dispatcher's sibling, resolved through symlinks).
  _ENFORCE_REAL="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || printf '%s' "${BASH_SOURCE[0]}")"
  _ENFORCE_DIR="$(cd "$(dirname "$_ENFORCE_REAL")" && pwd)"
  if [[ -d "${_ENFORCE_DIR}/scope-bound" ]]; then
    SCOPE_BOUND_DIR="${_ENFORCE_DIR}/scope-bound"
  else
    # Step 2: fall back to the toMachina mirror.
    _TM_MIRROR="${HOME_DIR}/Projects/toMachina/_RPI_STANDARDS/hookify/scope-bound"
    if [[ -d "$_TM_MIRROR" ]]; then
      SCOPE_BOUND_DIR="$_TM_MIRROR"
    fi
  fi
fi

log_violation() {
  local rule="$1"
  local tool="$2"
  local detail="$3"
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  detail="${detail//\"/\\\"}"
  # Best-effort write; missing log dir is non-fatal.
  mkdir -p "$(dirname "$VIOLATION_LOG")" 2>/dev/null || true
  echo "{\"timestamp\":\"${ts}\",\"rule\":\"${rule}\",\"tool\":\"${tool}\",\"detail\":\"${detail}\",\"hook\":\"enforce.sh\"}" >> "$VIOLATION_LOG" 2>/dev/null || true
}

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[[ -z "$TOOL_NAME" ]] && exit 0

# ─────────────────────────────────────────────────────────────────────────────
# SCOPE-005-1-F: per-session tool-call ledger.
# Append every MCP tool call to /tmp/scope-prior-art-<session>.jsonl so the
# pre-slack-post first-5-tool-call audit can read the invocation set later.
# Best-effort write — never blocks if tmux/jq unavailable or write fails.
# ─────────────────────────────────────────────────────────────────────────────
if [[ "$TOOL_NAME" == mcp__* ]]; then
  TMUX_SESSION="$(tmux display-message -p '#S' 2>/dev/null || true)"
  if [[ -n "$TMUX_SESSION" ]]; then
    LEDGER="/tmp/scope-prior-art-${TMUX_SESSION}.jsonl"
    LEDGER_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"ts\":\"${LEDGER_TS}\",\"tool\":\"${TOOL_NAME}\"}" >> "$LEDGER" 2>/dev/null || true
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Scope-bound event dispatch — runs before file-content rules so that a
# blocked Slack post or tmux kill never falls through to the file-content
# branches (which would short-circuit-exit 0 on non-Write/Edit anyway).
# ─────────────────────────────────────────────────────────────────────────────

# Walk scope-bound/*.local.md files whose frontmatter contains `event: <name>`,
# invoke each rule's sibling check script, and pass through stderr + a blocking
# exit 2 on non-zero. Extra args after the event are forwarded to the check
# script (used by pre-tmux-kill to pass the session name).
dispatch_scope_bound_event() {
  local event="$1"; shift
  local input_json="$1"; shift
  local extra_arg="${1:-}"

  [[ -d "$SCOPE_BOUND_DIR" ]] || return 0

  local underscored="${event//-/_}"
  local default_check_basename="check_${underscored}.sh"

  shopt -s nullglob
  local rule_file
  for rule_file in "$SCOPE_BOUND_DIR"/*.local.md; do
    # Extract `event: <list>` from anywhere in the rule body. Comma-separated
    # event lists are supported — a rule fires on ANY matching event in its list.
    local declared_event_raw
    declared_event_raw=$(grep -m1 -E '^event:[[:space:]]*' "$rule_file" 2>/dev/null | sed -E 's/^event:[[:space:]]*//; s/[[:space:]]*$//')
    [[ -n "$declared_event_raw" ]] || continue

    # Check if current event is in the rule's comma-separated event list
    local event_matches=0
    local single_event
    IFS=',' read -ra declared_events <<< "$declared_event_raw"
    for single_event in "${declared_events[@]}"; do
      # Trim whitespace
      single_event="${single_event#"${single_event%%[![:space:]]*}"}"
      single_event="${single_event%"${single_event##*[![:space:]]}"}"
      if [[ "$single_event" == "$event" ]]; then
        event_matches=1
        break
      fi
    done
    [[ "$event_matches" -eq 1 ]] || continue

    local rule_id
    rule_id=$(basename "$rule_file" .local.md)

    # Per-rule check script override via `check:` frontmatter field.
    # Falls back to canonical `check_<event-underscored>.sh` if not specified.
    local override_check
    override_check=$(grep -m1 -E '^check:[[:space:]]*' "$rule_file" 2>/dev/null | sed -E 's/^check:[[:space:]]*//; s/[[:space:]]*$//')
    local check_basename="${override_check:-$default_check_basename}"
    local check_script="${SCOPE_BOUND_DIR}/${check_basename}"

    if [[ ! -x "$check_script" ]]; then
      # Check script missing or non-executable — log + skip rather than block.
      log_violation "${rule_id}::missing-check" "$TOOL_NAME" "$check_script"
      continue
    fi

    # Run the rule's check script. INPUT JSON on stdin; optional positional arg.
    local rc=0
    INPUT="$input_json" "$check_script" "$extra_arg" || rc=$?
    if [[ $rc -ne 0 ]]; then
      log_violation "$rule_id" "$TOOL_NAME" "blocked-on-${event}"
      exit 2
    fi
    log_violation "${rule_id}::passed" "$TOOL_NAME" "${event}"
  done
  shopt -u nullglob
  return 0
}

# pre-slack-post — fires on mcp__slack__slack_post_message
if [[ "$TOOL_NAME" == "mcp__slack__slack_post_message" ]]; then
  dispatch_scope_bound_event "pre-slack-post" "$INPUT"
fi

# pre-tmux-kill — fires on `tmux kill-session [-t] <name>` Bash invocations
if [[ "$TOOL_NAME" == "Bash" ]]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
  if [[ "$CMD" =~ tmux[[:space:]]+kill-session([[:space:]]+-t)?[[:space:]]+([^[:space:]\;\&\|]+) ]]; then
    SESSION_NAME="${BASH_REMATCH[2]}"
    dispatch_scope_bound_event "pre-tmux-kill" "$INPUT" "$SESSION_NAME"
  fi
fi

# pre-write / pre-edit / pre-notebook-edit — fires on file-modification tool calls.
# SCOPE-005-1-K: extends dispatcher to fire scope-bound rules on file writes.
# Rules listening for these events get the file path as the extra positional arg.
if [[ "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH_ARG=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
  if [[ -n "$FILE_PATH_ARG" ]]; then
    dispatch_scope_bound_event "pre-write" "$INPUT" "$FILE_PATH_ARG"
  fi
fi
if [[ "$TOOL_NAME" == "Edit" ]]; then
  FILE_PATH_ARG=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
  if [[ -n "$FILE_PATH_ARG" ]]; then
    dispatch_scope_bound_event "pre-edit" "$INPUT" "$FILE_PATH_ARG"
  fi
fi
if [[ "$TOOL_NAME" == "NotebookEdit" ]]; then
  FILE_PATH_ARG=$(echo "$INPUT" | jq -r '.tool_input.notebook_path // empty' 2>/dev/null)
  if [[ -n "$FILE_PATH_ARG" ]]; then
    dispatch_scope_bound_event "pre-notebook-edit" "$INPUT" "$FILE_PATH_ARG"
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Tier 1 file-content rules — apply to Write/Edit only.
# ─────────────────────────────────────────────────────────────────────────────

CONTENT=""
FILEPATH=""
case "$TOOL_NAME" in
  Write)
    CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // empty' 2>/dev/null)
    FILEPATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    ;;
  Edit)
    CONTENT=$(echo "$INPUT" | jq -r '.tool_input.new_string // empty' 2>/dev/null)
    FILEPATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    ;;
  *)
    exit 0 ;;
esac

[[ -z "$CONTENT" ]] && exit 0

# === Rule: block-hardcoded-secrets ===
if echo "$CONTENT" | grep -qE 'sk-[a-zA-Z0-9]{20}|AIza[A-Za-z0-9_-]{35}|xox[bprs]-[a-zA-Z0-9-]{10}|ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16}|glpat-[a-zA-Z0-9_-]{20}'; then
  log_violation "block-hardcoded-secrets" "$TOOL_NAME" "$FILEPATH"
  cat >&2 <<'EOF'
ENFORCE [block-hardcoded-secrets]: API key or token detected in code.
Use Script Properties (PropertiesService) or environment variables.
Never commit secrets to source files.
EOF
  exit 2
fi

# === Rule: block-anyone-anonymous-access ===
if [[ "$FILEPATH" == *appsscript.json ]]; then
  if echo "$CONTENT" | grep -q 'ANYONE_ANONYMOUS'; then
    log_violation "block-anyone-anonymous-access" "$TOOL_NAME" "$FILEPATH"
    cat >&2 <<'EOF'
ENFORCE [block-anyone-anonymous-access]: Web app access set to ANYONE_ANONYMOUS.
Must be "DOMAIN" — restricted to "Anyone within Retirement Protectors INC".
Fix the "access" field in appsscript.json before deploying.
EOF
    exit 2
  fi
fi

# === Rule: block-alert-confirm-prompt ===
if [[ "$FILEPATH" =~ \.(gs|js|ts|html)$ ]]; then
  if echo "$CONTENT" | grep -qE '\balert[[:space:]]*\(|\bconfirm[[:space:]]*\(|\bprompt[[:space:]]*\('; then
    log_violation "block-alert-confirm-prompt" "$TOOL_NAME" "$FILEPATH"
    cat >&2 <<'EOF'
ENFORCE [block-alert-confirm-prompt]: alert()/confirm()/prompt() detected.
Use showToast('message', 'type') for notifications.
Use await showConfirmation({...}) for confirmations.
Never use browser dialog functions in RPI apps.
EOF
    exit 2
  fi
fi

# === Rule: block-phi-in-logs ===
if echo "$CONTENT" | grep -qE '(console\.log|Logger\.log)[[:space:]]*\(.*\b(ssn|SSN|dob|DOB|medicare_id|social_security)\b'; then
  log_violation "block-phi-in-logs" "$TOOL_NAME" "$FILEPATH"
  cat >&2 <<'EOF'
ENFORCE [block-phi-in-logs]: PHI reference in logging statement.
Never log SSN, DOB, or Medicare ID to console or Logger.
Remove PHI from log statements. Mask if debug context is needed.
EOF
  exit 2
fi

# === Rule: block-credentials-in-config ===
if [[ "$FILEPATH" =~ \.(json|yaml|yml)$ ]]; then
  if echo "$CONTENT" | grep -qE '"(token|secret|password|apiKey|api_key|client_secret)"[[:space:]]*:[[:space:]]*"[^"]{10,}"'; then
    if ! echo "$CONTENT" | grep -qE '"(token|secret|password|apiKey|api_key|client_secret)"[[:space:]]*:[[:space:]]*"(YOUR_|REPLACE_|placeholder|xxx)'; then
      log_violation "block-credentials-in-config" "$TOOL_NAME" "$FILEPATH"
      cat >&2 <<'EOF'
ENFORCE [block-credentials-in-config]: Credential value in config file.
Use Script Properties (PropertiesService.getScriptProperties()) for secrets.
Never store real credentials in JSON/YAML files that get committed to git.
EOF
      exit 2
    fi
  fi
fi

# All checks passed
exit 0
