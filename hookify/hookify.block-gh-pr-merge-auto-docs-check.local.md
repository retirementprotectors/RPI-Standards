---
name: block-gh-pr-merge-auto-docs-check
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+pr\s+merge\b.*--auto\b
owner: shinob1
---

🛑 **BLOCKED: `gh pr merge --auto` — verify this PR is NOT docs-only first.**

**Merge command must match the change type:**

| Change type | Command | Why |
|---|---|---|
| Code (needs CI gate) | `gh pr merge <#> --auto --squash --delete-branch` | Wait for type-check + build + e2e |
| Docs-only (HTML / MD / images / CSS / .txt / .pdf) | `gh pr merge <#> --admin --squash --delete-branch` | Bypass branch protection — no point waiting ~5 min for CI to no-op against static files |

**Quick check — run this against the PR before deciding:**

```bash
gh pr view --json files -q '.files[].path' | grep -vE '\.(html|md|png|svg|jpg|jpeg|gif|webp|css|txt|pdf)$'
```

- **Output empty** → 100% docs-only → rerun with `--admin --squash --delete-branch`
- **Output non-empty** → has code/config changes → `--auto` IS the right command — bypass this block by piping the verification through first, e.g. `gh pr view ... && gh pr merge <#> --auto --squash --delete-branch` (the regex won't match if `--auto` isn't on the literal `gh pr merge` line).

**Why BLOCK, not WARN:** 2026-05-19 (this session) — the WARN version fired but its `systemMessage` got attached as a side-channel `hook_system_message` and didn't reliably surface inline with the Bash tool output, so Claude could miss it. BLOCK forces the action to terminate; the reason MUST surface. Per Sensei: *"Memory is documentation, hookify is enforcement, BLOCK is the obvious play."*

**Override (rare):** if the BLOCK fires on a legitimate code-PR `--auto` and the verification one-liner confirms code changes exist, just rerun the merge command in a way that doesn't match the regex (e.g. shell variable: `CMD="gh pr merge $PR --auto --squash --delete-branch"; $CMD`).
