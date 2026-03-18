# Casework Process: GMIB/GLWB Annuity → Life Insurance Funding Analysis

**Created:** 2026-03-16
**Source Case:** Stephen & Joyce Mineart (Nassau Income Accelerator → JH Survivorship IUL)
**Purpose:** Repeatable process for developing a strategic funding analysis when redirecting annuity guaranteed income to fund life insurance.

---

## When This Process Applies

- Client has an annuity with a GMIB, GLWB, or GMWB rider
- Strategy is to redirect the guaranteed withdrawal to fund a life insurance policy
- Multiple illustration scenarios need to be compared
- Client-facing presentation is needed for the recommendation meeting

---

## Step 1: Gather the Source Data

### From the ACF (Active Client File on Google Drive)
Pull these documents from the client's account folder:

| Document | What You Need From It |
|----------|----------------------|
| **Carrier Account Value Statement** | Current account value, benefit base, rider status (activated or not), fee schedule, index allocations |
| **Original Contract PDF** | Rider specification pages (usually near the end): roll-up rate table, payout percentage table by age, bonus percentages, rider fee, roll-up period, max restarts |
| **Existing Life Insurance Illustrations** | Insured details (ages, classes, ratings), product, premium levels, death benefits, growth rate assumptions, DB protection guarantee period |

### From records.csv / Firestore
- Account number, carrier, product name, issue date, tax status (IRA/NQ), joint owner, beneficiaries

### Key Numbers to Extract

**From the annuity contract rider specifications:**
- Benefit base (phantom ledger, not account value)
- Roll-up rate (% per year, simple or compound)
- Roll-up period (years remaining)
- Payout percentage table (by attained age of youngest covered person)
- Rider fee (% of benefit base)
- Whether rider is activated or not

**From the life insurance illustration:**
- Both insureds: name, sex, age, underwriting class, table rating
- Product form number
- Assumed segment growth rate
- DB option (Level vs Increasing)
- Premium mode (Annual)
- Vitality/wellness status
- State of issue
- Target cash value assumptions

---

## Step 2: Do the Roll-Up Math

If the rider is NOT yet activated, calculate the impact of deferring activation:

```
Current benefit base × payout rate at current age = Current annual GMIB

Benefit base × (1 + roll-up rate) = Benefit base after 1 year
New benefit base × payout rate at (current age + 1) = New annual GMIB

Difference = Additional guaranteed lifetime income per year of deferral
Lifetime value = Difference × joint life expectancy
```

**Key insight to check:** Does the client have cash on hand (inheritance, bank reserves, other assets) to bridge the premium during the deferral period? If yes, the roll-up is essentially "free money."

### Tax Math for Each Option

```
GMIB withdrawal × combined tax rate (federal + state) = Annual tax
GMIB - premium to life policy = Remainder toward taxes
Annual tax - remainder = Annual out-of-pocket from bank reserves
```

---

## Step 3: Define the Options

Standard 3-option framework:

| Option | Strategy | When to Activate | Premium Source | Tax Handling |
|--------|----------|-----------------|----------------|--------------|
| **A** | Start now | Immediately | GMIB funds premium | Taxes from bank reserves |
| **B** | Wait + net of taxes | After 1+ roll-ups | Inheritance bridges Year 1, then GMIB net of taxes funds premium | Taxes deducted from GMIB, minimal OOP |
| **C** | Wait + full GMIB | After 1+ roll-ups | Inheritance bridges Year 1, then full GMIB to premium | Taxes from bank reserves |

Option B is typically recommended when the net-of-taxes GMIB amount closely matches an existing illustration premium level (e.g., $6M face amount). The GMIB self-funds the policy.

Option C is the aggressive play — maximum death benefit, but highest annual OOP.

---

## Step 4: Run the Life Insurance Illustration (Winflex)

### Inputs to Verify (Line-by-Line Against Existing Illustration)

| Category | Fields |
|----------|--------|
| **First Insured** | Name, Sex, Age, Class, Permanent Percentage (table rating), Flat Extra, State |
| **Second Insured** | Name, Sex, Age, Class, Flat Extra |
| **Solve For** | Solve type (Face Amount vs Premium vs No Solve), Premium amount, Vitality status (both insureds), Target CV, Target CV age |
| **Assumed Rate** | Allocation option, Base Capped Rate, allocation percentages, Fixed Rate |
| **Policy Options** | DB Option (Level), Premium Mode (Annual), Charges (Current), Prevent MEC |
| **Policy Riders** | Estate Preservation Rider, Cash Value Enhancement, Return of Premium DB |

### Solve Settings for "Max Face at Given Premium"
- Solve For: **Face Amount**
- Total Face Amount: **Max DB to Endow/Target**
- Premium: **[specified amount]** (e.g., $145,000)
- Target Cash Value: **$1,000** / Endow
- Target Cash Value Year/Age: **Age 100** (youngest insured)

### After Calculation — Record These Results
- Initial Death Benefit (face amount)
- Initial Annual Premium
- Target Premium
- Guaranteed Years
- Premium Pay Years
- Year-by-year table (at minimum: years 1, 5, 10, 15, 20, 24/JLE, 30)

### Save the Illustration
- Download PDF from Winflex results
- Save to Desktop with naming convention: `[Client] JH Backdated + $[Premium].pdf`
- Upload to client's ACF folder on Google Drive

---

## Step 5: Build the HTML Presentation

### Template
`~/Projects/_RPI_STANDARDS/reference/collateral/RPI-Strategic-Life-Insurance-Funding-Analysis.html`

### 4-Page Structure

**Page 1 — Cover**
- Client names, date, policy status, advisor name
- Source product → Target product

**Page 2 — The Opportunity + Roll-Up**
- Current benefit base and roll-up rate
- Side-by-side: activate now vs. wait (with exact dollar amounts)
- Explain how inheritance/cash bridges the gap
- Key insight: no withdrawal in Year 1 = no taxes + roll-up

**Page 3 — Three Options Comparison**
- Side-by-side table: A / B (recommended) / C
- Rows: strategy, Year 1 source, taxes, GMIB after roll-up, premium, OOP, death benefit, DB guarantee
- Money flow diagram for recommended option
- OOP comparison metric cards

**Page 4 — The Math**
- Lifetime cost comparison table (24-year JLE)
- Total OOP per option, cost per $1M of death benefit
- IRA vs Life Insurance comparison (tax-deferred vs tax-free)
- Bottom line metric cards

### Design System
- Font: Inter (Google Fonts), weights 300-800
- Colors: `--navy: #1a3158`, `--rpi-blue: #4a7ab5`, `--pale-blue: #e5ecf6`, `--gold: #c5a55a`, `--green: #16a34a`
- Print: Letter size, 0.5in/0.6in margins, `print-color-adjust: exact`
- Body text: 11pt minimum (senior audience)
- Logo: `rpi-shield.png` co-located with HTML

### Variables to Parameterize
See `RPI-STRATEGIC-FUNDING-ANALYSIS-HANDOFF.md` for the full variable table. Key ones:
- Client names, advisor name, prepared date
- GMIB amount, contract number, benefit base, roll-up rate
- Tax bracket, estimated annual tax
- Each option's premium, death benefit, OOP
- Lifetime cost calculations

---

## Step 6: Quality Check

Before delivering to the advisor:

- [ ] All numbers trace back to contract documents or Winflex output
- [ ] Tax calculations use correct combined rate (federal + state)
- [ ] Roll-up math verified: benefit base × (1 + rate) × payout percentage = annual income
- [ ] Lifetime OOP = Year 1 cost + (Annual OOP × remaining years)
- [ ] Cost per $1M = Total lifetime OOP / (DB / $1,000,000)
- [ ] Winflex inputs verified line-by-line against existing illustration
- [ ] Illustration PDF saved to Desktop AND uploaded to ACF
- [ ] HTML renders correctly in browser (check all 4 pages)
- [ ] Footnotes cite specific contract numbers, illustration dates, and assumptions
- [ ] No PHI in filenames or external-facing content beyond what's in the presentation

---

## Step 7: Deliver

1. Print HTML to PDF from Chrome (File → Print → Save as PDF)
2. File PDF to ACF in the client's Active Accounts → Retirement → [account] folder
3. Advisor presents alongside the JH illustrations at the client meeting

---

## Tools Used in This Process

| Tool | Purpose |
|------|---------|
| **Google Drive (gdrive MCP)** | Access ACF folder, list/download client documents |
| **Playwright** | Read contract PDFs via Drive viewer, run Winflex illustrations, upload files to Drive |
| **Winflex Web** | Generate JH Protection Survivorship IUL illustrations at different premium levels |
| **HTML/CSS** | Build the client-facing presentation (RPI brand design system) |
| **Nassau carrier portal** | Account value statements (downloaded to ACF) |

---

## Future: Automated Generation (toMachina)

When the casework pipeline is wired in toMachina:
- Flow stage trigger generates this output automatically
- Client data pulled from Firestore (accounts collection)
- Contract rider terms stored in structured format (benefit base, roll-up rate, payout table)
- Illustration data parsed from uploaded PDFs (or Winflex API if available)
- HTML rendered server-side → PDF via Puppeteer/Chrome
- Filed to ACF via Drive API
- Advisor gets notification: "[Client] strategic comparison ready for review"

This manual process document is the specification for that automation.
