#!/usr/bin/env bash
# check_disco_canonical_tabs.test.sh — self-test for SCOPE-DISCO-TABS-001 (TRK-HOOK-211).
#
# WHY THIS EXISTS
# TRK-HOOK-211: six scope-bound rules delegate their verdict to a check_*.sh, and not one had
# ever been DEMONSTRATED returning PASS. "reachable-clean" describes the RULE; it says nothing
# about whether the CHECK can ever succeed. A sibling checker was found this session that could
# never pass — a gate with no achievable pass condition (VACUOUS RED). An always-red gate gets
# forced past, and a gate always bypassed teaches the fleet that gates are noise.
#
# This test demonstrates the GREEN for check_disco_canonical_tabs.sh in BOTH directions:
# it constructs the real precondition and watches the check exit 0, then constructs its
# absence and watches it refuse. The checker itself is NOT modified — it needed no fix.
#
# POSITIVE CONTROL (never trust a null blind): the RED case is built from an input IDENTICAL
# to the GREEN except for the tab set. Because flipping only that one thing flips the verdict,
# the exit 0 is proven to be a real content read reaching the comparison — not one of the
# fail-open early returns. A green that no red can contradict would be worth zero bits.
#
# Exit 0 only if every case passes.
# Ticket: TRK-HOOK-211 · Rule: hookify.block-disco-missing-canonical-tabs.local.md

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/check_disco_canonical_tabs.sh"
RULE="$HERE/hookify.block-disco-missing-canonical-tabs.local.md"
ENFORCE="$(cd "$HERE/.." && pwd)/enforce.sh"

if ! command -v jq >/dev/null 2>&1; then
  echo "SKIP — jq unavailable; this test cannot build tool-call JSON." >&2
  exit 0
fi

fail=0
pass() { echo "  PASS  $1"; }
bad()  { echo "  FAIL  $1"; fail=$((fail+1)); }

# run <expected-exit> <name> <input-json> <file-path-arg>
run() {
  local want="$1" name="$2" json="$3" arg="${4:-}"
  local got=0
  INPUT="$json" "$CHECK" "$arg" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then pass "$name"; else bad "$name (want exit $want, got $got)"; fi
}

DISCO="/home/jdm/Projects/toMachina/docs/discoveries/trk-hook-211-selftest.html"

# The 8 canonical panel markers, assembled from the rule's own contract.
PANELS=(pain build arch decisions phases tickets files gates)
ALL8="<html><body>"
for p in "${PANELS[@]}"; do ALL8="${ALL8}<div class=\"panel\" id=\"panel-${p}\">x</div>"; done
ALL8="${ALL8}</body></html>"

# The RED input: byte-identical to ALL8 with exactly one panel removed.
MISSING_GATES="${ALL8//<div class=\"panel\" id=\"panel-gates\">x<\/div>/}"

j_write() { jq -cn --arg fp "$1" --arg c "$2" '{tool_name:"Write",tool_input:{file_path:$fp,content:$c}}'; }
j_edit()  { jq -cn --arg fp "$1" --arg s "$2" '{tool_name:"Edit", tool_input:{file_path:$fp,new_string:$s}}'; }

echo "== THE GREEN — the precondition constructed, the check must ALLOW (exit 0) =="
run 0 "all 8 canonical panels present in a discoveries .html" "$(j_write "$DISCO" "$ALL8")" "$DISCO"

echo "== THE RED — same input, one panel removed, must REFUSE (exit 1) =="
run 1 "panel-gates absent"                                    "$(j_write "$DISCO" "$MISSING_GATES")" "$DISCO"
run 1 "Edit rewrites tab scaffold incompletely"               "$(j_edit  "$DISCO" "$MISSING_GATES")" "$DISCO"

# Every single tab must be individually load-bearing. If any one could go missing without a
# refusal, the gate would be partially vacuous — passing on docs it is supposed to catch.
echo "== EVERY tab is load-bearing — removing any ONE must refuse =="
for p in "${PANELS[@]}"; do
  one="${ALL8//<div class=\"panel\" id=\"panel-${p}\">x<\/div>/}"
  run 1 "panel-${p} absent" "$(j_write "$DISCO" "$one")" "$DISCO"
done

echo "== POSITIVE CONTROL — the green is a real read, not a fail-open =="
g=0; INPUT="$(j_write "$DISCO" "$ALL8")"          "$CHECK" "$DISCO" >/dev/null 2>&1 || g=$?
r=0; INPUT="$(j_write "$DISCO" "$MISSING_GATES")" "$CHECK" "$DISCO" >/dev/null 2>&1 || r=$?
if [[ "$g" -eq 0 && "$r" -ne 0 ]]; then
  pass "same path, same tool, same shape — only the tab set differs, and the verdict flips"
else
  bad "green/red did not separate on tab set alone (green=$g red=$r) — verdict may not read content"
fi

echo "== WHAT IT PERMITS BY DESIGN (must NOT block) =="
run 0 "Edit with no panel markers — content-only change"      "$(j_edit "$DISCO" "<p>prose only</p>")" "$DISCO"
run 0 "file outside docs/discoveries/"                        "$(j_write "/x/docs/other/d.html" "$MISSING_GATES")" "/x/docs/other/d.html"

echo "== WHAT IT STILL REFUSES on path variants (no accidental escape hatch) =="
run 1 "nested discoveries subdirectory"                       "$(j_write "/x/docs/discoveries/sub/d.html" "$MISSING_GATES")" "/x/docs/discoveries/sub/d.html"
run 1 "repo-relative path form"                               "$(j_write "docs/discoveries/d.html" "$MISSING_GATES")" "docs/discoveries/d.html"

# ─────────────────────────────────────────────────────────────────────────────────────────
# PINNED DEFECTS — asserted PRESENT so they cannot rot into a silent regression.
# These live OUTSIDE this checker's file boundary (they belong to enforce.sh / the rule
# filename), so TRK-HOOK-211 does not fix them here. They are pinned, not repaired: if one
# ever starts working, THIS TEST FAILS LOUDLY so the fix is noticed and the census
# expectations get updated with it.
# ─────────────────────────────────────────────────────────────────────────────────────────
echo "== PINNED DEFECT 1 — logged identity != the rule's own name: field =="
NAME_FIELD="$(grep -m1 '^name:' "$RULE" | sed -E 's/^name:[[:space:]]*//; s/[[:space:]]*$//')"
FILE_ID="$(basename "$RULE" .local.md)"
if [[ "$FILE_ID" != "$NAME_FIELD" ]]; then
  pass "still present: enforce.sh keys the log on the FILENAME ('$FILE_ID'), not name: ('$NAME_FIELD')"
  echo "        → a census keying strictly on name: scores ZERO for this rule while it is firing."
else
  bad "PINNED DEFECT 1 IS FIXED (filename now equals name:) — update the census/never-fired ladder to match, then retire this pin"
fi

echo "== PINNED DEFECT 2 — dispatch order makes this rule the most-shadowed in the directory =="
# enforce.sh walks scope-bound/*.local.md in glob order and exits on the FIRST non-zero check,
# so walk order IS precedence. This rule's 'hookify.' prefix sorts it after every 'block-*'.
mapfile -t PREWRITE < <(
  for f in "$HERE"/*.local.md; do
    ev="$(grep -m1 -E '^event:' "$f" | sed 's/^event:[[:space:]]*//')"
    case ",${ev//[[:space:]]/}," in *,pre-write,*) basename "$f" .local.md ;; esac
  done
)
LAST="${PREWRITE[${#PREWRITE[@]}-1]}"
if [[ "${#PREWRITE[@]}" -gt 1 && "$LAST" == "$FILE_ID" ]]; then
  pass "still present: last of ${#PREWRITE[@]} pre-write rules — an earlier refusal exits the dispatcher before this one runs"
  echo "        → its evidence is suppressed twice: mis-keyed (defect 1) AND frequently unreached."
  echo "        → 'never fired, therefore retire' is wrong on two independent grounds here."
else
  bad "PINNED DEFECT 2 CHANGED (this rule is no longer last of the pre-write set) — re-verify shadowing before trusting fire counts"
fi

echo "== THE GREEN THROUGH THE REAL DISPATCHER, not just the script =="
# Isolating the scope dir proves the wiring contract (INPUT env + \$1 path) is correct and that
# a pass is actually RECORDED — distinguishing "did not fire" from "fired and passed".
if [[ -x "$ENFORCE" ]]; then
  T="$(mktemp -d)"; LOG="$T/violation-log.jsonl"
  cp "$RULE" "$CHECK" "$T"/
  ec=0
  j_write "$DISCO" "$ALL8" | HOOKIFY_VIOLATION_LOG="$LOG" HOOKIFY_SCOPE_BOUND_DIR="$T" \
    bash "$ENFORCE" >/dev/null 2>&1 || ec=$?
  if [[ "$ec" -eq 0 ]] && grep -q "${FILE_ID}::passed" "$LOG" 2>/dev/null; then
    pass "enforce.sh dispatched this rule, the check returned 0, and the pass was RECORDED"
  else
    bad "dispatcher green not demonstrated (enforce exit=$ec) — the wiring contract may be broken"
  fi
  rm -rf "$T"
else
  echo "  SKIP  enforce.sh not executable at $ENFORCE"
fi

echo
if [[ "$fail" -eq 0 ]]; then
  echo "ALL PASS — the green is achievable and demonstrated; the red is achievable and demonstrated."
  exit 0
fi
echo "$fail FAILURE(S)"
exit 1
