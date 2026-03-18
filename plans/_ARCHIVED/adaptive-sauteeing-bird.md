ARCHIVED: Consolidated into tomachina-epic-roadmap.md on 2026-03-13
# RPI Command Center — Development Roadmap v2.0

## Context

Command Center's backend (4,682 lines GAS) and frontend (1,848 lines JS) are fully operational at v5.1 (@9). All 7 document types have working CRUD, the meeting processor uses Claude for transcript analysis, and the UI is wired end-to-end with navigation, forms, modals, and search.

**The next evolution**: Turn Command Center from a document repository into an **accountability and automation engine**. The 7 phases below build the pipeline: meetings generate action items, action items route to people, people get notified, progress is tracked, leadership has visibility — all automatically — and then integrate the whole thing into RIIMO as a first-class module with proper permissions.

---

## Phase 1: Action Item Tracker (Highest Priority)

**Why**: Meetings without tracked action items = decisions that evaporate. This is the accountability layer everything else depends on.

### Architecture Decision
**New `_ACTION_ITEMS` MATRIX tab** (not derived from meeting JSON).

Reasoning: Action items need independent status tracking. Deriving from meeting JSON means O(N) parsing on every dashboard load, fragile JSON mutation for status updates, and no audit trail. A dedicated tab gives instant filtering, clean status updates, and becomes the canonical source for all downstream features.

### Schema: `_ACTION_ITEMS`
```
id, action, owner, priority, deadline, status, source_meeting_id,
source_meeting_title, source_meeting_date, notes, created_at,
updated_at, completed_at
```
- **Status values**: pending, in-progress, complete, cancelled
- **Priority values**: immediate, near-term, q1

### Backend (New: `CC_ActionItems.gs` ~250 lines)
- `CC_ActionItems.getAll(filters)` — Read all, supports filter: {owner, priority, status, dateFrom, dateTo}
- `CC_ActionItems.updateStatus(id, newStatus, notes)` — Updates status + timestamps
- `CC_ActionItems.syncFromMeeting(meetingId)` — Parses meeting's action_items JSON, upserts into tab (dedup on source_meeting_id + action text)
- `CC_ActionItems.getOverdue()` — Items where deadline < today and status != complete/cancelled
- `CC_ActionItems.getByOwner(ownerName)` — Filtered list for Slack digests

### Backend (Modify)
- **CC_Config.gs**: Add `ACTION_ITEMS` to `CC_TABS` and `CC_SCHEMAS`
- **Code.gs**: Add `uiGetActionItems(filters)`, `uiUpdateActionItemStatus(id, status, notes)`, `uiGetOverdueActionItems()` wrapper functions
- **Code.gs**: Hook `CC_ActionItems.syncFromMeeting()` into `uiSaveMeetingAnalysis()` post-save
- **CC_Dashboard.gs**: Add actionItemsOpen, actionItemsOverdue to stats
- **CC_DevTools.gs**: Add `SETUP_CreateActionItemsTab()` + backfill function

### Frontend (Modify: Index.html + Scripts.html + Styles.html ~380 lines)
- New nav item: "Action Items" in Overview section
- New view: `#view-action-items` with filter bar + table
- Filter controls: Owner dropdown, Priority dropdown, Status dropdown, Date range
- Table columns: Action, Owner, Priority, Deadline, Source Meeting, Status
- Overdue items: red-tinted row highlight
- Inline status dropdown: change status directly from the table
- Dashboard integration: action item counts in stats row

### Verification
1. Run `SETUP_CreateActionItemsTab()` to create tab
2. Backfill from existing meeting analyses
3. Process new transcript — verify auto-population
4. Test inline status updates from UI
5. Test all filter combinations
6. Verify overdue detection with past-deadline items
7. Confirm dashboard stats reflect action item counts

---

## Phase 2: Slack Digest on Save

**Why**: Creates accountability pressure without anyone logging into Command Center. People get their action items in Slack the moment a meeting is processed.

### Architecture Decision
**GAS-side Slack via existing `sendSlackNotification()`** (not MCP tools).

Reasoning: The function already exists in CC_Intake.gs with SLACK_BOT_TOKEN in Script Properties. GAS fires automatically on save — no Claude Code session needed. MCP tools can't be invoked from within a GAS execution context.

### Backend (New: `CC_SlackDigest.gs` ~150 lines)
- `CC_SlackDigest.notifyMeetingProcessed(meetingData)` — Main entry. Groups action items by owner, sends DMs
- `CC_SlackDigest.sendOwnerDM(ownerName, items, meetingTitle, meetingDate)` — Resolves name to Slack ID, sends Block Kit formatted DM with action items + deadlines
- `CC_SlackDigest.postChannelSummary(meetingData, channel)` — Posts formatted meeting summary to designated channel

### Team Slack ID Map (GAS constant)
```
Josh Millang    → U09BBHTN8F2
John Behn       → U09JBHUQ9S9  (always CC'd)
Matt McCormick  → U086YDNC7BK
Nikki Gray      → U08TQVC90DA
Vinnie Vazquez  → U07KXAF8EF4
Jason Moran     → U08AGC03HT9
Aprille Trupiano → U092U7FCCDT
```

### Backend (Modify: Code.gs ~5 lines)
- Hook `CC_SlackDigest.notifyMeetingProcessed()` into `uiSaveMeetingAnalysis()` post-save (try/catch, non-blocking)

### Verification
1. Verify SLACK_BOT_TOKEN in Script Properties
2. Save meeting with items for Matt + Nikki
3. Verify each gets a DM with only their items
4. Verify John gets CC notification
5. Verify channel summary posts correctly
6. Verify empty action items don't generate empty DMs
7. Verify Slack failure doesn't block the save

---

## Phase 3: Auto-Route on Save

**Why**: Zero-friction pipeline from meetings to roadmaps. No manual step required to keep roadmaps current.

### Backend (New: `CC_AutoRoute.gs` ~120 lines)
- `CC_AutoRoute.routeMeetingToRoadmaps(meetingData)` — Extracts action item owners, matches to roadmap people, calls appendToRoadmap()
- `CC_AutoRoute.appendToRoadmap(ownerName, meetingData)` — Finds owner's roadmap, appends new action items (dedup by source_meeting_id), updates current_initiatives if strategic implications reference the owner, logs to _ACTIVITY_LOG

### Owner-to-Roadmap Map
```
Matt McCormick  → Matt McCormick roadmap
Nikki Gray      → Nikki Gray roadmap
Vinnie Vazquez  → Vinnie Vazquez roadmap
Jason Moran     → Jason Moran roadmap
Aprille Trupiano → Aprille Trupiano roadmap
```
Fuzzy matching: Vince/Vinnie, Dr. Aprille/Aprille

### Backend (Modify: Code.gs ~5 lines)
- Hook `CC_AutoRoute.routeMeetingToRoadmaps()` into `uiSaveMeetingAnalysis()` post-save (try/catch, non-blocking)

### Verification
1. Save meeting with action items for Matt
2. Verify Matt's roadmap action_items JSON updated
3. Re-save — verify no duplicates
4. Verify _ACTIVITY_LOG has routing entry
5. Test with owner who has no roadmap — should skip gracefully

---

## Phase 4: Google Meet Auto-Detect

**Why**: The ultimate force multiplier. Team records a meeting, analysis appears in Command Center without anyone doing anything.

### Architecture Decision
**GAS time-driven trigger (10-minute polling)**, not Drive push notifications.

Reasoning: Drive push notifications require a public HTTPS endpoint (can't use org-only GAS web app). The existing polling pattern in CC_Intake.gs already handles dedup. 10-minute intervals are fast enough for meeting recordings.

### Backend (New: `CC_RecordingWatcher.gs` ~200 lines)
- `CC_RecordingWatcher.scanRecordingsFolder()` — Main trigger function. Lists files modified since last scan (stored in Script Properties as LAST_RECORDING_SCAN). Checks for associated transcript docs
- `CC_RecordingWatcher.processNewRecording(file)` — Finds transcript doc, fetches text, calls uiProcessTranscript(), saves analysis
- `CC_RecordingWatcher.findTranscriptDoc(recordingFile)` — Searches parent folder for Google Doc created within 30 min of recording
- `SETUP_CreateRecordingWatcherTrigger()` — Creates 10-minute time-driven trigger

### Configuration
- `RECORDINGS_FOLDER_ID` in Script Properties — points to Meet recordings Drive folder
- `LAST_RECORDING_SCAN` in Script Properties — timestamp watermark

### Verification
1. Set RECORDINGS_FOLDER_ID in Script Properties
2. Place test recording + transcript doc in folder
3. Run scanRecordingsFolder() manually
4. Verify meeting analysis auto-created with correct content
5. Run again — verify dedup
6. Create trigger — verify scheduled execution

---

## Phase 5: Weekly Slack Digest

**Why**: Recurring accountability. Every Monday, everyone sees their open items. Overdue items can't hide.

### Backend (Add to `CC_SlackDigest.gs` ~80 lines)
- `CC_SlackDigest.sendWeeklyDigest()` — Reads all open items from _ACTION_ITEMS, groups by owner, DMs each owner with: total open, overdue count, overdue items list, upcoming deadlines this week. Posts aggregate summary to channel
- `SETUP_CreateWeeklyDigestTrigger()` — Monday 8:00 AM CT trigger

### Verification
1. Create action items with varying deadlines and owners
2. Run sendWeeklyDigest() manually
3. Verify per-owner DMs with correct items
4. Verify aggregate channel summary
5. Create trigger — verify Monday execution

---

## Phase 6: Weekly Scorecard View (Placeholder)

**Why**: Leadership metrics dashboard. John Behn is defining the scorecard — we scaffold now, populate later.

### Frontend Only (~55 lines)
- Nav item: "Weekly Scorecard" in Overview section
- Placeholder view with empty state: "Coming soon. John Behn is defining the scorecard metrics."
- Navigation wiring in Scripts.html

### No backend work until John provides scorecard definition.

---

## Phase 7: RIIMO Integration + Permissions

**Why**: Command Center can't live as a standalone URL that leadership has to bookmark. It belongs inside RIIMO — the operations hub everyone already uses. Proper permissions ensure only EXECUTIVE+ users see it.

### Architecture (Already Wired)
RIIMO's module system is fully modular. Command Center is **already registered** in `PROJECT_REGISTRY` as `RPI_COMMAND_CTR` with its deployment ID. Integration requires only 3 changes across 2 projects.

### Step 1: Register Module in RAPID_CORE (~10 lines)
**File**: `RAPID_CORE/CORE_Entitlements.gs`

Add to `MODULES`:
```javascript
RPI_COMMAND_CENTER: {
  name: 'Command Center',
  fullName: 'Leadership Command Center',
  icon: '🎯',
  description: 'Meeting intelligence, action item tracking, and leadership roadmaps',
  status: 'active',
  suite: 'ADMIN_TOOLS',
  minUserLevel: 'EXECUTIVE'
}
```

Add to `TOOL_SUITES.ADMIN_TOOLS.modules` array:
```javascript
modules: ['ORG_STRUCTURE', 'PERMISSIONS', 'RPI_COMMAND_CENTER']
```

### Step 2: Wire Module Map in RIIMO (~1 line)
**File**: `RIIMO/RIIMO_Core.gs`

Add to `MODULE_PROJECT_MAP`:
```javascript
RPI_COMMAND_CENTER: 'RPI_COMMAND_CTR'
```

The `PROJECT_REGISTRY` entry already exists:
```javascript
RPI_COMMAND_CTR: {
  name: 'Command Center',
  deployId: 'AKfycbx2nKGakOwc_5wLVPmmseS5__N4cbFTGh1eUFtQLF_0BrJI_gQKcDCM_zACvdgno0OX',
  type: 'webapp',
  platform: 'B2E'
}
```

### Step 3: Deploy Both Projects
1. Deploy RAPID_CORE (clasp push + version) — library update propagates to all consumers
2. Deploy RIIMO (clasp push + version + deploy) — picks up new RAPID_CORE version
3. No HTML/frontend changes needed — RIIMO auto-loads modules from backend data

### Access Control
- **OWNER (Josh, John)**: Full access — VIEW, EDIT, ADD
- **EXECUTIVE**: Full access — VIEW, EDIT, ADD
- **LEADER**: No access (minUserLevel: EXECUTIVE)
- **USER**: No access

Per-user overrides available via `_USER_HIERARCHY` tab in RAPID_MATRIX if needed (e.g., granting a specific LEADER access).

### How It Works in RIIMO
1. User opens RIIMO → sidebar shows "Admin" section (EXECUTIVE+ only)
2. Admin section contains: Org Structure, Permissions, **Command Center**
3. Click Command Center → module card with description + "Launch" button
4. Launch opens Command Center web app in new tab
5. Command Center authenticates via org-only GAS access (same Google session)

### Verification
1. Deploy RAPID_CORE, verify version
2. Deploy RIIMO, verify version
3. Log in as OWNER → see Command Center in Admin nav → launch works
4. Log in as EXECUTIVE → see Command Center in Admin nav → launch works
5. Log in as LEADER → Command Center NOT visible
6. Log in as USER → Command Center NOT visible
7. Verify Command Center web app loads correctly from RIIMO launch

---

## Implementation Sequence

| Order | Phase | Depends On | New Files | Est. Lines | Key Risk |
|-------|-------|------------|-----------|------------|----------|
| 1 | Action Item Tracker | — | CC_ActionItems.gs | ~800 | Long save flow |
| 2 | Slack Digest | Phase 1 | CC_SlackDigest.gs | ~150 | Slack rate limits |
| 3 | Auto-Route | Phase 1 | CC_AutoRoute.gs | ~120 | Name matching |
| 4 | Scorecard Placeholder | — | — | ~55 | None |
| 5 | Recording Watcher | Phases 2+3 | CC_RecordingWatcher.gs | ~200 | Transcript detection |
| 6 | Weekly Digest | Phases 1+2 | — | ~80 | Rate limits at scale |
| 7 | RIIMO Integration | Phases 1-3 stable | — | ~15 | Multi-project deploy |

**Total**: ~1,420 new lines across 4 new GAS files + modifications to 8 existing files (across 3 projects).

Phase 4 (scorecard placeholder) can run in parallel with anything.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| `uiSaveMeetingAnalysis()` becomes slow with sync + Slack + route | All downstream calls wrapped in try/catch (non-blocking). Save completes first. Refactor to async queue if needed. |
| Slack rate limits (20 msgs/min) | Typical meeting = 2-5 DMs + 1 channel post. Well within limits. Weekly digest batches with 1s delays. |
| Action item dedup on re-save | Composite key: source_meeting_id + normalized action text. Re-saves update, not duplicate. |
| Owner name mismatch across systems | Exact match against SLACK_TEAM_MAP + ROADMAP_OWNER_MAP. Fuzzy fallback for Vince/Vinnie, Dr. Aprille/Aprille. |
| Recording watcher false positives | Check file MIME type + creation timestamp. Only process recordings with associated transcript docs. |

---

## The Full Pipeline (When Complete)

```
Team records a Google Meet
    ↓ (Phase 4: auto-detect)
Recording Watcher finds transcript
    ↓
Claude analyzes transcript → Meeting Analysis
    ↓ (Phase 1: sync)
Action items extracted → _ACTION_ITEMS tab
    ↓ (Phase 2: Slack)
Each owner gets DM with their items
John Behn gets CC on everything
Channel gets meeting summary
    ↓ (Phase 3: auto-route)
Roadmaps auto-updated with new items
    ↓ (Phase 1: tracker)
Action Item Tracker shows all open items
Overdue items highlighted
    ↓ (Phase 5: weekly)
Monday 8am: everyone gets accountability digest
    ↓ (Phase 6: scorecard)
Leadership sees metrics dashboard
    ↓ (Phase 7: RIIMO integration)
All of this accessible from RIIMO Admin nav
EXECUTIVE+ only, proper permissions
One hub, one login
```

**The end state**: A meeting happens → everything downstream is automatic. No manual steps. No items lost. No decisions evaporate. Leadership accesses it all through RIIMO — one login, one hub, proper permissions. The Machine runs itself.

---

*RPI Command Center v2.0 — Development Roadmap*
*Created: 2026-03-03*
*Author: Claude Code GA for JDM*
