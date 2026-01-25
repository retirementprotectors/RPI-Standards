---
name: CAM Full Setup
overview: Create CAM project with full structure, agent documentation for future specialists, and implement the HYPO Calculator as Phase 1 deliverable.
todos:
  - id: project-setup
    content: Create CAM folder structure, appsscript.json, placeholder files
    status: completed
  - id: agent-docs
    content: Create all 7 agent documentation files in Docs/ folder
    status: completed
  - id: core-backend
    content: Build Code.gs (routing), CAM_Config.gs (tiers, averages), CAM_Utils.gs
    status: completed
  - id: hypo-engine
    content: Build CAM_HYPO.gs with 3-year projection calculations
    status: completed
  - id: frontend-ui
    content: Build Index.html (slider UI), Styles.html (RPI design system)
    status: completed
  - id: api-layer
    content: Build CAM_API.gs with endpoints for SENTINEL integration
    status: completed
---

# CAM - Commission Accounting Masheen (Full Setup)

## Overview

Create CAM as a complete GAS Web App with:
1. Full project structure (all core files)
2. Agent documentation (for parallel development in future phases)
3. Working HYPO Calculator (Phase 1 deliverable)

---

## Project Structure

```
/Users/joshd.millang/Projects/CAM/
├── .clasp.json
├── appsscript.json
│
├── Code.gs                 # Entry point, routing
├── CAM_Config.gs           # Constants, RPI averages, commission tiers
├── CAM_Database.gs         # MATRIX operations
├── CAM_Utils.gs            # Shared utilities
├── CAM_HYPO.gs             # HYPO calculation engine
├── CAM_API.gs              # External API endpoints
│
├── Index.html              # Main shell + HYPO UI
├── Styles.html             # RPI Design System (CSS)
├── Scripts.html            # Shared JavaScript utilities
│
└── Docs/
    ├── 1-AGENT_BRIEFING.md
    ├── 2.1-AGENT_SCOPE_GENERAL.md
    ├── 2.2-AGENT_SCOPE_OPS.md
    ├── 3.1-AGENT_SCOPE_SPC1_BACKEND.md
    ├── 3.2-AGENT_SCOPE_SPC2_DATABASE.md
    ├── 3.3-AGENT_SCOPE_SPC3_FRONTEND.md
    └── 3.4-AGENT_SCOPE_SPC4_API.md
```

---

## Agent Documentation Structure

| Doc | Purpose |
|-----|---------|
| `1-AGENT_BRIEFING.md` | Universal context for all agents (project overview, rules, schema) |
| `2.1-AGENT_SCOPE_GENERAL.md` | GA role - coordination, delegation |
| `2.2-AGENT_SCOPE_OPS.md` | OPS role - validation, deployment |
| `3.1-SPC1_BACKEND.md` | Backend specialist - CAM_HYPO.gs, CAM_Config.gs |
| `3.2-SPC2_DATABASE.md` | Database specialist - CAM_Database.gs, MATRIX |
| `3.3-SPC3_FRONTEND.md` | Frontend specialist - Index.html, Styles.html |
| `3.4-SPC4_API.md` | API specialist - CAM_API.gs, Code.gs routing |

---

## HYPO Calculator Specification

**User Inputs (Sliders):**
- Retail: Sales Velocity
- Wholesale: Agency Count, Avg Clients, Sales Velocity
- Network: Referral Count, Avg Clients, Sales Velocity

**Backend Config:**
- Commission Tiers (Partner %, Override %)
- Gross Revenue per Client
- Cash Flow Timeline (TAT)

**Output:**
- 3-Year / 12-Quarter projection
- Retail / Wholesale / Network / Total breakdown
- PDF Export, Detailed Report, Data Audit CTAs

---

## Implementation Order

1. **Project Setup** - Create folder, initialize files, appsscript.json
2. **Agent Docs** - Create all 7 documentation files
3. **Core Backend** - Code.gs, CAM_Config.gs, CAM_Utils.gs
4. **HYPO Engine** - CAM_HYPO.gs with calculation logic
5. **Frontend** - Index.html with slider UI, Styles.html with RPI design
6. **API Layer** - CAM_API.gs for future SENTINEL integration
7. **Testing** - Verify calculations, UI responsiveness