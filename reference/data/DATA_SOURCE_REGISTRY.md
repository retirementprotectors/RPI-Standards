# RPI Data Source Registry

> Formal inventory of all external data sources, their integration status, and ingestion paths.
>
> **Maintained by:** Claude Code GA
> **Last updated:** 2026-03-03

---

## How to Read This Document

| Column | Meaning |
|--------|---------|
| **Source** | Where the data comes from |
| **Format** | File type or API format |
| **Frequency** | How often we receive/pull data |
| **Method** | How it enters the MATRIX |
| **Module** | Which GAS file or MCP handles this source |
| **Status** | Automated / Semi-auto / Manual / Planned / Not Started |

### Method Priority Cascade

When evaluating or planning integrations, prefer higher methods over lower ones. This is the order of preference for data ingestion:

| Priority | Method | Example |
|----------|--------|---------|
| 1 (best) | Real-time API | DTCC I&RS, Aetna FHIR, Schwab OpenView |
| 2 | Webhook push | SPARK webhooks to RAPID_API |
| 3 | Scheduled API pull | Stateable weekly commission pull |
| 4 | SFTP / bulk file transfer | Carrier monthly BoB feeds |
| 5 | Manual portal download + FIX_ function | UHC CSV export, Humana SMM |
| 6 (worst) | Paper / fax / phone | Legacy carrier communications |

Always push integrations UP the cascade when carrier capabilities allow it.

---

## 1. Insurance Carriers (Per-Carrier Integration Cascade)

This is the single-glance view of every carrier's integration status across all 5 data types. Each cell shows `[Method] ([Status])`.

### Medicare Carriers

| Carrier | Client Data | Account Data | Commission | New Biz / Pending | Reactive Service |
|---------|-------------|--------------|------------|-------------------|------------------|
| **Humana** | SPARK webhook (Auto) | SPARK webhook (Auto) | Stateable API (Auto) | SPARK webhook (Auto) | Portal (Manual) |
| **UHC/AARP** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal CSV (Semi-auto) | Portal (Manual) |
| **Aetna** | FHIR API (Auto) | FHIR API (Auto) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **Cigna** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **Wellcare/Centene** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal CSV (Semi-auto) | Portal (Manual) |
| **Anthem BCBS** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **Mutual of Omaha** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **Wellmark** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **Medico (Wellable)** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |

### Life/Annuity Carriers

| Carrier | Client Data | Account Data | Commission | New Biz / Pending | Reactive Service |
|---------|-------------|--------------|------------|-------------------|------------------|
| **CoF** | XLSX (Manual) | XLSX (Manual) | Stateable API (Auto) | N/A | N/A |
| **ALIC** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **North American** | Partner API (Planned) | Partner API (Planned) | Stateable API (Auto) | Partner API (Planned) | Portal (Manual) |
| **Midland** | Partner API (Planned) | Partner API (Planned) | Stateable API (Auto) | Partner API (Planned) | Portal (Manual) |
| **Allianz** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **American Equity** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **Athene** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |

### MATRIX Write Targets

| Data Type | Target Tab | MATRIX |
|-----------|------------|--------|
| Client demographics | `_CLIENT_MASTER` | PRODASH_MATRIX |
| Medicare accounts | `_ACCOUNT_MEDICARE` | PRODASH_MATRIX |
| Life accounts | `_ACCOUNT_LIFE` | PRODASH_MATRIX |
| Annuity accounts | `_ACCOUNT_ANNUITY` | PRODASH_MATRIX |
| BD/RIA accounts | `_ACCOUNT_BDRIA` | PRODASH_MATRIX |
| Banking accounts | `_ACCOUNT_BANKING` | PRODASH_MATRIX |
| Commission/Revenue | `_REVENUE_MASTER` | SENTINEL_MATRIX |
| Carrier reference | `_CARRIER_MASTER` | RAPID_MATRIX |

**Status key:**
- **Auto** = Fully automated, no human intervention required
- **Semi-auto** = Human triggers the process (e.g., downloads CSV), then automation handles the rest
- **Manual** = Requires human effort throughout
- **Planned** = Integration path identified, not yet built
- **Not Started** = No integration path identified or prioritized yet

**Pattern for new carriers:** See `IMPORT_BoBImport.gs` header and `RAPID_IMPORT/CLAUDE.md` -- BoB Import/Enrichment Workflow.

> **Per-carrier detail** (API endpoints, field mappings, auth methods, onboarding steps): See `CARRIER_INTEGRATION_MATRIX.md`.

---

## 2. IMO Partners

| IMO | Products | Current Integration | API Available | Status |
|-----|----------|---------------------|---------------|--------|
| SPARK (Integrity) | Medicare | Webhook to RAPID_API | Yes (REST + webhooks) | Active - Primary |
| Signal | Life/Annuity | Portal exports | Hexure/FireLight SSO | Transitioning out |
| Gradient | Life/Annuity + BD/RIA | Planned | Luma Financial partnerships | Incoming - onboarding |
| SMS (Senior Market Sales) | Medicare supplements | Portal exports | No | Active |
| PSMI | Commission | Portal exports | No | Active |
| AmeriLife | Commission | Portal exports | No | Active |

### Integration Details

| IMO | Integration Method | Module | MATRIX Target | Frequency |
|-----|-------------------|--------|---------------|-----------|
| SPARK | Webhook push to RAPID_API (`SPARK_LAST_WEBHOOK`) | `API_GHL_Sync.gs` (RAPID_API) | `_CLIENT_MASTER`, `_ACCOUNT_MEDICARE` | Real-time on event |
| Signal | Manual portal export + FIX_ function | `IMPORT_BoBImport.gs` | STB tab routes per product type | As needed |
| Gradient | Planned API sync | `IMPORT_Gradient.gs` (planned) | `_PRODUCER_MASTER`, `_ACCOUNT_LIFE`, `_ACCOUNT_ANNUITY`, `_ACCOUNT_BDRIA` | Planned - Sprint 3 |

**Notes:**
- Signal is being replaced by Gradient for life/annuity distribution
- SPARK remains the primary Medicare IMO (via Integrity)
- All IMO commission data flows through Stateable as the single aggregator
- STB (Stateable) tab in BoB import routes per product type: MAPD/MA/Medicare -> `_ACCOUNT_MEDICARE`, Annuity/FIA/MYGA -> `_ACCOUNT_ANNUITY`, Life/IUL/Term -> `_ACCOUNT_LIFE`

---

## 3. BD/RIA Custodians

| Custodian | Relationship | Current Integration | API Available | MATRIX Target | Status |
|-----------|-------------|---------------------|---------------|---------------|--------|
| Schwab | RIA custodian (via Gradient) | None | OpenView Gateway (370+ integrations) | `_ACCOUNT_BDRIA` | Planned - HIGH priority |
| RBC | BD custodian (via Gradient) | None | In development (form-based currently) | `_ACCOUNT_BDRIA` | Planned - MEDIUM |
| DST Vision | Data aggregator (mutual fund/VA) | None | FanMail/Vision feeds | `_ACCOUNT_BDRIA` | Planned - MEDIUM |
| DTCC | Life/Annuity data feeds | None | I&RS REST API + webhooks (launched Dec 2024) | `_ACCOUNT_LIFE`, `_ACCOUNT_ANNUITY` | Planned - HIGH priority |

**Notes:**
- Schwab OpenView Gateway is the highest-priority custodian integration (daily position/transaction feeds)
- DTCC I&RS provides real-time life/annuity policy data independent of carrier portals
- RBC integration is dependent on Gradient onboarding completion
- DST Vision enrollment will happen through Gradient's existing relationship

---

## 4. Commission Aggregators

| Source | Coverage | Frequency | Method | Module | MATRIX Target | Status |
|--------|----------|-----------|--------|--------|---------------|--------|
| Stateable API | All IMOs (SPARK, Signal, Gradient) | Weekly | REST API pull (POST with `x-api-key` auth) | `IMPORT_Revenue.gs` | `_REVENUE_MASTER` | Automated |
| Carrier commission sheets (via IMOs) | Gap fill for Stateable gaps | Monthly | CSV to FIX_ function | `IMPORT_BoBImport.gs` | `_REVENUE_MASTER` | Semi-auto |
| SPARK portal exports | Medicare (backup) | Monthly | Manual download + FIX_ function | `IMPORT_BoBImport.gs` | `_ACCOUNT_MEDICARE` | Manual |
| SMS portal exports | MedSupp (backup) | Monthly | Manual download | `IMPORT_BoBImport.gs` | `_ACCOUNT_MEDICARE` | Manual |

### Stateable API Details

| Attribute | Value |
|-----------|-------|
| Auth | `x-api-key` header (stored in Script Properties: `STATEABLE_API_KEY`) |
| Endpoint | `STATEABLE_URL` (Script Property) |
| Method | POST with JSON payload |
| Dedup Key | `stateable_id` field prevents duplicate imports |
| Revenue Types | FYC (first year), REN (renewal), OVR (override) |
| Pagination | `next_page_token` in payload |
| Module | `IMPORT_Revenue.gs` -- `fetchStateableCommissions()`, `mapStateableToRevenue()` |

**Notes:**
- Stateable is THE single feed for all commission data -- SPARK, Signal, and Gradient all flow through it
- Carrier commission sheets are only needed to fill gaps where Stateable has incomplete data
- Portal exports are backup/verification only

---

## 5. Communication Channels

| Channel | Provider | Direction | Method | Module | MATRIX Target | Status |
|---------|----------|-----------|--------|--------|---------------|--------|
| SMS/Voice | Twilio | In/Out | REST API (hourly sync) | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | Automated |
| Email (outbound) | SendGrid | Outbound | REST API (hourly sync) | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | Automated |
| Video Meetings | Google Meet | Outbound | Calendar API (hourly sync) | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | Automated |
| Chat | Google Chat | In/Out | Chat API v1 (hourly sync) | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | Automated |
| Call Recordings | Jira (archived) | Inbound | Drive scan to FIX_ import | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | One-time |
| Call/SMS (legacy) | GHL/Lead Connector | In/Out | CSV export to FIX_ import | `IMPORT_Comms.gs` | `_COMMUNICATION_LOG` | One-time |

### Twilio Integration Details

| Attribute | Value |
|-----------|-------|
| Auth | Basic Auth (`TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` in Script Properties) |
| SMS Endpoint | `https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json` |
| Calls Endpoint | `https://api.twilio.com/2010-04-01/Accounts/{SID}/Calls.json` |
| Lookback | 24 hours per sync |
| Max Records | 200 per sync |
| Dedup Key | `twilio_sid` (prevents duplicate imports) |

### SendGrid Integration Details

| Attribute | Value |
|-----------|-------|
| Auth | API Key (`SENDGRID_API_KEY` in Script Properties) |
| Lookback | 24 hours per sync |
| Max Records | 200 per sync |

### Google Chat Integration Details

| Attribute | Value |
|-----------|-------|
| Config | `CHAT_MONITORED_SPACES` Script Property (comma-separated space resource names) |
| Lookback | 24 hours per sync |
| Behavior | If `CHAT_MONITORED_SPACES` empty, syncs all accessible spaces |

**Notes:**
- Jira recording archive is a one-time migration of historical call recordings stored in Drive (`JIRA_RECORDINGS_FOLDER_ID`)
- GHL/Lead Connector legacy comms import captures historical data from before RPI's migration off GoHighLevel (`GHL_COMM_EXPORT_FILE_ID`)
- All comms writes route through RAPID_API via `callRapidAPIComms_()` -- no direct sheet writes

---

## 6. Healthcare Data

### 6a. Quoting Tools (MCP-Hub / QUE)

These are NOT data import sources -- they power real-time quoting and lookup within QUE-Medicare and PRODASHX.

| Tool | Provider | Method | MCP Server | Status |
|------|----------|--------|------------|--------|
| Medicare Plan Finder | CMS | Cloud Run API (`que-api-r6j33zf47q-uc.a.run.app`) | rpi-healthcare | Automated |
| NPI Registry | CMS NPPES | MCP API | claude.ai NPI Registry + rpi-healthcare | Automated |
| ICD-10 Codes (2026) | CMS | MCP API | claude.ai ICD-10 Codes + rpi-healthcare | Automated |
| Coverage Database (NCD/LCD) | CMS | MCP API | claude.ai CMS Coverage | Automated |
| Humana Agent Portal | Humana | FHIR API (sandbox + production) | rpi-healthcare | Automated |
| Aetna FHIR | Aetna | FHIR API | rpi-healthcare | Automated |
| Provider Directory (8 carriers) | Multiple | FHIR Provider Directory API | rpi-healthcare (`provider-network-tools.js`) | Automated |
| Formulary/Drug Coverage | CMS | Cloud Run API | rpi-healthcare | Automated |
| Pharmacy Network | CMS | Cloud Run API | rpi-healthcare | Automated |

### 6b. Actual Data Imports

These bring data INTO the MATRIX.

| Source | Data Type | Method | Module | MATRIX Target | Status |
|--------|-----------|--------|--------|---------------|--------|
| Blue Button (CMS via ID.me) | Original Medicare A&B claims/EOBs | FHIR OAuth per-client | `IMPORT_BlueButton.gs` (planned) | `_CLIENT_MASTER` | Planned - Sprint 3 |
| IRS Data Feed (via ID.me) | Tax data for RMD calculations | OAuth per-client | -- | -- | Planned - LOW |
| EHR Integrations | Provider clinical data | TBD | -- | -- | Planned - LOW |
| Aetna FHIR Patient Data | Claims + coverage for Aetna members | FHIR OAuth | rpi-healthcare MCP (`aetna-fhir-tools.js`) | `_CLIENT_MASTER` | Partial |
| Humana FHIR Patient Data | Claims + coverage for Humana members | FHIR OAuth | rpi-healthcare MCP (`humana-fhir-tools.js`) | `_CLIENT_MASTER` | Partial |

**Notes:**
- Blue Button requires per-client ID.me authorization -- cannot be bulk-imported
- IRS data feed is LOW priority until RMD service center is fully operational
- EHR integrations are exploratory and depend on provider partnerships
- Aetna/Humana patient data requires member OAuth consent flow (`get_patient_auth_url` -> `exchange_patient_code` -> `fetch_patient_data`)

---

## 7. Agent/Producer Data

| Source | Format | Frequency | Method | Module | MATRIX Target | Status |
|--------|--------|-----------|--------|--------|---------------|--------|
| NIPR (state licensing) | API | On-demand | `importAgentViaAPI()` + `parseNIPRData()` | `IMPORT_Agent.gs` | `_AGENT_MASTER` (SENTINEL) | Automated |
| LC3 Discovery (carrier appointments) | API | On-demand | `importAgentsViaAPI()` + `parseLC3DiscoveryData()` | `IMPORT_Agent.gs` | `_AGENT_MASTER` (SENTINEL) | Automated |
| NPI Registry (healthcare provider IDs) | MCP API | On-demand | MCP tools | MCP-Hub (rpi-healthcare) | Lookup only (no write) | Automated |
| Gradient (appointments/contracting) | API | Planned | `syncGradientProducerStatus()` | `IMPORT_Gradient.gs` (planned) | `_PRODUCER_MASTER` (SENTINEL) | Planned - Sprint 3 |

**Notes:**
- NIPR and LC3 Discovery are the primary sources for agent licensing and appointment data
- Gradient producer sync will replace Signal's portal-based appointment tracking
- NPI lookups are used for healthcare provider identification in Medicare workflows
- Agent import creates LC3 Drive folders automatically (`createAgentFolder()`)

---

## 8. Validation Services

| Source | Format | Frequency | Method | Module | MATRIX Target | Status |
|--------|--------|-----------|--------|--------|---------------|--------|
| PhoneValidator.com | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Writes back to `_CLIENT_MASTER` | Automated |
| NeverBounce (email validation) | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Writes back to `_CLIENT_MASTER` | Automated |
| USPS Address Validation v3 | API | Quarterly (Oct AEP mega sweep) | `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Writes back to `_CLIENT_MASTER` | Automated |
| WhitePages Pro (identity) | API | On-demand | rpi-business MCP (`whitepages-tools.js`) | MCP-Hub | Lookup only (no write) | Active |

### Validation Schedule

| Lane | Trigger | Frequency | Scope | Function |
|------|---------|-----------|-------|----------|
| Lane 1: Sentinel | On-demand | Per M&A evaluation | Batch scoring for due diligence | `generatePrePurchaseReport()` |
| Lane 2: Pipeline | Every 4 hours | Recently imported records (5hr lookback) | Phone + email validation | `pipelineValidationSweep()` |
| Lane 3: Quarterly | Jan/Apr/Jul/Oct 1st, 5 AM CT | All active/prospect clients | Phone + email (+ USPS address in October AEP sweep) | `quarterlyHygieneCheck()` |

### Chunked Execution

- 40 records per GAS execution (respects 6-minute limit)
- Trigger-chained with 60s delay via `hygieneChunkContinuation()`
- Progress stored in Script Properties (`HYGIENE_PROGRESS`), resumable on error

**Notes:**
- Pipeline validation runs every 4 hours on newly imported records
- Quarterly hygiene check re-validates the entire client base
- October AEP mega sweep is critical for address validation before Annual Enrollment Period mailings
- WhitePages Pro adds identity verification (age, household composition) for compliance and enrichment

---

## 9. Document Intake Sources

| Source | Format | Frequency | Method | Module | MATRIX Target | Status |
|--------|--------|-----------|--------|--------|---------------|--------|
| SPC Specialist Folders (Drive) | PDF/IMG | Continuous (5-min scan) | `scanIntakeFolders()` -> queue -> watcher | `IMPORT_Intake.gs` | `_INTAKE_QUEUE` -> `_APPROVAL_QUEUE` | Automated |
| Google Meet Transcripts | Google Doc | Continuous (5-min scan) | `scanMeetingRecordings()` -> queue -> watcher | `IMPORT_Intake.gs` | `_INTAKE_QUEUE` -> `_APPROVAL_QUEUE` | Automated |
| Physical Mail (scanned) | PDF/IMG | Continuous (5-min scan) | `scanMailFolder()` -> queue -> watcher | `IMPORT_Intake.gs` | `_INTAKE_QUEUE` -> `_APPROVAL_QUEUE` | Automated |
| Email Inboxes (Gmail) | Email/Attachments | Continuous (5-min scan) | `scanEmailInboxes()` -> queue -> watcher | `IMPORT_Intake.gs` | `_INTAKE_QUEUE` -> `_APPROVAL_QUEUE` | Automated |

### Intake Pipeline Flow

```
Source -> _INTAKE_QUEUE (PRODASH) -> MCP-Hub watcher (Claude Vision) -> _APPROVAL_QUEUE (RAPID)
  -> Slack notification -> Human review (Push/Edit/Kill) -> RAPID_API writes to target MATRIX
```

### Intake Folder Structure

```
SPC_INTAKE/ (1NczjcEifjXuc2uMBN70lHE_ZbtmeFOaU)
  [Specialist Name]/
    (intake documents)
    MEET_RECORDINGS/ (transcripts)

MAIL_INTAKE/ (1LV32r7w1k98B0S_zfJoavzpLQgsAB1Dg)
  Incoming/    <- Drop scanned mail here
  Processed/   <- System moves after processing
  Errors/      <- Couldn't process
```

---

## 10. Internal Systems

| Source | Format | Frequency | Method | Module | MATRIX Target | Status |
|--------|--------|-----------|--------|--------|---------------|--------|
| RAPID_CORE normalizers | Library | Every write | Auto-applied on `insertRow()`/`updateRow()` | `CORE_Database.gs` (90+ fields, 10 normalizer types) | All MATRIX tabs | Automated |
| RAPID_CORE reconciliation | Library | Weekly (Mon 6 AM) | `reconcileClients()` / `reconcileAccounts()` | `CORE_Reconcile.gs` | `_RECONCILIATION_LOG` (RAPID) | Automated |
| Drive Hygiene (md5 dedup) | Drive API | Weekly (Wed 6 AM) | `runDriveHygieneScan()` | `IMPORT_DriveHygiene.gs` | Dashboard card (no MATRIX write) | Automated |
| MCP Analytics push | Node.js script | Daily 3:30 AM | `scripts.run` to `pushAnalyticsData()` | MCP-Hub `unified-report.js` | `_AI_ANALYTICS` (RAPID) | Automated |
| Integration Health Monitor | GAS trigger | Every 30 min | `collectIntegrationStatuses()` | `IMPORT_IntegrationStatus.gs` | `_INTEGRATION_STATUS` (RAPID) | Automated |

### Integration Health Monitor (13 Integrations Tracked)

| Integration ID | Name | Trigger Type | Schedule |
|----------------|------|-------------|----------|
| `twilio_comms` | Twilio SMS/Calls | event | On send/receive |
| `sendgrid_email` | SendGrid Email | event | On send/receive |
| `google_chat` | Google Chat | hourly | Every hour |
| `google_meet` | Google Meet | hourly | Every hour |
| `spark_webhook` | SPARK Webhook | webhook | On event |
| `intake_pipeline` | Intake Pipeline | every_5min | Every 5 min |
| `pipeline_validation` | Pipeline Validation | every_4hr | Every 4 hours |
| `quarterly_hygiene` | Quarterly Hygiene | quarterly | Jan/Apr/Jul/Oct |
| `reconciliation` | Reconciliation | weekly | Mon 6 AM ET |
| `drive_hygiene` | Drive Hygiene | weekly | Wed 6 AM ET |
| `mcp_watcher` | MCP Watcher | every_5min | Every 5 min |
| `analytics_push` | Analytics Push | daily | Daily 3:30 AM |
| `ghl_sync` | GHL Sync | daily | Daily |

---

## CRM Data (GoHighLevel - Legacy)

> GHL import/sync code is RETAINED for M&A onboarding of GHL-based acquisitions via DAVID/SENTINEL. RPI no longer pushes TO GHL.

| Source | Format | Frequency | Method | Module | MATRIX Target | Status |
|--------|--------|-----------|--------|--------|---------------|--------|
| GHL Contacts | API (REST) | On-demand sync | `syncGHLContacts()` to RAPID_API | `IMPORT_GHL.gs` (4,394 lines) | `_CLIENT_MASTER` | Retained for M&A |
| GHL Custom Objects (Annuities) | API (REST) | On-demand sync | `syncGHLCustomObjects()` to RAPID_API | `IMPORT_GHL.gs` | `_ACCOUNT_ANNUITY` | Retained for M&A |
| GHL Custom Objects (Life) | API (REST) | On-demand sync | `syncGHLCustomObjects()` to RAPID_API | `IMPORT_GHL.gs` | `_ACCOUNT_LIFE` | Retained for M&A |
| GHL Contact Export (bulk) | CSV | One-time | Python to inline JS to FIX_ function | `IMPORT_BoBEnrich_Archive.gs` | `_CLIENT_MASTER` | Completed (Feb 2026) |

---

## MATRIX Tab Routing Reference

Complete TABLE_ROUTING from `RAPID_CORE/CORE_Database.gs`:

### PRODASH_MATRIX (B2C)

| Tab | Purpose |
|-----|---------|
| `_CLIENT_MASTER` | Client demographics |
| `_ACCOUNT_ANNUITY` | Annuity policies |
| `_ACCOUNT_LIFE` | Life insurance policies |
| `_ACCOUNT_MEDICARE` | Medicare plans |
| `_ACCOUNT_BDRIA` | BD/RIA investment accounts |
| `_ACCOUNT_BANKING` | Banking accounts |
| `_ACCOUNT_MASTER` | Unified account index |
| `_INTAKE_QUEUE` | Document intake pipeline |
| `_PIPELINES` | Sales pipeline stages |
| `_OPPORTUNITIES` | Sales opportunities |
| `_RELATIONSHIPS` | Client relationships |
| `_ACTIVITY_LOG` | Activity tracking |
| `_PERMISSIONS` | User permissions |
| `_CASE_TASKS` | Case task management |
| `_CONTENT_BLOCKS` | Campaign content blocks |
| `_TEMPLATES` | Campaign templates |
| `_CAMPAIGNS` | Campaign definitions |
| `_BOB_CONFIG` | Book of Business config |
| `_BOB_CAMPAIGNS` | BoB campaign assignments |
| `_CAMPAIGN_LOG` | Campaign execution log |
| `_CAMPAIGN_SEND_LOG` | Individual send records |

### SENTINEL_MATRIX (B2B)

| Tab | Purpose |
|-----|---------|
| `_AGENT_MASTER` | Agent/producer records |
| `_PRODUCER_MASTER` | Producer hierarchy |
| `_SENTINEL_PIPELINES` | M&A pipeline stages |
| `_SENTINEL_OPPORTUNITIES` | Deal opportunities |
| `_DEAL_MASTER` | Deal records |
| `_REVENUE_MASTER` | Commission/revenue data |

### RAPID_MATRIX (B2E Shared)

| Tab | Purpose |
|-----|---------|
| `_CARRIER_MASTER` | Carrier reference data |
| `_PRODUCT_MASTER` | Product catalog |
| `_IMO_MASTER` | IMO relationships |
| `_ACCOUNT_TYPE_MASTER` | Account type definitions |
| `_TRANSACTION_MASTER` | Transaction records |
| `_MAPD_COMP_GRID` | MAPD compensation grid |
| `_LIFE_COMP_GRID` | Life compensation grid |
| `_ANNUITY_COMP_GRID` | Annuity compensation grid |
| `_MEDSUP_COMP_GRID` | MedSupp compensation grid |
| `_CMS_PLANS_2026` | CMS plan data |
| `_SPECIALIST_FOLDERS` | Specialist Drive folder config |
| `_DOCUMENT_TAXONOMY` | Document classification taxonomy |
| `_TAXONOMY_SUGGESTIONS` | Auto-logged unknown doc types |
| `_EXTRACTION_TRAINING` | AI extraction training data |
| `_RECONCILIATION_LOG` | Dedup/merge audit trail |
| `_AI_ANALYTICS` | AI usage analytics |
| `_USER_HIERARCHY` | User org hierarchy |
| `_COMPANY_STRUCTURE` | Company org structure |
| `_PIPELINE_CONFIG` | Pipeline configuration |
| `_CONTACTS_CARRIERS` | Carrier contact records |
| `_CONTACTS_IMOS` | IMO contact records |
| `_CONTACTS_INTERNAL` | Internal contact records |
| `_COMMUNICATION_LOG` | Unified communication history |
| `_INTEGRATION_STATUS` | Integration health monitoring |

---

## Automation Priority Matrix

| Priority | Source | Current State | Automation Path | Sprint |
|----------|--------|---------------|-----------------|--------|
| **CRITICAL** | DTCC I&RS API | Not started | REST API + webhooks for life/annuity | Sprint 3 |
| **CRITICAL** | Schwab Advisor Services | Not started | OpenView Gateway daily feeds | Sprint 3 |
| **HIGH** | Humana/UHC/Aetna monthly BoB | Semi-auto (CSV download) | Carrier API or SFTP | Future |
| **MEDIUM** | Gradient IMO onboarding | Not started | Luma API integration | Sprint 3 |
| **MEDIUM** | Blue Button (CMS) | Not started | FHIR OAuth per-client | Sprint 3 |
| **MEDIUM** | Cigna/Wellcare BoB | Not started | Follow `FIX_ImportBoBData()` pattern | Future |
| **MEDIUM** | CoF inforce reports | Manual | Annual frequency = lower ROI | As needed |
| **LOW** | RBC API | Not started | Awaiting API launch | Future |
| **LOW** | DST Vision | Not started | Enrollment via Gradient | Future |
| **LOW** | IRS data feed | Not started | ID.me integration | Future |
| **LOW** | EHR partnerships | Not started | Provider-specific | Future |

---

## Adding a New Data Source

0. **Check `CARRIER_INTEGRATION_MATRIX.md`** for existing documentation on this source
1. **Identify category** from the sections above
2. **Document in this registry** (source, format, frequency, method, module, target, status)
3. **Choose ingestion path** (follow the Method Priority Cascade):
   - API available at priority 1-3 -> Add to appropriate RAPID_IMPORT module
   - CSV/XLSX at priority 4-5 -> Write Python converter + GAS FIX_ function (see RAPID_IMPORT/CLAUDE.md -- BoB Import Workflow)
   - Document -> Route through intake channels (SPC/Mail/Email)
4. **Add RAPID_CORE normalizers** if new field types are introduced
5. **Update TAB_SCHEMAS** in RAPID_CORE if new columns are needed
6. **Add to `INTEGRATIONS` array** in `IMPORT_IntegrationStatus.gs` for health monitoring
7. **Run reconciliation** after first import to catch duplicates

---

*This document is the single source of truth for RPI's data landscape. See `CARRIER_INTEGRATION_MATRIX.md` for per-carrier details. Update whenever a new source is onboarded.*
