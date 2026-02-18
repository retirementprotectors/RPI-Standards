---
name: quality-gate-commit-remind
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+commit
  - field: command
    operator: not_contains
    pattern: clasp push
  - field: command
    operator: regex_match
    pattern: \.(gs|html|json)
---

**BLOCKED: GAS commit without deploy**

You cannot commit GAS files (.gs/.html/.json) without deploying first.

**Never commit without deploying. Never deploy without committing.**

Run the full 6-step deploy sequence:
1. `clasp push --force`
2. `clasp version "vX.X - description"`
3. `clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X"` (chained with `clasp deployments` verify)
4. `git add -A && git commit -m "vX.X - description"`
5. `git push`
