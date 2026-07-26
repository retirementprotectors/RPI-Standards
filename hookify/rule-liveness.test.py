#!/usr/bin/env python3
"""rule-liveness.test.py — proves every hookify rule CAN fire, and that the two rules
activated by MZ-ACTIVATE-DEAD-RULES-001 actually DO.

MZ-ACTIVATE-DEAD-RULES-001 (megazord, 2026-07-26).

WHY THIS EXISTS
---------------
Two rules in this directory had never fired once since the day they were written:

  intent-create-disco-doc        (authored ~2026-07-08, updated for the 8-tab reconcile)
  warn-commit-missing-ticket-id  (authored 2026-06-25)

Neither was disabled. Neither was broken in any way a reader would notice. They were
DEAD because of frontmatter/filename details that produce NO error, NO log line, and NO
symptom — a rule that is loaded by nothing looks exactly like a rule that never matched.

That is the failure shape this file exists to kill: a control that cannot fail loudly.
A rule file sitting in the canonical directory reads as protection. If the loader never
picks it up, it is decoration. Nothing in the system said so.

WHAT IT CHECKS
--------------
Part 1 — STRUCTURAL LIVENESS, applied to EVERY rule in this directory. These are the
exact preconditions all three dispatchers enforce, so a rule failing any of them is
provably unable to fire:

  a) filename matches `hookify.*.local.md`
       config_loader.py:210, hookify-prompt-dispatch.py:61, hookify-stop-dispatch.py:95
       all glob for that literal shape. A file named otherwise is loaded by nothing.
  b) `event:` is one of file|bash|prompt|stop
       No dispatcher claims any other value. `PreToolUse`/`UserPromptSubmit` are Claude
       Code HOOK names, not hookify event names — a confusion that costs a rule silently.
  c) `enabled:` parses to exactly "true" or "false"
       Dispatchers compare against the literal string "true"; absent/blank != true.

Rules may opt out of (b)/(c) with an `# ALLOW-DORMANT:` line in frontmatter — used by
rules deliberately retired as documented references (e.g.
warn-firestore-collection-assumption, retired 2026-07-08 with a signed rationale).
Opting out is explicit and greppable; drifting into deadness is not.

Part 2 — BEHAVIOURAL, for the two activated rules: each must fire on its real triggers,
stay quiet on its documented escape hatches, and — critically — stay quiet when its
trigger words appear as PROSE inside another command. That last class (a rule matching
its own keywords quoted in someone else's text) is what caused five separate misfires on
2026-07-25/26, including one that injected a fabricated deploy procedure into six
warriors. A new rule is not allowed to reintroduce it.

RUN
---
    python3 hookify/rule-liveness.test.py           # canonical dir
    python3 hookify/rule-liveness.test.py <dir>     # a worktree, pre-merge

Exit 0 = all pass. Exit 1 = at least one rule cannot fire, or fires wrongly.
"""
import sys, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE
PLUGIN = os.path.expanduser(
    "~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify")

VALID_EVENTS = {"file", "bash", "prompt", "stop"}
LOADER_GLOB = "hookify.*.local.md"

failures = []
passes = 0


def fail(msg):
    failures.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg):
    global passes
    passes += 1
    print(f"  pass  {msg}")


def frontmatter(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    parts = txt.split("---")
    return parts[1] if len(parts) >= 3 else ""


# ── Part 1 — structural liveness, every rule ────────────────────────────────
print("\n=== Part 1: structural liveness (every rule in the directory) ===")
all_rules = sorted(glob.glob(os.path.join(RULES_DIR, "*.md")))
if not all_rules:
    fail(f"no rule files found in {RULES_DIR}")

for path in all_rules:
    base = os.path.basename(path)
    fm = frontmatter(path)
    if not fm:
        continue
    dormant = "# ALLOW-DORMANT:" in fm

    def field(k):
        m = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
        return (m.group(1).strip() if m else "")

    if not re.fullmatch(r"hookify\..*\.local\.md", base):
        fail(f"{base}: filename does not match loader glob '{LOADER_GLOB}' "
             f"-> loaded by NO engine, regardless of enabled/event")
        continue

    ev, en = field("event"), field("enabled")

    if dormant:
        ok(f"{base}: dormant by declaration (# ALLOW-DORMANT)")
        continue

    problems = []
    if ev not in VALID_EVENTS:
        problems.append(f"event {ev!r} not in {sorted(VALID_EVENTS)} -> no dispatcher claims it")
    if en not in ("true", "false"):
        problems.append(f"enabled {en!r} is neither 'true' nor 'false' -> dispatchers require =='true'")

    if problems:
        for p in problems:
            fail(f"{base}: {p}")
    else:
        ok(f"{base}: loadable, event={ev}, enabled={en}")


# ── Part 2 — behavioural, the two activated rules ───────────────────────────
print("\n=== Part 2: behaviour of the rules activated by MZ-ACTIVATE-DEAD-RULES-001 ===")

# -- 2a. warn-commit-missing-ticket-id (event: bash, plugin engine) ----------
print("\n-- warn-commit-missing-ticket-id (bash tier) --")
try:
    sys.path.insert(0, PLUGIN)
    import warnings
    warnings.filterwarnings("ignore")
    from core.config_loader import load_rule_file
    from core.rule_engine import RuleEngine

    rp = os.path.join(RULES_DIR, "hookify.warn-commit-missing-ticket-id.local.md")
    rule = load_rule_file(rp)
    if rule is None:
        fail("warn-commit-missing-ticket-id: engine could not load the file")
    elif not rule.enabled:
        fail("warn-commit-missing-ticket-id: loaded but enabled=False -> cannot fire")
    else:
        eng = RuleEngine()
        # (command, should_fire, label)
        cases = [
            ("git commit -m 'megazord(MZ-001): thing'",         True,  "plain commit"),
            ("git commit -m 'fixed stuff'",                     True,  "commit, no ticket id"),
            ("cd /repo && git commit -m 'x'",                   True,  "command position: after &&"),
            ("git add -A; git commit -m 'x'",                   True,  "command position: after ;"),
            ("git commit --amend -m 'x'",                       False, "escape hatch: --amend"),
            ("git commit --allow-empty -m 'x'",                 False, "escape hatch: --allow-empty"),
            ("git commit -m 'docs[no-ticket]: x'",              False, "escape hatch: [no-ticket]"),
            ("git status",                                      False, "not a commit"),
            ("echo 'how do I git commit properly'",             False, "PROSE: quoted in echo"),
            ("gh pr comment -b 'remember to git commit first'", False, "PROSE: quoted in a PR comment"),
        ]
        for cmd, expect, label in cases:
            res = eng.evaluate_rules([rule], {"tool_name": "Bash",
                                              "tool_input": {"command": cmd}})
            hit = bool(res.get("systemMessage"))
            if hit == expect:
                ok(f"{label}: {'fires' if expect else 'quiet'} — {cmd}")
            else:
                fail(f"{label}: expected {'FIRE' if expect else 'quiet'}, "
                     f"got {'FIRE' if hit else 'quiet'} — {cmd}")
except Exception as e:
    fail(f"warn-commit-missing-ticket-id: harness error: {e!r}")

# -- 2b. intent-create-disco-doc (event: prompt, prompt dispatcher) ----------
print("\n-- intent-create-disco-doc (prompt tier) --")
try:
    rp = os.path.join(RULES_DIR, "hookify.intent-create-disco-doc.local.md")
    fm = frontmatter(rp)

    def field(k):
        m = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
        return (m.group(1).strip() if m else "")

    if field("event") != "prompt":
        fail(f"intent-create-disco-doc: event is {field('event')!r}, prompt tier requires 'prompt'")
    elif field("enabled") != "true":
        fail(f"intent-create-disco-doc: enabled is {field('enabled')!r}, dispatcher requires 'true'")
    else:
        # Reproduce the dispatcher's own condition parse (hookify-prompt-dispatch.py:36-46,
        # 68-74): it reads ONLY `- field:` / `operator:` / `pattern:` triples, keeps those
        # whose field is user_prompt|prompt, and ANDs them.
        conds, cur = [], None
        for line in fm.splitlines():
            s = line.strip()
            if s.startswith("- field:"):
                cur = {"field": s.split(":", 1)[1].strip()}
                conds.append(cur)
            elif cur is not None and s.startswith("operator:"):
                cur["operator"] = s.split(":", 1)[1].strip()
            elif cur is not None and s.startswith("pattern:"):
                p = s.split(":", 1)[1].strip()
                if len(p) >= 2 and p[0] in "'\"" and p[-1] == p[0]:
                    p = p[1:-1]
                cur["pattern"] = p
        conds = [c for c in conds if c.get("field") in ("user_prompt", "prompt")]

        if not conds:
            fail("intent-create-disco-doc: dispatcher parses ZERO usable conditions "
                 "(it reads only `- field:`/`operator:`/`pattern:` triples) -> "
                 "`if not conds: continue` skips the rule")
        else:
            def fires(prompt):
                return all(c.get("operator") == "regex_match" and c.get("pattern")
                           and re.search(c["pattern"], prompt, re.IGNORECASE)
                           for c in conds)

            cases = [
                ("#LetsCreateTheDiscoDoc for sprint 9",                True,  "hashtag trigger"),
                ("#LetsCreateADiscoDoc",                              True,  "hashtag trigger (A)"),
                ("please create a discovery doc for the enrichment work", True, "natural phrasing"),
                ("write the disco doc",                               True,  "natural phrasing"),
                ("what is the status of the deploy",                  False, "unrelated"),
                ("read docs/discoveries/foo.html and summarize it",    False, "reading, not creating"),
                ("the disco doc already exists",                      False, "mentions it, no create verb"),
            ]
            for prompt, expect, label in cases:
                hit = fires(prompt)
                if hit == expect:
                    ok(f"{label}: {'fires' if expect else 'quiet'} — {prompt!r}")
                else:
                    fail(f"{label}: expected {'FIRE' if expect else 'quiet'}, "
                         f"got {'FIRE' if hit else 'quiet'} — {prompt!r}")
except Exception as e:
    fail(f"intent-create-disco-doc: harness error: {e!r}")


# ── Part 3 — the live-deploy-tree guards actually hold ──────────────────────
# MZ-LIVETREE-GUARD-001 (2026-07-26). Both of these are `action: block`, so both
# directions are load-bearing: a miss lets a warrior park a feature branch in a live
# deploy tree (which is how ~/Projects/toMachina ended up 105 commits behind on
# kagami/ob1-axe-contacts-qp-cleanup-001 for 8 days), and a false fire blocks legitimate
# worktree work, which is how guards get switched off.
print("\n=== Part 3: live-deploy-tree guards (both are action: block) ===")
try:
    sys.path.insert(0, PLUGIN)
    from core.config_loader import load_rule_file as _lrf
    from core.rule_engine import RuleEngine as _RE

    guards = []
    for n in ("hookify.block-git-checkout-main-in-worktree.local.md",
              "hookify.block-checkout-in-live-deploy-tree.local.md"):
        r = _lrf(os.path.join(RULES_DIR, n))
        if r is None:
            fail(f"{n}: failed to load")
        else:
            guards.append(r)

    if len(guards) == 2:
        _eng = _RE()

        def blocked(cmd):
            return bool(_eng.evaluate_rules(guards, {"tool_name": "Bash",
                                                     "tool_input": {"command": cmd}}).get("systemMessage"))

        cases = [
            ("git checkout main",                                             True,  "line-start checkout"),
            ("git switch main",                                               True,  "line-start switch"),
            ("git -C /home/jdm/Projects/toMachina switch main",               True,  "-C form (closed hole)"),
            ("cd /repo && git switch main",                                   True,  "after && (closed hole)"),
            ("git add -A; git checkout main",                                 True,  "after ;"),
            ("git -C /home/jdm/Projects/toMachina checkout kagami/foo",       True,  "toMachina live tree"),
            ("git -C /home/jdm/Projects/dojo-warriors checkout foo",          True,  "dojo-warriors live tree"),
            ("git -C /home/jdm/Projects/toMachina-megazord checkout foo",     False, "worktree stays allowed"),
            ("git -C /home/jdm/Projects/dojo-warriors-megazord checkout foo", False, "worktree stays allowed"),
            ("git checkout mainline-feature",                                 False, "'main' prefix, not main"),
            ("git status",                                                    False, "unrelated"),
            ("echo 'never run git checkout main here'",                       False, "prose must not block"),
        ]
        for cmd, expect, label in cases:
            h = blocked(cmd)
            if h == expect:
                ok(f"{label}: {'blocks' if expect else 'allows'} — {cmd}")
            else:
                fail(f"{label}: expected {'BLOCK' if expect else 'allow'}, "
                     f"got {'BLOCK' if h else 'allow'} — {cmd}")
except Exception as e:
    fail(f"live-tree guards: harness error: {e!r}")


# ── verdict ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
if failures:
    print(f"FAILED — {len(failures)} problem(s), {passes} passed\n")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print(f"PASSED — {passes} checks, every rule in {RULES_DIR} can fire")
sys.exit(0)
