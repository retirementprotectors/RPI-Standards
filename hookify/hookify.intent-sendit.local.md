---
name: intent-sendit
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#SendIt|#sendit|send\s+it|ship\s+it|deploy\s+to\s+prod)
---

**DEPLOY PROTOCOL TRIGGERED (#SendIt)**

toMachina Deploy Sequence:

1. **PRE-FLIGHT:** `git status` — working tree clean?
2. **BUILD VERIFY:** `npm run build` — all workspaces pass?
3. **COMMIT:** `git add -A && git commit`
4. **PUSH:** `git push origin main`
5. **CI MONITOR:** Watch GitHub Actions — check job + deploy-api job must both pass
6. **DEPLOY REPORT:**

| Step | Result |
|------|--------|
| npm run build | pass/fail |
| git commit | [hash] |
| git push | pass/fail |
| CI / check | pass/fail |
| CI / deploy-api | pass/fail |
| Firebase App Hosting | auto-deploys on CI pass |

**Do NOT push without `npm run build` passing locally.**
