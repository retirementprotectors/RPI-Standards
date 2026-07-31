#!/usr/bin/env python3
"""check_respond_where_received.test.py — TRK-HOOK-238

Drives the detector through STDIN, exactly the path check_respond_where_received.sh
uses — not by importing its functions — so a fixture proves the same thing a real
Stop-hook invocation would observe.

BOTH DIRECTIONS THROUGHOUT: every "this must fire" case is paired with a "this must
NOT fire" case that differs only in the thing under test, per SHINOB1's acceptance bar.

Run:  python3 hookify/check_respond_where_received.test.py     (exit 0 = pass)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DETECTOR = os.path.join(HERE, "check_respond_where_received.py")

FAILS = []


def run(msgs):
    """Pipe a list of transcript message dicts through the real detector process."""
    payload = "\n".join(json.dumps(m) for m in msgs)
    p = subprocess.run([sys.executable, DETECTOR], input=payload,
                       capture_output=True, text=True)
    return p.stdout


def check(label, got_violates, want_violates):
    ok = got_violates == want_violates
    if not ok:
        FAILS.append(label)
    print(f"  {'PASS' if ok else 'FAIL'}  {label:<70} "
          f"violated={got_violates!s:<5} want={want_violates}")


def user(text):
    return {"type": "user", "message": {"content": [{"type": "text", "text": text}]}}


def assistant_text(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def assistant_tool(name, **input_kwargs):
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": name, "input": input_kwargs}
    ]}}


SLACK_DIRECTIVE = "Incoming from U09BBHTN8F2\ndo the thing"
HUB_DIRECTIVE_JDM = "[Dojo DM from JDM — answer IN THE HUB, NOT Slack] do the thing\n" \
                    '↳ Reply: node /home/jdm/Projects/dojo-warriors/mdj-agent/scripts/' \
                    'dojo-reply.mjs T1 ronin josh@retireprotected.com "<your reply>"'
HUB_DIRECTIVE_OTHER = "[Dojo DM from vince@retireprotected.com — answer IN THE HUB, " \
                      "NOT Slack] do the thing"

REPLY_CMD = ('node /home/jdm/Projects/dojo-warriors/mdj-agent/scripts/dojo-reply.mjs '
             'T1 ronin josh@retireprotected.com --file /tmp/reply.txt')

print("=== A · Slack-era shape — the ORIGINAL behavior, kept as a regression guard ===")
check("Slack directive + slack post -> no violation",
      run([user(SLACK_DIRECTIVE), assistant_tool("mcp__slack__slack_post_message")])
      .startswith("VIOLATION"), False)
check("Slack directive + NO response tool at all -> violation",
      run([user(SLACK_DIRECTIVE), assistant_text("done")])
      .startswith("VIOLATION"), True)

print("\n=== B · THE FIX — the hub shape is now a recognized directive ===")
check("hub directive + NO reply -> violation (this used to be INVISIBLE)",
      run([user(HUB_DIRECTIVE_JDM), assistant_text("done, no reply sent")])
      .startswith("VIOLATION"), True)
check("hub directive + dojo-reply.mjs call -> no violation",
      run([user(HUB_DIRECTIVE_JDM), assistant_tool("Bash", command=REPLY_CMD)])
      .startswith("VIOLATION"), False)

print("\n=== C · THE DEAD REMEDY IS NO LONGER ENOUGH ===")
check("hub directive + ONLY a Slack post (the old, now-unperformable remedy) -> "
      "STILL a violation — posting to a decommissioned channel is not answering "
      "where it arrived",
      run([user(HUB_DIRECTIVE_JDM), assistant_tool("mcp__slack__slack_post_message")])
      .startswith("VIOLATION"), True)

print("\n=== D · scope discipline — declared limits, not silently widened ===")
check("hub directive from someone OTHER than JDM -> NOT judged (JDM-directive scope only)",
      run([user(HUB_DIRECTIVE_OTHER), assistant_text("stayed quiet")])
      .startswith("VIOLATION"), False)
check("an unrelated Bash call does not count as a reply",
      run([user(HUB_DIRECTIVE_JDM), assistant_tool("Bash", command="git status")])
      .startswith("VIOLATION"), True)
check("cross-warrior tmux traffic remains invisible (pre-existing scope, unchanged)",
      run([user("Mirror from SHINOB1: do the thing"), assistant_text("ok")])
      .startswith("VIOLATION"), False)
check("only the MOST RECENT directive is judged — an earlier violation does not "
      "haunt a later, correctly-answered one",
      run([user(HUB_DIRECTIVE_JDM), assistant_text("missed it"),
           user(SLACK_DIRECTIVE), assistant_tool("mcp__slack__slack_post_message")])
      .startswith("VIOLATION"), False)

print("\n=== E · snippet carries real content either era ===")
out = run([user(HUB_DIRECTIVE_JDM), assistant_text("no reply")])
check("violation snippet quotes the hub directive text, not empty",
      "do the thing" in out, True)

print()
if FAILS:
    print(f"FAILED — {len(FAILS)} case(s):")
    for f in FAILS:
        print(f"  - {f}")
    sys.exit(1)
print(f"PASSED — {5 + 2 + 1 + 4 + 1} assertions. "
      "Slack era unchanged, hub era now caught, dead remedy no longer accepted, "
      "scope not widened past JDM directives.")
sys.exit(0)
