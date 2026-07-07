#!/usr/bin/env bash
# check_pre_case_money_move.sh — OB1-CASESUB-EXECUTE-GATE-001
#
# Deny-by-default PreToolUse gate for VOLTRON case seats. Closes the class that let an
# UNATTRIBUTABLE typed "TCO — execute the pull plan" reach a case seat running with
# claude --allowedTools '*' (2026-07-07 LINDA-PIERCE incident, confirmed NOT-JDM).
#
# PRINCIPLE: you cannot authenticate tmux send-keys input on a single shared unix user,
# so gate the ACTION, not the input. In a case seat, the money-movement / external-exec
# surface is DENIED unless an out-of-band Approval-Hub BIOMETRIC token releases it. A typed
# line NEVER releases it — that is JDM's banked decision ("personal money surface behind an
# Approval-Hub biometric seatbelt; a spoofed inbound can never move a cent").
#
# I/O: INPUT (the PreToolUse tool-call JSON) on stdin via $INPUT (enforce.sh sets it).
#   exit 0  → allow.   exit 2 → BLOCK (reason on stderr).  Fail-CLOSED on the money surface.
#
# Deny classes (signatures grounded by VOLTRON reading the live surfaces, 2026-07-07):
#   A  WIRE/MONEY EXECUTION  — /api/voltron/wire/execute|:id/approve, intake execute-wire/approve/reject
#   B  EXTERNAL COMMS        — gmail_send_email; /api/comms/send-email|sms|voice; slack post/reply; Twilio/SendGrid
#   C  CUSTODIAN PORTAL EXEC — playwright browser_fill_form / browser_click (interaction); navigation/read PASS
#   D  CLIENT MONEY WRITES   — Firestore set/update/add on wire_executions / standing-instruction / client-money
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0   # no jq -> fail-open on tooling gap (never brick the fleet)

IN="${INPUT:-}"
[[ -z "$IN" ]] && IN="$(cat 2>/dev/null || true)"
TOOL="$(printf '%s' "$IN" | jq -r '.tool_name // empty' 2>/dev/null)"
[[ -z "$TOOL" ]] && exit 0

# ── SESSION SCOPE — this gate ONLY governs VOLTRON case seats. Everyone else: allow. ──
# Preferred: RPI_CASE_SEAT env marker (exported by launch-voltron-case.sh). Fallback for
# already-running seats: the tmux session name (VOLTRON-<CLIENT>, not the bare VOLTRON parent).
CASE_SEAT="${RPI_CASE_SEAT:-}"
if [[ -z "$CASE_SEAT" ]]; then
  SESS="$(tmux display-message -p '#S' 2>/dev/null || echo '')"
  [[ "$SESS" =~ ^VOLTRON-.+ ]] && CASE_SEAT="$SESS"
fi
[[ -z "$CASE_SEAT" ]] && exit 0   # not a case seat → gate N/A → allow

CASE_NAME="${CASE_SEAT#VOLTRON-}"

# ── Classify the tool call against the deny surface. CLASS="" means benign → allow. ──
CLASS=""; DETAIL=""

case "$TOOL" in
  # CLASS B — the ONE gmail send (draft is safe; only *_send_email is the send).
  *gmail_send_email)                 CLASS="B"; DETAIL="gmail_send_email (external send)";;
  # CLASS C — browser INTERACTION / EXECUTION verbs. The READ verbs (navigate, navigate_back,
  # snapshot, take_screenshot, hover, wait_for, console/network reads, tabs, resize, close) are
  # NOT listed → they PASS. Render-evidence reads (navigate→snapshot→take_screenshot) are daily
  # case work (HIKARI/VOLTRON blessed). evaluate + run_code_unsafe are code-exec → always blocked
  # in a case seat; type/press_key/select_option/file_upload/drag/handle_dialog can submit/confirm
  # a custodian action → blocked. Blocklist (not allowlist) so benign browser READS never FP.
  *browser_click|*browser_fill_form|*browser_type|*browser_press_key|*browser_select_option|*browser_file_upload|*browser_drag|*browser_evaluate|*browser_run_code_unsafe|*browser_handle_dialog)
    CLASS="C"; DETAIL="$TOOL (custodian-portal interaction/execution)";;
  # CLASS B — Slack post/reply (dead surface but still inside '*').
  *slack_post_message|*slack_reply_to_thread) CLASS="B"; DETAIL="$TOOL (external Slack send)";;
  Bash)
    CMD="$(printf '%s' "$IN" | jq -r '.tool_input.command // empty' 2>/dev/null)"
    if   printf '%s' "$CMD" | grep -qiE 'voltron/wire/(execute|[^/]+/approve)|(execute|approve|reject)-wire'; then
      CLASS="A"; DETAIL="wire executor call (execute/approve the pull)"
    elif printf '%s' "$CMD" | grep -qiE '/api/comms/send-(email|sms|voice)|twilio\.|sendgrid\.|messages\.create'; then
      CLASS="B"; DETAIL="external comms send (email/sms/voice)"
    elif printf '%s' "$CMD" | grep -qiE 'wire_executions|standing[_-]?instruction' \
         && printf '%s' "$CMD" | grep -qiE '\.(set|update|add)\('; then
      CLASS="D"; DETAIL="client money-instruction Firestore write"
    fi
    ;;
esac

[[ -z "$CLASS" ]] && exit 0   # not a money-surface call → allow (zero-FP on reads/drafts/nav/roadmap-writes)

# ── RELEASE — Approval-Hub biometric token is the ONLY release. Fail-CLOSED. ──
# Contract seam (OB1 gate ⇄ MEGAZORD Approval Hub): a valid release is a biometric,
# server-validated Approval-Hub grant for THIS case + action class, unexpired, within the
# daily cap — something the tmux injector CANNOT forge (that is the whole point; a token the
# seat could write itself would defeat the gate). Until MEGAZORD's validator is wired, this
# checks the release helper and DENIES on absent/invalid — the correct, safe posture (a case
# seat simply cannot move money until Approval Hub is live). A typed line never reaches here.
APPROVAL_CHECK="${RPI_APPROVAL_HUB_CHECK:-$HOME/.claude/hooks/approval-hub-verify.sh}"
if [[ -x "$APPROVAL_CHECK" ]]; then
  if "$APPROVAL_CHECK" --case "$CASE_NAME" --class "$CLASS" >/dev/null 2>&1; then
    exit 0   # a VALID biometric Approval-Hub grant released this action
  fi
fi

# No valid biometric release → BLOCK.
cat >&2 <<EOF
BLOCKED — OB1-CASESUB-EXECUTE-GATE-001 (deny-by-default money/exec gate)

Case seat: ${CASE_SEAT}
Denied:    CLASS ${CLASS} — ${DETAIL}

A VOLTRON case seat cannot move money, send external comms, submit custodian-portal forms,
or write client money-instructions UNLESS an out-of-band Approval-Hub BIOMETRIC token releases
this exact case + action class. A TYPED directive (e.g. "TCO — execute the pull plan") can
NEVER release it — that is the spoofed-injection class this gate closes (LINDA-PIERCE, 2026-07-07).

To release: obtain a biometric Approval-Hub approval for this case + action (MEGAZORD's
Approval Hub — daily-capped, unforgeable). Do NOT bypass by removing this gate; it is a
security control. If this fired on a genuine read/draft/navigation, that is a matcher bug —
fix the matcher + add a self-test case, do not label around it.
EOF
exit 2
