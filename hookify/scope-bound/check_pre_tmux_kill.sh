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

# ── TRK-HOOK-210 (ronin, 2026-07-30) — READ REALITY FOR THE MERGE HALF ──────────────────
#
# WHAT WAS BROKEN. `exit_gate.disco_pr_merged` is a FLAG, and five independent things stand
# between that flag and the truth it claims to report:
#   1. parent_ack flips only on a Slack reaction_added — that transport is decommissioned
#   2. disco_pr_merged flips only on a GitHub webhook to POST /api/forge/exit-gate
#   3. the exit_gate OBJECT is never seeded on the launcher path — only seedRunState creates
#      it, so the doc exists and is silent, and `// false` DEFAULTS rather than reads
#   4. exit-gate.ts:37 derives the session from the PR branch via ^(\w+)-disco-sub-(\S+)$ —
#      \w+ cannot match a slash, and the fleet's convention is <warrior>/<TICKET>. Measured
#      against every branch this contract used: 0 of 7 match. It is a convention mismatch,
#      not a typo, so no better regex fixes it.
#   5. parent_ack_channel is the EMPTY STRING — the ack has no destination even if the
#      transport returned
#
# Every one of those is a mechanism that REPORTS reality instead of BEING it. So this half
# now asks GitHub directly. The flag is kept as a FALLBACK, never as the primary.
#
# RESOLUTION IS BY SCOPE, NOT BY BRANCH NAME — break 4 is unfixable at the regex level, so
# the branch is not consulted at all. The session's scope slug is matched against the
# `scope:` line in merged PR bodies, case-insensitively.
#
# ⚠️ DECLARED LIMIT: scope → PR is ONE-TO-MANY. This verifies "a merged PR carrying this
# scope exists", NOT "the disco PR specifically". The satisfying PR is NAMED in the output so
# the verdict is auditable rather than asserted. Narrowing it further needs a scope→PR
# registry that does not exist today.
#
# "COULD NOT LOOK" IS NOT "NOT MERGED" — inherited from dojo-warriors/scripts/death-gate.sh
# (OB1-DEATHGATE-REPO-RESOLVE-001), which documents three observed failure modes from getting
# this wrong, including a FALSE PASS where "the guard reads green precisely when it has
# verified nothing." Cited, not copied: that script performs a close, this one is a predicate.
#
# THIS DOES NOT TIGHTEN THE GATE. Every tooling gap falls back to the pre-existing flag
# behaviour, so a box without gh or without network behaves exactly as it did before. Fixing
# a gate is not a licence to make it stricter on a path nobody asked about.
GATE_REPO="${FORGE_DISCO_REPO:-retirementprotectors/toMachina}"
SCOPE_SLUG="${SESSION_NAME#*-disco-sub-}"
PR_EVIDENCE=""
PR_LOOKUP="not attempted"

if [[ "$PR_MERGED" != "true" && -n "$SCOPE_SLUG" ]] && command -v gh >/dev/null 2>&1; then
  set +e
  MATCHED=$(timeout 25 gh pr list --repo "$GATE_REPO" --state merged --limit 40 \
      --json number,body,mergedAt \
      -q "[.[] | select(.body != null and (.body|test(\"scope:.*${SCOPE_SLUG}\";\"i\")))] \
          | sort_by(.mergedAt) | last | \"#\(.number) merged \(.mergedAt)\"" 2>/dev/null)
  GH_RC=$?
  set -e
  if [[ $GH_RC -ne 0 ]]; then
    PR_LOOKUP="COULD NOT LOOK (gh rc=${GH_RC}) — this is not 'your PR is unmerged'"
  elif [[ -n "$MATCHED" && "$MATCHED" != "null" ]]; then
    PR_MERGED="true"
    PR_EVIDENCE="$MATCHED"
    PR_LOOKUP="verified live in ${GATE_REPO}"
  else
    PR_LOOKUP="no merged PR in ${GATE_REPO} carries scope '${SCOPE_SLUG}'"
  fi
fi

# ── TRK-HOOK-218 (ronin, 2026-07-30) — DOES ANYTHING STILL POINT AT THIS SEAT? ──────────
#
# disco_pr_merged and parent_ack can both be legitimately true while work is still
# ROUTED to this seat — that combination is exactly how a correct, agreed, well-timed
# close orphans something. Two real instances, not hypothetical: seat-routed-enumerate.mjs
# was built from `shinob1-disco-sub-rpi-medicare-bob-valuation-001` and
# `megazord-disco-sub-mwm-book-ingestion`, both closed 2026-07-07 with a pending item still
# unhomed 23 days later. Routing was never among this gate's inputs; now it is.
#
# THIS SCOPE DOES NOT OWN THE ENUMERATION — TRK-HOOK-218 (RONIN-HOOKIFY-W6) built and owns
# scripts/seat-routed-enumerate.mjs; this call is the integration point it deliberately did
# not wire itself. Three-way exit code, kept distinct rather than collapsed to pass/fail:
#   0 nothing routed here → clear   1 open item names this seat → BLOCK
#   2 CANNOT-RUN (store unreadable / population empty) → BLOCK, never treated as clean
# Missing tooling (no node, no script at the resolved path) is the one case that falls
# open, consistent with this file's existing FORGE_STATE_LOAD posture — an infra gap is
# not license to hard-block a path nobody wired yet, but it is never silently reported as
# "checked clean".
SEAT_ROUTED_ENUMERATE="${SEAT_ROUTED_ENUMERATE:-/home/jdm/Projects/dojo-warriors/scripts/seat-routed-enumerate.mjs}"
ROUTING_CLEAR="true"
ROUTING_VERDICT="not checked — enumeration script unavailable at ${SEAT_ROUTED_ENUMERATE}"
ROUTING_OUT=""

if command -v node >/dev/null 2>&1 && [[ -f "$SEAT_ROUTED_ENUMERATE" ]]; then
  set +e
  ROUTING_OUT=$(node "$SEAT_ROUTED_ENUMERATE" "$SESSION_NAME" 2>&1)
  ROUTING_RC=$?
  set -e
  case "$ROUTING_RC" in
    0) ROUTING_CLEAR="true";  ROUTING_VERDICT="clean — nothing routed to ${SESSION_NAME}" ;;
    1) ROUTING_CLEAR="false"; ROUTING_VERDICT="BLOCKED — open item(s) are routed to ${SESSION_NAME}" ;;
    2) ROUTING_CLEAR="false"; ROUTING_VERDICT="CANNOT-RUN — routing store unreadable; refusing to treat as clean" ;;
    *) ROUTING_CLEAR="false"; ROUTING_VERDICT="unexpected exit ${ROUTING_RC}; refusing to treat as clean" ;;
  esac
fi

if [[ "$PR_MERGED" == "true" && "$PARENT_ACK" == "true" && "$ROUTING_CLEAR" == "true" ]]; then
  exit 0
fi

cat >&2 <<EOF
BLOCKED: tmux kill-session requires exit gate to be fully open.

Current gate state for ${SESSION_NAME}:
  disco_pr_merged: ${PR_MERGED}${PR_EVIDENCE:+  (VERIFIED LIVE: ${PR_EVIDENCE})}
      lookup: ${PR_LOOKUP}
  parent_ack:      ${PARENT_ACK}
  routed_items:    ${ROUTING_VERDICT}

To open the gate:
  1. A PR carrying scope '${SCOPE_SLUG}' must be MERGED in ${GATE_REPO}.
     This is now read from GitHub directly (TRK-HOOK-210); the Firestore flag is
     only a fallback. If the lookup line above says COULD NOT LOOK, the gate did
     not fail your PR — it failed to reach GitHub. Those are different problems.

  2. parent_ack — ⚠️ READ THIS BEFORE CHASING IT.
     PARENT ACK IS STILL REQUIRED BY DOCTRINE. This GATE cannot VERIFY it, and the
     two statements are different. There is currently NO live signal a parent can
     emit that this check could read: the Slack transport is decommissioned,
     parent_ack_channel is empty, formal GitHub approvals are structurally
     impossible (the fleet is one identity), and the attestation convention appears
     on roughly 1 merged PR in 50 and is SELF-DECLARED TEXT by its own header
     (.github/workflows/verify-signer-not-builder.yml:44-52 — "THIS CHECK'S PASS
     RATE IS NOT EVIDENCE THAT signer≠builder IS ENFORCED").
     Defining a signal a parent can actually EMIT is TRK-HOOK-219 (ARCH, SHINOB1).
     Until it exists, get your parent's ACK the way you already do — this gate just
     stops pretending it checked.

  3. routed_items (TRK-HOOK-218) — nothing may still name this seat as its home.
     If BLOCKED, re-home each open item to a live seat (or its warrior) before
     closing. If CANNOT-RUN, the routing store could not be read — fix that before
     retrying; do not force past it, that is the exact failure mode this closes.
     Detail:
${ROUTING_OUT}

Do NOT kill this session until all three are true.
ZRD-SCOPE-005-001 / TRK-14758 Death-Gate Protocol.
EOF
exit 1
