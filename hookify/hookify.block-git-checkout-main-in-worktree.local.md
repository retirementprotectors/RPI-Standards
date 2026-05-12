---
name: block-git-checkout-main-in-worktree
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: ^\s*git\s+(checkout|switch)\s+(-[a-zA-Z]*\s+)*main(\s|$)
---

**BLOCKED: `git checkout main` / `git switch main` in a worktree**

This pattern is the #1 source of warrior-collision pain at RPI's scale. Here's what's
happening and how to fix it:

**The architecture:**
This repo has 80+ parallel `git worktree` checkouts (one per warrior, plus sprints,
hotfixes, scratchpads). *Each branch can only be checked out in ONE worktree at a time.*
When one worktree holds `[main]`, no other worktree can checkout main — git errors with:

```
fatal: 'main' is already used by worktree at '/home/jdm/Projects/toMachina-X'
```

You don't need to take the main lock to read main state. Use the alternatives below.

**Use one of these instead:**

| What you want | Command |
|---|---|
| Update your local `main` ref without checkout | `git fetch origin main:main` |
| Read main's commit log | `git log origin/main` |
| Diff your work against main | `git diff origin/main` |
| Rebase your branch on latest main | `git fetch origin && git rebase origin/main` |
| Read a file as it exists on main | `git show origin/main:path/to/file` |
| Check if a commit is on main | `git branch --contains <sha>` (use `-r` for remote) |

**The deeper doctrine (Trunk-Based Development):**
*Never* check out main in your worktree. Stay on your warrior branch for the life of
the worktree. Treat `origin/main` as your reference point — always-fresh, always-readable,
never-blocking. Branches die in hours, not days. Rebase on every push, not just at merge time.

See `~/.claude/CLAUDE.md` § "Trunk-Based Discipline" for the full doctrine.

**If you have a legitimate need to actually move a worktree onto main:**
This rule fires on `git checkout main`. The justified exception is when you're cleaning
up a stale worktree that will be removed. In that case, run `git worktree remove <path>`
first, then operate from a fresh checkout — never park `main` in a long-lived worktree.

Why this exists: ZRD-WORKTREE-MAIN-CHECKOUT-PROTECTION-001 / ZRD-TRUNK-BASED-DEVELOPMENT-001
(JDM directive 2026-05-12 — "How does this shit happen?").
