---
name: Commission Intelligence MCP
overview: Build a Commission Intelligence MCP server that provides stateless calculation tools for commission level detection, rate lookups, and partnership value analysis - callable from Cursor AI, SENTINEL, and any MCP-capable application.
todos:
  - id: scaffold-mcp
    content: Create commission-mcp directory structure with MCP server boilerplate
    status: pending
  - id: migrate-detect
    content: Migrate commission_intelligence.py detection logic into MCP tool format
    status: pending
  - id: migrate-partnership
    content: Migrate partnership_calculator.py into MCP tool with house levels config
    status: pending
  - id: rate-data
    content: Structure Aetna and Mutual rate data as JSON for MCP consumption
    status: pending
  - id: test-cursor
    content: Test MCP tools from Cursor to verify they work for ad-hoc analysis
    status: pending
  - id: rest-wrapper
    content: Add REST API wrapper for GAS compatibility (SENTINEL integration)
    status: pending
  - id: update-sentinel
    content: Update SENTINEL_MedSupp.gs to call MCP instead of hardcoded rates
    status: pending
isProject: false
---

# Commission Intelligence MCP Architecture

## The Architecture Decision

Based on analysis of:
- [_RPI_STANDARDS/+0- RPI_PLATFORM_BLUEPRINT.md](../_RPI_STANDARDS/+0-RPI_PLATFORM_BLUEPRINT.md) - Layer 3 is "Applications / Business Logic"
- [sentinel/SENTINEL_Matrix.gs](../sentinel/SENTINEL_Matrix.gs) - Current comp grid storage pattern
- [sentinel/SENTINEL_MedSupp.gs](../sentinel/SENTINEL_MedSupp.gs) - Existing hardcoded rate tables

**Recommendation: Commission Intelligence as MCP (Middleware)**

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONSUMPTION LAYER                           │
│  Cursor AI  │  SENTINEL UI  │  PRODASH  │  Future Apps          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ MCP Protocol
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              COMMISSION INTELLIGENCE MCP                         │
│                                                                  │
│  Tools:                                                          │
│  ├── detect_commission_level                                     │
│  │   Input: carrier, state, plan, age, policy_year, actual_rate  │
│  │   Output: detected_level, confidence, full_rate_matrix        │
│  │                                                               │
│  ├── get_house_rates                                             │
│  │   Input: carrier                                              │
│  │   Output: our_contracted_rates, source (Spark, Direct, etc.)  │
│  │                                                               │
│  ├── calculate_partnership_value                                 │
│  │   Input: clients, avg_premium, their_rate, carrier            │
│  │   Output: commission_share, psm_revenue, retention_value...   │
│  │                                                               │
│  ├── project_revenue                                             │
│  │   Input: bob_summary, retention_rate, years                   │
│  │   Output: year_by_year_projection, lifetime_value             │
│  │                                                               │
│  └── compare_levels                                              │
│      Input: their_level, house_level, premium                    │
│      Output: rate_uplift, dollar_difference, partner_benefit     │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ Reads (optional, for rate updates)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    THE MATRIX (Data Layer)                       │
│                                                                  │
│  Google Sheets:                                                  │
│  ├── _MEDSUP_COMP_GRID (raw rate tables)                         │
│  ├── _MAPD_COMP_GRID                                             │
│  ├── _CARRIER_MASTER                                             │
│  ├── _IMO_MASTER                                                 │
│  └── _AGENT_MASTER (including contract levels)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why MCP (Not Matrix or SENTINEL Embedded)

| Approach | Pros | Cons |
|----------|------|------|
| **Embedded in Matrix** | Close to data | GAS limitations, not callable from AI, hard to test |
| **Embedded in SENTINEL** | Single deploy | Locked to one app, can't use from Cursor |
| **MCP Server** | Universal access, testable, versionable, AI-callable | Requires server setup |

**Winner: MCP** because:
1. Cursor AI can call it for ad-hoc analysis (like Matt's BoB)
2. SENTINEL can call it for structured analysis
3. Pure Python = powerful, testable, maintainable
4. Rate tables can be embedded OR pulled from Matrix via Google Sheets MCP

---

## Implementation Structure

Location: `/Users/joshd.millang/Projects/MCP-Hub/commission-mcp/`

```
commission-mcp/
├── src/
│   ├── server.py              # MCP server entry point
│   ├── tools/
│   │   ├── detect_level.py    # Level detection from transaction
│   │   ├── rate_lookup.py     # Rate matrix lookups
│   │   ├── partnership.py     # Partnership value calculator
│   │   └── projections.py     # Revenue projections
│   └── data/
│       ├── aetna_rates.json   # Aetna level → rate matrices
│       ├── mutual_rates.json  # Mutual rate schedules
│       ├── house_levels.json  # DAVID+RPI contracted levels
│       └── carriers.json      # Carrier normalization
├── tests/
│   └── test_*.py
├── pyproject.toml
└── README.md
```

---

## MCP Tool Specifications

### 1. `detect_commission_level`

```python
# Input
{
    "carrier": "aetna",
    "state": "IA",
    "plan": "G",
    "age_band": "65-80",
    "policy_year": 1,
    "actual_rate": 18.0
}

# Output
{
    "detected_level": "04",
    "level_name": "BRKPRDXX2_04",
    "confidence": 0.95,
    "rate_matrix": {
        "national": {"G": {"65-80": {"y1-6": 18.0, "y7+": 1.7}}},
        "state_adjustments": {...}
    }
}
```

### 2. `calculate_partnership_value`

```python
# Input
{
    "medsup_clients": 500,
    "avg_premium": 3000,
    "their_commission_rate": 22.0,
    "carrier": "aetna",
    "current_retention": 0.50
}

# Output
{
    "their_current": {"commission": 330000, "net_after_ops": 181500},
    "partnership": {
        "commission_share": 126000,
        "psm_revenue": 225000,
        "retention_value": 31500,
        "ops_savings": 118800,
        "total": 501300
    },
    "rate_uplift": {
        "street_rate": 22.0,
        "house_rate": 28.0,
        "uplift_value": 27000
    },
    "improvement": {"dollar": 319800, "multiple": 2.76}
}
```

---

## Integration with SENTINEL

Two options:

**Option A: Direct MCP Call (if SENTINEL moves to Node.js)**
```javascript
const result = await mcp.call('commission-intelligence', 'detect_commission_level', {...});
```

**Option B: REST API Wrapper (for GAS compatibility)**
- Deploy MCP with HTTP endpoint
- SENTINEL calls via `UrlFetchApp.fetch()`

```javascript
// In SENTINEL_Commission.gs
function detectCommissionLevel(carrier, state, plan, rate) {
  const response = UrlFetchApp.fetch('https://commission-mcp.rpi.com/detect', {
    method: 'POST',
    payload: JSON.stringify({carrier, state, plan, rate})
  });
  return JSON.parse(response.getContentText());
}
```

---

## Data Flow for Analysis Reports

```
1. User uploads BoB CSV to SENTINEL
   ↓
2. SENTINEL normalizes data, stores in deal spreadsheet
   ↓
3. SENTINEL calls Commission MCP:
   - detect_commission_level (for each carrier in book)
   - calculate_partnership_value (aggregate)
   ↓
4. MCP returns analysis with:
   - Their current levels
   - House levels (through Spark)
   - Rate uplift value
   - Full partnership ROI
   ↓
5. SENTINEL displays in Executive Summary
```

---

## House Levels Configuration

Stored in MCP (easy to update when contracts change):

```json
// house_levels.json
{
  "aetna": {
    "level": "12",
    "base_rate": 28.0,
    "source": "Spark",
    "effective_date": "2026-01-01"
  },
  "mutual": {
    "level": "100% National",
    "base_rate": 26.0,
    "source": "Direct"
  },
  "cigna": {
    "level": "TBD",
    "base_rate": 24.0,
    "source": "Spark"
  }
}
```

---

## Migration Path

### Phase 1: Build MCP (This Sprint)
- Convert Python tools to MCP server
- Test with Cursor
- Document all tools

### Phase 2: SENTINEL Integration
- Add REST wrapper if needed
- Replace hardcoded `MEDSUP_RATES` in `SENTINEL_MedSupp.gs` with MCP calls
- Update analysis modules to use MCP

### Phase 3: Matrix Sync (Optional)
- MCP can optionally read from `_MEDSUP_COMP_GRID` in Matrix
- Or keep rates embedded in MCP for simplicity
- Decision: embedded is simpler, Matrix is more maintainable long-term

---

## Key Files to Modify

**New (MCP-Hub):**
- `commission-mcp/src/server.py` - MCP server
- `commission-mcp/src/tools/*.py` - Tool implementations

**Existing (MCP-Hub) - Refactor into MCP:**
- `data/analysis_tools/commission_intelligence.py` → `commission-mcp/src/tools/detect_level.py`
- `data/analysis_tools/partnership_calculator.py` → `commission-mcp/src/tools/partnership.py`

**Existing (SENTINEL) - After MCP ready:**
- `SENTINEL_MedSupp.gs` - Replace `MEDSUP_RATES` with MCP calls
- `SENTINEL_AgencySetup.gs` - Use MCP for rate lookups
