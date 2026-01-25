# RPI MCP Tools Setup Guide

> **Version**: v1.0  
> **Created**: January 13, 2026  
> **Scope**: Universal - Available to ALL RPI Projects  
> **Repo**: `RPI-MCP-Servers`

---

## What is MCP?

**MCP (Model Context Protocol)** gives AI agents direct access to external tools and data during development sessions. Instead of you looking up information and pasting it into chat, agents can query data sources directly.

**Without MCP:**
```
You: "What's the NPI for Dr. Smith?"
Agent: "I don't have access to the NPI registry. Please look it up and paste it here."
You: *goes to website, searches, copies data*
```

**With MCP:**
```
You: "What's the NPI for Dr. Smith in Phoenix?"
Agent: *calls search_providers tool*
      "Found: Dr. John Smith, NPI 1234567890, Cardiology, Phoenix AZ..."
```

---

## Available RPI MCP Servers

| Server | Purpose | Data Source |
|--------|---------|-------------|
| **npi-registry** | Healthcare provider lookup | CMS NPPES API |
| **icd10-codes** | Diagnosis/procedure codes | NIH Clinical Tables API |
| **cms-coverage** | Medicare coverage info | CMS reference data |

---

## Setup Instructions

### Prerequisites
- Node.js installed (`node --version` to check)
- Cursor IDE

### One-Time Setup (Per Machine)

```bash
# 1. Clone the repo
cd ~/Projects
git clone https://github.com/retirementprotectors/RPI-MCP-Servers.git

# 2. Install dependencies
cd RPI-MCP-Servers
npm install

# 3. Run setup script (configures Cursor)
./setup.sh

# 4. Restart Cursor
```

### Verify Setup

In Cursor Settings → Tools & MCP, you should see:
- `npi-registry` - Connected
- `icd10-codes` - Connected  
- `cms-coverage` - Connected

---

## Tool Reference

### NPI Registry Tools

| Tool | Description | Example Query |
|------|-------------|---------------|
| `validate_npi` | Check if NPI format is valid | "Is NPI 1234567890 valid?" |
| `lookup_npi` | Get full provider details for an NPI | "Look up NPI 1245319599" |
| `search_providers` | Find providers by name/location/specialty | "Find cardiologists in Phoenix, AZ" |

**Search Parameters:**
- `first_name`, `last_name` - Provider name (wildcards supported: `Smi*`)
- `organization_name` - For NPI-2 (organizations)
- `city`, `state`, `postal_code` - Location filters
- `taxonomy_description` - Specialty (e.g., "Family Medicine", "Cardiology")
- `enumeration_type` - NPI-1 (individual) or NPI-2 (organization)

---

### ICD-10 Code Tools

| Tool | Description | Example Query |
|------|-------------|---------------|
| `search_diagnosis_codes` | Find ICD-10-CM codes | "ICD-10 code for type 2 diabetes" |
| `search_procedure_codes` | Find ICD-10-PCS codes | "ICD-10 code for hip replacement" |
| `lookup_code` | Get description for a code | "What is ICD-10 code E11.9?" |
| `validate_code` | Check if code exists | "Is E11.9 a valid ICD-10 code?" |
| `list_categories` | Show ICD-10-CM chapters | "List ICD-10 categories" |

---

### CMS Coverage Tools

| Tool | Description | Example Query |
|------|-------------|---------------|
| `explain_medicare_parts` | Explain Part A/B/C/D | "What does Medicare Part B cover?" |
| `check_preventive_coverage` | Preventive service coverage | "Does Medicare cover mammograms?" |
| `find_mac_jurisdiction` | Find MAC for a state | "Which MAC handles Arizona claims?" |
| `explain_coverage_types` | Explain NCD/LCD/etc. | "What's the difference between NCD and LCD?" |
| `check_dme_coverage` | DME coverage info | "Is a wheelchair covered by Medicare?" |
| `coverage_search_guidance` | How to search MCD | "How do I find coverage for CGM?" |

---

## When to Use MCP Tools

| Scenario | Tool to Use |
|----------|-------------|
| Building provider lookup feature | `search_providers`, `lookup_npi` |
| Testing with real provider data | `lookup_npi` |
| Need diagnosis code for test data | `search_diagnosis_codes` |
| Verifying code in existing data | `validate_code`, `lookup_code` |
| Medicare coverage questions | `explain_medicare_parts`, `check_dme_coverage` |
| Finding MAC for a region | `find_mac_jurisdiction` |

---

## MCP Quick Reference Card

**Copy this section into project agent briefings:**

```markdown
---

## MCP Tools Available

These tools are available in Cursor via RPI-MCP-Servers. Use them during development.

| Tool | Use When... | Example |
|------|-------------|---------|
| `lookup_npi` | You have a provider NPI to verify | "Look up NPI 1234567890" |
| `search_providers` | Finding providers by name/location | "Find cardiologists in Phoenix, AZ" |
| `validate_npi` | Checking if NPI format is valid | "Is NPI 9876543210 valid?" |
| `search_diagnosis_codes` | Need ICD-10 diagnosis code | "ICD-10 code for type 2 diabetes" |
| `search_procedure_codes` | Need ICD-10 procedure code | "ICD-10 code for hip replacement" |
| `lookup_code` | Have a code, need description | "What is ICD-10 code E11.9?" |
| `explain_medicare_parts` | Medicare coverage questions | "What does Medicare Part B cover?" |
| `check_dme_coverage` | DME coverage questions | "Is a wheelchair covered by Medicare?" |

**Setup:** See `RPI-Standards/0-Setup/MCP_TOOLS_SETUP.md`

---
```

---

## Troubleshooting

### Servers show "Error" in Cursor Settings

1. Check Node.js is installed: `node --version`
2. Check dependencies: `cd ~/Projects/RPI-MCP-Servers && npm install`
3. Re-run setup: `./setup.sh`
4. Restart Cursor completely (not just reload window)

### Tools not appearing in chat

1. Start a **new chat** after setup (existing chats don't reload MCP)
2. Verify servers show "Connected" in Settings → Tools & MCP

### "Command not found" errors

The setup script may need execute permission:
```bash
chmod +x ~/Projects/RPI-MCP-Servers/setup.sh
./setup.sh
```

### Wrong paths after moving repo

Re-run the setup script - it auto-detects the current repo location:
```bash
cd ~/Projects/RPI-MCP-Servers
./setup.sh
```

---

## Adding New MCP Servers

To add additional MCP servers to this repo:

1. Create server file in `src/servers/[name].js`
2. Follow the pattern in existing servers
3. Update `setup.sh` to include the new server
4. Update this documentation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 13, 2026 | Initial release - NPI, ICD-10, CMS Coverage |

---

*For questions or issues, contact the development team.*
