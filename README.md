# RPI Standards

> **Single Source of Truth** for all RPI project standards, templates, and frameworks.
> 
> **Location**: `/Users/joshd.millang/Projects/RPI-Standards/`  
> **GitHub**: https://github.com/retirementprotectors/RPI-Standards

---

## 📁 Structure Overview

```
RPI-Standards/
├── README.md                    # This file
│
├── 0-Setup/                     # SETUP: Every New Agent + Project
│   ├── AI_PLATFORM_STRATEGIC_ROADMAP.md
│   ├── CLAUDE_CODE_EXECUTION.md
│   ├── JDM_WORKING_CONTEXT.md
│   ├── MASTER_AGENT_FRAMEWORK.md
│   ├── MCP_TOOLS_SETUP.md
│   ├── MDJ_STRATEGIC_VISION.md
│   ├── NEW_MACHINE_SETUP.md
│   ├── PROJECT_KICKOFF_TEMPLATE.md
│   ├── RPI_PLATFORM_BLUEPRINT.md
│   └── UI_DESIGN_GUIDELINES.md
│
├── 1-Manage/                    # MANAGE: Weekly Audit/Cleanup
│   ├── DOCUMENTATION_CLEANUP_GUIDE.md
│   ├── ECOSYSTEM_DOCUMENTATION_INVENTORY.md
│   ├── EXISTING_PROJECT_STANDARDS_AUDIT.md
│   └── WEEKLY_HEALTH_CHECK.md
│
├── 2-Production/                # POLISH: Production Launch
│   ├── PRE_LAUNCH_CHECKLIST.md
│   └── PRODUCTION_LAUNCH_ROLLOUT_KIT.md
│
├── Plans/                       # Project Plans Archive
│   └── (12 plan files)
│
├── Playbooks/                   # Team Operational Guides
│   ├── ProDash 101.md
│   ├── RPI- Leadership Team Playbook.md
│   ├── RPI Sales Team- Playbook.md
│   ├── RPI Service Team- Playbook.md
│   └── RPI Support Team- Playbook.md
│
└── Strategic/                   # Company Strategy
    └── rpi-data-division-strategy.md
```

---

## 🎯 The Three Categories

### `0-Setup/` — SETUP: Every New Agent + Project

Documents every agent and new project MUST read. Core standards, frameworks, and context.

| File | Purpose |
|------|---------|
| `MASTER_AGENT_FRAMEWORK.md` | Agent team patterns, parallelization rules, handoff protocols |
| `CLAUDE_CODE_EXECUTION.md` | Native multi-agent orchestration via Claude Code Task tool |
| `JDM_WORKING_CONTEXT.md` | How to work effectively with Josh D. Millang |
| `MDJ_STRATEGIC_VISION.md` | MyDigitalJosh AI capability layer for scaling to 500K clients |
| `AI_PLATFORM_STRATEGIC_ROADMAP.md` | Platform architecture and MCP roadmap |
| `RPI_PLATFORM_BLUEPRINT.md` | Complete system architecture - data, apps, experiences |
| `PROJECT_KICKOFF_TEMPLATE.md` | Checklist and templates for starting NEW projects |
| `NEW_MACHINE_SETUP.md` | Complete setup guide for new development machines |
| `MCP_TOOLS_SETUP.md` | MCP server configuration and tool reference |
| `UI_DESIGN_GUIDELINES.md` | RPI Design System - colors, typography, components |

### `1-Manage/` — MANAGE: Weekly Audit/Cleanup

Documents for maintaining healthy projects on an ongoing basis.

| File | Purpose |
|------|---------|
| `WEEKLY_HEALTH_CHECK.md` | **NEW** Quick weekly verification of all projects |
| `EXISTING_PROJECT_STANDARDS_AUDIT.md` | Comprehensive project compliance audit |
| `DOCUMENTATION_CLEANUP_GUIDE.md` | Clean up scattered docs, enforce folder structure |
| `ECOSYSTEM_DOCUMENTATION_INVENTORY.md` | Inventory of all docs across all projects |

### `2-Production/` — POLISH: Production Launch

Documents for taking projects to production.

| File | Purpose |
|------|---------|
| `PRE_LAUNCH_CHECKLIST.md` | **NEW** Technical verification before deployment |
| `PRODUCTION_LAUNCH_ROLLOUT_KIT.md` | User-facing documentation suite for production launches |

---

## 📁 Supporting Folders

### `Plans/` — Project Plans Archive

Contains project plans covering Commission Intelligence, CAM, DAVID-HUB, and RPI infrastructure. See [Plans/PLAN_INDEX.md](Plans/PLAN_INDEX.md) for full inventory.

### `Playbooks/` — Team Operational Guides

Human-facing operational guides for RPI teams (Sales, Service, Support, Leadership). These are NOT agent standards—they're employee playbooks.

### `Strategic/` — Company Strategy

High-level company strategy documents (e.g., "Weaponizing Operational Excellence" Data Division strategy).

---

## 🔀 When to Use What

### Starting a New Project
```
0-Setup/PROJECT_KICKOFF_TEMPLATE.md → Follow step by step
```

### New Agent Joining a Project
```
0-Setup/JDM_WORKING_CONTEXT.md → Read first
0-Setup/MASTER_AGENT_FRAMEWORK.md → Understand roles
Project's Docs/1-AGENT_BRIEFING.md → Project specifics
```

### Weekly Maintenance
```
1-Manage/WEEKLY_HEALTH_CHECK.md → Quick 15-min check
```

### Fixing a Project's Standards
```
1-Manage/EXISTING_PROJECT_STANDARDS_AUDIT.md → Full audit
```

### Deploying to Production
```
2-Production/PRE_LAUNCH_CHECKLIST.md → Technical verification
2-Production/PRODUCTION_LAUNCH_ROLLOUT_KIT.md → User documentation
```

### Setting Up a New Machine
```
0-Setup/NEW_MACHINE_SETUP.md → Complete environment setup
```

---

## 🔄 Two Workflows

### Workflow A: Project Setup (Starting New)

```
READ standards → CREATE project → CREATE project-specific docs → REFERENCE standards
```

1. **Read** the standards in `0-Setup/`
2. AI creates project folder, GAS project, GitHub repo
3. AI creates project-specific `Docs/` that **reference** (not copy) standards
4. **JDM does first-time GAS auth** via Editor UI (one-time manual step)
5. AI deploys and continues

### Workflow B: Development (Learning Something New)

```
Working on project → Hit a gotcha → UPDATE standards → PUSH → Continue project
```

**"Shit, we forgot that. Document. Keep moving."**

```bash
cd /Users/joshd.millang/Projects/RPI-Standards
git add -A && git commit -m "docs: [what you learned]" && git push
cd /Users/joshd.millang/Projects/[PROJECT_NAME]  # Continue working
```

---

## 🔗 Referencing from Projects

In each project's `Docs/1-AGENT_BRIEFING.md`, add:

```markdown
## Standards Reference

Universal standards live in `RPI-Standards/` (not in this project):

| Folder | Purpose |
|--------|---------|
| `0-Setup/` | Agent frameworks, project kickoff, design system |
| `1-Manage/` | Weekly audits, documentation cleanup |
| `2-Production/` | Pre-launch checks, user documentation |

**Location**: `/Users/joshd.millang/Projects/RPI-Standards/`  
**GitHub**: https://github.com/retirementprotectors/RPI-Standards
```

---

## ⚠️ DO NOT

- ❌ Copy these files into project repos
- ❌ Create project-specific versions of universal standards
- ❌ Forget to push updates here after learning something new

## ✅ DO

- ✅ Reference these docs from project briefings
- ✅ Update these docs when you learn something universal
- ✅ Keep project-specific scope docs in project's `Docs/` folder
- ✅ Run weekly health checks

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | Jan 25, 2026 | Reorganized into `0-Setup/`, `1-Manage/`, `2-Production/` folders. Added WEEKLY_HEALTH_CHECK and PRE_LAUNCH_CHECKLIST. Consolidated Global_Project_Docs. |
| v1.0 | Jan 2026 | Initial structure with `+0-`, `+1-`, `+2-` prefix naming |
