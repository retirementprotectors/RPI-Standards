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
code. Run against a synthetic directory, Parts 2-4 legitimately fail (the rules they name by
hand are not there), so the process always exits 1. Reading the exit code here would prove
nothing. Stated rather than left for the next reader to rediscover.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUMENT = os.path.join(HERE, "rule-liveness.test.py")

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
        out = proc.stdout + proc.stderr

    if "=== Part 6" not in out:
        print("FAIL: Part 6 did not run — cannot assert on its verdicts.")
        print(out[-3000:])
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
        out = proc.stdout + proc.stderr

    if "=== Part 5" not in out:
        print("FAIL: Part 5 did not run at all — cannot assert on its verdicts.")
        print(out[-3000:])
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

    print("\n--- Part 6 (scope-bound / enforce.sh tier) ---")
    bad += run_part6()

    print("\n" + "=" * 70)
    if bad:
        print(f"MUTATION TEST FAILED — {bad} case(s) wrong. The instrument does not "
              f"discriminate; treat its verdicts on the real corpus as unproven.")
        return 1
    print("MUTATION TEST PASSED — Parts 5 and 6 fail broken rules and stay quiet on sound "
          "ones. The SAME operator gets opposite verdicts on the file and stop tiers, and "
          "scope-bound rules are judged by enforce.sh's contract rather than hookify's (G2).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
