> **DEPRECATED (2026-03-19):** This document references pre-toMachina architecture (MATRIX tabs, GAS functions). Data governance is now managed by ATLAS in Firestore (`services/api/src/routes/atlas.ts`). Retained for historical reference only.

# RPI Carrier Integration Matrix

> Per-carrier reference cards with API endpoints, authentication methods, field mappings, and integration status.
>
> **Maintained by:** Claude Code GA
> **Last updated:** 2026-03-03
> **Companion doc:** `DATA_SOURCE_REGISTRY.md` (the "what") -- this doc is the "how"

---

## How to Read This Document

Each carrier has a **reference card** with:

| Section | Contents |
|---------|----------|
| **Overview** | Carrier name, products, IMO intermediary |
| **Portals** | Agent portal URLs (for manual operations) |
| **API Endpoints** | FHIR URLs, REST endpoints, auth methods -- sourced from codebase |
| **MCP Tools** | Available rpi-healthcare MCP tools for this carrier |
| **BoB Import Config** | Tab configuration from `IMPORT_BoBImport.gs` |
| **Status** | Live / Planned / Not Started per data type |

### IMO Transition Note

RPI is transitioning life/annuity distribution from **Signal** to **Gradient**. Where noted:
- **Signal** = current but being phased out
- **Gradient** = incoming, onboarding in progress
- **SPARK (Integrity)** = Medicare -- no change planned

---

## Medicare Carriers

---

### Humana

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, D-SNP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Automated (SPARK webhook + FHIR) |

#### Portals

| Portal | URL | Purpose |
|--------|-----|---------|
| Vantage | `vantage.humana.com` | BoB reports, member lookup |

#### API Endpoints (from `humana-fhir-tools.js`)

**Production:**

| Endpoint | URL |
|----------|-----|
| Base API | `https://api.humana.com` |
| FHIR API | `https://fhir.humana.com/api` |
| OAuth Token | `https://api.humana.com/oauth/token` |
| Patient Authorization | `https://fhir.humana.com/auth/authorize` |
| Patient Token Exchange | `https://fhir.humana.com/auth/token` |

**Sandbox:**

| Endpoint | URL |
|----------|-----|
| Base API | `https://qa-api.humana.com` |
| FHIR API | `https://sandbox-fhir.humana.com/api` |
| OAuth Token | `https://qa-api.humana.com/oauth/token` |
| Patient Authorization | `https://sandbox-fhir.humana.com/auth/authorize` |
| Patient Token Exchange | `https://sandbox-fhir.humana.com/auth/token` |

**Auth Method:** OAuth 2.0 (client credentials for agent API, authorization code for patient data)

#### Provider Directory FHIR (from `provider-network-tools.js`)

| Attribute | Value |
|-----------|-------|
| Base URL | `https://fhir.humana.com/api` |
| Auth | None (public per CMS mandate) |
| Resources | Practitioner, PractitionerRole, Organization, Location, InsurancePlan |

#### Available MCP Tools (rpi-healthcare)

| Tool | Purpose |
|------|---------|
| `humana_get_agent` / `humana_get_agent_plans` / `humana_get_agent_all_plans` | Agent details and plan access |
| `humana_get_agent_certifications` / `humana_get_agent_licenses` | Agent compliance |
| `humana_get_medicare_plans` | Plan search by ZIP/county |
| `humana_get_medsup_plans` / `humana_get_medsup_quotes` | MedSupp quoting with pricing |
| `humana_get_idv_plans` / `humana_calculate_idv_rate` | Individual plan rates |
| `humana_search_beneficiary_eligibility` | MBI lookup, LIS status, ESRD |
| `humana_check_dsnp_eligibility` | Dual Special Needs eligibility |
| `humana_submit_medicare_enrollment` / `humana_get_enrollment_status` | Enrollment submission + tracking |
| `humana_submit_pharmacy_consent` | Pharmacy consent for enrollment |
| `humana_save_drug_list` | Drug list for formulary comparison |
| `humana_get_patient_auth_url` / `humana_exchange_patient_code` | Member FHIR consent flow |
| `humana_fetch_patient_data` | Member clinical data (15 FHIR resource types) |
| `humana_get_bam_report` / `humana_get_aped_report` | Book of Business + Agent Production reports |
| `humana_get_osb_list` | Other Supplemental Benefits |
| `humana_get_api_status` / `humana_test_connection` | API health checks |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `Humana- BoB.JDM` | Humana | `_ACCOUNT_MEDICARE` | MbrFirstName, MbrLastName, Birth Date, Primary Phone, Email, Humana ID, Medicare No, Product Description, Effective Date, Addr1, City, State, Zip |

| Import Function | Source | Purpose |
|-----------------|--------|---------|
| `FIX_ImportHumanaSMM()` | Humana SMM LOA Payments sheet | Q1-2026 BoB batch import |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client demographics | SPARK webhook | **Live** (Auto) |
| Account/enrollment | SPARK webhook + Portal CSV | **Live** (Auto + Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |
| New business/pending | SPARK webhook | **Live** (Auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |
| Patient FHIR Data | OAuth consent flow | **Live** (requires member auth) |
| Enrollment API | Agent REST API (sandbox + production) | **Live** (Auto) |
| Beneficiary Eligibility | Agent REST API | **Live** (Auto) |
| Service/claims | Portal (manual) | **Manual** |

---

### UHC/AARP (United Healthcare)

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, DSNP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Semi-automated (CSV + SPARK) |

#### Portals

| Portal | URL | Purpose |
|--------|-----|---------|
| Agent Portal | `uhcagent.com` | BoB reports, member lookup |

#### API Endpoints (from `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| Provider Directory (Optum) | `https://sandbox-apigw.optum.com` | OAuth 2.0 client credentials |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `UHC BOB Sheet` | UHC | `_ACCOUNT_MEDICARE` | memberFirstName, memberLastName, dateOfBirth, memberPhone, product, planStatus, memberAddress/City/State/Zip (**NOTE: no policy number column**) |
| `UHC- LWD 1.1.23` | UHC | `_ACCOUNT_MEDICARE` | Member Name (LAST, FIRST format), Policy Number, MedicareID, Plan Type, Original Effective Date, Prem Amount, Member State |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client demographics | Portal CSV + FIX_ function | **Live** (Semi-auto) |
| Account/enrollment | Portal CSV + FIX_ function | **Live** (Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |
| New business/pending | Portal CSV | **Live** (Semi-auto) |
| Provider Directory | FHIR Provider Directory API (Optum) | **Live** (Auto) |
| Patient FHIR Data | Not available | **Not Started** |
| Service/claims | Portal (manual) | **Manual** |

**Automation Path:** Monthly CSV download could be automated via Playwright if high-value.

---

### Aetna

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP, DSNP, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Partially automated (FHIR API + CSV) |

#### Portals

| Portal | URL | Purpose |
|--------|-----|---------|
| Producer World | `aetna.com` | BoB reports, commissions |

#### API Endpoints (from `aetna-fhir-tools.js` and `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| FHIR Base (sandbox + production) | `https://apif1.aetna.com/fhir/v1` | OAuth 2.0 client credentials |
| OAuth Token | `https://apif1.aetna.com/fhir/v1/fhirserver_auth/oauth2/token` | Client credentials |
| Provider Directory | `https://apisb.aetna.com/fhir/v1/providerdirectory` | API key |

#### Available MCP Tools (rpi-healthcare)

| Tool | Purpose |
|------|---------|
| `aetna_search_practitioners` | Provider search (by NPI or name+ZIP) |
| `aetna_search_organizations` | Organization search (requires ZIP) |
| `aetna_get_provider_by_npi` | Provider lookup by NPI |
| `aetna_search_insurance_plans` | Plan search by ZIP |
| `aetna_submit_prior_auth` / `aetna_inquire_prior_auth` | Prior authorization (Da Vinci PAS) |
| `aetna_build_prior_auth_bundle` | FHIR bundle builder for prior auth |
| `aetna_get_patient_auth_url` / `aetna_exchange_patient_code` | Member FHIR consent flow |
| `aetna_fetch_patient_data` | Member clinical data (15 FHIR resource types) |
| `aetna_get_api_status` / `aetna_test_connection` | API health checks |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `AETNA JDM LOA- MFGAN + MFGA` | Aetna | `_ACCOUNT_MEDICARE` | First Name, Last Name, Date of Birth, Phone Number, Member ID, Plan Name, Effective Date, Address, City, State, Zip |
| `AETNA- MFG OVR` | Aetna | `_ACCOUNT_MEDICARE` | Same field set |
| `AETNA- MFGA STR + OVR` | Aetna | `_ACCOUNT_MEDICARE` | Same field set |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client demographics | FHIR API + Portal CSV | **Live** (Auto + Semi-auto) |
| Account/enrollment | FHIR API + Portal CSV | **Live** (Auto + Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |
| New business/pending | Portal CSV | **Live** (Semi-auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |
| Patient FHIR Data | OAuth consent flow | **Live** (requires member auth) |
| Prior Authorization | Da Vinci PAS FHIR | **Live** (Auto) |
| Service/claims | Portal (manual) | **Manual** |

---

### Cigna

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, PDP |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

#### API Endpoints (from `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| Provider Directory | `https://p-hi2.digitaledge.cigna.com/ProviderDirectory/v1` | None (public) |
| Resources | Practitioner, PractitionerRole, Organization, Location, InsurancePlan, HealthcareService |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | -- | **Not Started** |
| Commission | Stateable API | **Live** (Auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |

**Automation Path:** Follow `FIX_ImportBoBData()` pattern from existing carriers. Medium priority.

---

### Wellcare/Centene

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, D-SNP |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Semi-automated (CSV) |

#### API Endpoints (from `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| Provider Directory | `https://prod.api.centene.com/fhir/providerdirectory` | None (public) |
| Resources | Practitioner, PractitionerRole, Organization, Location, Network, InsurancePlan |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `Wellcare- BoB` | Wellcare | `_ACCOUNT_MEDICARE` | Member First Name, Member Last Name, Member DoB, Phone, Centene ID, MBI, Plan Name, Effective Date, Address, City, State, Zip |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal CSV + FIX_ function | **Live** (Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |

---

### Anthem BCBS (Elevance Health)

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD, MedSupp |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

#### API Endpoints (from `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| Provider Directory | `https://totalview.healthos.elevancehealth.com/fhir` | None (public) |
| Resources | Practitioner, PractitionerRole, Organization, Location |

**Note:** BCBS endpoints vary by affiliate. The Elevance Health endpoint covers Anthem-branded plans.

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | -- | **Not Started** |
| Commission | Stateable API | **Live** (Auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |

---

### Mutual of Omaha

| Attribute | Value |
|-----------|-------|
| **Products** | MedSupp, Final Expense, Medicare Advantage |
| **IMO** | Direct / SPARK |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | -- | **Not Started** |
| Commission | Stateable API | **Live** (Auto) |

---

### Wellmark

| Attribute | Value |
|-----------|-------|
| **Products** | Medicare Advantage (Iowa market) |
| **IMO** | Direct |
| **Commission Aggregator** | Stateable |
| **Current Status** | Semi-automated (CSV) |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `Wellmark- BoB` | Wellmark | `_ACCOUNT_MEDICARE` | Name (LAST, FIRST format), Date of Birth, Member Id, Plan Name, Status, Address, City, State, Zip |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal CSV + FIX_ function | **Live** (Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |

---

### Medico (via Wellable)

| Attribute | Value |
|-----------|-------|
| **Products** | MedSupp |
| **IMO** | Wellable |
| **Commission Aggregator** | Stateable |
| **Current Status** | Semi-automated (CSV) |

#### BoB Import Configuration (from `IMPORT_BoBImport.gs`)

| Tab Name | Default Carrier | Target Tab | Key Columns |
|----------|----------------|------------|-------------|
| `Wellable- BoB` | Medico | `_ACCOUNT_MEDICARE` | Insured (FIRST LAST format), Insured DOB, Policy Number, Plan Description, Premium, Status, Address, City, State, Zip |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal CSV + FIX_ function | **Live** (Semi-auto) |
| Commission | Stateable API | **Live** (Auto) |

---

### Devoted Health

| Attribute | Value |
|-----------|-------|
| **Products** | MAPD |
| **IMO** | SPARK (Integrity) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

#### API Endpoints (from `provider-network-tools.js`)

| Endpoint | URL | Auth |
|----------|-----|------|
| Provider Directory | `https://fhir.devoted.com/fhir` | None (public) |
| Resources | Practitioner, PractitionerRole, Organization, Location |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | -- | **Not Started** |
| Commission | Stateable API | **Live** (Auto) |
| Provider Directory | FHIR Provider Directory API | **Live** (Auto) |

---

## Life/Annuity Carriers

---

### Catholic Order of Foresters (CoF)

| Attribute | Value |
|-----------|-------|
| **Products** | Whole Life, Term Life |
| **IMO** | Direct (member organization) |
| **Commission Aggregator** | Stateable |
| **Current Status** | Manual (XLSX annual) |

#### Current Integration

- Annual XLSX inforce report -> Python converter -> `FIX_ImportCoFMembers()` in `IMPORT_BoBImport.gs`
- Historical enrichment via `FIX_EnrichLifeFromCarrier()` / `FIX_EnrichClientsFromCarrier()` in `IMPORT_BoBEnrich_Archive.gs` (executed Feb 2026)
- Commission via Stateable API

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client demographics | XLSX (annual request) | **Live** (Manual) |
| Account/policy | XLSX (annual request) | **Live** (Manual) |
| Commission | Stateable API | **Live** (Auto) |
| New business | N/A | -- |

**Phase 6 (CoF policy import):** BLOCKED on CoF response for additional data as of Feb 2026.

**Module:** `IMPORT_BoBImport.gs` (`FIX_ImportCoFMembers()`), `IMPORT_BoBEnrich_Archive.gs` (historical)

---

### ALIC (American Life Insurance Company)

| Attribute | Value |
|-----------|-------|
| **Products** | Life Insurance |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | -- | **Not Started** |
| Commission | Stateable API | **Live** (Auto) |

---

### North American (Sammons Financial)

| Attribute | Value |
|-----------|-------|
| **Products** | IUL, FIA, MYGA |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

**Available APIs:** Partner API access exists (private, requires Gradient relationship).

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Partner API (via Gradient) | **Planned** |
| Commission | Stateable API | **Live** (Auto) |
| New business | Partner API (via Gradient) | **Planned** |

---

### Midland National (Sammons Financial)

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA, Life |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Commission only |

**Available APIs:** Same as North American (sister company under Sammons Financial).

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Partner API (via Gradient) | **Planned** |
| Commission | Stateable API | **Live** (Auto) |
| New business | Partner API (via Gradient) | **Planned** |

---

### Allianz Life

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, Life |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Portal only |

**Available APIs:** Marketplace-only (no direct agent API). Portal download + FIX_ function is the path.

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal (manual) | **Live** (Manual) |
| Commission | Stateable API | **Live** (Auto) |

---

### American Equity

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Portal only |

**Available APIs:** Portal-only. No public API.

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal (manual) | **Live** (Manual) |
| Commission | Stateable API | **Live** (Auto) |

---

### Athene

| Attribute | Value |
|-----------|-------|
| **Products** | FIA, MYGA |
| **IMO** | Signal -> Gradient |
| **Commission Aggregator** | Stateable |
| **Current Status** | Portal only |

**Available APIs:** Marketplace-only (Apollo ecosystem). No direct agent API.

#### Integration Status

| Data Type | Method | Status |
|-----------|--------|--------|
| Client/Account Data | Portal (manual) | **Live** (Manual) |
| Commission | Stateable API | **Live** (Auto) |

---

## BD/RIA Custodians

---

### Schwab (Charles Schwab Advisor Services)

| Attribute | Value |
|-----------|-------|
| **Relationship** | RIA custodian (via Gradient RIA side) |
| **Account Types** | Managed accounts, mutual funds, ETFs |
| **MATRIX Target** | `_ACCOUNT_BDRIA` |
| **Priority** | **HIGH** |
| **Current Status** | Not Started |

#### Integration Path

| Feature | Method | Status |
|---------|--------|--------|
| Daily Position Feed | Schwab OpenView Gateway | **Planned** |
| Transaction Feed | Schwab OpenView Gateway | **Planned** |
| Account Opening | Schwab OpenView Gateway | **Planned** |
| Client Demographics | Schwab OpenView Gateway | **Planned** |

**OpenView Gateway:** 370+ integrations, OAuth-based authentication, well-documented developer program.

**Setup Requirements:**
1. Enroll in Schwab Advisor Services developer program (through Gradient)
2. Obtain OAuth client credentials
3. Configure API access for RPI's Schwab accounts

**Planned Module:** `IMPORT_Schwab.gs` (Sprint 3)

---

### RBC (RBC Correspondent Services)

| Attribute | Value |
|-----------|-------|
| **Relationship** | BD custodian (via Gradient BD side) |
| **Account Types** | Brokerage accounts, securities |
| **MATRIX Target** | `_ACCOUNT_BDRIA` |
| **Priority** | **MEDIUM** |
| **Current Status** | Not Started |

**Available APIs:** API reportedly in development. Currently form-based data authorization.

**Dependency:** Gradient BD onboarding must complete first.

---

## Data Aggregators

---

### DTCC I&RS (Insurance & Retirement Services)

| Attribute | Value |
|-----------|-------|
| **Service** | Life/Annuity data feeds (industry utility) |
| **Products** | Policy data, transactions, agent compensation across multiple carriers |
| **MATRIX Target** | `_ACCOUNT_LIFE`, `_ACCOUNT_ANNUITY` |
| **Priority** | **CRITICAL** |
| **Current Status** | Not Started |

#### Available APIs

| Feature | Method | Status |
|---------|--------|--------|
| Policy Data | REST API (launched Dec 2024) | **Planned** |
| Transactions | REST API | **Planned** |
| Agent Compensation | REST API | **Planned** |
| Real-time Events | Webhooks | **Planned** |

**Setup Requirements:**
1. DTCC I&RS enrollment (industry membership)
2. Obtain API credentials
3. Confirm which carriers are covered via DTCC feeds

**Planned Module:** `IMPORT_DTCC.gs` + `API_DTCC.gs` (Sprint 3)

---

### DST Vision (SS&C Technologies)

| Attribute | Value |
|-----------|-------|
| **Service** | Mutual fund / variable annuity data aggregation |
| **Relationship** | Via Gradient |
| **MATRIX Target** | `_ACCOUNT_BDRIA` |
| **Priority** | **MEDIUM** |
| **Current Status** | Not Started |

**Available APIs:** FanMail/Vision established feeds. Requires enrollment via Gradient.

---

## Carrier FHIR Provider Directory Summary

All Medicare Advantage plans are CMS-mandated to provide public FHIR Provider Directory APIs. Accessed via `provider-network-tools.js` in the rpi-healthcare MCP.

| Carrier | FHIR Base URL | Auth | Status |
|---------|--------------|------|--------|
| Humana | `https://fhir.humana.com/api` | None (public) | **Live** |
| Aetna | `https://apisb.aetna.com/fhir/v1/providerdirectory` | API key | **Live** |
| UHC/Optum | `https://sandbox-apigw.optum.com` | OAuth 2.0 | **Live** |
| Devoted | `https://fhir.devoted.com/fhir` | None (public) | **Live** |
| Anthem/Elevance | `https://totalview.healthos.elevancehealth.com/fhir` | None (public) | **Live** |
| Centene/Wellcare | `https://prod.api.centene.com/fhir/providerdirectory` | None (public) | **Live** |
| Cigna | `https://p-hi2.digitaledge.cigna.com/ProviderDirectory/v1` | None (public) | **Live** |
| BCBS | Varies by affiliate | Varies | **Varies** |

### FHIR Resources by Carrier

| Resource | Humana | Aetna | UHC | Devoted | Anthem | Centene | Cigna |
|----------|--------|-------|-----|---------|--------|---------|-------|
| Practitioner | Y | Y | Y | Y | Y | Y | Y |
| PractitionerRole | Y | Y | Y | Y | Y | Y | Y |
| Organization | Y | Y | Y | Y | Y | Y | Y |
| Location | Y | Y | Y | Y | Y | Y | Y |
| InsurancePlan | Y | Y | -- | -- | -- | Y | Y |
| HealthcareService | -- | -- | -- | -- | -- | -- | Y |
| OrgAffiliation | -- | Y | -- | -- | -- | -- | -- |

---

## STB (Stateable) Product Type Routing

The STB tab in `IMPORT_BoBImport.gs` routes records by product type keyword to the correct MATRIX tab:

| Product Type Keywords | Target Tab |
|-----------------------|------------|
| `mapd`, `ma`, `medicare advantage`, `medicare supplement`, `med supp`, `pdp`, `supplement`, `medicare` | `_ACCOUNT_MEDICARE` |
| `annuity`, `fia`, `myga` | `_ACCOUNT_ANNUITY` |
| `life`, `iul`, `term`, `whole life`, `ul` | `_ACCOUNT_LIFE` |

---

## API Maturity Summary

| Source | API Type | Maturity | RPI Priority |
|--------|----------|----------|--------------|
| DTCC I&RS | REST + Webhooks | Production (Dec 2024) | **CRITICAL** |
| Schwab OpenView | REST (OAuth) | Mature (370+ integrations) | **HIGH** |
| Humana Agent/FHIR | REST + FHIR v4 | Production | **DONE** (via rpi-healthcare MCP) |
| Aetna FHIR | FHIR v4 | Production | **DONE** (via rpi-healthcare MCP) |
| Gradient (Luma) | TBD | New | **MEDIUM** |
| DST Vision | Feed-based | Established | **MEDIUM** |
| North American/Midland | Partner API | Private | **MEDIUM** |
| Signal (Hexure) | SSO/Embedded | Legacy | **LOW** (transitioning out) |
| RBC | TBD | In development | **LOW** |
| American Equity/Athene | None | Portal only | **LOW** |

---

## Cross-Reference

| Document | Purpose |
|----------|---------|
| `DATA_SOURCE_REGISTRY.md` | Single-glance cascade table + all data sources |
| `CARRIER_INTEGRATION_TEMPLATE.md` | Template for adding new carriers |
| `RAPID_IMPORT/CLAUDE.md` | Technical implementation details |
| `RAPID_CORE/CORE_Database.gs` | TAB_SCHEMAS and TABLE_ROUTING |

---

## Adding a New Carrier

1. **Create reference card** in this document (copy an existing carrier section)
2. **Update `DATA_SOURCE_REGISTRY.md`** -- add row to the carrier cascade table (Section 1)
3. **Add BoB import config** to `IMPORT_BoBImport.gs` `BOB_TABS` array if CSV import is needed
4. **Check FHIR Provider Directory** -- CMS mandates public FHIR for all MA carriers
5. **Add carrier to `CARRIER_ENDPOINTS`** in `provider-network-tools.js` if FHIR endpoint is known
6. **Verify Stateable coverage** -- confirm commission data flows through Stateable
7. **Test with DryRun** -- always run `FIX_ImportBoBDataDryRun()` before live import

---

*This document is updated when carrier integrations change. For the overall data landscape, see `DATA_SOURCE_REGISTRY.md`.*
