---
name: quality-gate-deploy-verify
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+push
---

**DEPLOY GATE: Verify before pushing**

Before `git push origin main`:
1. Did `npm run build` pass? (NOT just type-check)
2. Is `git status` clean?
3. Are all changes committed?

Push to main triggers auto-deploy. Make sure the code is ready.
