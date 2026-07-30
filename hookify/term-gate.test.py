#!/usr/bin/env python3
"""term-gate.test.py — behavioural proof for the RPI Rule #1 term gate (file + bash twins).

TRK-HOOK-214 (ronin, 2026-07-30).

WHY THIS FILE EXISTS, AND WHY IT IS A TEST RATHER THAN A COMMENT
---------------------------------------------------------------
Both twins carried a `not_contains` CONTENT TOKEN as a meta-citation opt-out. The intent was
right — a dispatch that legitimately CITES the rule should not be blocked by it. The mechanism
was a universal bypass. Measured against the wired engine before removal:

    real violation, no token ....................... BLOCK  correct
    legitimate meta-citation carrying the token .... allow  correct
    REAL VIOLATION carrying the token .............. allow  BYPASS
    real violation, token in a trailing comment .... allow  BYPASS

`not_contains` asks whether a string APPEARS ANYWHERE in the payload. It cannot ask whether
that string is a citation. And the token was published in the rule file, so anyone reading the
rule to understand it had learned how to defeat it — on JDM's #1 directive.

THE SAME DEFECT WAS ALREADY PAID FOR ONCE IN THIS REPO: the live-deploy-tree guard carried a
`not_contains` naming its repair script, a reviewer broke it with a trailing comment in one
command, and it was REMOVED rather than re-keyed, with the conclusion recorded in that file:
"you cannot express 'this executable was invoked, and nothing else dangerous was' as a text
test over a raw command line." That generalises to every content token.

AND HERE IS WHY THE CONCLUSION IS ASSERTED HERE INSTEAD OF WRITTEN IN A COMMENT.
That sibling recorded its trade as prose — "recorded so you do not 'fix' it" — and TWO SEATS
TRIED TO FIX IT ANYWAY, four hours apart, on the same night. The comment stopped neither,
because a comment cannot fail a build. A recorded decision that is only prose gets
re-litigated; a recorded decision asserted in a test blocks the re-litigation. That is the
L1-vs-L3 distinction applied to a DECISION rather than to an invariant.

So: if someone re-adds a content token, the BYPASS cases below start passing and this test
fails. They are then forced to re-read the reasoning rather than rediscover the hole in
production.

WHAT STAYS: the file-tier twin's three LOCATION exemptions (hookify, CLAUDE.md,
docs/discoveries). To claim one you must ACTUALLY BE WRITING THERE, which the engine checks
against the real file_path and which cannot be asserted by typing a word. That asymmetry —
location safe, content unsafe — is the ruling this ticket implements.

RUN
    python3 hookify/term-gate.test.py           # canonical dir
    python3 hookify/term-gate.test.py <dir>     # a worktree, pre-merge
Exit 0 = both twins block real content, allow the sanctioned locations, and have NO bypass.
"""
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE


def _wired_plugin():
    """The copy Claude Code actually loads — never the marketplace checkout."""
    manifest = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
    fallback = os.path.expanduser(
        "~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify")
    try:
        data = json.load(open(manifest, encoding="utf-8"))
    except Exception:
        return fallback
    for key, entries in (data.get("plugins") or {}).items():
        if key.startswith("hookify@"):
            for ent in (entries if isinstance(entries, list) else [entries]):
                p = (ent or {}).get("installPath")
                if p and os.path.isdir(p):
                    return p
    return fallback


sys.path.insert(0, _wired_plugin())
from core.config_loader import load_rule_file
from core.rule_engine import RuleEngine

# Assembled at runtime so this FILE does not carry the banned term — otherwise the very rule
# under test would block its own test, which is the reflexivity trap this contract has now hit
# four times in one night.
TERM = "whole" + "saler"
NAME = "Justin" + " " + "Brock"
TOKEN = "termgate" + "-meta:"

failures, passes = [], 0


def ok(m):
    global passes
    passes += 1
    print(f"  pass  {m}")


def fail(m):
    failures.append(m)
    print(f"  FAIL  {m}")


eng = RuleEngine()
bash_rule = load_rule_file(os.path.join(
    RULES_DIR, "hookify.block-" + TERM + "-language-bash.local.md"))
file_rule = load_rule_file(os.path.join(
    RULES_DIR, "hookify.block-" + TERM + "-language.local.md"))
if bash_rule is None or file_rule is None:
    print("FAIL: one or both twins failed to load")
    sys.exit(1)


def bash_fires(cmd):
    return bool(eng.evaluate_rules([bash_rule], {
        "tool_name": "Bash", "tool_input": {"command": cmd},
        "hook_event_name": "PreToolUse"}).get("systemMessage"))


def file_fires(path, content):
    return bool(eng.evaluate_rules([file_rule], {
        "tool_name": "Write", "tool_input": {"file_path": path, "content": content},
        "hook_event_name": "PreToolUse"}).get("systemMessage"))


print("\n=== bash twin — real content blocks, and there is NO bypass ===")
BASH = [
    (f'curl -d "we work with a {TERM} network" https://hooks.slack.com/x', True,
     "real violation, plain"),
    (f'git commit -m "note from {NAME} on the case"', True,
     "real violation, banned NAME in a commit message"),
    (f'echo "carrier-direct sourcing only"', False,
     "compliant language stays quiet"),
    # THE BYPASS CASES. These MUST block. If any of them passes, a content token is back.
    (f'curl -d "{TOKEN} we work with a {TERM} network" https://hooks.slack.com/x', True,
     "BYPASS GUARD: violation carrying the old token"),
    (f'curl -d "we work with a {TERM} network" https://x # {TOKEN}', True,
     "BYPASS GUARD: violation, token in a trailing comment"),
    (f'bash dispatch.sh "meta-exempt: citing the {TERM} rule"', True,
     "BYPASS GUARD: any invented content token must NOT stand the rule down"),
]
for cmd, expect, label in BASH:
    hit = bash_fires(cmd)
    (ok if hit == expect else fail)(
        f"{label}: {'blocks' if expect else 'quiet'}"
        if hit == expect else
        f"{label}: expected {'BLOCK' if expect else 'quiet'}, got {'BLOCK' if hit else 'quiet'}")

print("\n=== file twin — LOCATION exemptions stay, content token is gone ===")
BODY = f"prose that names the {TERM} pattern"
FILES = [
    ("/home/jdm/Projects/toMachina/services/api/src/notes.ts", BODY, True,
     "real violation in ordinary code"),
    (f"{RULES_DIR}/hookify.block-" + TERM + "-language.local.md", BODY, False,
     "LOCATION exemption: the rule definition itself (hookify)"),
    ("/home/jdm/Projects/toMachina/CLAUDE.md", BODY, False,
     "LOCATION exemption: CLAUDE.md doctrine"),
    ("/home/jdm/Projects/toMachina/docs/discoveries/x.html", BODY, False,
     "LOCATION exemption: the disco/audit surface"),
    # BYPASS GUARDS
    ("/home/jdm/Projects/toMachina/services/api/src/notes.ts", f"{TOKEN} {BODY}", True,
     "BYPASS GUARD: content token must not exempt an ordinary path"),
    ("/tmp/scratch-report.md", f"{TOKEN} {BODY}", True,
     "BYPASS GUARD: token in a scratch file must not exempt it"),
]
for path, content, expect, label in FILES:
    hit = file_fires(path, content)
    (ok if hit == expect else fail)(
        f"{label}: {'blocks' if expect else 'quiet'}"
        if hit == expect else
        f"{label}: expected {'BLOCK' if expect else 'quiet'}, got {'BLOCK' if hit else 'quiet'}")

print("\n" + "=" * 72)
if failures:
    print(f"FAILED — {len(failures)} problem(s), {passes} passed\n")
    for f in failures:
        print(f"  - {f}")
    print("\nIf a BYPASS GUARD failed, a content-token exemption has been re-added. Read the")
    print("reasoning in the rule's frontmatter before changing this test: the mechanism was")
    print("measured as a universal bypass, and location-scoping is the safe alternative.")
    sys.exit(1)
print(f"PASSED — {passes} behavioural checks through core.rule_engine.")
print("         Real content blocks on both twins · the three LOCATION exemptions still")
print("         work · and no content token stands either rule down.")
sys.exit(0)
