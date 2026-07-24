#!/usr/bin/env bash
# check_bridge_join_invariant.sh — MZD-DATA-601 (L2 write-gate)
#
# Fires under: pre-write / pre-edit events (see block-bridge-join-bypass.local.md)
# Companion L3 (merge-time): toMachina .github/workflows/bridge-join-invariant-gate.yml
#
# THE INVARIANT (contract: docs/warriors/megazord/contracts/mwm-signal-feed.contract.md §3-§4):
#   A MWM call-derived signal row's own `master_record_id` is OFTEN NULL. To get the
#   person key you MUST bridge through `call_transcripts` (JOIN on recording_id) and take
#   t.master_record_id — never trust the signal row's own field. A signal-table-only count
#   undercounts people (347/2138 vs the correct 366/2504).
#
# WHAT THIS BLOCKS (exit 1 -> dispatcher exit 2) — NEW code content that ALL of:
#   1. references a MWM signal table   ( medicare_signals | retirement_signals )
#   2. reads master_record_id
#   3. does NOT reference the bridge table call_transcripts (no bridge join present)
#   4. does NOT carry the explicit escape hatch  bridge-join-exempt
#
# WHY AN ESCAPE HATCH: exactly one documented legit direct-read exists — the CRM-notes
# source (run_tag='crm-notes-*', recording_id=NULL) has no call to bridge through, so it
# reads master_record_id natively (contract §7). That path — and any other genuinely
# bridge-less-by-design read — carries a `bridge-join-exempt: <reason>` marker. This is the
# doctrine's "never silent omission" rule: the exception is declared, not hidden.
#
# SCOPE (blast radius kept tiny, on purpose):
#   - Only code files: .ts .tsx .js .jsx .mjs .cjs .sql .py . Prose (.md/.html/docs) is skipped
#     — the contract + disco docs mention these tokens legitimately.
#   - Content evaluated is the Write `content` / Edit `new_string` ONLY = NEW code, never a
#     whole pre-existing file. Pre-existing consumers (e.g. _tmp-board-assembler.mjs reading
#     pre-resolved NDJSON / enriched_clients, or gt-qa-gate.mjs which already joins on
#     recording_id) are grandfathered — this gate governs new DATA code, per the scope.
#
# I/O: INPUT (the PreToolUse tool-call JSON) available via $INPUT env (enforce.sh sets it).
#   $1 = file path being written/edited (passed by the dispatcher).
#   exit 0 -> allow.   exit 1 -> BLOCK (reason on stderr; dispatcher translates to exit 2).
#   Fail-OPEN on any tooling gap (missing jq, unreadable input) — never brick a write on infra.
#
# MZD-DATA-601 · owner: shinob1 · immune-system lane (RESPONSIBILITIES.md A6)

set -uo pipefail

FILE_PATH="${1:-}"

# Fail-open on tooling gap — a missing jq must never block every Write across the fleet.
command -v jq >/dev/null 2>&1 || exit 0

# Only govern code files. Prose/markup carries these tokens legitimately (the contract itself).
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.sql|*.py) : ;;
  *) exit 0 ;;
esac

# Never gate the gate's own files (this script + its rule doc + the L3 matcher).
case "$FILE_PATH" in
  *check_bridge_join_invariant.sh|*block-bridge-join-bypass.local.md|*bridge-join-matcher*.js) exit 0 ;;
esac

# Extract the NEW content: Write.content, else Edit.new_string.
IN="${INPUT:-}"
[[ -z "$IN" ]] && IN="$(cat 2>/dev/null || true)"
CONTENT="$(printf '%s' "$IN" | jq -r '.tool_input.content // .tool_input.new_string // empty' 2>/dev/null)"
[[ -z "$CONTENT" ]] && exit 0

# ── Detection (all four conditions on the NEW content) ────────────────────────
# 1. references a MWM signal table
grep -qE '\b(medicare_signals|retirement_signals)\b' <<<"$CONTENT" || exit 0
# 2. reads master_record_id
grep -q 'master_record_id' <<<"$CONTENT" || exit 0
# 4. explicit escape hatch present -> allow (documented bridge-less-by-design read)
grep -q 'bridge-join-exempt' <<<"$CONTENT" && exit 0
# 3. bridge table present -> the join is there -> allow
grep -q 'call_transcripts' <<<"$CONTENT" && exit 0

# All conditions met -> BLOCK.
cat >&2 <<EOF
ENFORCE [block-bridge-join-bypass]: bridge-join invariant bypass in new DATA code.

Target: $FILE_PATH

This content references a MWM signal table (medicare_signals / retirement_signals)
and reads master_record_id, but does NOT bridge through call_transcripts.

A call-signal row's own master_record_id is OFTEN NULL — trusting it undercounts
people (contract §3-§4). Derive the person key by bridging:

    SELECT s.*, t.master_record_id AS bridged_master_record_id
    FROM \`partner_midwest_medigap.retirement_signals\` s
    JOIN \`partner_midwest_medigap.call_transcripts\` t USING (recording_id)
    WHERE t.master_record_id IS NOT NULL

Genuinely bridge-less BY DESIGN (e.g. the CRM-notes source: recording_id=NULL, no call
to bridge through — contract §7)? Declare it, don't hide it — add a marker on the read:

    // bridge-join-exempt: crm-notes source has recording_id=NULL, master_record_id native

Invariant: signals always bridge through call_transcripts; never trust the signal
row's own master_record_id alone. (MZD-DATA-601 · L2 · immune-system lane)
EOF
exit 1
