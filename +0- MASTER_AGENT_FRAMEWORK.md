# RPI Master Agent Framework
## Building AI Agent Teams for Cursor Projects

> **Version**: v1.6
> **Created**: January 10, 2026
> **Updated**: January 18, 2026  
> **Scope**: Universal - Applies to ALL RPI Projects  
> **Author**: Josh D. Millang + Claude

---

## Executive Summary

This framework defines how to structure AI agent teams for software development in Cursor. It provides:
1. **Core team structure** (GA + OPS are always present)
2. **Three specialist models** (Domain, Module, Hybrid)
3. **Decision tree** for choosing the right model
4. **Best practices** for documentation, handoffs, and compounding knowledge

---

## Part 1: Core Team Structure (Universal)

Every project has these **two static roles**:

### General Agent (GA) - Tech Lead / Coordinator

| GA DOES | GA DOES NOT |
|---------|-------------|
| Translate vision into tasks | Write feature code |
| Break down requirements | Run tests or validation |
| Assign tasks to specialists | Deploy anything |
| Review specialist reports | Fix bugs directly |
| Coordinate dependencies | Make product decisions (that's JDM) |

**GA Mindset**: "I plan the work, I don't do the work."

**GA Owns**: Entry point files (`Code.gs`), configuration, architecture decisions, documentation

---

### OPS/QA Agent - Quality Assurance + DevOps

| OPS DOES | OPS DOES NOT |
|----------|--------------|
| Run ALL validation (DEBUG_*, grep, tests) | Write new feature code |
| Check code quality across all files | Decide what features to build |
| Deploy to production | Assign tasks to specialists |
| Commit and push to git | Make architecture decisions |
| Document issues found | Fix bugs (sends back to SPC) |

**OPS Mindset**: "I verify everything works together, then ship it."

**OPS Owns**: Deployment, validation, version control

---

## Part 2: Specialist Models

Specialists (SPCs) are the workers who build features. **How you structure them depends on your project.**

### Model A: Domain-Based Specialists

**SPCs are experts in TECHNOLOGY domains.**

```
GA ─── OPS
 │
 ├── #1 AI (all AI/ML files)
 ├── #2 Integrations (all external APIs)
 ├── #3 Database (all data/schema)
 └── #4 Frontend (all UI)
```

**Best For:**
- Integration-heavy apps (many external APIs)
- Projects where tech domains are clearly separate
- Small-to-medium projects (4-6 total files)

**Example**: CEO Dashboard
- #1 AI owns `CEO_AI.gs`, `CEO_DailyBrief.gs`
- #2 Integrations owns `CEO_Slack.gs`, `CEO_Gmail.gs`, `CEO_Meetings.gs`
- #3 Database owns `CEO_Database.gs`
- #4 Frontend owns `Index.html`

**Pros**: Deep domain expertise, consistent patterns per domain
**Cons**: Features require multi-SPC coordination, UI bottleneck

---

### Model B: Module-Based Specialists

**SPCs own VERTICAL SLICES (full features).**

```
GA ─── OPS
 │
 ├── #1 Clients (ClientModule.gs + UI section)
 ├── #2 Accounts (AccountModule.gs + UI section)
 ├── #3 Reports (ReportModule.gs + UI section)
 └── #4 Admin (AdminModule.gs + UI section)
```

**Best For:**
- Apps with distinct business modules
- Large projects with independent features
- Teams that want maximum parallelization

**Example**: PRODASH
- #1 Clients owns `PRODASH_Clients.gs`
- #2 Accounts owns `PRODASH_Accounts.gs`
- #3 CLIENT360 owns `PRODASH_CLIENT360.gs`
- #4 RMD_CENTER owns `PRODASH_RMD_CENTER.gs`
- #5 UI owns `Index.html` (shared)

**Pros**: Full feature ownership, highly parallelizable, scales well
**Cons**: May duplicate patterns, UI still needs coordination

---

### Model C: Hybrid (Recommended for Most Projects)

**UI is domain-based (persistent), Modules are vertical (expandable).**

```
GA ─── OPS
 │
 ├── #1 UI (persistent - all frontend)
 │
 └── Module SPCs (added per phase):
     ├── #2 ModuleA (ModuleA.gs)
     ├── #3 ModuleB (ModuleB.gs)
     └── #4 ModuleC (ModuleC.gs)
```

**Best For:**
- Projects that grow over time (phased development)
- Apps with distinct business modules + shared UI
- When UI consistency matters (design system enforcement)

**Example**: CAM
- #1 UI owns `Index.html`, `Styles.html`, `Scripts.html` (persistent)
- #2 HYPO owns `CAM_HYPO.gs` (Phase 1)
- #3 Submitted owns `CAM_Submitted.gs` (Phase 2)
- #4 NewBiz owns `CAM_NewBiz.gs` (Phase 3)
- ...add SPCs as modules are built

**Pros**: UI consistency, module independence, scales by adding SPCs
**Cons**: UI specialist must coordinate with all module SPCs

---

## Part 3: Decision Tree

Use this flowchart to choose your specialist model:

```
START: New Project
    │
    ▼
┌─────────────────────────────────────────┐
│ How many distinct BUSINESS modules?     │
│ (e.g., Clients, Reports, Calculator)    │
└─────────────────────────────────────────┘
    │
    ├── 1-2 modules ──────────────────────► DOMAIN-BASED (Model A)
    │                                        Tech domains are more
    │                                        important than features
    │
    ├── 3+ modules, built ALL AT ONCE ────► MODULE-BASED (Model B)
    │                                        Max parallelization needed
    │
    └── 3+ modules, built IN PHASES ──────► HYBRID (Model C)
                                             Add SPCs as you go
    
ADDITIONAL FACTORS:
    │
    ├── UI consistency critical? ─────────► HYBRID (persistent UI SPC)
    │
    ├── Heavy integrations? ──────────────► DOMAIN-BASED (dedicated integration SPC)
    │
    └── Modules share lots of code? ──────► DOMAIN-BASED (avoid duplication)
```

### Quick Reference Table

| Scenario | Recommended Model |
|----------|-------------------|
| Personal tool, 4-5 files | Domain-Based |
| Large app, all built at once | Module-Based |
| Large app, phased development | Hybrid |
| Heavy external integrations | Domain-Based |
| Strong design system needed | Hybrid (persistent UI) |
| Rapid MVP, add features later | Hybrid |

---

## Part 4: Parallelization Rules

### What Can Run Concurrently?

| Task Type | Parallel? | Notes |
|-----------|-----------|-------|
| GA planning | NO | One GA per project |
| Independent SPCs | YES | If no shared dependencies |
| Dependent SPCs | NO | Wait for upstream SPC |
| OPS validation | NO | Sequential per version |
| Testing | YES | Multiple features can be tested |

### Dependency Patterns

**Domain-Based**: SPCs are independent (can all run in parallel)
```
#1 AI ──────┐
#2 Integrations ─┼──► OPS
#3 Database ─────┤
#4 Frontend ─────┘
```

**Module-Based**: Some modules depend on others
```
#1 Clients ───────┐
      ↓           │
#2 Accounts ──────┼──► #5 UI ──► OPS
      ↓           │
#3 Reports ───────┘
```

**Hybrid**: UI coordinates with all module SPCs
```
#1 UI ─────────────────────────────┐
                                   │
#2 Module (independent) ───────────┼──► OPS
#3 Module (independent) ───────────┤
#4 Module (depends on #2) ─────────┘
```

---

## Part 5: Living Documentation Protocol

> "Anytime we see Claude do something incorrectly, we add it to the briefing."

### How to Compound Knowledge

1. **Agent encounters issue or makes mistake**
2. **Agent reports to JDM with proposed addition**
3. **JDM (or GA) adds to appropriate section**
4. **Version increments** (v1.0 → v1.1)
5. **All future sessions benefit automatically**

### What to Document

| Category | Examples |
|----------|----------|
| **Code Standards** | No alert(), structured responses |
| **Gotchas** | GAS serialization limits, case sensitivity |
| **Patterns** | How to access MATRIX, how to format dates |
| **Anti-Patterns** | What NOT to do, with reasons |

### Recent Additions Log (Template)

```markdown
## Recent Additions Log

| Date | Version | Addition | Triggered By |
|------|---------|----------|--------------|
| Jan 10 | v1.1 | Hybrid model documentation | CAM project |
| Jan 5 | v1.0 | Initial framework | - |
```

---

## Part 6: Pre-Computed Context in Task Assignments

**Don't make agents discover context. Give it to them.**

### Bad Task Assignment
```markdown
# TASK: Fix the calculation bug
Look at the HYPO calculator and fix the issue.
```

### Good Task Assignment
```markdown
# TASK: Fix HYPO Q4 seasonal factor

## Pre-Computed Context
- File: `CAM_HYPO.gs`, lines 85-120
- Current Q4 factor: 1.4
- Expected behavior: Q4 should be highest (AEP peak)
- Actual behavior: Q4 showing lower than Q1
- DEBUG_HYPO() output: "Q4 total: $12,000 (expected: $18,000)"

## Root Cause (Suspected)
Line 95: `seasonalFactors[seasonKey]` may be using wrong key format

## Files to Modify
- `CAM_HYPO.gs` - Fix seasonal key lookup

## Acceptance Criteria
- [ ] Q4 shows highest revenue
- [ ] DEBUG_HYPO() returns expected values
```

**This reduces agent back-and-forth by 50%+.**

---

## Part 7: Self-Verification Checkpoints

**Every SPC should verify their own work BEFORE reporting complete.**

### Universal Checklist (All SPCs)

```markdown
Before reporting complete:
- [ ] No `alert()`, `confirm()`, `prompt()` in my changes
- [ ] All functions return `{ success: true/false, data/error }`
- [ ] No hardcoded colors (use CSS variables)
- [ ] My code follows existing patterns in the file
```

### Specialist-Specific Checklist (Template)

```markdown
## #X [Module] Self-Verification

Before reporting complete:
- [ ] Run: `DEBUG_[MyModule]()` - passes
- [ ] Run: `grep -r "alert\|confirm" [my files]` - no results
- [ ] Test: [specific manual test for this module]
- [ ] Verify: [what the output should look like]
```

---

## Part 8: Session Handoff Protocol

**Ensure continuity between sessions.**

### Handoff Document Template

```markdown
# Session Handoff

## Metadata
- **Date:** YYYY-MM-DD
- **Agent:** GA / SPC #X / OPS
- **Version Start:** vX.X
- **Version End:** vX.X

## Completed
- [ ] Task 1 - Done
- [ ] Task 2 - Done

## In Progress
- Task 3 - 60% complete, blocked by X

## State Left Behind
- Uncommitted changes: Yes/No
- Files modified: [list]
- Known issues: [any bugs introduced]

## Next Session MUST Do First
1. [Critical first step]
2. [Second priority]

## Context for Next Agent
[Nuance, gotchas, "I tried X but it didn't work because Y"]
```

---

## Part 9: Agent Document Hierarchy

For any project, create these documents:

```
/Project/
├── +0-MASTER_AGENT_FRAMEWORK.md    # THIS FILE (copy to new projects)
├── +0-PROJECT_KICKOFF_TEMPLATE.md  # How to start projects
├── +UI_DESIGN_GUIDELINES.md        # RPI UI standards
│
└── Docs/
    ├── 1-AGENT_BRIEFING.md         # Universal context for THIS project
    ├── 2.1-AGENT_SCOPE_GENERAL.md  # GA role
    ├── 2.2-AGENT_SCOPE_OPS.md      # OPS role
    └── 3.X-AGENT_SCOPE_SPC*.md     # One per specialist
```

### Document Flow

```
Agent starts session
    │
    ▼
Read 1-AGENT_BRIEFING.md (universal context)
    │
    ▼
Read own AGENT_SCOPE (role-specific)
    │
    ▼
Begin work
    │
    ▼
Report completion → GA reviews → OPS deploys
```

---

## Part 10: Mandatory Gates & Compliance

> **"The process enforces the standards, not JDM."**

These gates are **non-negotiable**. An agent cannot proceed past a gate without showing compliance in the chat. If a gate cannot be passed, the agent must report BLOCKED.

---

### GATE 1: Session Start (All Agents)

**Before ANY work begins, show this in chat:**

```
## SESSION START VERIFICATION

Project: [project name]
Role: [GA / SPC #X / OPS]
Working Directory: [path]

### Pre-Flight Checks
- [ ] Read briefing: `Docs/1-AGENT_BRIEFING.md` ✓
- [ ] Read scope doc: `Docs/[my scope doc]` ✓
- [ ] Git status: [paste output]
- [ ] Git remote: [paste output]

### Current State
- Version: vX.X
- Branch: [branch name]
- Uncommitted changes: Yes/No

### Session Goal
[What this session will accomplish]

**READY TO PROCEED: Yes / No (if No, explain blocker)**
```

**⛔ CANNOT START WORK until this is shown.**

---

### GATE 2: Before Modifying Files (SPCs)

**Before editing any file, confirm:**

```
## FILE MODIFICATION CHECK

File: [filename]
Owned by: [GA / SPC #X / OPS]
I am: [my role]

✅ I own this file - proceeding
❌ I do NOT own this file - BLOCKED, need [owner] to modify
```

**⛔ CANNOT EDIT files you don't own.**

---

### GATE 3: Before Reporting Complete (SPCs)

**Before saying "done", show this:**

```
## SPC COMPLETION REPORT: #X [Name]

### Changes Made
| File | Lines | Change |
|------|-------|--------|
| [file] | [X-Y] | [what changed] |

### Self-Verification Checklist
- [ ] No `alert()`, `confirm()`, `prompt()`
- [ ] All functions return `{ success, data/error }`
- [ ] No hardcoded colors
- [ ] Follows existing patterns in file
- [ ] [Module-specific check if applicable]

### Verification Method
[How I verified this works - e.g., "Reviewed code logic" or "Tested in browser"]

**STATUS: ✅ COMPLETE / ❌ BLOCKED**
[If blocked, explain what's stopping completion]
```

**⛔ CANNOT report "done" without this format.**

---

### GATE 4: Before Deployment (OPS)

**Before running deploy commands, show pre-flight:**

```
## OPS PRE-FLIGHT CHECK

### Git Verification
```bash
$ git status
[paste actual output]

$ git remote -v
[paste actual output]
```

### Pre-Flight Result
- [ ] On correct branch (main or feature branch)
- [ ] Working tree clean (or changes are intentional)
- [ ] Remote points to correct repo

**PRE-FLIGHT: ✅ PASSED / ❌ FAILED**
[If failed, STOP - do not proceed to deploy]
```

**⛔ CANNOT run deploy commands until pre-flight passes.**

---

### GATE 5: After Deployment (OPS)

**After deploy, show complete report:**

```
## OPS DEPLOY REPORT: vX.X

### Deploy Results
| Step | Command | Result |
|------|---------|--------|
| 1 | `clasp push` | ✅/❌ [output summary] |
| 2 | `clasp version` | ✅/❌ Version N created |
| 3 | `clasp deploy -i [ID] -V [N]` | ✅/❌ |
| 4 | `git commit` | ✅/❌ [hash] |
| 5 | `git push` | ✅/❌ |

### Post-Deploy Verification
- [ ] Tested in browser
- [ ] No console errors
- [ ] Expected behavior confirmed

**DEPLOY STATUS: ✅ COMPLETE / ❌ BLOCKED**
[If blocked, explain which step failed and why]
```

**⛔ "clasp push succeeded" is NOT a complete deploy. All 5 steps must pass and be shown.**

---

### GATE 6: Learning Detected

**When you encounter something undocumented:**

```
## LEARNING DETECTED

### What Was Learned
[The gotcha, pattern, or insight]

### Where to Document
- [ ] `_RPI_STANDARDS/+0- MASTER_AGENT_FRAMEWORK.md` (universal)
- [ ] `_RPI_STANDARDS/+0- [other standard]` (specific)
- [ ] `Project/Docs/[doc]` (project-specific)

### Documentation Action
- [ ] Added to [file] at [section]
- [ ] Committed: `docs: [message]`
- [ ] Pushed to repo

**LEARNING CAPTURED: ✅ Yes / ⏳ Deferred (explain why)**
```

**⛔ Learnings must be documented before session ends, or explicitly deferred with reason.**

---

### GATE 7: Session End (All Agents)

**Before ending session, show:**

```
## SESSION CLOSE

### Work Completed
- [x] [Task 1]
- [x] [Task 2]
- [ ] [Task 3 - not finished, state: X%]

### State Left Behind
- Uncommitted changes: Yes/No
- Deployed: Yes (vX.X) / No
- Handoff doc updated: Yes/No/N/A

### Learnings This Session
- [Learning 1 → documented in X]
- [Learning 2 → documented in Y]
- None

### Next Session Should
1. [First priority]
2. [Second priority]

**SESSION STATUS: ✅ Clean close / ⚠️ Handoff required / ❌ Incomplete**
```

**⛔ Sessions should not end without this summary.**

---

### Gate Enforcement Summary

| Gate | When | Blocker If Missing |
|------|------|-------------------|
| Session Start | Beginning of any work | Cannot proceed |
| File Modification | Before editing | Cannot edit |
| SPC Complete | Before reporting done | Cannot report complete |
| Pre-Flight | Before deploy commands | Cannot deploy |
| Deploy Report | After deploy | Deploy not confirmed |
| Learning Detected | When discovering something new | Must document or defer |
| Session End | Before closing | Incomplete handoff |

**JDM's role**: Review BLOCKED reports and exception requests. The gates handle routine compliance.

---

## Part 11: Anti-Patterns to Avoid

| Bad Pattern | Why It's Bad | Correct Approach |
|-------------|--------------|------------------|
| SPC runs DEBUG_* | Wastes SPC time, duplicates OPS work | SPC reports done → OPS validates |
| GA writes feature code | GA gets stuck, can't coordinate | GA assigns to SPC |
| SPC tests other SPC's code | Creates confusion, blame | OPS tests everything |
| OPS fixes bugs directly | Violates file ownership | OPS reports → JDM assigns to SPC |
| SPC deploys their own code | No quality gate | All deploys go through OPS |
| Creating SPCs without scope docs | Agents overlap, confusion | Always create scope doc first |
| Mixing Domain + Module arbitrarily | Unclear ownership | Choose one model, apply consistently |

---

## Appendix A: MCP Tools for Development

Agents have access to healthcare MCP tools during development sessions. These tools allow direct queries to external data sources without leaving the chat.

**Full Documentation:** `RPI-Standards/+0- MCP_TOOLS_SETUP.md`

### MCP Quick Reference

| Tool | Use When... | Example |
|------|-------------|---------|
| `lookup_npi` | Verify provider NPI | "Look up NPI 1234567890" |
| `search_providers` | Find providers by name/location | "Find cardiologists in Phoenix, AZ" |
| `search_diagnosis_codes` | Need ICD-10 diagnosis code | "ICD-10 code for type 2 diabetes" |
| `lookup_code` | Have a code, need description | "What is ICD-10 code E11.9?" |
| `check_dme_coverage` | Medicare DME questions | "Is a wheelchair covered by Medicare?" |

**Setup Required:** Clone `RPI-MCP-Servers`, run `npm install && ./setup.sh`, restart Cursor.

---

## Appendix B: Role Quick Reference Cards

### GA Quick Reference

```
YOUR JOB: Plan → Delegate → Review → Approve
NOT YOUR JOB: Code → Deploy → Test → Fix bugs

TASK ASSIGNMENT CHECKLIST:
- [ ] Clear title
- [ ] Pre-computed context
- [ ] Files to modify
- [ ] Acceptance criteria
- [ ] Dependencies noted

HANDOFF TO OPS:
"GA approval given. Ready for deployment. Version vX.X"
```

### OPS Quick Reference

```
YOUR JOB: Validate → Deploy → Document
NOT YOUR JOB: Write features → Make architecture decisions

PRE-FLIGHT (MUST PASS BEFORE DEPLOY):
cd /path
git status          # Must show "on branch main"
git remote -v       # Must show origin URL

DEPLOY (ALL 4 MUST SUCCEED):
1. clasp push --force
2. clasp version "vX.X - desc"
3. clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X"
4. git add -A && git commit -m "vX.X - desc" && git push

⚠️ IF GIT FAILS, REPORT FAILURE - DO NOT REPORT SUCCESS

VALIDATION:
- Run all DEBUG_* functions
- Check for alert/confirm/prompt
- Test in browser
- Verify no console errors
```

### OPS Deploy Report Template (MANDATORY)

```markdown
## OPS Deploy Report: vX.X

### Pre-Flight
- [ ] `git status`: On branch main, working tree clean
- [ ] `git remote -v`: origin https://github.com/retirementprotectors/[REPO].git

### Deploy Results
| Step | Command | Result |
|------|---------|--------|
| 1 | `clasp push` | ✅/❌ |
| 2 | `clasp version` | ✅/❌ Version N created |
| 3 | `clasp deploy` | ✅/❌ |
| 4 | `git commit` | ✅/❌ [commit hash] |
| 5 | `git push` | ✅/❌ |

### Status: ✅ COMPLETE / ❌ BLOCKED

[If blocked, explain what failed]
```

**⚠️ "clasp push succeeded" is NOT a complete deploy. All 5 steps must pass.**

### SPC Quick Reference

```
YOUR JOB: Build your piece → Report complete
NOT YOUR JOB: Touch other files → Deploy → Test other SPCs

BEFORE REPORTING:
- [ ] Self-verification checklist passes
- [ ] No banned patterns (alert, etc.)
- [ ] Code follows existing patterns

REPORT FORMAT:
## #X [Name] Complete
**Changes:** [File]: [What changed]
**Ready for:** OPS validation
```

---

## Part 11: Cursor Agent Deployment

**How to spin up SPC agents in separate Cursor chats.**

### Deployment Prompt Template

When GA delegates to an SPC, create a **single copy/paste prompt** containing:

```markdown
You are SPC #[N] [NAME] for the [PROJECT] project.

READ THESE FILES FIRST (in order):
1. /path/to/project/Docs/1-AGENT_BRIEFING.md
2. /path/to/project/Docs/3.X-AGENT_SCOPE_SPCX_[NAME].md
3. /path/to/project/Docs/0-SESSION_HANDOFF.md

TASK: [Clear Title]

Pre-Computed Context:
- Current version: vX.X
- Project: /path/to/project
- Current state: [what exists now]
- Desired state: [what should exist after]
- Reference pattern: [file to look at for patterns]
- Target user: [who this is for]

Files to Create/Modify:
- [filename] - [what to do]

Acceptance Criteria:
- [Specific, testable outcome]
- [Another outcome]
- No alert/confirm/prompt
- Follows existing patterns

When complete, report what you built and that it's ready for [next step].

Begin by reading the docs, then [do the work].
```

### Deployment Orchestration

GA tells JDM:
1. **What to deploy now** (which SPCs)
2. **What can run in parallel** (independent SPCs)
3. **What waits** (dependent SPCs, OPS)

Example:
```
DEPLOY NOW (parallel):
- #3 MEC ← new chat, paste prompt
- #4 SPH ← new chat, paste prompt

AFTER both report complete:
- OPS ← validates and deploys
```

### Parallelization Rules

| Can Run Simultaneously | Must Wait |
|------------------------|-----------|
| Independent module SPCs | UI waits for backend SPCs |
| Bug fixes in different files | OPS waits for all SPCs |
| | Dependent modules wait for upstream |

### OPS as Quality Gate

OPS validates BEFORE deployment:
- Run DEBUG_* functions
- grep for banned patterns
- Browser test
- Check for missing components (UI, API endpoints)

**OPS can BLOCK deployment** if validation fails. This is correct behavior.

---

## Part 12: GAS Deployment Gotchas

### Deployment ID Flag (CRITICAL)

Always specify deployment ID explicitly:
```bash
# WRONG - creates new deployment
clasp deploy -d "v1.0"

# RIGHT - updates existing deployment
clasp deploy -i AKfycby...DEPLOYMENT_ID... -V [VERSION] -d "v1.0"
```

### Template Variable Truthiness Bug

GAS HTML templates render booleans as strings:
```javascript
// In Code.gs
template.skipQual = false;

// In Index.html - WRONG (string "false" is truthy!)
const SKIP = <?= skipQual ?>;
if (SKIP) { /* THIS RUNS! */ }

// In Index.html - RIGHT
const SKIP = '<?= skipQual ?>' === 'true';
if (SKIP) { /* Only runs if actually true */ }
```

### Google Sheet Tab Names

Tab names must match **exactly**, including:
- Underscores: `_AGENT_MASTER` ≠ `AGENT MASTER`
- Case sensitivity
- Leading/trailing spaces

### GAS Caching

After `clasp push`, changes may take 2-3 minutes to reflect:
- Use versioned deployments for production
- Test in incognito to avoid browser cache
- Clear GAS cache: Deploy → Manage deployments → Archive old ones

### Multiple DOMContentLoaded Handlers

If you have multiple handlers, they ALL run:
```javascript
// WRONG - both run, may conflict
document.addEventListener('DOMContentLoaded', initQualWizard);
document.addEventListener('DOMContentLoaded', initCalculator);

// RIGHT - single handler with conditional logic
document.addEventListener('DOMContentLoaded', () => {
  if (shouldShowWizard) {
    initQualWizard();
  } else {
    initCalculator();
  }
});
```

---

## Appendix C: Incident Log

> "Document failures so we never repeat them."

### INC-001: DAVID-Hub Missing Git (Jan 11, 2026)

**What Happened:**
- DAVID-Hub project was created and developed over multiple sessions
- Agents deployed code via `clasp push` successfully
- OPS documentation included `git commit && git push` commands
- **Git was never initialized** - `git init` was skipped during project setup
- Result: Months of development with zero version control history

**Root Cause:**
- Project kickoff template had git init buried in a single bash block
- No verification checkpoint to confirm git was working
- Agents assumed git existed because deploy docs referenced it
- `clasp push` succeeded, so no one noticed git commands were failing

**Impact:**
- All version history lost (only final v6.1 state preserved)
- No ability to rollback or review changes
- 12,515 lines of code with no commit history

**Fix Applied:**
1. Updated `+0- PROJECT_KICKOFF_TEMPLATE.md`:
   - Git init is now Step 1 (before GAS setup)
   - Added mandatory `🛑 CHECKPOINT 2A` verification
   - Split setup into Phase 2A (Git) and Phase 2B (GAS)
   - Added explicit "DO NOT PROCEED" gate
2. Updated OPS Quick Reference:
   - Pre-flight now requires `git status` and `git remote -v`
   - Added mandatory **OPS Deploy Report Template**
   - Explicit warning: "clasp push succeeded" ≠ complete deploy
3. DAVID-Hub retroactively initialized with git + GitHub repo

**Prevention:**
- Agents MUST run `git remote -v` and report output before proceeding
- If output doesn't show `origin` URL, STOP and fix
- OPS must use Deploy Report Template showing ALL 5 steps passed
- If git fails, OPS must report BLOCKED, not success

---

## Appendix D: Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.6 | Jan 18, 2026 | Added Part 10: Mandatory Gates & Compliance - non-negotiable checkpoints |
| v1.5 | Jan 13, 2026 | Added reference to AI Platform Strategic Roadmap |
| v1.4 | Jan 13, 2026 | Added Appendix A (MCP Tools) - healthcare data access during development |
| v1.3 | Jan 12, 2026 | Added single code block format requirement for delegation prompts (Part 11) |
| v1.2 | Jan 12, 2026 | Added Appendix C (Incident Log) - INC-001 DAVID-Hub git failure |
| v1.1 | Jan 11, 2026 | Added Part 11 (Cursor Agent Deployment) and Part 12 (GAS Gotchas) from DAVID-Hub learnings |
| v1.0 | Jan 10, 2026 | Initial framework with Domain/Module/Hybrid models |

---

*This is the master framework for building AI agent teams. Update it as you learn.*
