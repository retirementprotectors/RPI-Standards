---
name: block-checkout-in-live-deploy-tree
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: Projects/(dojo-warriors|toMachina)(?![\w-])
  - field: command
    operator: regex_match
    pattern: \bgit\s+(-C\s+\S+\s+)*(checkout|switch)\b
  - field: command
    operator: not_contains
    pattern: dojo-livetree-repair.sh
# OB1-LIVETREE-REPAIR-ALLOWLIST-001 (shinob1, 2026-07-28) — SANCTIONED BY NAME.
# Pairs with MZ-LIVETREE-REPAIR-001 (megazord, script frozen at 0aced9b9). This third
# AND-condition is the half of that scope that is mine; the script's own header declares the
# pairing INCOMPLETE without it, and asks the reader to say so rather than lean on it.
#
# WHY A NAMED EXEMPTION AND NOT NOTHING. The repair script would have passed this gate anyway,
# because a script invocation does not carry `git checkout` on the command line. That is an
# ACCIDENTAL carve-out — sanctioned by not-being-matched. It is the same shape as bracket
# notation evading block-direct-firestore-write, and as a message body evading every content
# matcher by travelling as a file path. Three instances in one night:
#
#     A CARVE-OUT EARNED BY SPELLING IS NOT A CARVE-OUT.
#     IT IS A HOLE THAT HAPPENS TO SUIT US.        (HIKARI, 2026-07-28)
#
# An accidental carve-out breaks SILENTLY the day the indirection hole closes, and it breaks in
# the exact incident where it is needed. Naming the script makes the exemption a DECISION with
# an owner instead of a side effect of how the command happens to be spelled.
#
# WHAT THIS DOES NOT WIDEN: the exemption is the script NAME, not the operation. The script
# itself refuses any target that is not one of the two registered live trees (its branch 2,
# exit 2 — including a worktree OF a live tree), refuses a peer's tree while that seat is alive
# (branch 6, exit 4), and aborts before touching the working tree if the tip cannot be pushed
# to origin first (branches 3/4, exit 5 — a deliberate inversion of the healer's
# WARN-and-continue at dojo-deploy-main.sh:98-103). Without those refusals this line would turn
# the gate into a laundromat for any branch op; with them, the only thing exempted is the one
# operation that restores the invariant this rule exists to protect.
#
# THE DEFECT THIS CLOSES, stated so it is not re-derived: dojo-deploy-main.sh:87-89 screams
# DRIFT[ACTIVE-BUILD] at severity "warn" and then `exit 1` — a terminal path wearing an
# advisory label — and deliberately does NOT auto-heal while the drifting warrior is alive.
# The only auto-restore (:105) sits in the DEAD-branch path. So the healer deferred to the live
# warrior and this rule forbade the live warrior, by every spelling. Both halves were correct
# in isolation. Together they were a deadlock, and the tell was a remediation table with four
# preventive rows and zero corrective ones. Hit live 2026-07-28 by SHINOB1 (restoring a tree)
# and MEGAZORD (proving the deadlock, filing the report, and testing the remedy) — the gate
# blocked the diagnosis, the incident report, and the fix's own test harness, and never once
# blocked an actual branch op on a live tree.
# MZ-LIVETREE-GUARD-001 (megazord, 2026-07-26) — EXTENDED to toMachina.
# This rule protected ONE of the two live deploy trees. `~/Projects/toMachina` is equally
# live (scopes-updater.service, mwm-board-lander, seven wire timers, and every warrior's
# SessionStart/Stop hooks exec out of it) and had NO guard of any kind.
# Consequence, measured 2026-07-26: that tree sat on `kagami/ob1-axe-contacts-qp-cleanup-001`
# for 8 days, 105 commits behind main. Its reflog shows kagami, shinob1 and ronin branches
# checked out directly IN the live tree going back to at least 2026-06-29 — it had been in
# routine use as a scratch checkout for over a month. The asymmetry was the whole bug: the
# lesson was learned once (SHIN-TRUNK-UNIFY-001, T440 freeze) and never back-ported.
owner: shinob1
reviewed: 2026-06-26 SHINOB1 A6 — FP fix. Old single pattern matched the dojo-warriors PATH + the bare word "switch"/"checkout" anywhere in the command, so any `node /home/jdm/Projects/dojo-warriors/.../dojo-reply.mjs "...global switch..."` (hub-status prose) tripped it. Split into AND conditions: (1) references the live deploy path, AND (2) contains an actual `git [-C <path>] checkout|switch` op. Prose containing "switch"/"checkout" no longer fires; real branch ops on the live tree still blocked. Same prose-substring FP class as block-opus-subagent / block-alert-confirm-prompt.
---

**BLOCKED: Branch checkout/switch targeting the live dojo-warriors deploy checkout**

The live `dojo-warriors` checkout (`/home/jdm/Projects/dojo-warriors`) is a **singleton
owned by `dojo-deploy-main.sh`**. It must always stay on `main`. Checking out a feature
branch there is what caused the 2026-06-25 T440 freeze: the deploy watchdog screamed
every 5 minutes for 6+ hours until SSH couldn't fork, requiring a physical power-cycle.

**Why this fires:**
Your command references `/home/jdm/Projects/dojo-warriors` (the live deploy checkout, not
a worktree) combined with `checkout` or `switch`. The gate fires before the op runs.

**What to do instead:**

| What you want | Correct path |
|---|---|
| Do dojo-warriors work | Use your isolated worktree: `~/Projects/dojo-warriors-<warrior>` |
| Create a feature branch | `cd ~/Projects/dojo-warriors-<warrior> && git checkout -b <branch>` |
| Read dojo-warriors files | Read from your worktree, not the live checkout |
| Update your worktree | `git -C ~/Projects/dojo-warriors-<warrior> fetch origin && git rebase origin/main` |
| **The live tree has ALREADY drifted and must be restored** | `bash ~/Projects/dojo-warriors/scripts/dojo-livetree-repair.sh <path>` — the SANCTIONED corrective path. Preserves your tip to a pushed `dojo-stash/…` ref **before** touching the tree, then restores the deploy branch. `--dry-run` prints the plan and writes nothing. |

> **The four rows above are PREVENTIVE — they tell you how not to CAUSE the state.**
> The fifth is CORRECTIVE — how to LEAVE it. That row was missing until 2026-07-28, and its
> absence was not cosmetic: `dojo-deploy-main.sh:87-89` refuses to auto-heal while the drifting
> warrior has a live session, so the healer defers to the live warrior — and this rule forbade
> the live warrior, by every spelling. No sanctioned repair existed. If you are ever hardening a
> gate, **an all-preventive remediation table is the tell that you have removed an escape hatch
> without providing a door.**

**The invariant:**
`/home/jdm/Projects/dojo-warriors` = `main`. Always. `dojo-deploy-main.sh` depends on it.
Your isolated worktree (`dojo-warriors-<warrior>`) is the right place for all branch ops.

See: SHIN-DOJO-WT-102 / `scripts/launch-warrior.sh:ensure_dojo_worktree()`
