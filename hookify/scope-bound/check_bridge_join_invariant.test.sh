#!/usr/bin/env bash
# check_bridge_join_invariant.test.sh — self-test for MZD-DATA-601 (L2 write-gate).
# TRK-HOOK-211 (bridge-join slice) · RONIN-W5 · 2026-07-30
#
# WHY THIS FILE EXISTS
# The six scope-bound rules each delegate their verdict to a check_*.sh, and the corpus
# audit found that not one had ever been DEMONSTRATED returning a substantive PASS. The
# reachability instrument calls these rules "reachable-clean", which is true and says
# nothing about whether the checker they delegate to can ever succeed. The sibling rule
# block-tmux-kill-without-exit-gate turned out to have NO achievable pass condition at all
# — a vacuous red, which is the worse failure, because an always-red gate gets forced past
# and teaches the fleet that gates are noise.
#
# So this file's first job is not to find bugs. It is to DEMONSTRATE THE GREEN: construct
# the real precondition, watch the check exit 0, construct its absence, watch it refuse.
# Both directions, or the gate is not known to work.
#
# Its second job is to PIN what the demonstration exposed. Where this test asserts a defect
# is PRESENT, that is deliberate: the defect is outside this seat's file boundary or is a
# governance call, so it is pinned rather than fixed, and the assertion fails loudly if it
# ever silently changes. A pinned defect that starts passing is NOT a test failure to
# suppress — it is a signal to update this file and tell HIKARI the ground moved.
#
# WHY EXIT-CODE ASSERTIONS ARE NOT ENOUGH (and what this does instead)
# The dispatcher writes a `::passed` log record on ANY zero exit from a check. This check
# reaches zero exit by seven distinct paths and five of them mean "the rule never applied"
# (wrong extension, empty content, tokens absent). Only two are a real invariant-satisfied
# pass. In the fire log they are indistinguishable — which is why the rule's 2,906 recorded
# passes are not evidence its checker works. This test therefore separates SUBSTANTIVE
# passes (the invariant was evaluated and satisfied) from VACUOUS ones (the rule declined to
# apply), and asserts on which kind it got.
#
# Run: bash check_bridge_join_invariant.test.sh   → exit 0 only if every expectation holds.

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/check_bridge_join_invariant.sh"
ENFORCE="$HERE/../enforce.sh"

fail=0
pass=0
note() { printf '        %s\n' "$1"; }
ok()   { pass=$((pass+1)); printf '  PASS  %s\n' "$1"; }
bad()  { fail=$((fail+1)); printf '  FAIL  %s\n' "$1"; }

# The invariant's tokens are assembled here rather than written as literals so this file can
# be quoted into a report or a warrior's prompt without arming a matcher in the reader's seat.
SIG_A="medicare""_signals"
SIG_B="retirement""_signals"
KEY="master""_record_id"
BRIDGE="call""_transcripts"
EXEMPT="bridge-join""-exempt"

json() { jq -cn --arg c "$1" '{tool_name:"Write",tool_input:{content:$c,file_path:"/tmp/probe.py"}}'; }

# run <expected-exit> <name> <file-path> <content>
run() {
  local want="$1" name="$2" fp="$3" content="$4" got=0
  INPUT="$(jq -cn --arg c "$content" '{tool_input:{content:$c}}')" "$CHECK" "$fp" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then ok "$name"; else bad "$name (want exit $want, got $got)"; fi
}

echo "== 1 · THE GREEN — the invariant is satisfiable, and refusal is reachable =="
# This is the acceptance. Everything else in this file is commentary on it.
run 1 "REFUSES: real table ref + key read, no bridge" "/tmp/q.py" \
  "SELECT $KEY FROM \`pmm.$SIG_A\` LIMIT 10"
run 0 "GREEN (substantive): the bridge join is present" "/tmp/q.py" \
  "SELECT t.$KEY FROM \`pmm.$SIG_A\` s JOIN \`pmm.$BRIDGE\` t USING (recording_id)"
run 0 "GREEN (substantive): declared bridge-less-by-design" "/tmp/q.py" \
  "# $EXEMPT: crm-notes source has recording_id=NULL, key is native
SELECT $KEY FROM \`pmm.$SIG_B\`"
run 1 "REFUSES the same bypass in .sql, not just .py" "/tmp/q.sql" \
  "SELECT $KEY FROM \`pmm.$SIG_B\`"
note "Both directions reached on the real conditions. This gate is NOT vacuous."

echo
echo "== 2 · VACUOUS zero-exits — real, expected, and NOT evidence of a working gate =="
# Each of these exits 0 because the rule declined to apply. The dispatcher logs all of them
# as ::passed, identically to section 1's substantive passes. That is the measurement gap.
run 0 "declines: prose file (.md) is out of scope"      "/tmp/q.md" "SELECT $KEY FROM \`pmm.$SIG_A\`"
run 0 "declines: empty content"                          "/tmp/q.py" ""
run 0 "declines: no signal-table token present"          "/tmp/q.py" "SELECT $KEY FROM clients"
run 0 "declines: gate never gates its own script"        "$HERE/check_bridge_join_invariant.sh" \
  "SELECT $KEY FROM \`pmm.$SIG_A\`"

echo
echo "== 3 · WHAT ELSE DOES IT NOW REFUSE — false-positive class, PINNED not fixed =="
# The merge-time twin (toMachina .github/scripts/bridge-join-matcher.js, MZD-DATA-602) was
# narrowed on 2026-07-24 under OB1-BRIDGE-JOIN-REGEX-001 after PR #2565 — a BQ-free local
# script reading a parsed NDJSON record — was falsely held. The twin now requires one of
# three real BQ-table shapes. THIS write-time half never received that correction: it still
# matches the bare token, so it refuses code the merge gate would pass.
# Aligning the two is a live-gate behaviour change on a BLOCK rule. Not taken unilaterally.
run 1 "PINNED FP: plain property access off a parsed record" "/tmp/q.js" \
  "const r = o.$SIG_A; const k = r.$KEY;"
run 1 "PINNED FP: a comment that merely names both concepts" "/tmp/q.py" \
  "# $SIG_A rows carry $KEY
x = 1"
note "If either flipped to exit 0, the halves were aligned — GOOD. Update this file, tell HIKARI."

echo
echo "== 4 · WHAT ELSE DOES IT NOW PERMIT — bypass class, PINNED not fixed =="
# Do not tighten a gate while fixing it. These are recorded so the blast radius is known,
# not closed here. Closing any of them widens what a live BLOCK rule refuses.
run 0 "PINNED BYPASS: derived/versioned table name escapes the word-boundary anchor" "/tmp/q.py" \
  "SELECT $KEY FROM \`pmm.${SIG_A}_v2\`"
run 0 "PINNED BYPASS: matching is case-sensitive; the twin is not" "/tmp/q.py" \
  "SELECT ${KEY^^} FROM PMM.${SIG_A^^}"
run 0 "PINNED BYPASS: the escape marker anywhere clears the WHOLE file" "/tmp/q.py" \
  "# see the $EXEMPT docs elsewhere in this repo
SELECT $KEY FROM \`pmm.$SIG_A\`"
run 0 "PINNED BYPASS: file-wide, not per-statement — 2nd query rides the 1st's join" "/tmp/q.py" \
  "q1 = \"SELECT t.$KEY FROM $SIG_A s JOIN $BRIDGE t USING (recording_id)\"
q2 = \"SELECT $KEY FROM $SIG_B\""
note "The published escape marker is quoted in the rule doc, the contract and the disco —"
note "pasting any of those samples into code disarms this gate for that whole file."

echo
echo "== 5 · CARRIER ENUMERATION — which tool calls actually reach this check =="
# Asserted through the REAL dispatcher, and asserted on this rule's OWN log record rather
# than on the dispatcher's exit code, so a sibling scope-bound rule's verdict can never be
# mistaken for ours. This is also the positive control: sections asserting "no record" are
# only trustworthy because the Write/Edit cases prove a record DOES appear when it should.
if [[ -x "$ENFORCE" ]] && command -v jq >/dev/null 2>&1; then
  LOG="$(mktemp)"
  carrier() { # <name> <expect: block|passed|none> <tool_json>
    local name="$1" expect="$2" json="$3" got
    : > "$LOG"
    HOOKIFY_VIOLATION_LOG="$LOG" bash "$ENFORCE" <<<"$json" >/dev/null 2>&1
    if   grep -q '"rule":"block-bridge-join-bypass"'        "$LOG"; then got=block
    elif grep -q '"rule":"block-bridge-join-bypass::passed"' "$LOG"; then got=passed
    else got=none; fi
    if [[ "$got" == "$expect" ]]; then ok "$name"; else bad "$name (want $expect, got $got)"; fi
  }
  V="SELECT $KEY FROM \`pmm.$SIG_A\` LIMIT 10"
  B="SELECT t.$KEY FROM \`pmm.$SIG_A\` s JOIN \`pmm.$BRIDGE\` t USING (recording_id)"
  carrier "Write dispatches, and blocks the bypass"  block  "$(jq -cn --arg c "$V" '{tool_name:"Write",tool_input:{content:$c,file_path:"/tmp/q.py"}}')"
  carrier "Write dispatches, and passes the bridged" passed "$(jq -cn --arg c "$B" '{tool_name:"Write",tool_input:{content:$c,file_path:"/tmp/q.py"}}')"
  carrier "Edit dispatches, and blocks the bypass"   block  "$(jq -cn --arg c "$V" '{tool_name:"Edit",tool_input:{new_string:$c,file_path:"/tmp/q.py"}}')"
  # PINNED CARRIER GAP. MultiEdit carries the identical bytes to the identical path and is
  # never dispatched, so this rule cannot see it AND the fire log cannot record that it
  # happened. A null in that log is therefore not evidence of absence — the instrument
  # shares the blind spot. Routed to TRK-HOOK-208 (L2/L3 boundary), not closed here.
  carrier "PINNED GAP: MultiEdit is not a dispatched carrier" none \
    "$(jq -cn --arg c "$V" '{tool_name:"MultiEdit",tool_input:{file_path:"/tmp/q.py",edits:[{old_string:"x",new_string:$c}]}}')"
  # NotebookEdit DOES dispatch (pre-notebook-edit), but that event has ZERO listeners across
  # the whole scope-bound corpus — the one dispatched event nothing subscribes to.
  carrier "PINNED GAP: pre-notebook-edit has zero listeners" none \
    "$(jq -cn --arg c "$V" '{tool_name:"NotebookEdit",tool_input:{notebook_path:"/tmp/q.ipynb",new_source:$c}}')"
  rm -f "$LOG"
else
  note "SKIP — dispatcher or jq unavailable; carrier enumeration not run."
fi

echo
echo "== 6 · L2/L3 PARITY — measured against the twin when it is reachable =="
# Never a false red: if the toMachina checkout or node is absent, this section reports SKIP
# rather than failing. The parity claim is only made when it is actually measured.
TWIN="${BRIDGE_JOIN_MATCHER:-$HOME/Projects/toMachina/.github/scripts/bridge-join-matcher.js}"
if command -v node >/dev/null 2>&1 && [[ -f "$TWIN" ]]; then
  parity() { # <name> <expect-agree: yes|no> <content>
    local name="$1" expect="$2" content="$3" l2=ALLOW l3 got
    INPUT="$(jq -cn --arg c "$content" '{tool_input:{content:$c}}')" "$CHECK" "/tmp/q.py" >/dev/null 2>&1 || l2=BLOCK
    l3="$(node -e '
      const m=require(process.argv[1]);
      process.stdout.write(m.evaluateAddedContent(process.argv[2],"q.py")?"BLOCK":"ALLOW");
    ' "$TWIN" "$content" 2>/dev/null)"
    [[ -z "$l3" ]] && { note "SKIP $name — twin did not evaluate"; return; }
    [[ "$l2" == "$l3" ]] && got=yes || got=no
    if [[ "$got" == "$expect" ]]; then ok "$name (L2=$l2 L3=$l3)"; else bad "$name (want agree=$expect, got $got; L2=$l2 L3=$l3)"; fi
  }
  parity "agree: real table ref, un-bridged"     yes "SELECT $KEY FROM \`pmm.$SIG_A\`"
  parity "agree: bridged"                        yes "SELECT t.$KEY FROM \`pmm.$SIG_A\` s JOIN \`pmm.$BRIDGE\` t USING (recording_id)"
  parity "agree: declared exempt"                yes "// $EXEMPT: crm-notes
const k = row.$KEY"
  parity "PINNED DIVERGENCE: property access"    no  "const r = o.$SIG_A; const k = r.$KEY;"
  parity "PINNED DIVERGENCE: naming comment"     no  "# $SIG_A rows carry $KEY
x = 1"
else
  note "SKIP — node or the twin matcher is not reachable from here."
fi

echo
echo "─────────────────────────────────────────────────────────"
if [[ "$fail" -eq 0 ]]; then
  echo "check_bridge_join_invariant self-test: all green ($pass checks)"
  echo "The gate has an achievable PASS and an achievable REFUSAL. Both demonstrated."
  exit 0
fi
echo "check_bridge_join_invariant self-test: $fail FAILED, $pass passed"
echo
echo "If a PINNED case failed, the pinned defect may have been FIXED — that is good news,"
echo "not a break. Confirm the fix, update the pin in this file, and report it to HIKARI"
echo "so the L2/L3 boundary ledger (TRK-HOOK-208) stays true."
exit 1
