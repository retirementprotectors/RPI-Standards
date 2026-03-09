---
name: intent-atlas-consult
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (ATLAS\s+tool|ATLAS\s+registr|_TOOL_REGISTRY|_SOURCE_REGISTRY|data\s+import|data\s+migration|data\s+intake|bulk\s+import|BoB\s+import|book\s+of\s+business|commission\s+import|revenue\s+import|account\s+import|client\s+import|carrier\s+data|import\s+pipeline|intake\s+queue|data\s+foundation|operation\s+data)
---

## ATLAS Consultation — MANDATORY for Data Work

**ATLAS is the Data Operating System. It has two sections:**

### Section 1: Data Sources (`_SOURCE_REGISTRY`)
- Every carrier × product × domain mapped with gap status (RED/YELLOW/GREEN)
- Current method vs target method
- Automation percentages
- What's already flowing vs what's manual vs what's missing

### Section 2: Tools (`_TOOL_REGISTRY`)
- ~150 registered pipeline tools across 6 categories:
  1. **INTAKE_QUEUING** — scanners, processors (the tools that ingest data)
  2. **EXTRACTION_APPROVAL** — classification, AI extraction, approval workflows
  3. **NORMALIZATION_VALIDATION** — phone/address/email validation APIs
  4. **MATCHING_DEDUP** — client matching, deduplication
  5. **EXTERNAL_ENRICHMENT** — WhitePages, demographics
  6. **BULK_OPERATIONS** — batch processing
- Plus: `_AUTOMATION_REGISTRY` (launchd agents + GAS triggers), `_PIPELINE_STATUS` (queue depths), `WIRE_DEFINITIONS` (10+ data flow diagrams)

### What You MUST Do Before Any Data Work

1. **Read `_SOURCE_REGISTRY`** via execute_script on ATLAS — understand what sources exist, their gap status, and their current/target methods. Do NOT discover data sources by browsing folders when ATLAS already catalogs them.

2. **Read `_TOOL_REGISTRY`** via execute_script on ATLAS — check what intake/processing tools already exist BEFORE building new ones. Use registered tools. Do not reinvent the pipeline.

3. **Read `WIRE_DEFINITIONS`** for relevant data flows — understand the established path from source → intake → extraction → approval → MATRIX → frontend. Follow the wires.

4. **If working DATA-OUT** (from raw data toward the system): Still check ATLAS. The source registry tells you if this data source is already known, what method is expected, and what tools handle it. Even in a DATA-OUT session, ATLAS accelerates the work.

5. **Priority lists for data work should reference `_SOURCE_REGISTRY` gap analysis** — not be guessed from folder contents.

6. **If you find data sources NOT in `_SOURCE_REGISTRY`** — FLAG them for JDM, do NOT auto-register. Report a clear list:
   ```
   UNREGISTERED SOURCES FOUND (need JDM decision):
   - [file/folder name] — [what it appears to contain] — [recommended: register / skip / unclear]
   ```
   JDM decides what's a real source vs noise. Agents do NOT write to `_SOURCE_REGISTRY` without explicit approval. The registry is only useful if it stays clean — one garbage registration ("Josh's conference notepad") and the whole thing loses trust.

### ATLAS Project Details
- **Location:** `~/Projects/RAPID_TOOLS/ATLAS/`
- **Script ID:** `1dLLKTyOIOSN8W3X6oxn57FwbMHNCKDrI4HMdGojMRGfYAZpSNPHknUU_`
- **Key functions:** `getRegistryForUI({})`, `getGapAnalysisForUI({"group_by":"gap_status"})`, `getToolRegistryForUI({})` (WARNING: ~107K chars — read saved file if token limit hit), `getWiresByProductLineForUI()`, `getAutomationStatusForUI()`, `getPipelineSnapshotForUI()`

### Why This Rule Exists
On 2026-03-09, a data import session dismissed ATLAS as "Phase 5 visibility layer" when JDM directly asked if registered ATLAS tools were being used. Claude built import scripts from scratch, missed entire data folders, and generated priority lists by eyeballing folders — all while ATLAS had ~150 registered tools, 100+ cataloged sources, and wire definitions mapping every pipeline path. JDM asked the exact right question at the exact right time and got confidently wrong-answered. Never again.
