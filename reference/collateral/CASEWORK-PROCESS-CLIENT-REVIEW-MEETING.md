# Casework Process: Client Review Meeting Prep

**Created:** 2026-03-16
**Source Case:** Sharon Sibenaller & Larry Hansman (Annual Review — Archer, in-home visit)
**Purpose:** Repeatable process for pulling client data from all systems, identifying opportunities, and generating a printable meeting agenda for an advisor's client review meeting.

---

## When This Process Applies

- Advisor has a scheduled review meeting with an existing client/household
- Need a comprehensive "full picture" of what the client owns across all RPI lines of business
- Want to identify optimization opportunities (income activation, tax efficiency, product swaps, coverage gaps)
- Advisor needs a printable meeting agenda with talk tracks

---

## Step 1: Identify the Client(s)

Search across multiple systems in parallel:

### Google Drive (gdrive MCP)
```
mcp__gdrive__search → query: "[Last Name]"
```
Look for:
- **zACF folder** — `zACF- [Client Name]` on Shared Drive (*RPI | B2C Division > *Service Unit > Active Client Files)
- **Ai3 spreadsheet** — `[Client Name]- Q[N]25 Ai3` (quarterly review data)
- **PPL folder** — `PPL-[NNNN] - [Client Name]` (pipeline/case files)
- **Carrier documents** — applications, statements, contracts, beni changes

### Firestore (toMachina API)
```
WebFetch → https://api.tomachina.com/clients/search?q=[Last Name]
```
Pull:
- Client ID, GHL Contact ID
- Contact info (phone, email, address)
- Status, classification, book assignment
- Medicare number
- Tags, opportunities, account records

### ACF Folder Structure (Google Drive)
Navigate the ACF folder to inventory all documents:
```
zACF- [Client Name]/
├── Accounts/
│   ├── Active Accounts/
│   │   ├── Medicare/          ← Med Supp, MAPD, PDP, HIP policies
│   │   └── Retirement/
│   │       ├── Annuity/       ← FIA, MYGA, VA contracts by account #
│   │       └── Life/          ← UL, WL, Term policies
│   └── Inactive Accounts/
│       ├── Medicare/
│       └── Retirement/
├── Cases/
│   ├── Active Cases/
│   └── Inactive Cases/
├── [Driver's License images]
└── [Ai3 Spreadsheet]
```

### Ai3 Spreadsheet (the gold mine)
```
mcp__gdrive__getGoogleSheetContent → spreadsheetId, range: 'Sheet1!A1:Z100'
```
The Ai3 contains the full financial picture:
- **Client demographics** — DOB, age, marital status, tax bracket, filing status
- **Asset inventory** — every account with type, carrier, product, value, surrender value, issue date
- **Life insurance inventory** — policy details, death benefit, cash value, LTC riders, lapse ages
- **Income inventory** — all income sources (GMIB, SS, rental, pensions, employment)
- **Household summary** — investable assets, liquid assets, net worth, liabilities, disposable income
- **Financial experience** — years of experience with different product types

**Run all three searches (Drive, Firestore, Ai3) in parallel using sub-agents.**

---

## Step 2: Build the Client Profile

### Household Summary Table
Compile from Ai3 + Firestore:

| Field | Source |
|-------|--------|
| Net worth | Ai3 |
| Investable assets | Ai3 |
| Liquid assets (bank/CDs) | Ai3 |
| Household income | Ai3 |
| Household expenses | Ai3 |
| Disposable income | Ai3 (income - expenses) |
| Tax filing status | Ai3 |
| Federal tax bracket | Ai3 |

### Per-Client Info
| Field | Source |
|-------|--------|
| Full name | Firestore |
| DOB / Age | Ai3 (cross-check Firestore — flag discrepancies) |
| Phone | Firestore |
| Email | Firestore |
| Medicare number | Firestore |
| Address | Firestore |
| Client status | Firestore |
| Book of Business / Assigned agent | Firestore |

### Asset Inventory
Build a complete table for each client:

| Column | Source |
|--------|--------|
| Type (FIA, UL, WL, Med Supp, PDP, HIP, CD, Real Estate, SS) | Ai3 + Firestore accounts |
| Carrier | Ai3 + Firestore |
| Product name | Ai3 + Firestore |
| Account/Policy number | Ai3 + Firestore |
| Account Value | Ai3 (most current statement) |
| Surrender Value | Ai3 |
| Death Benefit (life only) | Ai3 |
| Cash Value (life only) | Ai3 |
| Issue Date | Ai3 + Firestore |
| Income status (Active/Inactive) | Ai3 |
| GMIB/GLWB amount | Ai3 |
| LTC rider details | Ai3 |
| Key flags (ownership, premium, guarantee period) | Ai3 + ACF documents |

### Income Inventory
| Column | Source |
|--------|--------|
| Type (GMIB, SS, Rental, Pension, Employment) | Ai3 |
| Payor | Ai3 |
| Owner | Ai3 |
| Tax type (IRA, NQ, Provisional) | Ai3 |
| Annual amount | Ai3 |
| Net amount (after withholding) | Ai3 |

---

## Step 3: Identify Opportunities

Analyze the full picture and flag opportunities in these categories:

### Income & Social Security
- [ ] Is each client collecting Social Security? If not, why? (Age 62+ = should be filed or have a reason)
- [ ] Are GMIB/GLWB payouts satisfying RMD requirements for IRA accounts?
- [ ] Are there IRAs outside RPI that need RMD coordination?

### Annuity Optimization
- [ ] Any annuity in accumulation that should be activated for income?
- [ ] Any annuity past surrender period that could be 1035'd to a better product?
- [ ] Any benefit base roll-up still running that could increase future income?
- [ ] MYGA opportunity for bank/CD money earning taxable interest?

### Life Insurance
- [ ] Any UL policies approaching end of guarantee period? Request in-force illustrations.
- [ ] Any ownership structures (trusts, foundations, charities) that need review?
- [ ] LTC riders — does the client know they exist? Can they access them?
- [ ] Any small/old whole life policies where CV ≈ DB (minimal death benefit)?
- [ ] Premium status — still being paid? By whom? Auto-debit or manual?

### Medicare
- [ ] Are Med Supp premiums competitive for their age/state? Run carrier comparison.
- [ ] Does each client have a PDP? (Missing PDP = late enrollment penalty accruing)
- [ ] Is the current PDP formulary still the best fit? (Review at AEP)
- [ ] Any HIP/cancer/hospital indemnity policies — still worth the premium?
- [ ] MAPD vs Med Supp — is the current structure optimal?

### Tax & Estate
- [ ] Filing status optimal? (MFS is usually worse than MFJ)
- [ ] Beneficiary designations current across ALL policies?
- [ ] Any estate planning structures that need review (trusts, foundations)?
- [ ] Tax bracket optimization — could Roth conversions or timing shifts help?

### Housekeeping
- [ ] Data discrepancies (DOB, marital status, contact info) to confirm
- [ ] Missing records (email, Medicare #, PDP) to collect
- [ ] Pending actions (unfunded applications, open cases) to verify status

---

## Step 4: Classify Each Opportunity

Rate each opportunity for the meeting agenda:

| Color | Meaning | Examples |
|-------|---------|---------|
| **Green** | Clear win, easy conversation | MYGA for CD money, missing PDP enrollment |
| **Yellow** | Needs investigation, confirm facts first | SS not collected, KCL guarantee period, ownership questions |
| **Blue** | Educational / long-term | Income activation timing, tax filing optimization, estate review |

---

## Step 5: Build the HTML Meeting Agenda

### Template
`~/Projects/_RPI_STANDARDS/reference/collateral/RPI-Client-Review-Meeting-Template.html`

### 3-Page Structure

**Page 1 — Client Snapshot**
- Header: "Client Review Meeting" + client names + RPI branding + date/agent/location
- Summary bar: Net Worth, Investable, Liquid, Income, Expenses, Disposable
- Client info cards (side-by-side for households)
- Asset tables per client (highlight rows for major accounts)
- Income summary table

**Page 2 — Opportunities**
- Header: "Opportunities & Discussion Points"
- Opportunity boxes (color-coded: green/yellow/blue left border)
- Each box: title, context paragraph, bullet points, italic talk track
- Order: yellow (confirm first) → green (easy wins) → blue (educational)

**Page 3 — Housekeeping & Notes**
- Header: "Housekeeping & Meeting Notes"
- Confirmation checklist (checkbox items for things to verify)
- Meeting flow table (numbered phases with descriptions)
- Blank notes section (dotted lines for handwriting)
- Blank next steps section

### Design System
- Font: 'Segoe UI', system-ui, -apple-system, sans-serif
- Colors: `#1a3a5c` (navy headers/accents), `#e8edf2` (table headers), `#f0f6ff` (highlight rows)
- Opportunity boxes: Green `#2a7d4f` border + `#f4faf6` bg, Yellow `#c49000` + `#fef9ee`, Blue `#2563b3` + `#f0f6ff`
- Print: Letter size, 0.5in/0.6in margins, `print-color-adjust: exact`
- Body text: 10pt (9pt in tables, 8.5pt in opportunity details)
- Page breaks between each page section
- Checklist: CSS pseudo-element checkboxes (printable, no JS)
- Notes area: dotted-line rows for handwriting

### Variables to Parameterize
| Variable | Where It Goes |
|----------|---------------|
| Client name(s) | Header, title, page 2/3 subtitles |
| Meeting date | Header |
| Agent name | Header |
| Location/address | Header |
| Household summary numbers | Summary bar (6 values) |
| Per-client demographics | Client info cards |
| Asset table rows | Per-client tables (type, carrier, product, account #, value, details) |
| Income table rows | Income summary |
| Opportunity blocks | Page 2 (title, context, bullets, talk track, color) |
| Checklist items | Page 3 confirmation section |
| Meeting flow phases | Page 3 flow table |

---

## Step 6: Quality Check

Before delivering to JDM / the advisor:

- [ ] All account values match the most recent source (Ai3 statement dates noted)
- [ ] DOB/age calculations are correct
- [ ] Phone numbers and emails verified from Firestore (never guessed)
- [ ] No PHI beyond what's appropriate for an internal meeting document
- [ ] Medicare numbers included (needed for Medicare review conversations)
- [ ] Every opportunity has a specific talk track the advisor can use verbatim
- [ ] Opportunity colors match severity (yellow = confirm first, green = action, blue = educate)
- [ ] HTML renders correctly in browser — check all 3 pages
- [ ] Print to PDF produces clean output with proper page breaks
- [ ] Checklist items cover every data gap and pending action identified
- [ ] Income total matches household income from Ai3
- [ ] Net worth matches Ai3 (cross-check: assets - liabilities)

---

## Step 7: Deliver

1. Write HTML to `~/Desktop/[ClientName]-Review-Meeting.html`
2. Tell JDM to open in Safari/Chrome → Print → Save as PDF
3. Advisor prints and brings to meeting
4. After meeting: advisor notes go back into system (update Firestore records, create pipeline cards for action items)

---

## Tools Used in This Process

| Tool | Purpose |
|------|---------|
| **Google Drive (gdrive MCP)** | Search for ACF folder, list documents, read Ai3 spreadsheet |
| **toMachina API (WebFetch)** | Pull client records, accounts, opportunities from Firestore |
| **Sub-agents (Agent tool)** | Parallel search across Drive, Firestore, and ACF folder simultaneously |
| **HTML/CSS** | Build the printable meeting agenda (RPI design system) |

---

## Common Patterns & Edge Cases

### Household vs Individual
- Some clients share an ACF folder (couples at same address)
- One client may have significantly more assets than the other
- Marital status in system may not match reality (cohabitating but filed as Single)
- Always confirm relationship at the meeting

### Ownership Structures
- Life policies may be owned by trusts, foundations, or charities (not the insured)
- This affects who can access benefits (especially LTC riders)
- Flag for discussion but don't assume — the advisor should ask the client

### Data Freshness
- Ai3 spreadsheet is updated quarterly (Q1/Q2/Q3/Q4 + year)
- Firestore accounts may have older statement dates
- Always note the "as-of" date for account values
- If values differ between Ai3 and Firestore, use the more recent one

### Missing Data
- No email on file → Add to checklist, advisor collects at meeting
- No Medicare number → Add to checklist
- No PDP → Flag as potential late enrollment penalty issue
- Social Security showing $0 → Could be not collected OR not recorded. Always confirm.

---

## Future: Automated Generation (toMachina)

When the client review pipeline is wired in toMachina:
- Flow stage trigger generates the meeting prep automatically
- Client data pulled from Firestore (clients + accounts + opportunities collections)
- Ai3 data synced via Bridge service or BigQuery
- Opportunity analysis runs as a rule engine against account data
- HTML rendered server-side → PDF via Puppeteer/Chrome
- Filed to ACF via Drive API
- Advisor gets notification: "[Client] review meeting prep ready"
- Post-meeting: advisor submits notes via ProDashX form, auto-creates pipeline cards

This manual process document is the specification for that automation.
