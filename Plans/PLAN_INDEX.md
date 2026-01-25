# RPI Project Plans Index

Central reference for all project plans across the RPI ecosystem.

**Location:** `/Users/joshd.millang/Projects/RPI-Standards/Plans/`  
**Last Updated:** 2026-01-25

---

## Quick Reference

| Plan | Status | Purpose |
|------|--------|---------|
| [commission_intelligence_integration_c4f29eee](commission_intelligence_integration_c4f29eee.plan.md) | Partial | **Master architecture** - 4-channel empire |
| [cam_comp_grid_build_b10bb6d3](cam_comp_grid_build_b10bb6d3.plan.md) | Pending | **Next CAM phase** - Comp Grid engine |
| [david-hub_build_2346e99e](david-hub_build_2346e99e.plan.md) | Pending | Qualification flow + calculators |
| [mcp_setup_+_cam_testing_813d2e93](mcp_setup_+_cam_testing_813d2e93.plan.md) | In Progress | MCP config + CAM testing |

---

## Completed Plans (Reference)

These plans have been executed. Keep for historical reference and context.

### Commission Intelligence System
| Plan | Summary |
|------|---------|
| [commission_intelligence_status_a793145c](commission_intelligence_status_a793145c.plan.md) | **Current state snapshot** - 573 MATRIX rows, 15 MCP tools, ecosystem diagram |
| [commission_ecosystem_integration_1f2bc361](commission_ecosystem_integration_1f2bc361.plan.md) | CAM/SENTINEL/DAVID-HUB/RAPID integration analysis, MAPD logic |
| [agent_commission_lookup_mcp_29d37975](agent_commission_lookup_mcp_29d37975.plan.md) | Refactored from detection to configuration+lookup model |
| [commission_intelligence_mcp_1c976f04](commission_intelligence_mcp_1c976f04.plan.md) | Original MCP architecture design |

### CAM (Commission Accounting Masheen)
| Plan | Summary |
|------|---------|
| [cam_full_setup_bdba33d6](cam_full_setup_bdba33d6.plan.md) | Full project structure, 7 agent docs, HYPO engine |
| [cam_platform_build_e9d007ab](cam_platform_build_e9d007ab.plan.md) | Shell committed, CSS aligned, Comp Grid backend/UI |

### RPI Infrastructure
| Plan | Summary |
|------|---------|
| [rpi_command_center_strategic_docs_7a8568f2](rpi_command_center_strategic_docs_7a8568f2.plan.md) | Strategic/ and Unlocks/ folders, Vision Briefing converted |
| [meeting_analysis_template_5cb38b0e](meeting_analysis_template_5cb38b0e.plan.md) | Standard Claude.ai meeting analysis output template |

---

## Active Plans (In Progress / Pending)

### High Priority
| Plan | Status | Next Action |
|------|--------|-------------|
| [cam_comp_grid_build_b10bb6d3](cam_comp_grid_build_b10bb6d3.plan.md) | Pending | Implement commission calculation engine with RAPID integration |
| [mcp_setup_+_cam_testing_813d2e93](mcp_setup_+_cam_testing_813d2e93.plan.md) | In Progress | Complete CAM UI/UX testing |

### Medium Priority
| Plan | Status | Next Action |
|------|--------|-------------|
| [david-hub_build_2346e99e](david-hub_build_2346e99e.plan.md) | Pending | Build qualification flow + MEC/PRP/SPH calculators |
| [rpi_docs_site_build_fece2811](rpi_docs_site_build_fece2811.plan.md) | Pending | Set up MkDocs Material documentation site |

### Review Needed
| Plan | Status | Notes |
|------|--------|-------|
| [notion_knowledge_base_migration_83dac260](notion_knowledge_base_migration_83dac260.plan.md) | Pending | May be obsolete if using MkDocs approach |

---

## Files in This Folder

```
Plans/
├── PLAN_INDEX.md                                    # This file
├── agent_commission_lookup_mcp_29d37975.plan.md     # Completed
├── cam_comp_grid_build_b10bb6d3.plan.md             # Pending - Next CAM phase
├── cam_full_setup_bdba33d6.plan.md                  # Completed
├── cam_platform_build_e9d007ab.plan.md              # Completed
├── commission_ecosystem_integration_1f2bc361.plan.md # Completed
├── commission_intelligence_integration_c4f29eee.plan.md # Partial - Master architecture
├── commission_intelligence_mcp_1c976f04.plan.md     # Completed (reference)
├── commission_intelligence_status_a793145c.plan.md  # Completed - Status snapshot
├── david-hub_build_2346e99e.plan.md                 # Pending
├── mcp_setup_+_cam_testing_813d2e93.plan.md         # In Progress
├── meeting_analysis_template_5cb38b0e.plan.md       # Completed
├── notion_knowledge_base_migration_83dac260.plan.md # Review needed
├── rpi_command_center_strategic_docs_7a8568f2.plan.md # Completed
└── rpi_docs_site_build_fece2811.plan.md             # Pending
```

---

## Plan File Naming Convention

```
{project}_{feature}_{hash}.plan.md
```

- **project**: cam, commission, david, rpi, mcp, etc.
- **feature**: brief description with underscores
- **hash**: 8-character unique identifier (from Cursor)

---

## Related Resources

| Resource | Location |
|----------|----------|
| RPI-Standards | `/Users/joshd.millang/Projects/RPI-Standards/` |
| MCP-Hub | `/Users/joshd.millang/Projects/MCP-Hub/` |
| Commission Intelligence MCP | `MCP-Hub/commission-intelligence/` |
| Healthcare MCPs | `MCP-Hub/healthcare-mcps/` |
| MATRIX | Google Sheets (source of truth for data) |

---

## Cleanup Log

**2026-01-25**: Initial organization
- Consolidated 31 plan files from Desktop/Trash
- Deleted 16 duplicates (timestamped copies, identical content, superseded versions)
- Moved 15 canonical plans to `RPI-Standards/Plans/`
- Created this index
