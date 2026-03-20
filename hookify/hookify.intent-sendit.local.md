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
4. **BRANCH + PR:** `git push origin [branch]` then `gh pr create --title "description"`
5. **CI GATE:** Wait for CI / check to pass (required by branch protection — cannot merge without green)
6. **MERGE:** `gh pr merge --squash` (merges to main → triggers deploy-api + Firebase App Hosting)
7. **DEPLOY REPORT:**

| Step | Result |
|------|--------|
| npm run build | pass/fail |
| git commit | [hash] |
| PR created | [URL] |
| CI / check | pass/fail (must pass to merge) |
| PR merged | [merge hash] |
| CI / deploy-api | pass/fail |
| Firebase App Hosting | auto-deploys on merge |

**Branch protection is ON.** Direct push to main is blocked. Must go through PR with CI green.
