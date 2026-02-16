# Campaign Master Index

> Cross-reference hub for all 4 RPI campaign engines. **Read this document first** to understand the entire campaign system before diving into individual engine docs.

---

## 1. Campaign Engine Overview

RPI operates 4 campaign engines that together cover every client lifecycle stage across Health, Wealth, and Legacy.

| Engine | Full Name | Campaigns | Trigger Type | Division Focus |
|--------|-----------|-----------|--------------|----------------|
| **PSM** | Proactive Service Model | 15 | Account events (plan changes, policy anniversaries, CMS data, FEMA, authorization gaps) | HEALTH + WEALTH + LEGACY |
| **T65** | Medicare Birthday Countdown | 15 | Age (12-month countdown to 65th birthday, through 2 months post) | HEALTH |
| **AGE** | Wealth Milestones | 9 | Age (50, 55, 59.5, 62, 66, 67, 70, 73, 75) | WEALTH |
| **COV** | Calendar Coverage Events | 7 | Calendar awareness months (national awareness months + seasonal events) | HEALTH + WEALTH + LEGACY |

**Totals:** 46 campaigns, 368 content blocks, 506 template touchpoints

### Engine Relationships

```
T65 (acquisition) ---> PSM (retention/service)
    T65+2 hands off new Medicare clients into PSM annual cycle

COV (cross-sell) ---> PSM (retention/service)
    COV gap-fill converts --> client enters PSM for that product

AGE (milestone) ---> PSM (retention/service)
    AGE milestone conversations create PSM product opportunities

AGE-62 (SS conversation) ---> T65 (pre-seed)
    Social Security at 62 plants Medicare awareness 3 years early
```

### Execution Path (All Engines)

```
C3 (campaign engine) --> PRODASH (delivery) --> 4 channels:
    1. Email (EmailBody + SubjectLine)
    2. Text/SMS (TextTemplate)
    3. Voicemail Drop (VMScript)
    4. USPS Mailer (physical mail)
```

---

## 2. Full Campaign Index (All 46)

### PSM -- Proactive Service Model (15 campaigns)

| # | Campaign ID | Campaign Name | Division | Trigger | Timing |
|---|-------------|---------------|----------|---------|--------|
| 1 | PSM-SEP-PREP | AEP SEP Prep | HEALTH | Missing/expired authorizations | September |
| 2 | PSM-AEP-REV | AEP Review | HEALTH | Annual plan review cycle | Sep--Oct |
| 3 | PSM-AEP-MOVE | AEP Move | HEALTH | Review found better plan | Nov--Dec |
| 4 | PSM-AEP-G2G | AEP Good to Go | HEALTH | Plan confirmed best | Nov--Dec |
| 5 | PSM-AEP-STAY | AEP Stay | HEALTH | Plan best, has changes | Nov--Dec |
| 6 | PSM-AEP-$0 | AEP Move ($0!) | HEALTH | $0-premium plan found | Nov--Dec |
| 7 | PSM-SEP-5 | SEP 5-Star | HEALTH | 5-star plan in area (CMS) | Year-round |
| 8 | PSM-SEP-3 | SEP Below 3-Star | HEALTH | Client plan below 3-star (CMS) | Year-round |
| 9 | PSM-SEP-FEMA | SEP FEMA | HEALTH | FEMA disaster declaration | 2-month window |
| 10 | PSM-OEP | OEP Benefit Check | HEALTH | New year plan rollover | Jan--Mar |
| 11 | PSM-NO-CORE | No-Core Cross-Sell | HEALTH | Client has no Medicare through RPI | Jan--Sep (paused Oct--Dec) |
| 12 | PSM-LIFE | Life Statement Review | LEGACY | Policy anniversary (+30 days) | Year-round |
| 13 | PSM-ANN-SUR | Annuity Surrender <10% | WEALTH | Surrender charge threshold | Year-round |
| 14 | PSM-ANN-ALLOC | Annuity Allocation Review | WEALTH | Policy anniversary | Year-round |
| 15 | PSM-ANN-LIQ | Annuity Fully Liquid | WEALTH | Surrender charges at 0% | Year-round |

### T65 -- Medicare Birthday Countdown (15 campaigns)

| # | Campaign ID | Campaign Name | Phase | Months to 65 |
|---|-------------|---------------|-------|--------------|
| 1 | T65-12 | First Introduction | Education | -12 |
| 2 | T65-11 | Medicare Basics | Education | -11 |
| 3 | T65-10 | Two Paths | Education | -10 |
| 4 | T65-09 | Authorization Introduction | Education | -9 |
| 5 | T65-08 | Data Gathering Begins | Education | -8 |
| 6 | T65-07 | Situation Assessment | Education | -7 |
| 7 | T65-06 | IEP Window Preview | Planning | -6 |
| 8 | T65-05 | Plan Comparison Prep | Planning | -5 |
| 9 | T65-04 | Recommendation Build | Planning | -4 |
| 10 | T65-03 | IEP Window Opens | Urgent | -3 |
| 11 | T65-02 | Enrollment Push | Urgent | -2 |
| 12 | T65-01 | Final Pre-Birthday | Urgent | -1 |
| 13 | T65-00 | Birthday Month | Action/Follow-up | 0 |
| 14 | T65+1 | Post-Enrollment Check | Action/Follow-up | +1 |
| 15 | T65+2 | Coverage Verification | Action/Follow-up | +2 |

### AGE -- Wealth Milestones (9 campaigns)

| # | Campaign ID | Campaign Name | Division | Trigger Age | Key Milestone |
|---|-------------|---------------|----------|-------------|---------------|
| 1 | AGE-50 | Catch-Up Contributions | WEALTH | 50 | IRS catch-up contribution eligibility (401k, IRA) |
| 2 | AGE-55 | Rule of 55 | WEALTH | 55 | Penalty-free 401k withdrawal if separated from service |
| 3 | AGE-59 | Penalty-Free Withdrawals | WEALTH | 59.5 | IRS penalty-free withdrawal from qualified accounts |
| 4 | AGE-62 | Social Security Eligibility | WEALTH | 62 | Early Social Security eligibility + Medicare pre-seed |
| 5 | AGE-66 | Full Retirement Age | WEALTH | 66 | Full Social Security benefit (for those born 1954--1956) |
| 6 | AGE-67 | Full Retirement Age | WEALTH | 67 | Full Social Security benefit (for those born 1960+) |
| 7 | AGE-70 | Maximum SS Benefit | WEALTH | 70 | Maximum delayed Social Security credits |
| 8 | AGE-73 | RMD Begins | WEALTH | 73 | Required Minimum Distributions from qualified accounts |
| 9 | AGE-75 | Legacy Transition | WEALTH | 75 | Estate planning, beneficiary review, wealth transfer |

### COV -- Calendar Coverage Events (7 campaigns)

| # | Campaign ID | Campaign Name | Division | Timing | Product Gap |
|---|-------------|---------------|----------|--------|-------------|
| 1 | COV-PREAEP | Pre-AEP Medicare Gap | HEALTH | Jul--Sep | Medicare (MAPD/MedSupp) |
| 2 | COV-LTC | Long-Term Care Awareness | LEGACY | November | LTC / Hybrid LTC |
| 3 | COV-LIAM | Life Insurance Awareness | LEGACY | September | Life Insurance |
| 4 | COV-DI | Disability Insurance Awareness | LEGACY | May | Disability Income |
| 5 | COV-LOVE | Love & Protection Month | LEGACY | February | Life Insurance (Valentine's framing) |
| 6 | COV-ANN | Annuity Awareness | WEALTH | June | Annuity / Retirement Income |
| 7 | COV-TAX | Tax Season Coverage Review | WEALTH | Feb--Apr | Annuity / IRA / Retirement Vehicles |

---

## 3. Campaign Lifecycle Patterns

Each engine follows a distinct lifecycle pattern. Understanding these patterns is critical for sequencing, handoffs, and avoiding overlap.

### T65: Education --> Planning --> Urgent --> Action --> Follow-up

```
Education (T65-12 to T65-07)    6 months of progressive learning
    "You might not even need to worry about it"
        |
Planning (T65-06 to T65-04)    3 months of data analysis and comparison
    "We're building your specific options"
        |
Urgent (T65-03 to T65-01)      3 months of IEP window enrollment
    "Your window is open -- let's make your decision"
        |
Action/Follow-up (T65-00 to T65+2)    3 months of execution and verification
    "You're covered. Welcome to the team."
```

### PSM: Event-Triggered --> Review --> Decision --> Confirmation

```
Account event fires (data change, anniversary, CMS rating, FEMA)
    |
Review initiated (agent pulls data, builds comparison)
    |
Decision presented (data-driven recommendation)
    |
Confirmation (outcome documented, next cycle scheduled)
```

The AEP cycle is the primary PSM pattern:
```
SEP-PREP (authorization) --> AEP-REV (review) --> One outcome:
    MOVE (switch plans)
    G2G (stay, confirmed best)
    STAY (stay, with changes noted)
    $0 (switch to $0-premium)
```

### COV: Awareness --> Education --> Gap Identification --> Conversion

```
Awareness month creates natural timing
    |
Education on the gap ("you have X but not Y")
    |
Gap identified with client's specific situation
    |
If client engages --> enters PSM service cycle for that product
```

### AGE: Milestone --> Education --> Options --> Planning

```
Birthday triggers age-based milestone
    |
Education on what the milestone means (IRS rules, SS eligibility, RMD)
    |
Options presented based on client's actual financial picture
    |
Planning conversation leads to product or strategy decisions
```

---

## 4. Seasonal Campaign Calendar

### Month-by-Month View

| Month | Active Campaigns | Notes |
|-------|-----------------|-------|
| **January** | PSM-OEP, COV-TAX starts | OEP opens Jan 1. Tax season begins. New plan year rollover. |
| **February** | PSM-OEP, COV-LOVE, COV-TAX | Valentine's life insurance framing. Tax season continues. |
| **March** | PSM-OEP ends (Mar 31), COV-TAX | OEP closes. Last month for MA-to-MA switch. |
| **April** | COV-TAX ends (Apr 15) | IRA contribution deadline. Tax filing deadline. |
| **May** | COV-DI | Disability Insurance Awareness Month. Working-age clients. |
| **June** | COV-ANN | Annuity Awareness Month. Retirement income conversations. |
| **July** | COV-PREAEP starts | Pre-AEP Medicare gap outreach begins. 3 months before AEP. |
| **August** | COV-PREAEP | Pre-AEP continues. Building pipeline for October. |
| **September** | PSM-SEP-PREP, PSM-AEP-REV starts, COV-PREAEP ends, COV-LIAM | Authorization gathering. Reviews begin. Life Insurance Awareness Month. Busiest campaign month. |
| **October** | PSM-AEP-REV, AEP opens Oct 15 | **AEP BLACKOUT BEGINS.** PSM-NO-CORE paused. Medicare campaigns dominate. |
| **November** | PSM-AEP-MOVE/G2G/STAY/$0, COV-LTC | Post-review outcome campaigns. Long-Term Care Awareness Month. |
| **December** | PSM-AEP-MOVE/G2G/STAY/$0, AEP closes Dec 7 | Final enrollment window. **AEP BLACKOUT ENDS after Dec 7.** |

### Year-Round Campaigns (Birthday/Trigger-Based)

These campaigns fire based on individual client data, not calendar months:

| Campaign | Trigger |
|----------|---------|
| PSM-SEP-5 | 5-star CMS plan identified in client area |
| PSM-SEP-3 | Client plan drops below 3-star CMS rating |
| PSM-SEP-FEMA | Client in FEMA-declared disaster area (2-month window) |
| PSM-LIFE | Policy anniversary + 30 days |
| PSM-ANN-SUR | Surrender charges drop below 10% |
| PSM-ANN-ALLOC | Policy anniversary (allocation review window) |
| PSM-ANN-LIQ | Surrender charges reach 0% |
| T65-12 through T65+2 | 12 months before through 2 months after 65th birthday |
| AGE-50 through AGE-75 | Client's birthday at milestone age |

---

## 5. AEP Blackout Rules

**October 15 through December 7 is the Annual Enrollment Period for Medicare.** During this window and the surrounding months (October through December), specific rules apply:

### What Changes During AEP Blackout (Oct--Dec)

| Rule | Detail |
|------|--------|
| **PSM-NO-CORE paused** | No cross-sell Medicare outreach during AEP. Regulatory risk and message confusion. |
| **COV-PREAEP stops before Oct** | Pre-AEP outreach wraps by end of September. |
| **Medicare campaigns dominate** | PSM-AEP-REV, MOVE, G2G, STAY, $0 are the priority. Team focused on plan reviews and enrollments. |
| **Non-Medicare campaigns continue** | PSM-LIFE, PSM-ANN-*, all AGE campaigns, COV-LTC (November) run on their own schedules. |
| **No Medicare cross-sell from other engines** | COV campaigns that touch Medicare do not run during this window. |

### What Runs During AEP

| Month | Medicare Campaigns | Non-Medicare Campaigns |
|-------|-------------------|----------------------|
| **October** | PSM-AEP-REV (reviews), PSM-SEP-PREP (stragglers) | PSM-LIFE*, PSM-ANN-*, AGE-* |
| **November** | PSM-AEP-MOVE, G2G, STAY, $0 | PSM-LIFE*, PSM-ANN-*, AGE-*, COV-LTC |
| **December** | PSM-AEP-MOVE, G2G, STAY, $0 (through Dec 7) | PSM-LIFE*, PSM-ANN-*, AGE-* |

*Anniversary/threshold-based, per individual client schedule.

### Key AEP Dates

| Date | Event |
|------|-------|
| **October 15** | AEP opens. Medicare plan changes can begin. |
| **December 7** | AEP closes. Final enrollment deadline. |
| **January 1** | New plan year begins. OEP opens for MA members. |
| **March 31** | OEP closes. Last chance for MA-to-MA switch. |

---

## 6. Cross-Engine Connections

The 4 engines are not silos. They hand off clients, pre-seed conversations, and reinforce each other.

### Primary Handoffs

```
T65+2 --> PSM
    New Medicare client completes T65 journey.
    Exits T65 engine, enters PSM annual service cycle.
    First AEP-REV fires the following October.

COV --> PSM
    Client fills a coverage gap through a COV campaign.
    Once product is in place, enters PSM service cycle for that product type:
        COV-PREAEP --> PSM-SEP-PREP --> PSM-AEP-REV --> annual cycle
        COV-LIAM/LOVE --> PSM-LIFE (anniversary cycle)
        COV-ANN/TAX --> PSM-ANN-ALLOC (anniversary cycle)
        COV-LTC --> standalone LTC management (policy anniversary reviews)
        COV-DI --> standalone DI management (working-age)

AGE --> PSM
    Milestone conversation reveals product need or repositioning opportunity.
    Client enters PSM cycle for the relevant product.
```

### Strategic Pre-Seeds

```
AGE-62 --> T65 pre-seed
    Social Security eligibility conversation at 62 naturally surfaces
    "Medicare starts at 65." Plants awareness 3 years before T65 engine fires.
    Client is mentally prepared when T65-12 arrives.

PSM-NO-CORE <--> COV
    Both target coverage gaps from different angles:
    - PSM-NO-CORE: account-triggered, fires when gap is detected (Jan--Sep)
    - COV-PREAEP: calendar-triggered, fires Jul--Sep as AEP approaches
    - COV-LIAM/LOVE: calendar-triggered for life insurance gaps
    Same goal, different timing and framing. Client receives whichever fires first.

PSM-ANN-SUR/LIQ <--> AGE-73/75
    Annuity events connect to RMD and legacy strategy:
    - PSM-ANN-SUR/LIQ: surrender charge milestones trigger repositioning
    - AGE-73: RMD begins, distribution strategy becomes critical
    - AGE-75: legacy transition, wealth transfer planning
    A client hitting ANN-LIQ near age 73 gets a combined repositioning + RMD conversation.
```

### Cross-Engine Conflict Prevention

| Scenario | Resolution |
|----------|------------|
| COV-PREAEP and PSM-NO-CORE both target same client | PSM-NO-CORE runs Jan--Sep; COV-PREAEP runs Jul--Sep. Client receives first to fire. If PSM-NO-CORE already touched the client, COV-PREAEP is suppressed. |
| COV-LIAM (Sep) and COV-LOVE (Feb) both target life insurance gap | Different timing, different framing. Client can receive both. LIAM is rational ("awareness month"), LOVE is emotional ("protect the people you love"). |
| T65 client also qualifies for AGE-62 | T65 takes priority for Medicare. AGE-62 focuses on Social Security. Both can run simultaneously -- different topics. |
| AEP blackout and COV-LTC (November) | COV-LTC is non-Medicare. It runs during November without conflict. |

---

## 7. Division Distribution

### By Division

| Division | Campaigns | Count |
|----------|-----------|-------|
| **HEALTH** | PSM-SEP-PREP, PSM-AEP-REV, PSM-AEP-MOVE, PSM-AEP-G2G, PSM-AEP-STAY, PSM-AEP-$0, PSM-SEP-5, PSM-SEP-3, PSM-SEP-FEMA, PSM-OEP, PSM-NO-CORE, all T65 (15), COV-PREAEP | **27** |
| **WEALTH** | PSM-ANN-SUR, PSM-ANN-ALLOC, PSM-ANN-LIQ, all AGE (9), COV-ANN, COV-TAX | **14** |
| **LEGACY** | PSM-LIFE, COV-LTC, COV-LIAM, COV-DI, COV-LOVE | **5** |

### By Team Assignment

| Team | Primary Campaigns | Busy Season |
|------|-------------------|-------------|
| **Sales (Vinnie)** | T65 (new enrollment), COV (cross-sell), AGE (milestone conversion) | Year-round, peaks Sep--Dec |
| **Service (Nikki)** | PSM (existing client management), PSM-OEP (benefit checks) | Sep--Mar (AEP + OEP cycle) |
| **Legacy (Aprille)** | PSM-LIFE, COV-LTC, COV-LIAM, COV-LOVE, COV-DI | Sep (LIAM), Nov (LTC), Feb (LOVE), May (DI) |

---

## 8. Merge Field Reference

### Universal Fields (ALL Campaigns)

| Field | Description | Example |
|-------|-------------|---------|
| `{FirstName}` | Client first name | "John" |
| `{LastName}` | Client last name | "Smith" |
| `{AgentName}` | Assigned agent full name | "Sarah Johnson" |
| `{BOBName}` | Book of Business name | "Retirement Protectors" |
| `{Phone}` | Agent phone number | "(515) 555-1234" |
| `{Email}` | Agent email address | "sarah@retireprotected.com" |
| `{CalendarLink}` | Scheduling/booking URL | https://calendly.com/... |

### Product-Specific Fields (PSM, COV -- where product exists)

| Field | Description | Example | Used In |
|-------|-------------|---------|---------|
| `{Carrier}` | Insurance carrier name | "Humana", "North American", "Kansas City Life" | PSM, COV |
| `{ProductName}` | Specific product name | "Gold Plus", "Versachoice 10", "Supernova" | PSM, COV |
| `{ProductType}` | Product category | "Medicare Advantage", "fixed index annuity", "universal life" | PSM, COV |
| `{PlanName}` | Medicare plan name (carrier + product) | "Humana Gold Plus" | PSM Medicare campaigns |

### T65-Specific Fields

| Field | Description | Example |
|-------|-------------|---------|
| `{BirthdayMonth}` | Client's 65th birthday month | "March 2026" |
| `{IEPStart}` | IEP window open date (3 months before birthday) | "December 2025" |
| `{IEPEnd}` | IEP window close date (3 months after birthday) | "June 2026" |
| `{MedigapDeadline}` | 6 months from Part B effective date | "September 2026" |

### AGE-Specific Fields

| Field | Description | Example |
|-------|-------------|---------|
| `{MilestoneAge}` | The milestone age being reached | "59 and a half", "73" |
| `{MilestoneYear}` | Calendar year the milestone occurs | "2026" |

---

## 9. BOB Customization Notes

### Brand-Agnostic Design

All campaign content is designed to work across any Book of Business (BOB):

| Principle | Detail |
|-----------|--------|
| **`{BOBName}` merge field** | Every campaign uses `{BOBName}` instead of hardcoded brand names. Works for RPI, Millang Financial, or any acquired BOB. |
| **No brand-specific language** | Content blocks never reference "Retirement Protectors" or any specific agency name directly. |
| **Consistent tone** | "We're your people" energy regardless of which BOB is delivering the campaign. |
| **Agent-centric** | The agent is the face of the relationship. The BOB provides the infrastructure. The client's loyalty is to the agent first, the brand second. |

### Multi-BOB Deployment

When RPI acquires a book of business:
1. Set `{BOBName}` to the acquired agency's name (or RPI's, depending on transition strategy)
2. Set `{AgentName}` to the servicing agent
3. All 46 campaigns work immediately -- no content changes required
4. Tone, messaging, and strategy are identical across all BOBs

---

## 10. Content Block Reference

### Block Structure

Every campaign has **8 content blocks**, each serving a specific channel or function:

| Block Type | Purpose | Channel |
|------------|---------|---------|
| **SubjectLine** | Email subject line | Email |
| **Introduction** | Opening paragraph with personalization | Email |
| **ValueProp** | Core value proposition / education | Email, USPS |
| **PainPoint** | Risk articulation / what happens without action | Email, USPS |
| **CTA** | Call to action (schedule, call, connect) | All channels |
| **TextTemplate** | Full SMS/text message | Text/SMS |
| **VMScript** | Voicemail drop script | Voicemail |
| **EmailBody** | Complete email body (assembled from blocks) | Email |

### Block ID Format

```
{TYPE_PREFIX}-{ENGINE}-{CAMPAIGN}-001

Examples:
    SL-PSM-SEP-PREP-001     (SubjectLine for PSM-SEP-PREP)
    VP-T65-12-001            (ValueProp for T65-12)
    TXT-COV-LOVE-001         (TextTemplate for COV-LOVE)
    VM-AGE-73-001            (VMScript for AGE-73)
```

**Type Prefixes:**

| Prefix | Block Type |
|--------|-----------|
| SL | SubjectLine |
| INTRO | Introduction |
| VP | ValueProp |
| PP | PainPoint |
| CTA | CTA |
| TXT | TextTemplate |
| VM | VMScript |
| EB | EmailBody |

### Content Staging Files

Raw content blocks are staged in these files before being loaded into C3:

| File | Engine | Campaigns | Blocks |
|------|--------|-----------|--------|
| `_PSM_CONTENT_STAGING.md` | PSM | 15 | 120 |
| `_T65_CONTENT_STAGING.md` | T65 | 15 | 120 |
| `_COV_CONTENT_STAGING.md` | COV | 7 | 56 |
| `_AGE_CONTENT_STAGING.md` | AGE | 9 | 72 |
| **Total** | | **46** | **368** |

### Knowledge Documents

Detailed campaign strategy, psychology, agent coaching, and compliance notes:

| File | Engine |
|------|--------|
| `PSM_PROACTIVE_SERVICE.md` | PSM -- Proactive Service Model |
| `T65_MEDICARE_BIRTHDAY.md` | T65 -- Medicare Birthday Countdown |
| `COV_CALENDAR_COVERAGE.md` | COV -- Calendar Coverage Events |
| `AGE_WEALTH_MILESTONES.md` | AGE -- Wealth Milestones |

All files located in: `_RPI_STANDARDS/reference/campaigns/`

---

## 11. Tone Rules (All Engines)

These rules are universal across all 46 campaigns, all 4 channels.

| Rule | Detail |
|------|--------|
| **No "free" language** | Commission-based model. There is no cost to imply the absence of. Never use the word "free." |
| **No urgency/sales mechanics** | No "15 minutes," "today only," "Reply YES," countdown timers, scarcity tactics. This is service and education, not sales. |
| **No technical jargon** | No "IEP," "EHR," "Blue Button," "formulary tier," "actuarial," "elimination period," "non-forfeiture," "creditable coverage." Use plain language always. |
| **Commission transparency** | Never mention commission. Never imply RPI charges the client. The service exists because "this is what we do." |
| **Always personalize** | Every touch includes `{FirstName}`, `{AgentName}`, and product-specific fields where applicable. |
| **No sales language** | No "opportunity of a lifetime," "act now," "don't miss out," "limited time." |
| **Agent as advisor** | The agent has already done the work. They are presenting data, not pitching. |
| **Energy** | Warm, confident, competent. "We're your people, this is what we do, let's connect." |

---

## 12. Compliance Quick Reference

### By Campaign Type

| Scenario | Requirement |
|----------|-------------|
| **Discussing specific Medicare plans** | Scope of Appointment (SOA) required before the conversation |
| **AEP blackout (Oct--Dec)** | No Medicare cross-sell. PSM-NO-CORE paused. COV-PREAEP stops before Oct. |
| **1035 exchange discussion** | Full suitability analysis required |
| **Life insurance replacement** | Suitability analysis + state replacement form where required |
| **Tax-related conversations** | RPI agents are NOT tax advisors. Always recommend consulting a qualified tax professional. |
| **PHI data** | Stored in Google Workspace ONLY. Never Slack, text, or personal email. |
| **Authorization/data access** | Client must actively consent. Document type and date. Never imply access to full medical records. |
| **FEMA SEP** | Confirm client ZIP is in declared area. Window = 2 months from END of declared emergency. |
| **Medigap guaranteed issue** | 6 months from Part B effective date. Miss it = potential medical underwriting forever. |
| **IEP penalties** | Part B: 10% per 12-month gap, PERMANENT. Part D: 1% of NBBP per month without creditable coverage, PERMANENT. |
| **COBRA / Retiree plans** | Do NOT protect from late enrollment penalties. Most common and costly mistake in Medicare. |

---

## 13. System Architecture

### Where Campaigns Live

```
C3 (Content/Campaign Manager)
    |
    |--> Campaign definitions (all 46)
    |--> Content blocks (368 blocks)
    |--> Template assembly (506 touchpoints)
    |--> Trigger rules + scheduling
    |
    v
PRODASH (Client Portal / Delivery Engine)
    |
    |--> Email delivery
    |--> SMS/Text delivery
    |--> Voicemail drop
    |--> USPS mailer queue
    |
    v
RAPID_MATRIX (Data Source)
    |
    |--> Client records (products, coverage, demographics)
    |--> Policy data (anniversaries, surrender schedules, carriers)
    |--> Healthcare data (P3, authorizations, CMS ratings)
    |--> Agent assignments (BOB, team, contact info)
```

### Data Dependencies

| Engine | Required Data |
|--------|---------------|
| **PSM** | Client product records, policy anniversaries, surrender schedules, CMS star ratings, FEMA declarations, authorization status, P3 data |
| **T65** | Client DOB, employer coverage status, P3 data, authorization status, IEP dates |
| **AGE** | Client DOB, qualified account balances, Social Security estimates, annuity details |
| **COV** | Client product inventory (what they have), gap detection (what they do NOT have), carrier/product merge fields |

---

## Document Map

For detailed information on any engine, read the corresponding knowledge document:

| Document | What It Covers |
|----------|---------------|
| **CAMPAIGN_MASTER_INDEX.md** (this file) | Cross-engine overview, calendar, connections, quick reference |
| **PSM_PROACTIVE_SERVICE.md** | 15 PSM campaigns: trigger details, psychology, agent coaching, compliance, cross-sell opportunities |
| **T65_MEDICARE_BIRTHDAY.md** | 15 T65 campaigns: IEP rules, phase progression, path branching, enrollment mechanics |
| **COV_CALENDAR_COVERAGE.md** | 7 COV campaigns: awareness month timing, gap detection logic, PSM handoff patterns |
| **AGE_WEALTH_MILESTONES.md** | 9 AGE campaigns: milestone rules, IRS regulations, Social Security strategy, RMD mechanics |

---

*We're Your People.(TM)*
