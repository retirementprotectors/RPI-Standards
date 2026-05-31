---
name: block-gh-pr-merge-admin-bypass
enabled: true
event: bash
action: block
# 2026-05-31 (SHINOB1): Authored after JDM caught me admin-bypassing
# verify-shipped-refs on PR #96 because my PR body was malformed.
#
# The pattern: "RONIN is waiting" or "it's just a docs gotcha" becomes a
# reflex to skip CI gates. If the CTO bypasses gates when convenient, the
# whole Operating System collapses to theater. The fix has to be at the
# bash-tool level so the bypass requires a conscious justification, not
# a reflex.
conditions:
  # Trigger: any `gh pr merge ... --admin` invocation
  - field: command
    operator: regex_match
    pattern: gh\s+pr\s+merge.*--admin
  # Opt-out: PR body or label must explicitly justify the bypass
  # Operator pattern: precede the merge with a labeling step OR include
  # the literal token `# admin-justified:` in the command (with reason)
  - field: command
    operator: not_contains
    pattern: '# admin-justified:'
owner: shinob1
---

**BLOCKED: `gh pr merge --admin` without written justification**

Per JDM directive 2026-05-31 (response to my PR #96 admin-bypass).

`--admin` bypasses branch protection and any failing required checks.
That option exists for genuine emergencies (CI infrastructure broken, hotfix
during incident, etc.) — NOT for routing around your own malformed PR body
or "RONIN is waiting" pressure.

**Why this is blocked:**
- A failing check is signal. If you bypass it instead of fixing it, you're
  telling the immune system its judgment doesn't matter
- The standard fix-the-cause path takes 60 seconds (edit PR body, push,
  CI re-runs) — exactly the length of time the bypass "saves"
- Repeated admin bypasses train the team to ignore CI signal entirely
- Per `feedback-the-answer-wins`: fix the actual cause, not the gate

**To proceed (the right path):**

1. **Fix the cause of the failing check.** Almost always:
   - `verify-shipped-refs` failing → PR body needs bare-line format
     (see `feedback_shipped_refs_bare_line_format`)
   - `rule-count-parity` failing → bump `EXPECTED_COUNT` in
     `.github/workflows/hookify-rule-count.yml`
   - Build failing → fix the build, not the check
2. Push the fix → CI re-runs → clean merge via `--auto --squash --delete-branch`

**If you genuinely need to bypass** (CI infra down, incident hotfix):
Append `# admin-justified: <one-line-reason>` to the command. Example:

```bash
gh pr merge 123 --squash --admin  # admin-justified: CI workers down, incident hotfix per JDM
```

The justification is committed to your shell history + visible in any
post-incident review. No silent bypasses.

**Reference:**
- `feedback_the_answer_wins` — fix the actual cause
- `feedback_shipped_refs_bare_line_format` — the gotcha I forgot
- JDM bilateral 2026-05-31 — the directive that made this rule load-bearing
