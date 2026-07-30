#!/usr/bin/env python3
"""rule-liveness.test.py — proves every hookify rule is LOADABLE and that its pattern is
not silently unmatchable, and that the two rules activated by MZ-ACTIVATE-DEAD-RULES-001
actually DO fire.

⚠️ WHAT THIS FILE PROVES, AND WHAT IT DOES NOT (corrected 2026-07-26, MZ-POSIX-PATTERN-DEATH-001)
    It originally claimed to prove "every hookify rule CAN fire." That was overstated, and the
    overstatement cost a live rule: block-bulk-import-without-atlas passed every check in Part 1
    while being incapable of matching any input, because its pattern used POSIX classes that
    Python `re` does not implement. A test that asserts more than it measures does not merely
    miss a defect — it CERTIFIES the blind spot, and the next reader trusts the green.
    Part 1 now proves: loadable (a-c) AND free of the one pattern defect known to compile clean
    and never match (d). It still does NOT prove a pattern matches its INTENDED triggers — only
    a behavioural case list (Part 2) does that, and only for the rules that have one.

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

Part 2 — BEHAVIOURAL. Each rule must fire on its real triggers, stay quiet on its documented
escape hatches, and — critically — stay quiet when its trigger words appear as PROSE inside
another command. That last class (a rule matching its own keywords quoted in someone else's
text) is what caused five separate misfires on 2026-07-25/26, including one that injected a
fabricated deploy procedure into six warriors. A new rule is not allowed to reintroduce it.

    2a  warn-commit-missing-ticket-id — bash tier, hand-written case list.
    2b  EVERY event: prompt rule — all 12, not the 1 this block used to cover
        (TRK-HOOK-102). Positive probes are DERIVED from each rule's own pattern and
        verified against it before use; a rule whose probe cannot be derived is reported
        UNPROVEN rather than counted as passing, because claimed-but-unmeasured coverage is
        the exact defect that left 11 of 12 rules untested inside a green report.

Part 5 — PER-TIER VOCABULARY REACHABILITY (TRK-HOOK-101, ronin, 2026-07-30). Parts 1-4 prove a
rule is LOADED. Part 5 proves its CONDITIONS can actually evaluate, against the vocabulary of
the engine that evaluates THAT tier — because there are three engines and they do not share
one. It closes the four silent-ignore shapes the corpus can hold: unknown operator, unknown
field, zero usable conditions, and a declared external detector that does not exist. Every
operator and field name it checks against is DERIVED LIVE from each dispatcher's own source at
run time; none is written down in this file. It also emits the classification census the Phase-1
report (TRK-HOOK-104) consumes, and refuses to pass unless that census partitions the corpus.

Part 6 — THE FOURTH TIER (TRK-HOOK-101). enforce.sh is a dispatcher too, with its own rule
directory (scope-bound/), its own file glob, its own event vocabulary, and its own reachability
contract — and it never reads `enabled:`. Parts 1-5 never looked at it, which is why this file
used to say "106 rules" when the ENFORCED corpus is 112. Part 6 derives that tier from
enforce.sh's own source and judges those rules by enforce.sh's contract, never hookify's.

Parts 5 and 6 discrimination is proven separately and must stay proven:
    python3 hookify/rule-liveness-reachability-mutation.test.py

RUN
---
    python3 hookify/rule-liveness.test.py           # canonical dir
    python3 hookify/rule-liveness.test.py <dir>     # a worktree, pre-merge

Exit 0 = all pass. Exit 1 = at least one rule cannot fire, or fires wrongly.
"""
import sys, os, re, glob, json
import warnings as warnings_mod

HERE = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE


# ── WHICH PLUGIN COPY IS THE ONE THAT ENFORCES? (TRK-HOOK-101, ronin, 2026-07-30) ──
# This file used to hardcode the MARKETPLACE checkout:
#     ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify
# That is not the copy Claude Code runs. There are ~19 copies of rule_engine.py on this
# box and only ONE is wired; `installed_plugins.json` names it in its `installPath` field.
# Every copy happens to agree on the same operator set TODAY — which is exactly why this
# was invisible, and exactly why it must not stay. The moment the marketplace checkout and
# the pinned cache build diverge, this file derives its vocabulary from a copy that
# enforces nothing and reports a clean green over the wrong ground truth.
#
# Same defect class the Discovery Doc corrected in its OWN citation (v1.0 cited the
# marketplace copy; v1.1 corrected it to the pinned build) — still live in the instrument
# that is supposed to catch it. An instrument reading the wrong source is not a weak
# instrument, it is a confident one pointed somewhere else.
def _wired_plugin_path():
    """Resolve the hookify plugin copy Claude Code ACTUALLY loads, from its own manifest.

    Returns (path, provenance_string). Never guesses silently: if the manifest cannot be
    read or names no hookify install, the fallback is returned WITH a provenance string
    that says so, and Part 5 reports it rather than pretending the path is authoritative.
    """
    manifest = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
    fallback = os.path.expanduser(
        "~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify")
    try:
        data = json.load(open(manifest, encoding="utf-8"))
    except Exception as e:
        return fallback, f"UNVERIFIED fallback — could not read {manifest} ({e!r})"
    for key, entries in (data.get("plugins") or {}).items():
        if not key.startswith("hookify@"):
            continue
        for ent in (entries if isinstance(entries, list) else [entries]):
            p = (ent or {}).get("installPath")
            if p and os.path.isdir(p):
                return p, f"wired build, per {manifest} -> plugins['{key}'].installPath"
    return fallback, f"UNVERIFIED fallback — {manifest} names no installed hookify plugin"


PLUGIN, PLUGIN_PROVENANCE = _wired_plugin_path()


# ── WHICH BUILD DID THIS RUN ACTUALLY MEASURE? (TRK-HOOK-101 criterion 5) ────
# Resolving the wired path at run time (above) is necessary and NOT sufficient. A
# reachability report that does not name the engine it measured is unreproducible, and here
# that is not a hypothetical:
#
#   installed_plugins.json records hookify's gitCommitSha as 5cf3bbc9e225... — a commit in
#   ~/.claude whose subject is "auto-backup: 2026-07-30 05:00 — 254 files changed". hookify,
#   context7 and playwright all carry the SAME version string, which is the proof it
#   identifies the ENCLOSING BACKUP REPO, not each plugin's own source. There are already
#   >=5 stale hookify build dirs cached beside today's.
#
# So the manifest's identifier is regenerated by a nightly backup and cannot answer "which
# engine produced this verdict." The only identifier that survives that is the CONTENT of the
# files actually read. Every dispatcher source below is hashed as it is opened, and the digest
# is printed with the census — same defect class as the marketplace-path bug one level up:
# not "it read the wrong engine" but "it could not prove which engine it read."
def _source_identity(path):
    """(sha256[:12], bytes) of a dispatcher source, or a reason it could not be read."""
    try:
        import hashlib
        blob = open(path, "rb").read()
        return f"sha256:{hashlib.sha256(blob).hexdigest()[:12]}", len(blob)
    except Exception as e:
        return f"UNREADABLE ({e!r})", 0


def _manifest_version():
    """The version string the manifest claims for hookify — reported WITH its caveat."""
    try:
        data = json.load(open(os.path.expanduser(
            "~/.claude/plugins/installed_plugins.json"), encoding="utf-8"))
        for key, entries in (data.get("plugins") or {}).items():
            if key.startswith("hookify@"):
                for ent in (entries if isinstance(entries, list) else [entries]):
                    if (ent or {}).get("version"):
                        return ent["version"]
    except Exception:
        pass
    return None

VALID_EVENTS = {"file", "bash", "prompt", "stop"}
LOADER_GLOB = "hookify.*.local.md"

# The three dispatcher sources Part 5 derives its vocabularies FROM. These are LOCATIONS,
# not vocabularies — the whole point of Part 5 is that no operator or field name is ever
# written down in this file. If one of these files moves, Part 5 fails loud rather than
# silently checking against a smaller set of tiers.
STOP_DISPATCH = os.path.expanduser("~/.claude/hooks/hookify-stop-dispatch.py")
PROMPT_DISPATCH = os.path.expanduser("~/.claude/hooks/hookify-prompt-dispatch.py")

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

    # (d) POSIX bracket expressions in a pattern -> the rule loads clean and NEVER matches.
    #     MZ-POSIX-PATTERN-DEATH-001 (megazord, 2026-07-26).
    #
    #     Every dispatcher evaluates patterns with Python `re`. Python `re` has NO POSIX
    #     character classes. `[[:space:]]` does not mean "whitespace" — it compiles to the
    #     set [ : s p a c e followed by a literal ], so it matches a bracket or a colon and
    #     then a `]`. The regex COMPILES. It raises no error. It emits only a FutureWarning
    #     ("Possible nested set"), which the dispatchers suppress or never surface. The rule
    #     is loaded, enabled, listed as coverage — and cannot fire on any real input.
    #
    #     This is the exact failure this file exists to catch, and checks (a)-(c) all PASS it:
    #     the filename is right, the event is valid, enabled is 'true'. Structural liveness
    #     proves a rule can be LOADED. It does not prove the pattern can MATCH.
    #
    #     Caught by narrowing my own rule with `grep -E` — which DOES support POSIX classes —
    #     and shipping it to an engine that does not. Two rules, both mine, verified 0/5 on
    #     genuine triggers before the fix and 5/5 after.
    #     STRENGTHENED at HIKARI's finding (2026-07-26): a literal `[[:` search catches only the
    #     defect we already know about. The GENERAL failure is a DIALECT MISMATCH — a pattern
    #     that is valid in the tool a warrior verified with (`grep -E`, `grep -P`) and means
    #     something else, or nothing, in the engine that actually runs it. She verified and
    #     SIGNED both of these rules using `grep -P`, where the same patterns return True.
    #     grep and Python `re` are both "regex" and disagree silently: no error, no shell
    #     warning, just False at runtime.
    #
    #     So the check below does not look for a token. It compiles each pattern through the
    #     EXACT call the live matcher uses — rule_engine.py:24, `re.compile(p, re.IGNORECASE)`
    #     — with warnings promoted to failures. Any pattern the real engine cannot compile
    #     cleanly is reported, whether or not we have seen that particular defect before.
    for pl in re.findall(r"^\s*pattern:\s*(.*)$", fm, re.M):
        pl = pl.strip()
        if len(pl) >= 2 and pl[0] in "'\"" and pl[-1] == pl[0]:
            pl = pl[1:-1]
        if not pl:
            continue
        posix = re.search(r"\[\[:\w+:\]", pl)
        with warnings_mod.catch_warnings(record=True) as caught:
            warnings_mod.simplefilter("always")
            try:
                re.compile(pl, re.IGNORECASE)   # same call as rule_engine.py:24
                compile_err = None
            except re.error as e:
                compile_err = str(e)
        if compile_err:
            problems.append(
                f"pattern does not compile in the live engine (re.compile): {compile_err}")
            break
        if caught:
            detail = "; ".join(str(w.message) for w in caught)
            if posix:
                problems.append(
                    "pattern contains a POSIX bracket expression ([[:...:]]) -> Python `re` has "
                    "no POSIX classes; it compiles but can never match. Use \\s / \\d / \\w. "
                    f"[engine warning: {detail}]")
            else:
                problems.append(
                    "pattern compiles with a warning in the live engine -> it likely does not "
                    f"mean what it appears to mean. [engine warning: {detail}]")
            break

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
# -- 2b. EVERY event: prompt rule, not two of them (TRK-HOOK-102, ronin, 2026-07-30) ---
#
# WHAT THIS REPLACES, AND WHY WIDENING IT IS THE WHOLE TICKET.
# This block used to exercise ONE prompt-tier rule (intent-create-disco-doc) for the
# field-filter-drop bug it documents inline. There are TWELVE. The other eleven were
# asserted about by nothing — and the docstring at the top of this file already states the
# principle they violated: a test that asserts more than it measures does not merely miss a
# defect, it CERTIFIES the blind spot. "Part 2 — behavioural" reads like behavioural coverage
# of the prompt tier. It was behavioural coverage of 1/12 of the prompt tier.
#
# THE BUG CLASS, restated from the dispatcher's own source:
#   hookify-prompt-dispatch.py:68  conds = [c for c in r["conditions"]
#                                           if c.get("field") in ("user_prompt", "prompt")]
#   hookify-prompt-dispatch.py:69  if not conds: continue
#   hookify-prompt-dispatch.py:72  ok = all(... for c in conds)
# A condition whose field the dispatcher does not recognize is not an error. It is DROPPED
# from the AND. Losing a term from an AND makes the rule MORE PERMISSIVE — it fires on a
# strictly wider set of inputs than its author wrote. If every condition is dropped, the
# rule is skipped entirely. One defect, two opposite symptoms, neither of them visible.
#
# WHAT IS ASSERTED FOR ALL TWELVE:
#   a) the dispatcher parses >= 1 usable condition                     FAIL if not
#   b) no condition is silently dropped from the AND                   FAIL if any, naming it
#   c) a POSITIVE probe derived from the rule's own pattern fires      FAIL if it does not
#   d) neutral, unrelated inputs stay quiet                            FAIL if any fires
#   e) the trigger QUOTED INSIDE PROSE                                 REPORTED, never failed
#
# ON (c) AND HONEST COVERAGE. The probe is derived by partially un-escaping the rule's own
# regex, then VERIFIED against that regex before it is used. If the derivation cannot produce
# a verified match, the rule is reported UNPROVEN rather than passed. This is the point of the
# whole exercise: coverage that is claimed and not measured is exactly what put 11 of these 12
# rules in a green report while nothing tested them.
#
# ON (e) AND WHY IT IS NOT A FAILURE. A rule firing on its own keywords quoted in someone
# else's text is a real misfire class — it caused five separate misfires on 2026-07-25/26,
# one of which injected a fabricated deploy procedure into six warriors. But most of these
# patterns are deliberately unanchored, fixing them is not this ticket's scope, and failing on
# a defect the reader is forbidden to repair only teaches the reader to ignore the check
# (same reasoning as Part 5's stop-tier report). It is surfaced for the MISFIRING bucket.
print("\n-- ALL event: prompt rules (hit-Enter tier) --")

# Neutral controls: ordinary working requests that no intent rule should claim. If one of
# these fires, that is a LIVE misfire on real traffic, not a test artifact.
NEUTRAL_INPUTS = [
    "what is the status of the deploy",
    "read docs/discoveries/foo.html and summarize it",
    "fix the typo in the readme",
    "why did CI fail on PR 42",
    "show me the last 10 commits",
]


def _derive_probe(pattern):
    """Best-effort: build a string that MATCHES `pattern`. Verified before use, None if not.

    Deliberately partial. It handles the shapes these rules actually use (escaped
    whitespace, alternation, optional groups, word boundaries, line anchors) and gives up
    on anything else. Giving up is SAFE because the result is verified against the real
    regex before it is trusted — an un-derivable probe becomes UNPROVEN, never a false pass
    and never a false failure.
    """
    def _split_alts(s):
        out, depth, cur = [], 0, ""
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "\\" and i + 1 < len(s):
                cur += s[i:i + 2]
                i += 2
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if ch == "|" and depth == 0:
                out.append(cur)
                cur = ""
            else:
                cur += ch
            i += 1
        out.append(cur)
        return out

    def _simplify(s):
        prev = None
        while prev != s:
            prev = s
            s = re.sub(r"\(\?i\)", "", s)
            s = re.sub(r"\(\?[:=!][^()]*\)\?", "", s)      # optional non-capturing group
            s = re.sub(r"\(\?![^()]*\)", "", s)            # negative lookahead
            s = re.sub(r"\(\?=[^()]*\)", "", s)            # positive lookahead
            s = re.sub(r"\([^()|]*\)\?", "", s)            # optional simple group
            s = re.sub(r"\(\?:\^\|\\n\)", "", s)           # line-start anchor group
            # innermost group -> its first alternative
            s = re.sub(r"\(\?:([^()]*)\)", lambda m: _split_alts(m.group(1))[0], s)
            s = re.sub(r"\(([^()]*)\)", lambda m: _split_alts(m.group(1))[0], s)
            s = re.sub(r"\[\^\\n\]\*", "", s)
            s = re.sub(r"\[ \\t\][*+]", " ", s)
            s = re.sub(r"\\s[*+]", " ", s)
            s = re.sub(r"\\w[*+]", "x", s)
            s = re.sub(r"\\d[*+]", "1", s)
            s = re.sub(r"\[[^\]]*\][*?]", "", s)
            s = re.sub(r"\[([^\]^])[^\]]*\]", r"\1", s)    # char class -> first member
            s = s.replace(r"\b", "").replace(r"\B", "")
            s = re.sub(r"[\^$]", "", s)
            s = re.sub(r"\\([-./'\"#\\])", r"\1", s)
            s = re.sub(r"([a-zA-Z0-9 ])\?", r"\1", s)      # optional single char -> keep it
        return s.strip()

    for branch in _split_alts(pattern):
        cand = _simplify(branch)
        if not cand or len(cand) < 3:
            continue
        try:
            if re.search(pattern, cand, re.IGNORECASE):
                return cand
        except re.error:
            return None
    return None


_hitenter_rules = []
for _p in sorted(glob.glob(os.path.join(RULES_DIR, LOADER_GLOB))):
    _fm2 = frontmatter(_p)
    if _fm2 and re.search(r"^event:\s*prompt\s*$", _fm2, re.M):
        _hitenter_rules.append((os.path.basename(_p), _fm2))

if not _hitenter_rules:
    # Same refusal as everywhere else in this file: an empty population must not read clean.
    fail(f"no event: prompt rules found in {RULES_DIR} — refusing to report the hit-Enter "
         f"tier as covered over an EMPTY population.")
else:
    print(f"  {len(_hitenter_rules)} rule(s) under test (was 1 before TRK-HOOK-102)")

_unproven, _misfire_prose = [], []
for _base, _rfm in _hitenter_rules:
    def _f2(k, _x=_rfm):
        m = re.search(rf"^{k}:\s*(.*)$", _x, re.M)
        return (m.group(1).strip() if m else "")

    _en = _f2("enabled")

    # Reproduce the dispatcher's OWN parse (hookify-prompt-dispatch.py:21-45), not a
    # reasonable-looking equivalent. The bug being tested for lives in that parse.
    _all_conds, _cur2 = [], None
    for _line in _rfm.splitlines():
        _s2 = _line.strip()
        if _s2.startswith("- field:"):
            _cur2 = {"field": _s2.split(":", 1)[1].strip()}
            _all_conds.append(_cur2)
        elif _cur2 is not None and _s2.startswith("operator:"):
            _cur2["operator"] = _s2.split(":", 1)[1].strip()
        elif _cur2 is not None and _s2.startswith("pattern:"):
            _pv = _s2.split(":", 1)[1].strip()
            if len(_pv) >= 2 and _pv[0] in "'\"" and _pv[-1] == _pv[0]:
                _pv = _pv[1:-1]
            _cur2["pattern"] = _pv

    _ACCEPTED = ("user_prompt", "prompt")
    _kept = [c for c in _all_conds if c.get("field") in _ACCEPTED]
    _dropped = [c for c in _all_conds if c.get("field") not in _ACCEPTED]

    # (b) a dropped condition is the headline bug of this tier — name it and say what it does.
    if _dropped:
        fail(f"{_base}: {len(_dropped)} condition(s) SILENTLY DROPPED by the dispatcher — "
             f"field(s) {[c.get('field') for c in _dropped]} are not in {list(_ACCEPTED)} "
             f"(hookify-prompt-dispatch.py:68). The AND loses those terms, so the rule "
             f"matches a STRICTLY WIDER set of inputs than it was written for. Not an "
             f"error, not a log line — a permissiveness change nobody asked for.")

    # (a) every condition dropped -> the dispatcher skips the rule outright.
    if not _kept:
        fail(f"{_base}: dispatcher parses ZERO usable conditions -> "
             f"`if not conds: continue` (hookify-prompt-dispatch.py:69) skips the rule "
             f"entirely. enabled={_en!r} and it enforces nothing.")
        continue

    def _fires(text, conds=_kept):
        # hookify-prompt-dispatch.py:72-73 — regex_match only, ANDed, IGNORECASE.
        try:
            return all(c.get("operator") == "regex_match" and c.get("pattern")
                       and re.search(c["pattern"], text, re.IGNORECASE) for c in conds)
        except re.error:
            return False

    # (c) positive control, derived from the rule's own pattern and verified before use.
    _probe = None
    if len(_kept) == 1 and _kept[0].get("pattern"):
        _probe = _derive_probe(_kept[0]["pattern"])
    if _probe is None:
        _unproven.append(_base)
        print(f"  ....  {_base}: UNPROVEN — no verified positive probe could be derived "
              f"from its pattern ({len(_kept)} condition(s)). Reported as uncovered rather "
              f"than counted as passing.")
    elif _fires(_probe):
        ok(f"{_base}: fires on a probe derived from its own pattern — {_probe!r}")
    else:
        fail(f"{_base}: a probe DERIVED FROM AND VERIFIED AGAINST its own pattern "
             f"({_probe!r}) does not fire through the dispatcher's evaluation path. The "
             f"pattern matches but the rule does not — the parse or the operator is the "
             f"defect, not the regex.")

    # (d) neutral controls — an intent rule claiming ordinary work is a live misfire.
    _wrong = [p for p in NEUTRAL_INPUTS if _fires(p)]
    if _wrong:
        fail(f"{_base}: fires on {len(_wrong)} unrelated input(s) that no intent rule "
             f"should claim: {_wrong!r}. This is a live misfire on ordinary traffic.")
    else:
        ok(f"{_base}: quiet on all {len(NEUTRAL_INPUTS)} neutral control inputs")

    # (e) trigger quoted inside prose — REPORTED, never failed. See the header note.
    if _probe and _fires(f'in the runbook it says "{_probe}" is the trigger phrase'):
        _misfire_prose.append(_base)

if _misfire_prose:
    print(f"\n  -- reported, NOT failed: {len(_misfire_prose)} rule(s) also fire when their "
          f"trigger appears QUOTED INSIDE PROSE --")
    for _b in _misfire_prose:
        print(f"     {_b}")
    print("     These patterns are unanchored by design. The class is real (five misfires on "
          "2026-07-25/26, one injected a fabricated deploy procedure into six warriors) but "
          "anchoring them is not this ticket's scope. Surfaced for the MISFIRING bucket.")

if _unproven:
    print(f"\n  -- honest coverage: {len(_unproven)} of {len(_hitenter_rules)} rule(s) have "
          f"NO verified positive probe --")
    for _b in _unproven:
        print(f"     {_b}")
    print("     Reported as uncovered rather than counted as passing. This file's own "
          "docstring: a test that asserts more than it measures CERTIFIES the blind spot.")

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


# ── Part 4 — SYMLINK RESOLUTION (MZ-SYMLINK-RESOLUTION-001, 2026-07-28) ─────
#
# WHY THIS PART EXISTS, AND WHY ITS ABSENCE WAS THIS FILE'S OWN BLIND SPOT.
# Parts 1-3 inspect the rule FILES IN A DIRECTORY. The dispatcher does not read that directory
# — it reads ~/.claude, where the rules are SYMLINKS into the canonical checkout. So a rule can
# be perfect in the directory and still be loaded by nothing, if the link that points at it
# dangles.
#
# MEASURED, and it is why this exists rather than being a hypothetical:
# hookify.block-blanket-rpi-on-phi-surface.local.md was symlinked into ~/.claude on 2026-07-26
# 19:07 — roughly 35 HOURS BEFORE its target first existed on main. An `enabled: true`,
# `action: block` PHI gate sat there, looking installed, unable to fire once. It was 1 of 106,
# so this is not rot: it is the specific defect of SYMLINKING AT AUTHORING TIME RATHER THAN AT
# MERGE TIME.
#
# This file's own docstring says it exists to kill "a rule that is loaded by nothing looks
# exactly like a rule that never matched." That is precisely what happened, and Parts 1-3
# walked past it for 35 hours, because they checked the rules I could see rather than the links
# the loader follows. A CONTROL THAT INSPECTS THE WRONG POPULATION IS NOT A WEAK CONTROL, IT IS
# AN ABSENT ONE.
#
# FAILURE DIRECTION, PER BRANCH — declared before the code, and branch 2 is the one that makes
# the rest mean anything (SHINOB1's addition, and it is the population lesson pointed at me):
#   1 dangling link ......... FAIL LOUD, naming the link AND its target. Never a warning: the
#                             rule it points at is not enforcing, and silence reads as enforced.
#   2 ZERO links found ...... FAIL, never pass. zero-of-zero and 106-of-106 produce identical
#                             output. A green from an empty population is the exact defect this
#                             part exists to catch, one layer up.
#   3 ~/.claude missing ..... FAIL LOUD, never skip. "Cannot check" is not "nothing wrong."
#   4 regular file, not a
#     symlink ............... NOT a failure. Counted and reported separately — a real file is
#                             loadable; it is simply not managed by the symlink sync.
# ── SCOPE CORRECTION (MZ-LOADER-POPULATION-001, 2026-07-28) ─────────────────
# Part 4 shipped in #92 inspecting ~/.claude ONLY. THAT IS 1/147th OF THE POPULATION.
# Read the dispatcher's own source before trusting any claim about what it loads:
#
#   ~/.claude/plugins/.../hookify/core/config_loader.py
#     :210  pattern = os.path.join('.claude', 'hookify.*.local.md')
#     :211  files = glob.glob(pattern)
#
# THE PATH IS RELATIVE. The loader globs `.claude/` relative to PROCESS CWD, so the rule set
# that is live depends on WHICH DIRECTORY THE WARRIOR IS SITTING IN. Measured on this box:
# 146 project .claude dirs carry hookify rules, with counts of 89 / 90 / 92 / 105 / 106 — the
# enforcement surface is DIVERGENT PER TREE, not uniform. When this was written,
# block-blanket-rpi-on-phi-surface (an enabled action:block PHI gate) was present in ONE of
# those 146 and in ~/.claude, and absent from the other 145.
#
# So the original Part 4 reported "all 106 resolve, 0 dangling, PASS" while the directory the
# running warrior actually loads from was missing a PHI gate. A COMPLETENESS CHECK INHERITS THE
# BLINDNESS OF ITS POPULATION — third recurrence of that lesson in one night, and this one was
# inside the Part written to implement it.
#
# ALSO SETTLED HERE, so nobody re-derives it: LOADER_GLOB is PROVEN, not inferred. It is the
# loader's literal pattern at :210. A file named `hookify.foo.md` without `.local` is not loaded
# by the dispatcher AT ALL, so Part 4 skipping it is CORRECT — and Part 1 already fails it
# ("filename does not match loader glob -> loaded by NO engine"). No glob-divergence check needed.
#
# FAILURE DIRECTION, PER BRANCH:
#   1 dangling in EITHER population ... FAIL LOUD. A link that resolves globally and dangles
#                                       locally still means the rule is dead where you are.
#   2 empty population ................ FAIL, never pass (unchanged from #92).
#   3 ~/.claude missing ............... FAIL LOUD, never skip (unchanged).
#   4 regular file .................... not a failure (unchanged).
#   5 CWD .claude MISSING ENTIRELY .... report, do NOT fail. Running from a directory with no
#                                       .claude is legitimate (a scratch dir); it is not a
#                                       disarmed gate, and failing here would train people to
#                                       ignore the check.
#   6 rules in ~/.claude ABSENT from the CWD set ... FAIL. This is the finding. Those rules do
#                                       not load where you are working, silently, and the tell
#                                       is only ever a count. Name them, do not just count them.
def _scan(d):
    """Return (links, regular_files, dangling[list of (name,target)]) for one .claude dir."""
    links = regular = 0
    dangling = []
    for p in sorted(glob.glob(os.path.join(d, LOADER_GLOB))):
        if os.path.islink(p):
            links += 1
            if not os.path.exists(p):
                dangling.append((os.path.basename(p), os.readlink(p)))
        else:
            regular += 1
    return links, regular, dangling


def _names(d):
    return {os.path.basename(p) for p in glob.glob(os.path.join(d, LOADER_GLOB))}


print("\n=== Part 4: symlink resolution (the links the DISPATCHER actually follows) ===")
CLAUDE_DIR = os.path.expanduser("~/.claude")
if not os.path.isdir(CLAUDE_DIR):
    # BRANCH 3 — never skip.
    fail(f"{CLAUDE_DIR} does not exist — cannot verify what the dispatcher loads. "
         f"This is a FAILURE, not a skip: 'cannot check' is not 'nothing wrong'.")
else:
    linked = sorted(glob.glob(os.path.join(CLAUDE_DIR, LOADER_GLOB)))
    n_links = n_files = n_dangling = 0
    for p in linked:
        if os.path.islink(p):
            n_links += 1
            if not os.path.exists(p):          # follows the link; False when target is missing
                n_dangling += 1
                # BRANCH 1 — name the link AND the target, or the reader cannot act on it.
                fail(f"DANGLING SYMLINK — rule is NOT loadable: {os.path.basename(p)}\n"
                     f"          -> {os.readlink(p)}\n"
                     f"          The rule reads as installed and enforces NOTHING. Most likely "
                     f"symlinked at authoring time, before its file reached main.")
        else:
            n_files += 1

    # BRANCH 2 — an empty population must not read as success.
    if n_links == 0 and n_files == 0:
        fail(f"no rules matching {LOADER_GLOB} found in {CLAUDE_DIR} — refusing to report PASS "
             f"over an EMPTY POPULATION. examined(0) == existing(0) is not evidence; it is the "
             f"absence of evidence. Check the path before trusting this result.")
    else:
        if n_dangling == 0 and n_links > 0:
            ok(f"~/.claude: all {n_links} symlinked rules resolve")
        if n_files:
            ok(f"~/.claude: {n_files} rule(s) present as regular files (not symlink-managed) — "
               f"loadable, reported for completeness rather than as a defect")
        print(f"  ~/.claude population: {n_links} symlink(s) + {n_files} regular file(s) "
              f"= {n_links + n_files} examined, {n_dangling} dangling")

# NOTE: this block is DELIBERATELY NOT nested under the ~/.claude check above. It was,
# and that was the same blindness one mirror over: if ~/.claude were missing we failed on
# it and never examined the CWD set — the population the loader ACTUALLY globs. The two
# populations are independent and both must always be reported. (HIKARI, review of #92:
# "do not let 'N resolve in ~/.claude' print while the CWD tree is unexamined.")
# ── the population the loader ACTUALLY globs for this invocation ────────────
cwd_dir = os.path.join(os.getcwd(), ".claude")
print(f"\n  -- CWD-relative population (what config_loader.py:210 globs right now) --")
print(f"  cwd: {os.getcwd()}")
if not os.path.isdir(cwd_dir):
    # BRANCH 5 — legitimate, not a disarmed gate. Report, do not fail.
    print(f"  {cwd_dir} does not exist — no project-local rule set for this directory. "
          f"Reported, NOT failed: running from a dir with no .claude is legitimate.")
else:
    c_links, c_files, c_dangling = _scan(cwd_dir)
    for name, target in c_dangling:
        # BRANCH 1 — dangling HERE means dead HERE, even if it resolves globally.
        fail(f"DANGLING SYMLINK in the CWD rule set — rule is NOT loadable from this "
             f"directory: {name}\n          -> {target}")
    if c_links + c_files == 0:
        print(f"  {cwd_dir} exists but holds no {LOADER_GLOB} — no project-local rules.")
    else:
        if not c_dangling and c_links:
            ok(f"CWD .claude: all {c_links} symlinked rule(s) resolve")
        elif not c_dangling:
            # zero-of-zero must not print like N-of-N. Not a failure — c_files>0 here, so
            # the population is real, it is simply not symlink-managed.
            print(f"  CWD .claude: 0 symlinks to resolve ({c_files} regular file(s)) — "
                  f"nothing checked, so nothing is claimed.")
        print(f"  CWD population: {c_links} symlink(s) + {c_files} regular file(s) "
              f"= {c_links + c_files} examined, {len(c_dangling)} dangling")

        # BRANCH 6 — THE FINDING. Rules that exist globally but not here do not load here.
        # BRANCH 7 — the BASELINE of that comparison must itself be proven non-empty.
        #     set() - anything == set(), so an absent or empty ~/.claude makes `missing`
        #     empty and branch 6 prints a PASS — while ~/.claude was never read at all.
        #     Branch 2 refuses exactly this ("examined(0) == existing(0) is not evidence")
        #     for the ~/.claude population; branch 6 then reported that PASS anyway, eleven
        #     lines later, over that same empty population. The rule was stated and not
        #     applied to the comparison's own baseline. This is the fourth recurrence of
        #     "a completeness check inherits the blindness of its population" — this time
        #     INSIDE the fix for the third. (HIKARI, review of #94.)
        baseline = _names(CLAUDE_DIR)
        missing = sorted(baseline - _names(cwd_dir))
        if not baseline:
            fail(f"BASELINE EMPTY — the CWD rule set was compared against NOTHING. "
                 f"{CLAUDE_DIR} yielded 0 rules matching {LOADER_GLOB} (absent, or present "
                 f"and empty), so 'missing nothing' is vacuously true and carries no "
                 f"information. Refusing to report PASS: this is the absence of evidence, "
                 f"not evidence of absence. Fix the baseline, then re-read this result.")
        elif missing:
            fail(f"{len(missing)} rule(s) present in ~/.claude are ABSENT from the CWD rule "
                 f"set — they DO NOT LOAD when working from this directory:\n          "
                 + "\n          ".join(missing)
                 + f"\n          The dispatcher globs .claude/ RELATIVE TO CWD "
                   f"(config_loader.py:210), so a rule missing here is not enforcing here, "
                   f"however green it looks globally. Named rather than counted: a count "
                   f"alone is what let a PHI gate sit dead.")
        else:
            # Name the BASELINE, not the examined set. The old message reported the CWD
            # count, which reads as "a real comparison over N rules" even when the thing
            # compared against was empty. The load-bearing number is the baseline size.
            ok(f"CWD rule set is not missing anything present in ~/.claude "
               f"(compared against {len(baseline)} baseline rule(s); "
               f"{len(_names(cwd_dir))} present here)")


# ── Part 5 — PER-TIER VOCABULARY REACHABILITY (TRK-HOOK-101, ronin, 2026-07-30) ──
#
# WHAT THIS PART KILLS, AND WHY PARTS 1-4 CANNOT.
# Parts 1-4 prove a rule is LOADED: right filename, valid event, enabled parses, pattern
# compiles, symlink resolves in both populations. A rule can pass all of that and still be
# incapable of matching anything, because the engine that evaluates it silently ignores
# whatever it does not understand:
#
#   rule_engine.py:178-180   unknown OPERATOR  -> `else: return False`   (no log, no error)
#   rule_engine.py:159-160   unknown FIELD     -> `None` -> return False (no log, no error)
#   rule_engine.py:117-118   zero CONDITIONS   -> `return False`         (no log, no error)
#   *-dispatch.py            field not in the tier's own filter -> `continue` (rule skipped)
#
# Four ways to be dead. All four read EXACTLY like a working rule from the file, from the
# directory listing, from ~/.claude, and from every fire-count instrument in this corpus.
#
# THE FINDING THAT SHAPES THIS PART: THERE IS NO SHARED VOCABULARY.
# Three independent engines evaluate hookify conditions, and each implements its own
# operator AND field set, with no contract between them:
#
#   file/bash -> rule_engine.py           (the plugin, via enforce.sh/PreToolUse)
#   stop      -> hookify-stop-dispatch.py (standalone)
#   prompt    -> hookify-prompt-dispatch.py (standalone)
#
# The SAME condition line is correct on one tier and silently dead on another. `regex_not_match`
# works on a stop rule and dies on a file rule. `field: last_assistant_message` works on a stop
# rule and dies on a file rule. Nothing in a rule file tells its author which vocabulary applies,
# and the v1.0 Discovery Doc got this wrong in exactly the predicted direction — it checked all
# four `regex_not_match` uses against ONE engine's list and produced three false positives.
#
# So this Part derives EVERY vocabulary PER TIER, LIVE, FROM THAT TIER'S OWN DISPATCHER SOURCE.
# There is not one operator name or field name written down anywhere below. That is not style:
# a hardcoded copy of a third-party value is the exact defect this scope exists to eliminate,
# and it goes stale silently the moment the plugin auto-updates. (Q2, SHINOB1 ruling B + JDM,
# 2026-07-30 — non-optional. Technique inherited from render-hook-inventory.sh, which already
# derives supported frontmatter KEYS this way; this is the same trick one level down.)
#
# FAILURE DIRECTION, DECLARED BEFORE THE CODE:
#   1 a derived vocabulary comes back EMPTY ... FAIL LOUD, never pass. An empty whitelist makes
#         every rule look compliant — `x not in set()` is False for all x. This is the same
#         "green over an empty population" defect Part 4 branch 2 and branch 7 already refuse,
#         one layer over: here the empty population is the CHECK'S OWN BASELINE.
#   2 a dispatcher source is MISSING ......... FAIL LOUD, never skip. "Cannot derive" is not
#         "nothing wrong" — it means an entire tier went unchecked.
#   3 unknown OPERATOR for the rule's tier ... FAIL, naming the tier and the tier's real set.
#   4 unknown FIELD for the rule's tier ...... FAIL, but only after EMPIRICALLY PROVING it (see
#         below). Never on the static list alone.
#   5 zero usable CONDITIONS ................. FAIL, unless the rule declares an `implementation:`
#         naming a real script — and that script's existence is VERIFIED, not believed.
#
# WHY THE FIELD CHECK PROBES INSTEAD OF ASSERTING.
# rule_engine._extract_field's FIRST branch is `if field in tool_input` — a DYNAMIC lookup whose
# keys depend on which tool fired. A purely static "is this name in the source" check would flag
# every legitimate tool-specific field as broken. So for each suspect field this Part CALLS the
# live engine's own _extract_field across every tool the engine implements, with a tool_input
# built from the keys the engine itself reads, and only reports the field dead when the engine
# returns None for ALL of them. Not "this name is not in a list I derived" — "I ran the wired
# engine and it could not produce a value under any tool."
print("\n=== Part 5: per-tier vocabulary reachability (operators, fields, conditions) ===")
print(f"  plugin copy under test: {PLUGIN}")
print(f"  provenance: {PLUGIN_PROVENANCE}")
if PLUGIN_PROVENANCE.startswith("UNVERIFIED"):
    # Not fatal on its own, but it must never pass silently: every verdict below would be
    # derived from a copy that may not be the one enforcing.
    fail("plugin path is UNVERIFIED — every operator/field verdict in Part 5 is derived from a "
         f"copy that may not be the one Claude Code loads. {PLUGIN_PROVENANCE}")


def _func_body(src, name):
    """Return the source text of a top-level-or-method `def name(...)`, body included."""
    m = re.search(rf"^([ \t]*)def {re.escape(name)}\(", src, re.M)
    if not m:
        return ""
    indent = len(m.group(1))
    lines = src[m.start():].splitlines()
    out = [lines[0]]
    for ln in lines[1:]:
        if ln.strip() and (len(ln) - len(ln.lstrip())) <= indent:
            break
        out.append(ln)
    return "\n".join(out)


def _quoted_names(blob):
    """Pull identifier-shaped quoted names out of a `... in ('a', 'b')` / `[...]` blob."""
    out = set()
    for raw in blob.split(","):
        v = raw.strip().strip("'\"").strip()
        if v.isidentifier():
            out.add(v)
    return out


def _derive_plugin(src):
    """Operators + statically-named fields + tool_input keys + tool names, from rule_engine.py."""
    cond = _func_body(src, "_check_condition")
    ops = set(re.findall(r"operator\s*==\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", cond))
    for grp in re.findall(r"operator\s+in\s+[\[\(]([^\]\)]*)[\]\)]", cond):
        ops |= _quoted_names(grp)

    ext = _func_body(src, "_extract_field")
    fields = set(re.findall(r"field\s*==\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", ext))
    for grp in re.findall(r"field\s+in\s+[\[\(]([^\]\)]*)[\]\)]", ext):
        fields |= _quoted_names(grp)
    # the keys the engine itself reads off tool_input — used to BUILD the probe payload,
    # so the probe exercises the engine with the exact shape it expects.
    ti_keys = set(re.findall(r"tool_input\.get\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", ext))
    tools = set(re.findall(r"tool_name\s*==\s*['\"]([A-Za-z][A-Za-z0-9_]*)['\"]", ext))
    for grp in re.findall(r"tool_name\s+in\s+[\[\(]([^\]\)]*)[\]\)]", ext):
        tools |= _quoted_names(grp)
    dynamic = bool(re.search(r"field\s+in\s+tool_input", ext))
    return ops, fields, ti_keys, tools, dynamic


def _derive_standalone(path):
    """Operators + fields for a standalone dispatcher, from its own source."""
    src = open(path, encoding="utf-8", errors="replace").read()
    ops = set(re.findall(r"\bop\s*==\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", src))
    ops |= set(re.findall(r"c\.get\(['\"]operator['\"]\)\s*==\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]",
                          src))
    for grp in re.findall(r"\bop\s+in\s+[\[\(]([^\]\)]*)[\]\)]", src):
        ops |= _quoted_names(grp)
    fields = set()
    for grp in re.findall(r"c\.get\(['\"]field['\"]\)\s+in\s+[\[\(]([^\]\)]*)[\]\)]", src):
        fields |= _quoted_names(grp)
    return ops, fields


# ── derive all three vocabularies ───────────────────────────────────────────
TIER_OPS, TIER_FIELDS = {}, {}
plugin_ti_keys, plugin_tools, plugin_dynamic = set(), set(), False
_engine_src_path = os.path.join(PLUGIN, "core", "rule_engine.py")
try:
    _src = open(_engine_src_path, encoding="utf-8", errors="replace").read()
    _ops, _flds, plugin_ti_keys, plugin_tools, plugin_dynamic = _derive_plugin(_src)
    for tier in ("file", "bash"):
        TIER_OPS[tier], TIER_FIELDS[tier] = _ops, _flds
except Exception as e:
    # BRANCH 2 — an unreadable dispatcher means a whole tier goes unchecked. Never a skip.
    fail(f"cannot derive the file/bash vocabulary — {_engine_src_path} unreadable ({e!r}). "
         f"Two tiers (60 file + 25 bash rules) would go UNCHECKED and this file would still "
         f"print PASS. Refusing.")

for tier, dpath in (("stop", STOP_DISPATCH), ("prompt", PROMPT_DISPATCH)):
    try:
        TIER_OPS[tier], TIER_FIELDS[tier] = _derive_standalone(dpath)
    except Exception as e:
        fail(f"cannot derive the {tier} vocabulary — {dpath} unreadable ({e!r}). That tier "
             f"would go UNCHECKED. Refusing.")

# BRANCH 1 — an empty vocabulary is not a permissive one, it is a blind one.
for tier in sorted(set(TIER_OPS) | set(TIER_FIELDS)):
    if not TIER_OPS.get(tier):
        fail(f"derived EMPTY operator set for tier {tier!r} — refusing to check against nothing. "
             f"`op not in set()` is False for every op, so every rule would read as compliant. "
             f"The derivation regex no longer matches this dispatcher's source; fix the "
             f"derivation, do not trust this result.")
    if not TIER_FIELDS.get(tier):
        fail(f"derived EMPTY field set for tier {tier!r} — refusing to check against nothing "
             f"(same reason as the operator set above).")

if TIER_OPS:
    print("\n  -- vocabularies derived live, per tier (nothing below is written in this file) --")
    for tier in sorted(TIER_OPS):
        src_label = {"file": "rule_engine.py", "bash": "rule_engine.py",
                     "stop": os.path.basename(STOP_DISPATCH),
                     "prompt": os.path.basename(PROMPT_DISPATCH)}[tier]
        print(f"  {tier:<7} [{src_label}]")
        print(f"          operators: {sorted(TIER_OPS.get(tier) or [])}")
        print(f"          fields:    {sorted(TIER_FIELDS.get(tier) or [])}")
    if plugin_dynamic:
        print(f"  note: rule_engine._extract_field also resolves ANY key present in tool_input "
              f"(dynamic) — which is why unknown file/bash fields are PROBED below, not "
              f"failed on the static list alone.")

# ── the empirical probe: can the live engine produce a value for this field, under ANY tool? ──
_probe_engine = None
if plugin_ti_keys and plugin_tools:
    try:
        sys.path.insert(0, PLUGIN)
        from core.rule_engine import RuleEngine as _ProbeRE
        _probe_engine = _ProbeRE()
    except Exception as e:
        fail(f"cannot import the wired engine for the field probe ({e!r}) — unknown-field "
             f"verdicts would rest on a static list alone. Refusing to claim them.")

_PROBE_SENTINEL = "__ronin_probe_value__"


def _field_is_dead(field_name):
    """Run the WIRED engine's own _extract_field for `field_name` under every tool it
    implements. Returns (dead, detail). dead=True only when the engine yields None for
    every tool — i.e. the condition can never receive a value, so it can never match."""
    if _probe_engine is None:
        return False, "probe unavailable"
    payload = {k: _PROBE_SENTINEL for k in plugin_ti_keys}
    resolved = []
    for tool in sorted(plugin_tools):
        try:
            v = _probe_engine._extract_field(field_name, tool, payload, {})
        except Exception as e:
            return False, f"probe raised for tool {tool}: {e!r}"
        if v is not None:
            resolved.append(f"{tool}={'<empty string>' if v == '' else 'value'}")
    if resolved:
        return False, "resolves under " + ", ".join(resolved)
    return True, ("engine returned None for every tool it implements "
                  f"({', '.join(sorted(plugin_tools))})")


def _conditions(fm):
    """Parse `- field:/operator:/pattern:` triples — the shape ALL THREE dispatchers read."""
    conds, cur = [], None
    for line in fm.splitlines():
        s = line.strip()
        if s.startswith("- field:"):
            cur = {"field": s.split(":", 1)[1].strip()}
            conds.append(cur)
        elif cur is not None and s.startswith("operator:"):
            cur["operator"] = s.split(":", 1)[1].strip()
        elif cur is not None and s.startswith("pattern:"):
            cur["pattern"] = s.split(":", 1)[1].strip()
    return conds


# Buckets, for the Phase-1 classification report (TRK-HOOK-104 consumes this).
# G1 requires these to SUM TO THE CORPUS with every rule in exactly one place. A census that
# quietly drops the rules it had nothing to say about is the same "green over an incomplete
# population" defect Part 4 exists to kill — the rules most likely to be dropped are the odd
# ones, which are exactly the ones worth looking at.
BUCKETS = {"unknown-operator": [], "unknown-field": [], "zero-conditions": [],
           "reachable-clean": [], "reachable-external-detector": [],
           "reachable-legacy-pattern": [], "dormant-declared": [], "not-checked": []}
# Reported separately, and DELIBERATELY NOT A FAILURE — see the stop-tier note below.
STOP_DUAL_ENGINE = []

if TIER_OPS and not [f for f in failures if "derived EMPTY" in f]:
    for path in sorted(glob.glob(os.path.join(RULES_DIR, LOADER_GLOB))):
        base = os.path.basename(path)
        fm = frontmatter(path)
        if not fm:
            continue

        def _f(k, _fm=fm):
            m = re.search(rf"^{k}:\s*(.*)$", _fm, re.M)
            return (m.group(1).strip() if m else "")

        ev, en = _f("event"), _f("enabled")
        if "# ALLOW-DORMANT:" in fm:
            BUCKETS["dormant-declared"].append(base)
            continue
        if ev not in TIER_OPS:
            # Part 1 already fails an invalid event with the right message; Part 5 must not
            # double-report it, but it must not silently drop it from the census either.
            BUCKETS["not-checked"].append(f"{base} (event={ev!r} — no tier claims it)")
            continue

        ops_ok, flds_ok = TIER_OPS[ev], TIER_FIELDS[ev]
        conds = _conditions(fm)
        problems = []

        # --- (5a) unknown operator, against this rule's OWN tier ---
        for c in conds:
            op = c.get("operator")
            if op and op not in ops_ok:
                other = sorted(t for t in TIER_OPS if op in (TIER_OPS.get(t) or ()))
                hint = (f" It IS supported on the {'/'.join(other)} tier — the same line is "
                        f"correct there and dead here." if other else "")
                problems.append(("unknown-operator",
                                 f"operator {op!r} is not implemented by the {ev} tier "
                                 f"({sorted(ops_ok)}) -> rule_engine.py's `else: return False` "
                                 f"branch, silently, every time.{hint}"))

        # --- (5b) unknown field, against this rule's OWN tier, PROVEN not assumed ---
        for c in conds:
            fld = c.get("field")
            if not fld or fld in flds_ok:
                continue
            if ev in ("file", "bash"):
                dead, detail = _field_is_dead(fld)
                if dead:
                    problems.append(("unknown-field",
                                     f"field {fld!r} is not implemented by the {ev} tier — "
                                     f"PROBED against the wired engine: {detail}. "
                                     f"_extract_field returns None -> _check_condition returns "
                                     f"False -> conditions are ANDed, so this rule can NEVER "
                                     f"match. Engine's real fields: {sorted(flds_ok)}."))
                # resolves under some tool -> legitimate tool-specific field, not a defect.
            else:
                # standalone dispatchers filter conditions by field and `continue` on none —
                # an unlisted field is dropped from the AND before evaluation.
                problems.append(("unknown-field",
                                 f"field {fld!r} is not in the {ev} dispatcher's own filter "
                                 f"{sorted(flds_ok)} -> the condition is DROPPED from the AND "
                                 f"before evaluation."))

        # --- (5c) zero usable conditions ---
        usable = [c for c in conds if c.get("field") in flds_ok]
        if not usable:
            impl = _f("implementation")
            script = None
            m = re.search(r"([A-Za-z0-9_.-]+\.(?:sh|py))", impl)
            if m:
                cand = m.group(1)
                for d in (RULES_DIR, os.path.expanduser("~/.claude/hooks")):
                    if os.path.exists(os.path.join(d, cand)):
                        script = os.path.join(d, cand)
                        break
            has_legacy = bool(_f("pattern"))
            if script:
                # Declared AND verified. The declaration alone is not enough — a rule that
                # names a script that does not exist is the same lie with better paperwork.
                BUCKETS["reachable-external-detector"].append(base)
                ok(f"{base}: zero generic conditions, but implementation: names a real "
                   f"detector ({os.path.basename(script)}) — dispatched outside the "
                   f"condition engine, not dead")
            elif has_legacy and ev in ("file", "bash"):
                # config_loader.py:56-73 converts a bare `pattern:` into one condition.
                BUCKETS["reachable-legacy-pattern"].append(base)
                ok(f"{base}: zero explicit conditions, legacy `pattern:` auto-converts "
                   f"(config_loader.py:56-73) -> 1 condition, loadable")
            elif m and not script:
                problems.append(("zero-conditions",
                                 f"zero usable conditions AND its implementation: names "
                                 f"{m.group(1)!r}, which does NOT exist in {RULES_DIR} or "
                                 f"~/.claude/hooks. The declaration reads as coverage and "
                                 f"points at nothing."))
            else:
                problems.append(("zero-conditions",
                                 f"zero conditions usable by the {ev} tier (fields present: "
                                 f"{sorted({c.get('field') for c in conds}) or 'none'}; tier "
                                 f"accepts {sorted(flds_ok)}) -> the dispatcher skips this rule "
                                 f"entirely. It is enabled={en!r} and enforces nothing."))

        if problems:
            for bucket, msg in problems:
                BUCKETS[bucket].append(base)
                fail(f"{base} [{ev} tier]: {msg}")
        elif usable:
            BUCKETS["reachable-clean"].append(base)

    # ── (5d) THE STOP TIER IS EVALUATED BY TWO ENGINES THAT DISAGREE ────────
    #
    # RESOLVED EMPIRICALLY 2026-07-30 (shinob1-project-hookify-overhaul, positive control
    # attached; HIKARI ruling relayed same session): the hookify plugin's MANIFEST-declared
    # hooks fire independently of ~/.claude/settings.json's explicit hooks array. So a
    # `event: stop` rule is read by BOTH engines on every turn:
    #
    #   hookify-stop-dispatch.py  fields: derived above  ·  action:block => INJECTS A GLYPH
    #   plugin stop.py -> rule_engine  fields: the file/bash set  ·  action:block => REAL
    #                                  {"decision":"block"} forced continuation
    #
    # Every conditioned stop rule in this corpus uses a field the STANDALONE engine defines
    # and the PLUGIN engine does not. Under the plugin they extract None and are inert.
    #
    # THIS IS REPORTED, NOT FAILED, AND THE DIRECTION IS DELIBERATE.
    # The "fix" — migrating these onto a plugin-supported field — would convert a rule that
    # renders a glyph today into a hard forced continuation in an engine that does NOT check
    # stop_hook_active, fleet-wide, on every warrior session. That is strictly more dangerous
    # than the inertness it repairs, and it is explicitly OUT of TRK-HOOK-202's scope by
    # ruling; the stop engine is TRK-HOOK-106's subject. A gate that fails on something the
    # reader is forbidden to fix trains the reader to ignore the gate — the same reasoning
    # Part 4 branch 5 already applies to a missing CWD .claude.
    _plugin_fields = TIER_FIELDS.get("file") or set()
    _plugin_ops = TIER_OPS.get("file") or set()
    for path in sorted(glob.glob(os.path.join(RULES_DIR, LOADER_GLOB))):
        fm = frontmatter(path)
        if not fm or re.search(r"^event:\s*stop\s*$", fm, re.M) is None:
            continue
        base = os.path.basename(path)
        conds = _conditions(fm)
        if not conds:
            continue
        inert = sorted({c["field"] for c in conds
                        if c.get("field") and c["field"] not in _plugin_fields})
        badop = sorted({c["operator"] for c in conds
                        if c.get("operator") and c["operator"] not in _plugin_ops})
        if inert or badop:
            action = (re.search(r"^action:\s*(.*)$", fm, re.M) or [None, "?"])[1] if \
                re.search(r"^action:\s*(.*)$", fm, re.M) else "?"
            enabled = (re.search(r"^enabled:\s*(.*)$", fm, re.M) or [None, "?"])[1] if \
                re.search(r"^enabled:\s*(.*)$", fm, re.M) else "?"
            STOP_DUAL_ENGINE.append((base, action.strip(), enabled.strip(), inert, badop))

    if STOP_DUAL_ENGINE:
        print("\n  -- stop tier: LIVE under the standalone dispatcher, INERT under the plugin "
              "engine (reported, not failed — TRK-HOOK-106) --")
        for base, action, enabled, inert, badop in STOP_DUAL_ENGINE:
            bits = []
            if inert:
                bits.append(f"field(s) {inert} absent from the plugin engine")
            if badop:
                bits.append(f"operator(s) {badop} absent from the plugin engine")
            print(f"  {base}\n      action={action} enabled={enabled} — " + "; ".join(bits))
        print(f"  {len(STOP_DUAL_ENGINE)} stop rule(s) affected. These fire correctly today via "
              f"hookify-stop-dispatch.py. Do NOT 'fix' them onto plugin-supported fields: the "
              f"plugin engine turns action:block into a real forced continuation and does not "
              f"check stop_hook_active. Routed to TRK-HOOK-106, not TRK-HOOK-202.")

    # ── census — a TRUE PARTITION: every rule in exactly one bucket, sum stated (G1) ──
    print("\n  -- classification census (TRK-HOOK-104 consumes this) --")
    defective = (set(BUCKETS["unknown-operator"]) | set(BUCKETS["unknown-field"])
                 | set(BUCKETS["zero-conditions"]))
    for bucket in ("reachable-clean", "reachable-external-detector", "reachable-legacy-pattern",
                   "unknown-operator", "unknown-field", "zero-conditions",
                   "dormant-declared", "not-checked"):
        names = sorted(set(BUCKETS[bucket]))
        print(f"  {bucket:<28} {len(names):>3}")
        if bucket not in ("reachable-clean",) and names:
            for nm in names:
                print(f"                               - {nm}")
    total = len(glob.glob(os.path.join(RULES_DIR, LOADER_GLOB)))
    partition = (len(set(BUCKETS["reachable-clean"])) + len(set(BUCKETS["reachable-external-detector"]))
                 + len(set(BUCKETS["reachable-legacy-pattern"])) + len(defective)
                 + len(set(BUCKETS["dormant-declared"])) + len(set(BUCKETS["not-checked"])))
    # ── MEASURED AGAINST — makes this run reproducible (criterion 5) ────────
    # Printed WITH the census, not in a header nobody scrolls back to: a verdict and the
    # identity of the engine that produced it belong in the same block.
    print("\n  -- measured against (content digests — the only identity that survives the "
          "nightly ~/.claude backup rewriting the manifest's sha) --")
    for _label, _spath in (("file/bash", os.path.join(PLUGIN, "core", "rule_engine.py")),
                           ("file/bash loader", os.path.join(PLUGIN, "core", "config_loader.py")),
                           ("stop", STOP_DISPATCH),
                           ("prompt", PROMPT_DISPATCH),
                           ("scope-bound", os.path.join(RULES_DIR, "enforce.sh"))):
        _digest, _nbytes = _source_identity(_spath)
        print(f"  {_label:<17} {_digest}  {_nbytes:>7} B  {_spath}")
    _mv = _manifest_version()
    if _mv:
        print(f"  manifest version string: {_mv} — NOT a plugin-source identifier. The same "
              f"value is recorded for unrelated plugins; it identifies the enclosing "
              f"~/.claude backup commit and is regenerated nightly. Cite the digests above.")

    print(f"\n  distinct rule files with >=1 defect: {len(defective)}  "
          f"(a rule with two defect kinds is listed under both above, counted ONCE here)")
    print(f"  partition sum: {partition}   corpus total: {total}")
    if partition != total:
        # G1's acceptance is that this sums. If it does not, the census is not a census and
        # no reader should be asked to eyeball which rules fell out.
        missing = sorted(
            {os.path.basename(p) for p in glob.glob(os.path.join(RULES_DIR, LOADER_GLOB))}
            - (set(BUCKETS["reachable-clean"]) | set(BUCKETS["reachable-external-detector"])
               | set(BUCKETS["reachable-legacy-pattern"]) | defective
               | set(BUCKETS["dormant-declared"]) | set(BUCKETS["not-checked"])))
        fail(f"CENSUS DOES NOT PARTITION THE CORPUS — {partition} classified vs {total} rule "
             f"files. {len(missing)} rule(s) fell through every branch and are silently "
             f"unclassified:\n          " + "\n          ".join(missing)
             + "\n          G1 requires the report to sum to the corpus. An unclassified rule "
               "is not a clean rule; it is a rule this instrument had nothing to say about, "
               "which is the population it was written to stop losing.")
    else:
        ok(f"census partitions the corpus exactly: {partition} classified == {total} rule files")


# ── Part 6 — THE FOURTH TIER: scope-bound/ (TRK-HOOK-101, ronin, 2026-07-30) ──
#
# THE POPULATION THIS WHOLE FILE WAS MISSING.
# Parts 1-5 examine `hookify.*.local.md` in ONE directory. There is a fourth dispatcher —
# enforce.sh — with its own rule directory (`scope-bound/`), its own file glob, its own event
# vocabulary, and its own definition of what makes a rule reachable. Six live rule files sit
# there. Five have real fires on record. Parts 1-5 never looked at any of them, so this file's
# headline number was 106 when the ENFORCED corpus is 112.
#
# That is this file's own recurring lesson, for the fifth time and at the widest scope yet:
# A COMPLETENESS CHECK INHERITS THE BLINDNESS OF ITS POPULATION. Part 4 learned it about
# ~/.claude vs the 146 CWD trees. Part 4 branch 7 learned it about its own baseline. Here the
# missed population is not a directory — it is an entire DISPATCHER.
#
# WHY THIS IS A DERIVED TIER AND NOT AN EXCLUSION LIST (HIKARI ruling, 2026-07-30).
# The cheap fix is `if 'scope-bound' in path: continue` — six names hardcoded as "these don't
# count." That would bake "these rules enforce invisibly and that is fine" into the instrument
# built to find rules that enforce invisibly. It re-creates this scope's core defect inside its
# own fix. enforce.sh is a dispatcher; it has a source and a vocabulary; it gets exactly the
# same treatment as the other three (Q2: derive from each dispatcher's own source, per tier).
#
# WHAT REACHABILITY MEANS ON THIS TIER — read off enforce.sh, not assumed:
#   enforce.sh:145  for rule_file in "$SCOPE_BOUND_DIR"/*.local.md   <- glob, NOT hookify.*
#   enforce.sh:149  event: <comma-separated list>, matched against the events enforce.sh
#                   actually calls dispatch_scope_bound_event with. An event no call site
#                   passes is never dispatched — the rule is inert.
#   enforce.sh:172  check: <basename> override, else check_<event_underscored>.sh
#   enforce.sh:177  [[ ! -x "$check_script" ]] -> log ::missing-check and SKIP. Not executable
#                   is the same as not there: the gate silently stops gating.
#
# AND WHAT IT DOES NOT MEAN: enforce.sh NEVER READS `enabled:` (grep -c: zero occurrences).
# None of these 6 files declares one. Judging them by Parts 1-5's vocabulary would fail all six
# live rules on `enabled` and `event` — six false positives on rules that are provably firing.
# Applying one tier's contract to another tier's rules is the exact error that put three false
# positives in Discovery Doc v1.0. Part 6 therefore checks these files against enforce.sh's
# rules and nothing else.
print("\n=== Part 6: scope-bound tier (enforce.sh — the fourth dispatcher) ===")

_ENFORCE = os.path.join(RULES_DIR, "enforce.sh")
SCOPE_BOUND_DIR = os.environ.get("HOOKIFY_SCOPE_BOUND_DIR") or os.path.join(
    RULES_DIR, "scope-bound")

if not os.path.exists(_ENFORCE):
    fail(f"cannot derive the scope-bound vocabulary — {_ENFORCE} not found. Six live rules "
         f"with real fires on record would go UNCHECKED and this file would still print a "
         f"census. 'Cannot check' is not 'nothing wrong'.")
elif not os.path.isdir(SCOPE_BOUND_DIR):
    print(f"  {SCOPE_BOUND_DIR} does not exist — no scope-bound rules for this checkout. "
          f"Reported, not failed (a worktree may legitimately not carry it).")
else:
    _esrc = open(_ENFORCE, encoding="utf-8", errors="replace").read()

    # (6a) the live event vocabulary = the events enforce.sh actually dispatches.
    DISPATCHED = sorted(set(re.findall(
        r"dispatch_scope_bound_event\s+[\"']([A-Za-z][A-Za-z0-9_-]*)[\"']", _esrc)))
    # (6b) the glob enforce.sh walks, and the default check-script name template.
    _gm = re.search(r"for\s+rule_file\s+in\s+\"\$SCOPE_BOUND_DIR\"/(\S+);", _esrc)
    SB_GLOB = _gm.group(1) if _gm else None
    _cm = re.search(r"default_check_basename=\"([^\"]+)\"", _esrc)
    CHECK_TMPL = _cm.group(1) if _cm else None

    if not DISPATCHED:
        # Same refusal as Part 5 branch 1: an empty vocabulary makes every rule look valid.
        fail("derived ZERO dispatched events from enforce.sh — refusing to check against "
             "nothing. Every scope-bound rule would read as reachable. The derivation no "
             "longer matches enforce.sh's call sites; fix the derivation, not the verdict.")
    elif not SB_GLOB or not CHECK_TMPL:
        fail(f"could not derive enforce.sh's rule glob ({SB_GLOB!r}) or check-script template "
             f"({CHECK_TMPL!r}) — the scope-bound population and its check resolution would be "
             f"guessed rather than read. Refusing.")
    else:
        print(f"  dispatcher: {_ENFORCE}")
        print(f"  rule dir:   {SCOPE_BOUND_DIR}")
        print(f"  glob:       {SB_GLOB}   (note: NOT {LOADER_GLOB} — a different population)")
        print(f"  events dispatched live: {DISPATCHED}")
        print(f"  check resolution: `check:` override, else {CHECK_TMPL}")
        print(f"  note: enforce.sh never reads `enabled:` — these rules are NOT judged by "
              f"Parts 1-5's vocabulary, and must not be.")

        sb_files = sorted(glob.glob(os.path.join(SCOPE_BOUND_DIR, SB_GLOB)))
        if not sb_files:
            fail(f"no files matching {SB_GLOB} in {SCOPE_BOUND_DIR} — refusing to report a "
                 f"clean scope-bound tier over an EMPTY population (Part 4 branch 2, one "
                 f"dispatcher over).")

        sb_clean, sb_broken = [], []
        for rf in sb_files:
            base = os.path.basename(rf)
            fm = frontmatter(rf)
            rule_id = base[:-len(".local.md")] if base.endswith(".local.md") else base
            problems = []

            m = re.search(r"^event:\s*(.*)$", fm, re.M)
            declared = [e.strip() for e in (m.group(1) if m else "").split(",") if e.strip()]
            if not declared:
                problems.append("declares no `event:` -> enforce.sh:150 `continue`s past it; "
                                "the rule is never dispatched by anything")
            else:
                dead = [e for e in declared if e not in DISPATCHED]
                if dead and len(dead) == len(declared):
                    problems.append(
                        f"every declared event {dead} is dispatched by NO call site in "
                        f"enforce.sh (live events: {DISPATCHED}) -> this rule can never run")
                elif dead:
                    problems.append(
                        f"declared event(s) {dead} are dispatched by no call site (live: "
                        f"{DISPATCHED}) — the rule still runs on its other events, but those "
                        f"entries are dead weight and read as coverage")

            cm = re.search(r"^check:\s*(.*)$", fm, re.M)
            if cm and cm.group(1).strip():
                check_basename = cm.group(1).strip()
                origin = "`check:` override"
            elif declared:
                check_basename = CHECK_TMPL.replace(
                    "${underscored}", declared[0].replace("-", "_"))
                origin = f"default template {CHECK_TMPL}"
            else:
                check_basename, origin = None, None

            if check_basename:
                cpath = os.path.join(SCOPE_BOUND_DIR, check_basename)
                if not os.path.exists(cpath):
                    problems.append(
                        f"its check script ({origin}) does not exist: {check_basename}. "
                        f"enforce.sh:177 logs `{rule_id}::missing-check` and SKIPS — the rule "
                        f"reads as a BLOCK gate and blocks nothing")
                elif not os.access(cpath, os.X_OK):
                    problems.append(
                        f"its check script {check_basename} exists but is NOT EXECUTABLE. "
                        f"enforce.sh:177 tests `-x`, so this fails exactly like a missing "
                        f"file — silently, via `continue`. A chmod is the whole difference "
                        f"between a live gate and a decoration")

            if problems:
                sb_broken.append(base)
                for p in problems:
                    fail(f"{base} [scope-bound tier]: {p}")
            else:
                sb_clean.append(base)
                ok(f"{base}: dispatched on {declared}, check {check_basename} present + "
                   f"executable")

        print(f"\n  -- scope-bound census --")
        print(f"  reachable-clean   {len(sb_clean):>3}")
        print(f"  defective         {len(sb_broken):>3}")
        print(f"  scope-bound total {len(sb_files):>3}")
        hookify_total = len(glob.glob(os.path.join(RULES_DIR, LOADER_GLOB)))
        print(f"\n  ENFORCED CORPUS = {hookify_total} (hookify tiers) + {len(sb_files)} "
              f"(scope-bound) = {hookify_total + len(sb_files)} rule files.")
        print(f"  The '{hookify_total} rules' figure quoted throughout this scope counts one "
              f"dispatcher's population and omits enforce.sh's own.")


# ── verdict ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
if failures:
    print(f"FAILED — {len(failures)} problem(s), {passes} passed\n")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print(f"PASSED — {passes} checks. Every rule in {RULES_DIR} is LOADABLE by its dispatcher "
      f"and its pattern compiles cleanly in the live engine.")
print("         This does NOT prove any rule matches its intended triggers — only the "
      "behavioural cases in Part 2 do that, and only for the rules that have them.")
sys.exit(0)
