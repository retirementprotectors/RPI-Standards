#!/usr/bin/env python3
"""rule-liveness-reachability-mutation.test.py — proves Parts 5 and 6 DISCRIMINATE, per tier,
in both directions.

TRK-HOOK-101 (ronin, 2026-07-30). Gate G2 of the Hookify Overhaul contract.

WHY THIS EXISTS
---------------
Part 5 of rule-liveness.test.py reports that 5 of 106 hookify rules cannot fire, and Part 6
reports that all 6 scope-bound rules can. Both claims are worth exactly nothing until someone
has watched the checks FAIL on a rule that is broken and STAY QUIET on a rule that is not —
because a check that returns "clean" for every input also returns "clean" for a clean corpus,
and reads identically.

That is not hypothetical here. Discovery Doc v1.0 shipped a check that flagged four rules for
using `regex_not_match`. Three were false positives: they are `event: stop`, and the stop
dispatcher implements that operator. The check had never been run against a rule it was
supposed to stay quiet on, so nothing caught it. v1.1 corrected the count from 4 to 1.

So the load-bearing case in this file is CASE 2: the SAME operator, on a DIFFERENT tier, must
produce the OPPOSITE verdict. Testing only the failing direction is how v1.0 happened.

  case 1  file tier + regex_not_match ......... MUST FAIL   (op absent from rule_engine.py)
  case 2  stop tier + regex_not_match ......... MUST BE QUIET (op present in the stop dispatcher)
          ^^ same operator, opposite verdict — the discrimination proof
  case 3  file tier + field: path ............. MUST FAIL   (probe: engine yields None)
  case 4  file tier + field: file_path ........ MUST BE QUIET (real field, must not false-fire)
  case 5  prompt tier + only a file-tier field  MUST FAIL   (dispatcher drops it -> zero usable)
  case 6  stop tier + implementation: <script
          that does not exist> ................ MUST FAIL   (declared coverage pointing at nothing)

Part 6's suite (SB_CASES, further down) applies the same standard to the scope-bound tier.

RUN
---
    python3 hookify/rule-liveness-reachability-mutation.test.py

Exit 0 = Parts 5 and 6 discriminate correctly on all 11 cases. Exit 1 = they do not, and no
verdict either produces about the real corpus should be trusted until they do.

NOTE ON EXIT CODES: this harness asserts on the instrument's OUTPUT LINES, not on its exit
code — run against a synthetic directory, Parts 1-4 legitimately fail on rules they name by
hand, so the process always exits 1. The exit code IS captured, directly off subprocess.run
and never through a shell pipeline (`cmd | tail` then `$?` reports tail's status, not the
command's — two seats produced a false red from that shape an hour apart on 2026-07-30). It is
reported alongside a completion proof rather than asserted on: see _completed_or_none, which
refuses to read any verdict from a run that crashed or stopped short, because an empty flag
set makes every MUST-BE-QUIET case pass for the wrong reason.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUMENT = os.path.join(HERE, "rule-liveness.test.py")


def _completed_or_none(proc, part_header):
    """Return the instrument's combined output, or None if this run cannot be trusted.

    THE FALSE-GREEN THIS CLOSES, which is subtle and was live in the first cut:
    every assertion below is "did the instrument FLAG this rule name?". If the instrument
    dies partway through — an unhandled exception, a missing dispatcher, a timeout — the
    flagged set comes back EMPTY. Every `MUST FAIL` case then correctly fails, but every
    `MUST BE QUIET` case PASSES, because nothing was flagged. A crashed run reports a
    partial green, and the quiet direction is exactly the direction that catches false
    positives. So the run's completion must be proven before any verdict is read off it.

    EXIT CODE HANDLING (HIKARI ruling + parent SHINOB1's ask, 2026-07-30): `proc.returncode`
    is read DIRECTLY off subprocess.run. It is never obtained through a shell pipeline —
    `cmd | tail` then `$?` yields tail's status, not the command's, and two seats produced a
    false red from exactly that shape an hour apart on the same evening. A false red in the
    instrument built to eliminate false reds is not an irony worth shipping.
    """
    out = (proc.stdout or "") + (proc.stderr or "")
    if "Traceback (most recent call last)" in out:
        print(f"FAIL: the instrument raised an unhandled exception (exit {proc.returncode}). "
              f"An empty flag set would make every MUST-BE-QUIET case pass for the wrong "
              f"reason, so no verdict is read from this run.")
        print(out[-2000:])
        return None
    if part_header not in out:
        print(f"FAIL: {part_header} did not run at all (exit {proc.returncode}) — cannot "
              f"assert on its verdicts.")
        print(out[-2000:])
        return None
    if "=" * 70 not in out:
        print(f"FAIL: the instrument did not reach its verdict banner (exit "
              f"{proc.returncode}) — it stopped partway, so the flag set is incomplete and "
              f"the quiet direction proves nothing.")
        print(out[-2000:])
        return None
    # Exit 1 is EXPECTED here: run against a synthetic directory, Parts 1-4 legitimately
    # fail on rules they name by hand. What must not happen is a crash, which the checks
    # above catch. Reported so the reader sees a captured code rather than an assumed one.
    print(f"  instrument completed, exit={proc.returncode} (captured from subprocess.run, "
          f"not through a pipe; exit 1 is expected on a synthetic corpus)")
    return out

# (filename_stem, frontmatter, must_fail, why)
CASES = [
    ("zz-mutant-file-badop", """name: zz-mutant-file-badop
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_not_match
    pattern: docs/
""", True, "file tier does not implement regex_not_match"),

    ("zz-mutant-stop-sameop", """name: zz-mutant-stop-sameop
enabled: true
event: stop
action: warn
conditions:
  - field: last_assistant_message
    operator: regex_not_match
    pattern: receipt
""", False, "SAME operator, stop tier — the dispatcher implements it, must stay quiet"),

    ("zz-mutant-file-badfield", """name: zz-mutant-file-badfield
enabled: true
event: file
action: warn
conditions:
  - field: path
    operator: regex_match
    pattern: services/
""", True, "no engine branch yields a value for 'path' under any tool"),

    ("zz-mutant-file-goodfield", """name: zz-mutant-file-goodfield
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: services/
""", False, "real field + real operator — must not false-fire"),

    ("zz-mutant-prompt-wrongfield", """name: zz-mutant-prompt-wrongfield
enabled: true
event: prompt
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: anything
""", True, "prompt dispatcher filters to its own fields -> zero usable conditions"),

    ("zz-mutant-fake-detector", """name: zz-mutant-fake-detector
enabled: true
event: stop
action: warn
implementation: stop-event shell hook via zz_no_such_detector_ronin.sh
""", True, "declares an external detector that does not exist"),
]


# ── Part 6 (scope-bound / enforce.sh tier) ──────────────────────────────────
# Part 6 must fail on rules enforce.sh can never run, and stay QUIET on the six live ones.
# The quiet direction is load-bearing here for a specific reason: none of the real scope-bound
# rules declares `enabled:`, and their events are not hookify events. Judged by Parts 1-5's
# vocabulary all six would fail — six false positives on rules that are provably firing in
# production. Case sb-good is the proof that Part 6 uses enforce.sh's contract, not hookify's.
#
#   sb-good ............ event enforce.sh dispatches + executable check .. MUST BE QUIET
#   sb-dead-event ...... event no call site passes ....................... MUST FAIL
#   sb-missing-check ... `check:` names a script that is not there ........ MUST FAIL
#   sb-nonexec-check ... check script EXISTS but is not executable ........ MUST FAIL
#                        (enforce.sh:177 tests -x; a chmod is the whole difference
#                         between a live gate and a decoration)
#   sb-no-event ........ no `event:` key at all .......................... MUST FAIL
SB_CASES = [
    ("sb-good", "event: pre-write\ncheck: check_ronin_probe.sh\n", False,
     "dispatched event + executable check — must not false-fire"),
    ("sb-dead-event", "event: pre-nothing-dispatches-this\ncheck: check_ronin_probe.sh\n", True,
     "no dispatch_scope_bound_event call site passes this event"),
    ("sb-missing-check", "event: pre-write\ncheck: check_ronin_absent.sh\n", True,
     "check script does not exist -> ::missing-check + skip"),
    ("sb-nonexec-check", "event: pre-write\ncheck: check_ronin_nonexec.sh\n", True,
     "check script exists but is not executable -> same silent skip"),
    ("sb-no-event", "check: check_ronin_probe.sh\n", True,
     "no event: key -> enforce.sh continues past it"),
]


# ── Part 2b (hit-Enter / prompt tier behavioural) ───────────────────────────
# TRK-HOOK-102 widened Part 2b from 1 rule to all 12. Those new assertions get the same
# treatment as every other one in this file: watched failing before they are believed.
#
# The quiet case (p2-clean) is load-bearing again. Part 2b now runs FIVE neutral controls
# against every rule and derives a positive probe from each rule's own pattern — plenty of
# surface to false-fire on. A suite that only proves the failing direction would not notice
# Part 2b calling every healthy rule broken.
#
#   p2-clean ....... unique trigger, matches no neutral control ...... MUST BE QUIET
#   p2-dropped ..... one condition on a field the dispatcher drops ... MUST FAIL
#   p2-allbad ...... every condition dropped -> rule skipped .......... MUST FAIL
#   p2-misfire ..... pattern claims an ordinary working request ....... MUST FAIL
P2_CASES = [
    ("p2-clean", "zzq-unique-trigger-alpha", False,
     "unique trigger, quiet on all neutral controls — must not false-fire"),
    ("p2-misfire", "status of the deploy", True,
     "claims an ordinary request — a live misfire on real traffic"),
]


def run_part2b():
    """Exercise the widened prompt-tier suite against synthetic rules."""
    with tempfile.TemporaryDirectory(prefix="ronin-mutation-p2-") as tmp:
        for stem, pat, _mf, _why in P2_CASES:
            with open(os.path.join(tmp, f"hookify.{stem}.local.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(f"---\nname: {stem}\nenabled: true\nevent: prompt\naction: warn\n"
                         f"conditions:\n  - field: user_prompt\n    operator: regex_match\n"
                         f"    pattern: {pat}\n---\n\nSynthetic prompt rule.\n")
        # one condition dropped (file_path is not in the dispatcher's accepted fields),
        # one kept -> the AND silently loses a term and the rule gets more permissive
        with open(os.path.join(tmp, "hookify.p2-dropped.local.md"), "w",
                  encoding="utf-8") as fh:
            fh.write("---\nname: p2-dropped\nenabled: true\nevent: prompt\naction: warn\n"
                     "conditions:\n  - field: file_path\n    operator: regex_match\n"
                     "    pattern: services/\n  - field: user_prompt\n"
                     "    operator: regex_match\n    pattern: zzq-unique-trigger-beta\n"
                     "---\n\nSynthetic prompt rule.\n")
        # every condition dropped -> `if not conds: continue` skips the rule outright
        with open(os.path.join(tmp, "hookify.p2-allbad.local.md"), "w",
                  encoding="utf-8") as fh:
            fh.write("---\nname: p2-allbad\nenabled: true\nevent: prompt\naction: warn\n"
                     "conditions:\n  - field: file_path\n    operator: regex_match\n"
                     "    pattern: services/\n---\n\nSynthetic prompt rule.\n")

        expected = [c[0] for c in P2_CASES] + ["p2-dropped", "p2-allbad"]
        written = sorted(f for f in os.listdir(tmp) if f.endswith(".local.md"))
        if len(written) != len(expected):
            print(f"FAIL: prompt-tier mutation did not land — "
                  f"{len(written)}/{len(expected)}")
            return 1
        print(f"prompt-tier mutation landed: {len(written)} synthetic rule(s)")

        proc = subprocess.run([sys.executable, INSTRUMENT, tmp],
                              capture_output=True, text=True, timeout=300)
        out = _completed_or_none(proc, "-- ALL event: prompt rules")

    if out is None:
        return 1
    # Scope to Part 2b's own section: Part 5 also evaluates these files and would flag the
    # dropped-field rules for its own reasons. Counting its verdicts here would prove Part 5
    # works twice and Part 2b not at all.
    seg = out.split("-- ALL event: prompt rules", 1)[1].split("=== Part 3", 1)[0]
    flagged = set()
    for line in seg.splitlines():
        m = re.search(r"FAIL\s+hookify\.(p2-[a-z-]+)\.local\.md", line)
        if m:
            flagged.add(m.group(1))

    print(f"\nPart 2b flagged: {sorted(flagged) or 'nothing'}\n")
    bad = 0
    checks = list(P2_CASES) + [
        ("p2-dropped", None, True, "one condition dropped -> AND silently widened"),
        ("p2-allbad", None, True, "all conditions dropped -> dispatcher skips the rule"),
    ]
    for stem, _pat, must_fail, why in checks:
        hit = stem in flagged
        if hit == must_fail:
            print(f"  pass  {stem}: {'flagged' if must_fail else 'quiet'} as required — {why}")
        else:
            bad += 1
            print(f"  FAIL  {stem}: expected {'FLAG' if must_fail else 'QUIET'}, "
                  f"got {'FLAG' if hit else 'QUIET'} — {why}")
    return 1 if bad else 0


def run_part6():
    """Build a synthetic scope-bound tier next to a real copy of enforce.sh, and assert."""
    real_enforce = os.path.join(HERE, "enforce.sh")
    if not os.path.exists(real_enforce):
        print("FAIL: enforce.sh not found — cannot exercise Part 6's derivation.")
        return 1

    with tempfile.TemporaryDirectory(prefix="ronin-mutation-sb-") as tmp:
        # Part 6 derives its vocabulary from enforce.sh, so the harness uses the REAL one.
        # A stub would prove the harness agrees with itself and nothing else.
        with open(real_enforce, encoding="utf-8", errors="replace") as src:
            with open(os.path.join(tmp, "enforce.sh"), "w", encoding="utf-8") as dst:
                dst.write(src.read())
        sb = os.path.join(tmp, "scope-bound")
        os.makedirs(sb)

        probe = os.path.join(sb, "check_ronin_probe.sh")
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\nexit 0\n")
        os.chmod(probe, 0o755)
        nonexec = os.path.join(sb, "check_ronin_nonexec.sh")
        with open(nonexec, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\nexit 0\n")
        os.chmod(nonexec, 0o644)          # exists, NOT executable — the whole point

        for stem, fm, _mf, _why in SB_CASES:
            with open(os.path.join(sb, f"{stem}.local.md"), "w", encoding="utf-8") as fh:
                fh.write(f"---\nname: {stem}\n{fm}---\n\nSynthetic scope-bound rule.\n")

        # prove the mutation landed, and that the non-executable file really is non-executable
        if os.access(nonexec, os.X_OK):
            print("FAIL: harness could not create a non-executable check script — the "
                  "sb-nonexec-check verdict would be meaningless.")
            return 1
        written = sorted(f for f in os.listdir(sb) if f.endswith(".local.md"))
        if len(written) != len(SB_CASES):
            print(f"FAIL: scope-bound mutation did not land — {len(written)}/{len(SB_CASES)}")
            return 1
        print(f"scope-bound mutation landed: {len(written)} rule(s), 1 non-executable check")

        proc = subprocess.run([sys.executable, INSTRUMENT, tmp],
                              capture_output=True, text=True, timeout=300)
        out = _completed_or_none(proc, "=== Part 6")

    if out is None:
        return 1
    part6 = out.split("=== Part 6", 1)[1]
    flagged = set()
    for line in part6.splitlines():
        m = re.search(r"FAIL\s+(sb-[a-z-]+)\.local\.md", line)
        if m:
            flagged.add(m.group(1))

    print(f"\nPart 6 flagged: {sorted(flagged) or 'nothing'}\n")
    bad = 0
    for stem, _fm, must_fail, why in SB_CASES:
        hit = stem in flagged
        if hit == must_fail:
            print(f"  pass  {stem}: {'flagged' if must_fail else 'quiet'} as required — {why}")
        else:
            bad += 1
            print(f"  FAIL  {stem}: expected {'FLAG' if must_fail else 'QUIET'}, "
                  f"got {'FLAG' if hit else 'QUIET'} — {why}")
    return 1 if bad else 0


TOTAL_RE = re.compile(
    r"ENFORCED CORPUS\s*=\s*(\d+)\s*\(hookify tiers\)\s*\+\s*(\d+)\s*\(scope-bound\)\s*"
    r"=\s*(\d+)\s*rule files")


def _corpus_totals(tmp, label):
    """Run the instrument over `tmp` and read the totals IT derived. None if untrustworthy."""
    proc = subprocess.run([sys.executable, INSTRUMENT, tmp],
                          capture_output=True, text=True, timeout=300)
    out = _completed_or_none(proc, "=== Part 6")
    if out is None:
        return None
    m = TOTAL_RE.search(out)
    if not m:
        print(f"FAIL [{label}]: the instrument printed no ENFORCED CORPUS line — there is no "
              f"derived denominator to check, which is itself the G1 failure.")
        return None
    hookify, sb, total = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if hookify + sb != total:
        print(f"FAIL [{label}]: the instrument's own arithmetic disagrees — "
              f"{hookify} + {sb} != {total}.")
        return None
    print(f"  {label}: hookify={hookify}  scope-bound={sb}  total={total}")
    return hookify, sb, total


def run_g1():
    """GATE G1 — THE DENOMINATOR IS DERIVED FROM DISK, NOT ASSERTED.

    G1's acceptance is not "the total is 112". It is that the total MOVES when the corpus moves,
    with zero code edits, in BOTH families. A hardcoded literal passes a spot-check of the number
    and fails this.

    THIS EXISTED ONLY AS A HAND-RUN UNTIL NOW. G1 was proved by adding one file per family to the
    live corpus and watching 112 -> 114 -> 112 (RONIN, 2026-07-30). That proof was real and it
    rotted the moment it finished: nothing re-ran it, and a gate whose evidence is a paragraph in
    a report is a gate nobody will notice breaking. HIKARI approved folding it in here.

    Both directions, because a total that only ever grows is also broken: add a file and it must
    rise, remove it and it must fall back. The removal arm is what catches a cache, a memoised
    glob, or a denominator read once at import.
    """
    print("\n--- Gate G1 (denominator derived from disk, both families, both directions) ---")
    real_enforce = os.path.join(HERE, "enforce.sh")
    if not os.path.exists(real_enforce):
        print("FAIL: enforce.sh not found — Part 6's half of the denominator cannot be derived.")
        return 1

    with tempfile.TemporaryDirectory(prefix="ronin-mutation-g1-") as tmp:
        with open(real_enforce, encoding="utf-8", errors="replace") as src:
            with open(os.path.join(tmp, "enforce.sh"), "w", encoding="utf-8") as dst:
                dst.write(src.read())
        sb = os.path.join(tmp, "scope-bound")
        os.makedirs(sb)

        def write_rule(stem):
            p = os.path.join(tmp, f"hookify.{stem}.local.md")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(f"---\nname: {stem}\nenabled: true\nevent: file\naction: warn\n"
                         f"conditions:\n  - field: file_path\n    operator: contains\n"
                         f"    value: {stem}-sentinel\n---\n\nSynthetic G1 rule.\n")
            return p

        def write_sb(stem):
            p = os.path.join(sb, f"{stem}.local.md")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(f"---\nname: {stem}\nevent: pre-write\n"
                         f"check: check_{stem.replace('-', '_')}.sh\n---\n\nSynthetic G1 rule.\n")
            return p

        for i in range(3):
            write_rule(f"zz-g1-base-{i}")
        for i in range(2):
            write_sb(f"zz-g1-sb-base-{i}")

        base = _corpus_totals(tmp, "baseline")
        if base is None:
            return 1
        if base != (3, 2, 5):
            print(f"FAIL: baseline should be 3 + 2 = 5 by construction, got {base}. The "
                  f"instrument is not counting the directory it was handed.")
            return 1

        added = [write_rule("zz-g1-added"), write_sb("zz-g1-sb-added")]
        # Prove the mutation landed BEFORE reading the verdict — a write that silently failed
        # returns the number already expected, which is the one nobody re-examines.
        landed = [p for p in added if os.path.exists(p)]
        if len(landed) != 2:
            print(f"FAIL: G1 mutation did not land ({len(landed)}/2 files) — the totals below "
                  f"would be meaningless.")
            return 1
        print(f"  mutation landed: {sum(os.path.getsize(p) for p in landed)} bytes across "
              f"2 files, one per family")

        grown = _corpus_totals(tmp, "after +1 per family")
        if grown is None:
            return 1

        for p in added:
            os.unlink(p)
        shrunk = _corpus_totals(tmp, "after removal")
        if shrunk is None:
            return 1

    bad = 0
    if grown != (4, 3, 7):
        print(f"  FAIL  the total did not follow the corpus UP: expected 4 + 3 = 7, got {grown}. "
              f"A denominator that ignores a new file is asserted, not derived.")
        bad += 1
    else:
        print("  pass  total rose with the corpus, in BOTH families (3+2=5 -> 4+3=7)")
    if shrunk != base:
        print(f"  FAIL  the total did not follow the corpus DOWN: expected {base}, got {shrunk}. "
              f"A total that only grows is reading a cache, not the disk.")
        bad += 1
    else:
        print("  pass  total fell back when the files were removed — the removal arm is what "
              "catches a memoised glob or an import-time read")
    return 1 if bad else 0


def main():
    if not os.path.exists(INSTRUMENT):
        print(f"FAIL: instrument not found at {INSTRUMENT}")
        return 1

    with tempfile.TemporaryDirectory(prefix="ronin-mutation-") as tmp:
        for stem, fm, _must_fail, _why in CASES:
            with open(os.path.join(tmp, f"hookify.{stem}.local.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(f"---\n{fm}---\n\nSynthetic rule. TRK-HOOK-101 mutation harness.\n")

        # PROVE THE MUTATION LANDED before trusting any verdict about it. A harness that
        # writes files and never confirms they exist can report a clean pass over an empty
        # directory — the same "green over an empty population" defect Part 4 refuses.
        written = sorted(f for f in os.listdir(tmp) if f.endswith(".local.md"))
        if len(written) != len(CASES):
            print(f"FAIL: mutation did not land — wrote {len(CASES)} rule(s), "
                  f"found {len(written)} in {tmp}. Verdicts below would be meaningless.")
            return 1
        print(f"mutation landed: {len(written)} synthetic rule(s) in {tmp}")

        proc = subprocess.run([sys.executable, INSTRUMENT, tmp],
                              capture_output=True, text=True, timeout=300)
        out = _completed_or_none(proc, "=== Part 5")

    if out is None:
        return 1

    # Only Part 5's own FAIL lines are in scope. Parts 1-4 fail by construction here.
    part5 = out.split("=== Part 5", 1)[1]
    flagged = set()
    for line in part5.splitlines():
        m = re.search(r"FAIL\s+hookify\.(zz-mutant-[a-z-]+)\.local\.md", line)
        if m:
            flagged.add(m.group(1))

    print(f"\nPart 5 flagged: {sorted(flagged) or 'nothing'}\n")

    bad = 0
    for stem, _fm, must_fail, why in CASES:
        hit = stem in flagged
        if hit == must_fail:
            print(f"  pass  {stem}: {'flagged' if must_fail else 'quiet'} as required — {why}")
        else:
            bad += 1
            print(f"  FAIL  {stem}: expected {'FLAG' if must_fail else 'QUIET'}, "
                  f"got {'FLAG' if hit else 'QUIET'} — {why}")

    print("\n--- Part 2b (hit-Enter / prompt tier behavioural) ---")
    bad += run_part2b()

    print("\n--- Part 6 (scope-bound / enforce.sh tier) ---")
    bad += run_part6()

    bad += run_g1()

    print("\n" + "=" * 70)
    if bad:
        print(f"MUTATION TEST FAILED — {bad} case(s) wrong. The instrument does not "
              f"discriminate; treat its verdicts on the real corpus as unproven.")
        return 1
    print("MUTATION TEST PASSED — Parts 5 and 6 fail broken rules and stay quiet on sound "
          "ones. The SAME operator gets opposite verdicts on the file and stop tiers, "
          "scope-bound rules are judged by enforce.sh's contract rather than hookify's (G2), "
          "and the corpus denominator follows the disk in both families and both directions "
          "(G1).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
