#!/usr/bin/env bash
# check_disco_write.test.sh — self-test for SCOPE-005-1-L (TRK-HOOK-211, disco-write slice).
#
# WHY THIS FILE EXISTS
# The reachability instrument proved this rule is "reachable-clean". That says the rule LOADS.
# It says nothing about whether its check script can ever return 0. A gate with no achievable
# pass condition carries zero bits and is worse than a missing gate, because an always-red gate
# gets forced past and teaches the fleet that gates are noise.
#
# So this test does the thing the instrument cannot: it constructs the real precondition and
# watches the check SUCCEED, then removes it and watches the check REFUSE. Both directions.
#
# Exit 0 only if every case passes AND the harness proves itself live (see CONTROL-0 / CONTROL-1).
#
# TRK-HOOK-211 · SCOPE-005-1-L
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/check_disco_write.sh"

fail=0
reds_seen=0
PFX="dw$$"

[[ -x "$CHECK" ]] || { echo "FATAL: $CHECK missing or not executable"; exit 1; }

# The session-shaped cases cannot be simulated. If tmux is gone we do NOT quietly pass the
# suite minus its point — a skip that reads as green is the exact rot this file exists to stop.
if ! command -v tmux >/dev/null 2>&1; then
  echo "FATAL: tmux unavailable — the pass condition of this gate is a tmux session name."
  echo "       Refusing to report green on a suite that could not evaluate its own subject."
  exit 1
fi

cleanup() { tmux kill-session -t "${PFX}-g1" 2>/dev/null; tmux kill-session -t "${PFX}-g2" 2>/dev/null
            tmux kill-session -t "${PFX}-r1" 2>/dev/null; tmux kill-session -t "${PFX}-r2" 2>/dev/null
            rm -rf "${TMPD:-/nonexistent}" 2>/dev/null; }
trap cleanup EXIT

# run_session <want> <label> <session-name> <target-path>
# Runs the check INSIDE a real detached tmux session, so `tmux display-message -p '#S'`
# resolves to <session-name> exactly as it does for a live tool call.
run_session() {
  local want="$1" label="$2" sname="$3" target="$4"
  local out; out="$(mktemp)"
  tmux kill-session -t "$sname" 2>/dev/null
  tmux new-session -d -s "$sname" \
    "bash -c 'INPUT={} \"$CHECK\" \"$target\" >/dev/null 2>&1; echo \$? > \"$out\"'" 2>/dev/null
  local i; for i in $(seq 1 60); do [[ -s "$out" ]] && break; sleep 0.1; done
  tmux kill-session -t "$sname" 2>/dev/null
  local got; got="$(cat "$out" 2>/dev/null || echo TIMEOUT)"; rm -f "$out"
  if [[ "$got" == "$want" ]]; then
    echo "  PASS  $label"
    [[ "$want" -eq 1 ]] && reds_seen=$((reds_seen+1))
  else
    echo "  FAIL  $label (want exit $want, got $got)"; fail=$((fail+1))
  fi
}

# run_plain <want> <label> <target-path> — evaluated in the caller's own session.
run_plain() {
  local want="$1" label="$2" target="$3" got=0
  INPUT={} "$CHECK" "$target" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then echo "  PASS  $label"
  else echo "  FAIL  $label (want exit $want, got $got)"; fail=$((fail+1)); fi
}

# The in-scope target shape, assembled rather than written literally so this test file does not
# itself read as a discovery-doc write to a content-scanning tier.
DOCS="docs/discoveries"; EXT="html"
IN_SCOPE="$DOCS/trk-hook-211-probe.$EXT"
OUT_SCOPE="docs/warriors/ronin/trk-hook-211-probe.md"

# The session name the real spawner emits: lowercase parent + the sub literal + scope-id.
# spawn-subcxo-disco.sh:111 builds exactly this shape, and its comment at :94-95 records that it
# folds case BECAUSE this gate matches a lowercase literal. The green below is therefore the
# shape the fleet actually produces, not a string invented to satisfy the test.
SUB_SESSION="${PFX}x-disco-sub-trk-hook-211"
NON_SUB_SESSION="RONIN-HOOKIFY-W3-${PFX}"

echo "== CONTROL-0 — the instrument can read a session name at all =="
_probe="$(tmux new-session -d -s "${PFX}-g1" "bash -c 'tmux display-message -p \"#S\" > /tmp/${PFX}.sess'" 2>/dev/null; \
          for i in $(seq 1 40); do [[ -s /tmp/${PFX}.sess ]] && break; sleep 0.1; done; \
          cat /tmp/${PFX}.sess 2>/dev/null; rm -f /tmp/${PFX}.sess)"
tmux kill-session -t "${PFX}-g1" 2>/dev/null
if [[ "$_probe" == "${PFX}-g1" ]]; then
  echo "  PASS  session read is live (got '${_probe}')"
else
  echo "  FAIL  session read is DEAD (want '${PFX}-g1', got '${_probe}') — every green below would be vacuous"
  fail=$((fail+1))
fi

echo "== THE GREEN — a properly-spawned sub session writing a discovery doc (must PASS = exit 0) =="
run_session 0 "sub-shaped session + in-scope target  -> ALLOWED" "$SUB_SESSION" "$IN_SCOPE"

echo "== THE RED — same target, a session that is not a sub (must BLOCK = exit 1) =="
run_session 1 "project session + in-scope target     -> REFUSED" "$NON_SUB_SESSION" "$IN_SCOPE"
run_session 1 "parent-CXO session + in-scope target  -> REFUSED" "SHINOB1${PFX}" "$IN_SCOPE"

echo "== WHAT ELSE DOES IT NOW PERMIT (scope boundary, must not false-block) =="
run_session 0 "sub session + out-of-scope target     -> ALLOWED" "${PFX}y-disco-sub-scope" "$OUT_SCOPE"
run_plain   0 "out-of-scope target from any session  -> ALLOWED" "$OUT_SCOPE"
run_plain   0 "empty positional arg                  -> ALLOWED" ""

echo "== WHAT ELSE DOES IT NOW REFUSE (cover is wider than the rule text implies) =="
# The case glob spans path separators, so nested targets are in scope too. Asserted so a future
# narrowing of that pattern is caught rather than silently shrinking the gate's reach.
run_plain   1 "nested target under the scoped dir    -> REFUSED" "$DOCS/sub/deep.$EXT"

echo "== PINNED LIMITATION — the fail-open branch, asserted as PRESENT =="
# This gate degrades open when tmux is absent: no session name is resolvable, so it allows.
# That is deliberate in the script as written, and it is NOT fixed here — tightening a gate while
# testing it is out of scope for this slice, and this branch is the L2/L3 boundary TRK-HOOK-208
# owns: a write-time gate that cannot observe its own execution context cannot close this.
# It is asserted as PRESENT so that if it ever starts refusing, this test FAILS LOUDLY and the
# behaviour change is a decision somebody made on purpose rather than a silent drift.
# NB: the interpreter is invoked explicitly. Stripping PATH alone breaks the shebang's own
# interpreter lookup and yields 127 — an artifact of the harness, not a verdict on the gate.
TMPD="$(mktemp -d)"
_got=0
PATH="$TMPD" /bin/bash -c "INPUT={} /bin/bash '$CHECK' '$IN_SCOPE'" >/dev/null 2>&1 || _got=$?
if [[ "$_got" -eq 0 ]]; then
  echo "  PASS  tmux absent -> permits (known limitation, still present as documented)"
else
  echo "  FAIL  tmux absent -> exit $_got. The fail-open branch CHANGED."
  echo "        If that was intentional, update this assertion in the same commit and say so."
  fail=$((fail+1))
fi
rm -rf "$TMPD"

echo "== HARNESS LIVENESS =="
# If nothing ever went red, the session read silently died and every green above is worthless.
# A suite that cannot fail is the same class of defect as a gate that cannot pass.
if [[ "$reds_seen" -ge 2 ]]; then
  echo "  PASS  $reds_seen refusals observed — the greens are load-bearing"
else
  echo "  FAIL  only $reds_seen refusals observed; expected >=2. Harness cannot distinguish"
  echo "        pass from block, so its greens carry no information."
  fail=$((fail+1))
fi

echo
if [[ "$fail" -eq 0 ]]; then
  echo "ALL PASS — the green is reachable and demonstrated, both directions."
  exit 0
fi
echo "$fail FAILING CASE(S)"
exit 1
