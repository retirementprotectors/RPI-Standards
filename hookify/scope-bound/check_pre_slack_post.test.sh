#!/usr/bin/env bash
# check_pre_slack_post.test.sh — self-test for TRK-HOOK-211 (scope-bound slice).
#
# WHY THIS FILE EXISTS. The reachability instrument scored this gate's RULE
# "reachable-clean" and said nothing about whether its CHECK could ever succeed.
# It could not: the active-sub branch was guarded on an artifact it never invoked,
# at a path that could never exist, so a fully-satisfied precondition still
# blocked. VACUOUS RED — a gate with no achievable pass condition. Every other
# defect on this contract could not FAIL; this one could not PASS. Both carry
# zero bits, and the red form is worse: an always-red gate gets forced past, and
# a gate always bypassed teaches the fleet that gates are noise.
#
# So the acceptance here is DEMONSTRATE THE GREEN, not "the code looks right":
# construct the real precondition and watch exit 0, construct its absence and
# watch it refuse. Both directions, every run.
#
# Exit 0 only if every case passes.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/check_pre_slack_post.sh"

fail=0
# run <expected-exit> <name> <input-json> [env assignments...]
run() {
  local want="$1" name="$2" json="$3"; shift 3
  local got=0
  INPUT="$json" env "$@" bash "$CHECK" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then
    echo "  PASS  $name"
  else
    echo "  FAIL  $name (want exit $want, got $got)"; fail=$((fail+1))
  fi
}

# Parent bilateral channel (SHINOB1) vs a non-parent channel.
PARENT_CH="C0AS0LETSBW"
OTHER_CH="C0ARUSZFKB8"

# A claim-shaped body: keyword + authoring verb in proximity, which is what the
# rule's regex is looking for.
CLAIM="Heads up — I am drafting the scope writeup for this initiative tonight."
BENIGN="status update: build is green, nothing else to report right now."

j() { jq -cn --arg c "$1" --arg t "$2" '{tool_name:"mcp__slack__slack_post_message", tool_input:{channel_id:$c, text:$t}}'; }

# A stub lister standing in for "an active sub-warrior exists in the window".
# The real forge-state-list.mjs prints a JSON array and exits 0 when non-empty;
# it prints [] and exits 1 when EMPTY (not on error — that exit code reads as
# failure and is not one). We reproduce the non-empty shape.
STUB_ACTIVE="$(mktemp)"
printf '#!/usr/bin/env bash\necho "[{\\"session\\":\\"shinob1-disco-sub-example\\"}]"\n' > "$STUB_ACTIVE"
chmod +x "$STUB_ACTIVE"
# And one standing in for "no active sub" — the real empty shape.
STUB_EMPTY="$(mktemp)"
printf '#!/usr/bin/env bash\necho "[]"\nexit 1\n' > "$STUB_EMPTY"
chmod +x "$STUB_EMPTY"

echo "== ALLOW-THROUGH (must PASS = exit 0, zero false-positives) =="
run 0 "channel is not a parent bilateral"            "$(j "$OTHER_CH"  "$CLAIM")"
run 0 "parent bilateral, no claim in the body"       "$(j "$PARENT_CH" "$BENIGN")"
run 0 "death-gate ACK (ACK + sub marker + a URL)"    "$(j "$PARENT_CH" "ACK on the -disco-sub- close, see https://example.invalid/pr/1")"
run 0 "sub's own completion post (session sentinel)" "$(j "$PARENT_CH" "$CLAIM [session:shinob1-disco-sub-example]")"
run 0 "no channel field at all (fail-open)"          "$(jq -cn --arg t "$CLAIM" '{tool_name:"x",tool_input:{text:$t}}')"

echo "== RED — claim in a parent bilateral with NO active sub (must REFUSE = exit 1) =="
run 1 "no lister wired at all"                       "$(j "$PARENT_CH" "$CLAIM")"
run 1 "lister reports empty (the real empty shape)"  "$(j "$PARENT_CH" "$CLAIM")" "HOOKIFY_FORGE_STATE_LIST=$STUB_EMPTY"

echo "== GREEN — the case that was IMPOSSIBLE before TRK-HOOK-211 (must ALLOW = exit 0) =="
# Before the fix this exited 1 with the precondition fully satisfied. If someone
# reintroduces a guard on an artifact this branch does not invoke, this case is
# the one that goes red — which is the whole point of asserting it.
run 0 "active sub present → post allowed"            "$(j "$PARENT_CH" "$CLAIM")" "HOOKIFY_FORGE_STATE_LIST=$STUB_ACTIVE"

rm -f "$STUB_ACTIVE" "$STUB_EMPTY"

echo ""
echo "== PINNED LIMIT — the transport this gate defends is decommissioned =="
# This is a defect we are deliberately NOT fixing here: enforce.sh enters this
# check on exactly one predicate, a Slack MCP tool name, and no Slack MCP server
# is wired on this box. So in production the check is never entered at all,
# independent of everything asserted above. Fixing the guard makes the gate
# correct and still dark; only a transport decision revives it, and that is not
# a builder's call.
#
# Declared in a TEST rather than a comment on purpose: a comment cannot fail a
# build, and this contract has already watched two seats "fix" a limit that was
# only written down in prose. If the transport ever returns, this goes red and
# somebody has to look at it.
ENFORCE="$HERE/../enforce.sh"
MCP_CFG="${HOME}/.mcp.json"
pin_fail=0

if ! grep -q 'slack_post_message' "$ENFORCE" 2>/dev/null; then
  echo "  FAIL  pin: enforce.sh no longer dispatches this check on the expected"
  echo "        predicate. The pin below is stale — re-derive how this check is"
  echo "        entered before trusting any result above."
  pin_fail=1
fi

if [[ -f "$MCP_CFG" ]] && grep -qi '"[^"]*slack[^"]*"[[:space:]]*:' "$MCP_CFG" 2>/dev/null; then
  echo "  FAIL  pin: a Slack MCP server is wired again. This gate has just become"
  echo "        LIVE for the first time since the transport was retired. Re-run"
  echo "        this matrix against the real dispatcher (not just this file),"
  echo "        confirm the active-sub lookup still reaches Firestore, and"
  echo "        re-verify TRK-HOOK-211 end to end before relying on it."
  pin_fail=1
fi

if [[ "$pin_fail" -eq 0 ]]; then
  echo "  PASS  pin: transport still absent — check is UNREACHABLE in production."
  echo "        Recorded as a declared limit, not a passing gate. The L2/L3"
  echo "        boundary question belongs to TRK-HOOK-208."
else
  fail=$((fail+1))
fi

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "✅ pre-slack-post self-test PASSED — allow-throughs clean, refuses without"
  echo "   an active sub, and ALLOWS with one (the green that could not previously"
  echo "   be reached). Transport limit pinned."
  exit 0
else
  echo "❌ pre-slack-post self-test FAILED — $fail case(s)."
  exit 1
fi
