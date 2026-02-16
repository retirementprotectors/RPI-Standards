# RPI Carrier Integration Matrix

> Detailed per-carrier integration reference. For the single-glance cascade table, see `DATA_SOURCE_REGISTRY.md`.
>
> **Maintained by:** Claude Code GA
> **Last updated:** 2026-02-16

---

## How to Use This Document

Each carrier section contains:
- **Overview**: Products, relationship, IMO intermediary
- **Current Integration**: What we have today
- **Available APIs**: What the carrier/aggregator offers
- **Data Types**: What data we can get, by which method
- **Field Mapping**: Key external field → MATRIX field mappings
- **Setup Requirements**: What JDM needs to do to enable
- **RAPID_IMPORT Module**: Which file handles this carrier

---

## Medicare Carriers

### Humana

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, D-SNP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Portal** | vantage.humana.com |
| **Current Status** | Automated (SPARK webhook) |

**Current Integration:**
- SPARK webhook pushes contact/enrollment data → `API_Spark.gs` → MATRIX
- SMM (Summary of Medicare Members) CSV import → `FIX_ImportHumanaSMM()` in `IMPORT_BoBImport.gs`
- Commission via Stateable API

**Available APIs (via rpi-healthcare MCP):**
- `humana_get_agent` — agent lookup
- `humana_get_medicare_plans` — plan details
- `humana_get_medsup_plans` / `humana_get_medsup_quotes` — MedSupp quoting
- `humana_search_beneficiary_eligibility` — eligibility check
- `humana_submit_medicare_enrollment` — enrollment submission
- `humana_get_enrollment_status` — enrollment tracking
- `humana_calculate_idv_rate` — IDV rate calculation
- `humana_check_dsnp_eligibility` — D-SNP eligibility

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Client demographics | SPARK webhook | Automated |
| Account/enrollment | SPARK webhook | Automated |
| Commission | Stateable API | Automated |
| New business/pending | SPARK webhook | Automated |
| Service/claims | Portal (manual) | Manual |

**Module:** `API_Spark.gs` (webhook handler), `IMPORT_BoBImport.gs` (SMM bulk import)

---

### UHC/AARP

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Portal** | uhcagent.com |
| **Current Status** | Semi-automated (CSV + SPARK) |

**Current Integration:**
- SPARK webhook for some data
- LWD format CSV download from portal → `FIX_ImportBoBData()` in `IMPORT_BoBImport.gs`
- Commission via Stateable API

**Available APIs:**
- No public API for BoB data
- SPARK webhook covers some enrollment events

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Client demographics | Portal CSV / SPARK | Semi-auto |
| Account/enrollment | Portal CSV / SPARK | Semi-auto |
| Commission | Stateable API | Automated |
| New business/pending | Portal CSV | Semi-auto |
| Service/claims | Portal (manual) | Manual |

**Setup Requirements:**
- Portal credentials already configured
- Monthly CSV download (could be automated via Playwright if high-value)

**Module:** `IMPORT_BoBImport.gs`

---

### Aetna

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Portal** | aetna.com |
| **Current Status** | Partially automated (FHIR API + CSV) |

**Current Integration:**
- CSV import via `FIX_ImportBoBData()` in `IMPORT_BoBImport.gs`
- FHIR API available via rpi-healthcare MCP (partially integrated)
- Commission via Stateable API

**Available APIs (via rpi-healthcare MCP):**
- `aetna_search_practitioners` — provider search
- `aetna_search_insurance_plans` — plan search
- `aetna_search_organizations` — organization search
- `aetna_get_provider_by_npi` — NPI lookup
- `aetna_fetch_patient_data` — FHIR patient data (requires patient OAuth)
- `aetna_build_prior_auth_bundle` — prior authorization
- `aetna_submit_prior_auth` — submit prior auth
- `aetna_inquire_prior_auth` — check prior auth status

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Client demographics | FHIR API / CSV | Semi-auto |
| Account/enrollment | FHIR API / CSV | Semi-auto |
| Commission | Stateable API | Automated |
| New business/pending | Portal (manual) | Manual |
| Service/claims | FHIR API (patient auth required) | Partial |

**Module:** `IMPORT_BoBImport.gs`, rpi-healthcare MCP

---

### Cigna

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP |
| **IMO** | SPARK (Integrity) |
| **Portal** | cigna.com |
| **Current Status** | Not Started |

**Current Integration:** None. Commission only via Stateable.

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Client demographics | Not Started | — |
| Account/enrollment | Not Started | — |
| Commission | Stateable API | Automated |
| New business/pending | Not Started | — |
| Service/claims | Not Started | — |

**Automation Path:** Follow `FIX_ImportBoBData()` pattern from existing carriers. Medium priority.

---

### Wellcare/Centene

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, D-SNP |
| **IMO** | SPARK (Integrity) |
| **Portal** | wellcare.com |
| **Current Status** | Not Started |

**Current Integration:** None. Commission only via Stateable.

**Automation Path:** Follow `FIX_ImportBoBData()` pattern. Medium priority.

---

### Anthem BCBS

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Portal** | anthem.com |
| **Current Status** | Not Started |

---

### Mutual of Omaha

| Attribute | Value |
|-----------|-------|
| **Products** | MedSupp, Final Expense |
| **IMO** | Direct / SPARK |
| **Portal** | mutualofomaha.com |
| **Current Status** | Not Started |

---

## Life Insurance Carriers

### Catholic Order of Foresters (CoF)

| Attribute | Value |
|-----------|-------|
| **Products** | Whole Life, Term Life |
| **IMO** | Direct (member organization) |
| **Portal** | N/A (manual correspondence) |
| **Current Status** | Manual (XLSX annual) |

**Current Integration:**
- Annual XLSX inforce report → Python converter → `FIX_EnrichLifeFromCarrier()` / `FIX_ReclassifyAnnuitiesFromCarrier()` in `IMPORT_BoBEnrich_Archive.gs`
- Member list CSV → `FIX_EnrichClientsFromCarrier()`
- Commission via Stateable API

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Client demographics | XLSX (annual) | Manual |
| Account/policy | XLSX (annual) | Manual |
| Commission | Stateable API | Automated |
| New business | N/A | — |
| Service | N/A | — |

**Phase 6 (CoF policy import):** BLOCKED on CoF response for additional data.

**Module:** `IMPORT_BoBEnrich_Archive.gs` (executed), `IMPORT_BoBEnrich.gs` (helpers)

---

### ALIC (American Life Insurance Company)

| Attribute | Value |
|-----------|-------|
| **Products** | Life |
| **IMO** | Signal → Gradient |
| **Portal** | TBD |
| **Current Status** | Not Started |

---

### North American (Sammons Financial)

| Attribute | Value |
|-----------|-------|
| **Products** | IUL, FIA, MYGA |
| **IMO** | Signal → Gradient |
| **Portal** | northamericancompany.com |
| **Current Status** | Not Started |

**Available APIs:** JDM confirms partner API access exists (private, not public). Requires Gradient relationship.

**JDM Action:** Confirm partner API access through Gradient, provide docs.

---

### Midland National (Sammons Financial)

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA, Life |
| **IMO** | Signal → Gradient |
| **Portal** | midlandnational.com |
| **Current Status** | Not Started |

**Available APIs:** Same as North American (sister company under Sammons Financial).

---

## Annuity Carriers

### Allianz

| Attribute | Value |
|-----------|-------|
| **Products** | FIA |
| **IMO** | Signal → Gradient |
| **Portal** | allianzlife.com |
| **Current Status** | Portal only |

**Available APIs:** Marketplace-only (no direct agent API found). Portal download + FIX_ function.

---

### American Equity

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA |
| **IMO** | Signal → Gradient |
| **Portal** | american-equity.com |
| **Current Status** | Portal only |

**Available APIs:** Portal-only. No public API.

---

### Athene

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA |
| **IMO** | Signal → Gradient |
| **Portal** | athene.com |
| **Current Status** | Portal only |

**Available APIs:** Marketplace-only (Apollo ecosystem). No direct agent API.

---

## BD/RIA Custodians

### Schwab (Charles Schwab Advisor Services)

| Attribute | Value |
|-----------|-------|
| **Products** | RIA custody (all securities) |
| **Relationship** | Via Gradient RIA |
| **Portal** | advisorservices.schwab.com |
| **Current Status** | Not Started |
| **Priority** | HIGH |

**Available APIs:**
- OpenView Gateway — daily account data feeds
- 370+ integrations, well-documented developer program
- OAuth-based authentication

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Account positions | OpenView API | Planned |
| Account balances | OpenView API | Planned |
| Transaction history | OpenView API | Planned |
| Client demographics | OpenView API | Planned |

**Setup Requirements:**
1. Enroll in Schwab Advisor Services developer program (through Gradient)
2. Obtain OAuth client credentials
3. Configure API access for RPI's Schwab accounts

**Planned Module:** `IMPORT_Schwab.gs` (Sprint 3)

---

### RBC (RBC Correspondent Services)

| Attribute | Value |
|-----------|-------|
| **Products** | BD custody |
| **Relationship** | Via Gradient BD |
| **Portal** | rbccm.com |
| **Current Status** | Not Started |
| **Priority** | MEDIUM |

**Available APIs:** API reportedly in development. Currently form-based data authorization.

**JDM Action:** Check API availability timeline through Gradient.

---

### DST Vision (SS&C Technologies)

| Attribute | Value |
|-----------|-------|
| **Products** | Mutual fund / VA data aggregation |
| **Relationship** | Via Gradient |
| **Portal** | dstvision.com |
| **Current Status** | Not Started |
| **Priority** | MEDIUM |

**Available APIs:** FanMail/Vision established feeds. Requires enrollment.

**JDM Action:** Enroll through Gradient BD relationship.

---

### DTCC I&RS (Insurance & Retirement Services)

| Attribute | Value |
|-----------|-------|
| **Products** | Life/Annuity data feeds |
| **Relationship** | Direct (industry utility) |
| **Portal** | dtcc.com |
| **Current Status** | Not Started |
| **Priority** | CRITICAL |

**Available APIs:**
- Full REST API launched December 2024
- Webhook support for real-time events
- Covers policy data, transactions, agent compensation across multiple carriers

**Data Types:**
| Type | Method | Status |
|------|--------|--------|
| Policy data (life/annuity) | REST API | Planned |
| Transactions | REST API | Planned |
| Agent compensation | REST API | Planned |
| Real-time events | Webhooks | Planned |

**Setup Requirements:**
1. DTCC I&RS enrollment (industry membership)
2. Obtain API credentials
3. Confirm which carriers are covered via DTCC feeds

**Planned Module:** `IMPORT_DTCC.gs` + `API_DTCC.gs` (Sprint 3)

---

## API Maturity Summary

| Source | API Type | Maturity | Priority |
|--------|----------|----------|----------|
| DTCC I&RS | REST + Webhooks | Production (Dec 2024) | CRITICAL |
| Schwab OpenView | REST (OAuth) | Mature (370+ integrations) | HIGH |
| Aetna FHIR | FHIR v4 | Production | MEDIUM (partially done) |
| Humana APIs | REST | Production (via rpi-healthcare MCP) | DONE |
| Signal (Hexure) | SSO/Embedded | Legacy | LOW (transitioning out) |
| Gradient (Luma) | TBD | New | MEDIUM |
| DST Vision | Feed-based | Established | MEDIUM |
| North American/Midland | Partner API | Private | MEDIUM |
| RBC | TBD | In development | LOW |
| American Equity/Athene | None | Portal only | LOW |

---

## Cross-Reference

| Document | Purpose |
|----------|---------|
| `DATA_SOURCE_REGISTRY.md` | Single-glance cascade table + all data sources |
| `CARRIER_INTEGRATION_TEMPLATE.md` | Template for adding new carriers |
| `RAPID_IMPORT/CLAUDE.md` | Technical implementation details |
| `RAPID_CORE/CORE_Database.gs` | TAB_SCHEMAS and TABLE_ROUTING |

---

*This document is updated when carrier integrations change. For the overall data landscape, see DATA_SOURCE_REGISTRY.md.*
