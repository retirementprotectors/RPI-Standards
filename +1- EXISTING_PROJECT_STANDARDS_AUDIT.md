# Existing Project Standards Audit

> **When to Use**: Bringing an EXISTING project up to date with RPI-Standards  
> **How to Use**: Copy the DEPLOYMENT PROMPT into a new Cursor chat for each project  
> **Created**: January 11, 2026  
> **Version**: v1.2 alignment

---

## 🎯 Purpose

Use this when you have an **existing project** that was created before the latest RPI-Standards updates, or that drifted out of compliance. This agent task:

Updates a project's `Docs/` folder to align with RPI-Standards v1.2, specifically:

1. **OPS Scope** - Adds mandatory git pre-flight checks
2. **OPS Scope** - Adds mandatory deploy report template
3. **OPS Scope** - Updates version history (if outdated)
4. **All Scope Docs** - Fixes any MATRIX tab name references
5. **Commits to Git** - Pushes changes to GitHub

---

## 📋 Pre-Deployment Checklist (JDM)

Before launching agent, verify:

- [ ] Project has `Docs/2.2-AGENT_SCOPE_OPS.md`
- [ ] Project has git initialized (`git remote -v` works)
- [ ] You know the current version number

---

## 🚀 DEPLOYMENT PROMPT

**Copy everything below this line into a new Cursor chat:**

---

```
You are an OPS Documentation Agent. Your task is to align this project's documentation with RPI-Standards v1.2.

## PROJECT INFO
- **Project Path**: /Users/joshd.millang/Projects/[PROJECT_NAME]
- **Current Version**: v[X.X]
- **GitHub Repo**: https://github.com/retirementprotectors/[PROJECT_NAME].git

## STANDARDS REFERENCE
Read first: /Users/joshd.millang/Projects/RPI-Standards/+0- MASTER_AGENT_FRAMEWORK.md
(Specifically: Part 12 GAS Gotchas, Appendix A OPS Quick Reference, Appendix B Incident Log)

## YOUR TASKS

### Task 1: Update OPS Scope Doc

File: `Docs/2.2-AGENT_SCOPE_OPS.md`

**Add this section BEFORE "Pre-Deployment Validation" (or equivalent):**

```markdown
## 🛑 Pre-Flight Checks (MANDATORY)

**Run these BEFORE any deployment:**

\`\`\`bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status          # Must show "on branch main"
git remote -v       # Must show origin URL
\`\`\`

**Expected output:**
\`\`\`
On branch main
origin  https://github.com/retirementprotectors/[PROJECT_NAME].git (fetch)
origin  https://github.com/retirementprotectors/[PROJECT_NAME].git (push)
\`\`\`

⚠️ **IF GIT FAILS, REPORT FAILURE - DO NOT REPORT SUCCESS**

> **Background**: INC-001 (Jan 2026) - A project ran deploy commands for months without git initialized. All version history lost. See `_RPI_STANDARDS/+0- MASTER_AGENT_FRAMEWORK.md` Appendix B.
```

**Add this section AFTER "Version History":**

```markdown
## 📋 OPS Deploy Report Template (MANDATORY)

**Use this template for EVERY deployment:**

\`\`\`markdown
## OPS Deploy Report: vX.X

### Pre-Flight
- [ ] \`git status\`: On branch main, working tree clean
- [ ] \`git remote -v\`: origin https://github.com/retirementprotectors/[PROJECT_NAME].git

### Deploy Results
| Step | Command | Result |
|------|---------|--------|
| 1 | \`clasp push\` | ✅/❌ |
| 2 | \`clasp version\` | ✅/❌ Version N created |
| 3 | \`clasp deploy\` | ✅/❌ |
| 4 | \`git commit\` | ✅/❌ [commit hash] |
| 5 | \`git push\` | ✅/❌ |

### Status: ✅ COMPLETE / ❌ BLOCKED

[If blocked, explain what failed]
\`\`\`

**⚠️ "clasp push succeeded" is NOT a complete deploy. All 5 steps must pass.**
```

### Task 2: Check for MATRIX References

If any scope doc references MATRIX tabs, ensure:
- Tab name uses underscore prefix: `_AGENT_MASTER` (not `AGENT MASTER`)
- Add warning note about exact naming

### Task 3: Update Version History

If version history in OPS doc is outdated, update it to current version.

### Task 4: Commit and Push

After making changes:

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status
git remote -v
git add -A
git commit -m "docs: align with RPI-Standards v1.2 - add git pre-flight, deploy report template"
git push
```

## REPORT FORMAT

When complete, report:

```markdown
## Docs Alignment Report: [PROJECT_NAME]

### Pre-Flight
- [ ] `git status`: [result]
- [ ] `git remote -v`: [result]

### Changes Made
| File | Change |
|------|--------|
| `Docs/2.2-AGENT_SCOPE_OPS.md` | Added pre-flight checks, deploy report template |
| [other files if any] | [what changed] |

### Git
- Commit: [hash]
- Push: ✅/❌

### Status: ✅ COMPLETE
```

Begin by reading the project's Docs/ folder, then make the updates.
```

---

## 📁 Active Projects to Update

| Project | Path | Status |
|---------|------|--------|
| DAVID-HUB | `/Projects/DAVID-HUB` | ✅ Done |
| CAM | `/Projects/CAM` | 🔲 Pending |
| PRODASH | `/Projects/PRODASH` | 🔲 Pending |
| SENTINEL | `/Projects/sentinel` | 🔲 Pending |
| [Add more] | | |

---

## 💡 Tips

1. **Parallel Execution**: Launch multiple agents simultaneously - they're updating different projects
2. **Replace Placeholders**: Before pasting, replace `[PROJECT_NAME]` and `[X.X]` with actual values
3. **Verify Results**: Each agent should report a commit hash - verify it exists in GitHub

---

*One incident taught us. Now every project benefits.*
