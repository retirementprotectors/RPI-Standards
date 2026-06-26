---
name: block-shinob1-arc-without-slackout
enabled: true
event: stop
action: block
severity: BLOCK
scope: SHINOB1-ARC-SLACKOUT-001
introduced: 2026-06-02
implementation: stop-event shell gate via check_shinob1_arc_slackout.sh, propagated by session-end-brain-export.sh (exit 2)
status: enforced
wired_in: session-end-brain-export.sh (Stop hook in ~/.claude/settings.json) + enforce.sh ledger ship-tagging
owner: shinob1
---

# block-shinob1-arc-without-slackout

**Blocks a SHINOB1 turn from ending when a ship action happened with no Slack-Out after it.** This is the BLOCK upgrade that closes the hole `warn-shinob1-session-end-no-heartbeat` structurally could not.

## Why the WARN rule wasn't enough

The companion `warn-shinob1-session-end-no-heartbeat` has three holes JDM caught on 2026-06-02 (after a 5-turn build arc shipped 3 PRs with completion reported only in the tmux console):

1. **It's a WARN, not a block** — it nags, it doesn't stop.
2. **It can't see ship-vs-quiet** — it only counts any Slack post across the whole session.
3. **The deep one: "I didn't post" is a non-event** — hooks fire on tool calls, and the *absence* of a `slack_post_message` is nothing to intercept. The immune system was blind to silence.

## How this makes the silence hookable

Two pieces turn the absence-of-a-post into a detectable, blockable condition:

1. **Ledger ship-tagging** (`enforce.sh`, PreToolUse): when a `Bash` call matches `git push` / `gh pr create|merge|ready`, an extra ledger line `{"tool":"__ship__"}` is appended to `/tmp/scope-prior-art-<session>.jsonl`. Additive + best-effort — a failure only skips the tag, never blocks the tool call.
2. **The Stop gate** (`check_shinob1_arc_slackout.sh`): on every Stop, compares the last `__ship__` line index against the last `mcp__slack__slack_post_message` line index. If a ship has no post after it → **exit 2** (Claude Code Stop-block contract; stderr is the reason shown to the model). `session-end-brain-export.sh` propagates that exit 2.

Posting resolves it: the post lands a `slack_post_message` line after the ship, and the next Stop allows.

## Scope + safety (blast radius = SHINOB1 only)

- The gate self-scopes by tmux session name (`^[Ss][Hh][Ii][Nn][Oo][Bb]1`). Every other warrior hits the scope gate and exits 0 — this can **only** block my sessions, even though the ledger ship-tagging is global.
- **Circuit breaker:** after 3 consecutive blocks for the same ship index with still no post, the gate degrades to a warn + exits 0, so a session can never hard-lock if posting is genuinely impossible.
- Best-effort everywhere: missing ledger, missing gate (`-x` guard), or no tmux → exit 0.

## Verification (2026-06-02, isolation + integration)

| Case | Expected | Result |
|---|---|---|
| ship, no post | exit 2 (block) | ✅ |
| ship, then post | exit 0 (allow) | ✅ |
| no ship | exit 0 | ✅ |
| non-SHINOB1 session, ship no post | exit 0 (scope) | ✅ |
| circuit breaker, 3rd block | exit 0 (degrade) | ✅ |
| ship-matcher: `gh pr 'merge'`, `git push` tagged; `gh pr view`, `ls` not | correct | ✅ |
| `enforce.sh` + `brain-export.sh` `bash -n` | syntax OK | ✅ |

## Escape hatch

- Remove the symlink in the project's `.claude/`, or
- Set `enabled: false` in this frontmatter, or
- Remove the propagation block in `session-end-brain-export.sh`.

## Companion rules

- `warn-shinob1-session-end-no-heartbeat` — the WARN this upgrades (kept; it covers the no-ship "post a closing heartbeat anyway" case).
- `enforce.sh` SCOPE-005-1-F ledger — the per-session tool ledger both gates read.

## Reference

- MEMORY.md `feedback_slack_comms_protocol` § "Slack is JDM's context-retention + mobile layer"
- The directive that produced this: JDM 2026-06-02 — "Don't you have a Rule and a Hook preventing you from doing anything other than that?!" + "Sure" (approving the structural gate).
