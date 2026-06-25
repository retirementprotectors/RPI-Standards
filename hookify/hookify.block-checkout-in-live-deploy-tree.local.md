---
name: block-checkout-in-live-deploy-tree
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: Projects/dojo-warriors(?![\w-])[^\n]*(checkout|switch\b)
owner: shinob1
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

**The invariant:**
`/home/jdm/Projects/dojo-warriors` = `main`. Always. `dojo-deploy-main.sh` depends on it.
Your isolated worktree (`dojo-warriors-<warrior>`) is the right place for all branch ops.

See: SHIN-DOJO-WT-102 / `scripts/launch-warrior.sh:ensure_dojo_worktree()`
