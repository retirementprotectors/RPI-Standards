#!/usr/bin/env python3
"""run-all.py — run every reviewer-authored adversarial corpus against a hookify rule.

MZ-ADVERSARIAL-CORPUS-001 (megazord, 2026-07-26).

WHY A RUNNER RATHER THAN JUST THE CORPORA
-----------------------------------------
The corpora in this directory are HIKARI's, committed byte-identical (see README.md). Two of
them exit 1 on a miss. `round4b-nesting-matrix.py` has NO sys.exit at all — it prints its
failures and returns 0 regardless. A committed test that cannot fail loudly is worse than no
test: the next reader sees green and stops looking. That is the exact defect this whole arc
was about, so the runner refuses to inherit it.

THIS RUNNER DOES NOT TRUST EXIT CODES. It reads each corpus's OUTPUT and treats any line
carrying the failure marker as a failure, then ANDs that with the exit code. A corpus that
prints failures and exits 0 fails here. A corpus that exits 1 silently also fails here.

  (This is not hypothetical. While wiring this up I read a corpus's exit status through
   `echo "$(basename $f): $?"` — the command substitution runs first and clobbers `$?`, so I
   read basename's status, not python's, and briefly concluded all three corpora were
   non-discriminating. Capture the status into a variable BEFORE any other command runs on
   that line. Same class as `cmd | tail` replacing `$?`.)

PER-CORPUS, NEVER A TOTAL
-------------------------
Results are reported per corpus. A summed pass-count across corpora would hide a corpus that
regressed to zero coverage while another grew — a rising total concealing a partial wipe.

USAGE
    python3 hookify/adversarial/run-all.py <path-to-rule.md>
    python3 hookify/adversarial/run-all.py <path-to-rule.md> --expect-fail

`--expect-fail` inverts the verdict: it asserts the corpora DO fail against the given rule.
Use it to prove a corpus can still discriminate — a corpus that passes against both a broken
and a fixed rule proves nothing, and that check is only meaningful if you actually run it.

Exit 0 = every corpus behaved as expected. Exit 1 = at least one did not.
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL_MARKER = "!!"          # what the corpora print on a miss
SCORE_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s+pass")


def run_corpus(path, rule):
    """Return (ok, passed, total, printed_failures, exit_code)."""
    proc = subprocess.run([sys.executable, path, rule],
                          capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    printed = sum(1 for line in out.splitlines() if FAIL_MARKER in line)
    m = SCORE_RE.search(out)
    passed, total = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    # clean == no printed failures AND exit 0 AND (if a score was printed) all cases passed
    clean = (printed == 0 and proc.returncode == 0
             and (passed is None or passed == total))
    return clean, passed, total, printed, proc.returncode


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    rule = sys.argv[1]
    expect_fail = "--expect-fail" in sys.argv[2:]
    if not os.path.isfile(rule):
        print(f"  rule file not found: {rule}")
        return 2

    corpora = sorted(glob.glob(os.path.join(HERE, "round*.py")))
    if not corpora:
        print(f"  no corpora found in {HERE}")
        return 2

    mode = "EXPECT FAIL" if expect_fail else "EXPECT CLEAN"
    print(f"\n=== adversarial corpora vs {os.path.basename(rule)}  [{mode}] ===")
    bad = []
    for c in corpora:
        clean, passed, total, printed, rc = run_corpus(c, rule)
        score = f"{passed}/{total}" if passed is not None else "n/a"
        verdict = "clean" if clean else "FAILS"
        agree = (not clean) if expect_fail else clean
        flag = "ok " if agree else "XX "
        print(f"  {flag} {os.path.basename(c):<34} {score:>7}  "
              f"printed_failures={printed}  exit={rc}  -> {verdict}")
        if not agree:
            bad.append(os.path.basename(c))

    print("\n" + "=" * 72)
    if bad:
        want = "fail" if expect_fail else "be clean"
        print(f"FAILED — {len(bad)} corpus/corpora did not {want}: {', '.join(bad)}")
        return 1
    if expect_fail:
        print(f"PASSED — all {len(corpora)} corpora still DISCRIMINATE against this rule.")
        print("         Their green against the fixed rule therefore carries information.")
    else:
        print(f"PASSED — all {len(corpora)} corpora clean against this rule.")
        print("         Verify discrimination separately with --expect-fail against a known-")
        print("         broken revision; a corpus that passes on both proves nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
