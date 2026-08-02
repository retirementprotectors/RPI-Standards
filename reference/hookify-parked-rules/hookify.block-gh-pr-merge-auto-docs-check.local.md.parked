---
name: block-gh-pr-merge-auto-docs-check
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+pr\s+merge\b.*--auto\b
  # Opt-out: a verified code-PR declares itself with this token (mirrors the
  # admin-bypass rule's `# admin-justified:`). The merge proceeds ONLY when the
  # operator has run the docs-vs-code file check and is consciously asserting
  # this is a code PR that legitimately needs the CI gate. Intent-revealing,
  # not a regex dodge. (2026-06-11: the old shell-var "dodge" example stopped
  # working when the regex outgrew it; replaced with this proper token.)
  - field: command
    operator: not_contains
    pattern: '# code-verified:'
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
- **Output non-empty** → has code/config changes → the auto-queue IS the right command. Append the intent token (see Override) so the gate passes a *verified* code PR.

**Why BLOCK, not WARN:** 2026-05-19 (this session) — the WARN version fired but its `systemMessage` got attached as a side-channel `hook_system_message` and didn't reliably surface inline with the Bash tool output, so Claude could miss it. BLOCK forces the action to terminate; the reason MUST surface. Per Sensei: *"Memory is documentation, hookify is enforcement, BLOCK is the obvious play."*

**Override (rare):** when the BLOCK fires on a legitimate code PR and the file check above confirms code changes exist, append a trailing comment containing the literal token `# code-verified:` plus a short reason to the merge command. The gate's `not_contains` clause then lets that command through. This declares intent (you ran the check, you assert it is a code PR needing CI) rather than hiding from the regex. The earlier shell-variable evasion is RETIRED — it stopped working on 2026-06-11 and a documented evasion was the wrong design. Mirrors the `# admin-justified:` token on the admin-bypass rule.
