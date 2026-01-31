# RPI Platform Blueprint

> **Version**: v0.2  
> **Created**: January 13, 2026  
> **Updated**: January 26, 2026  
> **Author**: Josh D. Millang + Claude  
> **Purpose**: Five-layer system architecture (Datasets → Experiences)  
> **Status**: Active - References THREE_PLATFORM_ARCHITECTURE.md

---

## ⚠️ Architecture Update Notice

**The platform architecture has evolved to a three-platform model.**

For the current master architecture including:
- Three platforms: **SENTINEL** (B2B), **RIIMO** (B2E), **PRODASH** (B2C)
- Three MATRIXes: SENTINEL_MATRIX, RAPID_MATRIX, PRODASH_MATRIX
- Channel definitions: RPI, DAVID, RAPID
- SuperProject folder structure
- Pipeline stages per platform

**See: `THREE_PLATFORM_ARCHITECTURE.md`**

This Blueprint document remains valid for:
- Five-layer architecture concept (Datasets → Experiences)
- Use-case definitions and workflows
- Build sequence concepts

---

## The Mission

> **Tearing the Health + Wealth + Legacy Industries to the ground, and #RunningOurOwnRACE — Rebuilding Around the Client Experience.**

---

## The Outcome

**Capture every retail client relationship in the US who needs a resource for their Health + Wealth + Legacy in Retirement.**

This document maps every piece required to achieve that outcome.

---

## Blueprint Overview

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    THE COMPLETE SYSTEM                       │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              LAYER 5: USE-CASES                      │   │
│   │         What each team actually DOES                 │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ▲                                  │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              LAYER 4: EXPERIENCES                    │   │
│   │         Team AI interfaces                           │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ▲                                  │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              LAYER 3: APPLICATIONS                   │   │
│   │         Business logic + calculations                │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ▲                                  │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              LAYER 2: DATABASES                      │   │
│   │         Structured data stores                       │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ▲                                  │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              LAYER 1: DATASETS                       │   │
│   │         Raw data sources                             │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# LAYER 1: DATASETS

> **What data exists or needs to exist?**

## 1.1 Internal Business Data

| Dataset | Description | Source | Status |
|---------|-------------|--------|--------|
| Client Data | Demographics, contact info, relationships | MATRIX | ✅ Exists |
| Account Data | Policies, balances, holdings | MATRIX | ✅ Exists |
| Agent Data | Producers, hierarchies, credentials | MATRIX | ✅ Exists |
| Carrier Data | Products, contacts, requirements | MATRIX | ✅ Exists |
| Revenue Data | Commissions, production, projections | MATRIX | ✅ Exists |
| *[Add more...]* | | | |

## 1.2 Client Health Data

| Dataset | Description | Source | Status |
|---------|-------------|--------|--------|
| Electronic Health Records | Diagnoses, treatments, providers | EHR System | 🔲 Planned |
| Medicare Blue Button | Claims history, medications, costs | CMS Blue Button API | 🔲 Planned |
| Provider Relationships | PCPs, specialists, facilities | NPI + internal | 🔲 Planned |
| *[Add more...]* | | | |

## 1.3 Plan & Coverage Data

| Dataset | Description | Source | Status |
|---------|-------------|--------|--------|
| Medicare Advantage Plans | Benefits, networks, costs | CMS Plan Finder | 🔲 Planned |
| Part D Prescription Plans | Formularies, tiers, costs | CMS | 🔲 Planned |
| Supplement Plans | Medigap options by state | Carriers | 🔲 Planned |
| Provider Networks | Who's in-network for what | Plan data | 🔲 Planned |
| Formulary Data | Drug coverage by plan | CMS | 🔲 Planned |
| *[Add more...]* | | | |

## 1.4 Reference Data

| Dataset | Description | Source | Status |
|---------|-------------|--------|--------|
| NPI Registry | Provider identifiers | CMS NPPES | ✅ MCP Built |
| ICD-10 Codes | Diagnosis/procedure codes | NIH | ✅ MCP Built |
| CMS Coverage Policies | NCDs, LCDs, coverage rules | CMS | ✅ MCP Built |
| ZIP Code Data | Demographics, plan availability | Census + CMS | 🔲 Planned |
| *[Add more...]* | | | |

## 1.5 Communication Data

| Dataset | Description | Source | Status |
|---------|-------------|--------|--------|
| Email History | Client/agent communications | Gmail | 🔲 Planned |
| Call Logs | Contact history | Phone system | 🔲 Planned |
| Documents | Contracts, forms, applications | Google Drive | 🔲 Planned |
| Team Messages | Internal coordination | Slack | 🔲 Planned |
| *[Add more...]* | | | |

---

# LAYER 2: DATABASES

> **How is data structured and connected?**

## 2.1 MATRIX (Core Business Database)

**Platform**: Google Sheets  
**Purpose**: Central source of truth for business operations

| Sheet/Table | Primary Data | Key Relationships |
|-------------|--------------|-------------------|
| Clients | Client records | → Accounts, → Agents |
| Accounts | Policy/account records | → Clients, → Carriers |
| Agents | Producer records | → Clients, → Hierarchy |
| Carriers | Carrier/product info | → Accounts |
| Revenue | Commission records | → Accounts, → Agents |
| *[Add more...]* | | |

## 2.2 Health Records Database

**Platform**: [TBD - Google Sheets / SQL / Other]  
**Purpose**: Client health information for plan optimization

| Table | Primary Data | Key Relationships |
|-------|--------------|-------------------|
| Client_Health_Profile | Demographics, conditions | → MATRIX.Clients |
| Claims_History | Blue Button claims | → Client_Health_Profile |
| Medications | Current prescriptions | → Client_Health_Profile |
| Providers | Client's care team | → NPI Registry |
| *[Add more...]* | | |

## 2.3 Plan Database

**Platform**: [TBD]  
**Purpose**: All available plan options for comparison

| Table | Primary Data | Key Relationships |
|-------|--------------|-------------------|
| MA_Plans | Medicare Advantage plans | → Networks, → Formularies |
| PDP_Plans | Part D plans | → Formularies |
| Supplement_Plans | Medigap options | → State availability |
| Networks | Provider networks by plan | → NPI Registry |
| Formularies | Drug coverage by plan | → Medications |
| *[Add more...]* | | |

## 2.4 Data Relationships Map

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA RELATIONSHIPS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   CLIENT (MATRIX)                                           │
│      │                                                       │
│      ├──→ ACCOUNTS ──→ CARRIERS                             │
│      │                                                       │
│      ├──→ HEALTH_PROFILE                                    │
│      │       │                                               │
│      │       ├──→ CLAIMS_HISTORY                            │
│      │       ├──→ MEDICATIONS ──→ FORMULARIES               │
│      │       └──→ PROVIDERS ──→ NPI_REGISTRY                │
│      │                                                       │
│      ├──→ CURRENT_PLANS ──→ PLAN_DATABASE                   │
│      │                                                       │
│      └──→ AGENT ──→ AGENT_HIERARCHY                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# LAYER 3: APPLICATIONS

> **What business logic operates on the data?**

## 3.1 Current Applications

| Application | Purpose | Key Functions | Database Access |
|-------------|---------|---------------|-----------------|
| **PRODASH** | Client/Account Portal | Client lookup, account management, RMD tracking | MATRIX |
| **DAVID-HUB** | BD Operations | Agent management, recruiting, production | MATRIX |
| **CAM** | Commission Management | Commission tracking, splits, projections | MATRIX |
| **SENTINEL** | [Purpose] | [Functions] | [Databases] |
| **C³** | Content Management | Campaigns, content blocks, scheduling | Content DB |
| *[Add more...]* | | | |

## 3.2 Planned Applications

| Application | Purpose | Key Functions | Database Access |
|-------------|---------|---------------|-----------------|
| **Plan Optimizer** | Plan comparison & recommendation | Cost projection, network matching, formulary check | Health + Plans |
| **RMD Center** | RMD management | Calculations, tracking, notifications | MATRIX |
| **Client 360** | Complete client view | Unified profile across all data | All |
| **Agent Portal** | Agent self-service | Production, clients, commissions | MATRIX |
| *[Add more...]* | | | |

## 3.3 Application → MCP Mapping

When each app becomes an MCP server:

| Application | MCP Server | Tools Exposed |
|-------------|------------|---------------|
| PRODASH | `prodash-mcp` | `get_client`, `get_accounts`, `search_clients` |
| DAVID-HUB | `david-mcp` | `get_agent`, `recruiting_pipeline`, `production_report` |
| CAM | `cam-mcp` | `get_commissions`, `calculate_split`, `project_revenue` |
| Plan Optimizer | `plan-optimizer-mcp` | `compare_plans`, `calculate_costs`, `check_network` |
| *[Add more...]* | | |

---

# LAYER 4: EXPERIENCES

> **How do teams interact with the system?**

## 4.1 Team AI Interfaces

| Interface | Primary Users | Data Access | Key Capabilities |
|-----------|---------------|-------------|------------------|
| **Sales AI** | Sales team | Clients, Plans, Prospects | Lead qualification, plan matching, follow-up prompts |
| **Service AI** | Service team | Clients, Accounts, Health, Plans | RMD management, plan changes, issue resolution |
| **BD AI** | Business Development | Agents, Recruiting, Production | Pipeline management, recruiting, performance tracking |
| **Marketing AI** | Marketing team | Content, Campaigns, Analytics | Campaign creation, content assembly, performance |
| **Compliance AI** | Compliance | All + Audit logs | Rule checking, documentation, audit prep |
| **Executive AI** | Leadership | All + Analytics | Dashboards, forecasts, strategic insights |
| *[Add more...]* | | | |

## 4.2 Experience Specifications

### Sales AI Experience

```
┌─────────────────────────────────────────────────────────────┐
│                      SALES AI                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PERSONA:                                                    │
│  "Help me find and close opportunities"                     │
│                                                              │
│  CAN ACCESS:                                                 │
│  ├── Client/Prospect data                                   │
│  ├── Plan comparison tools                                  │
│  ├── NPI Registry (provider lookups)                        │
│  ├── CMS Coverage (plan details)                            │
│  └── Calendar (scheduling)                                  │
│                                                              │
│  EXAMPLE QUERIES:                                            │
│  • "Who's turning 65 in my territory next month?"           │
│  • "Compare plan options for this client's situation"       │
│  • "What objections might this prospect have?"              │
│  • "Draft a follow-up email for yesterday's meeting"        │
│                                                              │
│  CANNOT ACCESS:                                              │
│  • Commission details                                        │
│  • Agent hierarchies                                         │
│  • Internal financials                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Service AI Experience

```
┌─────────────────────────────────────────────────────────────┐
│                     SERVICE AI                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PERSONA:                                                    │
│  "Help me take care of our clients"                         │
│                                                              │
│  CAN ACCESS:                                                 │
│  ├── Full client profiles                                   │
│  ├── Account/policy details                                 │
│  ├── Health records (with permission)                       │
│  ├── Plan details and benefits                              │
│  ├── RMD calculations                                       │
│  ├── Service history                                        │
│  └── Provider networks                                      │
│                                                              │
│  EXAMPLE QUERIES:                                            │
│  • "What RMDs are due this week?"                           │
│  • "Client's doctor is retiring - check new doc's network"  │
│  • "Pull everything I need for this client's annual review" │
│  • "What's the status of the Jones service request?"        │
│                                                              │
│  CANNOT ACCESS:                                              │
│  • Sales pipeline                                            │
│  • Recruiting data                                           │
│  • Commission structures                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### [Additional Experience Templates - To Be Completed]

- BD AI Experience
- Marketing AI Experience
- Compliance AI Experience
- Executive AI Experience

---

# LAYER 5: USE-CASES

> **What does each team actually DO?**

## 5.1 Client Lifecycle Use-Cases

| Use-Case | Trigger | Teams Involved | Data Needed | Apps Used |
|----------|---------|----------------|-------------|-----------|
| **New Client Onboarding** | Sale closed | Sales → Service | Client info, health profile, plan selection | PRODASH, Plan Optimizer |
| **Annual Plan Review** | Anniversary date | Service | Health changes, plan changes, costs | Service AI, Plan Optimizer |
| **RMD Processing** | RMD due date | Service | Account data, distribution rules | RMD Center |
| **PCP Change** | Provider retiring/moving | Service | Provider networks, plan compatibility | Service AI, NPI |
| **Plan Optimization** | AEP/OEP or life change | Service/Sales | Claims history, current costs, alternatives | Plan Optimizer |
| **Beneficiary Update** | Life event | Service | Account data, legal requirements | PRODASH |
| *[Add more...]* | | | | |

## 5.2 Agent Lifecycle Use-Cases

| Use-Case | Trigger | Teams Involved | Data Needed | Apps Used |
|----------|---------|----------------|-------------|-----------|
| **Agent Recruiting** | Pipeline activity | BD | Candidate info, market data | DAVID-HUB |
| **Agent Onboarding** | Contract signed | BD → Ops | Credentials, training, assignments | DAVID-HUB |
| **Production Tracking** | Ongoing | BD, Agents | Sales data, commission data | CAM, DAVID-HUB |
| **Agent Support** | Issue raised | BD | Agent profile, production history | BD AI |
| *[Add more...]* | | | | |

## 5.3 Operational Use-Cases

| Use-Case | Trigger | Teams Involved | Data Needed | Apps Used |
|----------|---------|----------------|-------------|-----------|
| **Commission Reconciliation** | Carrier payment | Operations | Expected vs received | CAM |
| **Compliance Audit** | Scheduled/triggered | Compliance | All relevant records | Compliance AI |
| **Campaign Execution** | Marketing calendar | Marketing | Content, segments, channels | C³ |
| **Executive Reporting** | Weekly/monthly | Leadership | All metrics | Executive AI |
| *[Add more...]* | | | | |

## 5.4 Critical Complex Use-Cases

### Use-Case: Provider Network Change

**Scenario**: Dr. Skir is retiring. His replacement is Dr. Johnston.

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER: Provider retiring notification                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STEP 1: Identify affected clients                          │
│  └── Query: Clients where PCP = Dr. Skir                    │
│  └── Data: MATRIX + Health Profile                          │
│                                                              │
│  STEP 2: Verify replacement provider                        │
│  └── Query: NPI lookup for Dr. Johnston                     │
│  └── Data: NPI Registry                                     │
│                                                              │
│  STEP 3: Check network compatibility                        │
│  └── Query: Is Dr. Johnston in-network for each plan?       │
│  └── Data: Plan Networks                                    │
│                                                              │
│  STEP 4: Identify at-risk clients                           │
│  └── Logic: Clients where new PCP not in current network    │
│  └── Output: List of clients needing plan review            │
│                                                              │
│  STEP 5: Calculate optimal alternatives                     │
│  └── Query: Plans where Dr. Johnston in-network             │
│  └── Logic: Cost projection based on 3yr claims             │
│  └── Data: Claims History + Plan Database                   │
│                                                              │
│  STEP 6: Generate action plan                               │
│  └── Output: Prioritized client list with recommendations   │
│  └── Output: Draft communications                           │
│  └── Output: Task assignments                               │
│                                                              │
│  TEAMS: Service (primary), Sales (if plan change needed)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### [Additional Complex Use-Cases - To Be Documented]

- Annual Enrollment Period (AEP) Campaign
- Large Group Rollover
- Carrier Exit from Market
- Compliance Investigation
- Agent Termination with Book Transfer

---

# BUILD SEQUENCE

> **What order do we build, and what unlocks what?**

## Phase 1: Foundation (Current)

| Component | Status | Unlocks |
|-----------|--------|---------|
| MATRIX (core business data) | ✅ Active | All apps |
| RAPID_API (data access layer) | ✅ Active | All apps |
| RPI-Standards (documentation) | ✅ Active | Agent efficiency |
| Reference MCPs (NPI, ICD-10, CMS) | ✅ Built | Healthcare queries |

**Outcome**: Core business operations + healthcare reference data

---

## Phase 2: Data Access (Next)

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| Google Sheets MCP | None | Direct MATRIX queries via AI |
| Google Drive MCP | None | Document search via AI |
| PRODASH completion | MATRIX | Client/Account management |

**Outcome**: AI can query business data directly

---

## Phase 3: Health Data Integration

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| Health Records Database | Schema design | Client health profiles |
| Blue Button Integration | Health DB | Claims history access |
| Provider Relationships | Health DB + NPI | Care team visibility |

**Outcome**: Complete client health picture

---

## Phase 4: Plan Intelligence

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| Plan Database | Schema design | Plan comparison |
| Network Data Integration | Plan DB + NPI | Network matching |
| Formulary Integration | Plan DB | Drug coverage checking |
| Plan Optimizer App | All above | Cost projections |

**Outcome**: Intelligent plan recommendations

---

## Phase 5: Application MCPs

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| PRODASH MCP | PRODASH complete | AI client queries with logic |
| Plan Optimizer MCP | Plan Optimizer complete | AI plan comparisons |
| CAM MCP | CAM complete | AI commission queries |
| DAVID-HUB MCP | DAVID-HUB complete | AI agent queries |

**Outcome**: AI has access to business logic, not just raw data

---

## Phase 6: Team Experiences

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| Service AI Interface | Phase 5 MCPs | Service team AI assistant |
| Sales AI Interface | Phase 5 MCPs | Sales team AI assistant |
| BD AI Interface | Phase 5 MCPs | BD team AI assistant |
| Executive AI Interface | All MCPs | Leadership dashboard |

**Outcome**: Every team has AI-powered operations

---

## Phase 7: Advanced Capabilities

| Component | Dependencies | Unlocks |
|-----------|--------------|---------|
| Predictive Analytics | Historical data | Proactive recommendations |
| Automated Workflows | All systems | AI-initiated actions |
| External Integrations | API development | Carrier/partner connectivity |

**Outcome**: System that acts, not just answers

---

# SUCCESS METRICS

> **How do we know it's working?**

## Operational Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Time to answer client question | [X] minutes | [Y] seconds | Service team tracking |
| RMD processing time | [X] hours | [Y] minutes | RMD Center logs |
| Plan comparison accuracy | [X]% | [Y]% | Audit sampling |
| Client retention rate | [X]% | [Y]% | MATRIX tracking |
| *[Add more...]* | | | |

## Strategic Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Market share (target segment) | [X]% | [Y]% | Industry data |
| Revenue per employee | $[X] | $[Y] | Financial tracking |
| Client acquisition cost | $[X] | $[Y] | Marketing analytics |
| Agent productivity | [X] clients | [Y] clients | DAVID-HUB |
| *[Add more...]* | | | |

---

# NEXT STEPS

## For JDM (When You Wake Up)

1. **Review this structure** - Does it capture the right layers?
2. **Fill in the gaps** - What datasets/apps/use-cases are missing?
3. **Validate the sequence** - Is the build order right?
4. **Add specifics** - What are the actual numbers, names, details?

## Questions to Answer

- [ ] What datasets exist that aren't listed?
- [ ] What apps are planned that aren't listed?
- [ ] What use-cases are critical that aren't documented?
- [ ] What's the priority order for Phase 2 and beyond?
- [ ] What external systems need integration?
- [ ] What team roles are missing from the Experiences layer?

---

# APPENDIX

## A. Glossary

| Term | Definition |
|------|------------|
| MATRIX | Core Google Sheets business database |
| MCP | Model Context Protocol - AI tool access standard |
| Blue Button | CMS standard for patient health data access |
| AEP | Annual Enrollment Period (Medicare) |
| OEP | Open Enrollment Period (Medicare) |
| RMD | Required Minimum Distribution |
| NPI | National Provider Identifier |
| *[Add more...]* | |

## B. Related Documents

| Document | Purpose |
|----------|---------|
| `0-Setup/AI_PLATFORM_STRATEGIC_ROADMAP.md` | Strategic vision and competitive positioning |
| `0-Setup/MCP_TOOLS_SETUP.md` | MCP server setup and tool reference |
| `0-Setup/MASTER_AGENT_FRAMEWORK.md` | Agent roles and patterns |

## C. Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jan 13, 2026 | Initial structure - awaiting JDM input |

---

*This is the master blueprint. Every project builds toward this vision.*

*"Tearing the Health + Wealth + Legacy Industries to the ground, and #RunningOurOwnRACE — Rebuilding Around the Client Experience."*
