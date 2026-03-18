# Casework Process: LTC MAX — Long-Term Care Access Mapping

**Created:** 2026-03-17
**Source Cases:** Connell LTC Access Analysis (4-Phase Framework), LTC HYBRID Life + FIA Comparison, FE v TERM v IUL
**Purpose:** Repeatable process for mapping all contracts to the proprietary RPI 4-Phase LTC Access Framework.

---

## When This Process Applies

- Client has multiple contracts with LTC access features
- Need to map the full LTC pool and access sequence
- Annual rider fees need justification against LTC benefit
- Evaluating hybrid life/LTC products vs existing portfolio

---

## Step 1: Gather the Source Data

### From the ACF
| Document | What You Need |
|----------|--------------|
| **Contract Rider Pages** | LTC features: enhanced withdrawal, income multiplier, enhanced liquidity, terminal waiver |
| **Annual Statements** | Account values, rider fees, base income amounts |
| **Product Spec Sheets** | Phase I-IV qualification requirements by carrier |

### Key Numbers per Contract
- Account Value
- Base Income (GMIB or equivalent)
- Enhanced Withdrawal: Yes/No, Percent (default 20%), Frequency (every-other-year)
- Income Multiplier: Yes/No, Factor (default 2x)
- Enhanced Liquidity: Yes/No
- Terminal/Confinement Waiver: Yes/No
- Annual Rider Fees

---

## Step 2: Run the LTC Analysis

### 4-Phase Access Framework (Proprietary RPI)

| Phase | Qualification | What's Accessible | Calculation |
|-------|-------------|-------------------|-------------|
| **I** | No qualification | Enhanced withdrawal | AV x 20% (every-other-year) |
| **II** | ADL-triggered (2+ Activities of Daily Living) | Income multiplier | Base Income x 2 |
| **III** | ADL-triggered | Enhanced liquidity | Full SV + enhanced income |
| **IV** | Confinement/Terminal | Full account access | 100% of AV |

### Fee Break-Even Analysis
```
Annual Rider Fees = Sum across all contracts
Phase II Annual Access = Sum of multiplied incomes
Break-Even Months = Annual Fees / (Phase II Access / 12)
```
If break-even < 12 months, the 2x multiplier justifies the fees within the first year of care.

### MGSV Floor Protection
```
MGSV = 87.5% of premiums x (1 + 3%)^years held
If MGSV > Surrender Value → contract is below floor protection
```

---

## Step 3: Evaluate the Pool

### Total LTC Pool
Sum across all 4 phases. This is the total accessible amount if the client needs care.

### Fee Efficiency
```
Fee-to-Pool Ratio = Annual Fees / Total LTC Pool
If > 3% → re-evaluate fee efficiency
If < 1% → fees are minimal relative to coverage
```

### Comparison: FE v TERM v IUL
| Metric | Final Expense (MOO) | Term-20 (TransAm) | IUL (JH) |
|--------|--------------------|--------------------|-----------|
| Monthly Premium | $257 | $592 | $1,134 |
| 20-Year Net Outlay | $32,468 | $142,188 | $135,514 |
| Year 21 DB (each) | $25,000 | $0 | $250,000 |
| LTC Monthly (x25) | $0 | $0 | $10,000 |

---

## Step 4: Build the Presentation

### Template
Use `generate-summary-html` with type `ltc_max` for 4-phase pool summary.
Use `generate-detail-html` with type `ltc_max` for contract-by-contract detail.

### Key Visual
The 4-Phase access table is the centerpiece. Show the progressive access from no-qualification (Phase I) through terminal (Phase IV).

---

## Step 5: Quality Check

- [ ] Every contract mapped to correct phases based on actual rider specifications
- [ ] Enhanced withdrawal frequency noted (every-other-year vs annual)
- [ ] Income multiplier factor verified per contract (not all are 2x)
- [ ] MGSV uses actual premium amounts and holding period
- [ ] Fee-to-pool ratio flagged if > 3%

---

## Step 6: Deliver

1. Generate HTML via `wireLtcMax`
2. DEX converts to PDF
3. File to ACF B4
4. Present at A+R meeting — the 4-phase visual is the hero slide

---

## Tools Used

| Tool | QUE Registry ID |
|------|----------------|
| calc-ltc-phase-access | `calc-ltc-phase-access` |
| calc-gmib | `calc-gmib` |
| calc-mgsv | `calc-mgsv` |
| lookup-carrier-product | `lookup-carrier-product` |
| ANALYZE_LTC | `ANALYZE_LTC` |
| WIRE_LTC_MAX | `WIRE_LTC_MAX` |
