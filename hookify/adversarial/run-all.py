#!/usr/bin/env python3
"""run-all.py — run every reviewer-authored adversarial corpus against a hookify rule.

MZ-ADVERSARIAL-CORPUS-001 (megazord, 2026-07-26).

WHY A RUNNER RATHER THAN JUST THE CORPORA
-----------------------------------------
The corpora in this directory are HIKARI's, committed byte-identical (see README.md). When
this runner was built, two of them exited 1 on a miss and `round4b-nesting-matrix.py` had NO
sys.exit at all — it printed its failures and returned 0 regardless. A committed test that
cannot fail loudly is worse than no test: the next reader sees green and stops looking. That
is the exact defect this whole arc was about, so the runner refuses to inherit it.

STATUS UPDATE (2026-07-26): that specific gap is CLOSED — HIKARI added the missing `sys.exit`
to round4b in #79, and all three corpora now fail loudly on their own. **The runner does not
relax because of it.** The design below is deliberately independent of whether any given
corpus happens to be well-behaved today: a corpus is one edit away from losing its exit at any
time, and the runner must not have to be re-hardened when that happens. Read the next
paragraph as a standing rule, not as a workaround for a defect that has since been fixed.

THIS RUNNER DOES NOT TRUST EXIT CODES. It reads each corpus's OUTPUT and treats any line
carrying the failure marker as a failure, then ANDs that with the exit code. A corpus that
prints failures and exits 0 fails here. A corpus that exits 1 silently also fails here.

NO SCORE IS NOT A PASS  (MZ-RUNALL-SCORE-CLAUSE-001, 2026-07-26)
----------------------------------------------------------------
The first cut of this runner shipped `passed is None or passed == total` — i.e. a corpus that
printed NO score at all was waved through as clean. SHINOB1 built the artifact that proved it:
a corpus which dies before it prints anything emits no score AND no failure marker, and if it
lacks a `sys.exit` its return code is 0 as well. All three "clean" signals are then satisfied
by a corpus that never ran a single case, and the runner reports PASSED. (The corpus that
originally demonstrated this, round4b, has since been given a `sys.exit` in #79 — which
removes one instance, not the class. Any corpus authored without one lands here again, and
this clause is what catches it.)

That is this whole arc's defect wearing the runner's own uniform: A TEST THAT ASSERTS MORE
THAN IT MEASURES DOES NOT MISS A DEFECT, IT CERTIFIES THE BLIND SPOT. The clause is now
`passed is not None and passed == total` — absence of a score is absence of evidence, and
absence of evidence is reported as FAILS, never as clean. If a corpus legitimately has no
score to print, it must be taught to print one; it does not get to be exempt from measurement.

Note the shape, because it generalises past this file: every one of the three signals was a
NEGATIVE (no failures printed, no non-zero exit, no score mismatch), and a corpus that does
nothing satisfies all negatives perfectly. A clean verdict needs at least one POSITIVE signal
to rest on. Here that positive is "a score was actually printed."

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

`--confirmatory <name>[,<name>]` exempts CONFIRMATORY corpora from that inversion.

NOT EVERY CORPUS HUNTS A DEFECT  (MZ-RUNALL-SCORE-CLAUSE-001, second finding)
-----------------------------------------------------------------------------
`--expect-fail` assumed every corpus is defect-hunting. Some CONFIRM a property instead —
`round4b-nesting-matrix.py` confirms the span clause is order-independent. Measured against the
real pre-#76 rule: round3 went 17/17 -> 12/17 and round4 13/13 -> 8/13, while round4b scored
4/4 against BOTH. That is not a broken corpus. The old rule has no span clause at all, so
nesting order is trivially irrelevant and its four cases pass for a COMPLETELY DIFFERENT REASON
than they pass against the live rule. Same score, opposite causes.

The runner reported that working corpus as `XX ... did not fail` and failed the whole run, so
the prescribed discrimination check pointed at a correct file — and the obvious "fix" is to
damage it. A tool that indicts working code is worse than one that stays quiet.

Exemption is DECLARED BY THE OPERATOR, deliberately:
  - never inferred from the corpus source — these are reviewer-authored and stay byte-identical,
    so the runner does not get to require a marker inside someone else's file;
  - never a hardcoded name list in here, which would rot the moment a corpus is added;
  - a declared name matching no corpus is REFUSED (exit 2), because a typo'd exemption silently
    exempts nothing while the operator believes it worked.
Default is empty: with no declaration, behaviour is exactly as before.

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
    # clean == no printed failures AND exit 0 AND a score was ACTUALLY PRINTED and complete.
    # `passed is not None` is load-bearing: absence of a score is absence of evidence, not
    # evidence of success. See NO SCORE IS NOT A PASS in the module docstring.
    clean = (printed == 0 and proc.returncode == 0
             and passed is not None and passed == total)
    return clean, passed, total, printed, proc.returncode


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    rule = sys.argv[1]
    expect_fail = "--expect-fail" in sys.argv[2:]

    # --confirmatory: corpora that CONFIRM a property rather than hunt a defect. They pass
    # against a broken rule too, legitimately, so under --expect-fail they can never "fail as
    # expected" and were being reported XX. Declared explicitly by the operator — never
    # inferred, never read out of the corpus file (these are reviewer-authored and must stay
    # byte-identical), and never defaulted to a hardcoded name list that would rot.
    confirmatory = set()
    if "--confirmatory" in sys.argv:
        i = sys.argv.index("--confirmatory")
        if i + 1 < len(sys.argv):
            confirmatory = {x.strip() for x in sys.argv[i + 1].split(",") if x.strip()}
    if not os.path.isfile(rule):
        print(f"  rule file not found: {rule}")
        return 2

    corpora = sorted(glob.glob(os.path.join(HERE, "round*.py")))
    if not corpora:
        print(f"  no corpora found in {HERE}")
        return 2

    # A declaration that matches nothing is not a declaration — it is a typo that silently
    # exempts nobody while the operator believes otherwise. Refuse rather than run.
    names = {os.path.basename(c) for c in corpora}
    unknown = confirmatory - names
    if unknown:
        print(f"  --confirmatory names no corpus here: {', '.join(sorted(unknown))}")
        print(f"  known: {', '.join(sorted(names))}")
        return 2

    mode = "EXPECT FAIL" if expect_fail else "EXPECT CLEAN"
    print(f"\n=== adversarial corpora vs {os.path.basename(rule)}  [{mode}] ===")
    bad = []
    for c in corpora:
        clean, passed, total, printed, rc = run_corpus(c, rule)
        name = os.path.basename(c)
        is_conf = name in confirmatory
        score = f"{passed}/{total}" if passed is not None else "n/a"
        verdict = "clean" if clean else "FAILS"
        # A confirmatory corpus is expected to stay CLEAN in both modes — that is what makes it
        # confirmatory. Only defect-hunting corpora are required to fail under --expect-fail.
        agree = clean if (is_conf or not expect_fail) else (not clean)
        flag = "ok " if agree else "XX "
        tag = "  [confirmatory]" if is_conf else ""
        print(f"  {flag} {name:<34} {score:>7}  "
              f"printed_failures={printed}  exit={rc}  -> {verdict}{tag}")
        if not agree:
            bad.append(name)

    print("\n" + "=" * 72)
    if bad:
        want = "fail" if expect_fail else "be clean"
        print(f"FAILED — {len(bad)} corpus/corpora did not {want}: {', '.join(bad)}")
        return 1
    if expect_fail:
        n_disc = len(corpora) - len(confirmatory)
        print(f"PASSED — all {n_disc} defect-hunting corpora still DISCRIMINATE against this rule.")
        print("         Their green against the fixed rule therefore carries information.")
        if confirmatory:
            print(f"         {len(confirmatory)} declared confirmatory and exempted: "
                  f"{', '.join(sorted(confirmatory))}")
            print("         Their green carries NO discrimination information, by construction.")
    else:
        print(f"PASSED — all {len(corpora)} corpora clean against this rule.")
        print("         Verify discrimination separately with --expect-fail against a known-")
        print("         broken revision; a corpus that passes on both proves nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
