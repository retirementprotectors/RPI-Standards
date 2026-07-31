#!/usr/bin/env python3
# Detector for check_respond_where_received.sh (RULE #1 enforcement).
# Reads the Claude Code transcript JSONL on stdin. Prints "VIOLATION\t<snippet>"
# iff the MOST RECENT genuine JDM directive (a user-role message whose TEXT
# carries a dispatcher tag) was NOT followed by the correct-channel reply for
# that tag's era. Otherwise prints nothing.
#
# Cross-warrior tmux traffic is invisible here — only JDM directives are judged.
# SHINOB1-RULE1-ENFORCE-001 · owner: shinob1 · 2026-06-12
#
# ── TRK-HOOK-238 (ronin, 2026-07-31) — THE CHANNEL THIS DETECTOR ENFORCES MOVED ──────────
# Built and validated 2026-06-12 against Slack-dispatched traffic. Live population,
# measured on this box 2026-07-31:
#     "Incoming from U09BBHTN8F2"    (the Slack-era mark this detector watched)   20
#     "[Dojo DM from JDM"            (the hub-era mark that replaced it)        205
# The detector was correct about a channel that is 91% no longer how directives arrive.
# Not dead code — it still fires on the 20 that DO match. It was CORRECT ABOUT A CHANNEL
# WE RETIRED, which is a worse failure than dead code: dead code is visibly inert, this
# read as live enforcement while missing the majority of what it exists to watch.
#
# THE OLD REMEDY WAS ALSO DEAD. Pre-fix, "responded correctly" meant one
# mcp__slack__slack_post_message call — Slack is decommissioned, so even on the 20 it could
# still see, the prescribed fix was unperformable. Same shape as the death gate waiting on
# a Slack ✅ reaction and the cite gate telling seats to confess into a dead channel.
#
# THE FIX TEACHES BOTH HALVES THE HUB SHAPE, NEITHER REPLACES THE OLD ONE:
#   directive mark   — dojo-deliver-watcher.mjs's formatDelivery() 1:1-DM shape:
#                       `[Dojo DM from JDM — answer IN THE HUB, NOT Slack] <body>`
#                       Matched only for sender "JDM" specifically (formatDelivery renders
#                       any other identified sender as their own email, and an absent owner
#                       as "UNKNOWN SENDER" — this detector's whole premise is a JDM
#                       directive, so a non-JDM hub DM is deliberately NOT a match here).
#   responded signal  — a Bash tool_use whose command references dojo-reply.mjs, the exact
#                       reply command formatDelivery prints in the delivery footer.
# The Slack-era mark and remedy are KEPT, not removed — a transcript from before the
# cutover is still real history and this detector may still be run against one.
#
# ⚠️ DECLARED LIMIT, NOT SILENTLY SKIPPED: GROUP hub messages
# (`[Group: ...] [Dojo GROUP msg from ... — answer IN THE HUB only if @mentioned or clearly
# your lane, else stay quiet]`) are NOT covered by this fix. A group message's correct
# response is CONDITIONAL — silence is often correct — and judging that needs knowing
# whether the seat was @mentioned or the topic was its lane, which this detector cannot see
# from the transcript alone. Widening into that is TRK-HOOK-235's shape of problem, not
# this one; out of scope here on purpose rather than guessed at.
import sys, json, re

MARK_SLACK = "Incoming from U09BBHTN8F2"
MARK_HUB = "[Dojo DM from JDM — answer IN THE HUB, NOT Slack]"

REPLY_CMD_RE = re.compile(r"dojo-reply\.mjs")


def role(o):
    return o.get("type")


def text_only(o):
    m = o.get("message", o)
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _tool_uses(o):
    m = o.get("message", o)
    c = m.get("content")
    if not isinstance(c, list):
        return []
    return [b for b in c if isinstance(b, dict) and b.get("type") == "tool_use"]


def has_slack_post(o):
    return any(b.get("name") == "mcp__slack__slack_post_message" for b in _tool_uses(o))


def has_hub_reply(o):
    for b in _tool_uses(o):
        if b.get("name") != "Bash":
            continue
        cmd = (b.get("input") or {}).get("command", "")
        if REPLY_CMD_RE.search(cmd):
            return True
    return False


def directive_era(o):
    """None, "slack", or "hub" — WHICH mark this user message carries, if either.

    Not a bool: the correct remedy differs by era, and collapsing both marks into one
    boolean (as a first cut of this fix did) let a Slack post satisfy a HUB directive.
    That is wrong on its own terms, not just stale — Slack is decommissioned, so posting
    there is not "an alternate valid channel", it is an action that cannot reach JDM at
    all (calling it hangs the session, per this box's own boot posture). A slack post
    must never count as an answer to a directive that arrived AFTER the cutover.
    """
    if role(o) != "user":
        return None
    for ln in text_only(o).splitlines():
        stripped = ln.lstrip("# ")
        if stripped.startswith(MARK_HUB):
            return "hub"
        if stripped.startswith(MARK_SLACK):
            return "slack"
    return None


def main():
    msgs = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except Exception:
            continue
    dir_idxs = [i for i, o in enumerate(msgs) if directive_era(o) is not None]
    if not dir_idxs:
        return
    i = dir_idxs[-1]  # judge only the most-recent (just-closed) directive turn
    era = directive_era(msgs[i])
    if era == "hub":
        # The ONLY live remedy. A Slack post does not satisfy a hub-era directive —
        # Slack cannot deliver it to JDM, so accepting one would certify a non-answer.
        posted = any(role(msgs[j]) == "assistant" and has_hub_reply(msgs[j])
                     for j in range(i + 1, len(msgs)))
    else:
        # Pre-cutover transcript. Slack WAS the live channel when this directive
        # arrived, so a slack post was the correct action at the time — keep reading
        # history correctly rather than judging the past by today's channel.
        posted = any(role(msgs[j]) == "assistant" and has_slack_post(msgs[j])
                     for j in range(i + 1, len(msgs)))
    if not posted:
        snip = text_only(msgs[i]).strip().replace("\n", " ")[:80]
        sys.stdout.write("VIOLATION\t" + snip)


if __name__ == "__main__":
    main()
