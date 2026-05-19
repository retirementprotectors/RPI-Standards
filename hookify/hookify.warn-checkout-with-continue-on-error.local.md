---
name: warn-checkout-with-continue-on-error
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/[^/]+\.ya?ml$
  - field: content
    operator: regex_match
    pattern: "uses:\\s+actions/checkout"
  - field: content
    operator: regex_match
    pattern: "continue-on-error:\\s+true"
---

**WARNING: `actions/checkout` + `continue-on-error: true` anti-pattern detected**

You are writing a GH Actions workflow where `actions/checkout` is used alongside
`continue-on-error: true`. This combination silently swallows auth failures, missing
repos, and invalid ref errors — converting hard failures into invisible skips.

**Why this matters:**

Tonight's incident (2026-05-19): a cross-repo checkout with a wrong repo name
(`_RPI_STANDARDS` instead of `RPI-Standards`) returned 404. `continue-on-error: true`
masked the failure for a day. The workflow appeared green. JDM had to diagnose it manually.

**The anti-pattern:**

```yaml
# WRONG — silent skip if checkout fails for ANY reason
- uses: actions/checkout@v4
  with:
    repository: retirementprotectors/RPI-Standards
    path: RPI-Standards
  continue-on-error: true
```

**Why this is dangerous:**
- Repo name typo → 404 → step marked "skipped" → downstream steps see empty dir
- Token scope too narrow → auth failure → same silent skip
- Ref deleted → same silent skip
- All look identical in the workflow log at a glance

**Preferred replacement — fail loud with a clear message:**

```yaml
- uses: actions/checkout@v4
  id: checkout-standards
  with:
    repository: retirementprotectors/RPI-Standards
    path: RPI-Standards

- name: Verify checkout succeeded
  if: steps.checkout-standards.outcome == 'failure'
  run: |
    echo "::error::Cross-repo checkout of RPI-Standards failed."
    echo "::error::Check: (1) repo name is correct, (2) PAT has repo scope, (3) ref exists."
    exit 1
```

**If a soft-fail is genuinely needed** (e.g., optional supplementary data source),
document it inline with a dated TODO and an explicit fallback:

```yaml
- uses: actions/checkout@v4
  id: checkout-optional
  with:
    repository: org/optional-repo
    path: optional-repo
  continue-on-error: true  # TODO(2026-07-01): remove — optional until repo goes public

- name: Log checkout status
  run: |
    if [ "${{ steps.checkout-optional.outcome }}" = "failure" ]; then
      echo "::warning::optional-repo checkout skipped — continuing without it"
    fi
```

**Rule:** every `continue-on-error: true` on a checkout step MUST have an inline
comment. No comment = silent bug waiting to happen.

**Doctrine:** JDM 2026-05-19 — "We MUST Improve. I should never be the SSOT for a repo name."
See also: `hookify.block-workflow-with-unverified-repo.local.md` (sibling BLOCK rule).
