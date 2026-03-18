# Casework Process: Income NOW — Immediate Income Activation

**Created:** 2026-03-17
**Source Cases:** Demetry Income Calculator, Anders Retirement Income Strategy, Income Portfolio Analysis
**Purpose:** Repeatable process for activating dormant income riders and optimizing current income streams.

---

## When This Process Applies

- Client has an annuity with a dormant GMIB, GLWB, or GMWB rider (not yet activated)
- Client needs income now from existing products
- Portfolio breakeven equity rate exceeds 7% (unsustainable withdrawal rate)
- RMD requirements create forced distributions that could be better coordinated

---

## Step 1: Gather the Source Data

### From the ACF
| Document | What You Need |
|----------|--------------|
| **Carrier Account Value Statement** | Current AV, benefit base, rider status, fee schedule |
| **Contract Rider Specifications** | Payout rate table by attained age, activation requirements |
| **Income Portfolio Analysis** | Current yield-gross, yield-net, breakeven equity % |

### From Firestore
- Account records: carrier, product, AV, benefit base, payout rate, rider status
- Household aggregate: total income, investable assets, net worth

### Key Numbers
- Benefit Base (phantom ledger, NOT account value)
- Payout Rate at current attained age
- All-in fees (M+E+A + GMIB + GMDB)
- Current withdrawals from each account
- Breakeven equity rate per account

---

## Step 2: Run the Income Analysis

### Dormant Rider Identification
For each account with a dormant rider:
```
Annual Income = Benefit Base x Payout Rate (at current age)
Monthly Income = Annual / 12
```

### Breakeven Equity Calculation
```
BEP = (Annual Withdrawals + Annual Fees - Income Credits) / Portfolio Value
If BEP > 7% → WARNING: Portfolio will deplete
```

### Income Gap/Surplus
```
Total Available Income = Active Rider Income + Dormant Rider Income
Income Gap = Total Expenses - Total Available Income
```

---

## Step 3: Evaluate Activation Options

| Scenario | When to Use | Outcome |
|----------|------------|---------|
| **Activate All** | BEP > 7%, immediate need | Maximum guaranteed floor |
| **Activate Largest** | Moderate need, preserve optionality | Biggest impact, least disruption |
| **Coordinate with RMDs** | IRA accounts with RMD | RMD satisfies income rider withdrawal |
| **Split-Start** | Multiple contracts, phased need | Stagger activations across years |

### NAC 2x LTC Multiplier Consideration
If the dormant rider includes a 2x LTC multiplier, activation locks in the base income amount. Calculate whether the current base income justifies activation vs. waiting for rollup growth (see INCOME LATER process).

---

## Step 4: Build the Presentation

### Template
Use `generate-summary-html` with type `income_now` for the Tier 1 one-pager.
Use `generate-detail-html` with type `income_now` for the Tier 2/3 year-by-year.

### Key Metrics to Highlight
- Dormant income available (annual and monthly)
- Current BEP vs. BEP after activation
- Fee comparison: current vs. with income active
- "Your money lasts X years longer" metric

---

## Step 5: Quality Check

- [ ] All benefit base numbers trace to contract documents
- [ ] Payout rates match the attained age table (not issue age)
- [ ] BEP calculation uses correct fee totals (all-in, not just M+E)
- [ ] Income gap calculation accounts for taxes on GMIB distributions
- [ ] If IRA, RMD coordination verified (no double-counting)

---

## Step 6: Deliver

1. Generate Summary HTML via `wireIncomeNow`
2. DEX converts HTML to PDF
3. File to ACF B4 Recommendations folder
4. Specialist presents at A+R meeting with Tier 1 one-pager
5. Tier 2/3 available for analytical clients who want year-by-year detail

---

## Tools Used

| Tool | QUE Registry ID |
|------|----------------|
| calc-household-aggregate | `calc-household-aggregate` |
| calc-gmib | `calc-gmib` |
| calc-rmd | `calc-rmd` |
| calc-breakeven-equity | `calc-breakeven-equity` |
| ANALYZE_INCOME_NOW | `ANALYZE_INCOME_NOW` |
| WIRE_INCOME_NOW | `WIRE_INCOME_NOW` |
