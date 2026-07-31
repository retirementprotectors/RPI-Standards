---
name: warn-respond-where-you-receive
enabled: true
event: stop
action: warn
severity: WARN
scope: SHINOB1-RULE1-ENFORCE-001
introduced: 2026-06-12
implementation: stop-event shell hook via check_respond_where_received.sh (+ .py detector)
status: enforced
wired_in: session-end-brain-export.sh (Stop hook registered in ~/.claude/settings.json)
owner: shinob1
---

# warn-respond-where-you-receive

Code-level enforcement of **RULE #1 — "RESPOND WHERE YOU RECEIVE"** (the #1
non-negotiable in the global CLAUDE.md, injected into every session).

> Acknowledge | Execute | Report — in the SAME channel the directive arrived in.
> A directive in your bilateral gets its ACK, its progress, AND its final report
> in that bilateral. Never make JDM chase your response to another surface.

## Why this exists (instruction → enforcement)

2026-06-12: the rule is injected into every session, yet MEGAZORD answered a JDM
directive **console-only** (replied in its tmux console / wrong surface, never
posted to its bilateral) and went silent on JDM. Then SHINOB1 did the **exact
same thing while reciting the rule** — proof that an injected instruction fades
mid-session. Per the enforcement hierarchy (hookify > CLAUDE.md), Rule #1 had to
become code. [[feedback_claude_md_context_fade]]

## What it fires on (the ONE violation class)

At the Stop event, the check reads the transcript and fires **iff**:
1. The most-recent message is a genuine **JDM directive**, in EITHER era:
   - hub era (current): text starting with `[Dojo DM from JDM — answer IN THE
     HUB, NOT Slack]` (`dojo-deliver-watcher.mjs`'s own delivery format — matched
     only when the sender resolves to JDM specifically, never another identified
     sender or an unknown one)
   - Slack era (historical): text starting with the dispatcher tag
     `Incoming from U09BBHTN8F2`
   (excludes tool-results, quoted mentions, and `Mirror from <WARRIOR>` /
   `[from <WARRIOR>]` cross-warrior traffic), AND
2. The response did not perform that era's live remedy:
   - hub-era directive → zero `Bash` calls referencing `dojo-reply.mjs`
   - Slack-era directive → zero `mcp__slack__slack_post_message` calls

→ the warrior answered the directive somewhere other than where it arrived.

**TRK-HOOK-238 (2026-07-31): the remedy is keyed to the directive's era, not
OR'd together.** A Slack post never satisfies a hub-era directive — Slack is
decommissioned, so posting there cannot reach JDM at all, and accepting it as
"responded" would certify a non-answer. Conversely a pre-cutover transcript is
read correctly against the channel that was actually live when it arrived.

## What it NEVER fires on (the critical scope, per JDM 2026-06-12)

**Cross-warrior tmux coordination is invisible to it.** Warriors talk to each
other in tmux *specifically* to keep the IRL team-facing bilateral channels
clean. A blanket "must post to your bilateral before stop" rule would shove that
tmux chatter into the team channels — the opposite of what we want. So the check
judges **only JDM directives**, never warrior-to-warrior traffic.

**⚠️ DECLARED LIMIT (TRK-HOOK-238): GROUP hub messages are not judged.** A group
directive's correct response is conditional (`only if @mentioned or clearly
your lane, else stay quiet`), and this detector cannot see from the transcript
alone whether either condition held. Widening into that is a different shape of
problem than this ticket closed — left explicit rather than silently expanded.

## Severity

WARN v1 (exit 0; loud reminder, matching the proven heartbeat Stop-hook). A hard
`{"decision":"block"}` upgrade ("can't stop until you've posted") is a tested
follow-up — a misfiring Stop-block can loop a warrior, so v1 is loud-but-safe.

## Files

- `check_respond_where_received.sh` — Stop-hook wrapper (reads transcript on stdin)
- `check_respond_where_received.py` — detector (era-aware directive + remedy match)
- `check_respond_where_received.test.py` — TRK-HOOK-238, both directions, drives the
  detector through stdin exactly as the shell wrapper does (no import — sidesteps the
  `__pycache__` staleness exposure the fleet found tonight rather than being exposed to it)
- validated against the 2026-06-12 SHINOB1 transcript: caught the 1 real violation
  among 14 directives, zero false-positives (Slack-era baseline, unchanged by this fix)
