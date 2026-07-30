#!/usr/bin/env python3
"""rule-liveness-part5-mutation.test.py — proves Part 5 DISCRIMINATES, per tier, both ways.

TRK-HOOK-101 (ronin, 2026-07-30). Gate G2 of the Hookify Overhaul contract.

WHY THIS EXISTS
---------------
Part 5 of rule-liveness.test.py reports that 5 of 106 rules cannot fire. That claim is worth
exactly nothing until someone has watched the check FAIL on a rule that is broken and STAY
QUIET on a rule that is not — because a check that returns "clean" for every input also
returns "clean" for a clean corpus, and reads identically.

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

RUN
---
    python3 hookify/rule-liveness-part5-mutation.test.py

Exit 0 = Part 5 discriminates correctly on all six. Exit 1 = it does not, and no verdict it
produces about the real corpus should be trusted until it does.

NOTE ON EXIT CODES: this harness asserts on Part 5's OUTPUT LINES, not on the instrument's
exit code. Run against a synthetic directory, Parts 2-4 legitimately fail (the rules they name
by hand are not there), so the process always exits 1. Reading the exit code here would prove
nothing about Part 5. Stated rather than left for the next reader to rediscover.
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

    print("\n" + "=" * 70)
    if bad:
        print(f"MUTATION TEST FAILED — {bad} case(s) wrong. Part 5 does not discriminate; "
              f"treat its verdicts on the real corpus as unproven.")
        return 1
    print("MUTATION TEST PASSED — Part 5 fails broken rules and stays quiet on sound ones, "
          "and the SAME operator gets opposite verdicts on the file and stop tiers (G2).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
