# RAPID_IMPORT Platform Roadmap

> Consolidated from 6 individual plans + cross-platform Comms Intake items from wondrous-snuggling-phoenix.
> Last updated: 2026-03-03

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| Phase 0 | Feb 2026 | RAPID_CORE normalizer expansion — `normalizeStatus()`, 12+ new CARRIER_ALIASES, date guard for day-of-week strings |
| Phase 1 | Feb 2026 | Normalize all existing data — 6 PRODASH_MATRIX tabs run through `normalizeExistingData()` (~5,200 clients, ~11,150 accounts) |
| Phase 2 | Feb 2026 | Targeted backfills — client_status backfill (~4,790 records), client state from ZIP (~885 records), Medicare garbage date cleanup |
| Phase 3 | Feb 2026 | Orphan resolution — GHL orphan linker + general orphan cleanup + CoF-specific linking |
| Phase 4 | Feb 2026 | Reconciliation pass — 270 client dupes merged (85+ auto, 70-84 manual review), 39 annuity dupes resolved via FK updates |
| Phase 5 | Feb 2026 | CoF Enrichment P1 — 699 CoF contact records enriched (DOB, phone, address, Medicare number) |
| Phase 7 | Feb 2026 | Final verification — `DEBUG_InventoryProdash()` confirmed 0 orphans, standardized carriers, clean statuses |
| FK Migration | Feb 24 | PRODASHX FK migration (v3.9 @191) — 4,649 clients normalized, 4,617 statuses cleaned, 270 client dupes merged, 39 annuity dupes resolved |
| SPARK Pass 1-2 | Feb 2026 | SPARK enrichment — 486 SPARK Medicare accounts mapped + initial field enrichment from SPARK CSVs |
| rpi-comms-mcp | Feb 2026 | Twilio + SendGrid + Campaign engine live — 18 MCP tools operational |
| Meet tools | Feb 2026 | 5 Google Meet tools added to rpi-workspace-mcp |
| Stream 1 | Mar 3, 2026 | Compliance & Security — ALL COMPLETE (SSN masking, confirmations, secrets, access all verified; SSN edit input fix v3.27.1 @184) |
| Stream 2 | Mar 3, 2026 | Code Quality & UX — ALL COMPLETE. Orphan pagination v3.29.0 @189. Hardcoded MATRIX ID removed v3.27.2 @185. Only 2C.2 (pin RAPID_CORE) pending JDM decision. |
| Stream 8 | Mar 3, 2026 | Comms Intake — ACTIVATED. _COMMUNICATION_LOG tab created, schema expanded (28 cols), Twilio/SendGrid/Meet/Chat all verified, hourly trigger set. |
| Stream 3 | Prior sessions | Mail Approval Workflow — ALL COMPLETE (Slack per-doc links, footer link, MAIL channel routing, pending batch list) |
| Stream 4 | Prior sessions | SPARK Enrichment Pass 3 — ALL COMPLETE (6 schema fields, SETUP, enrichment executed, testing guide) |

---

## Stream 1: Compliance & Security

**Status: COMPLETE**
**Source plan:** `shiny-whistling-lecun.md` (Phase 1)
**Completed:** 2026-03-03

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 1.1 | **SSN masking in APPROVAL_UI.html** | P0 | ✅ Done (prior) | `formatDisplayValue()` at L756-764 masks to `***-**-XXXX` |
| 1.2 | **SSN masking in RECONCILE_UI.html** | P0 | ✅ Done (prior) | `formatDisplayVal()` at L1008-1017 masks to `***-**-XXXX` |
| 1.3 | **Confirmation dialog before Execute Writes** | P0 | ✅ Done (prior) | `executeBatch()` at L1541-1555 calls `showConfirmation()` |
| 1.4 | **Confirmation dialogs in RECONCILE_UI.html** | P0 | ✅ Done (prior) | `doDeleteRecord()` L2029 + `autoMergeExecute()` L751 both use `showConfirmation()` |
| 1.5 | **DEBUG_DumpScriptProperties secret exposure** | P0 | ✅ Done (prior) | Sensitive key masking at IMPORT_CaseTasks.gs L714 |
| 1.6 | **appsscript.json source file audit** | P0 | ✅ Compliant | `"access": "DOMAIN"` at L34 + L38 |
| 1.7 | **Security tracker update** | P1 | ✅ Done (prior) | POSTURE.md L185: RAPID_IMPORT DOMAIN verified 2026-02-14 |
| NEW | **SSN masking in edit input** | P0 | ✅ Done (v3.27.1) | Edit input shows masked SSN, preserves original on save if unchanged |

---

## Stream 2: Code Quality & UX

**Status: OPEN**
**Source plan:** `shiny-whistling-lecun.md` (Phases 2-3)

### 2A: Bug Fixes & Code Quality (Phase 2) — COMPLETE

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2A.1 | **ZIP zero-pad fix** | P1 | ✅ Done (prior) | `normalizeZip()` L740-753 handles 4/5/8/9 digit. `validateZip()` L646-675 accepts 4-digit with warning. |
| 2A.2 | **DryRun for BoB import** | P1 | ✅ Done (prior) | `FIX_ImportBoBDataDryRun()` at L47. All major FIX_ functions have DryRun wrappers. |
| 2A.3 | **Home page "Loading Status"** | P2 | ✅ Done (prior) | `loadReconciliationStatus()` L2631 + `loadDriveHygieneStatus()` L2706 called on page load. |
| 2A.4 | **Queue depth on home page** | P2 | ✅ Done (prior) | `loadQueueDepths()` L2751 calls both intake + approval depth on load with badge rendering. |
| 2A.5 | **CLAUDE.md updates** | P3 | ✅ Done (v3.27.1) | Version bumped, 27 files documented, 42 ForUI functions listed, deploy ID current. |

### 2B: Frontend/Backend Gap Closure (Phase 3) — MOSTLY COMPLETE

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2B.1 | **Approval batch search** | P2 | ✅ Done (prior) | Search input in APPROVAL_UI.html L365 + JS L491-524. Searches by name, batch ID, or source. |
| 2B.2 | **Bulk orphan linking** | P2 | ✅ Done (prior) | Multi-select checkboxes + bulk link bar + confirmation. RECONCILE_UI.html L447, L1697-1768. |
| 2B.3 | **Orphan search pagination** | P3 | ✅ Done (v3.29.0) | Load More button when 50+ results. Server offset pagination. Page size raised from 15 to 50. |
| 2B.4 | **Merge summary before execute** | P3 | ✅ Done (prior) | Full modal with field-by-field preview, overwrite warnings. L473-489, L1930-1984. |
| 2B.5 | **Email inbox config link** | P3 | ✅ Done (prior) | "Configure Inboxes" button opens RAPID_MATRIX directly + toast. Code.gs L2178-2179. |

### 2C: Maintainability (Phase 5 from shiny-whistling-lecun) — MOSTLY COMPLETE

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2C.1 | **Archive executed FIX_ functions** | P3 | ✅ Done (prior) | `IMPORT_BoBEnrich_Archive.gs` (23,987 lines) split from active file (3,705 lines). `IMPORT_Approval.gs` still 21,881 lines — future trim candidate. |
| 2C.2 | **Pin RAPID_CORE library version** | P3 | Pending JDM decision | `developmentMode: true` in appsscript.json L27. Pin = set to `false`. |
| 2C.3 | **callRapidAPI_ timeout** | P2 | ✅ Done (prior) | `muteHttpExceptions: true` + `timeout: 45000` at Code.gs L98-99. (Note: GAS ignores timeout param, 60s runtime limit applies.) |
| 2C.4 | **Consolidate redundant functions** | P3 | ✅ Partial (v3.27.2) | Removed hardcoded MATRIX ID from `getMatrixSpreadsheet_Code_()`. `generateUUID` already delegates to RAPID_CORE. `getMatrixSpreadsheet_` still has 3 variants — future consolidation candidate. |

**Files:** `RAPID_CORE/CORE_Normalize.gs`, `IMPORT_Validation.gs`, `Code.gs`, `APPROVAL_UI.html`, `RECONCILE_UI.html`, `IMPORT_Approval.gs`, `IMPORT_Archive.gs` (new)
**Dependencies:** 2A.1 requires RAPID_CORE push first. 2C.1-2C.2 require JDM decisions on open questions Q1/Q2/Q4.
**Effort:** ~8-10 hours total across 2-3 sessions.

---

## Stream 3: Mail Approval Workflow

**Status: COMPLETE**
**Source plan:** `dapper-rolling-glade.md`
**Completed:** Prior sessions (verified 2026-03-03)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 3.1 | **Slack per-doc links** | P1 | ✅ Done (prior) | watcher.js L297-298: `<${CONFIG.rapidImportUrl}?page=approval&batch_id=${doc.batchId}\|📋 Review>` |
| 3.2 | **Footer "Review All" link** | P1 | ✅ Done (prior) | watcher.js L319-320: `<${CONFIG.rapidImportUrl}?page=training\|Review All in RAPID_IMPORT>` |
| 3.3 | **MAIL channel routing** | P1 | ✅ Done (prior) | watcher.js L1715-1726 + L3684-3890: `routed_channel: isMail ? CONFIG.slackServiceChannel : null` at both call sites |
| 3.4 | **Pending batch list on home page** | P2 | ✅ Done (prior) | Server (IMPORT_Approval.gs L4714-4782) + HTML (Code.gs L2197) + client renderer (Code.gs L2769-2804) |
| 3.5 | **Taxonomy verification for MAIL** | P2 | ✅ Verified (2026-03-03) | 36 MAIL entries active (12 Medicare + 24 Retirement). All with extraction hints, routing, priorities. |

---

## Stream 4: SPARK Enrichment Pass 3

**Status: COMPLETE**
**Source plan:** `lucky-tumbling-beacon.md`
**Completed:** Prior sessions (verified 2026-03-03, commit f525d1e)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 4.1 | **RAPID_CORE schema changes** | P1 | ✅ Done | 5 fields in `_ACCOUNT_MEDICARE` (L540-543), `county_fips` in `_CLIENT_MASTER` (L323), `submitted_date` in FIELD_NORMALIZERS |
| 4.2 | **SETUP_SparkSchemaColumns** | P1 | ✅ Done | IMPORT_BoBImport.gs L4551 |
| 4.3 | **Python data conversion** | P1 | ✅ Done | 551 account records + 9 client records generated |
| 4.4 | **FIX_EnrichSparkAccounts3_** | P1 | ✅ Done + Executed | IMPORT_BoBImport.gs L4590-5335, both DryRun and live run completed |
| 4.5 | **Push + Execute sequence** | P1 | ✅ Done | RAPID_CORE + RAPID_IMPORT pushed, SETUP + DryRun + Execute all ran |

---

## Stream 5: Data Quality Completion

**Status: BLOCKED -- Phase 6 waiting on CoF response**
**Source plan:** `stateless-marinating-hopper.md` (Phase 6)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 5.1 | **Python preprocessing** — Convert CoF policy detail dataset to inline JS (same pattern as CoF member import). Key = `cof_member_id` or `policy_number`. | P2 | BLOCKED | Waiting for JDM to provide CoF policy detail dataset |
| 5.2 | **FIX_EnrichCoFPolicyDetails_** — New function in `IMPORT_BoBEnrich.gs`. Match by `policy_number` against `_ACCOUNT_LIFE` records. Fill: `product_type`, `product_name`, `policy_type`. | P2 | BLOCKED | Depends on 5.1 |
| 5.3 | **Annuity reclassification** — Move policies to `_ACCOUNT_ANNUITY` if `product_type` resolves to annuity. | P2 | BLOCKED | Depends on 5.2 |
| 5.4 | **Post-enrichment normalization** — Run `normalizeExistingData('_ACCOUNT_LIFE')` and `normalizeExistingData('_ACCOUNT_ANNUITY')` to normalize new values. | P2 | BLOCKED | Depends on 5.2 |

**Files:** `RAPID_IMPORT/IMPORT_BoBImport.gs`, `RAPID_IMPORT/IMPORT_BoBEnrich.gs`
**Dependencies:** JDM must provide CoF policy detail dataset (response from Janet/CoF pending).
**Effort:** ~3 hours once data arrives.

**Context (completed phases):**
- Phases 0-5 + 7 are COMPLETE. 4,649 clients normalized, 4,617 statuses cleaned, 270 client dupes merged, 39 annuity dupes resolved via FK updates. CoF Enrichment P1 (699 contacts) complete. Final verification passed.
- Only Phase 6 (CoF policy detail import) remains.

---

## Stream 6: Data Integration Overhaul

**Status: OPEN -- documentation sprint can start now, code sprints depend on JDM vendor actions**
**Source plan:** `sparkling-nibbling-bird.md`

### 6A: Documentation Overhaul (Sprint 1 -- No Code)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 6A.1 | **Rebuild DATA_SOURCE_REGISTRY.md** — Restructure from flat inventory into per-carrier integration cascade matrix. 10 new sections: Insurance Carriers, IMO Partners, BD/RIA Custodians, Commission Aggregators, Communication Channels, Healthcare Data (split quoting vs. imports), Agent/Producer Data, Validation Services, Document Intake, Internal Systems. | P2 | Not started | ~3 hrs documentation |
| 6A.2 | **Create CARRIER_INTEGRATION_MATRIX.md** — Per-carrier reference with portal URLs, API endpoints, auth method, enrollment requirements, IMO intermediary. Carriers: Humana, UHC/AARP, Aetna, Cigna, Wellcare, Anthem BCBS, Mutual of Omaha (Medicare); CoF, ALIC, North American, Midland, Allianz, Athene (Life/Annuity); Schwab, RBC (BD/RIA). | P2 | Not started | New file in `_RPI_STANDARDS/reference/data/` |
| 6A.3 | **Create CARRIER_INTEGRATION_TEMPLATE.md** — Standard template for documenting each carrier integration. | P3 | Not started | Reusable pattern |
| 6A.4 | **Update RAPID_IMPORT CLAUDE.md** — Add proposed Integration Management Dashboard section. | P3 | Not started | Documentation |

### 6B: Communication Archives + New Channels (Sprint 2)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 6B.1 | **Google Chat intake channel** — New `syncGoogleChatMessages()` in `IMPORT_Comms.gs`. Call Google Chat API v1 via `UrlFetchApp.fetch()` + `ScriptApp.getOAuthToken()`. Dedup by `chat_message_name`. Log via `callRapidAPIComms_()` with `channel: 'chat'`, `provider: 'google_chat'`. Add to `syncAllCommunications()` orchestrator. | P2 | Not started | JDM action: OAuth consent after `chat.messages.readonly` scope added to appsscript.json. Confirm which Chat spaces to monitor. |
| 6B.2 | **Jira recording archive import** — New `FIX_ImportJiraRecordings()` / `FIX_ImportJiraRecordingsDryRun()`. Scan Drive folder recursively for recording files. Extract metadata. Match to `_CLIENT_MASTER` via `jira_key` or filename pattern. Log to `_COMMUNICATION_LOG` with `channel: 'recording'`, `provider: 'jira'`. | P2 | Not started | JDM action: Provide Drive folder ID. Confirm naming pattern. |
| 6B.3 | **GHL legacy communication archive** — New `FIX_ImportGHLCommHistory()` / DryRun. GHL API does NOT expose call recordings or SMS. Strategy: JDM exports CSV from GHL portal -> Python preprocessing -> inline JS FIX_ function. Match `ghl_contact_id` to `_CLIENT_MASTER` -> get `client_id`. Log with `provider: 'ghl_legacy'`. | P2 | Not started | JDM action: Export call recordings + SMS history from GHL portal before decommission. |
| 6B.4 | **Meet transcript cross-reference** — Modify `syncMeetRecordings()` to cross-reference `meet_event_id` between `_COMMUNICATION_LOG` and `_INTAKE_QUEUE`. | P3 | Not started | Minor enhancement |

### 6C: Carrier Integration Framework (Sprint 3)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 6C.1 | **DTCC I&RS integration** — New `IMPORT_DTCC.gs` with `SETUP_DTCCConfig()`, `TEST_DTCCConnection()`, `syncDTCCPolicies()`, `syncDTCCTransactions()`. New `API_DTCC.gs` in RAPID_API for webhook handler. Add `dtcc_policy_id` to RAPID_CORE account schemas. Full REST API + webhooks (launched Dec 2024). | HIGH | Not started | JDM action: DTCC I&RS enrollment, obtain API credentials |
| 6C.2 | **Schwab Advisor Services integration** — New `IMPORT_Schwab.gs` with `SETUP_SchwabConfig()`, `TEST_SchwabConnection()`, `syncSchwabAccounts()`, `syncSchwabTransactions()`. 370+ integrations, daily data feeds. | HIGH | Not started | JDM action: Enroll via Gradient, obtain OAuth credentials |
| 6C.3 | **Gradient IMO onboarding** — New `IMPORT_Gradient.gs` with `SETUP_GradientConfig()`, `syncGradientProducerStatus()`, `syncGradientPolicies()`. | MEDIUM | Not started | JDM action: Confirm timeline, obtain API docs |
| 6C.4 | **Blue Button (ID.me) integration** — New `IMPORT_BlueButton.gs` with OAuth client registration, patient authorization consent URL, FHIR data fetch, mapping to `_CLIENT_MASTER`. Add `blue_button_subscriber_id` to `_CLIENT_MASTER` schema. Per-client authorization required (consent flow lives in PRODASHX). | MEDIUM | Not started | JDM action: Register with CMS Blue Button developer sandbox |
| 6C.5 | **Stateable API enhancement** — Add `fetchDirectCarrierCommissions(carrier, filters)` fallback function in `IMPORT_Revenue.gs` for when Stateable doesn't cover a source. Document per-IMO coverage. | LOW | Not started | Fill gaps in commission coverage |

### 6D: Integration Dashboard (Sprint 4)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 6D.1 | **Integration status dashboard** — New `INTEGRATION_UI.html`, route `?page=integrations`. Card-based layout per source: Stateable, SPARK, Twilio, SendGrid, Google Chat, Google Meet, DTCC/Schwab (when ready). Color-coded: Green (on schedule), Yellow (overdue), Red (error). | P3 | Not started | Depends on Sprint 2+3 functions |
| 6D.2 | **Data quality tools section** — Buttons for normalization, backfill, dedup with DryRun preview. Live metrics: dupe count, orphan count, blank status count, last normalization date. | P3 | Not started | Surface existing backend capabilities |
| 6D.3 | **Communication history viewer** — Browse all comms across channels in unified timeline view per client. | P3 | Not started | Depends on comms intake being populated |

**Files:** `_RPI_STANDARDS/reference/data/DATA_SOURCE_REGISTRY.md`, `_RPI_STANDARDS/reference/data/CARRIER_INTEGRATION_MATRIX.md`, `RAPID_IMPORT/IMPORT_Comms.gs`, `RAPID_IMPORT/IMPORT_DTCC.gs` (new), `RAPID_IMPORT/IMPORT_Schwab.gs` (new), `RAPID_IMPORT/IMPORT_Gradient.gs` (new), `RAPID_IMPORT/IMPORT_BlueButton.gs` (new), `RAPID_API/API_DTCC.gs` (new), `RAPID_CORE/CORE_Database.gs` (schema additions), `RAPID_IMPORT/INTEGRATION_UI.html` (new), `RAPID_IMPORT/appsscript.json`
**Dependencies:** 6A (docs) can start now. 6B depends on JDM OAuth consent + folder IDs + GHL export. 6C depends on JDM vendor enrollments. 6D depends on 6B+6C functions existing.

**JDM Action Items (Stream 6):**

| # | Item | Sprint | What JDM Needs to Do |
|---|------|--------|---------------------|
| 1 | Google Chat scope | 6B | One-time OAuth consent after appsscript.json update |
| 2 | Chat space list | 6B | Tell which Chat spaces to monitor (all? specific?) |
| 3 | Jira recordings folder | 6B | Provide Google Drive folder ID(s) |
| 4 | GHL comm export | 6B | Export call recordings + SMS from GHL portal (CSV) |
| 5 | NACOLAH/Midland API | 6C | Confirm partner API access, provide docs |
| 6 | DTCC enrollment | 6C | Enroll with DTCC I&RS, obtain credentials |
| 7 | Schwab enrollment | 6C | Enroll via Gradient, obtain OAuth credentials |
| 8 | Gradient onboarding | 6C | Confirm timeline, obtain API docs |
| 9 | Blue Button registration | 6C | Register with CMS developer sandbox |
| 10 | RBC API timeline | 6C | Check availability through Gradient |
| 11 | DST Vision enrollment | 6C | Enroll through Gradient BD relationship |

---

## Stream 7: API Validation Architecture

**Status: RESEARCH COMPLETE -- awaiting JDM decisions**
**Source plans:** `shiny-whistling-lecun.md` (Phase 4), `shiny-whistling-lecun-agent-a87c5fb.md` (vendor research)

### Architecture Decision: Layered Model

```
LAYER 1: Frontend HTML (ProDashX, Sentinel, RIIMO forms)
  -- Google Places Autocomplete widget (client-side JS)

LAYER 2: RAPID_CORE (shared GAS library)
  -- New file: CORE_Validation_API.gs
     - validateAddress_viaAPI(address)
     - validatePhone_viaAPI(phone)
     - validateEmail_viaAPI(email)
     - enrichContact_viaAPI(name, phone, email, address)
     - API keys in Script Properties (NOT in RAPID_CORE code)

LAYER 3: RAPID_IMPORT (bulk orchestration)
  -- New file: IMPORT_BulkValidation.gs
     - FIX_BulkValidatePhones(dryRun)
     - FIX_BulkValidateEmails(dryRun)
     - FIX_BulkValidateAddresses(dryRun)
     - Rate limiting, batching, result storage

LAYER 4: MCP-Hub (future, lower priority)
  -- validate_contact, enrich_contact tools
```

### Vendor Selection (Research Complete)

| Need | Recommended Vendor | Cost (3,500 records) | Monthly Ongoing |
|------|-------------------|---------------------|-----------------|
| Frontend address autocomplete | Google Places Autocomplete | FREE (within 10K/mo) | FREE |
| Address + phone + email validation | WhitePages Pro | Included in subscription | Included |
| CASS-certified address standardization | Google Address Validation | ~$60 one-time | ~$2/mo |
| Deep email hygiene | NeverBounce | ~$28 one-time | ~$0.50-1.00/mo |
| **Total** | | **~$88** | **~$3/month** |

### Implementation Items

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 7.1 | **JDM confirms WhitePages Pro API access** — Is it web portal only or does subscription include API key? Check account settings. | P1 | Pending JDM | Determines scope of 7.3 |
| 7.2 | **Enable Google Places API + Maps JS API** — In GCP project `90741179392`. Restrict API key to `*.googleusercontent.com` referrers + Places/Maps API only. | P1 | Pending JDM | One-time GCP console action |
| 7.3 | **Build CORE_Validation_API.gs in RAPID_CORE** — WhitePages Pro wrappers: `validateAddress_viaAPI()`, `validatePhone_viaAPI()`, `validateEmail_viaAPI()`, `enrichContact_viaAPI()`. All return structured `{ success, data }`. | P2 | Not started | Foundation for all validation |
| 7.4 | **Build IMPORT_BulkValidation.gs in RAPID_IMPORT** — Batch runner with DryRun: `FIX_BulkValidatePhones(dryRun)`, `FIX_BulkValidateEmails(dryRun)`, `FIX_BulkValidateAddresses(dryRun)`. Rate limiting, batching, result storage. | P2 | Not started | Clean existing 3,500 records |
| 7.5 | **Google Places Autocomplete in ProDashX + Sentinel** — Add Maps JS library `<script>` tag to HTML templates. Attach `google.maps.places.Autocomplete` to address input fields. Handle `place_changed` event to populate structured address components. | P2 | Not started | Frontend UX win, client-side only |
| 7.6 | **NeverBounce bulk email clean** — Run one-time bulk validation on 3,500 email records (~$28). | P3 | Not started | Catches what WhitePages misses |
| 7.7 | **Google Address Validation bulk clean** — Run one-time CASS standardization (~$60). Only needed if RPI sends physical mail. | P3 | Not started | Optional based on mail needs |

**Files:** `RAPID_CORE/CORE_Validation_API.gs` (new), `RAPID_IMPORT/IMPORT_BulkValidation.gs` (new), `PRODASHX/Index.html`, `sentinel-v2/` HTML templates
**Dependencies:** 7.1-7.2 (JDM actions) must complete before code work. 7.3 must complete before 7.4.
**Effort:** ~12-16 hours total. P1 JDM actions, then P2 code in 2-3 sessions.

---

## Stream 8: Comms Intake Sync

**Status: OPEN -- rpi-comms-mcp and Meet tools already live, intake sync not yet built**
**Source plan:** `wondrous-snuggling-phoenix.md` (Sprint 9: RAPID_IMPORT Comms Intake)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 8.1 | **syncTwilioMessages()** — Pull Twilio SMS/call logs into `_COMMUNICATION_LOG`. Dedup by `twilio_sid`. Schedule as part of `syncAllCommunications()` hourly orchestrator. | P2 | Not started | rpi-comms-mcp already has `comms_list_sms` + `comms_list_recordings` tools live |
| 8.2 | **syncSendGridActivity()** — Pull SendGrid delivery/open/click/bounce events into `_COMMUNICATION_LOG`. Dedup by `sendgrid_message_id`. | P2 | Not started | rpi-comms-mcp already has `comms_get_email_activity` tool live |
| 8.3 | **syncMeetRecordings()** — Scan for new Google Meet recordings, create `_INTAKE_QUEUE` entries for transcription pipeline. Cross-reference `meet_event_id` between `_COMMUNICATION_LOG` and `_INTAKE_QUEUE`. | P2 | Not started | rpi-workspace already has `meet_list_recordings` + `meet_get_transcript` tools live |
| 8.4 | **importGHLContactsToNative()** — One-time migration function to ensure all GHL contact data exists in MATRIX before GHL decommission. Verify `ghl_contact_id` mappings are complete. | P2 | Not started | Pre-GHL-cancellation safety net |
| 8.5 | **GHL elimination verification** — After comms intake is live and GHL data migrated: grep all GAS projects for "GHL" -- zero matches except `ghl_contact_id` historical field. Cancel GHL subscription. | P3 | Not started | Final GHL decommission step |

**Files:** `RAPID_IMPORT/IMPORT_Comms.gs` (new or extend existing), `RAPID_IMPORT/appsscript.json` (scope additions)
**Dependencies:** rpi-comms-mcp (DONE), Meet tools in rpi-workspace (DONE). GHL elimination (8.5) depends on all other items complete + JDM approval.
**Effort:** ~4-5 hours for 8.1-8.3. 8.4 is ~2 hours. 8.5 is verification only.

---

## Recommended Execution Order

### Phase 1: Immediate (No blockers, high value) — COMPLETE ✅

**Streams 1 + 3 + 4** -- All verified complete as of 2026-03-03.

1. ~~**Stream 1: Compliance & Security**~~ — ✅ All 7 original items + 1 new SSN edit fix (v3.27.1 @184)
2. ~~**Stream 3: Mail Approval Workflow**~~ — ✅ All items implemented in prior sessions
3. ~~**Stream 4: SPARK Enrichment Pass 3**~~ — ✅ All items implemented and executed in prior sessions

### Phase 2: Code Quality (After Phase 1) — COMPLETE ✅

**Streams 2A + 2B** -- All verified complete except 2B.3 (P3 orphan pagination).

4. ~~**Stream 2A: Bug Fixes**~~ — ✅ All 5 items already implemented in prior sessions
5. ~~**Stream 2B: Frontend Gaps**~~ — ✅ All 5 items done (orphan pagination added v3.29.0 @189)

### Phase 3: Data Integration Docs (Parallel with Phase 2)

**Stream 6A** -- Documentation sprint, no code, no blockers.

6. **Stream 6A: Documentation Overhaul** -- DATA_SOURCE_REGISTRY.md rebuild, CARRIER_INTEGRATION_MATRIX.md. ~3 hours.

### Phase 4: Comms Intake + Validation (After JDM actions)

**Streams 7 + 8** -- API validation + communication intake sync.

7. **Stream 8: Comms Intake Sync** -- Twilio, SendGrid, Meet recording intake. Depends on existing MCP tools (already live). ~4-5 hours.
8. **Stream 7: API Validation** -- WhitePages Pro, Google Places, NeverBounce. Depends on JDM confirming API access + enabling GCP APIs. ~12-16 hours.

### Phase 5: Carrier Integrations (JDM vendor enrollment dependent)

**Stream 6B-6D** -- Communication archives, carrier APIs, integration dashboard.

9. **Stream 6B: Communication Archives** -- Chat, Jira, GHL legacy. Depends on JDM OAuth + folder IDs + exports.
10. **Stream 6C: Carrier Integration Framework** -- DTCC, Schwab, Gradient, Blue Button. Depends on JDM vendor enrollments.
11. **Stream 6D: Integration Dashboard** -- UI for all integration sources. Depends on 6B + 6C.

### Phase 6: Cleanup (When ready)

**Streams 2C + 5** -- Maintainability + blocked CoF data.

12. **Stream 2C: Maintainability** -- Archive FIX_ functions, pin RAPID_CORE, consolidate redundancies. Depends on JDM decisions Q1/Q2/Q4.
13. **Stream 5: CoF Policy Details** -- Blocked on CoF response. Execute immediately when data arrives.

---

## JDM Action Items (Updated 2026-03-03)

> These are the ONLY things blocking forward progress. Everything else Claude handles.

### Do Now (5 minutes each)

| # | Action | Why | How |
|---|--------|-----|-----|
| 1 | **Visit Integration Dashboard** | See all sync statuses | Open RAPID_IMPORT URL + `?page=integrations` |
| 2 | **Visit Comms Viewer** | See communication history | Open RAPID_IMPORT URL + `?page=comms` |
| 3 | **Confirm Chat spaces** | Currently syncing all 4 accessible spaces | Tell Claude which to monitor, or "all is fine" |
| 4 | **Verify hygiene triggers** | Auto phone/email validation may not be active | In GAS editor: RAPID_IMPORT → IMPORT_BulkValidation.gs → run `SETUP_HygieneTriggers` |

### Do This Week

| # | Action | Why | How |
|---|--------|-----|-----|
| 4 | **Provide Jira recordings folder ID** | One-time import of historical call recordings | Find the Drive folder, tell Claude the folder ID |
| 5 | **Export GHL comm history** | Archive SMS/call data before GHL decommission | GHL portal → Export call recordings + SMS as CSV → upload to Drive → tell Claude the file ID |
| 6 | **Enable Google Places API** | Free address autocomplete on ProDashX/Sentinel forms | Go to console.cloud.google.com → project 90741179392 → APIs & Services → Enable "Places API" + "Maps JavaScript API" → tell Claude "TCO" |

### Do This Month (Vendor Enrollments)

| # | Action | Why | How |
|---|--------|-----|-----|
| 7 | **Enroll with DTCC I&RS** | Automated life/annuity policy + transaction data feeds | Contact DTCC, enroll for I&RS API access, get credentials |
| 8 | **Enroll Schwab via Gradient** | Automated BD/RIA account + transaction feeds | Ask Gradient for Schwab Advisor Services API enrollment |
| 9 | **Get Gradient API docs** | Automated producer status + policy sync | Confirm timeline with Gradient, get API documentation |
| 10 | **Register Blue Button** | Client-authorized Medicare claims data via CMS | Register at developer.cms.gov for Blue Button sandbox |
| 11 | **Check RBC API via Gradient** | BD custodian data feeds | Ask Gradient about RBC API availability |
| 12 | **DST Vision enrollment** | Mutual fund/variable annuity data aggregation | Enroll through Gradient BD relationship |

### Nothing Needed (Already Live)

| Feature | Status | URL |
|---------|--------|-----|
| Comms intake (Twilio/SendGrid/Meet/Chat) | ✅ Hourly sync running | `?page=comms` |
| Integration Dashboard | ✅ Live | `?page=integrations` |
| Approval batch search | ✅ Live | `?page=approval` (search bar) |
| Pending batch list on home page | ✅ Live | Home page |
| Data validation (phone/email/address) | ✅ Quarterly + 4-hour pipeline | Automated |
| SSN masking (display + edit) | ✅ Live | All approval/reconcile UIs |
| All confirmation dialogs | ✅ Live | Delete, merge, execute all guarded |

---

## Open Questions for JDM

| # | Question | Recommendation | Blocks |
|---|----------|---------------|--------|
| Q1 | Should BoB raw data dump files stay in git? (~13K lines inline in FIX_ functions) | **Archive to Drive folder**, remove from git. Git history preserves them. Cuts IMPORT_Approval.gs from 20K to 7K lines. | Stream 2C.1 |
| Q2 | Should executed FIX_ functions be archived out of active code? | **Yes** -- move to `IMPORT_Archive.gs` (keep in project, just separate file). | Stream 2C.1 |
| Q3 | Should RAPID_API boundary include operational tabs (_CASE_TASKS, _INTAKE_QUEUE)? | **Yes** -- RAPID_API should route ALL MATRIX writes for consistency. | Architecture |
| Q4 | Keep `developmentMode: true` on RAPID_CORE or pin to version? | **Pin to version for production stability**, use HEAD only during active RAPID_CORE dev. | Stream 2C.2 |
| Q5 | Does WhitePages Pro subscription include API access (developer key)? | Check account settings for API key. Portal-only vs API determines Phase 7 scope. | Stream 7.1 |

---

## Source Plans (Archived Reference)

| Plan File | Stream | Status |
|-----------|--------|--------|
| `shiny-whistling-lecun.md` | Streams 1, 2, 7 (Phases 1-5) | PARTIAL -- Phases 1-3 open, Phase 4 research complete |
| `shiny-whistling-lecun-agent-a87c5fb.md` | Stream 7 (vendor research) | RESEARCH COMPLETE |
| `dapper-rolling-glade.md` | Stream 3 (mail workflow) | OPEN |
| `lucky-tumbling-beacon.md` | Stream 4 (SPARK Pass 3) | OPEN |
| `stateless-marinating-hopper.md` | Stream 5 (data quality) | PARTIAL -- Phases 0-5+7 COMPLETE, Phase 6 BLOCKED on CoF |
| `sparkling-nibbling-bird.md` | Stream 6 (data integration) | OPEN |
| `wondrous-snuggling-phoenix.md` | Stream 8 (comms intake) | OPEN -- rpi-comms-mcp + Meet tools DONE, intake sync not started |
