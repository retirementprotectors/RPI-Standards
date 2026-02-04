---
name: Midwest Medigap Document Inventory
overview: Inventory of 45 documents in the midwest-medigap data folder, categorized by carrier/source, document type, and intended use for commission reconciliation and book of business analysis.
todos:
  - id: identify-excel
    content: Open and identify the 13 unknown Excel files to determine carrier source
    status: completed
  - id: naming-convention
    content: "Establish and apply consistent file naming: {CARRIER}_{TYPE}_{DATE}.{ext}"
    status: completed
  - id: unified-bob
    content: Design unified Book of Business schema combining all carrier policy lists
    status: completed
  - id: commission-parser
    content: Build commission statement parser for automated reconciliation
    status: completed
  - id: subagent-matrix
    content: Create sub-agent hierarchy and split tracking matrix
    status: completed
isProject: false
---

# Midwest Medigap Document Inventory

## Document Categories

### 1. Wellabe/Medico Commission Statements (Monthly)

**Files:** 12 files matching `0115WA00_MC_*.csv`

- `0115WA00_MC_01-31-2025.csv` through `0115WA00_MC_12-31-2025.csv`

**Carrier:** Wellabe (formerly Medico)
**Agent Number:** 0115WA00 (Midwest Medigap)
**Content:** Monthly commission detail - Policy Nbr, Issue State, Client Name, Effective Date, Agent, Commission Rate, Commission Amount
**Use Case:** Commission reconciliation, tracking renewals vs new business, sub-agent splits (e.g., 0115WA03 Kristen Brown)

---

### 2. Wellabe/Medico New Business Reports (WA)

**Files:** 3 files matching `0115WA00_WA_*.csv`

- `0115WA00_WA_03-31-2025.csv`
- `0115WA00_WA_06-18-2025.csv`
- `0115WA00_WA_10-29-2025.csv`

**Carrier:** Wellabe (formerly Medico)
**Content:** Written/Delivered business - includes advance commission amounts
**Use Case:** Track new business pipeline, advance commission projections

---

### 3. Aetna Senior Products (AHL/NHIC) - Weekly BoB Exports

**Files:** 7 files matching `18352983_Midwest_Medigap_*.xls`

- `18352983_Midwest_Medigap_20251017.xls` through `18352983_Midwest_Medigap_20260123.xls`

**Carrier:** Aetna Senior Products (AHL = Aetna Health Life, NHIC = National Health Insurance Company)
**Agency ID:** 18352983
**Format:** Excel (.xls)
**Content:** Weekly book of business snapshots
**Use Case:** Track policy status changes over time, identify lapses/terminations

---

### 4. Aetna Customer & Policy Lists

**Files:**

- `18352983_CustomerList.csv` (121 rows - customer demographics)
- `18352983_PolicyList.csv` (150 rows - policy details with premium, status, payment info)

**Carrier:** Aetna Senior Products
**Content:**

- CustomerList: Member info, address, email, agent assignment, status
- PolicyList: Full policy detail including premium, plan type (Plan G, Plan N, DVH PPO), payment status, legal entity (AHL vs NHIC)

**Use Case:** Client 360 view, cross-sell analysis, retention tracking

---

### 5. GTL (Guarantee Trust Life) - Policy Extract & Commission History

**Files:**

- `44J45770000PolicyExtract.csv` (130 rows) - Current policy extract
- `I44J457700.csv` (2,090 rows) - Commission transaction history (2022-present)

**Agent Number:** 44J45770000 (Midwest Medigap agency), 44J46330000 (Eric Raasch sub-agent)
**Carrier:** GTL
**Products:** DVH (Dental/Vision/Hearing), Critical Illness, Short Term Care
**Content:**

- PolicyExtract: Active policies, modal/annual premium, writing agent splits
- I44J457700: Commission payment history with transaction codes (11-001 = 1st year, 11-024 = advance)

**Use Case:** Ancillary product tracking, commission reconciliation, sub-agent split verification

---

### 6. Mutual of Omaha Commission Statements

**Files:**

- `Commissions_1_24_2026 3_03_11 PM.csv` (428 rows)
- `Commissions_1_24_2026 3_04_49 PM.csv` (duplicate)

**Agent Number:** A14928VP66 (Midwest Medigap)
**Carrier:** Mutual of Omaha (M1, ML, MS company codes)
**Content:** Commission payments by company, date, statement type (Adv = Advance, Comm = Commission)
**Use Case:** Commission reconciliation, advance vs commission tracking

---

### 7. Devoted Health - MAPD Application Status

**Files:**

- `application_status_report_2026_01_24.csv` (19 rows)

**Carrier:** Devoted Health (Medicare Advantage)
**Content:** MAPD enrollment applications - approval status, agent NPN, plan IDs, AOR (Agent of Record) dates
**Use Case:** MAPD enrollment tracking, agent production by NPN

---

### 8. Cigna/Accendo - Customer & Policy Summaries

**Files:**

- `Customer summary.csv` (227 rows)
- `Customer List.csv`

**Carrier:** Cigna/Accendo (CHGA prefix = Cigna Health Group)
**Content:** Individual Medicare customers with YTD premium and compensation
**Use Case:** Renewal commission tracking, customer retention

---

### 9. Medico/Wellabe - Policy List

**Files:**

- `PolicyList - AAY8728 - MIDWEST MEDIGAP.csv` (127 rows)

**Distributor:** MIDWEST MEDIGAP
**Agent:** Matthew Mitchell (077809VP66)
**Carrier:** Medico (Medicare Supplement, DVH, Dental, Cancer)
**Content:** Full policy detail - insured info, plan, premium, issue date, paid-to-date, status
**Use Case:** Book of business master list, retention analysis

---

### 10. Humana - Monthly Production

**Files:**

- `Midwest Medigap Humana Dec 2025.xlsx`

**Carrier:** Humana
**Format:** Excel
**Use Case:** Humana production tracking (MAPD likely)

---

### 11. Various Commission/BoB Reports (Unidentified Carrier)

**Files:**

- `26_334020.xlsx` - Unknown (likely statement ID)
- `34_347506.xlsx` - Unknown (likely statement ID)
- `5130007-January2026.xlsx` - Monthly statement
- `5130007-June2020.xlsx` - Historical
- `5130007-May2020.xlsx` - Historical
- `AgentCommissionReport.xlsx`
- `BookOfBusinessExport-01242026.xlsx`
- `commission_statement_2938747_2026-01-01.xlsx`
- `CommissionData.xlsx`
- `CurrentPolicy.xlsx`
- `policySummary.xlsx`
- `Jarvis # BookOfBusiness - DownloadResults.xlsx`

**Use Case:** Need to open and identify carrier source

---

## Summary by Carrier

| Carrier | Files | Document Types |
|---------|-------|----------------|
| Wellabe/Medico | 15 | Monthly commission, new business, policy list |
| Aetna Senior Products | 9 | Weekly BoB, customer list, policy list |
| GTL | 2 | Policy extract, commission history |
| Mutual of Omaha | 2 | Commission statements |
| Devoted Health | 1 | MAPD application status |
| Cigna/Accendo | 2 | Customer summary |
| Humana | 1 | Monthly production |
| Unidentified | 13 | Various Excel reports |

---

## Recommended Actions

1. **Standardize naming convention** - Rename files to format: `{CARRIER}_{TYPE}_{DATE}.{ext}`

2. **Build commission reconciliation pipeline** - Parse monthly statements to verify payments against expected commissions

3. **Create unified Book of Business view** - Combine Aetna PolicyList, Medico PolicyList, GTL PolicyExtract into single client/policy database

4. **Identify unknown Excel files** - Open and categorize the 13 unidentified reports

5. **Archive historical data** - Move 2020-era files to archive subfolder

6. **Track sub-agent splits** - Build matrix of writing agents (0115WA03 Kristen Brown, 0115WA04 Rebecca Hayes, 44J46330000 Eric Raasch)