# RPI Project Kickoff Template
## Starting a New Project with Agent Teams

> **Version**: v1.0  
> **Created**: January 10, 2026  
> **Scope**: Universal - Use this to start ANY new project  
> **Prerequisite**: Read `+0-MASTER_AGENT_FRAMEWORK.md` first

---

## Phase 1: Project Setup Checklist

### Technical Setup

```bash
# 1. Create GAS project
clasp create --type webapp --title "PROJECT_NAME"

# 2. Create project folder
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME/Docs

# 3. Clone into folder
cd /Users/joshd.millang/Projects/PROJECT_NAME
clasp clone [SCRIPT_ID]

# 4. Initialize git
git init
git remote add origin https://github.com/retirementprotectors/PROJECT_NAME.git

# 5. Copy framework docs
cp /Users/joshd.millang/Projects/CAM/+0-MASTER_AGENT_FRAMEWORK.md .
cp /Users/joshd.millang/Projects/CAM/+UI_DESIGN_GUIDELINES.md .
```

### Checklist

- [ ] GAS project created (`clasp create`)
- [ ] Project folder created in `/Projects/`
- [ ] `Docs/` subfolder created
- [ ] Git repo initialized
- [ ] Remote added to GitHub
- [ ] Framework docs copied
- [ ] `appsscript.json` configured
- [ ] MATRIX_ID set in Script Properties (if applicable)

---

## Phase 2: Assess Project & Choose Agent Model

### Step 1: Answer These Questions

| Question | Answer |
|----------|--------|
| How many distinct business modules? | ___ |
| Will modules be built all at once or phased? | ___ |
| Heavy external integrations (APIs, etc.)? | ___ |
| Is UI consistency critical? | ___ |
| Estimated total files? | ___ |

### Step 2: Use Decision Tree

```
1-2 modules ──────────────────────► DOMAIN-BASED
3+ modules, all at once ──────────► MODULE-BASED
3+ modules, phased ───────────────► HYBRID
UI consistency critical ──────────► HYBRID (persistent UI SPC)
Heavy integrations ───────────────► DOMAIN-BASED
```

### Step 3: Record Your Decision

```markdown
**Project:** [NAME]
**Agent Model:** Domain-Based / Module-Based / Hybrid
**Reasoning:** [Why this model fits]

**Planned SPCs:**
- #1: [Name] - [Files]
- #2: [Name] - [Files]
- #3: [Name] - [Files]
```

---

## Phase 3: Create Agent Documents

### Required Documents

| Document | Create When | Template Below |
|----------|-------------|----------------|
| `1-AGENT_BRIEFING.md` | Always | Section A |
| `2.1-AGENT_SCOPE_GENERAL.md` | Always | Section B |
| `2.2-AGENT_SCOPE_OPS.md` | Always | Section C |
| `3.X-AGENT_SCOPE_SPC*.md` | Per specialist | Section D |

---

## Section A: Agent Briefing Template

```markdown
# [PROJECT_NAME] - Agent Briefing Document

> **Version**: v1.0  
> **Last Updated**: [DATE]  
> **Purpose**: Master context for ALL agents  
> **Action**: Every agent reads this FIRST

---

## Project Overview

**[PROJECT_NAME]** is [brief description of what the project does].

### The Stack

| Layer | Technology |
|-------|------------|
| Backend | Google Apps Script |
| Frontend | HTML/CSS/JS (GAS HtmlService) |
| Database | [MATRIX / Project-specific sheets] |
| Deploy | clasp CLI + Git |

### Key Identifiers

| Resource | Value |
|----------|-------|
| Project Path | `/Users/joshd.millang/Projects/[PROJECT_NAME]` |
| Script ID | [TBD after clasp create] |
| Database ID | [MATRIX_ID or project sheet] |
| Repo | `https://github.com/retirementprotectors/[PROJECT_NAME]` |

---

## Architecture

[Diagram or description of how components connect]

---

## Agent Team Structure

| Role | Agent | Responsibility |
|------|-------|----------------|
| CEO | JDM | Vision, priorities |
| Tech Lead | GA | Plan, delegate, review |
| [Specialists] | #1-N | [Per your model] |
| QA + DevOps | OPS | Validate, deploy |

### Agent Model: [Domain-Based / Module-Based / Hybrid]

[Explain why this model was chosen]

---

## Role Boundaries

[Copy from +0-MASTER_AGENT_FRAMEWORK.md - GA/SPC/OPS tables]

---

## File Ownership

| File | Owner | Purpose |
|------|-------|---------|
| `Code.gs` | GA | Entry point, routing |
| [List all files] | [Owner] | [Purpose] |

---

## Critical Rules

### No Native Dialogs
```javascript
// NEVER: alert(), confirm(), prompt()
// USE: showToast(), showConfirmation()
```

### Structured Responses
```javascript
return { success: true, data: [...] };
return { success: false, error: "Message" };
```

### [Project-Specific Rules]
[Add any rules specific to this project]

---

## Deployment

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -d "vX.X - Description"
git add -A && git commit -m "vX.X" && git push
```

---

## Living Documentation Protocol

This briefing is **compounding** - every mistake becomes a rule.

### Recent Additions Log

| Date | Version | Addition | Triggered By |
|------|---------|----------|--------------|
| [DATE] | v1.0 | Initial briefing | Project kickoff |

---

*Read your specialist scope document next.*
```

---

## Section B: GA Scope Template

```markdown
# [PROJECT_NAME] - General Agent (GA) Scope

> **Role**: Tech Lead / Coordinator  
> **Principle**: DELEGATE, DON'T DO  
> **Version**: v1.0

---

## Your Role

You are the coordinator. Translate JDM's vision into tasks, assign to specialists, review their work.

---

## Files You Own

| File | Purpose |
|------|---------|
| `Code.gs` | Entry point, routing |
| `[Config].gs` | Configuration, constants |
| `Docs/*.md` | Documentation |

---

## Agent Registry

| Agent | Focus | Files |
|-------|-------|-------|
| #1 | [Name] | [Files] |
| #2 | [Name] | [Files] |
| OPS | Validation | All (read-only) |

---

## Task Assignment Format

```markdown
# TASK: [Clear Title]

## Pre-Computed Context
- Current version: vX.X
- File: [filename], lines ~X-Y
- Current state: [what exists]
- Desired state: [what should exist]

## Files to Modify
- [filename] - [what to change]

## Acceptance Criteria
- [ ] [Specific outcome]

## Dependencies
- [Blocked by / Blocks / None]
```

---

## Coordination Protocol

### Session Start
1. Read `1-AGENT_BRIEFING.md`
2. Read this document
3. Assess current state
4. Create task breakdown

### Task Assignment
1. Create tasks in standard format
2. Identify parallelizable work
3. Note dependencies
4. Report plan to JDM

---

*You are the coordinator. Plan the work, let specialists do the work.*
```

---

## Section C: OPS Scope Template

```markdown
# [PROJECT_NAME] - OPS/QA Agent Scope

> **Role**: Quality Assurance + DevOps  
> **Version**: v1.0

---

## Your Role

You are the quality gate. Validate all specialist work, then deploy.

---

## Validation Checklist

### Code Quality
```bash
# No native dialogs
grep -r "alert\|confirm\|prompt" *.gs *.html

# Structured responses
# (manual review)
```

### Functional Validation

| Function | Expected |
|----------|----------|
| `DEBUG_[Module]()` | [Expected output] |

---

## Deployment Process

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]

# 1. Push
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push

# 2. Deploy
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -d "vX.X - Description"

# 3. Git
git add -A && git commit -m "vX.X" && git push
```

---

## Reporting Format

```markdown
## OPS Deployment Complete

**Version:** vX.X
**Deployed:** YYYY-MM-DD

### Validation
| Check | Result |
|-------|--------|
| Code quality | PASS/FAIL |
| DEBUG functions | PASS/FAIL |
| Web app loads | PASS/FAIL |

### Issues Found
- [Issue or "None"]
```

---

*Validate thoroughly, deploy carefully, document everything.*
```

---

## Section D: Specialist Scope Template

```markdown
# [PROJECT_NAME] - #[N] [SPECIALIST_NAME] Scope

> **Agent**: #[N] [Name]  
> **Files**: [List of owned files]  
> **Version**: v1.0

---

## Mission

[One sentence: what this specialist owns and does]

---

## Files You Own

| File | Purpose |
|------|---------|
| `[File].gs` | [Purpose] |

### Files You Read (Don't Modify)

| File | What You Use |
|------|--------------|
| `[Config].gs` | [What functions/constants] |

---

## Key Functions

```javascript
// List main functions this specialist implements
function [functionName]() { }
```

---

## Self-Verification Checklist

Before reporting complete:
- [ ] No `alert()`, `confirm()`, `prompt()`
- [ ] All functions return structured responses
- [ ] Run: `DEBUG_[MyModule]()` - passes
- [ ] [Module-specific checks]

---

## When Done

Report to JDM:

```markdown
## #[N] [Name] Complete

**Changes:** 
- [File]: [What changed]

**Ready for:** OPS validation
```

---

*Focus on your piece. OPS will validate.*
```

---

## Phase 4: First GA Session

Once documents are created, start your first GA session:

### GA Session 1 Checklist

1. **Read** `1-AGENT_BRIEFING.md` + `2.1-AGENT_SCOPE_GENERAL.md`
2. **Confirm** file structure is correct
3. **Create** initial task breakdown for Phase 1
4. **Assign** tasks to specialists
5. **Report** plan to JDM for approval

### Prompt for GA

```
You are the General Agent (GA) for [PROJECT_NAME].

Please read:
- 1-AGENT_BRIEFING.md (attached)
- 2.1-AGENT_SCOPE_GENERAL.md (attached)

Then create an initial task breakdown for Phase 1: [describe phase].

For each task, include:
- Clear title
- Pre-computed context
- Files to modify
- Acceptance criteria
- Which specialist should own it
```

---

## Phase 5: Running Parallel Specialists

### On 2 Machines

| Machine 1 | Machine 2 |
|-----------|-----------|
| SPC #1 | SPC #2 |
| SPC #3 | SPC #4 |
| GA review | OPS deploy |

### Prompt for Specialists

```
You are Specialist #[N] ([Name]) for [PROJECT_NAME].

Please read:
- 1-AGENT_BRIEFING.md (attached)
- 3.[N]-AGENT_SCOPE_SPC[N]_[NAME].md (attached)

Your task:
[Paste task from GA]

When complete, report in this format:
## #[N] [Name] Complete
**Changes:** [File]: [What changed]
**Ready for:** OPS validation
```

---

## Quick Reference: Project Paths

| Project | Path |
|---------|------|
| CAM | `/Users/joshd.millang/Projects/CAM` |
| PRODASH | `/Users/joshd.millang/Projects/PRODASH` |
| SENTINEL | `/Users/joshd.millang/Projects/sentinel` |
| CEO Dashboard | `/Users/joshd.millang/Projects/CEO Dashboard` |
| [NEW] | `/Users/joshd.millang/Projects/[NEW]` |

---

## Appendix: Files to Create for New Project

```
/Users/joshd.millang/Projects/[PROJECT_NAME]/
├── +0-MASTER_AGENT_FRAMEWORK.md    # Copy from CAM
├── +UI_DESIGN_GUIDELINES.md        # Copy from CAM
├── appsscript.json
├── Code.gs
├── [Project]_Config.gs
├── [Project]_[Module].gs           # Per module
├── Index.html
├── Styles.html
├── Scripts.html
└── Docs/
    ├── 1-AGENT_BRIEFING.md
    ├── 2.1-AGENT_SCOPE_GENERAL.md
    ├── 2.2-AGENT_SCOPE_OPS.md
    └── 3.X-AGENT_SCOPE_SPC*.md     # Per specialist
```

---

*Use this template every time you start a new project.*
