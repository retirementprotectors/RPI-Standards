---
name: warn-gh-pr-merge-auto-docs-check
enabled: true
event: bash
pattern: gh pr merge.*--auto
---

⚠️ **`gh pr merge --auto` detected. Confirm this PR is NOT docs-only before letting it queue behind CI.**

**Merge command must match the change type:**

| Change type | Command | Why |
|---|---|---|
| Code (needs CI gate) | `gh pr merge <#> --auto --squash --delete-branch` | Wait for type-check + build + e2e |
| Docs-only (HTML / MD / images / CSS / .txt / .pdf) | `gh pr merge <#> --admin --squash --delete-branch` | Bypass branch protection — no point waiting ~5 min for CI to no-op against static files |

**Quick check — run this against the PR before deciding:**

```bash
gh pr view --json files -q '.files[].path' | grep -vE '\.(html|md|png|svg|jpg|jpeg|gif|webp|css|txt|pdf)$'
```

- **Output empty** → 100% docs-only → cancel the `--auto` and rerun with `--admin --squash --delete-branch`
- **Output non-empty** → has code/config changes → `--auto` is correct, proceed

**Why this rule exists:** 2026-05-19 — SHINOB1 used `--auto` on `warrior-launch-guide.html` (PR #1223, docs-only). Memory file `feedback_docs_fast_path_main.md` documented the right pattern but didn't fire at the moment of action. Sensei caught it manually. This rule closes that gap by injecting the decision tree at the exact moment `--auto` is invoked.

**Upgrade path (if this WARN gets ignored):** swap to a `PreToolUse` shell hook in `settings.json` that runs the `gh pr view` check itself and BLOCKs on docs-only `--auto`. Heavier (requires settings.json edit + shell script in `~/.claude/hooks/`), reserved for after WARN has proven insufficient.
