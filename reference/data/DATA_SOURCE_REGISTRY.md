# RPI Data Source Registry

> Formal inventory of all external data sources, their integration status, and ingestion paths.
>
> **Maintained by:** Claude Code GA
> **Last updated:** 2026-02-15

---

## How to Read This Document

| Column | Meaning |
|--------|---------|
| **Source** | Where the data comes from |
| **Format** | File type or API format |
| **Frequency** | How often we receive/pull data |
| **Ingestion Method** | How it enters the MATRIX |
| **RAPID_IMPORT Module** | Which GAS file handles this source |
| **Status** | Automated / Manual / Not Started |
| **Priority** | How important automation is (H/M/L) |

---

## 1. CRM Data (GoHighLevel)

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| GHL Contacts | API (REST) | On-demand sync | `syncGHLContacts()` → RAPID_API | `IMPORT_GHL.gs` | Automated | — |
| GHL Custom Objects (Annuities) | API (REST) | On-demand sync | `syncGHLCustomObjects()` → RAPID_API | `IMPORT_GHL.gs` | Automated | — |
| GHL Custom Objects (Life) | API (REST) | On-demand sync | `syncGHLCustomObjects()` → RAPID_API | `IMPORT_GHL.gs` | Automated | — |
| GHL Contact Export (bulk) | CSV | One-time | Python → inline JS → FIX_ function | `IMPORT_BoBEnrich_Archive.gs` | Manual | L |

---

## 2. Carrier Inforce Reports

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| Catholic Order of Foresters (CoF) — Life | XLSX | Annual/On-request | Python → inline JS → `FIX_EnrichLifeFromCarrier()` | `IMPORT_BoBEnrich_Archive.gs` | Manual | M |
| Catholic Order of Foresters (CoF) — Annuity | XLSX | Annual/On-request | Python → inline JS → `FIX_ReclassifyAnnuitiesFromCarrier()` | `IMPORT_BoBEnrich_Archive.gs` | Manual | M |
| CoF Member List (contacts) | CSV | Annual/On-request | Python → inline JS → `FIX_EnrichClientsFromCarrier()` | `IMPORT_BoBEnrich_Archive.gs` | Manual | M |
| Humana SMM (Medicare) | CSV | Monthly | `FIX_ImportHumanaSMM()` | `IMPORT_BoBImport.gs` | Semi-auto | H |
| UHC/AARP Medicare | CSV (LWD format) | Monthly | `FIX_ImportBoBData()` | `IMPORT_BoBImport.gs` | Semi-auto | H |
| Aetna Medicare | CSV | Monthly | `FIX_ImportBoBData()` | `IMPORT_BoBImport.gs` | Semi-auto | H |
| Cigna Medicare | CSV | Monthly | Planned | — | Not Started | M |
| Wellcare/Centene Medicare | CSV | Monthly | Planned | — | Not Started | M |
| ALIC (American Life) — Life | PDF/CSV | Quarterly | Planned | — | Not Started | M |

**Pattern for new carriers:** See `IMPORT_BoBImport.gs` header and `CLAUDE.md` § BoB Import/Enrichment Workflow.

---

## 3. Commission Data

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| Stateable API (aggregated) | API (REST) | Weekly | `importRevenueRecordsViaAPI()` | `IMPORT_Revenue.gs` | Automated | — |
| Carrier commission sheets (via IMOs) | CSV/XLSX | Monthly | Manual review → `FIX_ImportBoBData()` | `IMPORT_BoBImport.gs` | Semi-auto | H |
| SPARK portal exports | CSV | Monthly | Manual download → bulk import | `IMPORT_BoBImport.gs` | Manual | M |
| SMS portal exports | CSV | Monthly | Manual download → bulk import | `IMPORT_BoBImport.gs` | Manual | M |

---

## 4. Agent/Producer Data

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| NIPR (National Insurance Producer Registry) | API | On-demand | `importAgentViaAPI()` | `IMPORT_Agent.gs` | Automated | — |
| LC3 Discovery (carrier appointments) | API | On-demand | `importAgentsViaAPI()` | `IMPORT_Agent.gs` | Automated | — |
| NPI Registry (healthcare providers) | MCP API | On-demand | `npi_search` / `npi_lookup` | MCP-Hub (rpi-healthcare) | Automated | — |

---

## 5. Government & Regulatory Data

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| CMS NPI Registry | MCP API | Real-time | `npi_validate` / `npi_search` / `npi_lookup` | MCP (claude.ai NPI Registry) | Automated | — |
| CMS Coverage Database | MCP API | Real-time | `search_national_coverage` / `search_local_coverage` | MCP (claude.ai CMS Coverage) | Automated | — |
| ICD-10 Code Set (2026) | MCP API | Real-time | `lookup_code` / `search_codes` | MCP (claude.ai ICD-10 Codes) | Automated | — |
| CMS Medicare Plan Finder | Cloud Run API | Real-time | `search_plans_by_county` / `get_plan_details` | healthcare-mcps (Cloud Run) | Automated | — |
| Humana Agent Portal | MCP API | Real-time | `humana_get_agent` / `humana_get_medicare_plans` | MCP (rpi-healthcare) | Automated | — |
| Aetna FHIR API | MCP API | Real-time | `aetna_search_practitioners` / `aetna_search_insurance_plans` | MCP (rpi-healthcare) | Automated | — |

---

## 6. Validation Services

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| PhoneValidator.com | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated | — |
| NeverBounce (email validation) | API | Pipeline (4hr) + Quarterly | `pipelineValidationSweep()` / `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated | — |
| USPS Address Validation v3 | API | Quarterly (Oct AEP mega sweep) | `quarterlyHygieneCheck()` | `IMPORT_BulkValidation.gs` | Automated | — |
| WhitePages Pro (identity) | API | Planned | — | — | Not Started | M |

---

## 7. Document Intake Sources

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| SPC Specialist Folders (Drive) | PDF/IMG | Continuous (5-min scan) | `scanIntakeFolders()` → queue → watcher | `IMPORT_Intake.gs` | Automated | — |
| Google Meet Transcripts | Google Doc | Continuous (5-min scan) | `scanMeetingRecordings()` → queue → watcher | `IMPORT_Intake.gs` | Automated | — |
| Physical Mail (scanned) | PDF/IMG | Continuous (5-min scan) | `scanMailFolder()` → queue → watcher | `IMPORT_Intake.gs` | Automated | — |
| Email Inboxes (Gmail) | Email/Attachments | Continuous (5-min scan) | `scanEmailInboxes()` → queue → watcher | `IMPORT_Intake.gs` | Automated | — |

---

## 8. Internal Systems

| Source | Format | Frequency | Ingestion Method | Module | Status | Priority |
|--------|--------|-----------|-----------------|--------|--------|----------|
| RAPID_CORE normalizers | Library | Every write | Auto-applied on insert/update | `CORE_Normalize.gs` | Automated | — |
| RAPID_CORE reconciliation | Library | Weekly (Mon 6 AM) | `reconcileClients()` / `reconcileAccounts()` | `CORE_Reconcile.gs` | Automated | — |
| Drive Hygiene (md5 dedup) | Drive API | Weekly (Wed 6 AM) | `runDriveHygieneScan()` | `IMPORT_DriveHygiene.gs` | Automated | — |
| MCP Analytics push | Node.js script | Daily 11 PM | `scripts.run → pushAnalyticsData()` | MCP-Hub analytics | Automated | — |

---

## IMO Portal Reference

| IMO | Portal URL | Data Available | Current Access |
|-----|-----------|----------------|----------------|
| SPARK | spark.integrity.com | Commission statements, BoB, appointments | Active |
| SMS (Senior Market Sales) | sms.com | Commission statements, BoB | Active |
| PSMI | psmi.com | Commission statements | Active |
| Integrity | integrity.com | Aggregated reporting | Active |
| AmeriLife | amerilife.com | Commission statements | Active |

---

## Automation Priority Matrix

| Priority | Source | Current State | Automation Path |
|----------|--------|---------------|-----------------|
| **HIGH** | Humana/UHC/Aetna monthly BoB | Semi-auto (manual CSV download) | Carrier API integration or scheduled SFTP pull |
| **HIGH** | Commission sheets from IMOs | Manual download + FIX_ function | Stateable API covers most; remaining need portal scraping |
| **MEDIUM** | CoF inforce reports | Manual XLSX → Python → GAS | Annual frequency makes automation lower ROI |
| **MEDIUM** | Cigna/Wellcare BoB | Not started | Follow `FIX_ImportBoBData()` pattern |
| **MEDIUM** | WhitePages Pro identity verification | Not started | Add to RAPID_CORE validation suite |
| **LOW** | GHL bulk export | One-time done | API sync covers ongoing needs |

---

## Adding a New Data Source

1. **Identify category** from the tables above
2. **Document in this registry** (source, format, frequency, responsible party)
3. **Choose ingestion path:**
   - API available → Add to appropriate RAPID_IMPORT module
   - CSV/XLSX → Write Python converter + GAS FIX_ function (see CLAUDE.md § BoB Import Workflow)
   - Document → Route through intake channels (SPC/Mail/Email)
4. **Add RAPID_CORE normalizers** if new field types are introduced
5. **Update TAB_SCHEMAS** in RAPID_CORE if new columns are needed
6. **Run reconciliation** after first import to catch duplicates

---

*This document is the single source of truth for RPI's data landscape. Update it whenever a new source is onboarded.*
