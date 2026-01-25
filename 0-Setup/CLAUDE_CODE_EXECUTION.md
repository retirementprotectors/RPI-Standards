# Claude Code Execution Layer
## Native Multi-Agent Orchestration for RPI Projects

> **Version**: v1.0
> **Created**: January 18, 2026
> **Scope**: Universal - Extends MASTER_AGENT_FRAMEWORK
> **Author**: Josh D. Millang + Claude

---

## Executive Summary

This document extends the Master Agent Framework to leverage Claude Code's native multi-agent capabilities. It **does not replace** existing standards - it automates their execution.

**What changes:** How agents are spawned and coordinated
**What stays the same:** Every rule, check, and standard in the framework

---

## Part 1: The Evolution

### Before (Manual Orchestration via Cursor)

```
JDM reads briefing
    ↓
JDM figures out what SPCs are needed
    ↓
JDM writes delegation prompts
    ↓
JDM copies prompts to new Cursor windows
    ↓
JDM tracks which windows are done
    ↓
JDM tells OPS to deploy
    ↓
JDM verifies deploy report
```

**Problem:** JDM was doing GA's job manually.

### After (Native Orchestration via Claude Code)

```
JDM says what they want (CEO role)
    ↓
Claude Code GA reads briefing + scope docs
    ↓
GA spawns SPC agents via Task tool
    ↓
SPCs work in parallel, report back to GA
    ↓
GA validates completeness
    ↓
GA executes OPS phase (deploy)
    ↓
GA reports deploy results to JDM
```

**Result:** JDM is CEO. Claude Code is the empowered GA.

---

## Part 2: Role Mapping

| Role | Who | What They Do |
|------|-----|--------------|
| **CEO** | JDM (Josh) | Vision, priorities, approval |
| **GA** | Claude Code (main session) | Plans, spawns agents, coordinates, deploys |
| **SPCs** | Task tool agents | Build assigned features, report back |
| **OPS** | GA (OPS phase) | Validate and deploy (GA wears OPS hat) |

### Key Insight: GA + OPS Merge

In Claude Code, the main session acts as both GA and OPS:
- **GA phase**: Planning, spawning SPCs, coordinating
- **OPS phase**: Validation, deployment, git operations

This works because:
1. Claude Code has persistent context (no window switching)
2. The Task tool agents report back to the main session
3. Deploy commands run in the same session

---

## Part 3: The Task Tool

Claude Code's `Task` tool spawns sub-agents that:
- Run autonomously with their own context
- Have access to all file tools (Read, Edit, Write, Glob, Grep)
- Report back with a summary when complete
- Can run in **parallel** (multiple Task calls in one message)

### Task Tool Syntax

```
Task tool parameters:
- subagent_type: "Explore" | "Plan" | "general-purpose"
- prompt: The full delegation prompt (like a Cursor prompt)
- description: Short label (3-5 words)
```

### Mapping to SPC Roles

| SPC Type | subagent_type | Use For |
|----------|---------------|---------|
| UI Specialist | general-purpose | Frontend changes |
| Module SPC | general-purpose | Backend module work |
| Research | Explore | Codebase exploration |
| Planning | Plan | Architecture decisions |

---

## Part 4: GA Orchestration Protocol

When JDM requests work, GA (Claude Code main session) follows this protocol:

### Step 1: Context Gathering

```
READ (in order):
1. Project's Docs/1-AGENT_BRIEFING.md
2. Relevant AGENT_SCOPE docs
3. RPI-Standards/0-Setup/MASTER_AGENT_FRAMEWORK.md (if needed)
4. Current state of files being modified
```

### Step 2: Task Planning

Determine:
- What SPCs are needed
- What files each SPC owns
- What can run in parallel vs sequential
- Pre-computed context for each SPC

### Step 3: SPC Deployment

Spawn agents using Task tool with full delegation prompts:

```markdown
[Task tool call with prompt:]

You are SPC #[N] [NAME] for the [PROJECT] project.

PROJECT CONTEXT:
- Project path: [path]
- You own these files: [list]
- Current version: vX.X

YOUR TASK: [Clear title]

Pre-Computed Context:
- Current state: [what exists]
- Desired state: [what should exist]
- Reference pattern: [file to follow]

Files to Modify:
- [file]: [what to do]

CRITICAL RULES (from RPI Standards):
- No alert(), confirm(), prompt() - use showToast/showConfirmation
- All functions return { success: true/false, data/error }
- No hardcoded colors - use CSS variables
- Follow existing patterns in the file

Self-Verification Before Reporting:
- [ ] No banned patterns
- [ ] Structured responses
- [ ] Follows existing code style

Report back with:
1. What you changed (file:line format)
2. Self-verification results
3. Any issues or questions
```

### Step 4: Parallel Execution

**Multiple independent SPCs can be spawned in ONE message:**

```
[Message with multiple Task tool calls]
- Task #1: SPC UI working on Styles.html
- Task #2: SPC HYPO working on CAM_HYPO.gs
Both run simultaneously, both report back
```

### Step 5: Coordination

When SPCs report back:
1. Review their changes
2. Check for conflicts or issues
3. If problems: spawn follow-up tasks
4. If complete: proceed to OPS phase

### Step 6: OPS Phase (Deploy)

GA executes deployment directly (no separate OPS agent needed):

```bash
# Pre-Flight (MANDATORY)
git status
git remote -v

# If pre-flight fails → STOP, report to JDM

# Deploy (ALL 5 STEPS)
1. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
2. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - description"
3. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X"
4. git add -A && git commit -m "vX.X - description"
5. git push
```

### Step 7: Deploy Report

GA reports to JDM using standard template:

```markdown
## Deploy Report: vX.X

### Pre-Flight
- [ ] `git status`: [result]
- [ ] `git remote -v`: [result]

### Deploy Results
| Step | Command | Result |
|------|---------|--------|
| 1 | clasp push | ✅/❌ |
| 2 | clasp version | ✅/❌ Version N |
| 3 | clasp deploy | ✅/❌ |
| 4 | git commit | ✅/❌ [hash] |
| 5 | git push | ✅/❌ |

### Status: ✅ COMPLETE / ❌ BLOCKED

[If blocked: what failed, what JDM needs to do]
```

---

## Part 5: Preserved Standards

These rules are **UNCHANGED** and **ENFORCED** in Claude Code execution:

### From Master Agent Framework

| Standard | How It's Enforced |
|----------|-------------------|
| File ownership | SPC prompts specify owned files only |
| No alert/confirm/prompt | Included in every SPC prompt |
| Structured responses | Included in every SPC prompt |
| Pre-flight git checks | GA runs before ANY deploy |
| 5-step deploy | GA executes all 5, reports each |
| Living documentation | GA updates standards when learning |

### From UI Design Guidelines

| Standard | How It's Enforced |
|----------|-------------------|
| CSS variables for colors | In SPC prompt rules |
| No inline color styles | In SPC prompt rules |
| RPI brand colors | Referenced in prompts |
| Mobile-first responsive | In UI SPC scope |

### From Project-Specific Docs

| Standard | How It's Enforced |
|----------|-------------------|
| Agent briefing context | GA reads first |
| Scope boundaries | SPC prompts define owned files |
| Current module status | GA checks before planning |

---

## Part 6: Error Handling

### SPC Reports Issue

```
SPC: "I found a problem - the function I need doesn't exist"
GA Action:
  1. Determine if another SPC should create it
  2. OR create it directly if it's infrastructure
  3. Spawn follow-up task with dependency resolved
```

### Deploy Step Fails

```
Step 3 (clasp deploy) fails with "invalid_grant"
GA Action:
  1. Report to JDM: "Clasp auth expired. Please run `clasp login`"
  2. Wait for JDM: "TCO" (Take Care Of)
  3. Retry deployment
```

### Git Not Initialized

```
Pre-flight: git status returns "not a git repository"
GA Action:
  1. STOP immediately
  2. Report to JDM: "Git not initialized. This is critical."
  3. Initialize git properly before ANY other work
  4. Reference INC-001 (DAVID-Hub incident)
```

---

## Part 7: Session Continuity

### Starting a New Session

GA should:
1. Check for `Docs/0-SESSION_HANDOFF.md`
2. Read current state
3. Pick up where previous session left off

### Ending a Session

GA should:
1. Update/create `Docs/0-SESSION_HANDOFF.md`
2. Document: what's done, what's in progress, what's next
3. Commit the handoff doc

### Handoff Template

```markdown
# Session Handoff

## Metadata
- **Date**: YYYY-MM-DD
- **Session Type**: Claude Code
- **Version Start**: vX.X
- **Version End**: vX.X

## Completed This Session
- [x] Task 1
- [x] Task 2

## In Progress
- Task 3 - 60% complete, [state]

## Next Session Should
1. [First priority]
2. [Second priority]

## Context for Continuation
[Anything the next session needs to know]
```

---

## Part 8: JDM's New Role

### What JDM Does Now

| Action | Example |
|--------|---------|
| State what you want | "Add dark mode to CAM" |
| Approve plans | "Yes, do it" or "No, change X" |
| Handle auth prompts | `clasp login` when requested |
| Review deploy reports | Verify success or investigate blocks |

### What JDM Does NOT Do

| Old Action | Now Handled By |
|------------|----------------|
| Write delegation prompts | GA (Claude Code) |
| Copy/paste to Cursor windows | Task tool |
| Track which SPCs are done | GA coordination |
| Tell OPS to deploy | GA triggers OPS phase |
| Manually verify standards | Embedded in SPC prompts |

### Magic Phrases

| JDM Says | GA Understands |
|----------|----------------|
| "TCO" | Auth/manual step complete, continue |
| "Ship it" | Deploy to production |
| "Hold" | Don't deploy yet |
| "Roll back" | Revert to previous version |

---

## Part 9: Example Flow

### JDM Request
> "The HYPO calculator needs a reset button that clears all inputs"

### GA Response

```
I'll handle this. Here's my plan:

**Analysis:**
- This touches UI (#1 UI scope) and possibly backend (#2 HYPO scope)
- UI: Add reset button to Index.html
- Backend: May need resetHYPO() function in CAM_HYPO.gs

**Execution:**
1. Spawn #1 UI to add reset button + click handler
2. Spawn #2 HYPO to add resetHYPO() if needed (checking first)
3. Both can run in parallel
4. After completion: OPS phase (validate + deploy)

Proceeding now...
```

### GA Spawns Tasks

```
[Task 1: UI Specialist]
- Add reset button to HYPO section
- Wire up click handler
- Follow existing button patterns

[Task 2: HYPO Specialist]
- Check if reset function exists
- If not, create resetHYPO()
- Return { success: true }
```

### SPCs Report Back

```
#1 UI Complete:
- Added reset button at Index.html:1247
- Styled with existing .btn-secondary class
- Click handler calls resetHYPO()

#2 HYPO Complete:
- Created resetHYPO() at CAM_HYPO.gs:45
- Clears all HYPO state variables
- Returns { success: true }
```

### GA Executes OPS Phase

```
Pre-flight passed. Deploying v1.7...

| Step | Result |
|------|--------|
| clasp push | ✅ |
| clasp version | ✅ v47 |
| clasp deploy | ✅ |
| git commit | ✅ a1b2c3d |
| git push | ✅ |

Status: ✅ COMPLETE

Reset button is live. Test at [URL].
```

---

## Part 10: When to Use Task Tool vs Direct Work

### Use Task Tool (Spawn SPC)

- Feature requires focused work in specific files
- Work can be parallelized with other tasks
- Clear scope boundaries exist
- Following SPC ownership model

### Do Directly (GA handles)

- Quick config changes
- Infrastructure/entry point files (GA owns these)
- Deployment operations
- Cross-cutting concerns
- Simple one-line fixes

### Use Explore Agent

- Understanding codebase structure
- Finding where something is implemented
- Research before planning

---

## Appendix A: Quick Reference

### GA Session Start Checklist

```
[ ] Read project's 1-AGENT_BRIEFING.md
[ ] Check for 0-SESSION_HANDOFF.md
[ ] Verify git status (learned from INC-001)
[ ] Understand current module status
[ ] Ready to receive JDM requests
```

### SPC Prompt Template

```
You are SPC #[N] [NAME] for [PROJECT].

PROJECT: [path]
YOUR FILES: [list]
VERSION: vX.X

TASK: [title]

Context:
- Current: [state]
- Desired: [state]
- Pattern: [reference]

Modify:
- [file]: [changes]

Rules:
- No alert/confirm/prompt
- Return { success, data/error }
- No hardcoded colors
- Follow existing patterns

Report: changes made, self-verification, issues
```

### Deploy Sequence

```bash
# Pre-flight
git status && git remote -v

# Deploy (all 5)
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - desc"
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [ID] -V [VER] -d "vX.X"
git add -A && git commit -m "vX.X - desc"
git push
```

---

## Appendix B: Relationship to Other Standards

```
┌─────────────────────────────────────────────────────────────┐
│                    _RPI_STANDARDS/                          │
│                                                             │
│  0-Setup/MASTER_AGENT_FRAMEWORK.md    ← Defines WHAT       │
│      (roles, rules, ownership)                              │
│                                                             │
│  0-Setup/CLAUDE_CODE_EXECUTION.md     ← Defines HOW        │
│      (THIS DOCUMENT - automation)    (you are here)        │
│                                                             │
│  0-Setup/UI_DESIGN_GUIDELINES.md      ← Defines LOOK       │
│      (colors, components, patterns)                         │
│                                                             │
│  0-Setup/PROJECT_KICKOFF_TEMPLATE.md  ← Defines START      │
│      (new project setup)                                    │
│                                                             │
│  1-Manage/EXISTING_PROJECT_STANDARDS_AUDIT.md ← Defines VERIFY │
│      (compliance checking)                                  │
└─────────────────────────────────────────────────────────────┘
```

**This document does not change the rules. It automates their enforcement.**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 18, 2026 | Initial Claude Code execution layer |

---

*This extends the Master Agent Framework for Claude Code native execution. All existing standards remain in effect.*
