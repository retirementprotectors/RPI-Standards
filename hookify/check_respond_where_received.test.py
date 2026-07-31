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

# ---------------------------------------------------------------------------------
# F · TIE MARK_HUB TO ITS SOURCE OF TRUTH (RONIN-HOOKIFY-W8, audit of RPI#123;
#     tightened per RONIN-HOOKIFY-W5's audit of the dojo-warriors twin, dw#446)
#
# THE ORIGINAL DEFECT, ONE TURN LATER. This detector was blind because it hardcoded a
# delivery format that was later retired. Fixing the hardcode without tying it to its
# source repeats the exact failure shape: MARK_HUB is a copy of formatDelivery()'s
# output in dojo-deliver-watcher.mjs — a different repo, a different language — and
# every fixture above builds its directive from THIS FILE's own constant. Detector and
# fixtures agree with each other while both could silently diverge from reality. If the
# watcher's template changes, this suite stays 13/13 green and cannot see it.
#
# ⛔ W5's finding on the dw#446 twin of this section: restating the invariant text as
# two NEW string literals here still leaves MARK_HUB itself — the field that DECIDES
# detection — tied to nothing. Rename MARK_HUB and its fixtures together (a careless
# "update the constant" edit, the shape the edit actually takes) and this assertion
# stayed green while the detector went blind, because INVARIANT_PREFIX/SUFFIX were
# never connected to MARK_HUB, only to the watcher.
#
# So the invariant text is now DERIVED from MARK_HUB — imported as a constant, not a
# function, so this stays true to the file's own rule (drive behaviour through stdin,
# never through an imported function) while still closing the gap. If MARK_HUB drifts,
# the derived prefix/suffix drift with it and stop matching the (unchanged) watcher —
# which is exactly the recurrence this assertion exists to catch.
#
# This asserts the INVARIANT CORE PHRASE — the literal text surrounding the
# interpolated ${senderLabel} — still appears verbatim in the live watcher source.
# FAILS LOUD (not skipped) if the source file cannot be found at all: a failed read is
# an error, not evidence the invariant holds. Declared in prose gets re-litigated;
# asserted in a test it blocks the re-litigation (TRK-HOOK-237's own standing rule).
print("\n=== F · MARK_HUB is tied to dojo-deliver-watcher.mjs, not just to itself ===")
WATCHER_CANDIDATES = [
    os.path.join(HERE, "..", "..", "dojo-warriors", "mdj-agent", "scripts",
                 "dojo-deliver-watcher.mjs"),
    os.path.expanduser("~/Projects/dojo-warriors/mdj-agent/scripts/dojo-deliver-watcher.mjs"),
]

import importlib.util
_spec = importlib.util.spec_from_file_location("_detector_under_test", DETECTOR)
_detector = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_detector)
MARK_HUB = _detector.MARK_HUB  # the field that DECIDES detection — not a restated copy

_before, _sep, _after = MARK_HUB.partition("JDM")
if not _sep:
    fail_msg = f"MARK_HUB {MARK_HUB!r} does not contain 'JDM' — cannot derive the invariant"
    FAILS.append(f"MARK_HUB source tie: {fail_msg}")
    print(f"  FAIL  MARK_HUB source tie: {fail_msg}")
INVARIANT_PREFIX = _before + "${senderLabel}"
INVARIANT_SUFFIX = _after.strip()

watcher_path = next((p for p in WATCHER_CANDIDATES if os.path.isfile(p)), None)
if watcher_path is None:
    fail_msg = ("source file not found at any candidate path — CANNOT VERIFY, "
                "not treated as a pass")
    FAILS.append(f"MARK_HUB source tie: {fail_msg}")
    print(f"  FAIL  MARK_HUB source tie: {fail_msg}")
else:
    src = open(watcher_path, encoding="utf-8").read()
    tied = INVARIANT_PREFIX in src and INVARIANT_SUFFIX in src
    check(f"invariant core phrase found verbatim in {os.path.basename(watcher_path)}",
          tied, True)

print()
if FAILS:
    print(f"FAILED — {len(FAILS)} case(s):")
    for f in FAILS:
        print(f"  - {f}")
    sys.exit(1)
print(f"PASSED — {5 + 2 + 1 + 4 + 1 + 1} assertions. "
      "Slack era unchanged, hub era now caught, dead remedy no longer accepted, "
      "scope not widened past JDM directives, MARK_HUB tied to its source.")
sys.exit(0)
