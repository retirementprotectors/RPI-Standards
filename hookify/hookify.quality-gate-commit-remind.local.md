---
name: quality-gate-commit-remind
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+commit.*\.(gs|html|json)
---

**QUALITY GATE: Commit + Deploy Together**

You just committed GAS files (.gs/.html/.json). Remember the rule:

**Never commit without deploying. Never deploy without committing.**

If you haven't already deployed, run the deploy sequence now:
1. `clasp push --force`
2. `clasp version "vX.X"`
3. `clasp deploy -i [ID] -V [VER] -d "vX.X"`
4. VERIFY: `clasp deployments | grep "@[VERSION]"`
