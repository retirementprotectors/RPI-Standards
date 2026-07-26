---
name: sendit
description: The toMachina #SendIt deploy sequence — pre-flight git status, build verify, commit, branch + PR, wait for CI green (branch protection blocks direct push to main), squash-merge, and produce a deploy report.
version: 0.1.0-draft
---

# SendIt

You have been invoked as the SendIt skill — deploy protocol triggered (#SendIt).

## toMachina Deploy Sequence

1. **PRE-FLIGHT:** `git status` — working tree clean?
2. **BUILD VERIFY:** `npm run build` — all workspaces pass?
3. **COMMIT:** `git add -A && git commit`
4. **BRANCH + PR:** `git push origin [branch]` then `gh pr create --title "description"`
5. **CI GATE:** wait for CI / check to pass (required by branch protection — cannot merge without green).
6. **MERGE:** `gh pr merge --squash` (merges to main → triggers deploy-api + Firebase App Hosting).
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

---

*SHINOB1, CTO · sendit · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-sendit` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
