---
name: quality-gate-deploy-verify
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: clasp\s+deploy\s+-
  - field: command
    operator: not_contains
    pattern: clasp deployments
---

**BLOCKED: Deploy without verification**

You cannot run `clasp deploy` without chaining the verification step.

Chain the verify command:
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X" && NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deployments | grep "@[VERSION]"
```

On 2026-02-14, RAPID_API production was stuck at @33 while code was at v108 because nobody verified. This gate prevents that from ever happening again.
