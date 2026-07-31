#!/usr/bin/env python3
"""atomic-symlink.test.py — prove the absent-window is REAL and that rename(2) closes it.

TRK-HOOK-309 · scope OB1-HOOKIFY-OVERHAUL-001

WHY THIS TEST EXISTS IN THIS SHAPE. Two earlier attempts did NOT discriminate and are recorded
so nobody repeats them:

  1. A bash observer polling `[ -L "$link" ]` while `ln -sf` ran in a loop returned ZERO misses
     for BOTH constructions. `ln -sf` is a process spawn (~ms) and the unlink->symlink window
     inside it is ~us, so a bash loop essentially never samples it. A test that cannot fail
     carries no information — that result was a failed test, not a passing one.
  2. strace would have proven it deterministically by syscall sequence. Not installed on this
     box.

THREE ARMS, and the third is the one that tests THIS PR:
  ARM 3  drives the SHIPPED bash atomic_ln from scripts/atomic-symlink.sh under the observer.
         Added after audit: arms 1 and 2 alone NEVER CALL atomic_ln, so they prove rename(2)
         is atomic — a property of the KERNEL. Both mutations survived them green, including
         DELETING atomic_ln entirely. A suite that passes when the unit under test is gone is
         not testing that unit.
  ARM 1  models unlink+symlink (what `ln -sf` does) — the CONTROL. Must report misses.
  ARM 2  models symlink+rename — confirms the construction is sound in isolation.
It must FAIL in the control direction to mean anything: a run where arm 1 reports zero misses
is a broken test, not a fixed defect.

MEASURED CORRECTION TO THIS TICKET'S ORIGINAL PREMISE — read this before "fixing" arm 3.
GNU coreutils 9.4 `ln -sf` IS ALREADY ATOMIC. It does not unlink-then-symlink; it creates a
temporary and rename(2)s it. Measured on this box, same observer, same loop shape:
    ln -sf         20,000 replacements ->         0 absent observations
    rm -f + ln -s   2,000 replacements -> 1,991,738 absent observations  (positive control)
The observer demonstrably CAN see a window; the zero for `ln -sf` is a real zero.

CONSEQUENCE: mutating atomic_ln to `ln -sf` SURVIVES arm 3 GREEN, and that is CORRECT — on
this coreutils the two are behaviourally identical. It is not a hole in the test. Deleting
atomic_ln entirely is caught (rc != 0).

atomic_ln is still the right thing to ship, for two reasons that are not the original one:
  · it makes the guarantee EXPLICIT rather than depending on an undocumented coreutils
    implementation detail that a version bump could change;
  · `ln -sf` is NOT atomic on every implementation (busybox, some BSDs unlink first), and this
    corpus is installed by scripts that may run elsewhere.
THE ONLY MEASURED DEFECT WAS `rm -f` FOLLOWED BY `ln -sf` at setup-skills-symlinks.sh:133-134 —
an explicit unlink that opens the entire window itself.

RUN:  python3 scripts/atomic-symlink.test.py     exit 0 = discriminated, 1 = did not
"""
import os, sys, tempfile, threading, shutil

def main():
    T = tempfile.mkdtemp()
    try:
        a, b, link = os.path.join(T, 'a'), os.path.join(T, 'b'), os.path.join(T, 'link')
        open(a, 'w').write('A'); open(b, 'w').write('B')
        os.symlink(a, link)

        def run(mode, n=4000):
            stop = threading.Event(); misses = [0]
            def observe():
                while not stop.is_set():
                    if not os.path.islink(link):
                        misses[0] += 1
            t = threading.Thread(target=observe); t.start()
            for i in range(n):
                tgt = a if i % 2 else b
                if mode == 'unlink_symlink':          # what `ln -sf` does
                    try: os.unlink(link)
                    except FileNotFoundError: pass
                    os.symlink(tgt, link)
                else:                                  # what atomic_ln does
                    tmp = link + '.__atomic'
                    try: os.unlink(tmp)
                    except FileNotFoundError: pass
                    os.symlink(tgt, tmp)
                    os.rename(tmp, link)               # rename(2) — atomic
            stop.set(); t.join()
            return misses[0]

        # ── ARM 3 — DRIVE THE SHIPPED FUNCTION ITSELF ────────────────────────
        # FOUND BY AUDIT (RONIN-HOOKIFY-PHASE2 on RPI#122). Arms 1 and 2 below re-model the
        # two constructions IN PYTHON and never call atomic_ln. So on their own they prove
        # rename(2) is atomic — A PROPERTY OF THE KERNEL, NOT OF THIS PR. Both mutations
        # survived them GREEN: rewriting atomic_ln to the exact defect it exists to fix, and
        # DELETING IT ENTIRELY, both passed. A suite that passes when the unit under test is
        # deleted is not testing that unit.
        #
        # This arm drives scripts/atomic-symlink.sh's real atomic_ln, in bash, under the same
        # observer. It is the arm that can actually fail if the shipped code is wrong.
        import subprocess
        here = os.path.dirname(os.path.abspath(__file__))
        helper = os.path.join(here, 'atomic-symlink.sh')

        def run_shipped(n=1500):
            stop = threading.Event(); misses = [0]
            def observe():
                while not stop.is_set():
                    if not os.path.islink(link):
                        misses[0] += 1
            t = threading.Thread(target=observe); t.start()
            script = (
                f'source "{helper}"\n'
                f'for i in $(seq {n}); do\n'
                f'  atomic_ln "{a}" "{link}" || exit 3\n'
                f'  atomic_ln "{b}" "{link}" || exit 3\n'
                f'done\n'
            )
            rc = subprocess.run(['bash', '-c', script]).returncode
            stop.set(); t.join()
            return misses[0], rc

        if not os.path.islink(link):
            os.symlink(a, link)
        m_shipped, rc_shipped = run_shipped()
        print(f"  SHIPPED atomic_ln (bash)        : {m_shipped} observation(s) with the path ABSENT  (rc={rc_shipped})")
        if rc_shipped != 0:
            print("\nFAIL — the shipped atomic_ln returned non-zero; it did not complete its writes.")
            return 1
        if m_shipped != 0:
            print(f"\nFAIL — THE SHIPPED FUNCTION left the path absent {m_shipped} time(s).")
            print("       This is the arm that tests THIS PR. rename(2) being atomic does not")
            print("       help if atomic_ln is not using it.")
            return 1

        m_defect = run('unlink_symlink')
        if not os.path.islink(link):
            os.symlink(a, link)
        m_fixed = run('symlink_rename')

        print(f"  unlink+symlink (ln -sf pattern) : {m_defect} observation(s) with the path ABSENT")
        print(f"  symlink+rename (atomic_ln)      : {m_fixed} observation(s) with the path ABSENT")

        if m_defect == 0:
            print("\nFAIL — the defect arm reported ZERO. The observer never sampled the window,")
            print("       so this run proves nothing. Do not read it as a pass.")
            return 1
        if m_fixed != 0:
            print(f"\nFAIL — the atomic arm left the path absent {m_fixed} time(s). rename(2) is")
            print("       atomic, so this indicates the construction is not what it claims.")
            return 1
        print("\nPASS — window is real in the defect arm and CLOSED in the atomic arm.")
        return 0
    finally:
        shutil.rmtree(T, ignore_errors=True)

if __name__ == '__main__':
    sys.exit(main())
