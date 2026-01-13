# RPI AI Platform - Strategic Roadmap & Architecture Guide

> **Version**: v1.2  
> **Created**: January 13, 2026  
> **Author**: Josh D. Millang + Claude  
> **Scope**: Universal - Defines the AI-powered future of RPI operations  
> **Status**: Strategic Vision + Active Development

---

## The Mission

> **Tearing the Health + Wealth + Legacy Industries to the ground, and #RunningOurOwnRACE — Rebuilding Around the Client Experience.**

This platform is how we execute that mission at scale.

---

## Executive Summary

RPI is building an **AI-powered business operating system** that unifies all company data, applications, and workflows under a conversational AI interface. This document outlines the vision, architecture, and roadmap for agents and projects to understand where they fit in the big picture.

**The Goal**: Any team member can ask questions like:
> "Which clients need plan changes because their PCP is retiring, and what are their optimal alternatives based on 3 years of claims history?"

And get an actionable, data-driven answer in seconds instead of days.

---

## Strategic Context: Why This Matters

### The Platform vs. The Weapon

Companies like Palantir build enterprise AI platforms and sell them for $5M-$50M+. They provide empty infrastructure that customers must fill with their own expertise, data, and workflows.

**RPI is not building a platform to sell. RPI is building a platform to dominate.**

| Platform Company (Palantir) | RPI/DAVID |
|-----------------------------|-----------|
| Builds the platform | Builds the platform |
| Sells it for millions | **Uses it to own the market** |
| Customers win battles | **We win the war** |
| Value = licensing fees | **Value = market capture** |
| Platform is the product | **Platform is the weapon** |

### Why This Is Unsellable

```
What Palantir Sells:              What We're Building:
┌─────────────────────┐           ┌─────────────────────────────────┐
│                     │           │                                 │
│   Empty Platform    │           │   20+ years domain expertise    │
│                     │           │   Encoded operational workflows │
│   + "Figure it out" │           │   Market relationships          │
│                     │           │   Competitive intelligence      │
│                     │           │   Industry-specific logic       │
│                     │           │                                 │
└─────────────────────┘           └─────────────────────────────────┘
         ↓                                      ↓
   They charge $50M                     This IS the moat
   for empty infrastructure             No price tag exists
```

**You cannot sell domain expertise. You can only deploy it.**

Even if a competitor purchased the most expensive enterprise AI platform on the market, they would have empty infrastructure. It would take them 20 years to encode the knowledge that RPI is systematically building into this system.

### The Knowledge Transfer Problem

Traditional businesses face an impossible challenge:
- Expert knowledge lives in people's heads
- Training and documentation capture only a fraction
- New hires take years to develop pattern recognition
- Key person departures create permanent knowledge gaps
- Scaling requires proportional headcount growth

**This platform solves that problem.**

Every workflow, calculation, decision tree, and domain insight gets encoded into applications that become AI-accessible. The platform doesn't just store information—it operationalizes expertise.

### The Competitive Endgame

```
CURRENT STATE (Industry):

Carriers ←────────────────────────────────────────→ Clients
            Agents, Brokers, Advisors (fragmented)
            Manual processes, tribal knowledge
            Inconsistent outcomes, scaling limits

FUTURE STATE (RPI/DAVID):

Carriers ←─────── RPI/DAVID AI Platform ──────→ Clients
                          │
                          │  Owns the middle layer
                          │  Sees everything
                          │  Acts instantly
                          │  Scales infinitely
                          │
                          ↓
              Health + Wealth + Legacy
              Every layer between Carrier and Client
```

### Why No One Can Catch Up

| Requirement | Competitors | RPI/DAVID |
|-------------|-------------|-----------|
| AI Platform | Could buy one | Building it |
| Domain Expertise | Would take 20 years | Already have it |
| Proprietary Data | Don't have ours | We own it |
| Industry Relationships | Would take decades | Already built |
| Coded Workflows | Can't copy what's not written | Encoding it now |

The platform isn't the asset. **The market position it enables is the asset.**

### What This Means For Your Work

Every application you build, every function you write, every workflow you encode adds to this strategic advantage. You're not just shipping features—you're building the operational infrastructure for market dominance.

**This is why quality matters. This is why documentation matters. This is why getting it right matters.**

The compound effect of every well-built piece creates a capability gap that competitors cannot close.

---

## Part 1: Core Concepts

### What is MCP?

**MCP (Model Context Protocol)** is a standard that lets AI assistants (like Claude) access external tools and data. Think of it as giving the AI "hands" to reach into databases, APIs, and applications.

| Without MCP | With MCP |
|-------------|----------|
| "Look up that NPI and paste it here" | "Look up NPI 1234567890" → instant results |
| AI can only see what you show it | AI queries data sources directly |
| You do the research, AI helps analyze | AI does research AND analysis |

### The Google Search Analogy

| Google Search | RPI AI Platform |
|---------------|-----------------|
| Indexes the public web | Indexes YOUR data |
| Returns links | Returns analyzed answers |
| You read and synthesize | AI reads and synthesizes |
| Can't take action | Can take action |
| Generic | Built on YOUR domain expertise |

---

## Part 2: Architecture Overview

### The Four Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     LAYER 1: AI INTERFACE                    │
│                                                              │
│   Claude (via Cursor, GAS Web Apps, or Claude.ai)           │
│   "I understand questions and orchestrate the answer"       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                         MCP Protocol
                              │
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 2: MCP SERVERS                      │
│                   (The Connection Layer)                     │
│                                                              │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│   │  Raw Data   │ │  App Logic  │ │  Reference  │          │
│   │    MCPs     │ │    MCPs     │ │    MCPs     │          │
│   └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 3: BUSINESS LOGIC                     │
│               (Your Apps & Calculations)                     │
│                                                              │
│   PRODASH │ DAVID-HUB │ CAM │ SENTINEL │ C³ │ Future Apps  │
│                                                              │
│   "We contain Josh's domain expertise, coded into logic"    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 4: DATA STORES                      │
│                                                              │
│   MATRIX │ Google Drive │ Gmail │ Slack │ External APIs    │
│                                                              │
│   "We store the raw data"                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### What Each Layer Does

| Layer | Purpose | Examples |
|-------|---------|----------|
| **AI Interface** | Understands questions, orchestrates tools, explains results | Claude in Cursor, GAS web app chat |
| **MCP Servers** | Bridges between AI and data/apps | npi-registry, matrix-mcp, prodash-mcp |
| **Business Logic** | Calculations, validation, domain rules | RMD calculations, commission logic, plan comparisons |
| **Data Stores** | Raw data storage | MATRIX (Sheets), Drive, external APIs |

---

## Part 3: MCP Server Types

### Three Categories

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP SERVER TYPES                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. RAW DATA MCPs                                           │
│     └── Direct access to data stores                        │
│     └── Simple queries, no business logic                   │
│     └── Examples: matrix-mcp, drive-mcp, gmail-mcp          │
│                                                              │
│  2. APPLICATION MCPs                                        │
│     └── Your apps exposed as MCP tools                      │
│     └── Contains business logic and calculations            │
│     └── Examples: prodash-mcp, cam-mcp, rmd-center-mcp     │
│                                                              │
│  3. REFERENCE MCPs                                          │
│     └── External public data sources                        │
│     └── Industry/regulatory data                            │
│     └── Examples: npi-registry, icd10-codes, cms-coverage  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Current Status

| MCP Server | Type | Status | What It Does |
|------------|------|--------|--------------|
| `npi-registry` | Reference | ✅ Built | Healthcare provider lookups |
| `icd10-codes` | Reference | ✅ Built | Diagnosis/procedure codes |
| `cms-coverage` | Reference | ✅ Built | Medicare coverage info |
| `matrix-mcp` | Raw Data | 🔲 Planned | Direct MATRIX queries |
| `drive-mcp` | Raw Data | 🔲 Planned | Google Drive search/read |
| `prodash-mcp` | Application | 🔲 Future | Client/account logic |
| `cam-mcp` | Application | 🔲 Future | Commission calculations |

---

## Part 4: The Key Insight - Apps Become MCPs

**Your apps ARE the middleware.**

Every GAS application you build contains business logic that represents your domain expertise. Instead of building separate calculation engines, your apps themselves become MCP servers.

```
TODAY:
┌──────────┐         ┌──────────┐
│  User    │ ──UI──► │  PRODASH │ ──► MATRIX
│ (clicks) │         │  (app)   │
└──────────┘         └──────────┘

FUTURE:
┌──────────┐         ┌──────────┐
│  User    │ ──UI──► │  PRODASH │ ──► MATRIX
│ (clicks) │         │  (app)   │
└──────────┘         └──────────┘
                           ▲
┌──────────┐               │
│  Claude  │ ──MCP─────────┘
│  (asks)  │
└──────────┘

Same app. Same logic. Two access methods.
```

### Why This Matters

| Building Separately | Apps as MCPs |
|--------------------|--------------|
| Build app + build MCP + build middleware | Build app once, expose as MCP |
| Logic duplicated | Logic in one place |
| Maintenance nightmare | Update app, MCP updates too |
| Slow to build | Already building it |

---

## Part 5: What Claude Can vs Can't Do

### The Division of Labor

| Claude's Job | NOT Claude's Job |
|--------------|------------------|
| Understand natural language | Complex actuarial calculations |
| Decide which tools to call | Process thousands of records |
| Synthesize multiple data sources | Guarantee numerical accuracy |
| Explain findings clearly | Apply intricate benefit rules |
| Generate reports | Financial/health calculations |

### The Rule

**Claude orchestrates. Your apps calculate.**

For complex operations (RMD calculations, plan cost projections, commission splits), the business logic lives in your apps. Claude calls those apps via MCP and presents the results.

```
User: "What's the optimal plan for this client?"

Claude: "I'll check that for you."
        → Calls prodash-mcp: get_client_profile(id)
        → Calls ehr-mcp: get_claims_history(id, years=3)
        → Calls plan-calculator-mcp: compare_plans(claims, zip)
        → Receives calculated results
        → Explains findings to user

The calculation happened in plan-calculator-mcp, not in Claude.
```

---

## Part 6: Strategic Roadmap

### Phase 1: Foundation (Current)

**Building the data layer and core applications**

| Component | Status | Owner |
|-----------|--------|-------|
| MATRIX (Google Sheets) | ✅ Active | Data foundation |
| RAPID_API | ✅ Active | Data access layer |
| PRODASH | 🔄 Building | Client/account management |
| Reference MCPs (NPI, ICD-10, CMS) | ✅ Built | Healthcare data access |
| RPI-Standards documentation | ✅ Active | Agent guidance |

**Deliverable**: Apps work via UI, reference MCPs work in Cursor.

---

### Phase 2: Data MCPs (Next)

**Direct data access for development**

| Component | Priority | Purpose |
|-----------|----------|---------|
| Google Sheets MCP | High | Direct MATRIX queries |
| Google Drive MCP | Medium | Document search/read |
| Gmail MCP | Low | Email context |
| Calendar MCP | Low | Scheduling context |

**Deliverable**: Developers can query raw data via Claude during development.

---

### Phase 3: Application MCPs (Future)

**Expose apps as MCP tools**

| App | Becomes MCP | Tools Exposed |
|-----|-------------|---------------|
| PRODASH | `prodash-mcp` | `get_client`, `get_accounts`, `calculate_rmd` |
| CAM | `cam-mcp` | `get_commissions`, `calculate_split`, `project_revenue` |
| DAVID-HUB | `david-mcp` | `get_agents`, `recruiting_pipeline`, `production_report` |
| C³ | `c3-mcp` | `get_campaigns`, `content_library`, `schedule_content` |

**Deliverable**: Claude can use your business logic, not just raw data.

---

### Phase 4: Team AI Interfaces (Vision)

**Role-based AI assistants**

```
┌─────────────────────────────────────────────────────────────┐
│                    TEAM AI INTERFACES                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SALES AI          SERVICE AI        BD AI                  │
│  ├─ PRODASH        ├─ PRODASH        ├─ DAVID-HUB          │
│  ├─ Client data    ├─ RMD Center     ├─ Agent data         │
│  ├─ NPI Registry   ├─ EHR data       ├─ Carrier data       │
│  └─ Plan data      ├─ Plan data      └─ Recruiting         │
│                    └─ Service forms                         │
│                                                              │
│  MARKETING AI      COMPLIANCE AI     EXECUTIVE AI          │
│  ├─ C³ Content     ├─ All data       ├─ Everything         │
│  ├─ Campaigns      ├─ Audit logs     ├─ Dashboards         │
│  ├─ GHL data       ├─ CMS rules      ├─ Analytics          │
│  └─ Analytics      └─ Documentation  └─ Forecasts          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Deliverable**: Each team has an AI assistant optimized for their workflows.

---

## Part 7: Where Your Project Fits

### For App Development Projects (PRODASH, CAM, DAVID-HUB, etc.)

**You are building Layer 3 (Business Logic).**

Your app will eventually become an MCP server. Build with this in mind:

| Do This | Why |
|---------|-----|
| Keep functions modular | Easier to expose as MCP tools |
| Return structured data | MCP needs JSON-friendly responses |
| Document your functions | MCP tool descriptions come from this |
| Think about what Claude would call | "What questions would someone ask?" |

**Example**: If you build `calculateRMD(accountId)` in PRODASH, that same function becomes the `calculate_rmd` MCP tool later.

---

### For MCP Server Projects

**You are building Layer 2 (Connections).**

| Type | Your Job |
|------|----------|
| Raw Data MCP | Create simple query tools for a data source |
| Reference MCP | Wrap an external API with helpful tools |
| Application MCP | Expose an existing app's functions as tools |

**Follow the pattern in** `RPI-MCP-Servers/`:
- Each server is a standalone Node.js file
- Tools are defined with clear descriptions
- Input/output is JSON
- Errors are handled gracefully

---

### For All Agents

**Understand the big picture:**

1. Apps contain business logic (your expertise coded)
2. MCPs make that logic accessible to AI
3. Claude orchestrates across multiple MCPs
4. Team interfaces scope access appropriately

**Your work compounds.** Every function you write well today becomes a capability Claude can use tomorrow.

---

## Part 8: Technical Reference

### MCP Server Location

```
~/Projects/RPI-MCP-Servers/
├── package.json
├── setup.sh              ← Run this after cloning
├── README.md
└── src/servers/
    ├── npi-registry.js   ← Healthcare provider lookups
    ├── icd10-codes.js    ← Diagnosis/procedure codes
    └── cms-coverage.js   ← Medicare coverage info
```

### Setup (One-Time Per Machine)

```bash
cd ~/Projects
git clone https://github.com/retirementprotectors/RPI-MCP-Servers.git
cd RPI-MCP-Servers
npm install
./setup.sh
# Restart Cursor
```

### Available Tools (Current)

| Tool | MCP Server | Use When... |
|------|------------|-------------|
| `lookup_npi` | npi-registry | Verify a provider NPI |
| `search_providers` | npi-registry | Find providers by name/location |
| `validate_npi` | npi-registry | Check NPI format |
| `search_diagnosis_codes` | icd10-codes | Find ICD-10-CM codes |
| `search_procedure_codes` | icd10-codes | Find ICD-10-PCS codes |
| `lookup_code` | icd10-codes | Get code description |
| `validate_code` | icd10-codes | Check if code exists |
| `explain_medicare_parts` | cms-coverage | Medicare coverage questions |
| `check_dme_coverage` | cms-coverage | DME coverage info |
| `check_preventive_coverage` | cms-coverage | Preventive services |
| `find_mac_jurisdiction` | cms-coverage | Find MAC for a state |

---

## Part 9: The Vision Query

When fully built, this becomes possible:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  You: "Dr. Skir is retiring. His replacement is Dr.         │
│        Johnston. Pull all our active clients with Dr. Skir  │
│        as PCP, confirm Dr. Johnston is in-network for       │
│        their plans, and run a cost comparison of their      │
│        current plan vs optimal based on 3 years of claims." │
│                                                              │
│  AI:                                                         │
│                                                              │
│  Found 23 clients affected.                                  │
│                                                              │
│  URGENT (7 clients) - Must change plans:                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Client       │ Current Plan │ Recommended │ Savings │    │
│  │ Johnson, Mary│ Humana HMO   │ Aetna PPO   │ $1,530  │    │
│  │ Davis, Sue   │ Wellcare     │ UHC MAPD    │ $890    │    │
│  │ ...                                                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  NO ACTION REQUIRED (16 clients) - Dr. Johnston in-network │
│                                                              │
│  Total optimization opportunity: $18,420/year               │
│                                                              │
│  [Download Report] [Create Tasks] [Schedule Calls]          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**This query touches:**
- NPI Registry (provider lookup)
- RPI Business MCP (client data)
- CMS Plans MCP (network checks)
- EHR/Blue Button MCP (claims history)
- Plan Calculator MCP (cost projections)

**And returns an actionable answer in seconds.**

---

## Part 10: Key Principles

### 1. Build Once, Access Two Ways

Every app should work via UI (for humans) AND be exposable via MCP (for AI).

### 2. Logic in Apps, Not Claude

Complex calculations belong in your apps. Claude orchestrates and explains.

### 3. Your Expertise is the Moat

Anyone can connect to public APIs. Your business logic, coded into apps, is what makes this system uniquely valuable.

### 4. Compound Knowledge

Every function you write, every app you build, every MCP you create adds capability to the entire system.

### 5. Role-Based Access

Not everyone needs everything. Team interfaces scope access appropriately.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - standard for AI tool access |
| **MCP Server** | A program that exposes tools/data to AI |
| **MATRIX** | RPI's core Google Sheets data store |
| **RAPID_API** | GAS layer for accessing MATRIX |
| **Tool** | A specific function an MCP server exposes |
| **Layer** | One of the four architectural levels |

---

## Appendix B: Related Documents

| Document | Purpose |
|----------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Agent roles and patterns |
| `+0- MCP_TOOLS_SETUP.md` | MCP server setup guide |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI design system |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | Starting new projects |

---

## Appendix C: Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.2 | Jan 13, 2026 | Added The Mission - #RunningOurOwnRACE |
| v1.1 | Jan 13, 2026 | Added Strategic Context section - platform vs weapon, competitive moat |
| v1.0 | Jan 13, 2026 | Initial strategic roadmap |

---

*This document defines where we're going. Every project contributes to this vision.*
