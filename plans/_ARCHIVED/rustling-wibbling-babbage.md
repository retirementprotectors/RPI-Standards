# Plan: Reply to Zane Gray — EP Onboarding Package

## Context
Zane Gray at Employee Pooling (EP) needs:
1. Company info for the ASA (service agreement) — his Feb 8 email
2. Data deliverables from the 2/10 call (Signal format, CoF format, bank transactions, commission rules)

This is a single comprehensive reply covering everything, sent as a reply to the ASA thread.

## Part 1: ASA Info (Zane's 5 Questions)

| # | Zane Asked For | Answer |
|---|---------------|--------|
| 1 | Anyone attached (name + title) | **Josh D. Millang, CEO** |
| 2 | Full legal name | **Millang Financial Group, LLC dba Retirement Protectors, Inc.** |
| 3 | Business address | **6750 Westown Parkway, Suite 200-382, West Des Moines, IA 50266** |
| 4 | Phone (main contact) | **515-707-0207** |
| 5 | Email (relevant contacts) | **josh@retireprotected.com** |

## Part 2: Data Deliverables (from 2/10 Call Notes)

### Signal Statement Format
- **Share:** Google Sheet `SIGNAL Transactions- 1.1.23 to 11.25.25`
- Drive ID: `1GFCd72nuYw19HscUR58lDNkdkb_aUBeYCiEOELomuDg`
- Contains: Full consolidated Signal/Stateable transaction data, Jan 2023–Nov 2025

### CoF Statement Format
- **Share 3 representative PDFs** from `Stateable- Q425 Launch/CoF/`:
  - `CR5229-20251125.pdf` (Nov 25) — ID: `1YcmCeNtXr_gkdzrEtN3tzcNXWYIg4_zW`
  - `CR5229-20251028.pdf` (Oct 28) — ID: `1OuT0gJBxmmgHKulS7Jg2-SUrOdgwaTZj`
  - `CR5229-20250909.pdf` (Sep 9) — ID: `1jxnkin43o66kiHRw_VuVzLg6BEkjIFXM`

### Carrier Inventory Sheet (NEW — Create as Google Sheet)
Create a Google Sheet: **"RPI x EP — Carrier Inventory"** with these columns:

| Carrier | Payment Frequency | Entity | Avg Monthly $ | Agent/Writing # | Username | Password | 2FA Method |
|---------|------------------|--------|---------------|-----------------|----------|----------|------------|

Pre-populate from bank statement analysis (Q4 2025 data):

**MFGAN (acct 5231) — Main account:**
| Carrier | Freq | Entity | Avg Mo $ |
|---------|------|--------|----------|
| Signal Advisors | Weekly | MFGAN | ~$232,000 |
| Aetna | Multiple/wk | MFGAN | ~$11,400 |
| UHC (UHIC) | Weekly | MFGAN | ~$3,500 |
| Medico/Wellabe | Multiple/mo | MFGAN | ~$2,400 |
| YourPlanChoice/Humana | Monthly | MFGAN | ~$950 |
| MMProtect MCS | Monthly | MFGAN | ~$480 |
| Catholic Order of Foresters | Monthly | MFGAN | ~$340 |
| Ethos Technologies | Monthly | MFGAN | ~$367 |
| ACE P&C / Chubb | Monthly | MFGAN | ~$300 |
| Ameritas Life | Monthly | MFGAN | ~$200 |
| NGIS | Monthly | MFGAN | ~$255 |
| Spark Advisors | Monthly | MFGAN | ~$162 |
| Kansas City Life | Irregular | MFGAN | varies |
| ITS Alliance Partners | Monthly | MFGAN | ~$667 |
| Lumico Life | Monthly | MFGAN | ~$109 |
| FGL (Fidelity & Guaranty Life) | Monthly | MFGAN | ~$130 |
| Manhattan Life | Monthly | MFGAN | ~$86 |
| Guarantee Trust (GTL) | Monthly | MFGAN | ~$81 |
| Elips Life | Monthly | MFGAN | ~$68 |
| Mutual of Omaha | Monthly | MFGAN | ~$34 |
| Cigna | Monthly | MFGAN | ~$30 |
| National Care (NCD) | Monthly | MFGAN | ~$29 |
| Premier Senior Marketing | Monthly | MFGAN | ~$52 |
| Lumeris Healthcare | Monthly | MFGAN | ~$13 |

**MFG (acct 4829):**
| GBL / Blue Cross Blue Shield | Monthly | MFG | ~$430 |
| Pacific Life (PAC) | Monthly | MFG | ~$63 |
| Protective Life | Monthly | MFG | ~$0.09 |

**MFGA (acct 5190):**
| Assurity Life | Monthly | MFGA | ~$36 |

Agent #, Username, Password, 2FA columns left blank — EP fills in as they extract from statements.

### Commission Payout Rules (Full CAM Structure)
Include in email body — EP needs the full detail since they'll be computing and splitting commissions:

**Flow:** Carrier → IMO (SPARK/Signal/Gradient) → RPI gross revenue → Apply rules → Agent/partner payout

**Formula:** `Net Commission = Gross Revenue × Product Multiplier × Source Multiplier × Tier %`

**Product Multipliers:** MAPD 2.0x, MedSupp 1.5x, PDP/Life/Annuity 1.0x

**Source Multipliers:** Merger 2.0x, Acquisition 1.5x, Partnership 1.0x

**Revenue Components:**
- FYC: ADV (advance), OVR (override), BNS (bonus)
- Renewal: ASE (as-earned), OVR (override), SVS (service/trail)

**B2C Agent Tiers (COR/AST/SPC):**
- COR-I 5%, COR-III(ITP) 7.5%, COR-III(ATP) 10%
- AST-I 12.5% ($300k+), AST-II 15% ($600k+), AST-III 20% ($1.2MM+)
- SPC-I 25% ($1.8MM+), SPC-II 27.5% ($2.5MM+), SPC-III 30% ($4MM+)

**B2B Partner Tiers (DAVID):**
- Bronze 20% ($0-$299k), Silver 22% ($600k-$1.2MM), Gold 24% ($1.2-$1.8MM)
- Platinum 26% ($1.8-$2.5MM), Titanium 28% ($2.5-$4MM), Diamond 30% ($4MM+)

**Split Rule:** Partners assign tier % to downline/network, retain difference.

### Commission Structure Sheet (NEW — Create as Google Sheet)
Create a Google Sheet: **"RPI x EP — Commission Structure"**

**Tab 1: Rules**
| Section | Content |
|---------|---------|
| Flow | Carrier → IMO (SPARK/Signal/Gradient) → RPI gross revenue → Apply rules → Agent/partner payout |
| Formula | `Net Commission = Gross Revenue × Product Multiplier × Source Multiplier × Tier %` |
| Revenue Components | FYC: ADV (advance) + OVR (override) + BNS (bonus); Renewal: ASE (as-earned) + OVR (override) + SVS (service/trail) |
| Product Multipliers | MAPD 2.0x, MedSupp 1.5x, PDP/Life/Annuity 1.0x |
| Source Multipliers | Merger 2.0x, Acquisition 1.5x, Partnership 1.0x |
| B2C Tiers | COR-I 5%, COR-III(ITP) 7.5%, COR-III(ATP) 10%, AST-I 12.5% ($300k+), AST-II 15% ($600k+), AST-III 20% ($1.2MM+), SPC-I 25% ($1.8MM+), SPC-II 27.5% ($2.5MM+), SPC-III 30% ($4MM+) |
| B2B Tiers | Bronze 20% ($0-$299k), Silver 22% ($600k-$1.2MM), Gold 24% ($1.2-$1.8MM), Platinum 26% ($1.8-$2.5MM), Titanium 28% ($2.5-$4MM), Diamond 30% ($4MM+) |
| Split Rule | Partners assign tier % to downline/network, retain difference |

**Tab 2: Examples (3 worked calculations)**

| # | Scenario | Product | Source | Tier | ADV | OVR | BNS | Gross | Prod Mult | Src Mult | Tier % | Net Payout |
|---|----------|---------|--------|------|-----|-----|-----|-------|-----------|----------|--------|------------|
| 1 | Medicare Specialist, MAPD | MAPD | Partnership | AST-II (15%) | $600 | $50 | $25 | $675 | 2.0x | 1.0x | 15% | $202.50 |
| 2 | Retirement Specialist, Life | Life | Acquisition | SPC-I (25%) | $4,000 | $400 | $200 | $4,600 | 1.0x | 1.5x | 25% | $1,725.00 |
| 3 | Top Producer, Annuity 7% | Annuity | Merger | SPC-III (30%) | $14,000 | $1,400 | $700 | $16,100 | 1.0x | 2.0x | 30% | $9,660.00 |

Each example shows: Gross = ADV + OVR + BNS → then Net = Gross × Product Mult × Source Mult × Tier %

### Agent Numbers & Carrier Portal Credentials
- No clean doc exists — credentials scattered across carrier portals/emails
- **Onboarding sequence with EP:**
  1. RPI provides statements (bank + Signal + CoF) → EP extracts agent/writing numbers
  2. RPI provides carrier portal credentials once agent numbers are mapped
  3. EP optimizes credential management (password manager)
  4. EP takes over statement pulling
- Email tells Zane: agent numbers are in the statements, credentials to follow

### GBL Correction
- "Group Benefits" on the MFG (4829) bank deposits = **GBL / Blue Cross Blue Shield** general agent paying directly
- NOT Integrity/SPARK as initially assumed

## Execution Steps

1. **Create Google Sheet** — "RPI x EP — Carrier Inventory" with carrier data pre-populated, credentials columns blank
2. **Create Google Sheet** — "RPI x EP — Commission Structure" with Rules tab + Examples tab (3 worked calculations)
3. **Share Drive files** with `zane@ep-insuranceservices.com`:
   - Carrier Inventory sheet — **editor** (so EP can fill in agent #s and credentials)
   - Commission Structure sheet — **viewer**
   - Signal Transactions Google Sheet — **viewer**
   - 3 CoF CR5229 PDFs — **viewer**
4. **Also share with** `a.kumar@epr-india.com` (same permissions)
5. **Draft email** replying to ASA thread (`19c3efbc0f2222dc`) with:
   - ASA info (5 items, numbered to match Zane's request)
   - Links to all 6 shared files
   - Brief commission overview (details in the sheet)
   - Carrier inventory overview: "28 carriers across 3 entities, agent numbers and credentials to be populated"
   - Next steps: "Pull statements → extract agent numbers → we provide portal credentials → you optimize and take over"
   - CC Abhishek (`a.kumar@epr-india.com`)
6. **SHOW EMAIL DRAFT TO JDM FOR APPROVAL** — do NOT auto-send
7. **Send via Gmail MCP** only after JDM approves

## Tone
Professional but personable — matches the casual-professional tone Zane and Abhishek set.

## Verification
- Confirm Drive sharing succeeded
- Confirm email sent (check Gmail sent folder)
- Report back to JDM with confirmation
