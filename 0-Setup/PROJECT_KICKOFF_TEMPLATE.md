# RPI Project Kickoff Template
## Starting a New Project with Agent Teams

> **Version**: v2.1  
> **Updated**: January 26, 2026  
> **Location**: `/Users/joshd.millang/Projects/_RPI_STANDARDS/0-Setup/`  
> **Scope**: Universal - Use this to start ANY new project

---

## 🏗️ Platform Selection (First Decision)

Before creating a new project, determine which **SuperProject** it belongs to:

| Platform | SuperProject | Purpose |
|----------|--------------|---------|
| **SENTINEL** | `SENTINEL_TOOLS/` | B2B apps (DAVID channel) |
| **RIIMO** | `RAPID_TOOLS/` | Shared services (B2E) |
| **PRODASH** | `PRODASH_TOOLS/` | B2C apps (RPI channel) |

**See `THREE_PLATFORM_ARCHITECTURE.md` for full architecture.**

---

## 🚨 CRITICAL: Directory Location Rule

> **All projects MUST be in `/Users/joshd.millang/Projects/` within the appropriate SuperProject folder**

```
/Users/joshd.millang/
└── Projects/                    ← ALL PROJECTS GO HERE
    ├── _RPI_STANDARDS/          ← This standards repo (root level)
    ├── RAPID_TOOLS/             ← Shared services (B2E)
    │   ├── C3/                  ← Content/Campaign Manager (was RPI-Content-Manager)
    │   ├── CAM/                 ← Commission Accounting
    │   ├── CEO-Dashboard/       ← Executive visibility
    │   ├── MCP-Hub/             ← Intelligence layer
    │   ├── RAPID_API/           ← REST API
    │   ├── RAPID_CORE/          ← Core GAS library
    │   ├── RAPID_IMPORT/        ← Data ingestion
    │   ├── RPI-Command-Center/  ← Cross-suite comms
    │   └── RIIMO/               ← Operations UI (to be built)
    ├── SENTINEL_TOOLS/          ← B2B apps (DAVID)
    │   ├── DAVID-HUB/           ← BD qualification + calculators
    │   └── sentinel/            ← M&A platform
    └── PRODASH_TOOLS/           ← B2C apps (RPI)
        ├── PRODASH/             ← Client portal
        └── QUE/                 ← Quoting suite
            └── QUE-Medicare/    ← Medicare quoting
```

### ❌ DON'T: Clone to home directory root
```bash
cd /Users/joshd.millang
git clone https://github.com/...  # WRONG!
```

### ✅ DO: Clone to Projects folder
```bash
cd /Users/joshd.millang/Projects
git clone https://github.com/...  # CORRECT!
```

---

## 🔄 Two Workflows: Setup vs Development

### Workflow A: Project Setup (Starting New)

```
READ standards → CREATE project → CREATE project-specific docs → REFERENCE standards
```

**You READ from `RPI-Standards/`, you DON'T COPY into projects.**

### Workflow B: Development (Learning Something New)

```
Working on project → Hit a gotcha → UPDATE RPI-Standards → PUSH standards repo → Continue project
```

**"Shit, we forgot that. Document. Keep moving."**

---

## Phase 1: Pre-Setup (READ Standards First)

### Before Creating Anything, Read:

| Document | Location | Purpose |
|----------|----------|---------|
| `MASTER_AGENT_FRAMEWORK.md` | `RPI-Standards/0-Setup/` | Agent team patterns, decision tree |
| `UI_DESIGN_GUIDELINES.md` | `RPI-Standards/0-Setup/` | RPI Design System |
| This template | `RPI-Standards/0-Setup/` | Step-by-step setup |

**Do NOT copy these into your project.**

---

## Phase 2: Technical Setup

### ⚠️ CRITICAL: Git MUST Be Initialized FIRST

**DAVID-Hub Incident (Jan 2026):** Git was never initialized. Agents ran deploy commands for months without version control. All history lost.

**Prevention:** Git init is now Step 1, with mandatory verification.

---

### Step 2A: Create Project + Git (AI Executes)

```bash
# 1. Create project folder
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME
mkdir -p /Users/joshd.millang/Projects/PROJECT_NAME/Docs
cd /Users/joshd.millang/Projects/PROJECT_NAME

# 2. Initialize git FIRST (before anything else)
git init
git config user.email "josh@retireprotected.com"
git config user.name "Josh Millang"

# 3. Create .gitignore
cat > .gitignore << 'EOF'
.DS_Store
.cursor/
.clasprc.json
node_modules/
.env
.env.local
*.log
EOF

# 4. Create GitHub repo
gh repo create retirementprotectors/PROJECT_NAME --private --source=. --push --description "PROJECT_NAME - [description]"
```

### 🛑 CHECKPOINT 2A: Git Verification (MANDATORY)

**Agent MUST run and report these results before proceeding:**

```bash
cd /Users/joshd.millang/Projects/PROJECT_NAME
git status
git remote -v
```

**Expected output:**
```
On branch main
origin  https://github.com/retirementprotectors/PROJECT_NAME.git (fetch)
origin  https://github.com/retirementprotectors/PROJECT_NAME.git (push)
```

**If this fails, DO NOT PROCEED. Fix git setup first.**

---

### Step 2B: Create GAS Project (AI Executes)

```bash
cd /Users/joshd.millang/Projects/PROJECT_NAME

# 5. Create GAS project
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp create --type webapp --title "PROJECT_NAME"

# 6. Configure appsscript.json (see template below)

# 7. Initial commit with GAS config
git add -A && git commit -m "Initial setup: GAS project created" && git push

# 8. Push to GAS
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force

# 9. STOP - JDM must do first-time auth (see below)
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

### Setup Checklist (GATE - All Must Pass)

**Phase 2A - Git Setup (MUST complete before 2B):**
- [ ] Project folder created in `/Projects/`
- [ ] `Docs/` subfolder created
- [ ] **`git init` executed**
- [ ] **`.gitignore` created**
- [ ] **GitHub repo created (`gh repo create`)**
- [ ] **🛑 CHECKPOINT: `git remote -v` shows origin URL**

**Phase 2B - GAS Setup:**
- [ ] GAS project created (`clasp create`)
- [ ] `appsscript.json` has `webapp` block
- [ ] Initial commit pushed to GitHub
- [ ] Code pushed to GAS (`clasp push`)
- [ ] **JDM: First-time auth via GAS Editor UI**
- [ ] Production URL documented
- [ ] MATRIX_ID set in Script Properties (if applicable)

**⚠️ If any Phase 2A item is unchecked, STOP. Do not proceed to 2B.**

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

Universal standards live in `RPI-Standards/` (NOT in this project):

| Document | Purpose |
|----------|---------|
| `0-Setup/MASTER_AGENT_FRAMEWORK.md` | Agent team patterns, parallelization |
| `0-Setup/PROJECT_KICKOFF_TEMPLATE.md` | New project checklist |
| `0-Setup/UI_DESIGN_GUIDELINES.md` | RPI Design System |
| `0-Setup/JDM_WORKING_CONTEXT.md` | How to work with JDM |

**Location**: `/Users/joshd.millang/Projects/RPI-Standards/`  
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
AI hits gotcha → AI updates RPI-Standards → AI pushes standards repo → AI continues project
```

**Commands to update standards:**

```bash
# 1. Update the relevant file in standards repo
cd /Users/joshd.millang/Projects/RPI-Standards

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
| Universal patterns | `RPI-Standards/0-Setup/` | "First-time GAS deploy needs Editor UI" |
| Weekly management | `RPI-Standards/1-Manage/` | "Project compliance audit checklist" |
| Production launch | `RPI-Standards/2-Production/` | "User documentation suite" |
| Project-specific | Project's `Docs/` | "CAM uses MATRIX for comp grids" |
| Project config | Project root | `CAM_Config.gs` |

---

## Quick Reference: URLs

| Resource | URL |
|----------|-----|
| Standards Repo | https://github.com/retirementprotectors/RPI-Standards |
| Standards Local | `/Users/joshd.millang/Projects/RPI-Standards/` |

| Project | GitHub | Local |
|---------|--------|-------|
| CAM | https://github.com/retirementprotectors/CAM | `/Projects/CAM` |
| PRODASH | https://github.com/retirementprotectors/PRODASH | `/Projects/PRODASH` |
| DAVID-HUB | https://github.com/retirementprotectors/DAVID-HUB | `/Projects/DAVID-HUB` |
| SENTINEL | https://github.com/retirementprotectors/SENTINEL | `/Projects/sentinel` |
| RAPID_CORE | https://github.com/retirementprotectors/RAPID_CORE | `/Projects/RAPID_CORE` |
| RAPID_IMPORT | https://github.com/retirementprotectors/RAPID_IMPORT | `/Projects/RAPID_IMPORT` |
| RAPID_API | https://github.com/retirementprotectors/RAPID_API | `/Projects/RAPID_API` |

---

## Appendix: Final Project Structure

```
/Users/joshd.millang/Projects/
│
├── RPI-Standards/               ← CENTRAL (read, don't copy)
│   ├── README.md
│   ├── 0-Setup/                 ← Every New Agent + Project
│   │   ├── MASTER_AGENT_FRAMEWORK.md
│   │   ├── PROJECT_KICKOFF_TEMPLATE.md
│   │   ├── UI_DESIGN_GUIDELINES.md
│   │   └── ...
│   ├── 1-Manage/                ← Weekly Audit/Cleanup
│   │   ├── EXISTING_PROJECT_STANDARDS_AUDIT.md
│   │   └── ...
│   ├── 2-Production/            ← Production Launch
│   │   ├── PRODUCTION_LAUNCH_ROLLOUT_KIT.md
│   │   └── ...
│   └── 3-Reference/             ← Supporting Materials
│       ├── Plans/               ← Project Plans Archive
│       ├── Playbooks/           ← Team Operational Guides
│       └── Strategic/           ← Company Strategy
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

## Appendix: GAS Common Issues

### After clasp push

**IMPORTANT**: For GAS web apps, after `clasp push` you must:

1. Open GAS Editor
2. Deploy → Manage deployments
3. Edit existing deployment OR create new
4. Click Deploy

The deployed version doesn't auto-update from `clasp push`!

### RAPID_CORE Library Issue

The RAPID_CORE library tends to "disappear" from GAS projects. If you see errors about the library not being found:

1. GAS Editor → Resources → Libraries
2. Add: `1-HKxgcOIkx6Ov2uXk6TU-yJM24cvB4ctyCTuqS3NLEBs5XA-FFGWGJSI`
3. Version: 2
4. Identifier: `RAPID_CORE`
5. **Redeploy the web app** (required!)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | Jan 25, 2026 | Merged PROJECT_DIRECTORY_STANDARDS, updated to new folder structure |
| v1.1 | Jan 10, 2026 | Added INC-001 git verification checkpoints |
| v1.0 | Jan 5, 2026 | Initial template |

---

*Use this template every time you start a new project.*
