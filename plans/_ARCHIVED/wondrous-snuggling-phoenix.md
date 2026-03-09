# RPI Communications Integration — Master Architecture Plan

## Context

**The Problem:** GoHighLevel (GHL) is the last external dependency blocking full ecosystem ownership. GHL bundles Twilio + SendGrid behind their platform, controls our contact data, and charges a premium for capabilities we can build natively. Meanwhile, the team uses Zoom (replaceable by Meet), Slack (replaceable by Chat), and has no embedded communications in PRODASH/SENTINEL/RIIMO.

**The Outcome:** Replace GHL with native Twilio + SendGrid + Google Meet + Google Chat + Google People integrations. Every communication — call, text, email, video meeting, chat — originates from and flows back into our ecosystem. C3 campaigns execute natively. The team never leaves their platform.

**Scope:** ~7,200 lines of GHL code eliminated. 1 new MCP server (rpi-comms-mcp). ~23 new MCP tools. 4 new MATRIX tabs. 3 UI integrations. Full GHL subscription cancellation.

---

## Architecture Decision: 4th Consolidated MCP

| MCP | Domain |
|-----|--------|
| **rpi-workspace** (existing, enhanced) | Google Meet + Chat + People (already has Chat/People, adding Meet) |
| **rpi-comms** (NEW) | Twilio SMS/Voice + SendGrid Email + Campaign Execution |
| rpi-business (unchanged) | Commission + Meeting |
| rpi-healthcare (unchanged) | NPI + ICD-10 + CMS + FHIR |

**Why separate?** rpi-workspace is 71 tools and Google-focused. Twilio + SendGrid are external paid APIs with their own auth, credentials, and webhook infrastructure. Clean separation = clean ownership.

---

## Sprint Plan (10 Sprints, 5 Phases)

### Phase 1: Foundation (Sprints 1-2)

**Sprint 1 — Twilio + SendGrid Accounts + rpi-comms-mcp Scaffold**

JDM action required: Create accounts (guided instructions provided).
- Twilio: Sign up, get Account SID + Auth Token, buy test number (~$1/mo)
- SendGrid: Sign up, create API key, verify `retireprotected.com` domain (DNS CNAME records)
- Store credentials in `~/.config/rpi-mcp/twilio-credentials.json` and `sendgrid-credentials.json`

New files:
```
MCP-Hub/rpi-comms-mcp/
  package.json
  src/
    index.js              # MCP entry point (standard pattern)
    auth.js               # Twilio + SendGrid credential loaders
    twilio-tools.js       # 6 tools: send_sms, get_sms_status, list_sms, initiate_call, get_call_status, list_recordings
    sendgrid-tools.js     # 6 tools: send_email, send_bulk_email, list_templates, create_template, get_delivery_stats, get_email_activity
  scripts/
    setup-twilio.js       # Interactive credential setup
    setup-sendgrid.js     # Interactive credential setup
```

Modified files:
- `MCP-Hub/mcp.json` — add rpi-comms entry
- `MCP-Hub/CLAUDE.md` — add rpi-comms to directory + tables
- `MCP-Hub/analytics/hem-config.json` — add 12 new tool HEM tiers

Verify: Send test SMS to JDM's phone + test email to JDM's inbox. 12 tools registered.

**Sprint 2 — Google Meet Tools in rpi-workspace** (parallel with Sprint 1)

New file:
```
MCP-Hub/rpi-workspace-mcp/src/meet-tools.js  # 5 tools
```

Tools: `meet_create_meeting`, `meet_get_meeting`, `meet_list_upcoming`, `meet_list_recordings`, `meet_get_transcript`

Note: Meet links are created via Calendar API (`conferenceData`). Recordings/transcripts use Meet REST API v2.

Modified files:
- `rpi-workspace-mcp/src/index.js` — import meet-tools
- `rpi-workspace-mcp/src/auth.js` — add `getCalendarClient()`, `getMeetClient()`
- `MCP-Hub/reauth-scopes.js` — add Calendar + Meet scopes

JDM action required: Re-authorize OAuth after scope addition (browser popup).

Verify: Create a meeting with Meet link. List upcoming meetings.

---

### Phase 2: Contact Infrastructure + Campaign Engine (Sprints 3-4)

**Sprint 3 — MATRIX Contact Tabs + Communication Log**

New MATRIX tabs (added to RAPID_CORE TAB_SCHEMAS + TABLE_ROUTING):

| Tab | Purpose | Key Fields |
|-----|---------|------------|
| `_CONTACTS_CARRIERS` | Insurance carriers we work with | carrier_name, contact_name, title, email, phone, relationship_type |
| `_CONTACTS_IMOS` | IMOs/FMOs we work with | imo_name, contact_name, title, email, phone, relationship_type |
| `_CONTACTS_INTERNAL` | RPI team members | team_member_name, role, division, email, google_chat_name, calendar_id |
| `_COMMUNICATION_LOG` | Unified comms history (all channels) | contact_type, contact_id, channel, direction, subject, content_preview, status, twilio_sid, sendgrid_message_id |

New file:
- `RAPID_API/API_Comms.gs` — REST endpoints: `POST /comms/log`, `GET /comms/history`, `GET /comms/stats`

New tools (added to `people-tools.js`):
- `sync_contacts_to_matrix` — sync Google People contacts to MATRIX by category
- `get_contact_sync_status` — check last sync status

Modified files:
- `RAPID_CORE/CORE_Database.gs` — 4 new schemas + TABLE_ROUTING entries
- `RAPID_API/Code.gs` — route `/comms/*` endpoints

**Sprint 4 — Campaign Execution Engine**

New file:
```
MCP-Hub/rpi-comms-mcp/src/campaign-tools.js  # 6 tools
```

Tools: `campaign_execute_send`, `campaign_execute_batch`, `campaign_get_send_status`, `campaign_list_sequences`, `campaign_check_eligibility`, `campaign_schedule_sequence`

Campaign sequence format (JSON in campaign record):
```json
{ "steps": [
    { "day": 1, "channel": "email", "templateId": "...", "subject": "Welcome" },
    { "day": 3, "channel": "sms", "content": "Hi {{first_name}}..." },
    { "day": 5, "channel": "voice", "recordingUrl": "..." }
]}
```

rpi-comms-mcp total after Sprint 4: **18 tools** (6 Twilio + 6 SendGrid + 6 Campaign)

---

### Phase 3: C3 Migration + Webhooks (Sprints 5-6)

**Sprint 5 — C3 GHL Code Replacement**

Replace/delete ~1,860 lines (C3/Code.js lines 2611-4470):
- `pushCampaignToGHL()` → `pushCampaign()` (calls rpi-comms-mcp)
- `getGHLTriggerOptions()` → `getCampaignTriggerOptions()` (reads from MATRIX)
- DELETE: `getGHLSettings`, `saveGHLSettings`, `syncGHLFieldsToSheet`, `getGHLCustomFields`, `getGHLPipelines`, `getGHLTags`, `getGHLFieldInventory`, all GHL API helpers (~20 functions)

C3 UI changes:
- Remove "API Settings" panel (GHL key/Location ID)
- Remove "Push to GHL" buttons
- Add "Execute Campaign" button → rpi-comms-mcp
- Add "Test Communications" → verify Twilio + SendGrid

**Sprint 6 — Webhook Handlers + Delivery Tracking**

New file: `RAPID_API/API_Webhook.gs`

Endpoints:
- `POST /webhook/sendgrid` — delivery, open, click, bounce events
- `POST /webhook/twilio/sms` — SMS delivery confirmations
- `POST /webhook/twilio/voice` — call completion, recording events

Flow: Webhook → RAPID_API → find send by `external_id` → update `_CAMPAIGN_SEND_LOG` status → log to `_COMMUNICATION_LOG`

Security: Webhook paths bypass standard auth (verified by Twilio signature / SendGrid signing key instead).

Schema change: Add `external_id` + `provider` columns to `_CAMPAIGN_SEND_LOG`

---

### Phase 4: UI Integration (Sprints 7-8)

**Sprint 7 — PRODASH CLIENT360 Communications Tab**

New tab in CLIENT360 between Connect and Activity:
- Communication history timeline (all channels, color-coded)
- "Send Email" button → compose modal → SendGrid
- "Send SMS" button → compose modal → Twilio
- "Schedule Meeting" button → Calendar + Meet link
- "Start Chat" button → Google Chat DM/space

New GAS functions:
- `getClientCommsForUI(clientId)` — fetch `_COMMUNICATION_LOG` for client
- `sendClientEmailForUI(clientId, subject, body)` — send via RAPID_API → rpi-comms
- `sendClientSMSForUI(clientId, message)` — send via RAPID_API → rpi-comms
- `scheduleClientMeetingForUI(clientId, startTime, endTime, subject)` — Calendar API

**Sprint 8 — RIIMO + SENTINEL** (parallel with Sprint 7)

RIIMO:
- "Team Availability" dashboard card (Calendar free/busy + Chat presence)
- Google Chat panel for internal comms

SENTINEL:
- Deal detail: "Communications" section scoped to deal contacts
- "Schedule Due Diligence Call" → Meet link
- Communication log filtered by deal contact_ids

---

### Phase 5: Data Pipeline + GHL Elimination (Sprints 9-10)

**Sprint 9 — RAPID_IMPORT Comms Intake**

New file: `RAPID_IMPORT/IMPORT_Comms.gs`
- `syncTwilioMessages()` — pull Twilio SMS/call logs → `_COMMUNICATION_LOG`
- `syncSendGridActivity()` — pull SendGrid events → `_COMMUNICATION_LOG`
- `syncMeetRecordings()` — scan for new recordings → `_INTAKE_QUEUE`
- `importGHLContactsToNative()` — one-time migration: ensure all GHL data in MATRIX

**Sprint 10 — GHL Elimination**

Delete files:
- `RAPID_IMPORT/IMPORT_GHL.gs` (4,394 lines)
- `RAPID_API/API_GHL_Sync.gs` (1,661 lines)

Clean up:
- Remove GHL routing from RAPID_API/Code.gs
- Remove GHL references from C3 (should be clean from Sprint 5)
- Remove `GHL_API_KEY`, `GHL_LOCATION_ID` from Script Properties
- Archive `_RPI_STANDARDS/reference/integrations/GHL_INTEGRATION.md`
- `ghl_contact_id` field stays in `_CLIENT_MASTER` as historical reference

Verify: Grep all GAS projects for "GHL" — zero matches (except `ghl_contact_id` field).
Cancel GHL subscription.

---

## Sprint Dependencies

```
Sprint 1 (Twilio/SendGrid MCP) ─┬─→ Sprint 3 (Contact tabs) → Sprint 4 (Campaign engine)
                                 │                                        │
Sprint 2 (Meet tools) ──────────┘                                        v
     [parallel]                                              Sprint 5 (C3 migration) → Sprint 6 (Webhooks)
                                                                         │
                                                              Sprint 7 (PRODASH UI) ─┬─→ Sprint 9 (Import)
                                                                                      │          │
                                                              Sprint 8 (RIIMO+SENT)──┘           v
                                                                   [parallel]           Sprint 10 (GHL kill)
```

---

## New MCP Tools Summary (23 total)

**rpi-comms-mcp (18 tools):**
- Twilio: `comms_send_sms`, `comms_get_sms_status`, `comms_list_sms`, `comms_initiate_call`, `comms_get_call_status`, `comms_list_recordings`
- SendGrid: `comms_send_email`, `comms_send_bulk_email`, `comms_list_templates`, `comms_create_template`, `comms_get_delivery_stats`, `comms_get_email_activity`
- Campaign: `campaign_execute_send`, `campaign_execute_batch`, `campaign_get_send_status`, `campaign_list_sequences`, `campaign_check_eligibility`, `campaign_schedule_sequence`

**rpi-workspace-mcp additions (5 tools):**
- Meet: `meet_create_meeting`, `meet_get_meeting`, `meet_list_upcoming`, `meet_list_recordings`, `meet_get_transcript`

---

## Risks + Mitigations

| Risk | Mitigation |
|------|------------|
| SendGrid domain verification (24-48h DNS) | Start Sprint 1 immediately; async |
| Twilio trial limits (verified numbers only) | Upgrade to paid ($20/mo min) after testing passes |
| Google Meet REST API requires Workspace tier | Verify RPI tier; fallback to Calendar API only |
| Webhook cold-start latency on GAS | RAPID_API already has keep-warm patterns |
| PHI in comms content | Never log full body — `content_preview` max 200 chars, mask SSN/DOB |
| Tool name collisions | All prefixed: `comms_`, `campaign_`, `meet_` |

---

## Verification Plan

Each sprint has built-in verification. End-to-end test after all sprints:
1. Create campaign in C3 → execute batch send (email + SMS) → verify delivery via webhooks
2. CLIENT360: view comms history, send email, send SMS, schedule Meet
3. RIIMO: team availability shows correctly
4. SENTINEL: deal communications tracked
5. Grep all GAS projects for "GHL" → zero (except `ghl_contact_id` historical field)
6. `claude mcp list` shows 4 consolidated MCPs
