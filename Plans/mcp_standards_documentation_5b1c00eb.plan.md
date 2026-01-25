---
name: MCP Standards Documentation
overview: Add MCP server setup documentation to RPI-Standards so all agents and projects have visibility to available AI tools and can set them up on any machine.
todos:
  - id: create-mcp-standards-doc
    content: Create +0- MCP_TOOLS_SETUP.md in RPI-Standards with full documentation
    status: pending
  - id: create-setup-script
    content: Create setup.sh in RPI-MCP-Servers for portable Cursor config
    status: pending
  - id: update-master-framework
    content: Add MCP reference to MASTER_AGENT_FRAMEWORK.md appendix
    status: pending
---

# Add MCP Tools Documentation to RPI-Standards

## Overview

Create a new standards document in `RPI-Standards/` that documents the MCP servers, how to set them up, and what tools are available. This ensures any agent starting on any project knows about and can use the healthcare MCP tools.

## Architecture

```mermaid
flowchart TD
    subgraph Standards ["RPI-Standards (Git Repo)"]
        MasterFramework["+0- MASTER_AGENT_FRAMEWORK.md"]
        MCPSetup["+0- MCP_TOOLS_SETUP.md (NEW)"]
        UIGuidelines["+0- UI_DESIGN_GUIDELINES.md"]
    end
    
    subgraph MCPRepo ["RPI-MCP-Servers (Git Repo)"]
        NPIServer["npi-registry.js"]
        ICD10Server["icd10-codes.js"]
        CMSServer["cms-coverage.js"]
        SetupScript["setup.sh (NEW)"]
    end
    
    subgraph Projects ["Any RPI Project"]
        Briefing["1-AGENT_BRIEFING.md"]
    end
    
    Briefing -->|references| Standards
    MCPSetup -->|documents| MCPRepo
    SetupScript -->|configures| CursorConfig["~/.cursor/mcp.json"]
```

## Changes

### 1. Create MCP Standards Document

**File:** [`RPI-Standards/+0- MCP_TOOLS_SETUP.md`](RPI-Standards/+0- MCP_TOOLS_SETUP.md)

Contents:
- What MCP is (brief explanation)
- Available RPI MCP servers (NPI, ICD-10, CMS Coverage)
- Setup instructions (clone, npm install, run setup script)
- Tool reference table (what each tool does)
- Example queries
- Troubleshooting

### 2. Add Setup Script to MCP Repo

**File:** [`RPI-MCP-Servers/setup.sh`](RPI-MCP-Servers/setup.sh)

A simple bash script that:
- Detects the current repo path
- Updates `~/.cursor/mcp.json` with correct absolute paths
- Preserves existing MCP server configs (like figma-desktop)
- Works on any machine after cloning

### 3. Update Master Framework (Optional)

**File:** [`RPI-Standards/+0- MASTER_AGENT_FRAMEWORK.md`](RPI-Standards/+0- MASTER_AGENT_FRAMEWORK.md)

Add a brief section in the appendix pointing to the MCP setup doc for agents who need healthcare data access.

## Portability Flow

```
New Machine Setup:
1. Clone RPI-Standards (already part of onboarding)
2. Clone RPI-MCP-Servers
3. cd RPI-MCP-Servers && npm install && ./setup.sh
4. Restart Cursor
5. MCP tools available in all projects
```

## Files Modified/Created

| File | Action |
|------|--------|
| `RPI-Standards/+0- MCP_TOOLS_SETUP.md` | Create |
| `RPI-MCP-Servers/setup.sh` | Create |
| `RPI-Standards/+0- MASTER_AGENT_FRAMEWORK.md` | Update (add reference) |
