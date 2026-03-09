# ATLAS v1.3: Data OS + MCP Wiring

## Context

ATLAS v1.2 tracks 54 external data sources across 29 carriers. But it has zero visibility into the internal plumbing — the 250+ MCP tools, the Watcher pipeline, 5 launchd agents, GAS triggers, and the end-to-end wire diagrams showing how data flows through The Machine.

JDM's direction: "Getting the Data is what ATLAS is all about, but when we get it — Where does it go? How does it get there? What happens?"

ATLAS is a standalone app that integrates into RIIMO (B2E), PRODASHX (B2C), and SENTINEL (B2B) based on user permissions. All new views live in ATLAS.

---

## What We're Building: 4 New Views + Recurrence Fix

| View | What It Shows |
|------|---------------|
| **Tools** | All 250+ MCP tools: name, server, description, category, which frontends use it |
| **Automation** | Watcher status, 5 launchd agents, GAS triggers — green/yellow/red health |
| **Pipeline** | Visual flow: Source > Intake > Extraction > Approval > MATRIX > Frontend |
| **Wires** | Per product line AND per data domain: complete source-to-UI paths |
| **Recurrence fix** | QUARTERLY: Quarter month + Day. ANNUAL: Month + Day. |

---

## Execution Order (4 sub-phases, each independently deployable)

### Phase 7.0: RAPID_CORE Foundation (prerequisite)

**File:** `~/Projects/RAPID_TOOLS/RAPID_CORE/CORE_Database.gs`

Add 3 entries to `TABLE_ROUTING`:
```
'_TOOL_REGISTRY': 'RAPID',
'_PIPELINE_STATUS': 'RAPID',
'_AUTOMATION_REGISTRY': 'RAPID',
```

Add 3 schemas to `TAB_SCHEMAS`:
```javascript
_TOOL_REGISTRY: [
  'tool_id', 'tool_name', 'source_project', 'source_file',
  'description', 'category', 'tool_type',
  'runnable', 'run_target', 'used_by_frontend',
  'product_lines', 'data_domains',
  'status', 'notes', 'created_at', 'updated_at'
],
// tool_type: FUNCTION (GAS), MCP_TOOL, API_ENDPOINT, LAUNCHD, SCRIPT
// runnable: true/false (can ATLAS trigger it via execute_script?)
// run_target: scriptId + functionName for runnable tools
// source_project: RAPID_IMPORT, RAPID_CORE, RAPID_API, rpi-business, rpi-healthcare, document-processor
_AUTOMATION_REGISTRY: [
  'automation_id', 'automation_name', 'automation_type', 'schedule',
  'script_path', 'last_run_at', 'last_status', 'last_error',
  'heartbeat_source', 'expected_interval_hours', 'owner',
  'status', 'notes', 'created_at', 'updated_at'
],
_PIPELINE_STATUS: [
  'snapshot_id', 'snapshot_at', 'stage', 'queue_name',
  'total_items', 'pending_items', 'processing_items',
  'completed_items', 'error_items', 'avg_processing_seconds',
  'created_at'
],
```

Deploy RAPID_CORE (clasp push, no deploy needed for library). Then create tabs in MATRIX via `SETUP_CreatePhase7Tabs()`.

---

### Phase 7A: Data Tool Registry + Recurrence Fix

**Scope shift:** NOT 250 MCP functions. Instead, ~150 meaningful data pipeline tools organized by capability. This includes RAPID_IMPORT's 269 backend-only FIX_/DEBUG_ functions that the team currently can't access without the GAS editor.

**6 Tool Categories:**
| Category | Source Project | Example Tools |
|----------|---------------|---------------|
| **Intake & Queuing** | RAPID_IMPORT | scanIntakeFolders, scanMeetRecordings, scanMailFolder, scanEmailInboxes |
| **Extraction & Approval** | document-processor | extractDataFromImages, classifyDocumentBoundaries, createApprovalViaApi |
| **Normalization & Validation** | RAPID_CORE + IMPORT | normalizeCarrierName, normalizePhone, validatePhoneAPI, validateEmailAPI, quarterlyHygieneCheck |
| **Matching & Dedup** | RAPID_CORE | matchClient, fuzzyMatch, reconcileClients, mergeRecords, bulkAutoMerge |
| **External Enrichment** | rpi-business MCP | WhitePages person search, commission rate lookup, property lookup |
| **Bulk Operations** | RAPID_IMPORT | FIX_NormalizeClients, FIX_BackfillState, FIX_AutoMergeClients, FIX_BulkValidatePhones |

**New files:**
| File | Purpose |
|------|---------|
| `ATLAS_ToolRegistry.gs` | CRUD for `_TOOL_REGISTRY` tab |
| `ATLAS_ToolSeed.gs` | Seed ~150 tools from RAPID_IMPORT, RAPID_CORE, MCP-Hub |
| `_VIEW_TOOLS.html` | Tool Registry view (search, filter, categorized) |

**ATLAS_ToolRegistry.gs functions:**
- `getToolRegistry(params)` — filter by category, source_project, status, runnable
- `getToolRegistryEntry(toolId)` — single tool detail
- `createToolEntry(data)` / `updateToolEntry(toolId, updates)` — curate after seed
- `getToolRegistryStats()` — counts by category, source project
- `searchTools(query)` — full-text across name + description

**ATLAS_ToolSeed.gs approach:**
Pre-built array of ~150 tools extracted from RAPID_IMPORT (.gs function names), RAPID_CORE (exported functions), and MCP-Hub (tool definitions). `SETUP_SeedToolRegistry()` is idempotent.

**_VIEW_TOOLS.html:**
- Stats row: total tools, per-category counts
- Search bar + filter pills (category, source project, runnable status)
- Grouped by category with collapsible sections
- Each tool: name, source project badge, description, category, runnable flag
- Future: "Run" button for tools marked runnable (via execute_script to RAPID_IMPORT)

**RAPID_IMPORT deprecation note:** RAPID_IMPORT's frontend is NOT deprecated — its approval workflow, reconciliation UI, and comms history viewer have no overlap with ATLAS. What ATLAS replaces is the *need to open the GAS editor* to run FIX_/DEBUG_ data tools. ATLAS becomes the unified catalog; RAPID_IMPORT remains the execution engine.

**Recurrence picker fix (Index.html `updateRecPicker()`):**
- QUARTERLY: "Quarter Month" select (1st/2nd/3rd) + "Day" select (1-28). Store as `Q1-15`.
- ANNUAL: "Month" select (Jan-Dec) + "Day" select (1-28). Store as `M03-15`.
- Update `computeNextDueDate_()` to parse `Q*-*` and `M*-*` formats (backward compatible with plain numbers).

**Router additions (Code.gs):**
- 6 new cases in `handleClientRequest`
- 2 new ForUI wrappers

---

### Phase 7B: Automation Dashboard

**New files:**
| File | Purpose |
|------|---------|
| `ATLAS_Automation.gs` | Status checks for launchd agents, GAS triggers, Watcher |
| `_VIEW_AUTOMATION.html` | Health cards with green/yellow/red indicators |

**ATLAS_Automation.gs functions:**
- `getAutomationStatus()` — reads `_AUTOMATION_REGISTRY`, computes live status by checking heartbeats
- `checkWatcherHeartbeat()` — polls `_INTAKE_QUEUE` for recent entries
- `checkTriggerHeartbeats()` — checks `_SOURCE_HISTORY` for recent AUTO_SYNC entries

**Seed data (8 entries):**
5 launchd agents + 3 ATLAS GAS triggers. Each with schedule, expected_interval_hours, heartbeat_source.

**_VIEW_AUTOMATION.html:**
- Status cards grid: name, type badge, schedule, last run, green/yellow/red dot
- Watcher special card: queue depth from `_INTAKE_QUEUE`
- Refresh button (snapshot-at-load)

---

### Phase 7C: Pipeline Map

**New files:**
| File | Purpose |
|------|---------|
| `ATLAS_Pipeline.gs` | Read `_INTAKE_QUEUE` + `_APPROVAL_QUEUE`, compute flow counts |
| `_VIEW_PIPELINE.html` | Horizontal flow diagram |

**ATLAS_Pipeline.gs functions:**
- `getPipelineSnapshot()` — reads queues, counts by status, returns flow data
- `getPipelineStageDetail(stage)` — drill into a stage
- `savePipelineSnapshot()` — persist to `_PIPELINE_STATUS` for history

**_VIEW_PIPELINE.html:**
- Horizontal flow: CSS flexbox nodes with arrows (no SVG library)
- Each node: stage name, item count, status breakdown, color coded
- Click node = detail table of items in that stage
- Refresh button (snapshot-at-load)

---

### Phase 7D: Wire Diagram

**New files:**
| File | Purpose |
|------|---------|
| `ATLAS_Wires.gs` | Wire definitions as config constants + query functions |
| `_VIEW_WIRES.html` | Wire diagram view with product line / data domain toggle |

**Why config, not MATRIX tab:** Wire definitions reference code artifacts (function names, MATRIX tabs, MCP tools). They change rarely. Git version control > Sheets storage.

**Wire definition structure:**
```javascript
{ wire_id, name, product_line, data_domain,
  stages: [
    { type: 'EXTERNAL|MCP_TOOL|GAS_FUNCTION|API|MATRIX_TAB|FRONTEND',
      name, server?, project?, method? }
  ] }
```

**Initial wires (~10-15):**
Medicare enrollment, commission sync, document intake, client enrichment, validation pipeline, NPI lookup, Medicare quoting, life/annuity accounts, BD/RIA accounts, agent management.

**_VIEW_WIRES.html:**
- Toggle: "By Product Line" / "By Data Domain"
- Dropdown to select product line or domain
- Horizontal flow chain per wire, color-coded by stage type
- Click stage = cross-reference to Tool Registry or MATRIX schema

---

## Shared Changes (All Phases)

**ATLAS_Config.gs additions:**
- 3 new tab constants in `ATLAS_TABS`
- New enums: `MCP_SERVERS`, `TOOL_CATEGORIES`, `AUTOMATION_TYPES`, `WIRE_STAGE_TYPES`

**Index.html nav restructure:**
```
[Dashboard] [Registry] [Tasks] [Analytics] [History] | [Tools] [Automation] [Pipeline] [Wires]
```
Each new view = minimal div + `<?!= include('_VIEW_*') ?>` to keep Index.html manageable.

**ATLAS_DevTools.gs additions:**
- `SETUP_CreatePhase7Tabs()` — creates 3 new MATRIX tabs
- `SETUP_SeedToolRegistry()` — populates ~250 tools
- `SETUP_SeedAutomationRegistry()` — populates 8 automations

---

## Files Modified (Summary)

| File | Changes |
|------|---------|
| **RAPID_CORE/CORE_Database.gs** | +3 TABLE_ROUTING, +3 TAB_SCHEMAS |
| **ATLAS_Config.gs** | +3 tab constants, new enums |
| **Code.gs** | ~20 new router cases, ~8 new ForUI wrappers |
| **Index.html** | Nav restructure (separator + 4 buttons), view containers, recurrence picker fix |
| **ATLAS_Tasks.gs** | `computeNextDueDate_()` Q/M format parsing |
| **ATLAS_DevTools.gs** | SETUP_ functions for Phase 7 |

## New Files Created

| File | Phase |
|------|-------|
| `ATLAS_ToolRegistry.gs` | 7A |
| `ATLAS_ToolSeed.gs` | 7A |
| `_VIEW_TOOLS.html` | 7A |
| `ATLAS_Automation.gs` | 7B |
| `_VIEW_AUTOMATION.html` | 7B |
| `ATLAS_Pipeline.gs` | 7C |
| `_VIEW_PIPELINE.html` | 7C |
| `ATLAS_Wires.gs` | 7D |
| `_VIEW_WIRES.html` | 7D |

---

## Verification (Per Phase)

1. `clasp push --force` + `clasp version` + `clasp deploy` + verify @version
2. Hard refresh frontend, navigate to new view
3. Verify data loads, filters work, no toast errors
4. For Tool Registry: confirm seed populated ~250 tools
5. For Automation: confirm green/yellow/red status renders
6. For Pipeline: confirm queue counts match MATRIX data
7. For Wires: confirm both toggle views render, cross-links work
8. `git add -A && git commit && git push` after each phase
