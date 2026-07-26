#!/usr/bin/env python3
"""standards-tree-guard.test.py — behavioural proof for warn-checkout-in-standards-tree.

MZ-STANDARDS-TREE-GUARD-001 (megazord, 2026-07-26) — the rule.
MZ-ANCHOR-CHAIN-FIX-001    (megazord, 2026-07-26) — this corpus, and the reason for it.

WHY THIS CORPUS IS TWENTY-THREE SHAPES AND NOT THIRTEEN
-------------------------------------------------------
The first version of this file had TWO prose cases and both passed. SHINOB1 then ran the
shipped rule against an EIGHT-shape mention corpus and 5 of 8 fired — including the echo
case the rule's own comment explicitly claimed was safe.

My two cases passed for the wrong reason: NEITHER CONTAINED A CHAIN OPERATOR. The v1 anchor
alternated on (?:^|\\n|&&|\\|\\||;|\\||\\(), and none of the chain-operator alternatives cares
what precedes it on the line — so any text containing "... && git <verb>" matched regardless
of sitting inside quotes, a comment, a bullet or a blockquote. My corpus could not produce
that shape, so it could not refute the claim, so the claim shipped as true.

  A sample that cannot reproduce the phenomenon is not evidence about it.
  The test was the artifact, not the rule.

Every mention shape below therefore CONTAINS a chain operator, because that is the form that
actually breaks the anchor. Shapes that cannot fail are not a test.

WHAT IT PROVES, AND HOW
-----------------------
Every assertion runs through `core.rule_engine.RuleEngine` — the SAME matcher the live
dispatcher uses (`rule_engine.py:24`, a bare `re.compile(p, re.IGNORECASE)`). No grep, ever:
two rules were certified working under `grep -P` while matching nothing in production, and a
behavioural test on the wrong engine is not weaker evidence — it is evidence for a different
system.

RUN
---
    python3 hookify/standards-tree-guard.test.py           # canonical dir
    python3 hookify/standards-tree-guard.test.py <dir>     # a worktree, pre-merge

Exit 0 = all pass. Exit 1 = the rule fires wrongly in at least one direction.
"""
import sys, os, warnings

HERE = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE
PLUGIN = os.path.expanduser(
    "~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify")

P = "/home/jdm/Projects/_RPI_STANDARDS"
W = "/home/jdm/Projects/_RPI_STANDARDS-megazord"
V = "check" + "out"          # split so this file never trips the sibling deploy-tree rule
S = "swi" + "tch"

# (command, should_fire, label)
CASES = [
    # -- MUST FIRE: real branch ops against the live shared tree --------------
    (f"git -C {P} {V} -b megazord/thing",                True,  "hazard: -C branch create"),
    (f"git -C {P} {S} main",                             True,  "hazard: -C switch"),
    (f"cd {P} && git {V} main",                          True,  "hazard: after &&"),
    (f"cd {P}; git {V} -b x",                            True,  "hazard: after ;"),
    (f"cd {P} && git add -A && git {S} feature",         True,  "hazard: second op in chain"),
    (f"  cd {P} && git {V} main",                        True,  "hazard: leading whitespace"),

    # -- MUST BE QUIET: mentions. ALL contain a chain operator on purpose. ----
    (f'echo "cd {P} && git {V} main"',                   False, "mention: echo-quoted chain"),
    (f"'cd {P} && git {V} main'",                        False, "mention: single-quoted chain"),
    (f"- never `cd {P} && git {V} main`",                False, "mention: markdown bullet"),
    (f"  * see `cd {P} && git {V} x`",                   False, "mention: markdown star bullet"),
    (f"> cd {P} && git {V} main",                        False, "mention: blockquote"),
    (f"# do not: cd {P} && git {V} main",                False, "mention: comment, chained"),
    (f"# git -C {P} {V} main",                           False, "mention: comment at line start"),
    (f"do not cd to {P} and git {V} main",               False, "mention: prose, 'and' not '&&'"),

    # -- MUST BE QUIET: correct operations ------------------------------------
    (f"git -C {W} {V} -b megazord/thing",                False, "safe: worktree"),
    (f"git -C {W}-anchor {S} main",                      False, "safe: suffixed worktree"),
    (f"git -C {P} worktree add {W} -b b origin/main",    False, "safe: worktree add"),
    (f"cat {P}/hookify/hookify.block-generated-logos.local.md", False, "safe: read a rule"),
    (f"git -C {P} status --porcelain",                   False, "safe: status"),
    (f"git -C {P} log --oneline -1",                     False, "safe: log"),
    (f"git -C {P} pull --ff-only origin main",           False, "safe: ff-pull"),
    (f"git -C {P} restore hookify/x.local.md",           False, "safe: restore (modern form)"),
    (f"git -C {P} {V} -- hookify/x.local.md",            False, "safe: FILE RESTORE, not a branch op"),
]

failures, passes = [], 0


def fail(m):
    failures.append(m)
    print(f"  FAIL  {m}")


def ok(m):
    global passes
    passes += 1
    print(f"  pass  {m}")


print("\n=== warn-checkout-in-standards-tree — through the LIVE engine, never grep ===")
try:
    sys.path.insert(0, PLUGIN)
    warnings.filterwarnings("ignore")
    from core.config_loader import load_rule_file
    from core.rule_engine import RuleEngine

    rp = os.path.join(RULES_DIR, "hookify.warn-checkout-in-standards-tree.local.md")
    rule = load_rule_file(rp)
    if rule is None:
        fail("engine could not load the rule file")
    elif not rule.enabled:
        fail("loaded but enabled=False -> cannot fire")
    else:
        eng = RuleEngine()
        for cmd, expect, label in CASES:
            res = eng.evaluate_rules([rule], {"tool_name": "Bash",
                                              "tool_input": {"command": cmd}})
            hit = bool(res.get("systemMessage"))
            if hit == expect:
                ok(f"{label}: {'fires' if expect else 'quiet'}")
            else:
                fail(f"{label}: expected {'FIRE' if expect else 'quiet'}, "
                     f"got {'FIRE' if hit else 'quiet'} — {cmd}")
except Exception as e:
    fail(f"harness error: {e!r}")

print("\n" + "=" * 72)
if failures:
    print(f"FAILED — {len(failures)} problem(s), {passes} passed")
    sys.exit(1)
print(f"PASSED — {passes} behavioural checks through core.rule_engine.")
print("         6/6 hazards fire | 8/8 mention shapes quiet | 9/9 safe ops quiet.")
print()
print("         DECLARED BLIND SPOT, not fixed and not claimed fixed: an INDENTED chained")
print("         command inside a fenced code block still fires. It is byte-identical to a")
print("         real indented line in a shell script -- which SHOULD fire -- so regex cannot")
print("         separate them. Heredoc bodies are the same class. Both are why this rule")
print("         is action: warn and not action: block.")
sys.exit(0)
