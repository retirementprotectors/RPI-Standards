#!/usr/bin/env bash
# check_disco_canonical_tabs.sh — pre-write / pre-edit check
#
# Fires under: pre-write / pre-edit scope-bound events
# Companion to: hookify.block-disco-missing-canonical-tabs.local.md
#
# Blocks (exit 1) when:
#   1. Tool target file matches docs/discoveries/*.html
#   2. AND the proposed content is missing any of the 8 canonical Discovery Doc
#      panel sections (id="panel-pain", id="panel-build", id="panel-arch",
#      id="panel-decisions", id="panel-phases", id="panel-tickets",
#      id="panel-files", id="panel-gates")
#
# Allows (exit 0) when:
#   - Target file is outside docs/discoveries/
#   - OR all 8 panel IDs are present in the proposed content
#   - OR jq is unavailable (graceful degrade — never block on missing tooling)
#
# Input: $INPUT env var (set by enforce.sh dispatch), OR stdin fallback.
# $1:   file path being written/edited
#
# JDM directive 2026-04-29: ALL new disco docs follow the canonical 8-tab
# format. This check enforces that mandate at write time.
#
# Reference:
#   Template:      docs/templates/discovery-doc-template.html
#   Format guide:  docs/templates/DISCOVERY_DOC_FORMAT.md
#
# NOTE: set -o pipefail causes grep -q to produce exit 141 (SIGPIPE) when the
# echo writer gets a broken pipe after grep's early exit. To avoid this, we use
# grep -c (count) instead of grep -q, which reads the full input before exiting.

set -uo pipefail

FILE_PATH="${1:-}"

# Allow if no file path arg
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Allow if file is not in docs/discoveries/
if [[ "$FILE_PATH" != */docs/discoveries/*.html && "$FILE_PATH" != docs/discoveries/*.html ]]; then
  exit 0
fi

# Allow if jq is unavailable — fail-open so tooling gaps don't block writes
if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

# Read INPUT JSON: prefer $INPUT env var (set by enforce.sh), fall back to stdin.
# This matches the pattern used by check_pre_slack_post.sh.
INPUT_JSON="${INPUT:-$(cat)}"

# Extract content from Write or Edit tool call
CONTENT=""
TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name // empty' 2>/dev/null)

if [[ "$TOOL_NAME" == "Write" ]]; then
  CONTENT=$(echo "$INPUT_JSON" | jq -r '.tool_input.content // empty' 2>/dev/null)
elif [[ "$TOOL_NAME" == "Edit" ]]; then
  # For Edit, check new_string — it may be a partial write. We only block
  # if the new_string itself contains panel-* markers but is missing some tabs
  # (i.e. the edit is replacing/rewriting the tab scaffold with an incomplete one).
  # If new_string has no panel-* markers at all, it's a content-only edit — allow.
  NEW_STRING=$(echo "$INPUT_JSON" | jq -r '.tool_input.new_string // empty' 2>/dev/null)
  # Use grep -c to avoid SIGPIPE with pipefail
  panel_count=$(echo "$NEW_STRING" | grep -cF 'id="panel-' || true)
  if [[ "$panel_count" -eq 0 ]]; then
    # No panel markers in the edit — it's not touching the tab scaffold
    exit 0
  fi
  CONTENT="$NEW_STRING"
else
  exit 0
fi

# Allow if content is empty
if [[ -z "$CONTENT" ]]; then
  exit 0
fi

# Write content to a temp file to avoid SIGPIPE issues with grep -q + pipefail.
# grep -q causes the writer (echo) to get SIGPIPE (exit 141) when it finds a match
# and exits early. With set -o pipefail this propagates as a non-zero exit even
# when the grep itself succeeds. Using a temp file sidesteps this entirely.
TMPFILE=$(mktemp)
# shellcheck disable=SC2064
trap "rm -f '$TMPFILE'" EXIT
printf '%s' "$CONTENT" > "$TMPFILE"

# Check for all 8 canonical panel IDs
CANONICAL_TABS=(
  'id="panel-pain"'
  'id="panel-build"'
  'id="panel-arch"'
  'id="panel-decisions"'
  'id="panel-phases"'
  'id="panel-tickets"'
  'id="panel-files"'
  'id="panel-gates"'
)

TAB_NAMES=(
  "01 · Pain"
  "02 · Build"
  "03 · Architecture"
  "04 · Decisions"
  "05 · Phases"
  "06 · Tickets"
  "07 · Files"
  "08 · Gates"
)

MISSING_TABS=()
for i in "${!CANONICAL_TABS[@]}"; do
  marker="${CANONICAL_TABS[$i]}"
  count=$(grep -cF "$marker" "$TMPFILE" || true)
  if [[ "$count" -eq 0 ]]; then
    MISSING_TABS+=("${TAB_NAMES[$i]}")
  fi
done

# All 8 present — allow
if [[ ${#MISSING_TABS[@]} -eq 0 ]]; then
  exit 0
fi

# BLOCK — one or more canonical tabs are missing
MISSING_LIST=$(printf '  - %s\n' "${MISSING_TABS[@]}")

cat >&2 <<EOF
ENFORCE [block-disco-missing-canonical-tabs]: Discovery Doc is missing canonical tabs.

File:    $FILE_PATH
Missing:
${MISSING_LIST}

All 8 canonical tabs are REQUIRED per JDM directive 2026-04-29.
A tab can be sparse, but it cannot be absent.

The 8 canonical panels (all must be present):
  01 · Pain          id="panel-pain"
  02 · Build         id="panel-build"
  03 · Architecture  id="panel-arch"
  04 · Decisions     id="panel-decisions"
  05 · Phases        id="panel-phases"
  06 · Tickets       id="panel-tickets"
  07 · Files         id="panel-files"
  08 · Gates         id="panel-gates"

Fix:
  1. Copy the canonical template:
     cp docs/templates/discovery-doc-template.html docs/discoveries/<your-doc>.html
  2. Fill in the placeholders -- do NOT remove any panel sections.
  3. See the format guide: docs/templates/DISCOVERY_DOC_FORMAT.md

Reference: JDM directive 2026-04-29 · toMachina CLAUDE.md section "Discovery Doc Format"
EOF
exit 1
