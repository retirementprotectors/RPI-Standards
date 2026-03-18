# Casework Process: Growth MAX — VA to FIA Repositioning

**Created:** 2026-03-17
**Source Cases:** Sebetka $579K Portfolio Consolidation, Stuart $548K Portfolio, GROWTH MAX Sheet, FIA MVA Calculator
**Purpose:** Repeatable process for comparing VA sustainability vs FIA alternatives with consolidation cost/bonus offset analysis.

---

## When This Process Applies

- Client has a Variable Annuity bleeding fees (typically 1.5-3% all-in)
- VA is on a depletion trajectory (account hits $0 before life expectancy)
- Client has idle CDs or bank money earning sub-inflation returns
- FIA repositioning with carrier bonus can offset or exceed transition costs

---

## Step 1: Gather the Source Data

### From the ACF
| Document | What You Need |
|----------|--------------|
| **VA Account Statement** | AV, SV, fund allocations, fee schedule (M+E+A + rider fees) |
| **VA Fund Performance** | Historical fund returns for depletion modeling |
| **FIA Product Specs** | Bonus rate, crediting method, cap, participation rate, surrender schedule |

### Key Numbers
- VA: Account Value, Surrender Value, Gross Return, Total Fee Rate (all-in)
- VA: Annual Withdrawal amount, Cost Basis
- FIA: Deposits, First Year Bonus, Hypothetical Growth Rate, Annual Fee Rate (typically 0%)
- Surrender: Charge %, Free Withdrawal % (default 10%)

---

## Step 2: Run the Growth Analysis

### VA Depletion Projection
```
NET Return = Gross (e.g., 6.04%) - Fees (e.g., 1.65%) = 4.39%
Each Year: Ending = (Starting - Withdrawal) x (1 + Net Return)
Track until Ending = $0 → Depletion Year
```

### FIA Sustainability Projection
```
Year 1 Starting = Deposits x (1 + First Year Bonus)
Each Year: Growth at hypo rate, 0% M+E fees
FIA typically never depletes due to zero fees + principal guarantee
```

### Delta Comparison
```
Delta = FIA Value - VA Value (per year)
Cumulative Delta = running sum
Crossover Year = first year FIA exceeds VA
```

### Consolidation Cost/Bonus Offset
```
Surrender Charge = AV x Charge%
LTCG Tax = (Market Value - Cost Basis) x 15%
Gross Cost = Surrender + LTCG
Bonus Credit = Deposits x Carrier Bonus Rate (e.g., Nassau 7%)
Net Cost = Gross Cost - Bonus Credit
If Net Cost < 0 → CLIENT NETS A GAIN
```

### Account-Type Matching
| Source Account | Target Product | Tax Treatment |
|---------------|---------------|---------------|
| ROTH | ROTH NGA | No tax on transfer |
| IRA | IRA NGA | No tax (trustee-to-trustee) |
| NQ | Nassau Bonus | LTCG on gains |
| Inherited (stepped-up) | Any | $0 LTCG |

---

## Step 3: Build the Presentation

### Template
Use `generate-summary-html` with type `growth_max` for A vs B comparison.
Use `generate-detail-html` with type `growth_max` for year-by-year delta table.

### Key Metrics
- Depletion year (VA)
- 30-year value comparison
- Net consolidation cost (highlight when negative = gain)
- Fee savings: total fees avoided over 30 years

---

## Step 4: Quality Check

- [ ] VA fee rate includes ALL fees (M+E+A + GMIB + GMDB + fund expenses)
- [ ] FIA growth rate is hypothetical, not guaranteed — footnote required
- [ ] Surrender charge matches actual schedule year (not a different year)
- [ ] Cost basis verified (NQ accounts have basis, IRA/Roth do not)
- [ ] Inherited accounts use stepped-up basis ($0 LTCG)
- [ ] NAC 11-year surrender schedule: 10/10/9/9/8/8/7/6/4/2/0

---

## Step 5: Deliver

1. Generate HTML via `wireGrowthMax`
2. DEX converts to PDF
3. File to ACF B4
4. Present at A+R meeting — lead with the depletion year, close with the net cost

---

## Tools Used

| Tool | QUE Registry ID |
|------|----------------|
| calc-va-depletion | `calc-va-depletion` |
| calc-fia-projection | `calc-fia-projection` |
| calc-delta | `calc-delta` |
| calc-surrender-charge | `calc-surrender-charge` |
| calc-ltcg | `calc-ltcg` |
| calc-bonus-offset | `calc-bonus-offset` |
| ANALYZE_GROWTH | `ANALYZE_GROWTH` |
| WIRE_GROWTH_MAX | `WIRE_GROWTH_MAX` |
