# QUE — The Quoting & Underwriting Engine

## Context

The RPI Retirement Sales Process (RSP) has a 4-color pipeline: Orange (Discovery) → Blue (Data Foundation) → Yellow (Case Building) → Green (Close). The Yellow Stage is where quoting, analysis, and casework happen — and it's currently manual. AST-2 opens 8 browser tabs (WinFlex, ARW, Signal, carrier portals), runs quotes one at a time, builds comparisons in spreadsheets, and assembles outputs by hand.

The Mineart casework session proved Claude can execute the entire Yellow Stage: read the contract, extract rider terms, calculate roll-up math, run Winflex illustrations via Playwright, build comparison HTML, and file everything to the ACF. That was the manual prototype. QUE is the productized version.

**QUE is to quoting what Pipeline Studio is to pipelines.** Pipeline Studio designs pipeline workflows. QUE designs and executes quoting workflows. The Flow Engine runs pipeline instances. The QUE Engine runs quoting sessions.

---

## The Compound Insight: QUE IS ATLAS Applied to Quoting

Two parallel discovery sessions changed this architecture fundamentally:

**ATLAS Wire + Super Tool Architecture** established a 3-tier execution model:
- **Tools** (atomic): Individual functions that do one thing
- **Super Tools** (sequences): Ordered tool chains that execute a workflow
- **Wires** (pipelines): Ordered Super Tool chains that execute a complete data flow

QUE follows this EXACT pattern. It's not a separate system — it's ATLAS's outbound mirror:

```
ATLAS wires flow DATA IN:    Source → INTROSPECT → VALIDATE → NORMALIZE → MATCH → WRITE
QUE wires flow ANALYSIS OUT: GATHER → QUOTE → COMPARE → RECOMMEND → OUTPUT
```

Together they complete the circle:
```
Data IN (ATLAS) → Household Record → Case Building (QUE) → Recommendation → NewBiz OUT (DEX)
```

**Householding** established that the household is the atomic unit of work:
- QUE sessions are HOUSEHOLD-scoped (Mineart case = both Stephen AND Joyce)
- Aggregate financials (combined income, filing status, tax bracket) feed directly into QUE tax calcs
- ACF outputs file to HOUSEHOLD folders (B4 Recommendations)
- Pipeline instances are household-scoped — QUE inherits the household context automatically
- Survivorship products need BOTH members' data — household gives this natively

**The Architecture Statement:**
- ATLAS imports data INTO households
- QUE quotes and analyzes AT the household level
- DEX generates outputs FOR the household
- Householding is the unit. ATLAS is inbound. QUE is outbound. DEX is the bridge to NewBiz.

---

## Architecture Decision: Module, Not App

QUE is a **Module** (portal-branded, operational) with a companion **Admin section**.

- The Workbench (daily use) lives in Sales Centers — portal-branded via CSS vars
- The Admin (configuration) lives in Admin section — same pattern as flow-admin
- QUE is NOT a standalone App like Pipeline Studio. Advisors don't "design" quotes, they execute them.

---

## How QUE Connects to Everything That Already Exists

```
SALES_RETIREMENT Pipeline (Flow Engine)
├── Orange: Discovery           → Flow Engine handles
├── Blue: Data Foundation       → Flow Engine + DEX forms (8 forms)
├── Yellow: Case Building       → Flow Engine orchestrates, QUE EXECUTES
│   ├── general_casework        → Flow tasks (manual)
│   ├── investment_casework     → QUE-Investment
│   ├── medicare_casework       → QUE-Medicare (ALREADY WORKING via CSG)
│   ├── life_casework           → QUE-Life (NEW — WinFlex, carriers)
│   └── annuity_casework        → QUE-Annuity (NEW — ARW, carriers)
├── Green: Close Ready          → Flow Engine + DEX output assembly
└── Red: A+R Close              → Flow Engine handles
```

**ATLAS** registers every quoting source and output as Sources/Tools/Wires.
**DEX** generates the deliverables (PDFs, illustrations, comparisons) from QUE data.
**Pipeline Studio** defines the pipeline structure. QUE Admin configures what happens inside quoting steps.

---

## What Ships

### packages/core/src/que/
- `types.ts` — QueProfile, QueSource, QueSession, QueQuoteResult, QueRecommendation, QueOutput
- `engine.ts` — Session state machine (draft → quoting → comparing → recommended → finalized)
- `comparison.ts` — Comparison algorithms (lowest_premium, best_value, carrier_rated)
- `adapters.ts` — Source adapter interface + CSG adapter (refactored from medicare-quote.ts)

### services/api/src/routes/
- `que.ts` — Session CRUD, quote execution, comparison, recommendation, output generation
- `que-admin.ts` — Profile/source/output template CRUD (leader+ auth)

### packages/ui/src/modules/
- `QueWorkbench/` — 6-step operational interface (Client Data → Parameters → Quote → Compare → Recommend → Output)
- `QueAdmin/` — Source registration, output templates, profile config (tabbed CRUD, ATLAS pattern)

### Firestore Collections
- `que_profiles` — 4 product line configs (Life, Annuity, Medicare, Investment)
- `que_sources` — Adapter configs linking to ATLAS sources
- `que_sessions` — Active quoting sessions (one per client per case)
- `que_output_templates` — Deliverable templates linking to DEX forms

### Sales Center Pages (upgraded from bare lists)
- `/sales-centers/life` → `<QueWorkbench productLine="LIFE" />`
- `/sales-centers/annuity` → `<QueWorkbench productLine="ANNUITY" />`
- `/sales-centers/medicare` → `<QueWorkbench productLine="MEDICARE" />` (refactored)
- `/sales-centers/advisory` → `<QueWorkbench productLine="INVESTMENT" />`

### Flow Engine Integration
- New `execution_type: 'que_workbench'` on casework steps
- `QUE_SESSION_COMPLETE` check handler for automatic gate advancement
- "Launch QUE" button in PipelineInstance for que_workbench steps

---

## Source Registration (11 External Tools)

| Tool | Product Line | Adapter Today | Adapter Tomorrow |
|------|-------------|---------------|-----------------|
| CSG Actuarial | Medicare | `api` (WORKING) | `api` |
| WinFlex | Life | `manual` (prefill URL) | `scrape` (Playwright) |
| Annuity Rate Watch | Annuity | `manual` | `scrape` (Playwright) |
| Signal Wealth | Investment | `manual` | `api` (if available) |
| Nitrogen/Riskalyze | Investment | `manual` | `api` (partner API) |
| Foresters Portal | Life | `manual` | `api` (carrier API) |
| Kansas City Life | Life | `manual` | `manual` |
| Ameritas Portal | Life | `manual` | `manual` |
| Nassau SS Timing | Life/Annuity | `manual` | `manual` |
| The Index Standard | Annuity | `manual` | `scrape` |
| MoneyGuidePro | Investment | `manual` | `manual` |

---

## Automation Phases

**Phase 1 (Sprint 11-12): Structured Manual**
- QUE Workbench UI with manual adapters
- Medicare fully automated (CSG API refactored into QUE)
- Life/Annuity: pre-fill URLs, advisor copies results back
- Value: Consistency, audit trail, standardized comparisons

**Phase 2 (Sprint 13-14): Semi-Automated**
- Playwright adapters for WinFlex, ARW, Index Standard
- API integrations for Nitrogen, carrier portals with APIs
- Value: Minutes instead of hours, fewer errors

**Phase 3 (Sprint 15+): Fully Automated (MDJ)**
- Auto-trigger when client enters Yellow Stage
- Parallel source queries
- AI comparison + draft recommendation
- Advisor approval workflow
- Auto-output via DEX
- Value: The Mineart case in 5 minutes instead of 5 hours

---

## Solution Categories (Yellow Stage Casework Types)

Each QUE session is tagged with a solution category:
- Income NOW — Immediate income solutions
- Income LATER — Deferred income strategies
- Estate MAX — Maximum estate/legacy transfer (Mineart case = this)
- Growth MAX — Maximum accumulation
- LTC MAX — Long-term care optimization
- ROTH Conversion — Tax optimization
- Tax Harvesting — Strategic tax management
- MGE Detailed — MoneyGuidePro deep dive

---

## Five Yellow Stage Outputs (via DEX)

1. Client-Facing AI3 PDF
2. Reports + In-Force Illustrations
3. Product Illustrations (top 3 solutions, multiple scenarios)
4. Casework Components (summary + detail versions)
5. RPI Factfinder (pre-filled application package)

All filed to ACF → B4 Recommendations folder.

---

## QUE as ATLAS Super Tools + Wire

QUE's execution model maps directly onto the ATLAS 3-tier architecture:

### QUE Atomic Tools (Layer 1)

| Tool | Category | What It Does |
|------|----------|-------------|
| `gather-household-data` | Input | Pull household + member data from Firestore |
| `gather-acf-documents` | Input | Pull Blue Stage deliverables from ACF |
| `extract-contract-terms` | Input | Read contract PDFs, extract rider specs (roll-ups, payout tables) |
| `query-csg` | Quote | CSG API for Medicare (EXISTS) |
| `query-winflex` | Quote | WinFlex adapter (manual → Playwright → API) |
| `query-arw` | Quote | Annuity Rate Watch adapter |
| `query-carrier-portal` | Quote | Generic carrier adapter (Foresters, KCL, Ameritas, Nassau) |
| `query-nitrogen` | Quote | Riskalyze risk analysis |
| `query-signal` | Quote | Signal Wealth investment reports |
| `compare-quotes` | Analysis | Comparison algorithm (lowest premium, best value, carrier rated) |
| `calc-tax-impact` | Analysis | Federal tax + state-specific rules (Iowa retirement exemption) |
| `calc-rollup-impact` | Analysis | GMIB/GLWB deferral analysis |
| `build-recommendation` | Output | Selected products + rationale + solution category |
| `generate-comparison-html` | Output | Casework HTML (RPI brand design system) |
| `file-to-acf` | Output | Upload to household ACF B4 folder |

### QUE Super Tools (Layer 2)

**QUE_GATHER** — "Get everything we need to quote."
```
gather-household-data → gather-acf-documents → extract-contract-terms
→ OUTPUT: Household snapshot + contract terms
```

**QUE_QUOTE** — "Hit the sources." (per product line, in parallel)
```
Medicare:   query-csg (automated)
Life:       query-winflex + query-carrier-portal
Annuity:    query-arw + query-carrier-portal
Investment: query-nitrogen + query-signal
→ OUTPUT: Raw quote results from all sources
```

**QUE_COMPARE** — "Rank and score."
```
compare-quotes → calc-tax-impact → calc-rollup-impact
→ OUTPUT: Scored comparison with tax-adjusted net values
```

**QUE_RECOMMEND** — "Build the case."
```
build-recommendation → generate-comparison-html → file-to-acf
→ OUTPUT: Finalized recommendation + filed deliverables
```

### QUE Wire (Layer 3)

**WIRE_CASEWORK** — The complete Yellow Stage Phase 1:
```
QUE_GATHER → QUE_QUOTE → QUE_COMPARE → QUE_RECOMMEND
```

Parallel to ATLAS:
- `WIRE_DATA_IMPORT`: INTROSPECT → VALIDATE → NORMALIZE → MATCH → WRITE
- `WIRE_CASEWORK`: QUE_GATHER → QUE_QUOTE → QUE_COMPARE → QUE_RECOMMEND

Same philosophy: drop the data in, the system figures out what to do.

---

## Householding Integration

### QUE Sessions Are Household-Scoped

The Mineart case was ALWAYS about the household — Stephen AND Joyce. QUE sessions operate at the household level, not the individual.

### What Householding Gives QUE for Free

| QUE Need | Householding Provides |
|----------|----------------------|
| Both insureds for survivorship | `household.members[]` |
| Combined income for tax calcs | `household.aggregate_financials.combined_income` |
| Filing status | `household.aggregate_financials.filing_status` |
| Tax bracket | `household.aggregate_financials.tax_bracket` |
| All accounts across both spouses | Accounts indexed by `household_id` |
| ACF folder for filing | `household.acf_folder_id` → B4 Recommendations |
| State tax rules | `household.address.state` → Iowa = retirement exempt |

### INTROSPECT Meets QUE

When a household enters Yellow Stage, QUE_GATHER runs INTROSPECT on the household's accounts:
- Nassau Income Accelerator → FIA with GMIB → activate QUE-Annuity
- JH Survivorship IUL → survivorship life → activate QUE-Life
- Corebridge AG Choice 10 → FIA with GMIB → activate QUE-Annuity

Auto-determines which tracks to run. No manual selection needed.

---

## Critical Files

| File | Why |
|------|-----|
| `packages/core/src/flow/configs/sales-retirement.ts` | Yellow Stage task defs — add `execution_type: 'que_workbench'` |
| `services/api/src/routes/medicare-quote.ts` | Working CSG adapter — becomes reference for all QUE adapters |
| `packages/core/src/flow/hooks.ts` | Check handler registry — register `QUE_SESSION_COMPLETE` |
| `packages/ui/src/modules/PipelineStudio/` | Reference pattern for complex module architecture |
| `packages/ui/src/modules/AtlasRegistry.tsx` | Reference pattern for QUE Admin (tabbed CRUD) |

---

## Verification

1. Seed QUE profiles + sources → confirm Firestore docs created
2. Create a QUE-Medicare session via API → confirm CSG quotes flow through
3. Open Sales Center Life page → confirm QUE Workbench renders
4. Create a manual Life session → confirm 6-step wizard works
5. Generate output → confirm DEX produces PDF in ACF
6. Open pipeline instance → confirm "Launch QUE" button on casework steps
7. Complete QUE session → confirm flow gate advances automatically
