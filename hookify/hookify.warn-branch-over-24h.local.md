---
name: warn-branch-over-24h
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: ^\s*git\s+push(\s|$)
---

**WARN: Trunk-Based Discipline check — is this branch <24 hours old?**

At RPI's parallel-warrior scale, *branches that outlive 24 hours create rebase friction
that compounds across the entire team.* Every warrior who has to rebase against your
stale branch pays a cost. Every "behind main" anxiety adds up.

**Before this push, verify:**

```bash
git log -1 --format='%cr' $(git merge-base HEAD origin/main)
```

If the merge-base with `origin/main` is more than 24 hours old, *this branch should
have shipped or been broken up by now*. Options:

1. **Push it and land it immediately** — if it's ready, auto-merge it (`gh pr merge --auto --squash --delete-branch`). The fix is to ship faster, not to delay further.
2. **Break it into smaller PRs** — vertical slices that can land in <2 hours each. Feature-flag the incomplete pieces so they land off-by-default in main.
3. **Rebase and push** — `git fetch origin && git rebase origin/main`. *Do this BEFORE every push, not just at merge time.* Continuous rebase = trivial rebase.

**The deeper doctrine:**
Branches die in hours, not days. Rebase on every push. Feature flags wrap incomplete
work so code lands in main with the feature OFF. Decouples "code shipped" from "feature visible."

See `~/.claude/CLAUDE.md` § "Trunk-Based Discipline" for the full doctrine.

**Why this exists:**
ZRD-TRUNK-BASED-DEVELOPMENT-001 (JDM directive 2026-05-12). The "I have to rebase
for this" / "X is N commits behind main" / "running into each other's shit" pattern
is what this rule catches. At 10+ parallel agents pushing 20+ PRs/day, the old GitHub
Flow pattern doesn't scale — trunk-based with constant rebase does.

**This is a WARN, not a BLOCK:** the rule fires to remind you of the discipline,
but doesn't stop the push. The expectation is that warriors *internalize the discipline*
and rebase before pushing. If the discipline is consistently ignored, we upgrade to BLOCK.
