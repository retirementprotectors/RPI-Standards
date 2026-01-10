# RPI Project Kickoff Template
## Starting a New Project with Agent Teams

> **Version**: v1.1  
> **Updated**: January 10, 2026  
> **Location**: `/Users/joshd.millang/Projects/_RPI_STANDARDS/`  
> **Scope**: Universal - Use this to start ANY new project

---

## 🔄 Two Workflows: Setup vs Development

### Workflow A: Project Setup (Starting New)

```
READ standards → CREATE project → CREATE project-specific docs → REFERENCE standards
```

**You READ from `_RPI_STANDARDS/`, you DON'T COPY into projects.**

### Workflow B: Development (Learning Something New)

```
Working on project → Hit a gotcha → UPDATE _RPI_STANDARDS → PUSH standards repo → Continue project
```

**"Shit, we forgot that. Document. Keep moving."**

---

## Phase 1: Pre-Setup (READ Standards First)

### Before Creating Anything, Read:

| Document | Location | Purpose |
|----------|----------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | `_RPI_STANDARDS/` | Agent team patterns, decision tree |
| `+0- UI_DESIGN_GUIDELINES.md` | `_RPI_STANDARDS/` | RPI Design System |
| This template | `_RPI_STANDARDS/` | Step-by-step setup |

**Do NOT copy these into your project.**

---

## Phase 2: Technical Setup

### AI Executes These Commands (JDM Does Not)

```bash
# 1. Create project folder
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME/Docs
cd /Users/joshd.millang/Projects/PROJECT_NAME

# 2. Create GAS project
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp create --type webapp --title "PROJECT_NAME"

# 3. Configure appsscript.json (CRITICAL for web apps)
# Must include webapp block or deployment URLs won't work

# 4. Initialize git
git init

# 5. Create GitHub repo and push
gh repo create retirementprotectors/PROJECT_NAME --public --source=. --push

# 6. Push to GAS
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force

# 7. STOP - JDM must do first-time auth (see below)
```

### ⚠️ First-Time GAS Deployment (JDM Manual Step)

**`clasp deploy` alone does NOT work for brand new projects.** GAS requires initial authorization through the Editor UI.

1. **AI provides**: GAS Editor URL (`https://script.google.com/home/projects/[SCRIPT_ID]/edit`)
2. **JDM opens** the URL in browser
3. **JDM clicks**: Deploy → New deployment → ⚙️ gear → Web app
4. **JDM sets**: Execute as **Me**, Who has access **Anyone within RPI**
5. **JDM clicks**: Deploy → Authorize access → Complete OAuth
6. **JDM provides**: The production URL back to AI
7. **AI documents**: URL in `Docs/2.2-AGENT_SCOPE_OPS.md`

**After this initial auth, all future `clasp deploy` commands work normally.**

### Required appsscript.json

```json
{
  "timeZone": "America/New_York",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "DOMAIN"
  }
}
```

### Setup Checklist

- [ ] Project folder created in `/Projects/`
- [ ] `Docs/` subfolder created
- [ ] GAS project created (`clasp create`)
- [ ] `appsscript.json` has `webapp` block
- [ ] Git repo initialized
- [ ] GitHub repo created (`gh repo create`)
- [ ] Code pushed to GAS (`clasp push`)
- [ ] **JDM: First-time auth via GAS Editor UI**
- [ ] Production URL documented
- [ ] MATRIX_ID set in Script Properties (if applicable)

---

## Phase 3: Assess & Choose Agent Model

### Answer These Questions

| Question | Answer |
|----------|--------|
| How many distinct business modules? | ___ |
| Will modules be built all at once or phased? | ___ |
| Heavy external integrations? | ___ |
| Is UI consistency critical? | ___ |

### Decision Tree

```
1-2 modules ──────────────────────► DOMAIN-BASED
3+ modules, all at once ──────────► MODULE-BASED  
3+ modules, phased ───────────────► HYBRID
UI consistency critical ──────────► HYBRID (persistent UI SPC)
Heavy integrations ───────────────► DOMAIN-BASED
```

### Record Your Decision

```markdown
**Project:** [NAME]
**Agent Model:** Domain-Based / Module-Based / Hybrid
**Reasoning:** [Why this model fits]

**Planned SPCs:**
- #1: [Name] - [Files]
- #2: [Name] - [Files]
```

---

## Phase 4: Create Project-Specific Docs

### Required Documents (In Project's `Docs/` Folder)

| Document | Purpose |
|----------|---------|
| `1-AGENT_BRIEFING.md` | Project context, references `_RPI_STANDARDS/` |
| `2.1-AGENT_SCOPE_GENERAL.md` | GA scope |
| `2.2-AGENT_SCOPE_OPS.md` | OPS scope, deployment URLs |
| `3.X-AGENT_SCOPE_SPC*.md` | Per specialist |

### Template: Agent Briefing Header

```markdown
# [PROJECT_NAME] - Agent Briefing Document

> **Version**: v1.0  
> **Last Updated**: [DATE]  
> **Purpose**: Master context for ALL agents  
> **Action**: Every agent reads this FIRST

---

## 📚 Standards Reference

Universal standards live in `_RPI_STANDARDS/` (NOT in this project):

| Document | Purpose |
|----------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Agent team patterns, parallelization |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | New project checklist |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI Design System |

**Location**: `/Users/joshd.millang/Projects/_RPI_STANDARDS/`  
**GitHub**: https://github.com/retirementprotectors/RPI-Standards

⚠️ **Do NOT copy standards into project repos** - reference them from central location.

---

## 🚨 CRITICAL: AI Executes Commands, JDM Does Not

**Josh (JDM) does not manually run terminal commands.** AI agents handle ALL:
- `clasp push`, `clasp deploy`
- `git commit`, `git push`
- File creation and editing

**Exceptions (JDM does manually):**
- `clasp login` (OAuth expired)
- First-time GAS deployment auth (browser UI)

---

[Continue with project-specific content...]
```

---

## Phase 5: Development Workflow

### During Normal Development

```
JDM assigns task → AI does work → AI deploys → Repeat
```

### When You Learn Something New (Living Documentation)

```
AI hits gotcha → AI updates _RPI_STANDARDS → AI pushes standards repo → AI continues project
```

**Commands to update standards:**

```bash
# 1. Update the relevant file in standards repo
cd /Users/joshd.millang/Projects/_RPI_STANDARDS

# 2. Commit and push
git add -A
git commit -m "docs: [what you learned]"
git push

# 3. Return to project and continue
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
```

### What Goes Where?

| Content | Location | Example |
|---------|----------|---------|
| Universal patterns | `_RPI_STANDARDS/` | "First-time GAS deploy needs Editor UI" |
| Project-specific | Project's `Docs/` | "CAM uses MATRIX for comp grids" |
| Project config | Project root | `CAM_Config.gs` |

---

## Quick Reference: URLs

| Resource | URL |
|----------|-----|
| Standards Repo | https://github.com/retirementprotectors/RPI-Standards |
| Standards Local | `/Users/joshd.millang/Projects/_RPI_STANDARDS/` |

| Project | GitHub | Local |
|---------|--------|-------|
| CAM | https://github.com/retirementprotectors/CAM | `/Projects/CAM` |
| PRODASH | https://github.com/retirementprotectors/PRODASH | `/Projects/PRODASH` |
| SENTINEL | https://github.com/retirementprotectors/SENTINEL | `/Projects/sentinel` |

---

## Appendix: Final Project Structure

```
/Users/joshd.millang/Projects/
│
├── _RPI_STANDARDS/              ← CENTRAL (read, don't copy)
│   ├── +0- MASTER_AGENT_FRAMEWORK.md
│   ├── +0- PROJECT_KICKOFF_TEMPLATE.md
│   ├── +0- UI_DESIGN_GUIDELINES.md
│   └── README.md
│
└── [PROJECT_NAME]/              ← PROJECT-SPECIFIC
    ├── Docs/
    │   ├── 1-AGENT_BRIEFING.md  ← References standards
    │   ├── 2.1-AGENT_SCOPE_GENERAL.md
    │   ├── 2.2-AGENT_SCOPE_OPS.md
    │   └── 3.X-AGENT_SCOPE_SPC*.md
    ├── appsscript.json
    ├── Code.gs
    ├── [Project]_Config.gs
    ├── [Project]_[Module].gs
    ├── Index.html
    ├── Styles.html
    └── Scripts.html
```

---

## Appendix: GAS Deployment Reference

### URL Types

| Type | Behavior | Use For |
|------|----------|---------|
| HEAD | Auto-updates with `clasp push` | Development |
| Versioned | Frozen snapshot | Production |

### Deployment Limits

| Limit | Value |
|-------|-------|
| Max deployments | 50 per project |
| Execution time | 6 minutes |
| URL fetch calls | 20,000/day |

### Default Access Settings (RPI)

- **Execute as**: Me
- **Who has access**: Anyone within RPI (Domain)

---

*Use this template every time you start a new project.*
