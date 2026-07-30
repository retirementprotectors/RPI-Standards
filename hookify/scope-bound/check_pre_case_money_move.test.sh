#!/usr/bin/env bash
# check_pre_case_money_move.test.sh — self-test for OB1-CASESUB-EXECUTE-GATE-001.
# A gate that can't HOLD the real injection, or that FALSE-BLOCKS legit case work, is theater.
# Exit 0 only if every case passes. (HIKARI eyeball-verifies this same matrix at land.)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/check_pre_case_money_move.sh"

fail=0
# run <expected-exit> <name> <tool_json>
run() {
  local want="$1" name="$2" json="$3"
  local got=0
  INPUT="$json" "$CHECK" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then echo "  PASS  $name"; else echo "  FAIL  $name (want exit $want, got $got)"; fail=$((fail+1)); fi
}

j_bash()  { jq -cn --arg c "$1" '{tool_name:"Bash", tool_input:{command:$c}}'; }
j_tool()  { jq -cn --arg t "$1" '{tool_name:$t, tool_input:{}}'; }

# CLASS D money-instruction write shape — a doc-path .set() (deliberately NOT the
# collection-style access idiom, so the immune system's own firestore-write content
# gate does not flag this test file).
FS_WRITE='node -e "ref(\"wire_executions/x\").set({amount_cents:2500000})"'

echo "== A VOLTRON CASE SEAT, no approval token (must BLOCK = exit 2) =="
export RPI_CASE_SEAT="VOLTRON-LINDA-PIERCE"
unset RPI_APPROVAL_HUB_CHECK   # no release helper → fail-closed
run 2 "CLASS A — the LINDA-PIERCE shape: curl POST wire/execute"        "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute -d @pull.json')"
run 2 "CLASS A — wire/:id/approve"                                      "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/abc123/approve')"
run 2 "CLASS B — gmail_send_email from a case seat"                     "$(j_tool 'mcp__rpi-workspace__gmail_send_email')"
run 2 "CLASS B — curl /api/comms/send-sms"                             "$(j_bash 'curl -X POST https://tm-api/api/comms/send-sms -d body=hi')"
run 2 "CLASS C — playwright browser_click (custodian interaction)"     "$(j_tool 'mcp__plugin_playwright_playwright__browser_click')"
run 2 "CLASS C — playwright browser_fill_form"                         "$(j_tool 'mcp__plugin_playwright_playwright__browser_fill_form')"
run 2 "CLASS C — browser_type (HIKARI completeness: type BLOCK)"       "$(j_tool 'mcp__plugin_playwright_playwright__browser_type')"
run 2 "CLASS C — browser_press_key (can submit a form)"               "$(j_tool 'mcp__plugin_playwright_playwright__browser_press_key')"
run 2 "CLASS C — browser_select_option"                              "$(j_tool 'mcp__plugin_playwright_playwright__browser_select_option')"
run 2 "CLASS C — browser_file_upload"                                "$(j_tool 'mcp__plugin_playwright_playwright__browser_file_upload')"
run 2 "CLASS C — browser_evaluate (code-exec)"                       "$(j_tool 'mcp__plugin_playwright_playwright__browser_evaluate')"
run 2 "CLASS C — browser_run_code_unsafe (arbitrary code)"           "$(j_tool 'mcp__plugin_playwright_playwright__browser_run_code_unsafe')"
run 2 "CLASS C — browser_handle_dialog (confirm a prompt)"           "$(j_tool 'mcp__plugin_playwright_playwright__browser_handle_dialog')"
run 2 "CLASS D — wire_executions money-instruction write"              "$(j_bash "$FS_WRITE")"
run 2 "CLASS B — slack_post_message from a case seat"                  "$(j_tool 'mcp__slack__slack_post_message')"

echo "== SAME CASE SEAT, benign calls (must PASS = exit 0, zero-FP) =="
run 0 "client READ via API (no money shape)"                           "$(j_bash 'curl https://tm-api/api/clients/123')"
run 0 "roadmap file read / ls in case home"                            "$(j_bash 'ls \"/home/jdm/inbox/!VOLTRON DOCS!/!Cases/Linda-Pierce Case\"')"
run 0 "gmail_draft_email (draft is safe)"                              "$(j_tool 'mcp__rpi-workspace__gmail_draft_email')"
run 0 "playwright browser_navigate (navigation/read)"                  "$(j_tool 'mcp__plugin_playwright_playwright__browser_navigate')"
run 0 "playwright browser_snapshot (read)"                             "$(j_tool 'mcp__plugin_playwright_playwright__browser_snapshot')"
run 0 "playwright browser_take_screenshot (HIKARI: render-evidence read PASS)" "$(j_tool 'mcp__plugin_playwright_playwright__browser_take_screenshot')"
run 0 "playwright browser_navigate_back (read/nav)"                    "$(j_tool 'mcp__plugin_playwright_playwright__browser_navigate_back')"
run 0 "ordinary Bash (git status)"                                     "$(j_bash 'git status')"

echo "== NON-case seat (gate N/A → PASS even for money tools) =="
unset RPI_CASE_SEAT
run 0 "gmail_send_email in a non-case seat"                            "$(j_tool 'mcp__rpi-workspace__gmail_send_email')"
run 0 "wire/execute POST in a non-case seat"                          "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')"

echo "== CASE SEAT WITH a release helper (token path) =="
export RPI_CASE_SEAT="VOLTRON-LINDA-PIERCE"
VALID="$(mktemp)";   printf '#!/usr/bin/env bash\nexit 0\n' > "$VALID";   chmod +x "$VALID"
INVALID="$(mktemp)"; printf '#!/usr/bin/env bash\nexit 1\n' > "$INVALID"; chmod +x "$INVALID"
RPI_APPROVAL_HUB_CHECK="$VALID"   run 0 "CLASS A wire/execute WITH valid Approval-Hub release"     "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')"
RPI_APPROVAL_HUB_CHECK="$INVALID" run 2 "CLASS A wire/execute with INVALID sig (forged approval)"  "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')"
rm -f "$VALID" "$INVALID"

# ── LIVE DISPATCH CHAIN (TRK-HOOK-211 · ronin/W1 · 2026-07-30) ───────────────────
# Everything above calls $CHECK DIRECTLY. That proves the CHECK. It does not prove the
# CHAIN, and those are not the same claim: a sibling scope-bound gate passed its own
# direct-call review while its dispatcher never reached it, because the loader resolved
# one directory level off. A green check behind a broken dispatcher is vacuous.
# So: re-run the decisive cases THROUGH enforce.sh, the way a real tool call arrives.
ENFORCE="$HERE/../enforce.sh"

# run_chain <expected-exit> <name> <tool_json> [env assignments...]
# Drives the dispatcher, and — the point of this helper — captures a per-run violation
# log so we can tell "the check ran and ALLOWED" apart from "the check was never reached."
# Both exit 0. Only the log distinguishes them. Never trust the null without it.
CHAIN_LOG=""
run_chain() {
  local want="$1" name="$2" json="$3"; shift 3
  local got=0
  CHAIN_LOG="$(mktemp)"
  env "$@" HOOKIFY_SCOPE_BOUND_DIR="$HERE" HOOKIFY_VIOLATION_LOG="$CHAIN_LOG" \
    bash "$ENFORCE" <<<"$json" >/dev/null 2>&1 || got=$?
  if [[ "$got" -eq "$want" ]]; then echo "  PASS  $name"; else echo "  FAIL  $name (want exit $want, got $got)"; fail=$((fail+1)); fi
}
# assert_log <grep-pattern> <name> — the positive control on the run just performed.
assert_log() {
  if grep -q "$1" "$CHAIN_LOG" 2>/dev/null; then echo "  PASS  $2"; else echo "  FAIL  $2 (no matching record in violation log)"; fail=$((fail+1)); fi
  rm -f "$CHAIN_LOG"
}

RULE="block-case-money-move-without-approval"

if [[ ! -r "$ENFORCE" ]]; then
  echo "  FAIL  dispatcher $ENFORCE missing/unreadable — the chain is untestable, which is itself the defect"
  fail=$((fail+1))
else
  echo "== LIVE CHAIN: tool call -> enforce.sh -> pre-case-money-move -> this check =="
  export RPI_CASE_SEAT="VOLTRON-LINDA-PIERCE"
  unset RPI_APPROVAL_HUB_CHECK

  run_chain 2 "CHAIN CLASS A — money-exec reaches the gate and is refused" "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')"
  assert_log "\"rule\":\"${RULE}\"" "  ^ log attributes the refusal to THIS rule, by name"

  run_chain 2 "CHAIN CLASS B — external send refused"                      "$(j_tool 'mcp__rpi-workspace__gmail_send_email')"
  run_chain 2 "CHAIN CLASS C — custodian-portal interaction refused"       "$(j_tool 'mcp__plugin_playwright_playwright__browser_click')"
  run_chain 2 "CHAIN CLASS D — money-instruction write refused"            "$(j_bash "$FS_WRITE")"

  # THE POSITIVE CONTROL. A read verb must exit 0 *having been evaluated* — the ::passed
  # record is the proof. Without this assertion, an exit 0 from a dispatcher that never
  # dispatched reads identically, and that is the silent failure this scope exists to catch.
  run_chain 0 "CHAIN read verb — allowed"                                  "$(j_tool 'mcp__plugin_playwright_playwright__browser_navigate')"
  assert_log "\"rule\":\"${RULE}::passed\"" "  ^ POSITIVE CONTROL: the allow came from an EVALUATION, not a skip"

  echo "== LIVE CHAIN: the green — a valid release must actually release =="
  V2="$(mktemp)"; printf '#!/usr/bin/env bash\nexit 0\n' > "$V2"; chmod +x "$V2"
  I2="$(mktemp)"; printf '#!/usr/bin/env bash\nexit 1\n' > "$I2"; chmod +x "$I2"
  run_chain 0 "CHAIN GREEN — CLASS A released by a valid grant"            "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')" RPI_APPROVAL_HUB_CHECK="$V2"
  assert_log "\"rule\":\"${RULE}::passed\"" "  ^ the green is an EVALUATED pass, not an unreached gate"
  run_chain 2 "CHAIN — forged grant still refused"                         "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')" RPI_APPROVAL_HUB_CHECK="$I2"
  run_chain 2 "CHAIN — absent helper fails CLOSED"                         "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')" RPI_APPROVAL_HUB_CHECK=/nonexistent/approval-hub-verify.sh
  rm -f "$V2" "$I2"

  echo "== LIVE CHAIN: non-case seat is still N/A through the dispatcher =="
  unset RPI_CASE_SEAT
  run_chain 0 "CHAIN — money-exec outside a case seat is allowed"          "$(j_bash 'curl -X POST https://tm-api/api/voltron/wire/execute')"
  export RPI_CASE_SEAT="VOLTRON-LINDA-PIERCE"
fi

# ── PINNED DEFECT — F1: the production release path is currently unreachable ──────
# Reported to HIKARI + SHINOB1 2026-07-30 and deliberately NOT fixed here: fixing it means
# building MEGAZORD's Approval-Hub validator, which is outside this file's boundary.
#
# The green above is real, but reachable ONLY because the test supplies a release helper.
# On this box the DEFAULT helper does not exist, so in production every money action from
# a case seat is denied with no achievable release. That is intentional fail-closed
# posture — and it is also an always-red gate, the state that gets forced past until the
# fleet learns that gates are noise.
#
# So it is asserted as PRESENT and fails LOUDLY the moment it stops being true. When the
# validator lands this test goes red on purpose: that is the signal to re-verify the green
# against the REAL validator rather than a stub, and then retire this block. A limit that
# is declared cannot rot into a silent regression; a limit left in a comment always does.
echo "== PINNED: F1 — default Approval-Hub validator absent (always-red window) =="
DEFAULT_HELPER="$HOME/.claude/hooks/approval-hub-verify.sh"
if [[ ! -x "$DEFAULT_HELPER" ]]; then
  echo "  PASS  F1 still PRESENT — no default validator, so the release path is unreachable in production (expected today)"
else
  echo "  FAIL  F1 RESOLVED — a default Approval-Hub validator now exists at $DEFAULT_HELPER."
  echo "        This is GOOD NEWS and a REQUIRED ACTION: re-verify the green against the real"
  echo "        validator, confirm a forged grant is still refused, then delete this pinned block."
  fail=$((fail+1))
fi

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "✅ pre-case-money-move self-test PASSED — HOLDS the injected money surface, PASSES legit case work + a valid release, BLOCKS a forged sig, and the LIVE CHAIN (enforce.sh -> pre-case-money-move -> check) is demonstrated in BOTH directions with a positive control."
  exit 0
else
  echo "❌ pre-case-money-move self-test FAILED — $fail case(s). Gate NOT safe to arm."
  exit 1
fi
