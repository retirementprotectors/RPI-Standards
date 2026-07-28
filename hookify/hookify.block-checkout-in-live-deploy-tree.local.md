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
# OB1-LIVETREE-REPAIR-ALLOWLIST-001 (shinob1, 2026-07-28) — THE EXEMPTION WAS TRIED, PROVEN
# BYPASSABLE, AND REMOVED. THERE IS DELIBERATELY NO MACHINE EXEMPTION HERE. Do not add one.
#
# I added a third AND-condition `not_contains: dojo-livetree-repair.sh` so the sanctioned repair
# path would be exempt BY NAME rather than by accident. HIKARI broke it in one command, and I
# reproduced it before believing her:
#
#   CONTROL   git -C /home/jdm/Projects/toMachina switch                       -> BLOCKED by gate
#   MUTATION  git -C /home/jdm/Projects/toMachina switch # dojo-livetree-repair.sh
#                                                                              -> PASSED the gate,
#             died at git's own "fatal: missing branch or commit argument"
#
# The failure came from GIT, not from the gate. `not_contains` tests for MENTION, not
# INVOCATION, so a trailing comment stands the whole rule down. Anyone appending that comment to
# a REAL branch argument gets a raw checkout in a live deploy tree, past a block-action rule.
# It was strictly worse than the hole it replaced: the accidental carve-out was at least
# obscure, while this PUBLISHED A MAGIC STRING in the rule file — anyone reading the rule to
# understand it had learned how to defeat it.
#
# ANCHORING DOES NOT RESCUE IT, which is why there is no exemption rather than a cleverer one.
# Anchoring to command position stops the comment form but not chaining: any command that pairs
# a real checkout with a real invocation (`git -C <live> switch <branch> ; bash …repair.sh
# --dry-run <live>`) still satisfies an invocation-anchored test. The exemption is evaluated
# over the WHOLE command string, so it cannot distinguish "this program ran" from "this program
# is named somewhere in here." YOU CANNOT EXPRESS "THIS EXECUTABLE WAS INVOKED, AND NOTHING
# ELSE DANGEROUS WAS" AS A TEXT TEST OVER A RAW COMMAND LINE. My binding condition demanded
# something the mechanism cannot safely provide, and that was my error, not HIKARI's objection.
#
# WHY REMOVING IT COSTS NOTHING: the repair script never needed an exemption. It passes this
# gate because a script invocation carries no `git checkout` token — the accidental carve-out.
# An accidental carve-out is a real weakness, but it is a QUIETER one than a documented
# password, and the script's own refusals are what actually make it safe (registered targets
# only, incl. rejecting a worktree OF a live tree; refuse a peer's live seat; abort before
# touching the tree if the tip cannot be pushed to origin first).
#
# IF YOU EVER MAKE THIS RULE INSPECT SCRIPT CONTENTS OR RESOLVED EXECUTABLES, the repair path
# must be exempted THEN — keyed on the resolved executable, which the engine can actually
# verify, never on a substring of the command. Until the engine can do that, documentation is
# the exemption: see the corrective row in the table below.
#
# THE ROW THIS EARNED: a NEGATIVE condition needs the MIRROR of gotcha #46. Watching it fail
# in the intended direction is not enough — you must ask what ELSE it exempts. I disclosed that
# I could not make this condition fire as intended and labelled it unproven; nobody, including
# me, tested the unintended direction. That disclosure is what made HIKARI look.
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
