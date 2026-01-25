---
name: Agent Commission Lookup MCP
overview: Refactor Commission Intelligence MCP from "detection" model to "configuration + lookup" model where agent commission levels are stored and full rate matrices can be queried by agent/carrier/product/state.
todos:
  - id: create-agents-config
    content: Create agents-config.json with Midwest Medigap configured (Aetna Level 08, Mutual TBD)
    status: completed
  - id: extract-aetna-levels
    content: Extract Aetna Level 08 rate tables from comp grid PDFs or build from known structure
    status: completed
  - id: refactor-mcp-tools
    content: "Replace detection tools with lookup tools: get_agent_rates, configure_agent_level, list_agents"
    status: completed
  - id: test-query
    content: "Test: 'What are Matt's Aetna rates for Plan G in Iowa?'"
    status: completed
isProject: false
---

# Agent Commission Lookup MCP

## Architecture Change

**From**: Detection-based (analyze transaction → guess level)
**To**: Configuration-based (store known levels → lookup rates)

## Data Model

### 1. Agent Configuration (`agents-config.json`)

```json
{
  "midwest_medigap": {
    "name": "Midwest Medigap LLC",
    "principals": ["Matt Mitchell"],
    "levels": {
      "aetna": {
        "type": "named_level",
        "level": "08",
        "level_name": "BRKPRDXX2_08"
      },
      "mutual_of_omaha": {
        "type": "percent_of_national",
        "percentage": 100
      }
    }
  }
}
```

### 2. Carrier Rate Data (existing `commission_data.json`)

Already has national grids for Mutual family carriers.

Need to add: **Aetna Level Rate Tables** (from Aetna comp grids in `/data/Comp Grids/`)

## MCP Tools

### `get_agent_rates`
- **Input**: `agent_id`, `carrier`, optional: `state`, `plan`, `policy_year`
- **Output**: Full rate matrix or specific rate
- **Logic**:
  - Aetna → lookup level table
  - Mutual → national_rate × percentage

### `configure_agent_level`
- **Input**: `agent_id`, `carrier`, `level_config`
- **Output**: Confirmation
- Allows setting/updating agent levels

### `list_agents`
- Returns all configured agents and their levels

### `calculate_commission`
- **Input**: `agent_id`, `carrier`, `premium`, `state`, `plan`, `policy_year`
- **Output**: Commission amount

## Files to Create/Modify

1. `commission-intelligence/data/agents-config.json` - Agent level configurations
2. `commission-intelligence/data/aetna-levels.json` - Aetna level rate tables (from PDFs)
3. `commission-intelligence/src/commission-intelligence.js` - Updated tools

## Immediate Test Case

**Query**: "What are Matt's Aetna rates for Plan G in Iowa?"

**Response**:
```
Matt Mitchell (Midwest Medigap) - Aetna Level 08

Plan G - Iowa:
  Year 1-6: 22%
  Year 7+: 8%

Plan N - Iowa:
  Year 1-6: 22%
  Year 7+: 8%
```

## Data Gap

Need Aetna Level 08 rate tables. Options:
1. Extract from PDFs in `/data/Comp Grids/` (AFLAC, SGA PDFs)
2. Use estimated rates based on known structure
3. User provides a sample rate, we calculate the level multiplier
