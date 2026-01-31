# RPI Three-Platform Architecture

> **Version**: v1.0  
> **Created**: January 26, 2026  
> **Author**: Josh D. Millang + Claude  
> **Status**: MASTER ARCHITECTURE DOCUMENT  
> **Purpose**: Single source of truth for RPI's three-platform architecture

---

## Overview

RPI operates through **three channels**, each with a dedicated **platform UI** and **database**:

| Channel | Acronym | Full Name | Platform UI | Database | Focus |
|---------|---------|-----------|-------------|----------|-------|
| **B2C** | RPI | Retirement Protectors, Inc | **PRODASH** | PRODASH_MATRIX | Direct client sales + service |
| **B2B** | DAVID | Disruptive and Vertically Integrated Distribution | **SENTINEL** | SENTINEL_MATRIX | M&A + Partnerships |
| **B2E** | RAPID | The [API]s between [R]PI and [D]AVID | **RIIMO** | RAPID_MATRIX | Shared services operations |

**RIIMO** = Retirement Insurance and Insurance **Management Operations**

---

## Platform Architecture (Visual)

```
=======================================================================================
                          RPI STANDARDS (Cross-Suite)
=======================================================================================

┌────────────────────────────────────────────────────────────────────────────────────┐
│                     RPI COMMAND CENTER (Cross-Suite Tool)                           │
│            Internal/External Communications Hub + Leadership Visibility             │
└────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┬─────────────────────────┬─────────────────────────────────┐
│   SENTINEL (B2B/DAVID)  │    RIIMO (B2E/RAPID)    │      PRODASH (B2C/RPI)          │
│   Partner Focus         │    Operations Focus     │      Client Focus               │
├─────────────────────────┤                         ├─────────────────────────────────┤
│                         │                         │                                 │
│  MODULES    PIPELINES   │  MODULES    PIPELINES   │  MODULES    PIPELINES           │
│  ────────   ─────────   │  ────────   ─────────   │  ────────   ─────────           │
│                         │                         │                                 │
│  Producers  PROSPECTING │  C3         DATA MAINT  │  Clients    PROSPECTING         │
│             ─────────── │             ─────────── │             ───────────         │
│  C3         New Lead    │  TOMIS      Matrix Sync │  C3         New Lead            │
│  Campaigns  Engaged     │             Validation  │  Campaigns  Engaged             │
│             Coordinating│  Proposal   Cleanup     │             Coordinating        │
│  DAVID-HUB  HUB Init'd  │  Maker      Backup      │  QUE Suite  Scheduled           │
│   - MEC     ─────────── │             ─────────── │   - Medicare───────────         │
│   - PRP     SALES PROC  │  Contract   TECH MAINT  │   - Life    SALES PROCESS       │
│   - SPH     ─────────── │  Generator  ─────────── │   - Annuity ───────────         │
│             Report Req  │             Deploy      │             Discovery           │
│  Proposal   Analysis    │  LC3        Testing     │  Proposal   Analysis            │
│  Maker      Proposal    │             Monitoring  │  Maker      Proposal            │
│             NDA/LOI     │  RAPID      Hotfix      │             Authorization       │
│  Contract   Close       │  Import     ─────────── │  Contract   Close               │
│  Generator  ─────────── │             SECURITY    │  Generator  ───────────         │
│             TRANSITION  │  CAM        ─────────── │             NEWBIZ              │
│  LC3        ─────────── │             Access Ctrl │  LC3        ───────────         │
│  (Inventory) Docs Kit   │  MCP-Hub    Audit Log   │  (Maintain) Application         │
│             Tech Setup  │             Compliance  │             Underwriting        │
│  RAPID      Credentials │  MDJs       Backup/DR   │  RAPID      Issued              │
│  Import     Data Migr   │  Per Unit               │  Import     Placed              │
│             LIVE        │                         │             Active              │
│  CAM                    │                         │  CAM                            │
│  (M-A-P Splits)         │                         │  (Team Splits)                  │
│                         │                         │                                 │
│  MDJs Per Unit          │                         │  MDJs Per Unit                  │
│                         │                         │                                 │
├─────────────────────────┤                         ├─────────────────────────────────┤
│   SENTINEL_MATRIX       │     RAPID_MATRIX        │      PRODASH_MATRIX             │
│  (Producer/Agent Data)  │    (Reference Data)     │    (Client/Account Data)        │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────┘
```

---

## SuperProject Folder Structure

```
/Users/joshd.millang/Projects/
│
├── _RPI_STANDARDS/                       # Cross-suite standards (ROOT)
│
├── RAPID_TOOLS/                          # Shared Services (B2E)
│   ├── C3/                               # Content/Campaign Manager ✓
│   ├── CAM/                              # Commission Accounting ✓
│   ├── CEO-Dashboard/                    # Executive visibility ✓
│   ├── MCP-Hub/                          # Intelligence + Calculations ✓
│   ├── RAPID_API/                        # REST API layer ✓
│   ├── RAPID_CORE/                       # Shared GAS library ✓
│   ├── RAPID_IMPORT/                     # Data ingestion ✓
│   ├── RPI-Command-Center/               # Cross-suite communications ✓
│   ├── RIIMO/                            # Operations UI (TO BUILD)
│   ├── TOMIS/                            # Field Specialist App (TO BUILD)
│   ├── Proposal-Maker/                   # Analysis output (TO BUILD)
│   ├── Contract-Generator/               # DocuSign generation (TO BUILD)
│   ├── LC3/                              # Licensing/Contracting (TO BUILD)
│   └── MDJs/                             # AI Assistants (TO BUILD)
│
├── SENTINEL_TOOLS/                       # B2B Platform (DAVID)
│   ├── DAVID-HUB/                        # Entry point (calculators) ✓
│   ├── sentinel/                         # Main B2B app ✓
│   ├── SENTINEL_MATRIX/                  # Producer database (TO CREATE)
│   └── MDJs/                             # BD AI assistants (TO BUILD)
│
└── PRODASH_TOOLS/                        # B2C Platform (RPI)
    ├── PRODASH/                          # Main B2C app ✓
    ├── PRODASH_MATRIX/                   # Client database (TO CREATE)
    ├── QUE/                              # Quoting Suite
    │   ├── QUE-Medicare/                 # Medicare quoting ✓
    │   ├── QUE-Life/                     # Life quoting (TO BUILD)
    │   └── QUE-Annuity/                  # Annuity quoting (TO BUILD)
    └── MDJs/                             # Service/Sales AI (TO BUILD)
```

---

## Three MATRIXes

### RAPID_MATRIX (Shared Reference Data)

| Tab | Purpose |
|-----|---------|
| `_CARRIER_MASTER` | Canonical carrier registry |
| `_PRODUCT_MASTER` | Product type definitions |
| `_IMO_MASTER` | IMO/FMO registry |
| `_MAPD_COMP_GRID` | Medicare Advantage rates |
| `_LIFE_COMP_GRID` | Life insurance rates |
| `_ANNUITY_COMP_GRID` | Annuity rates |
| `_MEDSUP_COMP_GRID` | Medicare Supplement rates |
| `_ANC_COMP_GRID` | Ancillary product rates |
| `_CMS_PLANS` | CMS plan reference |
| `_CMS_FMV_RATES` | Fair Market Value rates |
| `_IMPORT_MAPPINGS` | Data ingestion configs |
| `_SYSTEM_CONFIG` | App configuration |
| `_ERROR_LOG` | System errors |

### SENTINEL_MATRIX (B2B Producer/Deal Data)

| Tab | Purpose |
|-----|---------|
| `_PRODUCER_MASTER` | B2B partners/agents |
| `Opportunities` | Deal tracking |
| `_DEAL_VALUATIONS` | M-A-P analysis results |
| `_PARTNER_TIERS` | Tier structure (DAVID) |
| `_PRODUCER_HIERARCHY` | Downline structure |
| `_PRODUCER_CREDENTIALS` | Licensing/Certifications |
| `_REVENUE_MASTER` | Commission tracking |
| `_COMMISSION_CYCLES` | Payout processing |
| `_COMMISSION_DETAILS` | Payout breakdown |
| `_STATEMENT_IMPORTS` | Carrier statements |
| `_RECONCILIATION_LOG` | Statement matching |
| `Tasks` | Deal/transition tasks |
| `ActivityLog` | Deal activity |
| `_ERROR_LOG` | System errors |

### PRODASH_MATRIX (B2C Client/Account Data)

| Tab | Purpose |
|-----|---------|
| `_CLIENT_MASTER` | B2C clients |
| `_ACCOUNT_MASTER` | Client accounts/policies |
| `Opportunities` | Sales opportunities |
| `_GHL_CONTACTS` | GHL sync cache |
| `_GHL_OPPORTUNITIES` | GHL pipeline sync |
| `_ACTIVITY_LOG` | Client activity |
| `_RMD_TRACKING` | Required Min Distributions |
| `_COMMISSION_SUMMARY` | Client revenue view |
| `_POLICY_RENEWALS` | Renewal tracking |
| `Tasks` | Service tasks |
| `_DOCUMENTS` | Document registry |
| `_NOTES` | Client notes |
| `_ERROR_LOG` | System errors |

---

## Pipeline Stages

### RIIMO Pipelines (Operations)

| Pipeline | Stages |
|----------|--------|
| **Data Maintenance** | Matrix Sync → Validation → Cleanup → Backup |
| **Tech Maintenance** | Deploy → Testing → Monitoring → Hotfix |
| **Security** | Access Control → Audit Log → Compliance → Backup/DR |

### SENTINEL Pipelines (B2B)

| Pipeline | Stages |
|----------|--------|
| **Prospecting** | New Lead → Engaged → Coordinating → HUB Initiated |
| **Sales Process** | Report Req'd → Analysis → Proposal → NDA/LOI → Close |
| **Transition** | Docs Kit → Tech Setup → Credentials → Data Migration → LIVE |

### PRODASH Pipelines (B2C)

| Pipeline | Stages |
|----------|--------|
| **Prospecting** | New Lead → Engaged → Coordinating → Scheduled |
| **Sales Process** | Discovery → Analysis → Proposal → Authorization → Close |
| **NewBiz** | Application → Underwriting → Issued → Placed → Active |

---

## Shared Services (RAPID_TOOLS)

These services are consumed by both SENTINEL and PRODASH:

| Service | SENTINEL (B2B) Use | PRODASH (B2C) Use |
|---------|-------------------|-------------------|
| **C3** | B2B campaign triggers | B2C campaign triggers |
| **TOMIS** | Field BD interactions | Field Sales/Service interactions |
| **Proposal Maker** | M-A-P analysis output | Client comparison output |
| **Contract Generator** | NDA/LOI/Partnership docs | Client agreements |
| **LC3** | Inventory existing data | Manage/maintain for team |
| **RAPID Import** | Partner data migration | Client data import |
| **CAM** | M-A-P Revenue Shares | Sales Team Revenue Shares |
| **MCP-Hub** | Commission intelligence | Plan intelligence |
| **MDJs** | BD unit assistants | Service/Sales unit assistants |

---

## Workflow Pattern

| Step | SENTINEL (B2B) | Shared (RAPID) | PRODASH (B2C) |
|------|----------------|----------------|---------------|
| 1 | Data In (Partner BoB) | | Data In (Client Info) |
| 2 | DAVID-HUB (MEC/PRP/SPH) | | QUE Suite (Medicare/Life/Annuity) |
| 3 | | MCP-Hub (Intelligence) | |
| 4 | | Proposal Maker (Output) | |
| 5 | Presentation → Close | | Presentation → Close |

---

## Cross-Matrix Relationships

- `carrier_id` in SENTINEL and PRODASH references `_CARRIER_MASTER` in RAPID
- `product_type` in both channels references `_PRODUCT_MASTER` in RAPID
- `producer_id` in SENTINEL links to `agent_id` in PRODASH for client assignments
- `stateable_id` links revenue tracking between B2B and B2C

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `RPI_PLATFORM_BLUEPRINT.md` | Five-layer architecture (Datasets → Experiences) |
| `AI_PLATFORM_STRATEGIC_ROADMAP.md` | MCP architecture and AI platform strategy |
| `MDJ_STRATEGIC_VISION.md` | AI assistant deployment per unit |
| `MASTER_AGENT_FRAMEWORK.md` | Development agent patterns |

---

## Implementation Roadmap

See the full implementation plan at:  
`/Users/joshd.millang/.cursor/plans/three-matrix_database_architecture_6ff65db7.plan.md`

**Phases**:
1. Foundation (folder structure)
2. Database Architecture (three MATRIXes)
3. RIIMO Platform
4. App Development
5. Pipeline Implementation
6. QUE Suite
7. MDJ Integration

---

*This document supersedes the single-MATRIX architecture in previous documents.*
