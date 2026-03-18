# Casework Process: Estate MAX — Estate & Legacy Planning

**Created:** 2026-03-17
**Source Cases:** DeGeeter Estate Scenarios (15-year projection), Mineart 3-Option Estate Comparison, Family Needs Calculator
**Purpose:** Repeatable process for identifying lapsing life policies, inadequate death benefits, and 1035 exchange opportunities.

---

## When This Process Applies

- Client has life insurance approaching guaranteed lapse age
- Death benefit is inadequate relative to survivor income needs
- 1035 exchange opportunity exists (repositioning to no-lapse product)
- VA death benefit is eroding due to fee drag

---

## Step 1: Gather the Source Data

### From the ACF
| Document | What You Need |
|----------|--------------|
| **Life Policy Illustrations** | Current DB, CV, premium, guaranteed lapse age, policy type |
| **VA Account Statements** | AV, death benefit, fee schedule, fund returns |
| **Family/Survivor Info** | Dependents, ages, college plans, survivor income needs |

### Key Numbers
- Per policy: Death Benefit, Cash Value, Annual Premium, Guaranteed Lapse Age
- Per member: Age, Annual Income, Life Expectancy
- Per dependent: Age, College plans (years until college)

---

## Step 2: Run the Estate Analysis

### Lapse Detection
```
If Guaranteed Lapse Age < Life Expectancy → FLAG for 1035 exchange
Years to Lapse = Guaranteed Lapse Age - Current Age
DB at Risk = Sum of all flagged Death Benefits
```

### Survivor Needs (Income Multiplier Method)
```
Age-based multipliers: 20-39=30x, 40-44=25x, 45-49=20x, 50-54=15x, 55-59=12x, 60-69=10x, 70+=5x
Recommended Coverage = Annual Income x Multiplier
College Funding = $35,331 x (1 + 6.80%)^(18 - child age) x 4 years
Total Need = Income Replacement + College + Debt - Existing Coverage
Gap = Total Need - Current Coverage
```

### VA Death Benefit Erosion
Project VA accounts forward 30 years:
```
Net Return = Gross Return - Total Fee Rate
Ending = (Starting - Withdrawal) x (1 + Net Return)
If ending hits $0 → Death Benefit erodes
```

---

## Step 3: Identify 1035 Exchange Candidates

For each lapsing policy:
1. Calculate remaining cash value available for 1035
2. Look up replacement product options (COF Value 4 Life, NAC BenefitSolutions)
3. Compare: current lapse timeline vs. guaranteed no-lapse replacement
4. Use FYC Rate lookup to compare carrier compensation

### Preferred Carriers (from UL Case Matrix)
| Carrier | Target % | Excess % | Preferred |
|---------|----------|----------|-----------|
| CoF | 80.0% | 10.00% | Yes |
| JH | 95.0% | 1.50% | Yes |
| MOO | 95.0% | 2.00% | Yes |
| NAC | 109.8% | 4.50% | |

---

## Step 4: Build the Presentation

### Template
Use `generate-summary-html` with type `estate_max` for the Tier 1 one-pager.
Use `generate-detail-html` with type `estate_max` for 15-year household projection.

### Color-Coded Ownership (Detail Template)
- Pink = Wife's assets
- Blue = Husband's assets
- Yellow = Joint assets

---

## Step 5: Quality Check

- [ ] Guaranteed lapse ages verified against actual policy documents
- [ ] Income multipliers match the correct age bracket
- [ ] College funding uses 6.80% inflation rate
- [ ] 1035 candidates verified for tax-free exchange eligibility
- [ ] Two survivorship scenarios analyzed ("A Survives B" and "B Survives A")

---

## Step 6: Deliver

1. Generate HTML via `wireEstateMax`
2. DEX converts to PDF
3. File to ACF B4
4. Present alongside carrier illustrations at A+R meeting

---

## Tools Used

| Tool | QUE Registry ID |
|------|----------------|
| calc-va-depletion | `calc-va-depletion` |
| calc-income-multiplier | `calc-income-multiplier` |
| calc-college-funding | `calc-college-funding` |
| lookup-fyc-rate | `lookup-fyc-rate` |
| ANALYZE_ESTATE | `ANALYZE_ESTATE` |
| WIRE_ESTATE_MAX | `WIRE_ESTATE_MAX` |
