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

So the test models the two CONSTRUCTIONS directly — which is exactly what the fix changes —
with a tight in-process observer. It must FAIL in the first direction to mean anything:
a run where the unlink+symlink arm reports zero misses is a broken test, not a fixed defect.

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
