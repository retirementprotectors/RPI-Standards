# Discovery: Yellow Stage — Phase 2 (Casework Components) + Phase 3 (Outputs)

**Created:** 2026-03-17
**Domain:** Yellow Stage AST-2 — Casework Component Development + Five Output Assembly
**Scope:** Everything AFTER analysis & quoting (Phase 1), BEFORE the Green Stage close
**Companion Discoveries:** HOUSEHOLDING.md, ATLAS-WIRE-SUPER-TOOL-ARCHITECTURE.md, YELLOW_STAGE_PHASE1_ANALYSIS_QUOTING.md
**Status:** Discovery Complete → Ready for FORGE

---

## What This Document Is

This is the complete discovery synthesis for the second and third phases of the RPI Yellow Stage sales process. It catalogs every casework component, calculator, template, formula, and output format extracted from three sources, then maps them onto the QUE architecture as registered tools, super tools, and wires.

**Sources Scanned:**

1. **Claude.AI Project Archive** — 21 B2C-RPI project folders (150+ files)
2. **\*CaseWork- Components** — Google Shared Drive folder (61 items, folder ID: `1BXJsTtg3RkEaqtlVhWDtbUnB1JYSTv1U`)
3. **RPI Sales Team Playbook** — Master process document (606KB, Yellow Stage v2.0)

**Companion Documents (count as done — being built in parallel):**

- **Householding** — `toMachina/.claude/discovery/HOUSEHOLDING.md` — Household is the unit of work. All casework components read from `households/{id}`. All outputs file to household ACF.
- **ATLAS Wire Architecture** — `toMachina/.claude/discovery/ATLAS-WIRE-SUPER-TOOL-ARCHITECTURE.md` — Tool → Super Tool → Wire 3-tier model. QUE mirrors this architecture for outbound analysis.
- **QUE Plan** — `toMachina/.claude/discovery/YELLOW_STAGE_PHASE1_ANALYSIS_QUOTING.md` — QUE_GATHER → QUE_QUOTE → QUE_COMPARE → QUE_RECOMMEND. Phase 2+3 implements the guts of QUE_COMPARE and QUE_RECOMMEND.

**Roadmap Doc (Google Drive):**
- Casework Component Library — Extraction Roadmap: `https://docs.google.com/document/d/1r1-XWm1APiIySZrmdiqqfQWLZyrnG6lunxHxDSjWZhQ/edit`

**Completed Casework Process Docs:**
- `_RPI_STANDARDS/reference/collateral/CASEWORK-PROCESS-GMIB-TO-LIFE.md`
- `_RPI_STANDARDS/reference/collateral/CASEWORK-PROCESS-CLIENT-REVIEW-MEETING.md`
- `_RPI_STANDARDS/reference/collateral/RPI-Strategic-Life-Insurance-Funding-Analysis.html`
- `_RPI_STANDARDS/reference/collateral/RPI-Client-Review-Meeting-Template.html`

---

## Where This Sits

### In the Pipeline

```
ORANGE (COR) — Book Discovery Meeting
  > BLUE (AST-1) — Intake / Input / Data Foundation
    > YELLOW (AST-2)
        Phase 1: Analysis & Quoting            ← QUE_GATHER + QUE_QUOTE (other agent)
        Phase 2: Casework Component Dev        ← THIS DOCUMENT (QUE_COMPARE guts)
        Phase 3: Five Outputs → B4 folder      ← THIS DOCUMENT (QUE_RECOMMEND guts + ASSEMBLE)
      > GREEN (SPC) — Close / A+R Meeting
        > RED — NewBiz Handoff
```

### In the QUE Architecture

```
QUE_GATHER   (other agent)    → Pull household data + ACF docs + contract terms
QUE_QUOTE    (other agent)    → Hit external sources (CSG, WinFlex, ARW, Signal)
QUE_COMPARE  (THIS DOCUMENT)  → ANALYZE_* super tools run per solution category
QUE_RECOMMEND (THIS DOCUMENT) → GENERATE_CASEWORK + ASSEMBLE_OUTPUT
```

My calc-* tools are QUE Layer 1 atomic tools.
My ANALYZE_* sequences are sub-routines within QUE_COMPARE.
My GENERATE/ASSEMBLE work is the implementation of QUE_RECOMMEND.
All registered in the QUE tool registry with `domain: 'que'`.
Pipeline Studio orchestrates which wires fire at which stages.

### In the Household Model

All casework components operate at the household level:
- Data reads from `households/{id}` + `aggregate_financials`
- Accounts indexed by `household_id` across all members
- Outputs file to household ACF B4 Recommendations folder
- Per-member detail sections within household-scoped documents

---

## Phase 2: Casework Component Development

### The Philosophy — "12 Arrows in Your Quiver"

Josh Millang's core principle: walk into every A+R meeting prepared for ANY client response.

**Progressive Disclosure (3 tiers):**

| Tier | % of Clients | What They See | Specialist Script |
|------|-------------|---------------|-------------------|
| **Tier 1** | 85-90% | AI3 + Reports = Decision made | "Here's your situation, here's what we found, here's what we recommend, and here's why." |
| **Tier 2** | 5% | + Product illustrations seal the deal | "Let me show you more details about how this works and why we work with this company." |
| **Tier 3** | 5% | + Detailed casework for analytical clients | "I have detailed analysis for every question you might have — let's dive into the specifics." |

### Component Structure (Every Type Follows This Pattern)

Each casework type produces three layers:

1. **Summary** (85-90%) — Simple A vs B comparison, one-pager, client-friendly language, visual charts
2. **Detail** (5%) — Year-by-year projections, fee breakdowns, tax implications, comprehensive spreadsheets
3. **Supporting Tools** — Head-to-head comparisons, income calculators, 1035 exchange analysis, scenario modeling

### The 8 Named Casework Types

1. Income NOW
2. Income LATER
3. Estate MAX
4. Growth MAX
5. LTC MAX
6. MGE - DETAILED Analysis
7. ROTH Conversion
8. Tax Harvesting

---

## QUE Tool Registry — Phase 2+3 Tools

### Calculation Tools (QUE Layer 1 — Atomic)

| Tool ID | What It Does | Formula | Source |
|---------|-------------|---------|--------|
| `calc-rmd` | Required Minimum Distribution | Prior Year Value / IRS Uniform Lifetime Factor | RMD Calc sheet |
| `calc-gmib` | Guaranteed income from benefit base | Benefit Base × Payout Rate (by attained age) | Income Comparison sheet |
| `calc-rollup` | Benefit base growth projection | Base × (1 + Rollup Rate) per year, simple or compound | GMIB-to-Life process |
| `calc-surrender-charge` | Cost to exit existing product | AV × Charge % (by surrender year in schedule) | Consolidation templates |
| `calc-ltcg` | Long-term capital gains tax | (Market Value - Cost Basis) × Tax Rate | Tax Harvesting templates |
| `calc-bonus-offset` | Net cost after carrier bonus | (Surrender + LTCG) - (Deposits × Bonus %) | Consolidation templates |
| `calc-provisional-income` | IRS formula for SS taxation | 50% SS + Pensions + Wages + Interest + IRA Dist | PROV+FEDS+STATE sheet |
| `calc-ss-taxation` | How much SS is taxable | Apply 0%/50%/85% brackets on provisional income | PROV+FEDS+STATE sheet |
| `calc-federal-tax` | Federal income tax | Apply MFJ brackets to taxable income after deduction | PROV+FEDS+STATE sheet |
| `calc-state-tax` | State income tax | State-specific rate on taxable income | PROV+FEDS+STATE sheet |
| `calc-irmaa` | Medicare premium surcharge | MAGI bracket lookup → Part B + Part D surcharge | IRMAA Calculator sheet |
| `calc-ss-earnings-limit` | Pre-FRA earnings impact | $1 withheld per $2 above limit + months deferred | SS FRA Calc sheet |
| `calc-income-multiplier` | Life insurance needs by age | Age-based: 20-39=30x, 40-44=25x ... 70+=5x | Family Needs Calculator |
| `calc-college-funding` | Future cost of college | $35,331 × (1 + 6.80%)^(18-age) × 4 years | Family Needs Calculator |
| `calc-net-outlay` | True cost of life insurance | Premium Outlay - Cash Value | FE v TERM v IUL sheet |
| `calc-breakeven-equity` | Return needed to not lose principal | (Withdrawals + Fees - Income) / Portfolio Value | Income Portfolio Analysis |
| `calc-mva` | Hidden market value adjustment | (AV - SV) / AV × 100, decompose into components | MVA Calculator |
| `calc-mgsv` | Minimum guaranteed surrender value | 87.5% of premiums at 3% interest | MVA Calculator |
| `calc-va-depletion` | Year-by-year VA burn rate | (Starting - Withdrawal) × (1 + Net Return) per year | GROWTH MAX + VA DB sheets |
| `calc-fia-projection` | Year-by-year FIA growth | Deposits × (1 + Bonus) then × (1 + Hypo Growth) per year | GROWTH MAX sheet |
| `calc-delta` | Advantage of proposed over current | FIA Value - VA Value per year | GROWTH MAX sheet |
| `calc-lot-selection` | Optimal tax lots for liquidation | Sort by gain%, sell lowest first until target reached | Tax Harvesting templates |
| `calc-ltc-phase-access` | LTC access by qualification level | Phase I-IV amounts based on contract features | LTC Access framework |
| `calc-household-aggregate` | Combined household financials | Sum across all members: income, NW, investable, accounts | Householding |
| `calc-effective-tax-rate` | Combined tax efficiency | (Federal + State) / Gross Income | PROV+FEDS+STATE sheet |

### Lookup Tools (QUE Layer 1 — Atomic)

| Tool ID | What It Does | Data Source |
|---------|-------------|-------------|
| `lookup-irs-factor` | Uniform Lifetime Table divisor by age | RMD Calc sheet (ages 72-120) |
| `lookup-carrier-product` | Product specs, rates, features | Index + MVA Calcs sheet (10 carriers) |
| `lookup-index-rate` | FIA index/crediting method/cap/par rate | Index + MVA Calcs sheet (17 indexes) |
| `lookup-surrender-schedule` | Surrender charge % by carrier/product/year | MVA Calculator carrier data |
| `lookup-fyc-rate` | FYC Target% + Excess% by carrier | UL Case Matrix (14 carriers) |
| `lookup-tax-bracket` | Federal + state by filing status + income | PROV+FEDS+STATE (2025 brackets) |
| `lookup-irmaa-bracket` | Part B + D surcharge by MAGI tier | IRMAA Calculator (2024+2025) |
| `lookup-community-property` | States requiring spousal signatures | AK, AZ, CA, ID, LA, NM, NV, TX, WA, WI |

### Generation Tools (QUE Layer 1 — Atomic)

| Tool ID | What It Does | Output |
|---------|-------------|--------|
| `generate-summary-html` | Tier 1 one-pager per casework type | A vs B comparison, client-friendly, RPI branded |
| `generate-detail-html` | Tier 2/3 year-by-year projections | Comprehensive tables, fee breakdowns, scenario modeling |
| `generate-ai3-pdf` | Client-facing AI3 from household data | Clean PDF, internal sections removed, exec summary |
| `generate-meeting-prep` | Review meeting agenda with talk tracks | 3-page HTML: snapshot + opportunities + notes |
| `generate-factfinder` | Pre-filled application package | Forms + timeline + signature checklist |

### DEX Tools (Document Operations — Shared Across Domains)

| Tool ID | What It Does |
|---------|-------------|
| `create-acf-folder` | Build household ACF Drive structure |
| `file-to-acf` | Route document to correct ACF subfolder |
| `html-to-pdf` | Render HTML → PDF via Puppeteer |
| `merge-documents` | Combine multiple outputs into meeting package |
| `classify-outgoing-doc` | Apply naming convention to output doc |

---

## QUE Super Tools — Phase 2+3 (QUE Layer 2)

### Analysis Super Tools (one per casework type — run inside QUE_COMPARE)

#### ANALYZE_INCOME_NOW
```
1. calc-household-aggregate    → Combined income, expenses, disposable
2. calc-gmib                   → Current GMIB payouts across all FIAs
3. calc-rmd                    → RMD requirements for IRA accounts
4. calc-breakeven-equity       → Can portfolio sustain current withdrawals?
→ OUTPUT: Income gap/surplus, BEP metric, recommended activation
```

#### ANALYZE_INCOME_LATER
```
1. calc-rollup                 → Project benefit base growth by deferral year
2. calc-gmib                   → Payout at each future activation age
3. calc-provisional-income     → Tax impact of future GMIB distributions
4. calc-federal-tax            → Bracket impact of additional income
→ OUTPUT: Roll-up advantage table, 3-option framework, tax math per option
```

#### ANALYZE_ESTATE
```
1. calc-va-depletion           → Project each policy forward (lapse detection)
2. calc-income-multiplier      → Survivor needs calculation
3. calc-college-funding        → If dependents exist
4. lookup-fyc-rate             → Carrier comparison for replacements
→ OUTPUT: Lapse warnings, DB erosion total, 1035 candidates, survivor gap
```

#### ANALYZE_GROWTH
```
1. calc-va-depletion           → Existing VA burn-rate (with actual fund returns)
2. calc-fia-projection         → Proposed FIA sustainability (with bonus)
3. calc-delta                  → Year-by-year advantage
4. calc-surrender-charge       → Cost to exit existing product
5. calc-ltcg                   → Tax on gains realized
6. calc-bonus-offset           → Carrier bonus covers costs?
→ OUTPUT: Depletion age, delta table, net cost (often negative), consolidation math
```

#### ANALYZE_LTC
```
1. calc-ltc-phase-access       → Map all contracts to Phase I/II/III/IV
2. calc-gmib                   → Base income × 2x multiplier (Phase II)
3. calc-mgsv                   → Floor protection values
4. lookup-carrier-product      → Which contracts have which LTC features
→ OUTPUT: 4-phase access table, total LTC pool, annual fee analysis, break-even
```

#### ANALYZE_ROTH
```
1. calc-provisional-income     → Current MAGI without conversion
2. calc-ss-taxation            → Current SS taxation bracket
3. calc-federal-tax            → Current effective rate
4. calc-irmaa                  → Current IRMAA impact
5. [simulate conversion amount]
6. calc-provisional-income     → MAGI WITH conversion added
7. calc-federal-tax            → New effective rate + bracket jump
8. calc-irmaa                  → New IRMAA impact (2-year lag)
→ OUTPUT: Before/after tax comparison, bracket jump warning, IRMAA cliff, break-even year
```

#### ANALYZE_TAX_HARVEST
```
1. calc-lot-selection          → Sort all lots by gain%, select for target
2. calc-ltcg                   → Tax on selected lots
3. calc-ss-earnings-limit      → If pre-FRA, impact on SS benefits
4. calc-provisional-income     → Impact on SS taxation
→ OUTPUT: Lot selection table, effective tax rate, net proceeds, loss carryforward
```

#### ANALYZE_MGE (Orchestrator)
```
1. calc-household-aggregate    → Full household financial snapshot
2. [detect applicable types]   → Which of the 8 types are relevant based on household data?
3. [call relevant ANALYZE_*]   → Run each applicable analysis
→ OUTPUT: Household summary + list of applicable casework types with preliminary findings
```

### Shared Super Tools (Phase 3 — run inside QUE_RECOMMEND)

#### GENERATE_CASEWORK
```
1. generate-summary-html       → Tier 1 one-pager for each applicable casework type
2. generate-detail-html        → Tier 2/3 year-by-year (flagged as "on demand")
→ OUTPUT: Summary HTML + Detail HTML per casework type
```

#### ASSEMBLE_OUTPUT
```
1. generate-ai3-pdf            → Household AI3 (Output 1)
2. [collect IFIs + reports]    → Organized carrier docs (Output 2)
3. [collect illustrations]     → Product illustrations (Output 3)
4. [collect casework]          → All generated casework components (Output 4)
5. generate-factfinder         → Pre-filled application package (Output 5)
6. html-to-pdf                 → Convert all HTML to PDF
7. file-to-acf                 → Upload everything to household ACF B4 folder
→ OUTPUT: Complete 5-output package in ACF B4
```

---

## QUE Wires — Phase 2+3 (QUE Layer 3)

| Wire | Super Tool Sequence | Trigger |
|------|-------------------|---------|
| `WIRE_INCOME_NOW` | ANALYZE_INCOME_NOW → GENERATE_CASEWORK | Dormant income riders detected |
| `WIRE_INCOME_LATER` | ANALYZE_INCOME_LATER → GENERATE_CASEWORK | Rollup opportunity detected |
| `WIRE_ESTATE_MAX` | ANALYZE_ESTATE → GENERATE_CASEWORK | Life policies approaching lapse |
| `WIRE_GROWTH_MAX` | ANALYZE_GROWTH → GENERATE_CASEWORK | VA bleeding fees or idle CDs |
| `WIRE_LTC_MAX` | ANALYZE_LTC → GENERATE_CASEWORK | Multi-contract LTC portfolio |
| `WIRE_ROTH_CONVERSION` | ANALYZE_ROTH → GENERATE_CASEWORK | Large traditional IRA balances |
| `WIRE_TAX_HARVEST` | ANALYZE_TAX_HARVEST → GENERATE_CASEWORK | NQ liquidation needed |
| `WIRE_MGE_DETAILED` | ANALYZE_MGE → GENERATE_CASEWORK | Full review / discovery meeting |
| `WIRE_REVIEW_MEETING` | ANALYZE_MGE → generate-meeting-prep → file-to-acf | Scheduled review meeting |
| `WIRE_ASSEMBLE_B4` | ASSEMBLE_OUTPUT | All casework wires complete — package and file |

### Pipeline Studio Integration

```
Yellow Stage Pipeline (configured in Pipeline Studio):
┌──────────────────────────────────────────────────────────────┐
│ Stage: "Analysis"                                             │
│   Trigger: Household enters stage                             │
│   Action: Fire WIRE_MGE_DETAILED                              │
│   Result: Determines which casework types are applicable      │
├──────────────────────────────────────────────────────────────┤
│ Stage: "Case Building"                                        │
│   Trigger: MGE analysis complete                              │
│   Action: Fire applicable wires in parallel:                  │
│     - WIRE_GROWTH_MAX (if VA detected)                        │
│     - WIRE_INCOME_NOW (if dormant GMIB detected)              │
│     - WIRE_ESTATE_MAX (if lapse risk detected)                │
│     - WIRE_LTC_MAX (if multi-contract LTC detected)           │
│   Result: All casework components generated                   │
├──────────────────────────────────────────────────────────────┤
│ Stage: "Package Assembly"                                     │
│   Trigger: All casework wires complete                        │
│   Action: Fire WIRE_ASSEMBLE_B4                               │
│   Result: 5 outputs filed to household ACF B4                 │
├──────────────────────────────────────────────────────────────┤
│ Stage: "Case Ready"                                           │
│   Trigger: Assembly complete                                  │
│   Gate: DEX_PACKAGE_FILED (all 5 outputs exist in ACF B4)     │
│   Action: Notify specialist: "Mineart household ready"        │
│   Result: → Green Stage                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## The 8 Casework Types — Detailed Discovery

### Type 1: INCOME NOW

**When to use:** Client needs income activated immediately from existing or proposed products.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Shared Drive | ANNUITY- Income Comparison | Google Sheet | Active — VA vs FIA side-by-side |
| Shared Drive | ANNUITY- Income Portfolio Analysis | Google Sheet | Active — $1.4M portfolio, 7.28% BEP |
| Shared Drive | RETIREMENT- Income Strategy.BASIC | Google Sheet | Active — 24-year projection |
| Claude.AI | Retirement Income Strategy templates | 4 HTML files | Production (Demetry, Anders) |
| Claude.AI | Demetry Income Calculator | Interactive HTML | Dark-themed |
| Shared Drive | Claude- FIA GMIB Activation Analysis | PDF (422KB) | Claude output |

**Key Business Logic:**

Income Comparison (VA vs FIA):
- Compares ALL-IN cost: M+E+A Fee + GMIB Fee + GMDB Fee
- Year-by-year projection showing income growth differential
- Benefit Base grows via rollup rate (simple or compound)
- First year bonus inflates starting benefit base
- Income % = Income $ / Starting Account Value

Portfolio Yield Analysis:
- YIELD-Gross = Income / Value (before fees)
- YIELD-Net = (Income - Advisory Fees) / Value
- PRINCIPAL impact = Income - Fees - Withdrawals (negative = erosion)
- KILLER METRIC: EQUITY % for Breakeven = return needed to avoid losing principal
- If BEP > 7-8%, client is guaranteed to run out of money

Summary Version: Current income vs proposed, fee comparison, income gap/surplus, "your money lasts X years longer"
Detail Version: Year-by-year starting value → income → fees → growth → ending value, running delta, income as % of balance
Supporting: GLWB activation timing, split-start optimization, NAC 2x LTC multiplier break-even

**Process Doc Status:** Ready to build

---

### Type 2: INCOME LATER

**When to use:** Client has an annuity with income rider not yet activated. Strategy: defer for rollup growth, possibly redirect future income to fund life insurance.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Collateral | CASEWORK-PROCESS-GMIB-TO-LIFE.md | Process Doc | COMPLETE |
| Collateral | RPI-Strategic-Life-Insurance-Funding-Analysis.html | HTML Template | COMPLETE |
| Collateral | RPI-STRATEGIC-FUNDING-ANALYSIS-HANDOFF.md | Handoff Doc | COMPLETE |
| Shared Drive | RETIREMENT- Income Strategy.DETAILED | Google Sheet | Active — CURRENT vs PROPOSED |
| Shared Drive | Retirement Growth+Income+Legacy Strategy | Google Sheet | Master 3-bucket |
| Shared Drive | RETIREMENT- NEAP + NEBF | Google Sheet | IBEW-specific (3 scenarios) |

**Key Business Logic:**

Roll-Up Math:
```
Current benefit base × payout rate at current age = Current annual GMIB
Benefit base × (1 + roll-up rate) = Benefit base after 1 year
New benefit base × payout rate at (current age + 1) = New annual GMIB
Difference = Additional guaranteed lifetime income per year of deferral
```

3-Option Framework:
| Option | Strategy | Premium Source | Tax Handling |
|--------|----------|---------------|--------------|
| A | Start now | GMIB funds premium | Taxes from bank reserves |
| B | Wait + net of taxes | Inheritance bridges Year 1 | Minimal OOP |
| C | Wait + full GMIB | Inheritance bridges Year 1 | Taxes from bank |

**Process Doc Status:** COMPLETE

---

### Type 3: ESTATE MAX

**When to use:** Client has life insurance approaching lapse, inadequate death benefit, or 1035 repositioning opportunity.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Claude.AI | DeGeeter Estate Scenarios | Production HTML | 15-year projection, lapse detection |
| Claude.AI | Mineart 3-Option Estate Comparison | 2 HTML versions | Current vs Roth vs Estate Max |
| Shared Drive | LIFE- Family Needs Calculator | Google Sheet | Age-based multiplier, survivor scenarios |
| Shared Drive | LIFE- UL Case Matrix | Google Sheet | 14 carriers, FYC rates |
| Shared Drive | ANNUITY- VA DB Illustration | Google Sheet | VA burn-rate projection |

**Key Business Logic:**

15-Year Household Projection:
- Color-coded ownership: Pink = wife, Blue = husband, Yellow = joint
- Categories: Life (CV + DB), IRAs, Roths, Joint NQ, Real Estate
- Investable Assets = Sum of all CVs + IRAs + Roths + Bank
- Estate Value = Sum of all DBs + IRAs + Roths + Banks + Residence

Lapse Detection:
- If guaranteed lapse age < life expectancy → FLAG for 1035
- Death Benefit Erosion = Sum of DB lost to lapse across all policies
- Repositioning targets: COF Value 4 Life, NAC BenefitSolutions

Family Needs Calculator:
- Age-based income multiplier: 20-39=30x, 40-44=25x, 45-49=20x, 50-54=15x, 55-59=12x, 60-69=10x, 70+=5x
- Needs = Income Replacement + Debt + College + Misc - Existing Coverage
- College = $35,331 × (1 + 6.80%)^(18-age) × 4 years
- Two survivorship scenarios: "A Survives B" and "B Survives A"

Carrier FYC Rates (UL Case Matrix):
| Carrier | Target % | Excess % | Preferred? |
|---------|----------|----------|-----------|
| CoF | 80.0% | 10.00% | Yes |
| JH | 95.0% | 1.50% | Yes |
| MOO | 95.0% | 2.00% | Yes |
| AIG | 104.8% | 2.50% | |
| ALIC | 119.8% | 3.75% | |
| F&G | 124.8% | 3.00% | |
| KCL | 120.0% | 3.00% | |
| LFG | 109.8% | 5.00% | |
| NAC | 109.8% | 4.50% | |
| NWF | 109.8% | 3.00% | |
| PRO | 109.8% | 4.00% | |
| SYM | 119.8% | 5.00% | |

**Process Doc Status:** Ready to build

---

### Type 4: GROWTH MAX

**When to use:** Client has a VA bleeding fees, or CDs/bank money that could grow faster in an FIA.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Shared Drive | ANNUITY- GROWTH MAX | Google Sheet | VA $0 at 91, FIA $257K at 92 |
| Shared Drive | ANNUITY- VA DB Illustration | Google Sheet | Fund-level returns, depletion at 87 |
| Shared Drive | ANNUITY- Index + MVA Calcs | Google Sheet | 10 carriers, 17 indexes |
| Claude.AI | FIA MVA Calculator | 5 React iterations | Reverse-engineers MVA |
| Claude.AI | Portfolio Consolidation templates | 4 HTML files | Sebetka $579K, Stuart $548K |

**Key Business Logic:**

VA vs FIA Sustainability:
```
Existing VA: NET Return = Gross (6.04%) - M+E+A (1.65%) = 4.39%
  Ending Value = (Starting - Income) × (1 + Net Return) → hits $0 at age 91
Proposed FIA: Starting = Deposits × (1 + First Year Bonus)
  Growth at 5% hypo, 0% M+E+A → still $257K at age 92
DELTA = FIA Value - VA Value (grows every year)
```

Consolidation Cost/Bonus Offset:
```
Surrender Charge + LTCG = Gross Cost
Gross Cost - Nassau 7% Bonus = Net Cost (OFTEN NEGATIVE = net gain to client)
```

Account-Type Matching: ROTH→ROTH NGA, IRA→IRA NGA, NQ→Nassau Bonus, Inherited (stepped-up basis)→$0 LTCG

MVA Reverse-Engineering:
```
Total NET CSV Penalty = (AV - SV) / AV × 100
Decompose: Free Withdrawal (10%) + Surrender Charge + hidden MVA
MGSV Floor = 87.5% of premiums at 3% interest
```

FIA Product Reference (Index + MVA Calcs sheet):
- 10 carriers: Ameritas, Corebridge (x2), Delaware (x2), F&G (x3), NAC (x2)
- 17 indexes: Barclays Trailblazer, Goldman Sachs TimeX, S&P 500, PIMCO, etc.
- 4 methods: Annual Point-to-Point, Monthly Averaging, Trigger, Monthly Sum
- Factors: Cap (0-9.85%), Participation Rate (10-350%), Spread, Fee (0.25-5%)

North American 11-year surrender schedule: 10/10/9/9/8/8/7/6/4/2/0

**Process Doc Status:** Ready to build

---

### Type 5: LTC MAX

**When to use:** Client has multiple contracts with LTC access features. Map the full pool and access sequence.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Claude.AI | LTC Access Analysis (Connell) | 2 HTML presentations | 4-phase framework |
| Shared Drive | CONCEPT- LTC MAX! | Excel | Not yet scanned |
| Shared Drive | LTC- HYBRID Life + FIA Comparison | Excel | Not yet scanned |
| Shared Drive | LIFE- FE v TERM v IUL | Google Sheet | LTC rider comparison |

**Key Business Logic — 4-Phase Access Framework (Proprietary RPI):**

| Phase | Qualification | What's Accessible | Example |
|-------|--------------|-------------------|---------|
| **I** | No qualification | Enhanced withdrawal | 20% of AV, every-other-year |
| **II** | ADL-triggered | Income multiplier | 2x base income |
| **III** | ADL-triggered | Enhanced liquidity | Full SV + enhanced income |
| **IV** | Confinement/Terminal | Full account access | 100% of AV |

Calculations:
- Phase I Access = Account Value × 20% (every-other-year restriction)
- Phase II Income = Base Income × 2 (ADL multiplier)
- Total Annual Fees = Sum across all contracts
- Break-Even: 2x multiplier justifies lower base after < 1 year of care

FE v TERM v IUL Comparison:
| Metric | Final Expense (MOO) | Term-20 (TransAm) | IUL (JH) |
|--------|--------------------|--------------------|-----------|
| Monthly Premium | $257 | $592 | $1,134 |
| 20-Year Net Outlay | $32,468 | $142,188 | $135,514 |
| Year 21 DB (each) | $25,000 | $0 | $250,000 |
| LTC Monthly (x25) | $0 | $0 | $10,000 |

**Process Doc Status:** Ready to build

---

### Type 6: MGE - DETAILED Analysis

**When to use:** Full financial picture review — the comprehensive case that feeds ALL other types.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Collateral | CASEWORK-PROCESS-CLIENT-REVIEW-MEETING.md | Process Doc | COMPLETE |
| Collateral | RPI-Client-Review-Meeting-Template.html | HTML Template | COMPLETE |
| Shared Drive | CONCEPT- Asset Types Overview | Google Sheet | 3-bucket model |
| Shared Drive | CONCEPT- Balanced Retirement Portfolio | Google Sheet | 4-quadrant |
| Shared Drive | CONCEPT- Accumulation vs Distribution | Google Sheet | Teaching framework |
| Claude.AI | Ai3 Framework Definition | Memory doc | The methodology |

**Key Business Logic:**

3-Bucket Asset Model:
| | Safety | Liquidity | Growth |
|--|--------|-----------|--------|
| **Bank** | Yes | Yes | No |
| **Institutional** (FIA/MYGA) | Yes | No | Yes |
| **Fiduciary** (RIA) | No | Yes | Yes |

Rule: "Pick 2 of 3" — No asset delivers all three.
RPI Sales Motion: Move over-concentrated fiduciary → institutional.

4-Quadrant Portfolio:
| | NOW (0-10 years) | LATER (10+ years) |
|--|-------------------|---------------------|
| **Liquidity/Growth** | Market-exposed, accessible | Long-term growth |
| **Income Foundation** | Guaranteed floor (FIA, pension, SS) | Deferred income riders |

Ai3 = Assets / Income / Insurance / Inventory — the master methodology.

**Process Doc Status:** COMPLETE

---

### Type 7: ROTH Conversion

**When to use:** Client has large traditional IRA balances. Model bracket impact, IRMAA consequences, break-even timeline.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Shared Drive | ANNUITY- ROTH Conversion Analysis | Google Sheet | EMPTY template |
| Shared Drive | !RETIREMENT- PROV+FEDS+STATE | Google Sheet | THE TAX ENGINE |
| Shared Drive | MEDICARE- IRMAA Calculator | Google Sheet | Surcharge by MAGI |
| Shared Drive | RETIREMENT- Full Retirement Age SS Calc | Google Sheet | Earnings limit |

**Key Business Logic:**

Provisional Income:
```
= 50% of Social Security
+ Taxable Pensions/Wages
+ Interest/Dividends
+ IRA Conversions/Distributions  ← makes Roth conversions expensive
+ Tax-Exempt Income

SS Taxation Brackets (MFJ):
  $0-$32K: 0% taxable
  $32K-$44K: 50% taxable
  $44K+: 85% taxable
```

2025 Federal Tax Brackets (MFJ):
10% ($0-$23,850), 12% ($23,851-$96,950), 22% ($96,951-$206,700), 24% ($206,701-$394,600), 32% ($394,601-$501,050), 35% ($501,051-$751,600), 37% ($751,601+)

2025 IRMAA Brackets (MFJ):
$0-$212K (none), $212K-$265K, $265K-$332K, $332K-$398K, $398K-$750K, $750K+ (max)

Special: VA disability pension (partial taxable/partial exempt), FERS pension (fully taxable), IRA conversions push SS taxation from 50%→85%

SS Earnings Limit (Pre-FRA): $1 withheld per $2 above $21,240 (2023), MAX Earnings = Limit + (Yearly Benefit × 2)

**Process Doc Status:** Ready to build (Tax Engine exists, ROTH template needs population)

---

### Type 8: Tax Harvesting

**When to use:** Client needs to liquidate a specific dollar amount from NQ brokerage/advisory account. Minimize tax.

**Components Found:**

| Source | Component | Type | Status |
|--------|-----------|------|--------|
| Claude.AI | Tax-Efficient Liquidation templates | 4 HTML files | $115K, $60K, full, IRA transfer |
| Claude.AI | Tax Harvesting project | Process + workflow | 4-phase defined |
| Shared Drive | Claude- Portfolio Liquidation Analysis | PDF (365KB) | Claude output |
| Shared Drive | Claude- CaseWork.INPUTS | Google Sheet | Automation recipe |

**Key Business Logic:**

NQ Strategy: Sort by gain%, sell lowest first (losses → smallest gains) until target reached. Net loss offsets other gains, then $3K ordinary income deduction, carry forward.

IRA Strategy (inverted): Sort by gain% but sell underperformers to preserve winners. Tax is identical regardless of lots (all ordinary income). Goal: keep best performers.

IRA Direct Transfer: Same lot selection, zero-tax (trustee-to-trustee), "no 60-day clock."

Key Calculations: Effective Tax Rate = Tax / Proceeds × 100. NIIT at 23.8% above $250K MAGI MFJ.

Compliance: All outputs require RPI + Signal Advisors Wealth disclosure.

**Process Doc Status:** Ready to build

---

## Phase 3: The Five Yellow Stage Outputs

Everything from Phase 2 feeds into five deliverables filed to household ACF B4.

### Output 1: Client-Facing AI3 PDF
**Status:** Process exists, standardized template needed
- Clean Ai3 — internal sections removed, recommendations highlighted, exec summary, specialist talking points
- Data: household demographics, asset inventory, life insurance, income, financial summary
- Source: `households/{id}` aggregate_financials + per-member account data

### Output 2: Reports + In-Force Illustrations
**Status:** Process documented, tools in place
- Ameritas IFI: 10-step process with Loom video
- IFI TypeScript interface: 24 fields (policyNumber through currentLapseAge)
- UL Case Matrix: 14 carriers with illustration instructions
- SIGNAL outputs: 17 sample PDFs (RightCapital, Riskalyze, etc.)
- External tools: WinFlex, ARW, Index Standard, Nitrogen, MoneyGuidePro, Signal Wealth

### Output 3: Product Illustrations
**Status:** Tools exist, templates partial
- Income Comparison (VA vs FIA), GROWTH MAX (depletion vs sustainability)
- FE v TERM v IUL (3-option life), Primerica Term Conversion (3 scenarios)
- Index + MVA Calcs (product/rate lookup), FIA MVA Calculator (5 iterations)
- Needed: standardized one-pager format per product type

### Output 4: Casework Components
**Status:** Most complete — the bulk of this document
- 40 components found across 8 types
- 2 complete process docs, 5 ready to build, 1 blocked (ROTH template empty)
- Summary + Detail versions per type with progressive disclosure

### Output 5: RPI Factfinder
**Status:** Referenced but not located
- Called "RPI 2025 Factfinder" in Yellow Stage guide
- Three auth types: Life, Wealth, ITS
- Goes into B4 as final output
- Needed: locate template, digitize, pre-fill from Firestore

---

## Cross-Cutting Reference Data

### Carrier Contact Directory

| Carrier | Service Email | Fax |
|---------|--------------|-----|
| Nassau | customerservice@nsre.com, transactions@nsre.com | 785-368-1386 |
| ManhattanLife | customerservice@manhattanlife.com | 713-402-2803 |
| F&G | customerservice@fglife.com, allocations@fglife.com | 888-417-3702 |
| North American | customerservice@nacolah.com, beneficiary@nacolah.com | 877-586-0244 |
| Kansas City Life | billing@kclife.com, policychanges@kclife.com | — |
| Universal Life | customerservice@ulins.com | 847-699-0895 |
| Charles Schwab | advisorbeneficiary@schwab.com | — |

### Document Classification (18 Types)
Transaction Confirmation, Address Change, Delivery Receipt, RMD, Direct Deposit, Allocation Change, Beneficiary Change, Contract Issuance, Maturity Notice, Auto Withdrawal, General Information, Lapse Protection, Policy Change, Banking Change, Allocation Option, Income Payments, Annual Statement, Partial Surrender, Tax Withholding, Policy Replacement

### PDF Naming Convention
`Document Type.[Year]- Policy/Contract# CLIENT_NAME Carrier.pdf`

### Community Property States
AK, AZ, CA, ID, LA, NM, NV, TX, WA, WI

---

## Shared Drive Location Reference

| Item | Folder ID |
|------|-----------|
| B2C Shared Drive Root | 0AFdBtrmK-amnUk9PVA |
| *Service Unit | 1HE8MiA-Dy3PbCVhYDr0l0mmvmftfLnSl |
| Active Client Files | 1g3lyRPnsWu0opfyv0vUiZTBEJoEhrP4m |
| *CASE Data | 1N9FXkCy_GcGeUbzUuNUqFOIwGITKqT7X |
| *CaseWork- Components | 1BXJsTtg3RkEaqtlVhWDtbUnB1JYSTv1U |
| Claude- CaseWork Templates | 1SXXCFkz_QdAatI7rbCqrjQQLU18DxC8e |
| SIGNAL- CaseWork Outputs | 1-mF6wSEdBU8h_xnkmYokU8HerK0mqvcO |
| RMD INFO subfolder | 19o_y6PBZbF5uz1hGg9JW4igBZfptI2b0 |

---

## Items Still Needing Scan

- 6 Excel files in *CaseWork- Components (FIA Head2Head, Premium Deposit Fund, LTC MAX!, LTC HYBRID, Med Supp Trends, Medicare 30k/Detail/BlueButton)
- 4 visual-only Google Sheets (LEP Calculator, OneIN-OneOUT, T65 Checklist, VA Rx Calculator)
- 2 sheets with non-default tabs (RMD/IRA MAX, Retirement Checklist)
- RPI Factfinder template (Output 5 — referenced but not located)
- Individual client CaseWork folders (30+ on Shared Drive — patterns to extract)

---

## Build Scope Summary

**Phase 2 (the work):**
- Implement 25 calc-* tools as QUE atomic functions
- Implement 8 lookup-* tools with carrier/tax/IRS data
- Wire 8 ANALYZE_* super tool sequences
- Build 5 remaining CASEWORK-PROCESS-*.md files
- Create Summary + Detail HTML templates for each of 8 casework types
- Register all tools in QUE tool registry

**Phase 3 (the layup):**
- Implement 5 generate-* tools (AI3 PDF, meeting prep, factfinder, summary HTML, detail HTML)
- Wire GENERATE_CASEWORK and ASSEMBLE_OUTPUT super tools
- Wire WIRE_ASSEMBLE_B4
- Locate and digitize RPI Factfinder (Output 5)
- File everything to household ACF B4 via DEX

---

*This discovery file is the specification for building the casework component and output layers of QUE within toMachina. Every formula, template, and process documented here becomes a registered QUE tool. ATLAS feeds the data in. QUE analyzes and builds. DEX outputs the deliverables. Pipeline Studio orchestrates the flow. Householding is the unit everything operates on.*
