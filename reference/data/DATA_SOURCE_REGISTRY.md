# RPI Data Source Registry

> Formal inventory of all external data sources, their integration status, and ingestion paths.
>
> **Maintained by:** Claude Code GA
> **Last updated:** 2026-02-16

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

| Carrier | Client Data | Account Data | Commission | New Biz / Pending | Reactive Service |
|---------|-------------|--------------|------------|-------------------|------------------|
| **Humana** | SPARK webhook (Auto) | SPARK webhook (Auto) | Stateable API (Auto) | SPARK webhook (Auto) | Portal (Manual) |
| **UHC/AARP** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal CSV (Semi-auto) | Portal (Manual) |
| **Aetna** | FHIR API (Auto) | FHIR API (Auto) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **Cigna** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **Wellcare/Centene** | Portal CSV (Semi-auto) | Portal CSV (Semi-auto) | Stateable API (Auto) | Portal CSV (Semi-auto) | Portal (Manual) |
| **Anthem BCBS** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **Mutual of Omaha** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **CoF** | XLSX (Manual) | XLSX (Manual) | Stateable API (Auto) | N/A | N/A |
| **ALIC** | Not Started | Not Started | Stateable API (Auto) | Not Started | Not Started |
| **North American** | Partner API (Planned) | Partner API (Planned) | Stateable API (Auto) | Partner API (Planned) | Portal (Manual) |
| **Midland** | Partner API (Planned) | Partner API (Planned) | Stateable API (Auto) | Partner API (Planned) | Portal (Manual) |
| **Allianz** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **American Equity** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |
| **Athene** | Portal (Manual) | Portal (Manual) | Stateable API (Auto) | Portal (Manual) | Portal (Manual) |

> **Note:** This cascade table is the "single-glance" view. See `CARRIER_INTEGRATION_MATRIX.md` for the full per-carrier detail including API endpoints, field mappings, authentication methods, and onboarding steps.

**Status key:**
- **Auto** = Fully automated, no human intervention required
- **Semi-auto** = Human triggers the process (e.g., downloads CSV), then automation handles the rest
- **Manual** = Requires human effort throughout
- **Planned** = Integration path identified, not yet built
- **Not Started** = No integration path identified or prioritized yet

**Pattern for new carriers:** See `IMPORT_BoBImport.gs` header and `CLAUDE.md` -- BoB Import/Enrichment Workflow.

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

**Notes:**
- Signal is being replaced by Gradient for life/annuity distribution
- SPARK remains the primary Medicare IMO (via Integrity)
- All IMO commission data flows through Stateable as the single aggregator

---

## 3. BD/RIA Custodians

| Custodian | Relationship | Current Integration | API Available | Status |
|-----------|-------------|---------------------|---------------|--------|
| Schwab | RIA custodian (via Gradient) | None | OpenView Gateway (370+ integrations) | Planned - HIGH priority |
| RBC | BD custodian (via Gradient) | None | In development (form-based currently) | Planned - MEDIUM |
| DST Vision | Data aggregator (mutual fund/VA) | None | FanMail/Vision feeds | Planned - MEDIUM |
| DTCC | Life/Annuity data feeds | None | I&RS REST API + webhooks (launched Dec 2024) | Planned - HIGH priority |

**Notes:**
- Schwab OpenView Gateway is the highest-priority custodian integration (daily position/transaction feeds)
- DTCC I&RS provides real-time life/annuity policy data independent of carrier portals
- RBC integration is dependent on Gradient onboarding completion
- DST Vision enrollment will happen through Gradient's existing relationship

---

## 4. Commission Aggregators

| Source | Coverage | Frequency | Method | Module | Status |
|--------|----------|-----------|--------|--------|--------|
| Stateable API | All IMOs (SPARK, Signal, Gradient) | Weekly | REST API pull | `IMPORT_Revenue.gs` | Automated |
| Carrier commission sheets (via IMOs) | Gap fill for Stateable gaps | Monthly | CSV to FIX_ function | `IMPORT_BoBImport.gs` | Semi-auto |
| SPARK portal exports | Medicare (backup) | Monthly | Manual download | `IMPORT_BoBImport.gs` | Manual |
| SMS portal exports | MedSupp (backup) | Monthly | Manual download | `IMPORT_BoBImport.gs` | Manual |

**Notes:**
- Stateable is THE single feed for all commission data -- SPARK, Signal, and Gradient all flow through it
- Carrier commission sheets are only needed to fill gaps where Stateable has incomplete data
- Portal exports are backup/verification only

---

## 5. Communication Channels

| Channel | Provider | Direction | Method | Module | Status |
|---------|----------|-----------|--------|--------|--------|
| SMS/Voice | Twilio | In/Out | REST API (hourly sync) | `IMPORT_Comms.gs` | Automated |
| Email (outbound) | SendGrid | Outbound | REST API (hourly sync) | `IMPORT_Comms.gs` | Automated |
| Video Meetings | Google Meet | Outbound | Calendar API (hourly sync) | `IMPORT_Comms.gs` | Automated |
| Chat | Google Chat | In/Out | Chat API v1 (hourly sync) | `IMPORT_Comms.gs` | **NEW - Sprint 2** |
| Call Recordings | Jira (archived) | Inbound | Drive scan to FIX_ import | `IMPORT_Comms.gs` | **NEW - Sprint 2** |
| Call/SMS (legacy) | GHL/Lead Connector | In/Out | CSV export to FIX_ import | `IMPORT_Comms.gs` | **NEW - Sprint 2** |

**Notes:**
- Google Chat integration uses Chat API v1 for hourly message sync into MATRIX
- Jira recording archive is a one-time migration of historical call recordings stored in Drive
- GHL/Lead Connector legacy comms import captures historical call recordings and SMS threads from before RPI's migration off GoHighLevel

---

## 6. Healthcare Data

### 6a. Quoting Tools (MCP-Hub / QUE)

These are NOT data import sources -- they power real-time quoting and lookup within QUE-Medicare and PRODASHX.

| Tool | Provider | Method | MCP Server | Status |
|------|----------|--------|------------|--------|
| Medicare Plan Finder | CMS | Cloud Run API | rpi-healthcare | Automated |
| NPI Registry | CMS NPPES | MCP API | claude.ai NPI Registry | Automated |
| ICD-10 Codes (2026) | CMS | MCP API | claude.ai ICD-10 Codes | Automated |
| Coverage Database | CMS | MCP API | claude.ai CMS Coverage | Automated |
| Humana Agent Portal | Humana | MCP API | rpi-healthcare | Automated |
| Aetna FHIR | Aetna | MCP API | rpi-healthcare | Automated |

### 6b. Actual Data Imports

These bring data INTO the MATRIX.

| Source | Data Type | Method | Module | Status |
|--------|-----------|--------|--------|--------|
| Blue Button (CMS via ID.me) | Original Medicare A&B claims/EOBs | FHIR OAuth per-client | `IMPORT_BlueButton.gs` | Planned - Sprint 3 |
| IRS Data Feed (via ID.me) | Tax data for RMD calculations | OAuth per-client | -- | Planned - LOW |
| EHR Integrations | Provider clinical data | TBD | -- | Planned - LOW |
| Aetna FHIR Patient Data | Claims + coverage for Aetna members | FHIR OAuth | `IMPORT_Comms.gs` (via rpi-healthcare MCP) | Partial |

**Notes:**
- Blue Button requires per-client ID.me authorization -- cannot be bulk-imported
- IRS data feed is LOW priority until RMD service center is fully operational
- EHR integrations are exploratory and depend on provider partnerships

---

## 7. Agent/Producer Data

| Source | Format | Frequency | Method | Module | Status |
|--------|--------|-----------|--------|--------|--------|
| NIPR (state licensing) | API | On-demand | `importAgentViaAPI()` | `IMPORT_Agent.gs` | Automated |
| LC3 Discovery (carrier appointments) | API | On-demand | `importAgentsViaAPI()` | `IMPORT_Agent.gs` | Automated |
| NPI Registry (healthcare provider IDs) | MCP API | On-demand | MCP tools | MCP-Hub (rpi-healthcare) | Automated |
| Gradient (appointments/contracting) | API | Planned | `syncGradientProducerStatus()` | `IMPORT_Gradient.gs` | Planned - Sprint 3 |

**Notes:**
- NIPR and LC3 Discovery are the primary sources for agent licensing and appointment data
- Gradient producer sync will replace Signal's portal-based appointment tracking
- NPI lookups are used for healthcare provider identification in Medicare workflows

---

## 8. Validation Services

| Source | Format | Frequency | Method | Module | Status |
|--------|--------|-----------|--------|--------|--------|
| PhoneValidator.com | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated |
| NeverBounce (email validation) | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated |
| USPS Address Validation v3 | API | Quarterly (Oct AEP mega sweep) | `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated |
| WhitePages Pro (identity) | API | Planned | -- | -- | Not Started |

**Notes:**
- Pipeline validation runs every 4 hours on newly imported records
- Quarterly hygiene check re-validates the entire client base
- October AEP mega sweep is critical for address validation before Annual Enrollment Period mailings
- WhitePages Pro will add identity verification (age, household composition) for compliance

---

## 9. Document Intake Sources

| Source | Format | Frequency | Method | Module | Status |
|--------|--------|-----------|--------|--------|--------|
| SPC Specialist Folders (Drive) | PDF/IMG | Continuous (5-min scan) | `scanIntakeFolders()` to queue to watcher | `IMPORT_Intake.gs` | Automated |
| Google Meet Transcripts | Google Doc | Continuous (5-min scan) | `scanMeetingRecordings()` to queue to watcher | `IMPORT_Intake.gs` | Automated |
| Physical Mail (scanned) | PDF/IMG | Continuous (5-min scan) | `scanMailFolder()` to queue to watcher | `IMPORT_Intake.gs` | Automated |
| Email Inboxes (Gmail) | Email/Attachments | Continuous (5-min scan) | `scanEmailInboxes()` to queue to watcher | `IMPORT_Intake.gs` | Automated |

---

## 10. Internal Systems

| Source | Format | Frequency | Method | Module | Status |
|--------|--------|-----------|--------|--------|--------|
| RAPID_CORE normalizers | Library | Every write | Auto-applied on insert/update | `CORE_Normalize.gs` | Automated |
| RAPID_CORE reconciliation | Library | Weekly (Mon 6 AM) | `reconcileClients()` / `reconcileAccounts()` | `CORE_Reconcile.gs` | Automated |
| Drive Hygiene (md5 dedup) | Drive API | Weekly (Wed 6 AM) | `runDriveHygieneScan()` | `IMPORT_DriveHygiene.gs` | Automated |
| MCP Analytics push | Node.js script | Daily 11 PM | `scripts.run` to `pushAnalyticsData()` | MCP-Hub analytics | Automated |

---

## CRM Data (GoHighLevel - Legacy)

> GHL import/sync code is RETAINED for M&A onboarding of GHL-based acquisitions via DAVID/SENTINEL. RPI no longer pushes TO GHL.

| Source | Format | Frequency | Method | Module | Status |
|--------|--------|-----------|--------|--------|--------|
| GHL Contacts | API (REST) | On-demand sync | `syncGHLContacts()` to RAPID_API | `IMPORT_GHL.gs` | Automated |
| GHL Custom Objects (Annuities) | API (REST) | On-demand sync | `syncGHLCustomObjects()` to RAPID_API | `IMPORT_GHL.gs` | Automated |
| GHL Custom Objects (Life) | API (REST) | On-demand sync | `syncGHLCustomObjects()` to RAPID_API | `IMPORT_GHL.gs` | Automated |
| GHL Contact Export (bulk) | CSV | One-time | Python to inline JS to FIX_ function | `IMPORT_BoBEnrich_Archive.gs` | Manual |

---

## Automation Priority Matrix

| Priority | Source | Current State | Automation Path | Sprint |
|----------|--------|---------------|-----------------|--------|
| **CRITICAL** | DTCC I&RS API | Not started | REST API + webhooks for life/annuity | Sprint 3 |
| **CRITICAL** | Schwab Advisor Services | Not started | OpenView Gateway daily feeds | Sprint 3 |
| **HIGH** | Google Chat integration | Not started | Chat API v1 hourly sync | Sprint 2 |
| **HIGH** | Jira recording archive | Not started | Drive scan to FIX_ import | Sprint 2 |
| **HIGH** | GHL legacy comms | Not started | CSV export to FIX_ import | Sprint 2 |
| **HIGH** | Humana/UHC/Aetna monthly BoB | Semi-auto (CSV download) | Carrier API or SFTP | Future |
| **MEDIUM** | Gradient IMO onboarding | Not started | Luma API integration | Sprint 3 |
| **MEDIUM** | Blue Button (CMS) | Not started | FHIR OAuth per-client | Sprint 3 |
| **MEDIUM** | Cigna/Wellcare BoB | Not started | Follow `FIX_ImportBoBData()` pattern | Future |
| **MEDIUM** | CoF inforce reports | Manual | Annual frequency = lower ROI | As needed |
| **MEDIUM** | WhitePages Pro | Not started | Add to RAPID_CORE validation suite | Future |
| **LOW** | RBC API | Not started | Awaiting API launch | Future |
| **LOW** | DST Vision | Not started | Enrollment via Gradient | Future |
| **LOW** | IRS data feed | Not started | ID.me integration | Future |
| **LOW** | EHR partnerships | Not started | Provider-specific | Future |

---

## Adding a New Data Source

0. **Check `CARRIER_INTEGRATION_MATRIX.md`** for existing documentation on this source
1. **Identify category** from the sections above
2. **Document in this registry** (source, format, frequency, method, module, status)
3. **Choose ingestion path** (follow the Method Priority Cascade):
   - API available at priority 1-3 --> Add to appropriate RAPID_IMPORT module
   - CSV/XLSX at priority 4-5 --> Write Python converter + GAS FIX_ function (see CLAUDE.md -- BoB Import Workflow)
   - Document --> Route through intake channels (SPC/Mail/Email)
4. **Add RAPID_CORE normalizers** if new field types are introduced
5. **Update TAB_SCHEMAS** in RAPID_CORE if new columns are needed
6. **Run reconciliation** after first import to catch duplicates

---

*This document is the single source of truth for RPI's data landscape. See `CARRIER_INTEGRATION_MATRIX.md` for per-carrier details. Update whenever a new source is onboarded.*
