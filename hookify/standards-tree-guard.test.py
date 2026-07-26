#!/usr/bin/env python3
"""standards-tree-guard.test.py — behavioural proof for warn-checkout-in-standards-tree.

MZ-STANDARDS-TREE-GUARD-001 (megazord, 2026-07-26).

WHY A SEPARATE FILE
-------------------
These cases belong in rule-liveness.test.py Part 2. That file is being modified on the
open MZ-POSIX-PATTERN-DEATH-001 branch, and stacking would make one PR wait on the other,
which trunk-based discipline forbids. Fold this in once both have landed.

WHAT IT PROVES, AND HOW
-----------------------
Every assertion runs through `core.rule_engine.RuleEngine` — the SAME matcher the live
dispatcher uses (`rule_engine.py:24`, a bare `re.compile(p, re.IGNORECASE)`).

That is not a stylistic choice. HIKARI verified and SIGNED two rules using `grep -P`, where
their patterns returned True; the live engine is Python `re`, where the identical patterns
returned False on the exact asks they existed to catch. grep and Python `re` are both "regex"
and disagree silently — no error, no warning, just False at runtime.

  A behavioural test on the wrong engine is not weaker evidence.
  It is evidence for a different system.

So this harness refuses to use grep, and the two-sided table below is the whole claim:
the rule must FIRE on real branch ops against the live tree, and stay QUIET on worktrees,
on reads, on worktree-creation, and on prose that merely quotes a branch op.

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

LIVE = "/home/jdm/Projects/_RPI_STANDARDS"
WORKTREE = "/home/jdm/Projects/_RPI_STANDARDS-megazord"

# (command, should_fire, label)
CASES = [
    # --- MUST FIRE: a real branch op against the live shared tree -------------
    (f"git -C {LIVE} checkout -b megazord/thing",          True,  "-C form, branch create"),
    (f"git -C {LIVE} switch main",                         True,  "-C form, switch"),
    (f"cd {LIVE} && git checkout main",                    True,  "after && (command position)"),
    (f"cd {LIVE}; git checkout -b x",                      True,  "after ; (command position)"),
    (f"cd {LIVE} && git add -A && git switch feature",     True,  "second op in a chain"),

    # --- MUST BE QUIET: worktrees are the CORRECT path -----------------------
    (f"git -C {WORKTREE} checkout -b megazord/thing",      False, "worktree, not the live tree"),
    (f"git -C {WORKTREE}-stdguard switch main",            False, "suffixed worktree"),

    # --- MUST BE QUIET: worktree creation is what the rule steers TOWARD -----
    (f"git -C {LIVE} worktree add {WORKTREE} -b b origin/main", False, "worktree add is correct"),

    # --- MUST BE QUIET: reads are safe ---------------------------------------
    (f"cat {LIVE}/hookify/hookify.block-generated-logos.local.md", False, "read a rule"),
    (f"git -C {LIVE} status --porcelain",                  False, "status is not a branch op"),
    (f"git -C {LIVE} log --oneline -1",                    False, "log is not a branch op"),

    # --- MUST BE QUIET: prose. The declaration-vs-mention half. ---------------
    (f'echo "never run git checkout main in {LIVE}"',      False, "PROSE: quoted in echo"),
    (f'echo "the guard covers {LIVE} for git switch ops"', False, "PROSE: describing the rule"),
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

print("\n" + "=" * 70)
if failures:
    print(f"FAILED — {len(failures)} problem(s), {passes} passed")
    sys.exit(1)
print(f"PASSED — {passes} behavioural checks through core.rule_engine.")
print("         Fires on real branch ops against the live tree; quiet on worktrees,")
print("         reads, worktree-creation, and prose that quotes a branch op.")
print("         KNOWN BLIND SPOT: a branch op at the start of a line inside a heredoc")
print("         still fires. Regex cannot separate a heredoc body from a script body —")
print("         which is why this rule is action: warn and not action: block.")
sys.exit(0)
