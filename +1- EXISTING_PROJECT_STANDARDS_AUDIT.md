# Existing Project Standards Audit

> **When to Use**: Verifying an EXISTING project follows RPI-Standards  
> **Counterpart**: `+0- PROJECT_KICKOFF_TEMPLATE.md` (for NEW projects)  
> **How to Use**: Copy the DEPLOYMENT PROMPT into a new Cursor chat  
> **Version**: v2.0 (January 11, 2026)

---

## 🎯 Purpose

This audit verifies an **existing project** is fully compliant with RPI-Standards. It checks everything the Kickoff Template establishes, but retroactively.

| Kickoff Template | This Audit |
|------------------|------------|
| "Build it right" | "Is it right?" |
| Day 0 | Any day after |
| Creates docs | Verifies docs |

---

## 📋 What Gets Checked

| Category | Items |
|----------|-------|
| **Git & Deployment** | Git initialized, remote set, pre-flight in OPS, deploy report template |
| **Document Structure** | All required docs exist in `Docs/` |
| **Standards Reference** | Agent Briefing references `_RPI_STANDARDS/`, doesn't copy |
| **Agent Model** | Correct model chosen (Domain/Module/Hybrid) with rationale |
| **Role Boundaries** | GA/OPS/SPC scopes clearly defined |
| **Self-Verification** | Each SPC has checklist |
| **UI Compliance** | Design system followed, no forbidden patterns |
| **Code Quality** | No `alert()`/`confirm()`/`prompt()`, structured responses |

---

## 🚀 DEPLOYMENT PROMPT

**Copy everything below this line into a new Cursor chat:**

---

```
You are a Standards Audit Agent. Your task is to verify this project complies with RPI-Standards and fix any gaps.

## PROJECT INFO
- **Project Path**: /Users/joshd.millang/Projects/[PROJECT_NAME]
- **Project Name**: [PROJECT_NAME]
- **GitHub Repo**: https://github.com/retirementprotectors/[PROJECT_NAME].git

## STANDARDS REFERENCE (Read First)
- /Users/joshd.millang/Projects/RPI-Standards/+0- MASTER_AGENT_FRAMEWORK.md
- /Users/joshd.millang/Projects/RPI-Standards/+0- PROJECT_KICKOFF_TEMPLATE.md
- /Users/joshd.millang/Projects/RPI-Standards/+0- UI_DESIGN_GUIDELINES.md

---

## AUDIT CHECKLIST

### Phase 1: Git & Infrastructure

**1.1 Git Verification**
```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status
git remote -v
```

Expected:
- On branch main
- Remote origin points to `https://github.com/retirementprotectors/[PROJECT_NAME].git`

**Action if FAIL**: Initialize git, create GitHub repo, push.

---

### Phase 2: Document Structure

**2.1 Required Documents**

Check `Docs/` folder contains:

| Document | Required | Purpose |
|----------|----------|---------|
| `0-SESSION_HANDOFF.md` | ✅ | Current state, continuity |
| `1-AGENT_BRIEFING.md` | ✅ | Project context for all agents |
| `2.1-AGENT_SCOPE_GENERAL.md` | ✅ | GA role definition |
| `2.2-AGENT_SCOPE_OPS.md` | ✅ | OPS role + deployment info |
| `3.X-AGENT_SCOPE_SPC*.md` | Per specialist | One per SPC |

**Action if missing**: Create from templates in MASTER_AGENT_FRAMEWORK.md

---

### Phase 3: Standards Reference (Not Copies)

**3.1 Agent Briefing Header**

`1-AGENT_BRIEFING.md` MUST contain this section (or equivalent):

```markdown
## 📚 Standards Reference

Universal standards live in `_RPI_STANDARDS/` (NOT in this project):

| Document | Purpose |
|----------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Agent team patterns, parallelization |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | New project checklist |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI Design System |

**Location**: `/Users/joshd.millang/Projects/RPI-Standards/`
**GitHub**: https://github.com/retirementprotectors/RPI-Standards

⚠️ **Do NOT copy standards into project repos** - reference them from central location.
```

**3.2 No Duplicate Standards**

Search for and DELETE any files like:
- `+PROJECT_STANDARDS.md`
- `+DEPLOYMENT_MASTER_PLAN.md`
- `+Claude_Code_Strategies*.md`
- Any file duplicating content from `_RPI_STANDARDS/`

---

### Phase 4: Agent Model Documentation

**4.1 Model Selection**

`1-AGENT_BRIEFING.md` should document which model is used:

| Model | When to Use |
|-------|-------------|
| Domain-Based | 1-2 modules, tech domains more important |
| Module-Based | 3+ modules, all built at once |
| Hybrid | 3+ modules, built in phases, UI consistency critical |

**Check for**: Clear statement like "CAM uses the **Hybrid model** because..."

**Action if missing**: Add agent model section with rationale.

---

### Phase 5: OPS Scope Compliance

**5.1 Pre-Flight Checks (MANDATORY)**

`2.2-AGENT_SCOPE_OPS.md` MUST contain:

```markdown
## 🛑 Pre-Flight Checks (MANDATORY)

**Run these BEFORE any deployment:**

\`\`\`bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status          # Must show "on branch main"
git remote -v       # Must show origin URL
\`\`\`

⚠️ **IF GIT FAILS, REPORT FAILURE - DO NOT REPORT SUCCESS**
```

**5.2 Deploy Report Template (MANDATORY)**

`2.2-AGENT_SCOPE_OPS.md` MUST contain:

```markdown
## 📋 OPS Deploy Report Template (MANDATORY)

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
\`\`\`

**⚠️ "clasp push succeeded" is NOT a complete deploy. All 5 steps must pass.**
```

**5.3 Deployment Info**

OPS scope should include:
- [ ] Production URL documented
- [ ] Deployment ID for `clasp deploy -i` flag
- [ ] Version history (reasonably current)

---

### Phase 6: SPC Scope Compliance

**6.1 Self-Verification Checklists**

Each `3.X-AGENT_SCOPE_SPC*.md` should contain:

```markdown
## ✅ Self-Verification Checklist

Before reporting complete:
- [ ] No `alert()`, `confirm()`, `prompt()` in my changes
- [ ] All functions return `{ success: true/false, data/error }`
- [ ] No hardcoded colors (use CSS variables)
- [ ] My code follows existing patterns in the file
```

---

### Phase 7: Code Quality Scan

**7.1 Forbidden Patterns**

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]

# Check for banned dialog functions
grep -r "alert\|confirm\|prompt" *.html *.gs 2>/dev/null | grep -v "// " | grep -v "showConfirm"

# Check for hardcoded colors in HTML
grep -r 'style=.*#[0-9a-fA-F]' *.html 2>/dev/null
```

**Action if found**: Report specific file:line for remediation.

**7.2 MATRIX Tab Names**

If project uses MATRIX, verify tab names use underscore prefix:
- ✅ `_AGENT_MASTER`
- ❌ `AGENT MASTER`

---

### Phase 8: Session Handoff

**8.1 Handoff Document**

`0-SESSION_HANDOFF.md` should contain:
- [ ] Current version number
- [ ] What's complete vs in-progress
- [ ] Production URL
- [ ] Deployment commands
- [ ] Key learnings/gotchas

---

## AUDIT REPORT FORMAT

After completing all checks, report:

```markdown
## Standards Audit Report: [PROJECT_NAME]

### Pre-Flight
- [ ] `git status`: [result]
- [ ] `git remote -v`: [result]

### Document Structure
| Document | Status |
|----------|--------|
| `0-SESSION_HANDOFF.md` | ✅/❌/🔧 Fixed |
| `1-AGENT_BRIEFING.md` | ✅/❌/🔧 Fixed |
| `2.1-AGENT_SCOPE_GENERAL.md` | ✅/❌/🔧 Fixed |
| `2.2-AGENT_SCOPE_OPS.md` | ✅/❌/🔧 Fixed |
| `3.X-AGENT_SCOPE_SPC*.md` | ✅/❌/🔧 Fixed |

### Standards Compliance
| Check | Status |
|-------|--------|
| References `_RPI_STANDARDS/` (no copies) | ✅/❌/🔧 |
| Agent model documented with rationale | ✅/❌/🔧 |
| OPS has pre-flight checks | ✅/❌/🔧 |
| OPS has deploy report template | ✅/❌/🔧 |
| SPC scopes have self-verification | ✅/❌/🔧 |
| No forbidden patterns in code | ✅/❌/🔧 |

### Changes Made
| File | Change |
|------|--------|
| [file] | [what was added/fixed] |

### Git
- Commit: [hash]
- Push: ✅/❌

### Final Status: ✅ FULLY COMPLIANT / ⚠️ PARTIAL / ❌ NEEDS WORK

[Notes on any remaining issues]
```

---

## EXECUTION INSTRUCTIONS

1. Read the standards reference docs first
2. Run through each phase sequentially
3. Fix issues as you find them (don't just report)
4. Commit all changes with message: `docs: RPI-Standards audit - [summary of fixes]`
5. Push to GitHub
6. Report final status using the template above

Begin by checking git status and listing the Docs/ folder.
```

---

## 📁 Project Tracker

| Project | Path | Audit Status |
|---------|------|--------------|
| DAVID-HUB | `/Projects/DAVID-HUB` | ✅ Compliant |
| CAM | `/Projects/CAM` | ✅ Compliant |
| PRODASH | `/Projects/PRODASH` | ✅ Compliant |
| SENTINEL | `/Projects/sentinel` | ✅ Compliant |
| [Add more] | | |

---

## 💡 Tips for Batch Audits

1. **Parallel Execution**: Launch multiple agents simultaneously — they're independent projects
2. **Replace Placeholders**: Before pasting, replace `[PROJECT_NAME]` with actual name
3. **Verify Commits**: Each agent reports a commit hash — verify in GitHub
4. **Update Tracker**: Mark projects as compliant after successful audit

---

*One standard. Every project. No exceptions.*
