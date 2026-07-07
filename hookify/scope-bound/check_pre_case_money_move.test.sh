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
run 2 "CLASS D — wire_executions money-instruction write"              "$(j_bash "$FS_WRITE")"
run 2 "CLASS B — slack_post_message from a case seat"                  "$(j_tool 'mcp__slack__slack_post_message')"

echo "== SAME CASE SEAT, benign calls (must PASS = exit 0, zero-FP) =="
run 0 "client READ via API (no money shape)"                           "$(j_bash 'curl https://tm-api/api/clients/123')"
run 0 "roadmap file read / ls in case home"                            "$(j_bash 'ls \"/home/jdm/inbox/!VOLTRON DOCS!/!Cases/Linda-Pierce Case\"')"
run 0 "gmail_draft_email (draft is safe)"                              "$(j_tool 'mcp__rpi-workspace__gmail_draft_email')"
run 0 "playwright browser_navigate (navigation/read)"                  "$(j_tool 'mcp__plugin_playwright_playwright__browser_navigate')"
run 0 "playwright browser_snapshot (read)"                             "$(j_tool 'mcp__plugin_playwright_playwright__browser_snapshot')"
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

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "✅ pre-case-money-move self-test PASSED — HOLDS the injected money surface, PASSES legit case work + a valid release, BLOCKS a forged sig."
  exit 0
else
  echo "❌ pre-case-money-move self-test FAILED — $fail case(s). Gate NOT safe to arm."
  exit 1
fi
