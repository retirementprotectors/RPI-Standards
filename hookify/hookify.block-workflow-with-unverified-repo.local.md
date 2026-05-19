---
name: block-workflow-with-unverified-repo
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/[^/]+\.ya?ml$
  - field: content
    operator: regex_match
    pattern: "repository:\\s+[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+"
---

**BLOCKED: Unverified `repository:` reference in GH Actions workflow**

You are writing a GitHub Actions workflow that contains a `repository: <org>/<name>` field
(typically inside an `actions/checkout` step). This repo reference will 404 at runtime if
the org/name is wrong — and that failure is silent if `continue-on-error: true` is set.

**Why this is blocked:**

Tonight's incident (2026-05-19): `.github/workflows/hookify-rule-count.yml` had
`repository: retirementprotectors/_RPI_STANDARDS` but the actual repo is
`retirementprotectors/RPI-Standards` (hyphenated, mixed-case). The cross-repo checkout
returned 404. `continue-on-error: true` masked the failure for a day. JDM had to point
it out — he should never be the SSOT for a repo name.

**Before writing this workflow, verify EVERY `repository:` field exists:**

```bash
# Verify each referenced repo — must return HTTP 200, not 404
gh api repos/retirementprotectors/RPI-Standards      # correct
gh api repos/retirementprotectors/_RPI_STANDARDS     # WRONG — returns 404
```

If `gh api` returns 404, fix the repo name. Do NOT paper over the failure with
`continue-on-error: true`.

**NEVER do this:**

```yaml
# WRONG — unverified repo name + soft-fail hides the 404
- uses: actions/checkout@v4
  with:
    repository: retirementprotectors/_RPI_STANDARDS  # ← wrong name
    path: _RPI_STANDARDS
  continue-on-error: true                             # ← hides 404 for days
```

**Do this instead:**

```yaml
# CORRECT — verified repo name, hard-fail on error
- uses: actions/checkout@v4
  with:
    repository: retirementprotectors/RPI-Standards   # ← curl-verified
    path: RPI-Standards
# NO continue-on-error — let it fail loud if auth/repo breaks
```

**The anti-pattern `continue-on-error: true` on `actions/checkout`:**

Using `continue-on-error: true` on a checkout step converts a hard repo-not-found error
into a silent skip. Downstream steps then operate on a missing directory, producing
misleading partial results. The correct alternative is to surface the failure explicitly:

```yaml
- uses: actions/checkout@v4
  id: checkout-standards
  with:
    repository: retirementprotectors/RPI-Standards
    path: RPI-Standards

- name: Fail loud if checkout was skipped
  if: steps.checkout-standards.outcome == 'failure'
  run: |
    echo "::error::Cross-repo checkout failed. Verify repo name + PAT scope."
    exit 1
```

If a soft-fail is genuinely required, include an inline comment explaining the
expected failure condition and a dated TODO:

```yaml
  continue-on-error: true  # TODO(2026-06-01): remove when repo goes public — private fallback
```

**Doctrine:** JDM 2026-05-19 — "We MUST Improve. I should never be the SSOT for a repo name."
