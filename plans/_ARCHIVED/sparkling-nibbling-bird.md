# RPI Data Integration Overhaul Plan

## Context

The MATRIX data quality cleanup (Phases 1-7) is COMPLETE. The pipeline is clean and normalizing new data on entry. Now we need to:

1. **Rebuild the Data Source Registry** with the full carrier/IMO/BD/RIA/comms landscape JDM described
2. **Import communication archives** (Jira recordings from Drive, GHL/Lead Connector legacy call recordings + texts)
3. **Wire Google Chat** as a new communication intake channel
4. **Document per-carrier integration cascades** (API > webhook > manual) for 5 data types
5. **Reconsider the backend + frontend capability gap** with all new integrations

Previous plan (Part A/B/C) is 100% complete — this is a fresh plan.

---

## Sprint 1: Documentation Overhaul (No Code)

### 1A. Rebuild DATA_SOURCE_REGISTRY.md

**File:** `_RPI_STANDARDS/reference/data/DATA_SOURCE_REGISTRY.md`

Restructure from flat inventory into **per-carrier integration cascade matrix**:

**New Section Structure:**
1. Insurance Carriers (per-carrier cascade table)
2. IMO Partners (SPARK, Signal, Gradient)
3. BD/RIA Custodians (Schwab, RBC, DST Vision, DTCC)
4. Commission Aggregators (Stateable primary, carrier fallbacks)
5. Communication Channels (Twilio, SendGrid, Meet, Chat, Jira archive, GHL legacy)
6. Healthcare Data — split into:
   - 6a. **Quoting Tools** (CMS Plan Finder, NPI, ICD-10, Coverage DB) — NOT import sources, these are MCP-Hub/QUE tools
   - 6b. **Actual Data Imports** (Blue Button/ID.me, IRS feed/ID.me, EHR integrations, Aetna FHIR)
7. Agent/Producer Data (NIPR source of truth, carrier records, IMO records)
8. Validation Services (PhoneValidator, NeverBounce, USPS, WhitePages Pro)
9. Document Intake (SPC, Meet, Mail, Email — existing)
10. Internal Systems (normalizers, reconciliation, Drive hygiene, analytics)

**Per-Carrier Integration Cascade Table** (the core deliverable):

| Carrier | Client Data | Account Data | Commission | New Biz/Pending | Reactive Service |
|---------|-------------|--------------|------------|-----------------|------------------|
| Humana | SPARK webhook | SPARK webhook | Stateable API | SPARK webhook | Portal (manual) |
| UHC/AARP | Portal CSV | Portal CSV | Stateable API | Portal CSV | Portal (manual) |
| Aetna | FHIR API | FHIR API | Stateable API | Portal | Portal |
| North American | API (partner) | API (partner) | Stateable API | API (partner) | Portal |
| Midland | API (partner) | API (partner) | Stateable API | API (partner) | Portal |
| CoF | XLSX (annual) | XLSX (annual) | Stateable API | N/A | N/A |
| Cigna | Not Started | Not Started | Stateable API | Not Started | Not Started |
| Wellcare | Portal CSV | Portal CSV | Stateable API | Portal CSV | Portal |
| (etc for all carriers) |

Each cell: `[Method] ([Status]: Automated/Semi-auto/Manual/Not Started)`

**Method Priority Cascade:**
1. Real-time API (DTCC, Aetna FHIR, Schwab)
2. Webhook push (SPARK)
3. Scheduled API pull (Stateable)
4. SFTP/bulk file transfer
5. Manual portal download + FIX_ function
6. Paper/fax/phone

### 1B. Create CARRIER_INTEGRATION_MATRIX.md

**New file:** `_RPI_STANDARDS/reference/data/CARRIER_INTEGRATION_MATRIX.md`

Detailed per-carrier reference with: portal URLs, API endpoints, auth method, enrollment requirements, IMO intermediary, JDM action items.

**Carriers to document:** Humana, UHC/AARP, Aetna, Cigna, Wellcare/Centene, Anthem BCBS, Mutual of Omaha (Medicare); CoF, ALIC, North American, Midland, Allianz, Athene (Life); North American, Midland, Allianz, American Equity, Athene (Annuity); Schwab, RBC (BD/RIA)

**API Maturity Research Results:**
- DTCC I&RS: Full REST API + webhooks (launched Dec 2024) — **HIGH priority**
- Schwab: 370+ integrations, daily data feeds, OpenView Gateway — **HIGH priority**
- Aetna FHIR: Full FHIR v4, already partially integrated
- Signal: Embedded APIs via Hexure/FireLight, SSO — **MEDIUM**
- Gradient: Luma Financial Technologies partnerships — **MEDIUM**
- DST FanMail/Vision: Established aggregator, requires enrollment — **MEDIUM**
- North American/Midland: No public API found (JDM says they exist — likely partner/private)
- RBC: API in development, form-based data authorization currently
- American Equity/Athene/Voya: Portal-only or marketplace-only

### 1C. Update UI Capability Gap (RAPID_IMPORT CLAUDE.md)

Add new proposed section:
- **Integration Management Dashboard** — Per-source sync status, last sync, error counts, manual trigger buttons

### Sprint 1 Effort: ~3 hrs documentation. No JDM action needed.

---

## Sprint 2: Communication Archives + New Channels

### 2A. Google Chat Intake Channel

**File:** `RAPID_IMPORT/IMPORT_Comms.gs`

New function `syncGoogleChatMessages()`:
- Call Google Chat API v1 via `UrlFetchApp.fetch()` + `ScriptApp.getOAuthToken()`
- List monitored spaces → list messages since last sync (24hr lookback)
- Dedup by `chat_message_name` (already in `_COMMUNICATION_LOG` schema)
- Log each message via `callRapidAPIComms_()` with `channel: 'chat'`, `provider: 'google_chat'`
- PHI safe: content_preview truncated to 200 chars
- Add to `syncAllCommunications()` orchestrator — picked up by existing hourly trigger

**File:** `RAPID_IMPORT/appsscript.json` — add `chat.messages.readonly` OAuth scope

**JDM Action:** One-time OAuth consent after scope addition. Confirm which Chat spaces to monitor.

### 2B. Jira Recording Archive Import

**File:** `RAPID_IMPORT/IMPORT_Comms.gs`

New functions `FIX_ImportJiraRecordings()` / `FIX_ImportJiraRecordingsDryRun()`:
- Scan Drive folder recursively for recording files
- Extract metadata (filename, creation date, Drive URL)
- Match to `_CLIENT_MASTER` via `jira_key` field or filename pattern
- Log to `_COMMUNICATION_LOG` with `channel: 'recording'`, `provider: 'jira'`

**JDM Action:** Provide Drive folder ID containing Jira recordings. Confirm naming pattern.

### 2C. GHL Legacy Communication Archive

**File:** `RAPID_IMPORT/IMPORT_Comms.gs`

New functions `FIX_ImportGHLCommHistory()` / `FIX_ImportGHLCommHistoryDryRun()`:
- GHL API does NOT expose call recordings or SMS (confirmed in research)
- Strategy: JDM exports from GHL portal as CSV → Python preprocessing → inline JS FIX_ function (following BoB pattern)
- Match `ghl_contact_id` to `_CLIENT_MASTER` → get `client_id`
- Log with `provider: 'ghl_legacy'` — distinct from ongoing Twilio records (`provider: 'twilio'`)
- GHL overlap handling: provider field distinguishes legacy vs. new

**JDM Action:** Export call recordings + SMS history from GHL portal before decommission.

### 2D. Meet Transcript Cross-Reference (Minor Enhancement)

**File:** `RAPID_IMPORT/IMPORT_Comms.gs` — modify `syncMeetRecordings()`

Cross-reference `meet_event_id` between `_COMMUNICATION_LOG` and `_INTAKE_QUEUE` so meeting recordings are linked to their intake pipeline entries.

### Sprint 2 Verification:
- `FIX_ImportJiraRecordingsDryRun()` → finds recordings, matches to clients
- `FIX_ImportGHLCommHistoryDryRun()` → matches ghl_contact_id to client_id
- `syncGoogleChatMessages()` manual run → Chat messages appear in `_COMMUNICATION_LOG`
- `syncAllCommunications()` runs all 4 channels (Twilio, SendGrid, Meet, Chat)
- No PHI in content_preview fields
- No duplicate records (check by external_id)

### Sprint 2 Effort: ~4 hrs code. JDM actions: Chat scope consent, Jira folder ID, GHL export.

---

## Sprint 3: Carrier Integration Framework

### 3A. DTCC I&RS Integration (New Module)

**Priority: HIGH** — Full REST API + webhooks for life/annuity data. Backbone for automated account data.

**New file:** `RAPID_IMPORT/IMPORT_DTCC.gs`
- `SETUP_DTCCConfig()` — credentials in Script Properties
- `TEST_DTCCConnection()` — verify access
- `syncDTCCPolicies(filters)` — pull policy data → `_ACCOUNT_LIFE` / `_ACCOUNT_ANNUITY`
- `syncDTCCTransactions(filters)` — pull transactions

**New file:** `RAPID_API/API_DTCC.gs` — webhook handler (following `API_Spark.gs` pattern)

**RAPID_CORE schema:** Add `dtcc_policy_id` to account TAB_SCHEMAS

**JDM Action:** DTCC I&RS enrollment, obtain API credentials, confirm which carriers are covered

### 3B. Schwab Advisor Services Integration (New Module)

**Priority: HIGH** — 370+ integrations, daily data feeds for BD/RIA accounts.

**New file:** `RAPID_IMPORT/IMPORT_Schwab.gs`
- `SETUP_SchwabConfig()` — OAuth credentials
- `TEST_SchwabConnection()` — verify access
- `syncSchwabAccounts()` — pull account positions → `_ACCOUNT_BDRIA`
- `syncSchwabTransactions()` — pull transaction history

**JDM Action:** Enroll in Schwab Advisor Services developer program through Gradient

### 3C. Gradient IMO Onboarding (New Module)

**New file:** `RAPID_IMPORT/IMPORT_Gradient.gs`
- `SETUP_GradientConfig()` — credentials
- `syncGradientProducerStatus()` — appointment/contracting → `_AGENT_MASTER`
- `syncGradientPolicies()` — new business/pending → `_ACCOUNT_LIFE`, `_ACCOUNT_ANNUITY`

**JDM Action:** Confirm Gradient timeline, obtain API docs/credentials

### 3D. Blue Button (ID.me) Integration (New Module)

CMS Blue Button 2.0: Original Medicare A&B claims via FHIR, authenticated through ID.me.

**New file:** `RAPID_IMPORT/IMPORT_BlueButton.gs`
- `SETUP_BlueButtonConfig()` — OAuth client registration with CMS
- `requestPatientAuthorization(clientId)` — generate consent URL
- `fetchBeneficiaryData(accessToken)` — pull claims, EOBs, coverage
- `mapBlueButtonToClient(fhirData)` — map FHIR Patient to `_CLIENT_MASTER`

Requires per-client authorization (consent via ID.me). Client consent flow lives in PRODASHX.

**RAPID_CORE schema:** Add `blue_button_subscriber_id` to `_CLIENT_MASTER`

**JDM Action:** Register with CMS Blue Button developer sandbox

### 3E. Stateable API Enhancement

**File:** `RAPID_IMPORT/IMPORT_Revenue.gs`

Add `fetchDirectCarrierCommissions(carrier, filters)` fallback function for when Stateable doesn't cover a commission source. Document per-IMO Stateable coverage:
- SPARK (Integrity): Covered
- Signal: Covered during transition
- Gradient: TBD pending enrollment

### 3F. Carrier Integration Template

**New file:** `_RPI_STANDARDS/reference/data/CARRIER_INTEGRATION_TEMPLATE.md`

Standard template for documenting each carrier integration: connection details, data types, field mapping, setup steps.

### Sprint 3 is heavily JDM-action-dependent (vendor enrollments). Build modules as APIs become available.

---

## Sprint 4: UI Dashboard

### 4A. Integration Status Dashboard

**New file:** `RAPID_IMPORT/INTEGRATION_UI.html`
**Route:** `?page=integrations`

Card-based layout, one per source:
- Stateable (commission): Last sync, record count, "Sync Now"
- SPARK (webhook): Last event, events processed, status
- Twilio (SMS/Voice): Last sync, "Sync Now"
- SendGrid (Email): Last sync, "Sync Now"
- Google Chat: Last sync, "Sync Now"
- Google Meet: Last sync, "Sync Now"
- DTCC / Schwab (when ready): Connection status, last sync

Color-coded: Green (on schedule), Yellow (overdue), Red (error)

### 4B. Data Quality Tools (Home Page Section)

- Buttons for normalization, backfill, dedup with DryRun preview
- Live metrics: dupe count, orphan count, blank status count, last normalization date
- Each FIX_ function gets a ForUI wrapper

### 4C. Communication History Viewer

Browse all comms across channels (Twilio, SendGrid, Meet, Chat, Jira, GHL legacy) in unified timeline view per client.

### Sprint 4 depends on Sprint 2 + 3 functions existing.

---

## Execution Order & Dependencies

```
Sprint 1 (Documentation) ──→ Can start NOW, no dependencies
    │
    ├──→ Sprint 2 (Comms) ──→ Depends on JDM: Chat scope, Jira folder, GHL export
    │         │
    └──→ Sprint 3 (Carriers) ──→ Depends on JDM: DTCC/Schwab/Gradient enrollment
              │
              └──→ Sprint 4 (UI) ──→ Depends on Sprint 2+3 functions
```

**Sprint 1 and Sprint 2 can run in parallel** (docs vs. code).

---

## JDM Action Items (All Sprints)

| # | Item | Sprint | Priority | What JDM Needs to Do |
|---|------|--------|----------|---------------------|
| 1 | Google Chat scope | 2 | HIGH | One-time OAuth consent after appsscript.json update |
| 2 | Chat space list | 2 | HIGH | Tell me which Chat spaces to monitor (all? specific?) |
| 3 | Jira recordings folder | 2 | HIGH | Provide Google Drive folder ID(s) |
| 4 | GHL comm export | 2 | HIGH | Export call recordings + SMS from GHL portal (CSV) |
| 5 | NACOLAH/Midland API | 3 | HIGH | Confirm partner API access, provide docs |
| 6 | DTCC enrollment | 3 | HIGH | Enroll with DTCC I&RS, obtain credentials |
| 7 | Schwab enrollment | 3 | HIGH | Enroll via Gradient, obtain OAuth credentials |
| 8 | Gradient onboarding | 3 | MEDIUM | Confirm timeline, obtain API docs |
| 9 | RBC API timeline | 3 | MEDIUM | Check availability through Gradient |
| 10 | Blue Button registration | 3 | MEDIUM | Register with CMS developer sandbox |
| 11 | DST Vision enrollment | 3 | MEDIUM | Enroll through Gradient BD relationship |
| 12 | IRS data feed | 3 | LOW | Investigate ID.me IRS integration requirements |
| 13 | EHR partnerships | 3 | LOW | Confirm which providers/systems for integration |

---

## Critical Files

| File | Sprint | Role |
|------|--------|------|
| `_RPI_STANDARDS/reference/data/DATA_SOURCE_REGISTRY.md` | 1 | Rebuild with full landscape |
| `_RPI_STANDARDS/reference/data/CARRIER_INTEGRATION_MATRIX.md` | 1 | NEW — per-carrier detail |
| `RAPID_IMPORT/IMPORT_Comms.gs` | 2 | Add Chat sync, Jira import, GHL legacy import |
| `RAPID_IMPORT/appsscript.json` | 2 | Add Chat OAuth scope |
| `RAPID_IMPORT/IMPORT_DTCC.gs` | 3 | NEW — DTCC integration |
| `RAPID_IMPORT/IMPORT_Schwab.gs` | 3 | NEW — Schwab integration |
| `RAPID_IMPORT/IMPORT_Gradient.gs` | 3 | NEW — Gradient integration |
| `RAPID_IMPORT/IMPORT_BlueButton.gs` | 3 | NEW — Blue Button integration |
| `RAPID_API/API_DTCC.gs` | 3 | NEW — DTCC webhook handler |
| `RAPID_CORE/CORE_Database.gs` | 3 | Schema additions (dtcc_policy_id, blue_button_subscriber_id) |
| `RAPID_IMPORT/INTEGRATION_UI.html` | 4 | NEW — Integration dashboard |
| `RAPID_IMPORT/CLAUDE.md` | 1-4 | Update throughout |
