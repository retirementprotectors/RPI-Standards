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


# TRK-HOOK-215 (ronin, 2026-07-30): this pointed at the MARKETPLACE checkout, which is not the
# copy Claude Code runs. installed_plugins.json names the wired build in its installPath; there
# are ~19 copies of rule_engine.py on this box and only one enforces. They agree today, which is
# exactly why it was invisible — the moment they diverge, this file certifies the rule against a
# copy that enforces nothing. Same defect corrected in rule-liveness.test.py under TRK-HOOK-101,
# and in the Discovery Doc's own citation before that; third instance of one class.
def _wired_plugin():
    import json
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


PLUGIN = _wired_plugin()

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

    # -- reviewer-chosen shapes (SHINOB1, against 4d815aa). A reviewer must pick inputs the
    #    builder could not anticipate; these four fired on my v3 and none was in my declared
    #    blind spot. `|` is itself in the operator alternation, so a table ROW is a chain
    #    operator by construction.
    (f"<!-- cd {P} && git {V} main -->",                 False, "mention: html comment"),
    (f"| cd {P} && git {V} main | bad |",                False, "mention: markdown table cell"),
    (f"1. cd {P} && git {V} main",                       False, "mention: numbered list"),
    (f"1) cd {P} && git {V} main",                       False, "mention: numbered list, paren"),
    (f"\tcd {P} && git {V} main",                        True,  "hazard: tab indent"),
    (f"(cd {P} && git {V} main)",                        True,  "hazard: subshell"),
    (f"cd {P} | git {V} main",                           True,  "hazard: pipe chain"),

    # -- reviewer-chosen HAZARD shapes (HIKARI, against 4d815aa). She built a hazard-shaped
    #    corpus because mine was mention-shaped, and found 4 FALSE NEGATIVES: real branch ops
    #    going silent because a quote appeared earlier on the line. A false negative is
    #    strictly worse than a false positive here -- the rule exists to catch exactly these.
    #    Cases 2 and 3 are byte-for-byte the incident shape that created this rule.
    (f'git -C {P} commit -m "fix the thing" && git {V} main', True, "hazard: quoted -m then chain"),
    (f"cd '{P}' && git {V} main",                         True,  "hazard: single-quoted path"),
    (f'cd "{P}" && git {S} main',                         True,  "hazard: double-quoted path"),
    (f'git -C {P} stash push -m "wip" ; git {S} main',    True,  "hazard: quoted stash then ;"),

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

    # ── TRK-HOOK-215 (ronin, 2026-07-30) — WRAPPER + PREFIX HAZARDS ─────────────────────
    # A FOURTH review pass, and the first to sample this axis. Three prior rounds all chose
    # MENTION shapes; the rule was measured 23 ways and went QUIET on 4 of 8 real branch ops
    # because nobody asked how a command could be WRAPPED. Same lesson as this file's own
    # header, one axis over: a corpus that cannot produce the shape cannot refute the claim.
    #
    # Why the shipped pattern missed all four: in the bash -c forms the && lives INSIDE a
    # quoted span, which the chain branch consumes as a unit, so the operator is never
    # available — and the line-start branch requires `git` itself at line start.
    (f'bash -c "cd {P} && git {V} main"',                True,  "hazard: bash -c, double quotes"),
    (f"bash -c 'cd {P} && git {V} main'",                True,  "hazard: bash -c, single quotes"),
    (f'sh -c "git -C {P} {S} main"',                     True,  "hazard: sh -c with the -C form"),
    (f'cd /tmp && bash -c "git -C {P} {V} main"',        True,  "hazard: wrapper after a chain op"),

    # -- DOCUMENTATION OF THE HAZARDS. The decisive corpus, and the reason the first fix
    #    attempt was thrown away: a synthetic mention list called it clean, then it fired on a
    #    real status report describing these same four shapes. Documentation of a hazard is the
    #    shape MOST likely to false-fire, because it contains the hazard verbatim.
    (f'bash n.sh "r:\n  bash -c \\"cd {P} && git {V} main\\" QUIET"', False, "DOC: bash -c double"),
    (f"bash n.sh \"r:\n  bash -c 'cd {P} && git {V} main' QUIET\"",   False, "DOC: bash -c single"),
    (f'bash n.sh "r:\n  sh -c \\"git -C {P} {S} main\\" QUIET"',      False, "DOC: sh -c"),
    (f'bash n.sh "r:\n  GIT_PAGER=cat git -C {P} {V} main QUIET"',    False, "DOC: env prefix"),

    # -- DECLARED INEXPRESSIBLE, asserted as STILL MISSED so the limit cannot rot into a
    #    silent regression. Allowing an env-var prefix catches this hazard AND fires on the
    #    DOC line above it — measured both ways, and there is no third option available to a
    #    text test. An env-prefixed branch op on this tree needs a check that reads TREE STATE,
    #    not command text: routed to TRK-HOOK-208's L2/L3 half.
    #    IF THIS EVER FIRES: either someone solved it — then delete this row and re-run the
    #    DOC cases, which is exactly where the previous attempt broke — or it fires for a
    #    reason nobody measured.
    (f"GIT_PAGER=cat git -C {P} {V} main",               False, "DECLARED-MISS: env-var prefix (TRK-HOOK-208)"),
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
print("         17/17 hazards fire | 16/16 mention + documentation shapes quiet |")
print("         9/9 safe ops quiet | 1 declared-inexpressible hazard still declared.")
print()
print("         DECLARED BLIND SPOT -- mis-stated as 'the one shape' before a reviewer")
print("         measured four more. What actually remains: an INDENTED chained")
print("         command inside a fenced code block still fires. It is byte-identical to a")
print("         real indented line in a shell script -- which SHOULD fire -- so regex cannot")
print("         separate them. Heredoc bodies are the same class. Both are why this rule")
print("         is action: warn and not action: block.")
sys.exit(0)
