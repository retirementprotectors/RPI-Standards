# Casework Process: Tax Harvesting — Tax-Efficient Liquidation

**Created:** 2026-03-17
**Source Cases:** Tax-Efficient Liquidation Templates ($115K, $60K, full, IRA transfer), CaseWork.INPUTS automation recipe
**Purpose:** Repeatable process for liquidating a target amount from NQ brokerage/advisory accounts with minimum tax impact.

---

## When This Process Applies

- Client needs to liquidate a specific dollar amount from NQ (non-qualified) accounts
- Client has NQ positions with varying cost basis and gain percentages
- Tax-loss harvesting opportunity exists (positions below cost basis)
- IRA direct transfer optimization (lot selection for portfolio quality)

---

## Step 1: Gather the Source Data

### From the ACF / Advisory Platform
| Document | What You Need |
|----------|--------------|
| **Brokerage/Advisory Statement** | Position-by-position: ticker, shares, market value, cost basis |
| **Tax Lot Detail** | Per-lot cost basis (specific identification method preferred) |
| **Client Tax Return** | Current MAGI, filing status, SS benefits (for provisional income calc) |

### Key Numbers
- Per position: Market Value, Cost Basis, Gain/Loss, Gain %
- Target liquidation amount
- Client's filing status and MAGI
- SS benefits (for provisional income impact)
- Age (for SS earnings limit if pre-FRA)

---

## Step 2: Run the Tax Harvest Analysis

### NQ Strategy: Sell Lowest Gain First
```
1. Sort all lots by gain percentage (ascending)
2. Sell losses first → offsets gains dollar-for-dollar
3. Then sell smallest gains → minimizes LTCG
4. Continue until target amount reached (partial lot if needed)
5. Calculate effective tax rate on proceeds
```

### Loss Harvesting Math
```
Total Losses = Sum of all positions below cost basis
Offset: Losses offset gains first
Then: Up to $3,000 offsets ordinary income
Remainder: Carries forward to next tax year
```

### IRA Strategy (Inverted)
```
Same sort order but different goal:
- Tax is identical regardless of lots (all ordinary income on distribution)
- Goal: Sell underperformers to preserve winners
- Trustee-to-trustee transfer = zero tax, no 60-day clock
```

### Key Calculations
```
Effective Tax Rate = Tax / Proceeds x 100
NIIT (Net Investment Income Tax) = 3.8% above $250K MAGI (MFJ)
Total Rate = LTCG Rate + NIIT (if applicable)
```

---

## Step 3: Assess Downstream Impacts

### Provisional Income Impact
```
Capital gains add to provisional income
May push SS taxation from 50% → 85% bracket
Calculate before AND after to show the cliff effect
```

### SS Earnings Limit (Pre-FRA)
```
If client is pre-Full Retirement Age:
$1 withheld per $2 above $23,400 (2025 limit)
Capital gains count as earnings in some cases
```

---

## Step 4: Build the Presentation

### Template
Use `generate-summary-html` with type `tax_harvesting` for lot selection summary.
Use `generate-detail-html` with type `tax_harvesting` for position-by-position detail.

### COMPLIANCE REQUIREMENT
All Tax Harvesting outputs MUST include the RPI + Signal Advisors Wealth compliance disclosure:

> This analysis is provided for informational purposes only and does not constitute tax, legal, or investment advice. Tax lot selection and liquidation strategies should be reviewed with a qualified tax advisor. Securities offered through Signal Advisors Wealth, member FINRA/SIPC. Advisory services offered through Signal Advisors Wealth, a registered investment advisor. Retirement Protectors, Inc. and Signal Advisors Wealth are not affiliated entities. Past performance is not indicative of future results.

---

## Step 5: Quality Check

- [ ] Cost basis verified per lot (not just average)
- [ ] Loss positions confirmed (not temporary dip vs actual loss)
- [ ] Wash sale rule considered (no repurchase within 30 days)
- [ ] NIIT threshold checked ($250K MFJ, $200K single)
- [ ] Provisional income impact calculated and disclosed
- [ ] Compliance disclosure footer present on ALL outputs
- [ ] IRA transfers use trustee-to-trustee language

---

## Step 6: Deliver

1. Generate HTML via `wireTaxHarvest`
2. DEX converts to PDF
3. File to ACF B4
4. Present lot selection table first, then effective rate, then proceed recommendation
5. Client reviews with their CPA before execution

---

## Tools Used

| Tool | QUE Registry ID |
|------|----------------|
| calc-lot-selection | `calc-lot-selection` |
| calc-ltcg | `calc-ltcg` |
| calc-ss-earnings-limit | `calc-ss-earnings-limit` |
| calc-provisional-income | `calc-provisional-income` |
| ANALYZE_TAX_HARVEST | `ANALYZE_TAX_HARVEST` |
| WIRE_TAX_HARVEST | `WIRE_TAX_HARVEST` |
