---
name: quality-gate-deploy-verify
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: clasp\s+deploy
---

**QUALITY GATE: Verify Deploy Version**

You just ran `clasp deploy`. Now you MUST verify the deployment:

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deployments | grep "@[VERSION]"
```

Confirm the @VERSION number matches what you just deployed.
If it shows an OLD version number, the deploy FAILED — fix it before reporting success.

This is non-negotiable. On 2026-02-14 we discovered RAPID_API was stuck at @33 while code was at v108 because nobody verified.
