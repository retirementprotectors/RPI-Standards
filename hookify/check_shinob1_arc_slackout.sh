#!/usr/bin/env bash
# check_shinob1_arc_slackout.sh — Stop-event BLOCK gate
# Rule: block-shinob1-arc-without-slackout · SHINOB1-ARC-SLACKOUT-001 · 2026-06-02
#
# Closes the blind spot the WARN heartbeat rule could not: it makes the SILENCE
# hookable. Blocks turn-end when a SHIP action (git push / gh pr create|merge)
# happened in this session with NO mcp__slack__slack_post_message AFTER it in the
# ledger — i.e. you shipped and didn't Slack-Out. Posting resolves it (the next
# Stop sees a post after the ship → allows).
#
# WHY this is the only thing that works: hooks fire on tool calls, and "I didn't
# post" is a non-event. By tagging ships into the ledger (enforce.sh) and gating
# at Stop, the absence-of-a-post becomes a detectable, blockable condition.
#
# Scope: SHINOB1 sessions ONLY (blast radius = my sessions). Other warriors hit
# the scope gate and exit 0. Exit 2 = block (Claude Code Stop contract, stderr is
# shown to the model); exit 0 = allow. A circuit breaker degrades to allow after
# repeated blocks so a session can never hard-lock if posting is impossible.
#
# Escape hatch: remove the symlink, or the brain-export.sh propagation block, or
# set frontmatter enabled:false on the rule.

set -uo pipefail

TMUX_SESSION="${TMUX_SESSION:-$(tmux display-message -p '#S' 2>/dev/null || echo '')}"

# ── Scope gate: SHINOB1 sessions only ────────────────────────────────────────
[[ -z "$TMUX_SESSION" ]] && exit 0
[[ ! "$TMUX_SESSION" =~ ^[Ss][Hh][Ii][Nn][Oo][Bb]1 ]] && exit 0

LEDGER="/tmp/scope-prior-art-${TMUX_SESSION}.jsonl"
[[ ! -f "$LEDGER" ]] && exit 0

# ── Find the last ship marker and the last Slack post (1-based line numbers) ──
last_ship=$(grep -n '"tool":"__ship__"' "$LEDGER" 2>/dev/null | tail -1 | cut -d: -f1)
last_slack=$(grep -n '"tool":"mcp__slack__slack_post_message"' "$LEDGER" 2>/dev/null | tail -1 | cut -d: -f1)

# Nothing shipped this session → nothing to report. Allow.
[[ -z "$last_ship" ]] && exit 0
# A Slack-Out landed AFTER the last ship → satisfied. Allow.
[[ -n "$last_slack" && "$last_slack" -gt "$last_ship" ]] && exit 0

# ── Circuit breaker — never hard-lock a session ──────────────────────────────
# Track consecutive blocks for THIS ship index. After 3, degrade to a warn+allow
# so the session can end even if posting is genuinely impossible.
BRK="/tmp/arc-slackout-brk-${TMUX_SESSION}"
prev=$(cat "$BRK" 2>/dev/null || echo "")
if [[ "$prev" == "${last_ship}:"* ]]; then
  count="${prev##*:}"
else
  count=0
fi
count=$((count + 1))
echo "${last_ship}:${count}" > "$BRK" 2>/dev/null || true

if [[ "$count" -ge 3 ]]; then
  echo "::block-shinob1-arc-without-slackout:: degraded after ${count} blocks — post to #shinob1 ASAP; allowing session to proceed." >&2
  exit 0
fi

# ── BLOCK ────────────────────────────────────────────────────────────────────
cat >&2 <<'MSG'
::block-shinob1-arc-without-slackout::
You SHIPPED (git push / gh pr create|merge) but have NOT posted to #shinob1
(C0AS0LETSBW) since. Slack-Out is the core comms principle: JDM isn't always at
the Command Center and the tmux console scrolls away — Slack is his durable,
mobile-accessible record of what shipped.

BEFORE ending this turn: post the result to the #shinob1 bilateral via
mcp__slack__slack_post_message — include the PR #, what shipped, and the
verification — then stop. (This gate clears automatically once a post lands
after the ship.)
MSG
exit 2
