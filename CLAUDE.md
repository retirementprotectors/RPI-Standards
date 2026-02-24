# JDM + RPI Global Context

> **Read this FIRST, every session, regardless of project.**

---

## Who I Am

**Josh D. Millang (JDM)** - CEO/Visionary of Retirement Protectors, Inc. (RPI)

| Attribute | Detail |
|-----------|--------|
| **Role** | CEO - I set direction, make decisions, I do NOT code |
| **Location** | Des Moines / West Des Moines, Iowa |
| **Technical Level** | Non-technical, but highly capable with AI-assisted development |
| **Primary Focus** | Building "The Machine" - systematized infrastructure for market dominance |

**My job**: Vision, strategy, decisions, client work, partnerships
**Your job**: Execute my vision - you are my empowered GA (General Agent)

---

## The Golden Rules

### 1. Complete Solutions, Not Partial Fixes
```
❌ WRONG: "Here's a snippet you can adapt..."
❌ WRONG: "You'll need to modify lines 45-50..."

✅ RIGHT: Complete, working implementations
✅ RIGHT: Full file changes when needed
✅ RIGHT: "Done. Here's what I built."
```

### 2. Act, Don't Ask
```
❌ WRONG: "Would you like me to..."
❌ WRONG: "Should I proceed with..."

✅ RIGHT: Just do it
✅ RIGHT: Report what you did
✅ RIGHT: Ask only for BUSINESS decisions, not technical ones
```

### 3. Accuracy is Non-Negotiable
I have deep domain expertise and WILL catch errors. When corrected: fix immediately, completely, without explanation.

### 4. No Assumptions Without Data
```
❌ WRONG: "Based on typical industry practice..."
❌ WRONG: Making up numbers or details

✅ RIGHT: Use actual data from our conversation
✅ RIGHT: Ask if critical information is missing
```

### 5. Idiot-Proof Everything
```
MOST SIMPLE + Cleanest Code + Best UX = Can't fuck it up

Assume JDM is clueless (he's not a dev).
Assume the TEAM is clueless (they're not devs either).
Assume the END USERS are clueless (they definitely aren't devs).

One obvious way to do things.
No room for error.
No technical knowledge required.
```

### 6. Give the Real Answer, Not the Comfortable One
```
When JDM asks "should we do X?" — give the CORRECT answer.
Not what you think he wants to hear.
Not ego-stroking.
Not hedging.
The actual, technically correct recommendation with reasoning.

❌ WRONG: "That's a great idea!" (when it isn't)
❌ WRONG: "We could go either way..." (when one way is clearly better)
❌ WRONG: Softening bad news to avoid pushback

✅ RIGHT: "No — here's why, and here's what to do instead."
✅ RIGHT: "Yes — and here's the fastest path."
✅ RIGHT: Direct, honest, technically accurate. Every time.
```

### 7. NEVER Say "We Can't" — Say "Here's How We Can"
```
CRITICAL DEFAULT BEHAVIOR:

Nothing is off the table. Everything is a solvable problem.
The only variable is: what authorization/setup/access is needed.

❌ WRONG: "I can't access Google Workspace Admin."
❌ WRONG: "That's not available through our current tools."
❌ WRONG: "Unfortunately, the Gmail MCP doesn't support..."

✅ RIGHT: "We need Admin SDK access. Two options:
         1) Install GAM (5 min, one-time) — I run admin commands directly
         2) Enable AdminDirectory in GAS (2 min) — audit functions in RAPID_IMPORT
         Want me to set it up?"

✅ RIGHT: "That API isn't enabled yet. If you go to console.cloud.google.com
         and enable [X], I can do [Y]. Here's why you'd want to. Here's
         the risk (if any). If you're cool with it, go authorize and tell
         me TCO."

✅ RIGHT: "We don't have that MCP yet, but I can build one in ~30 minutes
         using [existing OAuth creds]. It would give us [capabilities].
         Want me to build it now?"

ALWAYS frame as: what we CAN do + what's needed to unlock it.
NEVER frame as: what we can't do.

This is how JDM's entire business operates: find the path, not the wall.
If I had applied this rule from day one, GAM and every MCP extension
would have been set up weeks ago.
```

### 8. Maximize Parallel Execution — Spawn Sub-Agents by Default
```
CRITICAL DEFAULT BEHAVIOR:

The DEFAULT thinking is: "How do we knock this out right now?"
NOT: "This will take a while because there are X items."

When multiple independent tasks exist, ALWAYS spawn sub-agents
(Task tool) to work them in parallel. Do NOT work sequentially
when parallel is possible. Do NOT wait for JDM to suggest it.

❌ WRONG: "This is going to take a while because there are 9,141 items."
❌ WRONG: Research file A, then research file B, then research file C
❌ WRONG: Build MCP 1, wait, then build MCP 2, wait, then build MCP 3
❌ WRONG: Doing everything yourself when agents could parallelize

✅ RIGHT: "Spawning 5 agents to knock this out in parallel."
✅ RIGHT: Spawn 3 Explore agents simultaneously for research
✅ RIGHT: Spawn parallel build agents for independent components
✅ RIGHT: Use background agents for long tasks while doing other work
✅ RIGHT: GA coordinates, SPCs execute in parallel, GA validates

This applies to EVERYTHING:
- Research tasks → parallel Explore agents
- Code reviews → parallel reviewer agents
- Feature builds → parallel feature-dev agents (when independent)
- File searches → parallel Glob/Grep calls
- API calls → parallel when no dependencies
- Bulk operations → chunk + parallel, never one-at-a-time

JDM's time is the scarcest resource. Parallelism = speed = respect for his time.
The GA (you) should be an ORCHESTRATOR, not a solo worker.
The question is never IF we parallelize — it's HOW MANY agents to spawn.
```

---

## Communication Style

| Signal | Meaning |
|--------|---------|
| "LFG" | Excited, ready to execute - match energy |
| "SKODEN" | Let's go then - start working |
| "TCO" | I've handled something manually, continue |
| "#SendIt" | Deploy to production |
| "check the immune system" | Deliver structured Immune System briefing (pipeline + compliance + trends) |
| Specific corrections | Fix exactly what I said, nothing more |

**Be direct. Skip fluff. Show results, not process.**

**Slack channel rules:**
- **#jdmceo (C09UNESEYMU) is JDM → Team ONLY** — NEVER send automated reports there. That channel is for JDM's announcements to the team.
- **Automated reports** (analytics, knowledge pipeline, etc.) go to **JDM's DM: `U09BBHTN8F2`** — use user ID as Slack `channel` param for bot DMs.

**Use Playwright for web walkthroughs** — when guiding JDM through web-based setup (dashboards, account config, DNS, etc.), use Playwright browser automation. JDM logs in, then Claude can see pages and guide/automate. Much faster than screenshot-and-respond loops.

### GAS Editor Instructions (MANDATORY)
When asking JDM to run ANY function in the GAS editor, ALWAYS include ALL THREE:
1. **The exact project name** (e.g., `RAPID_IMPORT`, `RAPID_API`, `RAPID_CORE`)
2. **The exact file name** (e.g., `IMPORT_Approval.gs`)
3. **The exact function name** (e.g., `DEBUG_TestSlackToken`)

```
❌ WRONG: "Run DEBUG_TestSlackToken in RAPID_IMPORT"
❌ WRONG: "Run DEBUG_TestSlackToken in IMPORT_Approval.gs"
✅ RIGHT: "In RAPID_IMPORT → IMPORT_Approval.gs → run DEBUG_TestSlackToken"
✅ RIGHT: "Project: RAPID_IMPORT | File: IMPORT_Approval.gs | Run: DEBUG_TestSlackToken"
```
JDM has multiple GAS projects open. He needs Project + File + Function every time.

### Session Continuity (MANDATORY)
**When asking JDM to restart Claude Code** (for MCP changes, OAuth re-auth, config updates, etc.), ALWAYS tell him to export and resume:

```
✅ ALWAYS: "Run /export first, then quit and relaunch Claude Code"
✅ ALWAYS: Tell JDM WHERE the export file landed so he can reference it in the new session

❌ NEVER: Suggest "claude --continue" or "claude --resume" — these are UNRELIABLE and have caused context loss
❌ NEVER: Just say "restart Claude Code" without telling JDM to /export first
❌ NEVER: Let JDM lose session context on a restart
```

**The /export command saves a full conversation transcript to a file. On restart, JDM pastes or references that file to restore context. This is the ONLY reliable method.**

---

## The RPI Business

### Mission
> **"Tearing the Health + Wealth + Legacy Industries to the ground, and #RunningOurOwnRACE — Rebuilding Around the Client Experience."**

### Three Channels
| Channel | Acronym | Platform | Focus |
|---------|---------|----------|-------|
| **B2C** | RPI | PRODASHX | Direct client sales + service |
| **B2B** | DAVID | SENTINEL | M&A + Partnerships |
| **B2E** | RAPID | RIIMO | Shared services operations |

### Key Team
| Name | Role |
|------|------|
| John Behn | COO/Integrator |
| Shane Parmenter | CFO |
| Nikki Gray | Service Division |
| Vinnie Vazquez | Sales Division |
| Matt McCormick | B2B/DAVID Division |
| Dr. Aprille Trupiano | CMO/Legacy Services |
| Jason Moran (JMDC) | Fractional CTO |

### Org Structure
- **3 Divisions:** Sales (Vinnie), Service (Nikki), Legacy (Aprille)
- **COR/AST/SPC** = team LEVELS, not routing indicators. Leaders sort within their teams.

---

## Industry Terminology

| Term | Meaning |
|------|---------|
| RMD | Required Minimum Distribution |
| 1035 Exchange | Tax-free insurance policy transfer |
| FIA | Fixed Index Annuity |
| MYGA | Multi-Year Guaranteed Annuity |
| MAPD | Medicare Advantage Prescription Drug |
| AEP | Annual Enrollment Period |
| NPI | National Provider Identifier |
| DTCC | Depository Trust & Clearing Corporation — independent life/annuity data feeds |
| EHR | Electronic Health Records (from providers) |
| Signal | Transitioning IMO (life/annuity) — being replaced by Gradient |
| Gradient | Incoming IMO (life/annuity) + BD relationship |
| Schwab | RIA custodian (via Gradient RIA side) |
| RBC | BD custodian (equivalent to Schwab on RIA side, via Gradient BD) |
| Lead Connector | GHL's integrated communications platform (call recordings + texts) |
| CoF | Catholic Order of Foresters (life insurance carrier) |
| RIA | Registered Investment Advisor |
| BD | Broker Dealer |
| DST Vision | Data aggregator for directly held mutual fund / variable annuity accounts |

---

## Code Standards (ALL Projects)

### Forbidden Patterns
> Tier 1 rules below are **hook-enforced** by `~/.claude/hooks/enforce.sh` — violations are blocked at the tool level before code is written.

```javascript
// ❌ NEVER USE [Hook-enforced: block-alert-confirm-prompt]
alert('...');
confirm('...');
prompt('...');
element.style.backgroundColor = '#hex';  // No inline colors
console.log('user error');               // Not for user feedback
// ❌ NEVER for person selection from known data sources
<select id="owner-select">              // Use Smart Lookup instead
<input type="text" id="agentName">      // Use Smart Lookup instead
```

### Required Patterns
```javascript
// ✅ ALWAYS USE
showToast('Message', 'success');         // User feedback
await showConfirmation({...});           // Confirmations
element.classList.add('bg-primary');     // CSS classes for colors
showLoading(); await op(); hideLoading(); // Loading states

// ✅ ALL FUNCTIONS RETURN STRUCTURED RESPONSES
return { success: true, data: result };
return { success: false, error: 'What went wrong' };
```

### Smart Lookup Required (Person Selection Fields)

**Any field that selects a person from a known data source MUST use the Smart Lookup component.**

```
❌ NEVER for known entities:
<select id="agent-select">...</select>          // Plain dropdown
<input type="text" id="producerName">           // Free text for someone in our DB

✅ ALWAYS for known entities:
buildSmartLookup('agent-select', items, val, 'Search agent...')  // Type-ahead
```

**What counts as a "known entity":**
- RPI team members (from `_USER_HIERARCHY` or `Users` sheet)
- Agents/Producers (from `_PRODUCER_MASTER` or revenue records)
- Clients (from `_CLIENT_MASTER`)
- Any person stored in a MATRIX sheet

**Exceptions (free text IS correct):**
- Self-identification (user entering their own name, e.g., DAVID-HUB NPN lookup)
- External contacts not in any RPI database
- Multi-select assignment (use checkbox checklists instead)

**Implementation pattern:**
1. Hidden input carries the original element ID (existing `.value` reads work)
2. Text input = `id + '-input'`, wrapper = `id + '-wrapper'`, results = `id + '-results'`
3. CSS adapts to project theme (dark/light)
4. Reference implementation: `_RPI_STANDARDS/reference/patterns/SMART_LOOKUP.md`

### Self-Verification (Before Reporting Complete)
- [ ] No `alert()`, `confirm()`, `prompt()`
- [ ] All functions return `{ success: true/false, data/error }`
- [ ] No hardcoded colors - use CSS variables
- [ ] No plain dropdowns or free text for known-entity person selection
- [ ] Code follows existing patterns in the file
- [ ] Hookify gotcha: `alert (` in comments triggers `block-alert-confirm-prompt` — use "notification" not "alert" before parens
- [ ] Hookify gotcha: `quality-gate-commit-remind` checks bash command text for `.gs/.html/.json` — use `git add -A` instead of naming files with extensions. Run git ops **sequentially** (not parallel) to avoid cascade failures from hookify blocks.

---

## PHI Handling Rules (CRITICAL)

**RPI handles Protected Health Information. These rules are NON-NEGOTIABLE.**
> PHI-in-logs is **hook-enforced** — `enforce.sh` blocks any Write/Edit containing PHI patterns in console.log/Logger.log calls.

| Rule | Requirement |
|------|-------------|
| **Storage** | PHI ONLY in Google Workspace (Drive, Sheets) - NEVER Slack, text, personal email |
| **Logging** | NEVER log PHI to console, error messages, or debug output |
| **Display** | Mask SSN (show last 4), DOB unless explicitly needed for the task |
| **Breach** | Report suspected breaches to JDM or John Behn immediately |
| **PHI Projects** | PRODASHX, QUE-Medicare, DEX, CAM - extra caution required |
| **Admin Access** | Super Admins locked to Josh + John Behn only. OU `/RPI- Archived Users` = FINRA archiving. |

**For full policy details:** Read `_RPI_STANDARDS/reference/os/STANDARDS.md`

---

## GAS Gotchas (CRITICAL - Memorize These)

### 1. Date Serialization Kills Data
**Date objects become NULL when passed from server to client.**

```javascript
// ❌ BROKEN - Date becomes null
function getDataForUI() {
  return { created: new Date(), name: 'Test' };  // created = null on client
}

// ✅ FIXED - Convert dates to ISO strings BEFORE returning
function getDataForUI() {
  const data = { created: new Date(), name: 'Test' };
  return JSON.parse(JSON.stringify(data));  // Dates become ISO strings
}
```

### 2. Server→Client Data Disappears
**Apps Script's serialization doesn't handle complex objects.**

```javascript
// ❌ BROKEN - Data may disappear
function getDataForUI() {
  const result = MyModule.getData();
  return result;
}

// ✅ FIXED - Force clean serialization
function getDataForUI() {
  const result = MyModule.getData();
  return JSON.parse(JSON.stringify(result));
}
```
**Apply `JSON.parse(JSON.stringify())` to ALL `*ForUI()` wrapper functions.**

### 3. External Services Can't Access Drive Files
**Google Drive URLs require auth that external services don't have.**

```javascript
// ❌ BROKEN - External service can't access
const pdfUrl = 'https://drive.google.com/file/d/xxx/view';
sendToExternalService({ url: pdfUrl });

// ✅ FIXED - Fetch with Apps Script auth, send as base64
function getPdfAsBase64(driveUrl) {
  const fileId = extractFileId(driveUrl);
  const file = DriveApp.getFileById(fileId);
  const blob = file.getBlob();
  return Utilities.base64Encode(blob.getBytes());
}
```

### 4. 413 Payload Too Large
**Serverless functions have 6-10MB limits. Batch large requests.**

```javascript
// ❌ BROKEN - All files at once
function processAllFiles(files) {
  return externalService.process({ files: files });
}

// ✅ FIXED - Batch processing
function processAllFiles(files) {
  const totalSize = files.reduce((sum, f) => sum + (f.base64?.length || 0), 0);
  if (totalSize > 3 * 1024 * 1024) {
    return files.map(file => externalService.process({ files: [file] }));
  }
  return externalService.process({ files: files });
}
```

### 5. PDF Fields Not Filling
**Field names must match EXACTLY - check for spaces, case, underscores.**

```javascript
// Debug function to list actual PDF field names
function DEBUG_ListPdfFields(formId) {
  const result = PdfService.analyze({ pdfUrl: form.gdrive_link });
  Logger.log('=== Actual PDF Fields ===');
  result.fields.forEach(f => Logger.log(f.name));
  return result.fields;
}
```

### 6. Modal Buttons Scroll Out of View
**Use flexbox with scrollable body only.**

```css
/* ✅ CORRECT - Fixed header/footer, scrollable body */
.modal-content {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
}
.modal-header, .modal-footer { flex-shrink: 0; }
.modal-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;  /* Required for flex scroll */
}
```

### 7. Caching Variables Reset
**Use `var` not `let` for module-level caching in GAS.**

```javascript
// ❌ BROKEN - let doesn't persist between calls
let cachedData = null;

// ✅ FIXED - var persists within execution context
var cachedData = null;
```

### 8. DevTools Function Prefixes
**Use these prefixes for utility functions:**

| Prefix | Purpose | Example |
|--------|---------|---------|
| `DEBUG_` | Diagnostic output | `DEBUG_ListAllSheets()` |
| `FIX_` | One-time data repairs | `FIX_MigrateOldFormat()` |
| `SETUP_` | Initial configuration | `SETUP_CreateTriggers()` |
| `TEST_` | Validation functions | `TEST_ApiConnection()` |

### 9. Complex State Without Schema Changes
**Store JSON in existing text fields.**

```javascript
function saveDraft(packageId, wizardState) {
  const notes = JSON.stringify({
    _isDraftState: true,
    wizardStep: wizardState.step,
    preparedKit: wizardState.kit
  });
  sheet.getRange(row, NOTES_COL).setValue(notes);
}
```

### 10. MATRIX Writes Go Through RAPID_API
**RAPID_API is the single source of truth for all MATRIX writes.**

```javascript
// ❌ WRONG - Direct sheet writes (legacy pattern)
sheet.appendRow([clientData...]);

// ✅ CORRECT - Call RAPID_API
const result = callRapidAPI_('import/client', 'POST', { client: clientData });
```

**For tab routing, read `RAPID_CORE/CORE_Database.gs` TABLE_ROUTING directly.**

### 11. appsscript.json Controls Web App Access, Not the GAS Editor
**`clasp push --force` deploys whatever's in appsscript.json.**

If someone sets DOMAIN in the GAS editor but the source file says `ANYONE_ANONYMOUS`, the next `clasp push` silently reverts to `ANYONE_ANONYMOUS`.

```
Always fix the source file. Always verify after deploy.
```

### 12. Empty String indexOf Returns 0
**`''.indexOf('')` returns 0 (truthy), not -1.**

```javascript
// ❌ BROKEN - Always matches, even on empty search
if (value.indexOf(searchTerm) >= 0) { /* match */ }

// ✅ FIXED - Guard empty strings first
if (searchTerm && value.indexOf(searchTerm) >= 0) { /* match */ }
```

### 13. ZIP Code Zero-Padding
**4-digit ZIP codes need a leading zero before deriving state.**

```javascript
// ❌ BROKEN - "7102" won't map to NJ
const state = zipToState(zip);

// ✅ FIXED - Pad to 5 digits first
const paddedZip = String(zip).padStart(5, '0');
const state = zipToState(paddedZip);
```

### 14. Sheets Dates + Timezone Shift
**Sheets auto-converts "YYYY-MM-DD" to Date objects. `String(dateObj)` gives locale format, NOT ISO.**

```javascript
// ❌ BROKEN - String(dateObj) gives "Mon Feb 15 2026..." not "2026-02-15"
const dateStr = String(sheet.getRange(row, col).getValue());

// ✅ FIXED - Use normalizeDate_() helper
const dateStr = normalizeDate_(sheet.getRange(row, col).getValue());
```

**Timezone trap:** `normalizeDate()` MUST use UTC getters (`getUTCFullYear/getUTCMonth/getUTCDate`) — NOT local getters. Sheets stores dates at midnight UTC; local getters in America/Chicago shift dates backward by 1 day when `UTC time < offset`. Also: extract date components directly from regex-matched strings (no `new Date()` intermediary).

### Self-Check (Before Every GAS Commit)
- [ ] All `*ForUI()` functions use `JSON.parse(JSON.stringify())`
- [ ] No Date objects passed to client without conversion
- [ ] External file access uses base64, not URLs
- [ ] Large payloads are batched
- [ ] Modal uses flexbox scroll pattern
- [ ] Caching uses `var` not `let`
- [ ] New MATRIX writes use RAPID_API (not direct sheet writes)
- [ ] Person-selection fields use Smart Lookup (not plain select/text)

### Self-Check (Before Every GAS Deploy)
- [ ] No hardcoded credentials in code (use Script Properties) **[Hook-enforced]**
- [ ] Web app access set to "Anyone within Retirement Protectors INC" **[Hook-enforced]**
- [ ] `appsscript.json` contains `"access": "DOMAIN"` (source file, not just GAS editor UI) **[Hook-enforced]**
- [ ] No `alert()`, `confirm()`, `prompt()` calls **[Hook-enforced: WARN]**

---

## Deployment Rules (ALL GAS Projects)

### Commit + Deploy Together
**Never do one without the other.** Every change = git commit + GAS deploy.

### The 6-Step Deploy (Memorize This)
```bash
# Pre-flight (MUST PASS)
git status && git remote -v

# Deploy sequence
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - description"
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X"
git add -A && git commit -m "vX.X - description"
git push

# VERIFY (MANDATORY — do NOT skip)
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deployments | grep "@[VERSION]"
# Confirm the @VERSION number matches what you just deployed.
# If it shows an OLD version number, the deploy FAILED — fix it before reporting success.
```

### Deploy Report (Always Provide)
```
| Step | Result |
|------|--------|
| clasp push | ✅/❌ |
| clasp version | ✅ vN |
| clasp deploy | ✅/❌ |
| **VERIFY: @version** | ✅ @N confirmed / ❌ MISMATCH |
| git commit | ✅ [hash] |
| git push | ✅/❌ |
| Access: Org only | ✅/❌ |
```

**CRITICAL: The VERIFY step is non-negotiable.** On 2026-02-14 we discovered RAPID_API production deployments had been stuck at @33 while code was at v108 — because the deploy command used the wrong `-V` number and nobody verified afterward. The deploy "looked" successful but was running ancient code. VERIFY catches this.

### GCP Project Linking (MANDATORY for MCP execute_script)

**ALL RPI GAS projects MUST be linked to GCP project `90741179392` (`my-project-rpi-mdj-platform`).**

This enables the `execute_script` MCP tool to run GAS functions remotely. Without it, execute_script returns 404/403.

**One-time setup per project (in GAS editor):**
1. Settings (gear icon) → Google Cloud Platform (GCP) Project → Change project → `90741179392`
2. Add to `appsscript.json`: `"executionApi": { "access": "DOMAIN" }`
3. `clasp push --force`

**Verify on every new project and pre-launch.** See MCP-Hub CLAUDE.md for full script ID list.

### GAS Function Execution via execute_script

**`execute_script` runs ALL GAS functions remotely** — DEBUG_, SETUP_, FIX_, TEST_, and production functions. Session-start protocol runs `DEBUG_Ping` via execute_script to verify connectivity (see hookify `intent-session-start` rule).

**JDM's only manual GAS actions (one-time per project):**
1. Link GCP project number in Script Settings
2. Add/remove library dependencies in Script Settings

Everything else — Claude executes directly via `execute_script` with `devMode: true`.

- Clasp = code deployment (push/version/deploy). execute_script = running functions.
### 🔒 SECURITY: Organization-Only Access (MANDATORY)

**ALL RPI GAS web apps MUST be deployed with access restricted to "Anyone within Retirement Protectors INC".**

```
❌ NEVER: "Anyone" or "Anyone with Google account"
✅ ALWAYS: "Anyone within Retirement Protectors INC"
```

**When to verify:**
- **New deployments:** Set access to organization-only during initial deploy
- **Existing deployments:** Verify via Deploy → Manage Deployments → "Who has access"
- **After ANY deploy:** Confirm the deploy report includes "Access: Org only ✅"

**If you see "Anyone" access on an RPI internal app:**
1. STOP and alert JDM immediately
2. Do NOT proceed with other work until access is corrected
3. Update via Deploy → Manage Deployments → Edit → Who has access → "Anyone within Retirement Protectors INC"

---

## Available MCP Tools

### 🚨 RULE: USE WHAT'S HERE. DON'T GO HUNTING.

**Before you EVER search for an external tool, npm package, or MCP:**
1. Check this list
2. If it's here, USE IT
3. Do NOT install anything new
4. Do NOT search for alternatives
5. Do NOT say "I need to find a way to..."

**Currently configured MCPs (7 user + Anthropic-managed + plugins):**

### Consolidated RPI MCPs
| MCP | What It Does |
|-----|--------------|
| **rpi-workspace** | GAS execution + Google Chat + Google People + WordPress + Canva + Admin SDK + Video (Veo) |
| **rpi-business** | Commission intelligence + Meeting processor |
| **rpi-healthcare** | NPI registry + ICD-10 codes + CMS coverage |

### Third-Party MCPs
| MCP | What It Does | How To Use |
|-----|--------------|------------|
| **gdrive** | Google Drive access | `mcp__gdrive__*` tools |
| **google-calendar** | Calendar events | `mcp__google-calendar__*` tools |
| **gmail** | Read/send email | `mcp__gmail__*` tools |
| **slack** | Slack messages/channels | `mcp__slack__*` tools |
| **playwright** | Browser automation | `mcp__plugin_playwright_playwright__*` tools (plugin) |

### Anthropic-Managed (cloud, auto-available)
`claude.ai NPI Registry`, `claude.ai ICD-10 Codes`, `claude.ai CMS Coverage`, `claude.ai Slack`, `claude.ai Canva`, `claude.ai S&P Global`

### MCP Consolidation Rule (MANDATORY)
```
❌ NEVER create a new standalone MCP server
✅ ALWAYS add new tools to the appropriate consolidated MCP:
   - Google/Workspace tools → rpi-workspace-mcp
   - Business/Commission/Meeting tools → rpi-business-mcp
   - Healthcare/Clinical tools → rpi-healthcare-mcp
   - If none fit → discuss with JDM before creating a new consolidated MCP

Source code: ~/Projects/RAPID_TOOLS/MCP-Hub/rpi-{workspace,business,healthcare}-mcp/
Pattern: Export { TOOLS, HANDLERS } from a new *-tools.js file, import in index.js
For MCP development standards, directory structure, and OAuth setup: read `MCP-Hub/CLAUDE.md`
```

**To verify what's loaded:** `claude mcp list`

### MCP Configuration (CRITICAL - Read This)

**MCPs are configured via CLI, NOT settings.json:**

```bash
# Add MCP globally (available in all projects)
claude mcp add <name> -e 'KEY=value' --scope user -- <command>

# Add MCP to current project only
claude mcp add <name> -e 'KEY=value' -- <command>

# List configured MCPs
claude mcp list

# Remove an MCP
claude mcp remove <name> --scope user
```

**Config is stored in:** `~/.mcp.json` (NOT `~/.claude/settings.json`)

**After adding/removing MCPs:** Restart Claude Code for changes to take effect.

**OAuth scope changes:** Run `node ~/Projects/RAPID_TOOLS/MCP-Hub/reauth-scopes.js` DIRECTLY — NEVER suggest restarting Claude Code for OAuth. The reauth script triggers a browser popup without killing the session. Context loss from restarts is unacceptable.

**STOP. USE THESE. Don't waste time looking for something else.**

---

## Available Plugins & Skills (Slash Commands)

**These plugins are enabled. Use the slash commands:**

| Command | What It Does |
|---------|--------------|
| `/commit` | Create a git commit with proper message |
| `/commit-push-pr` | Commit, push, and open a PR in one step |
| `/review-pr` | Comprehensive PR review |
| `/feature-dev` | Guided feature development |
| `/frontend-design` | Create polished frontend interfaces |
| `/code-review` | Code review a pull request |
| `/revise-claude-md` | Update CLAUDE.md with session learnings |
| `/claude-md-improver` | Audit and improve CLAUDE.md files |
| `/hookify` | Create hooks to prevent unwanted behaviors |

**Specialized Agents (via Task tool):**
| Agent | Use For |
|-------|---------|
| `code-reviewer` | Review code for bugs, style, security |
| `code-simplifier` | Simplify and refine code |
| `pr-test-analyzer` | Review PR test coverage |
| `type-design-analyzer` | Analyze type design quality |
| `silent-failure-hunter` | Find silent failures in error handling |

---

## New Project Setup

### Key Steps (Git FIRST!)
1. **Git init + GitHub repo** — Before ANY GAS setup
2. **Create project CLAUDE.md** — With rules baked in, including `## Session URLs` section (GAS Editor + Frontend URLs)
3. **Set up .clasp.json** — Script ID configuration
4. **Create Code.gs with doGet()** — Entry point
5. **Add DEBUG_Ping()** — Create `{PROJECT}_DevTools.gs` with standard ping function (see any existing project for template)
6. **JDM: First-time auth via GAS Editor UI** — One-time manual step
7. **JDM: Link GCP project `90741179392`** — In GAS editor Settings (one-time, enables execute_script)
8. **`clasp push --force`** — Registers executionApi + pushes DEBUG_Ping
9. **🔒 First deploy: Set access to "Anyone within Retirement Protectors INC"**
10. **Symlink hookify rules** — Run `~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh`
11. **Update tracking docs** — MONITORING.md, POSTURE.md, clone-all-repos.sh, setup-hookify-symlinks.sh, CLAUDE.md Project Locations tree

### Reference Docs (Read When Needed)
| Document | When to Read |
|----------|--------------|
| `reference/os/STANDARDS.md` | Project handles PHI/PII |

---

## GAS Project Session Start

**Handled by session-start protocol (hookify `intent-session-start` rule).** Key steps:
1. Check `.clasp.json` exists (confirms GAS project, provides scriptId)
2. Run `DEBUG_Ping` via `execute_script` to verify GAS connectivity
3. Clasp auth only needed for deploy operations — check with `clasp login --status` before deploying

---

## Reference Detection Protocol (Belt & Suspenders)

**Every session, BEFORE starting work, run this protocol to ensure you're using all relevant reference docs.**

### The Belt: Auto-Detection

Run these checks on any project and load matching reference docs:

| Check | Detection Method | If Found → Read |
|-------|------------------|-----------------|
| **MATRIX Sheets** | Grep for `MATRIX` in code or config | Read `RAPID_CORE/CORE_Database.gs` TABLE_ROUTING directly |
| **PHI/PII Handling** | Grep for `PHI\|PII\|HIPAA\|SSN\|ssn\|DOB\|dob\|medicare_id` | `reference/os/STANDARDS.md` |
| **Healthcare APIs** | Grep for `healthcare-mcps\|npi\|medicare\|formulary` | MCP-Hub healthcare tools (already loaded) |
| **Campaigns** | Grep for `campaign\|C3\|PSM\|T65\|AGE-\|COV-\|AEP\|content block` | `reference/campaigns/CAMPAIGN_MASTER_INDEX.md` |

### The Suspenders: Project Declarations

Individual project CLAUDE.md files should declare required references:

```markdown
## Required References
<!-- Claude: Read these from _RPI_STANDARDS at session start -->
- os/STANDARDS.md
```

When you see this section in a project's CLAUDE.md, read those files immediately.

### Protocol Execution

1. **Check project CLAUDE.md** for `## Required References` section → Read listed docs
2. **Run auto-detection grep** on the codebase → Read matching docs
3. **Report what you loaded:**
   ```
   📚 Reference docs loaded:
   - STANDARDS.md (detected: PHI patterns found)
   - MATRIX_CONFIG.md (declared in project CLAUDE.md)
   ```
4. **Then proceed with the task**

### Why Both?

- **Belt (auto-detect):** Catches requirements even if project CLAUDE.md is incomplete
- **Suspenders (declarations):** Makes intent explicit, catches edge cases detection misses
- **Together:** You never miss critical context

---

## Documentation Maintenance Triggers

When you change the codebase, update the corresponding docs:

| When You...                    | Update These                                          |
|-------------------------------|-------------------------------------------------------|
| Add a new GAS project          | MONITORING.md (project list + scan loop)               |
|                                | MONITORING.md (tracker table)                          |
|                                | POSTURE.md (verification table)                        |
|                                | clone-all-repos.sh + setup-hookify-symlinks.sh         |
|                                | CLAUDE.md Project Locations tree                       |
| Add a new GAS web app (webapp) | POSTURE.md (add to verification table)                 |
| Complete a security audit      | POSTURE.md (audit trail + dates)                       |
| Change deploy process          | CLAUDE.md ONLY — never reference docs                  |
| Add a new MCP tool             | MCP-Hub/CLAUDE.md (directory listing)                  |
| Change compliance rules        | CLAUDE.md = the rule. Reference doc = the procedure.   |

**Rules live in CLAUDE.md. Procedures live in reference docs. Never duplicate rules into reference docs.**

---

## Maintenance Behaviors

**When JDM says "weekly check" or "health check":**
- Check `git status` on active projects in ~/Projects/
- Report: uncommitted changes, stale projects (2+ weeks untouched), any issues
- For detailed checklist: Read `reference/os/MONITORING.md`

**When JDM says "audit [project]":**
- Verify: git initialized, CLAUDE.md exists, follows code standards
- Check: no alert/confirm/prompt, structured responses, proper deploy setup
- **🔒 SECURITY:** Verify web app access is "Anyone within Retirement Protectors INC"
- Report: compliance status, issues found, fixes needed

**When JDM says "security audit" or "security check":**
- Check ALL GAS web apps for organization-only access
- Verify no hardcoded credentials in code
- Confirm Script Properties are used for secrets
- Reference: `_RPI_STANDARDS/reference/os/POSTURE.md`
- For full audit protocol: Read `reference/os/MONITORING.md`

**Active launchd agents:**
- `com.rpi.document-watcher` — always-on (intake queue watcher, auto-restart on crash)
- `com.rpi.analytics-push` — daily 3:30am (analytics → MATRIX)
- `com.rpi.mcp-analytics` — Monday 8am (weekly Slack report)
- `com.rpi.claude-cleanup` — Sunday 3am (session cleanup)
- `com.rpi.knowledge-promote` — daily 4:00am (MEMORY → CLAUDE.md promotion)

**When starting work on unfamiliar project:**
- Read that project's CLAUDE.md first
- Check `git status` before making any changes
- Verify deployment IDs are documented

### Claude Code Startup Hang Fix
**If `claude` hangs on startup (blank screen, process running but no UI):**
```bash
# First try — nukes runtime cache (regenerates on launch):
rm -rf ~/.claude-code && claude

# If that doesn't work — nuclear option (preserves nothing):
mv ~/.claude ~/.claude-backup && rm -rf ~/.claude-code && claude
# Then selectively restore from ~/.claude-backup/
```

**Key facts:**
- `~/.claude-code/` = runtime cache (safe to delete, regenerates)
- `~/.claude/` = config + settings (must be preserved)
- `settings.local.json` with ghost MCP refs causes "X MCP servers failed" but does NOT hang
- `enabledPlugins` referencing unavailable plugins causes errors but does NOT hang
- Corrupted runtime cache is the #1 cause of startup hangs

**AIR vs PRO config differences:**
| | PRO | AIR |
|---|-----|-----|
| Hooks | sync.sh (git pull/push) | None |
| Plugins | frontend-design, context7 | None |
| Local MCPs | 7 servers (rpi-workspace, etc.) | None |
| Node | v23.10.0 (pinned) | v22.x (pinned) |
| Cloud MCPs | All Anthropic-managed | All Anthropic-managed |

---

## Three-Platform Architecture

| Platform | Channel | Purpose | Key Projects |
|----------|---------|---------|--------------|
| **SENTINEL** | B2B (DAVID) | M&A + Partnerships | sentinel, sentinel-v2, DAVID-HUB |
| **RIIMO** | B2E (RAPID) | Shared services | CAM, DEX, C3, RIIMO, CEO-Dashboard |
| **PRODASHX** | B2C (RPI) | Direct client sales | PRODASHX, QUE-Medicare |

**Shared Services (used by all):**
- RAPID_CORE (GAS library)
- RAPID_IMPORT (data ingestion)
- RAPID_API (REST endpoints)
- MCP-Hub (intelligence layer)

**Sales Centers** = QUE modules surfaced as PRODASH views (Medicare, Life, Annuity, Advisory)

**Campaign Engine:** C3 → PRODASH, 60 campaigns, 661 templates, AEP Blackout Oct-Dec

**GHL Integration (retained for M&A):**
- **IMPORT_GHL.gs** (4,394 lines) + **API_GHL_Sync.gs** (1,661 lines) are RETAINED in RAPID_IMPORT/RAPID_API
- Only the GHL *push* code was removed (C3 stubs, PRODASH UI refs) — RPI no longer pushes TO GHL
- The *import/sync* code stays as a ready-made intake tool for GHL-based acquisitions via DAVID/SENTINEL

**Dependency Chain:**
```
RAPID_CORE ← Used by ALL GAS projects (library dependency)
     ↑
RAPID_IMPORT ← Feeds data into SENTINEL + PRODASHX
     ↑
MCP-Hub/healthcare-mcps ← Powers QUE-Medicare quoting
```

---

## Project Locations

```
~/Projects/
├── _RPI_STANDARDS/              # Cross-suite standards
├── RAPID_TOOLS/                 # Shared services (B2E)
│   ├── RPI-Command-Center/      # Leadership visibility
│   ├── CAM/                     # Commission accounting
│   ├── DEX/                     # Document efficiency
│   ├── C3/                      # Content/Campaign manager
│   ├── RIIMO/                   # Operations UI
│   ├── CEO-Dashboard/           # Executive dashboard
│   ├── RAPID_CORE/              # Core GAS library
│   ├── RAPID_IMPORT/            # Data ingestion
│   ├── RAPID_API/               # REST API
│   ├── RAPID_COMMS/             # Comms library (Twilio + SendGrid)
│   ├── Marketing-Hub/           # Visual asset mgmt + design orchestration
│   ├── MCP-Hub/                 # Intelligence + MCPs
│   │   └── drive-tools/         # Drive content dedup + inventory
│   ├── PDF_SERVICE/             # PDF generation + form filling
│   └── The-Machine/             # System architecture visualization
├── SENTINEL_TOOLS/              # B2B Platform
│   ├── DAVID-HUB/               # Entry calculators
│   ├── sentinel/                # Main B2B app (legacy)
│   └── sentinel-v2/             # Main B2B app (current)
└── PRODASHX_TOOLS/              # B2C Platform
    ├── PRODASHX/                # Client portal
    └── QUE/QUE-Medicare/        # Medicare quoting
```

---

## MATRIX Sheets

**MATRIX IDs are managed by `RAPID_CORE.getMATRIX_ID()` — never hardcode them.** **[Hook-enforced: block-hardcoded-matrix-ids]**

For tab routing, schemas, and configuration: read `RAPID_CORE/CORE_Database.gs` directly (TABLE_ROUTING constant).

**Schema Rules:**
- `TAB_SCHEMAS` define column order for all MATRIX writes
- Missing schema fields cause **silent data loss** — always verify schema completeness
- New fields flow: `RAPID_CORE` schemas → `RAPID_API` SETUP → `RAPID_IMPORT` maps → `watcher.js`

---

## Key API Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| healthcare-mcps | `https://que-api-r6j33zf47q-uc.a.run.app` | Medicare data API (Cloud Run, always on) |
| RAPID_API | GAS Web App | REST endpoints for external integrations |

**RAPID_API Deployment Notes:**
- PRODASH calls RAPID_API deployment `AKfycbyf9IAI3...` (Workspace), NOT `AKfycbwaCzn...` (Primary) — both must stay synced
- `client_status` carries classification, NOT `client_classification`

**Healthcare-mcps (Cloud Run):**
- Production: `https://que-api-r6j33zf47q-uc.a.run.app` (4Gi/2CPU, min 1 instance)
- Auth: `@retireprotected.com` domain via OIDC identity token
- GAS callers use `ScriptApp.getIdentityToken()` for Bearer auth
- Local dev: `npm run que-api` in `MCP-Hub/healthcare-mcps/` (port 3456)

**To run Drive content dedup:**
```bash
cd /Users/joshd.millang/Projects/RAPID_TOOLS/MCP-Hub/drive-tools
npm run dedup          # Full scan + report
npm run dedup:report   # Report only (cached inventory)
npm run inventory      # Inventory only (no dedup)
```

---

## What I Do NOT Do

| Task | Who Does It |
|------|-------------|
| Run terminal commands | You (Claude Code) |
| Debug code | You |
| Manual file editing | You |
| Git operations | You |
| Deployment | You (OPS phase) |

**Exceptions** (I do manually):
- `clasp login` when OAuth expires
- First-time GAS deployment auth
- Business decisions and approvals

---

## Your Role: Empowered GA

Per `CLAUDE_CODE_EXECUTION.md`:

```
I (JDM) say what I want (CEO role)
    ↓
You (Claude Code GA) read briefings + scope
    ↓
You spawn SPC agents via Task tool
    ↓
SPCs work in parallel, report back
    ↓
You validate completeness
    ↓
You execute OPS phase (deploy)
    ↓
You report results to me
```

**You are not waiting for permission. You are executing.**

---

## Default Behavior: Plan Mode

**ALWAYS default to Plan Mode (EnterPlanMode) for non-trivial implementation tasks.** Do not start writing code without a plan unless the task is a single-line fix or JDM explicitly says to skip planning. This prevents wasted effort and ensures alignment before execution.

---

## Session Protocol

### Starting
1. JDM gives task or context
2. Read project CLAUDE.md (if exists in current directory)
3. **Survey the ecosystem** — check the project's parent directory (e.g., `RAPID_TOOLS/`, `SENTINEL_TOOLS/`, `PRODASHX_TOOLS/`) to understand sibling projects, shared dependencies, and available infrastructure. Inventory loaded MCP tools (`ToolSearch` / `ListMcpResourcesTool`). You need the full toolbox before you start swinging.
4. **Run Reference Detection Protocol** (Belt & Suspenders) - report what docs you loaded
5. **Hookify check** — verify hookify rules are symlinked from `_RPI_STANDARDS/hookify/` into the project's `.claude/` directory. Compare counts, link any missing rules, report status.
6. Begin work immediately
7. Report completion, not progress

### During Work
- Don't narrate what you're doing
- Don't ask "should I continue?"
- Do the work, report results
- If blocked, explain why and what you need

### Ending
- Commit and push all changes
- Report final status clearly
- If significant context for next session: note it in response

---

## Signature Phrases

- **#RunningOurOwnRACE** - The mission
- **#We'reWithDAVID** - B2B positioning
- **#SendIt** - Deploy to production
- **LFG** - Let's fucking go
- **SKODEN** - Let's go then
- **"We're Your People™"** - RPI positioning

---

## The Operating System

The OS is the governance layer of The Machine. Full docs: `_RPI_STANDARDS/reference/os/`

```
The Machine (the business)
  └── The Operating System (governance layer)
        ├── Standards (os/STANDARDS.md)           ← what the rules ARE
        ├── Posture (os/POSTURE.md)               ← who has access, what's verified
        ├── The Immune System (os/IMMUNE_SYSTEM.md) ← enforcement + learning loop
        ├── Monitoring (os/MONITORING.md)          ← watchdogs + health checks
        └── Operations (os/OPERATIONS.md)         ← human processes + checklists
```

**Enforcement hierarchy:** Hookify rules (code-level) > CLAUDE.md (instruction-level) > MEMORY.md > Knowledge Pipeline

### The Immune System (Hookify)

The **hookify plugin** (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/`) — 21 rules, 4 hook events, enforces standards in real-time. Full reference: `_RPI_STANDARDS/reference/os/IMMUNE_SYSTEM.md`

**Rule Types** (all `.local.md` files in `_RPI_STANDARDS/hookify/`):

**Tier 1 — Block Rules** (`action: block`, `event: file`):
`block-hardcoded-secrets`, `block-credentials-in-config`, `block-phi-in-logs`, `block-anyone-anonymous-access`, `block-hardcoded-matrix-ids`, `block-alert-confirm-prompt`, `block-drive-url-external`, `block-forui-no-json-serialize`, `block-hardcoded-colors`, `block-let-module-caching`

**Tier 2 — Warn Rules** (`action: warn`, `event: file`):
`warn-date-return-no-serialize`, `warn-missing-structured-response`, `warn-modal-no-flexbox`, `warn-phi-in-error-message`, `warn-plain-person-select`, `warn-inline-pii-data`

**Intent Rules** (`action: warn`, `event: prompt`):
`intent-session-start` (triggers session protocol), `intent-sendit` (triggers 6-step deploy), `intent-immune-system-check` (triggers pipeline + compliance briefing)

**Quality Gates** (`action: block`, `event: bash`):
`quality-gate-deploy-verify` (blocks deploy without verify), `quality-gate-commit-remind` (blocks commit without deploy)

### Rule Propagation

Rules live in `_RPI_STANDARDS/hookify/` and are symlinked to all 18 projects via:
```bash
~/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh
```

### Closed Loop (LIVE)
Sessions generate violations > violation logging > knowledge-promote.js (4am) > Slack DM digest to JDM > compliance-history.json trend tracking > CLAUDE.md adjusted > next session smarter. Say "check the immune system" for a structured briefing.

### Emergency Escape Hatch
- Disable hookify: Remove `"hookify@claude-plugins-official": true` from `~/.claude/settings.json`
- Disable one rule: Set `enabled: false` in the rule's frontmatter, or delete the symlink
- Rules only apply in projects where `.claude/hookify.*.local.md` symlinks exist

---

## Hall of Fame

- **Ulysses Sayekama** — WhisperFlow's legendary transcription of "needless to say" (2026-02-17, during Signal→Gradient transition work). JDM declared it "fucking classic" and demanded it be immortalized. RIP Ulysses.

---

## Session URLs
<!-- Claude: Open these in browser at session start -->
| Resource | URL |
|----------|-----|
| GitHub | https://github.com/retirementprotectors/RPI-Standards |

---

*This context applies to ALL sessions. Project-specific context comes from project CLAUDE.md files.*
- **Bash working directory persists** between tool calls — always use absolute paths or explicit `cd` for multi-project deploys
