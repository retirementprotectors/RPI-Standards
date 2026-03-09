> ARCHIVED: Consolidated into prodashx-platform-roadmap.md (Stream 7: Communications Wiring) on 2026-03-08

# COMMS WIRING — Top to Bottom

## Context

PRODASHX communications are **70% done**. CLIENT360 + Comms Hub already send email/SMS/voice via RAPID_COMMS, log to `_COMMUNICATION_LOG`, and display history. What's missing: campaign sends are stubs, no enrollment/queue system, DND enforcement is absent, and delivery status doesn't display in the UI. This plan wires the remaining 30% — from campaign execution through automated drip sequences to delivery tracking.

**Separate scope (other session):** Pipeline stages, Kanban, Casework, Medicare Rec, Rules Engine, Call Transcription. Those are PRODASHX platform readiness — not comms wiring.

**JDM prerequisites (DONE):**
- RAPID_COMMS library added to PRODASHX ✅
- RAPID_COMMS library added to RAPID_API ✅

---

## Architecture (Current → Target)

```
TODAY:
  PRODASHX CLIENT360 ──→ RAPID_COMMS ──→ Twilio/SendGrid  ✅ (ad-hoc sends work)
  RAPID_API stubs ──→ logs "stub" to _CAMPAIGN_SEND_LOG    ❌ (campaigns don't actually send)
  Webhooks ready ──→ waiting for external_ids               ✅ (handlers built, nothing to match)
  DND UI ──→ saves to _CLIENT_MASTER                        ✅ (data saved, never checked)

TARGET:
  PRODASHX Campaign UI ──→ Enroll contacts ──→ _CAMPAIGN_ENROLLMENTS + _QUEUED_SENDS
       ↓                                              ↓
  Queue processor (15-min trigger)              RAPID_API send functions
       ↓                                              ↓
  RAPID_COMMS.sendEmail/SMS/initiateCall()      external_id stored
       ↓                                              ↓
  Twilio/SendGrid ──→ Webhook callbacks ──→ _CAMPAIGN_SEND_LOG status updates
       ↓
  CLIENT360 shows delivery status (sent → delivered → opened)
  DND checked BEFORE every send
```

---

## What Already Exists (DO NOT REBUILD)

| Component | Location | Status |
|-----------|----------|--------|
| `uiSendClientEmail/SMS/Call()` | `PRODASH_CLIENT360.gs:595-723` | LIVE — calls RAPID_COMMS directly |
| `uiSendComm()` | `PRODASH_Communications.gs:79-190` | LIVE — unified dispatcher |
| `formatPhoneE164_()` | `PRODASH_CLIENT360.gs:810-817` | LIVE — phone normalization |
| `escapeXml_()` | `PRODASH_CLIENT360.gs:822-829` | LIVE — TwiML safety |
| SendGrid webhook | `API_Webhook.gs:61-127` | LIVE — maps events to statuses |
| Twilio SMS webhook | `API_Webhook.gs:141-179` | LIVE — maps delivery statuses |
| Twilio Voice webhook | `API_Webhook.gs:192-236` | LIVE — maps call statuses |
| `updateSendLogByExternalId_()` | `API_Webhook.gs:243-280` | LIVE — finds row by external_id |
| `updateCommLogByExternalId_()` | `API_Webhook.gs:282-300` | LIVE — updates _COMMUNICATION_LOG |
| `/comms/log`, `/comms/history`, `/comms/stats` | `API_Comms.gs:1-240` | LIVE — full logging endpoints |
| `getTargetContacts_()` | `API_CampaignSend.gs:125-318` | LIVE — 10-filter targeting engine |
| `logCampaignSend_()` | `API_CampaignSend.gs` | LIVE — appends to _CAMPAIGN_SEND_LOG |
| DND UI (3-mode + checkboxes) | `PRODASHX Index.html:637-661` | LIVE — saves to _CLIENT_MASTER |
| DND save functions | `Scripts.html:3471-3546` | LIVE — `setDndMode()`, `saveDndChannel()` |
| `_CAMPAIGN_SEND_LOG` schema | `CORE_Database.gs` | LIVE — 14 columns |
| `_COMMUNICATION_LOG` schema | `CORE_Database.gs` | LIVE — in RAPID_MATRIX |
| `_CAMPAIGNS` schema | `CORE_Database.gs` | LIVE — 61 columns with triggers |
| `_TEMPLATES` schema | `CORE_Database.gs` | LIVE — touchpoint → block slot mapping |
| Campaign CRUD endpoints | `API_Campaign.gs` | LIVE — full REST API |

---

## Work Plan — 3 Waves

### WAVE 1: Foundation (parallel — 4 items, ~1 session)

#### 1A. RAPID_CORE — Add enrollment + queue schemas

**File:** `~/Projects/RAPID_TOOLS/RAPID_CORE/CORE_Database.gs`

Add to `TABLE_ROUTING`:
```javascript
'_CAMPAIGN_ENROLLMENTS': 'PRODASH',
'_QUEUED_SENDS': 'PRODASH',
```

Add to `TAB_SCHEMAS`:
```javascript
'_CAMPAIGN_ENROLLMENTS': [
  'enrollment_id', 'campaign_id', 'contact_id', 'contact_name', 'contact_email', 'contact_phone',
  'enrolled_by', 'enrolled_at', 'start_date', 'current_step', 'total_steps',
  'next_send_at', 'status', 'completed_at', 'created_at', 'updated_at'
],
'_QUEUED_SENDS': [
  'queued_send_id', 'enrollment_id', 'campaign_id', 'contact_id',
  'step_index', 'scheduled_for', 'channel', 'subject', 'content',
  'template_id', 'status', 'actual_sent_at', 'send_id', 'external_id',
  'error_message', 'created_at'
]
```

**Deploy:** `clasp push` + `clasp version` only (library, no web deploy)

#### 1B. RAPID_API — Wire 3 send stubs to RAPID_COMMS

**File:** `~/Projects/RAPID_TOOLS/RAPID_API/API_CampaignSend.gs`

Replace each stub function. Pattern for all three:
1. Look up contact from `_CLIENT_MASTER` via `getProdashRowById_()` — get email/phone
2. Check DND flags (`dnd_email`, `dnd_sms`, `dnd_phone`) — skip if blocked
3. Call RAPID_COMMS method (sendEmail/sendSMS/initiateCall)
4. Extract external_id from response (messageId / messageSid / callSid)
5. Log to `_CAMPAIGN_SEND_LOG` with `external_id`, `provider`, `status: 'sent'`
6. Log to `_COMMUNICATION_LOG` via `callRapidAPI_('comms/log', ...)` — same pattern as CLIENT360
7. Return structured response

**`sendCampaignEmail_(contactId, campaignId, content, subject)`:**
- Lookup `email` from client record
- Guard: `if (!email)` → return error
- Guard: `if (client.dnd_email === 'true' || client.dnd_all === 'true')` → return `{ success: false, error: 'DND_EMAIL' }`
- Call `RAPID_COMMS.sendEmail({ to: email, subject, html: content })`
- Store `external_id = result.data.messageId`, `provider = 'sendgrid'`

**`sendCampaignSMS_(contactId, campaignId, content)`:**
- Lookup `phone` from client record, format with `formatPhoneE164_()` (copy from PRODASH or inline)
- Guard: `if (!phone)` → return error
- Guard: `if (client.dnd_sms === 'true' || client.dnd_all === 'true')` → return `{ success: false, error: 'DND_SMS' }`
- Call `RAPID_COMMS.sendSMS({ to: phone, body: content, statusCallback: webhookUrl + '/webhook/twilio/sms' })`
- Store `external_id = result.data.messageSid`, `provider = 'twilio'`

**`sendCampaignVMDrop_(contactId, campaignId, audioUrl)`:**
- Lookup `phone` from client record
- Guard: `if (!phone)` → return error
- Guard: `if (client.dnd_phone === 'true' || client.dnd_all === 'true')` → return `{ success: false, error: 'DND_PHONE' }`
- Call `RAPID_COMMS.initiateCall({ to: phone, twiml: '<Response><Play>' + audioUrl + '</Play></Response>', statusCallback: webhookUrl + '/webhook/twilio/voice' })`
- Store `external_id = result.data.callSid`, `provider = 'twilio'`

**`sendCampaignDirectMail_()` — KEEP AS STUB** (Lob integration future)

**Also add:**
- `var WEBHOOK_BASE_URL = PropertiesService.getScriptProperties().getProperty('WEBHOOK_BASE_URL') || '';`
- `formatPhoneE164_()` helper (same logic as PRODASH version)
- JDM one-time: Set `WEBHOOK_BASE_URL` Script Property in RAPID_API to the web app URL

**Also update `appsscript.json`** to include RAPID_COMMS library (sync local file with what JDM added in editor):
```json
{ "userSymbol": "RAPID_COMMS", "libraryId": "1G-yWr58E9aJ3DWNRasHtFHXGzg-dTykBtvtxrU8gXIXRZrik2V4a7_F7", "version": "3", "developmentMode": true }
```

#### 1C. PRODASHX — Add DND enforcement to send path

**File:** `~/Projects/PRODASHX_TOOLS/PRODASHX/PRODASH_CLIENT360.gs`

Add DND check at the top of each send function:
- `uiSendClientEmail()` — check `client.dnd_email === 'true' || client.dnd_all === 'true'`
- `uiSendClientSMS()` — check `client.dnd_sms === 'true' || client.dnd_all === 'true'`
- `uiInitiateClientCall()` — check `client.dnd_phone === 'true' || client.dnd_all === 'true'`
- Return `{ success: false, error: 'Client has opted out of [channel] communications' }`

**File:** `~/Projects/PRODASHX_TOOLS/PRODASHX/PRODASH_Communications.gs`
- Same DND check in `uiSendComm()` before routing to RAPID_COMMS

**Frontend (no change needed)** — `sendCommsMessage()` already handles `response.success === false` with `showToast(response.error, 'error')`.

#### 1D. RAPID_API — Webhook URL configuration

**JDM one-time action:** In RAPID_API Script Properties, set:
```
WEBHOOK_BASE_URL = https://script.google.com/macros/s/AKfycbwaCzn-U1arJn17b4s2afF8ZIGJTs-Uf5PdA5t63o8Rx0hLNXuzZD4SJs7IJ0GLnaFb/exec
```

(The Primary deployment URL — webhooks hit the public endpoint, not the Workspace one)

---

### WAVE 2: Enrollment Engine (~2 sessions)

#### 2A. RAPID_API — Enrollment endpoint

**File:** `~/Projects/RAPID_TOOLS/RAPID_API/API_CampaignSend.gs` (add functions)

**New: `enrollContacts_(campaignId, contactIds, startDate, enrolledBy)`**
- Load campaign from `_CAMPAIGNS` by `campaign_id`
- Load templates from `_TEMPLATES` where `campaign_id` matches, ordered by `touchpoint_day`
- For each contact:
  - Create `_CAMPAIGN_ENROLLMENTS` record: enrollment_id, campaign_id, contact_id, enrolled_by, start_date, current_step=0, total_steps=templates.length, status='active'
  - For each template touchpoint:
    - Calculate `scheduled_for = startDate + touchpoint_day * 86400000`
    - Assemble content from content blocks (reuse C3's assembly pattern or keep simple: just store template_id, resolve at send time)
    - Create `_QUEUED_SENDS` record: queued_send_id, enrollment_id, campaign_id, contact_id, step_index, scheduled_for, channel, template_id, status='queued'
- Return `{ success: true, data: { enrolled: contactIds.length, totalSends: queuedCount } }`

**New route in Code.gs:**
- `POST /campaign/enroll` → `enrollContacts_()`
- `GET /campaign/enrollments/{campaign_id}` → list enrollments for a campaign
- `GET /campaign/queue/{campaign_id}` → list queued sends for a campaign

#### 2B. PRODASHX — Campaign views + enrollment UI

**New file:** `~/Projects/PRODASHX_TOOLS/PRODASHX/PRODASH_Campaigns.gs`

Functions (all read from C3 data or PRODASH_MATRIX):
- `uiGetCampaignsForUI()` — list campaigns with status/type/engine filters
- `uiGetCampaignDetailForUI(campaignId)` — campaign + templates/touchpoints
- `uiGetTargetPreviewForUI(campaignId)` — calls `getTargetContacts_()` via RAPID_API, returns count + sample
- `uiEnrollContactsForUI(campaignId, startDate)` — calls enrollment endpoint
- `uiGetSendHistoryForUI(campaignId)` — reads `_CAMPAIGN_SEND_LOG` for campaign
- `uiGetEnrollmentStatsForUI(campaignId)` — enrollment counts + send status breakdown

**Frontend (PRODASHX Index.html):**
- "Campaigns" section in Sales Center nav
- Campaign list grid: filterable by status, type, engine
- Campaign detail view: sequence timeline (touchpoints with day offset, channel badge, content preview)
- Target preview: "X contacts match" with sample list
- "Enroll Contacts" button → confirmation modal with start date picker
- Send history table: contact name, channel, status badge (sent/delivered/bounced/failed), timestamp
- Campaign dashboard card: enrolled count, sends completed, pending, next scheduled

---

### WAVE 3: Automation + Status UI (~1 session)

#### 3A. RAPID_API — Queue processor

**File:** `~/Projects/RAPID_TOOLS/RAPID_API/API_CampaignSend.gs` (add function)

**New: `processQueuedSends_trigger()`**
- Query `_QUEUED_SENDS` where `status = 'queued'` AND `scheduled_for <= now()`
- Limit: 50 per execution (avoid GAS 6-min timeout)
- For each queued send:
  - Load enrollment from `_CAMPAIGN_ENROLLMENTS`
  - Skip if enrollment status !== 'active'
  - Resolve content: load template → assemble from content blocks (or use pre-assembled content if stored)
  - Route by channel:
    - `email` → `sendCampaignEmail_(contactId, campaignId, content, subject)`
    - `sms` → `sendCampaignSMS_(contactId, campaignId, content)`
    - `vm` → `sendCampaignVMDrop_(contactId, campaignId, audioUrl)`
  - Update queued send: `status = 'sent'`, `actual_sent_at = now()`, `send_id` from log, `external_id` from provider
  - If send fails: `status = 'failed'`, `error_message` from response
  - Update enrollment: `current_step++`, calculate `next_send_at` from next queued send
  - If all steps complete: enrollment `status = 'completed'`, `completed_at = now()`
- Return `{ processed, failed, skipped, remaining }`

**Safety:**
- Dedup: skip if `status !== 'queued'` (prevents double-send on retry)
- Error isolation: one failed send doesn't block others (try/catch per send)
- Max 50 per run: prevents timeout, next trigger picks up remainder
- DND checked inside send functions (from Wave 1)

**JDM action (after deploy):** Create trigger in GAS editor:
- Project: RAPID_API | File: API_CampaignSend.gs | Trigger: `processQueuedSends_trigger`, time-driven, every 15 minutes

#### 3B. PRODASHX — Delivery status in CLIENT360

**File:** `~/Projects/PRODASHX_TOOLS/PRODASHX/Scripts.html`

Enhance `renderC360Communications()`:
- Add status badges to comms timeline: sent (blue), delivered (green), opened (teal), clicked (purple), bounced (red), failed (red)
- Show channel icon (email/sms/phone/meet)
- Show timestamp + relative time ("2 hours ago")
- Campaign sends show campaign name badge

**File:** `~/Projects/PRODASHX_TOOLS/PRODASHX/Index.html`
- Status badge CSS classes (reuse existing badge pattern)

---

## Deploy Sequence

**Wave 1:**
1. RAPID_CORE: `clasp push` + `clasp version` (schema additions)
2. RAPID_API: 6-step deploy (BOTH Primary + Workspace)
3. PRODASHX: 6-step deploy

**Wave 2:**
4. RAPID_API: 6-step deploy (BOTH Primary + Workspace)
5. PRODASHX: 6-step deploy

**Wave 3:**
6. RAPID_API: 6-step deploy (BOTH Primary + Workspace)
7. PRODASHX: 6-step deploy
8. JDM: Create `processQueuedSends_trigger` in RAPID_API GAS editor

---

## Verification

**Wave 1 — Send wiring:**
- [ ] `sendCampaignEmail_()` sends real email via SendGrid (test with JDM's email)
- [ ] `sendCampaignSMS_()` sends real SMS via Twilio toll-free (test with JDM's phone)
- [ ] `sendCampaignVMDrop_()` initiates real call (test with JDM's phone)
- [ ] `_CAMPAIGN_SEND_LOG` records include `external_id` + `provider`
- [ ] `_COMMUNICATION_LOG` gets populated on each send
- [ ] Webhook callbacks update status in `_CAMPAIGN_SEND_LOG` (check after delivery)
- [ ] DND-blocked client returns error, no send executed
- [ ] CLIENT360 "Send SMS" to DND-blocked client shows toast error

**Wave 2 — Enrollment:**
- [ ] Campaign list loads in PRODASHX Campaigns section
- [ ] Campaign detail shows touchpoint sequence
- [ ] Target preview shows matching contact count
- [ ] "Enroll Contacts" creates records in `_CAMPAIGN_ENROLLMENTS` + `_QUEUED_SENDS`
- [ ] Send history shows enrolled contacts + statuses

**Wave 3 — Automation + Status:**
- [ ] Queue processor picks up due sends and executes them
- [ ] Failed sends logged with error, don't block others
- [ ] Completed enrollments marked as 'completed'
- [ ] CLIENT360 comms timeline shows delivery status badges
- [ ] Campaign sends show campaign name in timeline

**Edge cases:**
- [ ] Contact with no email → email send returns clear error, not crash
- [ ] Contact with no phone → SMS/voice returns clear error
- [ ] DND_ALL blocks all channels
- [ ] Queue processor handles 50 sends without timeout
- [ ] Duplicate enrollment prevented (same contact + campaign)

---

## Files Modified (Complete List)

| File | Project | Wave | Changes |
|------|---------|------|---------|
| `CORE_Database.gs` | RAPID_CORE | 1 | Add `_CAMPAIGN_ENROLLMENTS` + `_QUEUED_SENDS` to TABLE_ROUTING + TAB_SCHEMAS |
| `API_CampaignSend.gs` | RAPID_API | 1,2,3 | Wire 3 stubs → RAPID_COMMS; add enrollment endpoint; add queue processor |
| `Code.gs` | RAPID_API | 2 | Add enrollment routes |
| `appsscript.json` | RAPID_API | 1 | Add RAPID_COMMS library to dependencies |
| `PRODASH_CLIENT360.gs` | PRODASHX | 1 | Add DND enforcement to 3 send functions |
| `PRODASH_Communications.gs` | PRODASHX | 1 | Add DND enforcement to `uiSendComm()` |
| `PRODASH_Campaigns.gs` (NEW) | PRODASHX | 2 | Campaign list, detail, target preview, enrollment, send history |
| `Code.gs` | PRODASHX | 2 | Add campaign ForUI wrappers + nav entry |
| `Index.html` | PRODASHX | 2,3 | Campaign section UI + delivery status badges |
| `Scripts.html` | PRODASHX | 2,3 | Campaign JS + enhanced comms timeline rendering |

---

## JDM Actions Required

| Action | When | How |
|--------|------|-----|
| Set `WEBHOOK_BASE_URL` in RAPID_API Script Properties | Before Wave 1 deploy | Project: RAPID_API → Script Properties → `WEBHOOK_BASE_URL` = `https://script.google.com/macros/s/AKfycbwaCzn.../exec` |
| Create queue processor trigger | After Wave 3 deploy | Project: RAPID_API \| File: API_CampaignSend.gs \| Trigger: `processQueuedSends_trigger`, time-driven, every 15 min |

---

## Estimated Effort

| Wave | Sessions | What |
|------|----------|------|
| Wave 1 | 1 | Schema + stub wiring + DND + webhook config |
| Wave 2 | 2 | Enrollment engine + campaign UI |
| Wave 3 | 1 | Queue processor + delivery status UI |
| **Total** | **4 sessions** | |
