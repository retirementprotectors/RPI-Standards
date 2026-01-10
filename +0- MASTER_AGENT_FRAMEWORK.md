# RPI Master Agent Framework
## Building AI Agent Teams for Cursor Projects

> **Version**: v1.0  
> **Created**: January 10, 2026  
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

## Part 10: Anti-Patterns to Avoid

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

## Appendix A: Role Quick Reference Cards

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

PRE-FLIGHT:
cd /path && git pull && git status

DEPLOY (3-command):
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push && \
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -d "vX.X" && \
git add -A && git commit -m "vX.X" && git push

VALIDATION:
- Run all DEBUG_* functions
- Check for alert/confirm/prompt
- Test in browser
- Verify no console errors
```

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

## Appendix B: Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 10, 2026 | Initial framework with Domain/Module/Hybrid models |

---

*This is the master framework for building AI agent teams. Update it as you learn.*
