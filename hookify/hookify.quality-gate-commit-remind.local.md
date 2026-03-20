---
name: quality-gate-commit-remind
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+commit
---

**COMMIT GATE: Did you verify the build?**

Before committing:
1. `npm run build` passed? (catches webpack issues type-check misses)
2. No server-only code (fs, child_process) exported from shared package barrels?
3. All changes intentional? (`git diff --staged` reviewed?)
