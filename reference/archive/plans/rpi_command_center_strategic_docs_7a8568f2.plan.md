---
name: RPI Command Center Strategic Docs
overview: Expand RPI-Command-Center to include company-wide Strategic documents and an Unlocks system for capturing major milestones, integrating the Complete Vision Briefing as the first strategic living document.
todos:
  - id: create-strategic-folder
    content: Create Docs/Strategic/ folder structure
    status: completed
  - id: create-unlocks-folder
    content: Create Docs/Unlocks/ folder with first unlock
    status: completed
  - id: create-templates
    content: Create Strategic and Unlock templates
    status: completed
  - id: convert-vision
    content: Convert Vision Briefing PDF to Complete_Vision_LIVE.md
    status: completed
  - id: update-readme
    content: Update RPI-Command-Center README with new document types
    status: completed
isProject: false
---

# Expand RPI-Command-Center for Strategic Living Documents

## Current State

RPI-Command-Center currently handles:

- **Meeting-Analyses/** - Point-in-time meeting records
- **Roadmaps/** - Per-person LIVE documents (Matt, Nikki, Vinnie, Jason, Aprille)
- **Templates/** - Standard formats for meeting analysis

**Gap:** No place for company-wide strategic documents or milestone tracking.

---

## Proposed Structure

```
RPI-Command-Center/
├── Docs/
│   ├── Meeting-Analyses/              # (existing)
│   ├── Roadmaps/                      # (existing) - Per-person
│   ├── Strategic/                     # NEW - Company-wide vision docs
│   │   ├── Complete_Vision_LIVE.md
│   │   ├── Data_Tech_Advantage_LIVE.md
│   │   ├── Proactive_Service_Model_LIVE.md
│   │   ├── Four_Channel_Empire_LIVE.md
│   │   └── Carrier_Partnerships_LIVE.md
│   ├── Unlocks/                       # NEW - Major milestones
│   │   └── [YYYY-MM]_[Unlock_Name].md
│   └── Templates/
│       ├── RPI_Meeting_Analysis_Template.md    # (existing)
│       ├── RPI_Strategic_Document_Template.md  # NEW
│       └── RPI_Unlock_Template.md              # NEW
└── README.md                          # Updated with new sections
```

---

## Strategic Documents (from Vision Briefing)

The Complete Vision Briefing breaks into these living documents:

| Document | Source Sections | Purpose |

|----------|-----------------|---------|

| `Complete_Vision_LIVE.md` | Full briefing | Master strategic vision |

| `Data_Tech_Advantage_LIVE.md` | Part III | BlueButton, EHR, Avatar filter |

| `Proactive_Service_Model_LIVE.md` | Part IV | Provider guidance, health outcomes |

| `Four_Channel_Empire_LIVE.md` | Part VII | B2C, B2B, B2E, B2I structure |

| `Carrier_Partnerships_LIVE.md` | Part V, IX | BFL, North American, deal status |

Each document:

- Has a CHANGELOG at top for tracking updates
- Links to related Unlocks when major progress happens
- Syncs to Google Docs for team access

---

## Unlocks System

**What is an Unlock?** A documented milestone that materially advances the vision.

**Naming:** `[YYYY-MM]_[Unlock_Name].md`

**Examples:**

- `2026-01_Healthcare_MCPs_Built.md` - NPI, ICD-10, CMS Coverage MCPs operational
- `2026-01_BlueButton_Architecture_Defined.md` - Health profile data layer designed
- `2026-02_BFL_Board_Presentation.md` - Carrier partnership milestone
- `2026-03_First_Proprietary_Product.md` - Product ownership achieved

**Unlock documents include:**

- What was unlocked
- How it advances the vision
- What it enables next
- Links to related Strategic docs

---

## Integration with MCPs

The Strategic docs reference MCP-Hub for technical implementation:

```
Strategic Vision (What)          MCP-Hub (How)
─────────────────────           ──────────────
Data + Tech Advantage    →      bluebutton-mcp, health-profile-mcp
Proactive Service        →      npi-registry, cms-coverage
Provider Guidance        →      npi-registry (quality metrics)
Avatar Filtering         →      health-profile-mcp + QUE apps
```

---

## Deliverables

1. **Create `Docs/Strategic/` folder** with initial documents
2. **Create `Docs/Unlocks/` folder** with first unlock (Healthcare MCPs)
3. **Create two new templates:**

   - `RPI_Strategic_Document_Template.md`
   - `RPI_Unlock_Template.md`

4. **Convert Vision Briefing** to `Complete_Vision_LIVE.md`
5. **Update README.md** with new document types

---

## Key Design Decisions

**Q: Keep as one big Vision doc or split into parts?**

Recommend: **Both.** Keep `Complete_Vision_LIVE.md` as the master, but also create focused docs for each major theme. Team members can read the section relevant to them without wading through 19 pages.

**Q: Where do Unlocks link?**

Each Unlock links back to:

- The Strategic doc it advances
- The MCP-Hub component (if technical)
- The person Roadmap (if person-specific)

This creates a connected knowledge graph:

```
Meeting Analysis → Person Roadmap → Strategic Doc → Unlock → MCP-Hub
```