---
name: intent-atlas-consult
enabled: false
# → migrated to skill atlas-consult (GV2 WS-B pilot, STAGED). See
#   _RPI_STANDARDS/skills/atlas-consult/. Pattern + regex kept below as
#   historical reference and as the fallback if the skill conversion is
#   not ratified. Do NOT re-enable without SHINOB1 review.
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    # OB1-ATLAS-CONSULT-ANCHOR-001 (2026-07-26, megazord — owner).
    # THE TWIN OF `block-bulk-import-without-atlas`. Found by SHINOB1, corroborated by HIKARI.
    #
    # WAS: 19 BARE ALTERNATIONS, COMPLETELY UNANCHORED —
    #   (ATLAS\s+tool|...|data\s+import|...|bulk\s+import|...|carrier\s+data|...)
    #
    # It matched a MENTION anywhere in a prompt and could not distinguish a QUOTATION from a
    # DECLARATION. It fired on SHINOB1, then on HIKARI, then on ME — each time on a routed peer
    # message *reporting that it fires*, matching the quoted test string inside the report.
    # Four+ false fires in one night.
    #
    # ⚠️ WHY THIS TWIN IS THE MORE DANGEROUS OF THE PAIR — and it is NOT the action field.
    # HIKARI's correction, which is the sharper diagnosis: BOTH rules are `action: block`, so
    # mechanically the hit-Enter tier injects the rule BODY as context either way. The danger
    # scales with BODY IMPERATIVENESS, not action type. This body is a full numbered procedure
    # in imperative voice ("What You MUST Do Before Any Data Work", six steps, function names,
    # a script ID). **A body written as a procedure READS AS A DIRECTIVE when injected.**
    # That is the fabricated-directive failure OB1-INTENT-INJECT-001 exists to contain.
    # ⇒ Any `event: prompt` rule whose body is a numbered procedure is in this class. Audit on
    #   that axis, not on the action axis.
    #
    # THE CLASS THIS BELONGS TO: I narrowed the other twin first and declared the class closed.
    # **A fix whose coverage is PARTIAL looks exactly like a fix that worked.** The pair was never
    # enumerated — and the enumeration is one command: `ls hookify/*atlas*` returns exactly 2.
    # Same shape as the duplicated six-name brain.txt allowlist, `context.payload` (one syntactic
    # form of two), and the three unwired regression tests where only the exemplar was examined.
    #
    # NOW: line-initial imperative + a data-domain object WITHIN 60 CHARS ON THE SAME LINE.
    # A declaration cannot be faked by prose that merely names the words.
    #
    # VERIFIED BY EXECUTION on a corpus that REPRODUCES the false fire — including the
    # quoted-string forms, which is the corpus that caught this twin and which none of us had
    # until the rule fired on the message announcing the other fix:
    #   QUIET on: an indented quoted test table · a routed peer message · prose naming the terms
    #             · "Do not cite..." · "I ran the falsifier against the data import corpus..."
    #   FIRES on: "please bulk import records into the table" · "do a data import of the carrier
    #             statements" · "migrate the book of business into firestore" · "Import the BoB
    #             data for Devoted" · "backfill the commission records into bigquery"
    # 10/10. Both halves — no false positive, and NO false negative traded for it.
    # (`do a data import` failed my first draft; shipping that would have traded one defect for
    #  the other, so the verb branch was widened and everything re-run.)
    pattern: (?i)(?:^|\n)[[:space:]]*(?:please[[:space:]]+)?(?:bulk[[:space:]-]?(?:import|load)|import|migrate|ingest|backfill|load|intake|(?:do|run|start|perform|kick[[:space:]]+off)[[:space:]]+(?:a[[:space:]]+)?(?:bulk[[:space:]-]|data[[:space:]-])?(?:import|migration|intake|load|backfill))\b[^\n]{0,60}\b(?:data|records?|contacts?|book[[:space:]]+of[[:space:]]+business|BoB|carrier[[:space:]]+(?:data|statements?)|commissions?|revenue|firestore|bigquery|collection|table|pipeline|queue|registry)\b
owner: megazord
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

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
- **Location:** `~/Projects/archive/ATLAS/`
  - ⚠️ CORRECTED 2026-07-22 (JDM: "There IS NO RAPID_TOOLS Library any longer"). This rule
    pointed at `~/Projects/RAPID_TOOLS/ATLAS/` for months. That path does not exist, so a warrior
    following the rule literally dead-ends and may conclude ATLAS is unavailable — the exact
    opposite of what this rule exists to cause. Key files: `ATLAS_Seed.gs` (`_SOURCE_REGISTRY`),
    `ATLAS_ToolSeed.gs` (`_TOOL_REGISTRY`).
  - Live Firestore/Apps-Script reads are billing-walled during the 2026-07 GCP incident; the
    local `.gs` tree is the readable consult surface until reads unwall.
- **Script ID:** `1dLLKTyOIOSN8W3X6oxn57FwbMHNCKDrI4HMdGojMRGfYAZpSNPHknUU_`
- **Key functions:** `getRegistryForUI({})`, `getGapAnalysisForUI({"group_by":"gap_status"})`, `getToolRegistryForUI({})` (WARNING: ~107K chars — read saved file if token limit hit), `getWiresByProductLineForUI()`, `getAutomationStatusForUI()`, `getPipelineSnapshotForUI()`

### Why This Rule Exists
On 2026-03-09, a data import session dismissed ATLAS as "Phase 5 visibility layer" when JDM directly asked if registered ATLAS tools were being used. Claude built import scripts from scratch, missed entire data folders, and generated priority lists by eyeballing folders — all while ATLAS had ~150 registered tools, 100+ cataloged sources, and wire definitions mapping every pipeline path. JDM asked the exact right question at the exact right time and got confidently wrong-answered. Never again.
