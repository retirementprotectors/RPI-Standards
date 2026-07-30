#!/usr/bin/env bash
# check_pre_tmux_kill.test.sh — behavioural proof for the death-gate's merge half.
#
# TRK-HOOK-210 (ronin, 2026-07-30).
#
# WHY THIS EXISTS
# ---------------
# The gate read `exit_gate.disco_pr_merged`, a FLAG, with five independent things standing
# between it and the truth it claimed to report. The flag had never once been set for the live
# disco-sub, so the gate could not pass — and the seat was closed through it anyway. A gate
# that cannot pass does not get satisfied, it gets forced past, and nothing records the bypass
# because there is nothing to record.
#
# So the merge half now asks GitHub. This file proves that it does, and — equally important —
# proves it did NOT tighten anything on the way. Two seats nearly shipped a tightening as a
# correctness fix on this contract; a gate repair that quietly starts blocking a new path is
# the same failure wearing a fix's clothes.
#
# THE DEMONSTRATION IS AGAINST A REAL MERGED PR, not a fixture. Acceptance for this ticket was
# explicitly "merge a real PR and watch the gate resolve from that" — setting a flag and
# watching it pass would prove the flag works and nothing about the gate.
#
# RUN
#     bash hookify/scope-bound/check_pre_tmux_kill.test.sh
# Exit 0 = all pass. Requires gh for case 2; case 2 SKIPS loudly without it rather than
# silently passing, because a skipped live check that prints nothing is how a green board
# certifies an unverified claim.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="${HERE}/check_pre_tmux_kill.sh"
# ⚠️ THIS OVERRIDE IS THE REASON CASE 0 EXISTS. Read both together.
#
# Cases 1-5 export FORGE_STATE_LOAD so they can exercise the merge-half logic at all. That is
# a configuration PRODUCTION DOES NOT HAVE, and on a ticket whose subject is that the DEFAULT
# resolution is broken, a suite that only ever runs with the override CERTIFIES THE FIX AND
# CANNOT OBSERVE THE BUG.
#
# I shipped that in the first cut of this file and flagged it rather than quietly correcting
# it, because a test that passed for the wrong reason and got silently fixed leaves the next
# reader with the same false confidence I had.
#
# Case 0 therefore runs FIRST, with NO override, and asserts the default path as a real
# session computes it.
export FORGE_STATE_LOAD="${FORGE_STATE_LOAD:-/home/jdm/Projects/toMachina/scripts/forge-state-load.mjs}"

PASS=0
FAIL=0
ok()   { PASS=$((PASS+1)); echo "  pass  $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }

echo "=== 0. DEFAULT LOADER RESOLUTION — no override, the way a real session computes it ==="
# ⚠️ THIS CASE ASSERTS A KNOWN DEFECT AS PRESENT, not as fixed. Do not "make it pass."
#
# check_pre_tmux_kill.sh derives the loader from SCRIPT_DIR/../../.. — which is
# /home/jdm/Projects, one directory too high — then exits 0 at the `[[ ! -f ]]` guard before
# reading either exit_gate field. Measured on the live box: 233 firings, 233 passes, 0 blocks.
# The gate has never read a field in its life, and every other break we catalogued sits
# DOWNSTREAM of this one.
#
# THE MERGE-HALF FIX IN THIS PR DELIBERATELY DOES NOT REPAIR IT. Repairing the path ALONE
# makes every disco-sub on the fleet unkillable, because disco_pr_merged is never written
# today either. Path fix + parent_ack reduction ship as ONE UNIT, under doctrine audit.
#
# So this case pins the defect so it is VISIBLE and so the one-unit build has to change this
# assertion deliberately rather than discover it. Declaring a limit is a pass; hiding it
# behind an override is what made the first cut of this file worthless.
_SD="$HERE"
_GUESS="$(cd "${_SD}/../../.." && pwd)/scripts/forge-state-load.mjs"
echo "        default resolves to: ${_GUESS}"
if [ ! -f "$_GUESS" ]; then
  ok "default loader path does NOT exist — the documented defect is still present as expected"
else
  bad "default loader path now EXISTS. If the one-unit fix landed, UPDATE THIS CASE and re-run
        cases 1-5 without the override — do not simply delete this assertion."
fi
_OUT0=$(env -u FORGE_STATE_LOAD timeout 60 bash "$CHECK" "shinob1-disco-sub-hookify-overhaul-001" 2>&1); _RC0=$?
if [ $_RC0 -eq 0 ] && [ -z "$_OUT0" ]; then
  ok "with NO override the gate exits 0 silently — it never reaches either exit_gate field"
else
  bad "unexpected behaviour with no override (rc=$_RC0) — re-read this case before changing it"
fi

echo
echo "=== 1. a non-sub session is not this gate's business ==="
OUT=$(bash "$CHECK" "RONIN-HOOKIFY-OVERHAUL" 2>&1); RC=$?
[ $RC -eq 0 ] && ok "ordinary session passes through (rc=0)" \
             || bad "ordinary session should pass through, got rc=$RC"

echo
echo "=== 2. the merge half resolves from a REAL merged PR, not from the flag ==="
if ! command -v gh >/dev/null 2>&1; then
  echo "  SKIP  gh not available — this case is UNVERIFIED, not passed."
else
  OUT=$(timeout 120 bash "$CHECK" "shinob1-disco-sub-hookify-overhaul-001" 2>&1)
  if grep -q "disco_pr_merged: true" <<<"$OUT" && grep -q "VERIFIED LIVE: #" <<<"$OUT"; then
    ok "merge half TRUE, sourced from a real merged PR and named in the output"
    echo "        $(grep -o 'VERIFIED LIVE: #[0-9]* merged [^)]*' <<<"$OUT" | head -1)"
  else
    bad "merge half did not resolve from GitHub — got: $(grep -m1 'disco_pr_merged' <<<"$OUT")"
  fi
  # The Firestore flag for this session is absent (the exit_gate object was never seeded), so
  # a TRUE here cannot have come from the flag. That is what makes this a real demonstration.
  if grep -q "lookup: verified live" <<<"$OUT"; then
    ok "provenance is stated — the verdict names where it came from"
  else
    bad "verdict did not state its provenance"
  fi
fi

echo
echo "=== 3. NO DOC and DOC-BUT-SILENT are different paths, and only one blocks ==="
# This case initially asserted that an unknown scope BLOCKS. It does not, and the failing test
# is what surfaced my own bad assumption — the assertion was wrong, not the code.
#
# The spec (check_pre_tmux_kill.sh:56-62) allows a sub-shaped session with NO Firestore doc
# straight through: CLI rc != 0 -> exit 0. The path that HARD BLOCKS is a doc that EXISTS and
# is silent on exit_gate — which is precisely what stranded the live disco-sub, and which
# everyone (me included) had been describing as "the doc never got the field."
#
# Locking the distinction here because conflating the two is what made the diagnosis wrong for
# most of an evening: absence is permitted, silence is not.
OUT=$(timeout 120 bash "$CHECK" "ghost-disco-sub-scope-that-does-not-exist-zzz" 2>&1); RC=$?
if [ $RC -eq 0 ]; then
  ok "sub-shaped session with NO Firestore doc passes through (spec :56-62 — absence is allowed)"
else
  bad "a session with no doc should pass through, got rc=$RC"
fi
# And the contrast: the live session's doc EXISTS and has no exit_gate object, so it reaches
# the blocking path rather than the allowed one. Case 2 above already proved it gets there.
if grep -q "parent_ack:      false" <<<"$(timeout 120 bash "$CHECK" "shinob1-disco-sub-hookify-overhaul-001" 2>&1)"; then
  ok "doc-exists-but-silent reaches the blocking path (the state that stranded the live sub)"
else
  bad "doc-exists-but-silent did not reach the blocking path"
fi

echo
echo "=== 4. NO TIGHTENING: with gh unreachable the gate behaves exactly as before ==="
# Mask gh so the lookup cannot run. The pre-existing behaviour was: flag false -> BLOCK.
# It must still be BLOCK — not allow (that would be a silent weakening) and not a crash.
FAKEBIN=$(mktemp -d)
printf '#!/usr/bin/env bash\nexit 127\n' > "$FAKEBIN/gh"; chmod +x "$FAKEBIN/gh"
OUT=$(PATH="$FAKEBIN:$PATH" timeout 120 bash "$CHECK" "shinob1-disco-sub-hookify-overhaul-001" 2>&1); RC=$?
rm -rf "$FAKEBIN"
if [ $RC -eq 1 ]; then
  ok "gh unreachable still BLOCKS — the repair did not weaken the closed path"
else
  bad "gh unreachable changed the verdict (rc=$RC) — that is a silent weakening"
fi
if grep -q "COULD NOT LOOK" <<<"$OUT"; then
  ok "'could not look' is distinguished from 'not merged' (death-gate.sh's taxonomy)"
else
  bad "a failed lookup was not distinguished from an unmerged PR"
fi

echo
echo "=== 5. the parent_ack half is DECLARED, not silently dropped ==="
OUT=$(timeout 120 bash "$CHECK" "shinob1-disco-sub-hookify-overhaul-001" 2>&1)
if grep -q "STILL REQUIRED BY DOCTRINE" <<<"$OUT" && grep -q "TRK-HOOK-219" <<<"$OUT"; then
  ok "message separates 'required by doctrine' from 'verified by this gate', and routes the fix"
else
  bad "the parent_ack limit is not declared in terms a hurried reader can act on"
fi

echo
echo "======================================================================"
if [ $FAIL -gt 0 ]; then
  echo "FAILED — $FAIL case(s), $PASS passed"
  exit 1
fi
echo "PASSED — $PASS checks."
echo "         The merge half reads REALITY and names its evidence; a failed lookup is"
echo "         distinguished from an unmerged PR; the closed path is unchanged; and the"
echo "         unverifiable half is declared rather than quietly dropped."
exit 0
