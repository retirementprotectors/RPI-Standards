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
1. The most-recent message is a genuine **JDM directive** — a user-role message
   whose TEXT starts with the dispatcher tag `Incoming from U09BBHTN8F2`
   (excludes tool-results, quoted mentions, and `Mirror from <WARRIOR>` /
   `[from <WARRIOR>]` cross-warrior traffic), AND
2. The response made **zero** `mcp__slack__slack_post_message` calls.

→ the warrior answered the directive somewhere other than its bilateral.

## What it NEVER fires on (the critical scope, per JDM 2026-06-12)

**Cross-warrior tmux coordination is invisible to it.** Warriors talk to each
other in tmux *specifically* to keep the IRL team-facing bilateral channels
clean. A blanket "must post to your bilateral before stop" rule would shove that
tmux chatter into the team channels — the opposite of what we want. So the check
judges **only JDM directives**, never warrior-to-warrior traffic.

## Severity

WARN v1 (exit 0; loud reminder, matching the proven heartbeat Stop-hook). A hard
`{"decision":"block"}` upgrade ("can't stop until you've posted") is a tested
follow-up — a misfiring Stop-block can loop a warrior, so v1 is loud-but-safe.

## Files

- `check_respond_where_received.sh` — Stop-hook wrapper (reads transcript on stdin)
- `check_respond_where_received.py` — detector (precise directive + slack-post analysis)
- validated against the 2026-06-12 SHINOB1 transcript: caught the 1 real violation
  among 14 directives, zero false-positives.
