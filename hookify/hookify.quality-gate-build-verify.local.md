---
name: quality-gate-build-verify
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (type-check\s+pass|type.check.*13/13|13/13.*pass|npm run type-check)
---

**BUILD GATE: type-check is insufficient**

`npm run type-check` only validates TypeScript types. It does NOT catch:
- Webpack module resolution errors
- Server-only code leaked into browser bundles (fs, child_process)
- Next.js build failures

**Required:** `npm run build` (must pass all workspaces)

Learned 2026-03-19: 3 consecutive CI runs failed because type-check passed but webpack build did not.
