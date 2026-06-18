---
name: warn-gh-pr-edit-graphql-broken
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+pr\s+edit\b
owner: shinob1
---

⚠️ **`gh pr edit` is currently BROKEN — use a `gh api` REST PATCH instead.**

`gh pr edit` exits 1 on a GitHub **GraphQL "Projects (classic) deprecation"** error — the
command fetches `projectCards` during the edit, and GitHub deprecated that field. So ANY
`gh pr edit` (body, labels, title, reviewers) **silently fails the same way** right now —
the edit doesn't apply and the caller may not notice the exit 1.

**Workaround (REST path — dodges the deprecated GraphQL call):**

```bash
# Edit the PR body:
gh api repos/<owner>/<repo>/pulls/<N> -X PATCH -f body="$(cat body.md)"

# Add a label:
gh api repos/<owner>/<repo>/issues/<N>/labels -f "labels[]=<label-name>"

# Edit title:
gh api repos/<owner>/<repo>/pulls/<N> -X PATCH -f title="<new title>"
```

(`gh pr merge`, `gh pr view`, `gh pr checks`, `gh pr create` are all fine — only `gh pr edit`
hits the projectCards GraphQL path.)

**Why this exists:** hit independently twice — once landing shipped_refs via `gh api repos/.../pulls/N -X PATCH`
(SHINOB1), once by MEGAZORD patching the #1938 body to clear verify-shipped-refs (2026-06-16). It
fails quietly, so warriors burn time thinking the edit landed. WARN (not block) — the REST form is
the fix, and this lifts once `gh` ships the updated client / GitHub finishes the Projects-classic
sunset. If the breakage outlives the quarter, revisit whether to block + auto-suggest the REST form.
