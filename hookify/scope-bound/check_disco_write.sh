#!/usr/bin/env bash
# check_disco_write.sh — SCOPE-005-1-L check script
#
# Fires under: pre-write / pre-edit events
# Companion to: block-disco-write-from-non-sub-session.local.md
#
# Blocks (exit 1) when:
#   1. Tool target file matches docs/discoveries/*.html
#   2. AND the current tmux session is NOT a *-disco-sub-* session
#
# Allows (exit 0) when:
#   - Target file is outside docs/discoveries/
#   - OR session is a properly-spawned <parent>-disco-sub-<scope> sub-CXO
#   - OR tmux is unavailable (graceful degrade — don't block on missing tmux)
#
# stdin: JSON of the tool call (full INPUT from enforce.sh)
# $1: file path being written/edited
#
# ZRD-SCOPE-005-1 v1.1 · SCOPE-005-1-L

set -uo pipefail

FILE_PATH="${1:-}"

# Allow if no file path arg (shouldn't happen — dispatcher passes the arg)
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Allow if file is not in docs/discoveries/
case "$FILE_PATH" in
  */docs/discoveries/*.html|docs/discoveries/*.html)
    : # in scope — continue
    ;;
  *)
    exit 0
    ;;
esac

# Determine current tmux session name
TMUX_SESSION=""
if command -v tmux >/dev/null 2>&1; then
  TMUX_SESSION="$(tmux display-message -p '#S' 2>/dev/null || true)"
fi

# Allow if tmux is unavailable or session can't be determined.
# Better to under-block than to break developers who aren't in tmux.
if [[ -z "$TMUX_SESSION" ]]; then
  exit 0
fi

# Allow if session matches the sub-CXO pattern: <parent>-disco-sub-<scope>
# Parent is anything matching \w+; scope is anything matching \S+
if [[ "$TMUX_SESSION" =~ ^[a-zA-Z0-9_]+-disco-sub-[^[:space:]]+$ ]]; then
  exit 0
fi

# BLOCK — disco file write from non-sub-CXO session
cat >&2 <<EOF
ENFORCE [block-disco-write-from-non-sub-session]: Disco file write blocked.

Target:  $FILE_PATH
Session: $TMUX_SESSION  (not a *-disco-sub-* sub-CXO session)

Discoveries can only be written by properly-spawned sub-CXO sessions.

To proceed legitimately:
  1. Write a 1-page seed brief at /home/jdm/inbox/!<WARRIOR> DOCS!/Discovery/seed-<scope>.md
  2. Run:
       bash scripts/spawn-subcxo-disco.sh \\
         --parent <WARRIOR>           # SHINOB1 / MUSASHI / MEGAZORD / VOLTRON / TAIKO / RONIN
         --scope-id <scope-id>         # kebab-case
         --brief <abs-path-to-brief>
  3. The sub-CXO session writes the disco; you ACK in your bilateral channel.

ZRD-SCOPE-005-1 v1.1 · SCOPE-005-1-L
EOF
exit 1
