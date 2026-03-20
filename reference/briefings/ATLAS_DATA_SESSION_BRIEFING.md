# ATLAS Data Session Briefing
> **Paste this into any session doing data import/migration/consolidation work.**

---

## MANDATORY: Read Before Doing ANYTHING With Data

**ATLAS is the Data Operating System.** It is NOT a "Phase 5 visibility layer." It is NOT something you get to later. It is the central registry of every data source, every pipeline tool, and every data flow in The Machine.

### Before you write a single function, build a single preprocessor, or touch a single file:

**1. Read ATLAS `_SOURCE_REGISTRY` + Gap Analysis**
Query via toMachina API at `services/api/src/routes/atlas.ts` or directly in Firestore.
- Call `GET /api/atlas/sources` via portal proxy — full source registry (100+ entries)
- Call `GET /api/atlas/analytics?group_by=gap_status` — RED/YELLOW/GREEN breakdown for prioritization
This gives you every carrier × product × domain with gap status, current method, target method, and automation %.
**Use this to understand what data sources exist BEFORE browsing Drive folders.**

**2. Read ATLAS `_TOOL_REGISTRY`**
Call `GET /api/atlas/tools` via portal proxy.
**WARNING:** This returns ~107K characters. If it exceeds token limits, read the output file it saves to disk.
This gives you ~150 registered pipeline tools across 6 categories:
- **INTAKE_QUEUING** — scanners, processors (use these, don't build new ones)
- **EXTRACTION_APPROVAL** — classification, AI extraction, approval workflows
- **NORMALIZATION_VALIDATION** — phone/address/email APIs
- **MATCHING_DEDUP** — client matching, dedup algorithms
- **EXTERNAL_ENRICHMENT** — WhitePages, demographics
- **BULK_OPERATIONS** — batch processing
**If a tool exists for what you're about to build, USE IT.**

**3. Read ATLAS Wire Definitions**
Call `getWiresByProductLineForUI()` with `devMode: true`.
These show the exact pipeline path from source → intake → extraction → approval → MATRIX → frontend for 10+ data flows. **Follow the wires. Do not invent pipeline paths.**

**4. Read the ACCOUNT UPLOAD MASTER**
In Drive folder `1nzdAWT...` (Account/BoB Hub ROOT).
This is the field mapping schema: Contact Id → Annuity/Life/Medicare/BD/RIA.
**Read this before writing ANY import field mapping.**

### When Building Priority Lists
Derive priorities from `_SOURCE_REGISTRY` gap analysis (RED sources first, then YELLOW), NOT from eyeballing folder contents. ATLAS already scores everything.

### When You Find Data Sources NOT in the Registry
**FLAG them — do NOT auto-register.** Report to JDM:
```
UNREGISTERED SOURCES FOUND (need JDM decision):
- [file/folder name] — [what it appears to contain] — [recommended: register / skip / unclear]
```
JDM decides what's a real source vs noise. You do NOT write to `_SOURCE_REGISTRY` without explicit approval. The registry is only useful if it stays clean.

### When Building Import Functions
Check `_TOOL_REGISTRY` INTAKE_QUEUING category first. Registered scanners and processors already exist for many source types. Extend existing tools rather than building from scratch.

### The Two Sections of ATLAS

| Section | What It Contains | MATRIX Tabs |
|---------|-----------------|-------------|
| **Data Sources** | Every external data source mapped | `_SOURCE_REGISTRY`, `_SOURCE_TASKS`, `_SOURCE_HISTORY`, `_SOURCE_METRICS` |
| **Tools** | Every pipeline tool cataloged | `_TOOL_REGISTRY`, `_AUTOMATION_REGISTRY`, `_PIPELINE_STATUS`, `WIRE_DEFINITIONS` |

### Why This Briefing Exists
Previous sessions dismissed ATLAS and rebuilt import infrastructure from scratch, missing data folders, building tools that already existed, and generating priority lists by guesswork. This wasted hours. ATLAS has the answers — consult it first.

---

## Q&A — Common Questions During Data Sessions

**Q: I found a Google Sheet / XLSX / CSV with carrier data. Should I build a preprocessor and import it?**
A: STOP. Before building anything:
1. Check `_SOURCE_REGISTRY` — is this source already registered? What's its gap_status?
2. Check `_TOOL_REGISTRY` INTAKE_QUEUING — does a scanner/processor already exist for this source type?
3. Check Wire Definitions — what's the documented path from this source type to MATRIX?
4. Read the ACCOUNT UPLOAD MASTER — does the field mapping match?
If the source isn't registered, FLAG it for JDM. If a tool exists, USE IT. If a wire exists, FOLLOW IT.

**Q: Can I write directly to MATRIX sheets using setValues() for speed?**
A: NO. All MATRIX writes go through RAPID_API or RAPID_CORE.insertRow(). Direct writes bypass carrier normalization, NAIC code population, parent carrier derivation, validation hooks, and audit trail logging. This is hook-enforced (`block-direct-matrix-write`). The February 2026 Medicare import and the March 2026 Life/Annuity/BD/RIA imports both bypassed the pipeline and required retroactive normalization to fix. Don't repeat this.

**Q: I found data in Drive folders that isn't in the ATLAS source registry. Should I register it?**
A: NO. Flag it for JDM using the template in the briefing. JDM decides what's a real source vs noise. The registry is only useful if it stays clean. Present what you found, recommend register/skip/unclear, and wait for the decision.

**Q: Should I build my own priority list based on what folders I find?**
A: NO. Run `getGapAnalysisForUI({"group_by":"gap_status"})` on ATLAS. RED gaps first, then YELLOW. The registry already has health scores, automation percentages, and priority rankings. Your job is to execute against that list, not invent a new one.

**Q: The import is for 900+ records. Do I need to route each one through RAPID_API individually?**
A: For bulk imports, the pattern is: preprocess data locally, then use a GAS FIX_ function that calls RAPID_CORE normalization functions (normalizeCarrierName, deriveParentCarrier) AND writes through the standard pipeline. The wire for bulk carrier data is: Carrier Statement → scanIntakeFolders (RAPID_IMPORT) → extractDataFromImages (document-processor) → _INTAKE_QUEUE → Approval UI → MATRIX. For structured spreadsheet data that doesn't need OCR, use IMPORT_BoBImport.gs helpers which call RAPID_CORE internally.

**Q: Do I need to update ATLAS after importing data?**
A: YES. After any import:
1. Update `_SOURCE_HISTORY` with what was imported (source, record count, date)
2. Check if the import changes a source's gap_status (e.g., RED → YELLOW because data now flows via MANUAL_CSV)
3. If you built a new tool/function, register it in `_TOOL_REGISTRY`
ATLAS is the operating system — it needs to know what happened.

**Q: There are carrier-specific XLSX/CSV files in the BoB Hub subfolders. Do I need to import ALL of them?**
A: Read them first. Many will be the same data that's already in the curated ProDash BoB sheets (just carrier-specific views). Cross-reference against what's already in MATRIX by checking policy/account numbers. Only import records that don't already exist. The curated BoB sheets are the summary — the carrier subfolders are the detail. Check both.

**Q: I see PDFs (commission statements, carrier statements). How do I import those?**
A: PDFs go through the document processing pipeline, NOT bulk import. The wire is: PDF → scanIntakeFolders or scanEmailInboxes → watcher.js (document-processor) → Claude Vision extraction → _APPROVAL_QUEUE → human approval → MATRIX. Drop them in the appropriate SPC_INTAKE folder or forward to a monitored email inbox. Don't try to parse PDFs in a preprocessor script.

**Q: What's the ACCOUNT UPLOAD MASTER and why do I need it?**
A: It's the Rosetta Stone for field mapping. Located in the Account/BoB Hub ROOT folder (`1nzdAWT...`). It defines exactly which fields map from source data to each MATRIX tab (Client, Annuity, Life, Medicare, BD/RIA). Contact Id is the key that links everything. If your import function's field mapping doesn't match this schema, your data will land in the wrong columns or get silently dropped. Read it FIRST.

**Q: What if ATLAS shows a source as GREEN but I know the data is stale/incomplete?**
A: GREEN means the pipeline is connected and flowing — not that the data is perfect. Check `_SOURCE_HISTORY` for last_pull_at and record counts. If the data is stale, update the source's notes and flag it. GREEN with stale data is a monitoring issue, not a gap issue.

**Q: I'm building for Life/Annuity. The schemas have 50+ fields each. Do I need to map all of them?**
A: Map what your source data has. Use the ACCOUNT UPLOAD MASTER to identify which source columns map to which MATRIX fields. Empty fields are fine — they get filled by enrichment passes later (FIX_Normalize, FIX_Backfill, WhitePages enrichment). Don't fabricate data to fill empty columns. But DO populate: carrier_name, policy/account_number, status, client_id (if matchable), import_source, and created_at/updated_at at minimum.

**Q: What's the difference between the Data Vault folders and the Account/BoB Hub folders?**
A: **Data Vault** (`RPI Data Vault/CARRIER_DATA/`) = raw carrier files uploaded from local disk. Organized by product line and carrier. Source of truth for what files RPI has. **Account/BoB Hub** (`[BRAND][ADVISOR]- * BoBs/`) = pre-existing Drive folders with curated BoB sheets and carrier-specific subfolders. Often contains both the curated summary sheet (Google Sheet) and the raw carrier exports (XLSX/PDF) in subfolders. Check both locations — they may have different data or different versions of the same data.

**Q: ATLAS says a source's target_method is API_FEED but current_method is NOT_AVAILABLE. What do I do?**
A: That's a RED gap where the target is API integration but no connection exists yet. For Phase 3b data import work, you can still import available CSV/XLSX data as MANUAL_CSV — that moves the gap from RED to YELLOW. The API_FEED target is a future automation goal, not a blocker for getting data into MATRIX today. Import what's available now, automate later.

---

*ATLAS project: `~/Projects/RAPID_TOOLS/ATLAS/` | Script ID: `1dLLKTyOIOSN8W3X6oxn57FwbMHNCKDrI4HMdGojMRGfYAZpSNPHknUU_`*
