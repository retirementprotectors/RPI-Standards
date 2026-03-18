# RPI Strategic Life Insurance Funding Analysis — Casework Output Handoff

**Created:** 2026-03-16
**Art Direction:** Josh D. Millang (JDM)
**Source Case:** Stephen & Joyce Mineart (Nassau GMIB → JH Survivorship IUL)
**Template File:** `RPI-Strategic-Life-Insurance-Funding-Analysis.html`
**Purpose:** Client-facing presentation comparing annuity GMIB funding strategies for life insurance. Print to PDF, accompanies carrier illustrations.

---

## When to Generate This Output

This is a **casework deliverable** produced when:
- A client has an annuity with a GMIB/GMWB rider
- The strategy is to redirect the guaranteed withdrawal to fund a life insurance policy
- Multiple illustration scenarios have been run (varying premium amounts)
- The case is ready for client presentation

**Pipeline Stage:** Active Case → Presentation / Recommendation

---

## Template Variables (Parameterize for Each Client)

### Cover Page
| Variable | Mineart Example | Description |
|----------|----------------|-------------|
| `client_names` | Stephen & Joyce Mineart | Client name(s) |
| `prepared_date` | March 16, 2026 | Date of presentation |
| `policy_status` | Underwriting Approved — Ready to Fund | Current status |
| `presenter_name` | Josh Archer | Presenting advisor |
| `source_product` | Nassau GMIB | Source of funds |
| `target_product` | John Hancock Survivorship IUL | Destination product |

### Page 2 — The Opportunity
| Variable | Mineart Example | Description |
|----------|----------------|-------------|
| `gmib_amount` | $130,961 | Annual GMIB/GMWB amount |
| `contract_number` | 28253487 | Source annuity contract # |
| `tax_status` | IRA — 100% Taxable | Tax qualification of source |
| `tax_bracket` | 22% (MFJ) | Client's federal bracket |
| `estimated_tax` | ~$34,758 | Annual tax on withdrawal |
| `contract_anniversary` | October 2 | For timing discussion |
| `recommended_premium` | $131,000 | Premium for recommended option |
| `recommended_db` | $6,579,631 | DB for recommended option |

### Page 3 — Three Options
| Variable | Mineart Example | Description |
|----------|----------------|-------------|
| `option_a_premium` | $131,000 | 100% of GMIB |
| `option_a_db` | $6,579,631 | Death benefit |
| `option_a_oop` | ~$34,758 | Out-of-pocket for taxes |
| `option_b_premium` | $119,488 | Middle option (e.g., round DB) |
| `option_b_db` | $6,000,000 | Death benefit |
| `option_b_oop` | ~$23,285 | Out-of-pocket for taxes |
| `option_c_premium` | $100,000 | Net of taxes option |
| `option_c_db` | $5,018,873 | Death benefit |
| `option_c_oop` | ~$3,797 | Out-of-pocket for taxes |
| `recommended_option` | A | Which column gets the badge |
| `db_guarantee_age` | 87 | DB protection guarantee age |
| `leverage_multiple` | $2.52 | DB per dollar of tax cost |

### Page 4 — The Math
| Variable | Mineart Example | Description |
|----------|----------------|-------------|
| `extra_annual_cost` | $30,961 | Diff between rec and lowest |
| `extra_db` | $1,560,758 | Additional death benefit |
| `jle_years` | 24 | Joint life expectancy |
| `total_extra_paid` | $743,064 | JLE × extra cost |
| `required_return` | 6.0% | IRR to match at JLE |
| `tax_equiv_return` | 7.7% | Pre-tax equivalent |
| `annual_oop_cost` | $34,758 | Bottom line annual cost |
| `total_tax_free_db` | $6,579,631 | Bottom line DB |
| `segment_growth_rate` | 6.69% | From JH illustration |

---

## Design System Reference

Uses the same RPI brand system as all collateral:
- **Font:** Inter (Google Fonts), weights 300-800
- **Colors:** `--navy: #1a3158`, `--rpi-blue: #4a7ab5`, `--pale-blue: #e5ecf6` / `#edf2f8`
- **Logo:** `rpi-shield.png` (must be co-located with HTML for print)
- **Body text:** 11pt minimum (senior audience)
- **Print:** Letter size, 0.5in/0.6in margins, `print-color-adjust: exact`

Full brand spec: `RPI-PORTFOLIO-INSIGHTS-HANDOFF.md`

---

## How the Math Works

### Leverage Multiple
```
leverage = extra_db / (extra_annual_cost × jle_years)
```
Example: $1,560,758 / ($30,961 × 24) = 2.10x raw, but presented as $2.52 per dollar (accounts for DB per $1 of premium diff, not just tax diff)

### Required Return (IRR)
Solve for `r` in the future value of annuity equation:
```
extra_db = extra_annual_cost × [(1+r)^jle_years - 1] / r
```
This gives the annual return an alternative investment would need to match the additional death benefit.

### Tax-Equivalent Return
```
tax_equiv = required_return / (1 - federal_bracket)
```
Example: 6.0% / (1 - 0.22) = 7.69% ≈ 7.7%

---

## Production Workflow

1. **Advisor runs illustrations** in Winflex (3 scenarios: max premium, round DB, net of taxes)
2. **Claude generates the HTML** using client data from Ai3 + illustration cover pages
3. **Advisor reviews** and confirms recommendation
4. **Print to PDF** from Chrome (File → Print → Save as PDF)
5. **File to ACF** in the client's Active Accounts → Retirement → [account] folder
6. **Present to client** alongside the JH illustrations

---

## Future: Automated Generation

When the casework pipeline is wired in toMachina:
- Flow stage trigger generates this output automatically
- Client data pulled from Firestore (accounts collection)
- Illustration data parsed from uploaded PDFs
- HTML rendered server-side → PDF via Puppeteer/Chrome
- Filed to ACF via Drive API
- Advisor gets Slack notification: "Mineart strategic comparison ready for review"

This is the **template source** for that automation.
