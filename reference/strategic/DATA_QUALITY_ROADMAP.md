# Data Quality, Bulk Actions & Enrichment Roadmap

> **The master plan for clean data, deduplication, bulk operations, and API-powered enrichment across the entire RPI ecosystem.**
>
> Origin: Feb 6, 2026 (NEXT_DATA_QUALITY_HANDOFF.md) + JDM vision outline
> Supersedes: `RAPID_CORE/NEXT_DATA_QUALITY_HANDOFF.md`

---

## The Problem

Data goes in dirty. Existing data is already dirty. Every new source (BoB imports, CRM syncs, document extraction, mail, email, commission statements, carrier feeds) compounds duplication and inconsistency exponentially.

Training review (Feb 2026) proved it: Francesca Damasceno got 9+ duplicate client rows from repeated extractions. Every extraction creates new records instead of matching existing ones.

Three layers need to happen:
1. **Back-End** — Auto-normalize, dedup, and reconcile on every write
2. **Back-End Bulk** — ACF/Client/Account batch operations + PDF processing
3. **Front-End** — ProDash bulk actions, enrichment center, API integrations

---

## 1. Back-End: Write Path Quality (RAPID_CORE)

All writes flow through RAPID_API -> RAPID_CORE. Fix it once in CORE, every platform benefits.

```
Source                          -> RAPID_API      -> RAPID_CORE         -> MATRIX
                                   (gateway)        (engine)             (sheets)
----------------------------------------------------------------------
Approval UI (DONE button)      -> callRapidAPI_() -> CORE.updateRow()   -> Sheet
PRODASH inline edits           -> callRapidAPI()  -> CORE.updateRow()   -> Sheet
SENTINEL v2 inline edits       -> callRapidAPI_() -> CORE.updateRow()   -> Sheet
RAPID_IMPORT batch imports     -> callRapidAPI_() -> CORE.insertRow()   -> Sheet
Watcher extractions            -> callRapidAPI_() -> CORE.insertRow()   -> Sheet
```

### What EXISTS but isn't wired

**CORE_Normalize.gs** (628 lines) — All working, none called during writes:

| Function | What It Does |
|----------|-------------|
| `normalizeCarrierName(raw)` | Carrier alias map + `_CARRIER_MASTER` lookup + title case fallback |
| `normalizeIMOName(raw)` | IMO alias map + `_IMO_MASTER` lookup |
| `normalizeProductType(raw)` | Product type standardization (MAPD, FIA, MedSupp, etc.) |
| `normalizeName(first, last)` | Handles McName, O'Name patterns, title case |
| `normalizePhone(raw)` | Formats to `(XXX) XXX-XXXX` |
| `normalizeDate(raw)` | Parses MM/DD/YYYY, YYYY-MM-DD, MM-DD-YYYY -> `YYYY-MM-DD` |
| `normalizeEmail(raw)` | Lowercase + trim |
| `normalizeState(raw)` | Full state name -> 2-letter code |
| `normalizeZip(raw)` | 5-digit or ZIP+4 formatting |
| `normalizeAmount(raw)` | Strip `$,` -> number |

**CORE_Match.gs** (515 lines) — All working, none called during inserts:

| Function | What It Does |
|----------|-------------|
| `matchClient(criteria)` | Fuzzy match on name+DOB, SSN last 4, phone+last name, email |
| `matchAccount(criteria)` | Exact policy number match, client+carrier+date match |
| `matchAgent(criteria)` | NPN exact match, email match, name match |
| `fuzzyMatch(str1, str2)` | Levenshtein distance -> 0-100 similarity score |
| `findDuplicates(records, fields, threshold)` | Bulk duplicate scanner |
| `batchMatch(tabName, records, matchFn)` | Batch matching against MATRIX |

### Phase 1: Auto-Normalization in Write Path

**Status**: NOT STARTED
**Priority**: HIGH — This is the fire
**Effort**: Small (functions exist, just wire them)
**Impact**: Every write from every project gets clean data. Zero caller changes.
**File**: `CORE_Database.gs`

Add `normalizeData_(tabName, data)` private function + `FIELD_NORMALIZERS` constant. Wire into `insertRow()` and `updateRow()`.

```javascript
const FIELD_NORMALIZERS = {
  // Name fields
  first_name: 'name', last_name: 'name', preferred_name: 'name',
  middle_name: 'name', spouse_name: 'name',
  child_1_name: 'name', child_2_name: 'name', child_3_name: 'name',
  child_4_name: 'name', child_5_name: 'name', child_6_name: 'name',

  // Phone fields
  phone: 'phone', cell_phone: 'phone', alternate_phone: 'phone',
  spouse_phone: 'phone', contact_phone: 'phone',

  // Email fields
  email: 'email', secondary_email: 'email', spouse_email: 'email',
  contact_email: 'email',

  // Date fields
  dob: 'date', spouse_dob: 'date', effective_date: 'date',
  wedding_date: 'date', created_at: 'skip', updated_at: 'skip',
  source_date: 'date', deleted_at: 'skip',

  // Address fields
  state: 'state', mailing_state: 'state',
  zip: 'zip', mailing_zip: 'zip',

  // Industry fields
  carrier_name: 'carrier',
  product_type: 'product',

  // Currency fields
  amount: 'amount', premium: 'amount', scheduled_premium: 'amount',
  net_worth: 'amount', investable_assets: 'amount',
  household_income: 'amount', annual_income: 'amount',
};
```

### Phase 2: Pre-Write Dedup Matching

**Status**: NOT STARTED
**Priority**: HIGH — Stops the bleeding
**Effort**: Medium (callers must handle new response types)
**Files**: `CORE_Database.gs` + `CORE_Match.gs`

Before `insertRow()` appends, call the appropriate matcher. Return confidence-tiered responses:

| Tier | Score | Trigger | Action |
|------|-------|---------|--------|
| **Exact** | 100 | NPN match, policy number, SSN last 4 + name | Auto-merge, return existing ID |
| **Strong** | 85-99 | Name + DOB + state, email exact, phone + last name | Auto-merge, log notification |
| **Possible** | 70-84 | Name only, partial address match | Return `REVIEW_NEEDED`, caller decides |
| **None** | <70 | No meaningful match | Insert new record |

Dedup by table:

| Tab | Match Criteria | Exact Match Key |
|-----|---------------|-----------------|
| `_CLIENT_MASTER` | name+DOB, SSN last 4, email, phone+last name | SSN last 4 + last name |
| `_AGENT_MASTER` | NPN, email, name+state | NPN |
| `_ACCOUNT_*` | policy number, client_id+carrier+product | Policy number |
| `_REVENUE_MASTER` | account_id+date+amount+type | (no exact -- always insert) |

Callers handle responses: `MERGED` / `MERGED_NOTIFY` / `REVIEW_NEEDED` / `INSERTED`

### Phase 3: Reconciliation Jobs

**Status**: NOT STARTED
**Priority**: MEDIUM — Cleans the existing mess
**Effort**: Medium (new file + scheduled triggers)
**File**: `CORE_Reconcile.gs` (NEW)

| Function | Purpose |
|----------|---------|
| `reconcileClients()` | Scan `_CLIENT_MASTER` for duplicate pairs, produce merge candidates |
| `reconcileAccounts()` | Scan all `_ACCOUNT_*` tabs for orphaned/duplicate accounts |
| `reconcileAgents()` | Scan `_AGENT_MASTER` for duplicate NPNs, fuzzy name matches |
| `normalizeExistingData(tabName)` | Run all normalizers on every row in a tab (backfill) |
| `mergeRecords(tabName, keepId, mergeId)` | Merge two records: keep one, update foreign keys, soft-delete other |

Produces reconciliation report in `_RECONCILIATION_LOG` tab with duplicate pairs, confidence scores, auto-merged count, human review needed count.

---

## 2. Back-End Bulk Actions

Batch operations that go beyond single-record CRUD.

### 2.1 ACF — Create / Update / De-Dupe

| Operation | What It Does |
|-----------|-------------|
| **Create** | Auto-generate ACF folder structure for new client (specialist subfolder, standard naming) |
| **Update** | Re-file documents when client data changes (name correction, specialist reassignment) |
| **De-Dupe** | Scan for duplicate ACF folders, merge contents, update Drive references in MATRIX |

### 2.2 CLIENT — Create / Update / De-Dupe

| Operation | What It Does |
|-----------|-------------|
| **Create** | Insert new client with full normalization + dedup check (Phase 1+2) |
| **Update** | Bulk update client fields (address changes, phone updates) with normalization |
| **De-Dupe** | Phase 3 reconciliation — find duplicate clients, merge records, consolidate accounts |

### 2.3 ACCOUNT — Create / Update / De-Dupe

| Operation | What It Does |
|-----------|-------------|
| **Create** | Insert accounts with policy number dedup, client_id linking |
| **Update** | Bulk update account values (balance refreshes, status changes) |
| **De-Dupe** | Scan all `_ACCOUNT_*` tabs for duplicate policy numbers, orphaned accounts |

### 2.4 Extract / Label / File PDFs

| Operation | What It Does |
|-----------|-------------|
| **Extract** | Claude Vision extraction via watcher (already built) |
| **Label** | Document taxonomy classification (52 types in `_DOCUMENT_TAXONOMY`, already built) |
| **File** | Auto-route to correct ACF subfolder based on label + specialist (already built) |
| **Bulk Re-File** | Re-process documents that were filed before labeling existed |

---

## 3. Front-End Bulk Actions (ProDash)

### 3.1 Spouse + Kits <> Beni Center Run

Batch operation that:
- Scans clients for missing spouse data
- Cross-references beneficiary designations across all account types
- Flags mismatches (spouse not listed as beni, outdated beni after divorce, etc.)
- Generates kit packages for clients needing beni updates

### 3.2 Data Enrichment Center (NEW)

A ProDash UI module that orchestrates data quality through MCP-Hub.

#### 3.2.1 Proactive Runs — "Don't have XYZ, fire automation"

Scan MATRIX for gaps and auto-fill:
- Client has no phone -> WhitePages lookup
- Client has no email -> data append
- Address not verified -> Google Address Verification
- Missing DOB -> flag for manual collection
- Account missing balance -> flag for statement request

#### 3.2.2 Reactive Runs — "Not Updated Since X, fire automation"

Time-based triggers:
- Account balance not updated in 6+ months -> flag for refresh
- Client address not verified in 12+ months -> re-verify
- Phone number not validated in 12+ months -> re-validate
- Medicare plan not reviewed since last AEP -> flag

#### 3.2.3 Client-Facing APIs (Authorization Required)

APIs that require client consent/authentication:

**Mastercard (Open Banking)**
| Category | Data |
|----------|------|
| Bank | Checking/savings accounts, balances, transactions |
| Insurance | Policy data, coverage details |
| Investment | Brokerage accounts, holdings, performance |
| Liabilities | Mortgages, loans, credit cards, balances |

**ID.ME (Identity Verification Gateway)**
| Service | Data |
|---------|------|
| CMS Blue Button | Medicare claims, coverage history, Part D utilization |
| CMS Carrier Connect | Direct carrier data exchange |
| IRS | Tax transcripts, income verification |
| SSA | Social Security benefits, earnings history |

**Health Data Platforms (FHIR)**
| Platform | Coverage |
|----------|----------|
| EPIC | MyChart data — conditions, medications, encounters |
| CERNER / Oracle | Health data — labs, imaging, clinical notes |
| Athena | Practice data — visits, billing, prescriptions |

#### 3.2.4 Data-Facing APIs (No Client Auth Needed)

APIs RPI calls directly for data quality:

| API | Purpose | Where |
|-----|---------|-------|
| WhitePages | Phone/name/address verification + append | MCP-Hub batch job |
| Google Address Verification | Standardize addresses to USPS format | RAPID_API endpoint |
| Email Verification | Validate deliverability, catch typos | MCP-Hub batch job |
| Phone Type / Validation | Mobile vs landline, carrier lookup, active status | MCP-Hub batch job |

---

## Files to Modify

### Phase 1 (Normalization)
| File | Project | Change |
|------|---------|--------|
| `CORE_Database.gs` | RAPID_CORE | Add `normalizeData_()`, `FIELD_NORMALIZERS`, wire into `insertRow()`/`updateRow()` |

### Phase 2 (Dedup)
| File | Project | Change |
|------|---------|--------|
| `CORE_Database.gs` | RAPID_CORE | Add `checkForDuplicate_()`, wire into `insertRow()` |
| `CORE_Match.gs` | RAPID_CORE | Enhance matchers, add confidence tiers |
| `API_Import.gs` | RAPID_API | Handle `REVIEW_NEEDED` response from CORE |
| `API_Client.gs` | RAPID_API | Handle `MERGED` response from CORE |
| `IMPORT_Approval.gs` | RAPID_IMPORT | Handle `REVIEW_NEEDED` in `executeApprovedBatch_()` |

### Phase 3 (Reconciliation)
| File | Project | Change |
|------|---------|--------|
| `CORE_Reconcile.gs` | RAPID_CORE | **NEW** — Batch reconciliation jobs |

### Enrichment Center (Future)
| File | Project | Change |
|------|---------|--------|
| New enrichment MCP servers | MCP-Hub | WhitePages, address verification, phone validation |
| New enrichment endpoints | RAPID_API | `/enrich/address`, `/enrich/phone`, `/enrich/email` |
| Enrichment Center UI | PRODASH | New module for proactive/reactive runs |

---

## Build Order

| # | What | Impact | Effort | Status |
|---|------|--------|--------|--------|
| 1 | Wire `CORE_Normalize` into write path | Every write auto-cleans | Small | NOT STARTED |
| 2 | Wire `CORE_Match` into write path | No new duplicates | Medium | NOT STARTED |
| 3 | Reconciliation batch jobs | Clean existing data | Medium | NOT STARTED |
| 4 | Back-End Bulk Actions (ACF/Client/Account) | Batch operations | Medium | PARTIAL (Extract/Label/File done) |
| 5 | Twilio migration (Jira + GHL archives) | Unified comm history | Large | NOT STARTED |
| 6 | Carrier + IMO API/Webhook channels | Direct data feeds | Large | NOT STARTED |
| 7 | Data-Facing API integrations | Auto-fill gaps | Medium | NOT STARTED |
| 8 | ProDash Enrichment Center UI | User-facing data quality | Large | NOT STARTED |
| 9 | Client-Facing API integrations | Full financial picture | Large | NOT STARTED |

**Phase 1 is the fire.** Small, low-risk, instant impact on every write in the system.

---

## Risks

| Risk | Mitigation |
|------|-----------|
| Normalization changes existing behavior | Phase 1 only formats (doesn't reject). Run `normalizeExistingData()` to align existing data. |
| Dedup false positives | Confidence tiers + `REVIEW_NEEDED` for uncertain matches. Only auto-merge on exact keys. |
| Performance impact on writes | Normalization is fast (string ops). Matching is slower — use caching, index on key fields. |
| Callers not handling new responses | Phase 2 requires updating RAPID_API handlers. Phase 1 requires zero caller changes. |
| Client-facing APIs require consent flows | Build consent management into ProDash before enabling Mastercard/ID.ME integrations. |
| Health data APIs require compliance | HIPAA BAAs needed for EPIC/CERNER/Athena. PHI handling rules already in place. |

---

## Testing Plan

### Phase 1 Test
1. Run `TEST_CORE_Normalize()` — verify all normalizers work
2. Insert client with dirty data: `{first_name: 'JOHN', phone: '5551234567', state: 'Iowa', email: 'JOHN@EMAIL.COM'}`
3. Verify stored as: `{first_name: 'John', phone: '(555) 123-4567', state: 'IA', email: 'john@email.com'}`
4. Update client with dirty data — verify same normalization
5. Verify timestamps and UUIDs are NOT normalized (skip list)

### Phase 2 Test
1. Insert client: `{first_name: 'John', last_name: 'Smith', dob: '1960-01-15'}`
2. Insert same client again — verify `action: 'MERGED'`, same `client_id` returned
3. Insert similar client: `{first_name: 'Jon', last_name: 'Smith', dob: '1960-01-15'}` — verify `action: 'REVIEW_NEEDED'`
4. Insert different client: `{first_name: 'Jane', last_name: 'Doe'}` — verify `action: 'INSERTED'`
5. Test agent dedup with NPN exact match
6. Test account dedup with policy number exact match

---

## 4. Intake Source Expansion (RAPID_IMPORT)

The current 4 intake channels (SPC, MAIL, EMAIL, MEET) are just the beginning. Two major source categories are coming, and all new sources flow through the same Training Lab phases (Extraction -> Routing -> Corrections -> Production -> Graduated).

### 4.1 Unified Communications — Twilio Migration

**What**: Migrate all client communications from Jira + GoHighLevel into an integrated Twilio solution in ProDash X.

**Data to migrate**:

| Source | Data Types |
|--------|-----------|
| **Jira (archive)** | Text messages, inbound call recordings, outbound call recordings, call logs |
| **GoHighLevel (current)** | Text messages, inbound call recordings, outbound call recordings, call logs, conversation threads |

**Target**: ProDash X with native Twilio integration for:
- Inbound / outbound calling
- SMS / MMS messaging
- Call recording + transcription
- Conversation history (unified timeline per client)

**RAPID_IMPORT role**:
- New intake channel: `COMM_ARCHIVE` — bulk import historical comms from Jira + GHL exports
- New intake channel: `TWILIO_WEBHOOK` — real-time inbound from Twilio (calls, texts, recordings)
- Recordings -> Claude transcription -> extraction -> Training Lab phases
- All comm data links to `client_id` in `_CLIENT_MASTER`

### 4.2 Carrier APIs + Webhooks

**What**: Direct data feeds from insurance carriers — both pull (API) and push (webhook).

**Sources**:

| Source | Side | Data Types |
|--------|------|-----------|
| **Carrier APIs** (pull) | All lines | Policy status, values, beneficiaries, billing, claims |
| **Carrier Webhooks** (push) | All lines | Status changes, issue notifications, commission updates |

**RAPID_IMPORT role**:
- New intake channel: `CARRIER_API` — scheduled pulls from carrier portals
- New intake channel: `CARRIER_WEBHOOK` — real-time push notifications
- Data flows through normalization (CORE Phase 1) + dedup (CORE Phase 2) before MATRIX writes
- Carrier-specific field mappings needed (each carrier has different data formats)
- All carrier data runs through Training Lab to validate extraction quality

### 4.3 IMO APIs + Webhooks

**What**: Data feeds from RPI's upline IMOs who aggregate carrier data.

**Sources**:

| IMO | Lines | Data Types |
|-----|-------|-----------|
| **Spark** | Medicare (MAPD, MedSupp, PDP) | Enrollments, commissions, policy status, renewals, carrier notifications |
| **Gradient** | Life, Annuity, Broker Dealer, RIA | Policy data, commission statements, production reports, compliance alerts |

**RAPID_IMPORT role**:
- New intake channel: `IMO_API` — scheduled pulls from Spark + Gradient portals
- New intake channel: `IMO_WEBHOOK` — real-time push from IMO systems
- IMO data is often pre-aggregated (multiple carriers in one feed) — needs carrier normalization
- Commission data routes to `_REVENUE_MASTER` via SENTINEL
- Policy data routes to `_ACCOUNT_*` tabs via PRODASH
- All IMO data runs through Training Lab phases

### Intake Channel Summary (Current + Planned)

| Channel | Source | Status | Priority |
|---------|--------|--------|----------|
| `SPC_INTAKE` | Specialist Drive folders | DEPLOYED | - |
| `MAIL` | Scanned physical mail | DEPLOYED | - |
| `EMAIL` | Gmail inboxes | DEPLOYED | - |
| `MEET_TRANSCRIPT` | Google Meet recordings | DEPLOYED | - |
| `COMM_ARCHIVE` | Jira + GHL historical export | PLANNED | HIGH |
| `TWILIO_WEBHOOK` | Real-time Twilio events | PLANNED | HIGH |
| `CARRIER_API` | Carrier portal pulls | PLANNED | MEDIUM |
| `CARRIER_WEBHOOK` | Carrier push notifications | PLANNED | MEDIUM |
| `IMO_API` | Spark + Gradient pulls | PLANNED | MEDIUM |
| `IMO_WEBHOOK` | IMO push notifications | PLANNED | MEDIUM |

---

## Parallel Execution: RAPID_CORE + RAPID_IMPORT

These two tracks run simultaneously. The only sync point is CORE Phase 2.

```
RAPID_CORE Track                         RAPID_IMPORT Track
(Data Quality Engine)                    (Training + Intake Finalization)
─────────────────────                    ─────────────────────────────────
Phase 1: Wire normalizers                Build _EXTRACTION_TRAINING tab
  into insertRow()/updateRow()           Store JDM's corrections as corpus
  (zero caller changes)                  Continue training review (141 pending)
         |                                        |
Phase 1 deploys ────────────────────────→ Re-extract pending batches
         |                                (data now auto-normalized)
         v                                        |
Phase 2: Wire dedup                               v
  into insertRow()                       Update executeApprovedBatch_()
  (new response types)                   to handle MERGED / REVIEW_NEEDED
         |                                        |
Phase 2 deploys ────────────────────────→ Phase 4: Execute for real MATRIX writes
         |                                (normalization + dedup catches the mess)
         v                                        |
Phase 3: Reconcile existing data                  v
  (batch cleanup of _CLIENT_MASTER etc.) Graduate training corpus to gold standard
```

**Sync Points**:
- CORE Phase 1 → triggers IMPORT re-extraction (clean data = fewer corrections)
- CORE Phase 2 → triggers IMPORT code update (handle dedup responses)
- Everything else runs independently

**Handoff docs**:
- RAPID_CORE: This document (`DATA_QUALITY_ROADMAP.md`)
- RAPID_IMPORT: `RAPID_IMPORT/HANDOFF_RAPID_IMPORT_FINALIZATION.md`

---

*This is the foundation that makes "The Machine" trustworthy at scale. Clean data in, no duplicates, enriched over time.*
