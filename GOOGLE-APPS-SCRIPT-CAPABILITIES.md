# Google Apps Script Automation Capabilities

## Overview

Google Apps Script (GAS) is a **serverless JavaScript platform** that runs inside Google's infrastructure. It can automate virtually anything in the Google ecosystem and connect to external systems.

**Key Insight:** This runs on Google's servers, not your machine. Set it up once, it runs forever.

---

## Trigger Types

| Trigger | When It Fires | Use Case |
|---------|---------------|----------|
| **Time-driven** | Scheduled (hourly, daily, weekly, specific time) | Daily data sync, nightly reports, weekly summaries |
| **On Edit** | User changes a cell | Real-time validation, auto-calculations, cascading updates |
| **On Change** | Structure change (add/delete rows, sheets) | Audit logging, schema enforcement |
| **On Form Submit** | Google Form submitted | Lead capture, intake processing, survey handling |
| **On Open** | Spreadsheet/Doc opened | Custom menus, welcome messages, session logging |
| **HTTP (doGet/doPost)** | External web request | Webhooks, API endpoints, integrations |

---

## What Apps Script Can DO

### 1. Google Workspace Automation

| Service | Capabilities |
|---------|--------------|
| **Sheets** | Read/write cells, create charts, conditional formatting, pivot tables, named ranges |
| **Docs** | Generate documents, mail merge, find/replace, insert images |
| **Drive** | Create/move/delete files, manage permissions, search, organize folders |
| **Gmail** | Send emails, read inbox, create drafts, manage labels, search |
| **Calendar** | Create events, send invites, check availability, sync calendars |
| **Slides** | Generate presentations, update templates, insert charts from Sheets |
| **Forms** | Create forms dynamically, process responses, route submissions |

### 2. External Integrations

| Integration | How |
|-------------|-----|
| **REST APIs** | `UrlFetchApp.fetch()` - call any HTTP endpoint |
| **Webhooks (Outbound)** | POST to Slack, Discord, Teams, Zapier, n8n, custom servers |
| **Webhooks (Inbound)** | Deploy as web app, receive POSTs from external systems |
| **Databases** | Connect to Cloud SQL, Firebase, external DBs via API |
| **Authentication** | OAuth2, API keys, service accounts |

### 3. Scheduling Capabilities

```javascript
// Run every day at 6 AM
ScriptApp.newTrigger('dailyFunction')
  .timeBased()
  .atHour(6)
  .everyDays(1)
  .create();

// Run every hour
ScriptApp.newTrigger('hourlyFunction')
  .timeBased()
  .everyHours(1)
  .create();

// Run every Monday at 9 AM
ScriptApp.newTrigger('weeklyFunction')
  .timeBased()
  .onWeekDay(ScriptApp.WeekDay.MONDAY)
  .atHour(9)
  .create();
```

---

## RPI Project Suite Applications

### 1. MATRIX Commission Sync (Already Built)

**Trigger:** Daily at 6 AM + On Edit (debounced)
**Action:** Export comp grids to JSON format, log sync, notify via Slack

```
MATRIX → Apps Script → JSON Export → Drive Folder
                    → Slack Notification
                    → Sync Log
```

### 2. SENTINEL Data Pipeline

**Potential Triggers:**
- **On Edit** → Validate data entry, check for duplicates
- **Daily** → Generate carrier reports, sync to external systems
- **On Form Submit** → Process new agent applications

**Capabilities:**
- Auto-populate fields based on lookups
- Validate NPN numbers against external API
- Generate producer agreements from templates
- Send welcome emails via Gmail
- Create calendar events for follow-ups

### 3. Commission Statement Processing

**Trigger:** When new file added to Drive folder (using Drive API polling)

**Workflow:**
```
New XLSX in Comp-Statements/
        ↓
Apps Script detects new file (hourly check)
        ↓
Parse XLSX, extract commission data
        ↓
Update MATRIX tracking sheet
        ↓
Flag discrepancies
        ↓
Slack alert: "New statement processed: $X,XXX"
```

### 4. Meeting Intelligence Enhancement

**Trigger:** When new recording lands in `Pending/` folder

**Workflow:**
```
New recording in Pending/
        ↓
Apps Script detects (hourly)
        ↓
Trigger Claude via webhook: "Process this meeting"
        ↓
Move to Processed/ when done
        ↓
Update meeting log spreadsheet
        ↓
Slack: "Meeting processed - 3 action items"
```

### 5. Book of Business Monitoring

**Triggers:**
- **Daily at 7 AM** → Check for policy lapses in next 30 days
- **Weekly** → Generate retention report
- **Monthly** → Calculate commission projections

**Alerts:**
- Policy about to lapse → Slack + Email
- Renewal cliff approaching → Notification
- Premium changes → Flag for review

### 6. Carrier API Integration Hub

**Trigger:** Scheduled or On-Demand

**Connect to:**
- Sunfire API (carrier contracting)
- CMS API (Medicare plan data)
- NPI Registry API (provider lookups)
- Your own MCP endpoints

### 7. Client Communication Automation

**Trigger:** Based on data conditions in sheets

**Examples:**
- Birthday coming up → Send card via Gmail
- Policy anniversary → Send review reminder
- AEP approaching → Send educational content
- Claim filed → Follow-up sequence

### 8. Financial Dashboard Updates

**Trigger:** Daily at midnight

**Workflow:**
```
Pull commission data from statements
        ↓
Calculate YTD, MTD, projections
        ↓
Update dashboard Sheet
        ↓
Refresh connected Looker Studio
        ↓
Slack: Daily revenue snapshot
```

---

## Architecture Patterns

### Pattern 1: Spreadsheet as Database + UI

```
Google Sheet (Data + UI)
        ↓
Apps Script (Business Logic)
        ↓
External APIs / Services
```

**Best for:** Internal tools, dashboards, simple workflows

### Pattern 2: Webhook Receiver

```
External System (Zapier, n8n, GitHub, etc.)
        ↓ POST
Apps Script Web App (doPost)
        ↓
Process + Route to Google Services
```

**Best for:** Integrating external events into Google ecosystem

### Pattern 3: Scheduled ETL

```
External Data Sources
        ↓ (Scheduled fetch)
Apps Script
        ↓
Transform + Load into Sheets
        ↓
Downstream consumers
```

**Best for:** Data pipelines, reporting, sync jobs

### Pattern 4: Event-Driven Automation

```
User Action (edit, form submit, file upload)
        ↓ Trigger
Apps Script
        ↓
Cascade of actions (validate, notify, update, create)
```

**Best for:** Workflow automation, data validation

---

## Limitations to Know

| Limitation | Details | Workaround |
|------------|---------|------------|
| **Execution time** | 6 min max (30 min for Workspace) | Break into smaller jobs, use triggers |
| **Daily quota** | Varies by action type | Monitor usage, prioritize critical actions |
| **No persistent state** | Scripts are stateless | Use PropertiesService or Sheet as state store |
| **Cold starts** | First run can be slow | Keep critical scripts warm with periodic pings |
| **CORS** | Can't call from browser JS | Use as backend only |

---

## Quick Implementation Examples

### Send Slack Notification

```javascript
function sendSlackNotification(message) {
  const webhook = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL';
  UrlFetchApp.fetch(webhook, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ text: message })
  });
}
```

### Call External API

```javascript
function callExternalAPI() {
  const response = UrlFetchApp.fetch('https://api.example.com/data', {
    method: 'get',
    headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
  });
  return JSON.parse(response.getContentText());
}
```

### Create Webhook Endpoint

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  // Process incoming webhook
  SpreadsheetApp.getActive().getSheetByName('Log').appendRow([
    new Date(), JSON.stringify(data)
  ]);
  return ContentService.createTextOutput('OK');
}
```

### Monitor Drive Folder

```javascript
function checkForNewFiles() {
  const folder = DriveApp.getFolderById('FOLDER_ID');
  const files = folder.getFilesByType(MimeType.PDF);
  
  while (files.hasNext()) {
    const file = files.next();
    if (isNewFile(file)) {
      processFile(file);
      moveToProcessed(file);
    }
  }
}
```

---

## Next Steps for RPI

1. **Start with commission sync** (already built in `matrix-sync.gs`)
2. **Add Slack notifications** for key events
3. **Build statement processor** for auto-ingestion
4. **Create meeting trigger** to kick off processing
5. **Build retention alerts** based on BoB data

---

## Resources

- [Apps Script Documentation](https://developers.google.com/apps-script)
- [Triggers Guide](https://developers.google.com/apps-script/guides/triggers)
- [Web Apps](https://developers.google.com/apps-script/guides/web)
- [Quotas & Limits](https://developers.google.com/apps-script/guides/services/quotas)

---

*This is a game-changer for automation. Anything in Google's ecosystem can be automated, scheduled, and connected to external systems - all without running a server.*
