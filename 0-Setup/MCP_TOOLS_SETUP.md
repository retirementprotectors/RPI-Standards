# RPI MCP Tools Setup Guide

> ⚠️ **UPDATED**: MCP setup has moved to MCP-Hub.
> 
> **Go to:** `/Users/joshd.millang/Projects/MCP-Hub/`

---

## Single Source of Truth

MCP-Hub is now the canonical source for all MCP documentation:

| What You Need | Where To Go |
|---------------|-------------|
| Full MCP setup guide | `MCP-Hub/docs/setup-new-machine.md` |
| Current MCP config | `MCP-Hub/mcp.json` |
| Credential locations | `MCP-Hub/docs/credentials.md` |
| Strategic roadmap | `MCP-Hub/docs/roadmap.md` |
| Healthcare MCPs | `MCP-Hub/healthcare-mcps/` |

---

## Available MCPs (Quick Reference)

### Integration MCPs
| MCP | Purpose |
|-----|---------|
| `gdrive` | Google Drive access |
| `gmail` | Email read/send |
| `google-calendar` | Calendar events |
| `slack` | Slack messaging |
| `playwright` | Browser automation |

### Healthcare MCPs (RPI-Built)
| MCP | Purpose | API |
|-----|---------|-----|
| `npi-registry` | Provider lookup | CMS NPPES (free) |
| `icd10-codes` | Diagnosis/procedure codes | NIH Clinical Tables (free) |
| `cms-coverage` | Medicare coverage info | Embedded reference data |

### Workflow MCPs (RPI-Built)
| MCP | Purpose |
|-----|---------|
| `rpi-meeting-processor` | Process meeting transcripts, route updates to LIVE docs |

---

## For Project Briefings

Include this in agent briefings:

```markdown
## MCP Tools Available

MCP Hub: `/Users/joshd.millang/Projects/MCP-Hub/`

Active tools:
- Google Drive, Gmail, Calendar, Slack, Playwright (integration)
- NPI Registry, ICD-10 Codes, CMS Coverage (healthcare)
- RPI Meeting Processor (workflow)

Setup: See MCP-Hub/docs/setup-new-machine.md
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | Jan 22, 2026 | Redirected to MCP-Hub |
| v1.0 | Jan 13, 2026 | Initial setup guide |

---

*For detailed documentation, see MCP-Hub.*
