---
name: warn-stale-branch-before-pr
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+pr\s+create\b
owner: shinob1
---

⚠️ **Before this PR — verify your branch carries ONLY your commits.**

Run this first:

```bash
git log origin/main..HEAD --oneline
```

- **Shows only the commits YOU made on this branch** → clean, proceed.
- **Shows commits you do NOT recognize (already-merged work, pre-squash SHAs, dozens of files)** → your worktree scratch branch was cut from a **STALE main** and is silently carrying already-squash-merged commits as pre-squash SHAs. The PR diff will be inflated (real case: **63 files instead of 4**, PR #1927). **Rebuild clean off current `origin/main` on a fresh worktree** before opening the PR.

**Why this exists:** a launcher-created worktree (`launch-warrior.sh` cuts `<warrior>/scratch`) can branch from a stale `main` ref. The squash-merge model means already-landed work reappears as un-squashed SHAs, so a diff against an old base re-includes it. Caught + corrected during ZRD-SCOPE-WLG-REDO-001 (PR #1927 closed contaminated → #1928 clean). Curated as craft doctrine in the RONIN `_INDEX` Build Reference (Worktree hygiene); this is the enforcement half — belt + suspenders, fleet-wide.

**WARN (not block):** the check needs live git state this hook cannot read — it fires the reminder; you run the one-liner. If a branch's base being stale becomes a recurring real failure, this upgrades to a pre-create gate.
