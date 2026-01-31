# RPI Project Plans Index

Central reference for all project plans across the RPI ecosystem.

**Location:** `/Users/joshd.millang/Projects/_RPI_STANDARDS/3-Reference/Plans/`  
**Last Updated:** 2026-01-26

---

## ⚠️ Master Architecture (Jan 26, 2026)

**The master platform architecture is now defined in:**

`0-Setup/THREE_PLATFORM_ARCHITECTURE.md`

This document defines:
- Three platforms: **SENTINEL** (B2B), **RIIMO** (B2E), **PRODASH** (B2C)
- Three MATRIXes: SENTINEL_MATRIX, RAPID_MATRIX, PRODASH_MATRIX
- Channel definitions: RPI, DAVID, RAPID
- SuperProject folder structure
- Pipeline stages per platform
- Implementation roadmap

Plans in this folder are implementation-specific and reference the master architecture.

---

## Quick Reference (12 Plans)

| Plan | Status | Purpose |
|------|--------|---------|
| [commission_intelligence_integration_c4f29eee](commission_intelligence_integration_c4f29eee.plan.md) | Partial | Commission Intelligence MCP + 4-channel context (see THREE_PLATFORM for master arch) |
| [commission_intelligence_status_a793145c](commission_intelligence_status_a793145c.plan.md) | Completed | Current state snapshot (573 rows, 15 tools) |
| [cam_platform_build_e9d007ab](cam_platform_build_e9d007ab.plan.md) | Completed | CAM current state |
| [cam_comp_grid_build_b10bb6d3](cam_comp_grid_build_b10bb6d3.plan.md) | **Pending** | Next CAM phase - Comp Grid engine |
| [david-hub_build_2346e99e](david-hub_build_2346e99e.plan.md) | Pending | Qualification flow + calculators |
| [mcp_setup_+_cam_testing_813d2e93](mcp_setup_+_cam_testing_813d2e93.plan.md) | In Progress | MCP config + CAM testing |
| [mcp_standards_documentation_f714bec3](mcp_standards_documentation_f714bec3.plan.md) | Completed | MCP setup docs for RPI-Standards |
| [midwest_medigap_document_inventory_c4276db6](midwest_medigap_document_inventory_c4276db6.plan.md) | Completed | Carrier document inventory (45 files) |
| [rpi_docs_site_build_fece2811](rpi_docs_site_build_fece2811.plan.md) | Pending | MkDocs documentation site |
| [rpi_command_center_strategic_docs_7a8568f2](rpi_command_center_strategic_docs_7a8568f2.plan.md) | Completed | Strategic docs + Unlocks system |
| [meeting_analysis_template_5cb38b0e](meeting_analysis_template_5cb38b0e.plan.md) | Completed | Claude.ai meeting analysis template |

---

## By Category

### Commission Intelligence
| Plan | Summary |
|------|---------|
| [commission_intelligence_integration_c4f29eee](commission_intelligence_integration_c4f29eee.plan.md) | **Master doc** - 4-channel architecture (B2C/B2B/B2E/B2I), tech stacks, MDJ instances, build sequence, app integration reference |
| [commission_intelligence_status_a793145c](commission_intelligence_status_a793145c.plan.md) | Status snapshot - 573 MATRIX rows, 15 MCP tools, ecosystem diagram |

### CAM
| Plan | Summary |
|------|---------|
| [cam_platform_build_e9d007ab](cam_platform_build_e9d007ab.plan.md) | Current state - Shell committed, Comp Grid UI built |
| [cam_comp_grid_build_b10bb6d3](cam_comp_grid_build_b10bb6d3.plan.md) | **Next phase** - RAPID integration, tier systems, calculator engine |

### DAVID-HUB
| Plan | Summary |
|------|---------|
| [david-hub_build_2346e99e](david-hub_build_2346e99e.plan.md) | Qualification flow + MEC/PRP/SPH calculator modules |

### Infrastructure
| Plan | Summary |
|------|---------|
| [mcp_setup_+_cam_testing_813d2e93](mcp_setup_+_cam_testing_813d2e93.plan.md) | GDrive/Slack MCP config, CAM UI/UX testing |
| [mcp_standards_documentation_f714bec3](mcp_standards_documentation_f714bec3.plan.md) | MCP setup docs + quick reference cards |
| [rpi_docs_site_build_fece2811](rpi_docs_site_build_fece2811.plan.md) | MkDocs Material documentation site |
| [rpi_command_center_strategic_docs_7a8568f2](rpi_command_center_strategic_docs_7a8568f2.plan.md) | Strategic/ and Unlocks/ folders |
| [meeting_analysis_template_5cb38b0e](meeting_analysis_template_5cb38b0e.plan.md) | Standard meeting analysis output format |

### Data Analysis
| Plan | Summary |
|------|---------|
| [midwest_medigap_document_inventory_c4276db6](midwest_medigap_document_inventory_c4276db6.plan.md) | 45-file carrier inventory for commission reconciliation |

---

## Files in This Folder

```
Plans/
├── PLAN_INDEX.md                                    # This file
├── cam_comp_grid_build_b10bb6d3.plan.md             # Pending - Next CAM phase
├── cam_platform_build_e9d007ab.plan.md              # Completed - CAM current state
├── commission_intelligence_integration_c4f29eee.plan.md # Master architecture doc
├── commission_intelligence_status_a793145c.plan.md  # Completed - Status snapshot
├── david-hub_build_2346e99e.plan.md                 # Pending
├── mcp_setup_+_cam_testing_813d2e93.plan.md         # In Progress
├── mcp_standards_documentation_f714bec3.plan.md     # Completed - MCP docs
├── meeting_analysis_template_5cb38b0e.plan.md       # Completed
├── midwest_medigap_document_inventory_c4276db6.plan.md # Completed - Carrier inventory
├── rpi_command_center_strategic_docs_7a8568f2.plan.md # Completed
└── rpi_docs_site_build_fece2811.plan.md             # Pending
```

---

## Consolidation Log

**2026-01-25**: Deleted duplicate plan
- `mcp_standards_documentation_5b1c00eb` - Early version deleted, keeping completed `f714bec3`

**2026-01-25**: Rescued 3 plans from hidden `~/.cursor/plans/`
- `midwest_medigap_document_inventory_c4276db6` - Carrier document inventory
- `mcp_standards_documentation_f714bec3` - MCP setup (completed version)
- `mcp_standards_documentation_5b1c00eb` - MCP setup (early version) - **DELETED**

**2026-01-25**: Consolidated from 15 → 10 files

**Merged into `commission_intelligence_integration_c4f29eee`:**
- `commission_intelligence_mcp_1c976f04` (early design, superseded)
- `commission_ecosystem_integration_1f2bc361` (app integration details)
- `agent_commission_lookup_mcp_29d37975` (refactor complete)

**Removed:**
- `cam_full_setup_bdba33d6` (superseded by `cam_platform_build`)
- `notion_knowledge_base_migration_83dac260` (competing approach to MkDocs)

---

## Related Resources

| Resource | Location |
|----------|----------|
| RPI-Standards | `/Users/joshd.millang/Projects/_RPI_STANDARDS/` |
| Three-Platform Architecture | `0-Setup/THREE_PLATFORM_ARCHITECTURE.md` |
| MCP-Hub | `/Users/joshd.millang/Projects/MCP-Hub/` |
| Commission Intelligence MCP | `MCP-Hub/commission-intelligence/` |
| Healthcare MCPs | `MCP-Hub/healthcare-mcps/` |
| Implementation Plan | `~/.cursor/plans/three-matrix_database_architecture_6ff65db7.plan.md` |
