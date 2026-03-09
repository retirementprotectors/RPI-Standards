# Sales Casework Workbench — Implementation Plan

## Context

The team is finding sales opportunities that need to be worked before they enter formal QUE flows (Annuity, Life, Medicare). Today, PRODASHX has the pipeline infrastructure (Orange > Blue > Yellow > Green > Red) and Yellow Stage = "Case Building" — but the Yellow Stage UI is a **read-only scoreboard**, not a workbench. The team sees report counts but can't:

- Track granular tasks per case
- Update report statuses from the UI (backend exists, no UI wired)
- See client-aware QUE module status (backend exists, UI is static)
- Add case notes or collaborate
- See their personal case queue filtered and prioritized

**Goal:** Turn Yellow Stage into a real Casework Workbench where the team can crank on opportunities NOW, with or without QUE-Annuity/Life being built yet.

---

## What Changes

| Layer | File | Change |
|-------|------|--------|
| Schema | `RAPID_CORE/CORE_Database.gs` | Add `_CASE_TASKS` to TABLE_ROUTING + TAB_SCHEMAS |
| API | New `RAPID_API/API_Task.gs` | Full CRUD: list, get, create, update, delete |
| API | `RAPID_API/Code.gs` | Register `task/tasks` route + SETUP column creator |
| Backend | New `PRODASHX/PRODASH_CASEWORK.gs` | Layer 2/3: task scanning, case detail assembly, notes, readiness calc |
| Backend | `PRODASHX/PRODASH_YELLOW_STAGE.gs` | Minor: add casework data to yellow stage scan |
| Frontend | `PRODASHX/Index.html` | New sub-tabs in Yellow Stage: My Cases, Case Detail |
| Frontend | `PRODASHX/Scripts.html` | JS for My Cases list, Case Detail view (tasks, reports, QUE, notes) |
| Frontend | `PRODASHX/Styles.html` | Minimal additions for task list, readiness bars, note cards |

**No new GAS projects. No new MATRIX spreadsheets. Everything lives in the existing PRODASHX + RAPID_API stack.**

---

## Data Model

### New: `_CASE_TASKS` (PRODASH_MATRIX)

```
TABLE_ROUTING: '_CASE_TASKS': 'PRODASH'

TAB_SCHEMAS:
_CASE_TASKS: [
  'task_id',            // UUID primary key
  'opportunity_id',     // FK to _OPPORTUNITIES
  'client_id',          // FK to _CLIENT_MASTER (denormalized for queries)
  'product_line',       // medicare | annuity | life | bdria | banking | general
  'title',              // Short description
  'description',        // Optional detail
  'status',             // open | in_progress | complete | blocked
  'assigned_to',        // User email
  'due_date',           // Target date
  'completed_date',     // When marked complete
  'sort_order',         // Display ordering within product_line
  'created_by',         // Who created
  'created_at',
  'updated_at'
]
```

### Enhanced: `type_fields` JSON on Opportunities

Add `casework` key alongside existing `discovery_kit` and `report_order`:

```json
{
  "discovery_kit": { "..." },
  "report_order": { "..." },
  "casework": {
    "entered_yellow": "2026-02-24",
    "product_lines": ["medicare", "annuity"],
    "notes": [
      { "id": "uuid", "date": "2026-02-24T10:30:00Z", "author": "vinnie@retireprotected.com", "text": "Client prefers FIA over MYGA" }
    ]
  }
}
```

Notes live in `type_fields.casework.notes` (lightweight, per-opportunity). Tasks live in `_CASE_TASKS` tab (queryable across all cases for "My Cases" view).

---

## API Layer: `RAPID_API/API_Task.gs`

Follow exact `API_Opportunity.gs` pattern:

```
const TASK_TAB = '_CASE_TASKS';

const API_Task = {
  handleRequest(e, method, pathParts) { ... }
};

GET    /task              — list (filters: opportunity_id, client_id, assigned_to, status, product_line)
GET    /task/{id}         — single task
POST   /task              — create (auto UUID, timestamps)
PUT    /task/{id}         — update any fields
DELETE /task/{id}         — soft delete (status = 'archived')
POST   /task/bulk         — create multiple tasks at once (for template application)
```

Uses `getProdashData_()` for list, `RAPID_CORE.insertRow()` for create, `RAPID_CORE.updateRow()` for update.

### Route Registration in Code.gs

Add to `handleRequest` dispatcher:
```javascript
} else if (pathParts[0] === 'task' || pathParts[0] === 'tasks') {
  return API_Task.handleRequest(e, method, pathParts);
}
```

Add `_CASE_TASKS` columns to `SETUP_AddMissingColumns`.

---

## Backend Layer: `PRODASHX/PRODASH_CASEWORK.gs`

### Layer 2 Functions

**`scanCaseworkData_(scanData)`**
- Calls `scanStageOpportunities_('yellow')` for all yellow-stage opps
- For each opp: fetches tasks via `callRapidAPI('task', { opportunity_id })`, calculates readiness per product line
- Returns `{ cases: [...], stats: { totalCases, myCase, staleCases, tasksOpen, tasksComplete } }`

**`getCaseDetail_(oppId, scanData)`**
- Gets opportunity from API (with type_fields)
- Gets client info from scanData
- Gets all tasks for this opportunity
- Gets report order status (reuses existing `getReportOrderForOpp_`)
- Gets QUE module status (reuses existing `getQUEModuleStatus_`)
- Calculates product line readiness (% tasks complete per line)
- Returns assembled case detail object

**`getProductLineReadiness_(tasks)`**
- Groups tasks by `product_line`
- Returns `{ medicare: { total, complete, pct }, annuity: { ... }, ... }`

**`addCaseNote_(oppId, noteText, author)`**
- Reads opp type_fields, appends to `casework.notes` array
- Writes back via PUT

**`getTaskTemplates_(clientAccounts)`**
- Based on which account types exist, returns default task lists per product line
- E.g., client has annuity accounts -> returns 4 standard annuity casework tasks
- Templates are a constant in this file (easy to edit, no config sheet needed)

**`applyCaseTaskTemplates_(oppId, clientId, clientAccounts)`**
- Calls `getTaskTemplates_()`, then bulk-creates tasks via `callRapidAPI('task/bulk', {}, 'POST', tasks)`

### Layer 3 Functions (UI-callable)

All follow the pattern: guard input, try/catch, `JSON.parse(JSON.stringify(result))`.

```
uiGetMyCases(userEmail)              — filtered to assigned_to, returns case list + stats
uiGetCaseDetail(oppId)               — full case assembly
uiCreateTask(oppId, taskData)        — single task create
uiUpdateTask(taskId, updates)        — status change, reassign, etc.
uiDeleteTask(taskId)                 — soft delete
uiApplyTaskTemplates(oppId)          — auto-generate standard tasks from templates
uiAddCaseNote(oppId, noteText)       — append note
uiMoveCaseStage(oppId, direction)    — move to Green (forward) or back to Blue
```

---

## Frontend: Yellow Stage Enhancement

### Updated Sub-Tab Structure

```
Yellow Stage
├── My Cases        ← NEW (default tab)
├── Case Detail     ← NEW (loads when case selected)
├── Case Central    ← EXISTS (routing sheet)
└── QUE Modules     ← EXISTS (enhance to be client-aware)
```

### My Cases Tab

**Stat Cards (top):**
```
[My Cases]    [Tasks Open]    [Stale (7d+)]    [Ready for Green]
```

**Filter Bar:**
- Assigned To: dropdown (me / all / specific person via Smart Lookup)
- Product Line: checkbox badges (Medicare / Annuity / Life / BD-RIA)
- Status: toggle (Active / Stale / All)

**Case Table:**

| Client | Product Lines | Tasks | Reports | Days in Yellow | Actions |
|--------|--------------|-------|---------|---------------|---------|
| Badge icons per acct type | 3/7 done | 4/9 complete | 12 | [Open] |

- Sorted: stale first (amber row), then by days descending
- Click "Open" -> switches to Case Detail tab, loads that case

### Case Detail Tab

**Header Bar:**
```
← Back to My Cases    SMITH, JOHN    Agent: Vinnie V.    [← Blue] [Green →]
```

**Product Line Readiness Strip:**
```
Medicare ████████░░ 80%    Annuity ███░░░░░░░ 30%    Life ░░░░░░░░░░ 0%
```
Progress = tasks complete / total tasks for that product line.

**Four Section Cards:**

**A. Tasks**
- Grouped by product_line headers
- Each task: checkbox + title + assigned_to badge + due_date + status chip
- Click checkbox -> calls `uiUpdateTask(id, { status: 'complete' })`
- [+ Add Task] button per product line group
- [Apply Templates] button if no tasks exist yet (calls `uiApplyTaskTemplates`)
- Assignment uses Smart Lookup (per standards)

**B. Reports**
- Reuses existing report order data from `type_fields.report_order`
- Status dropdown toggles per report (Pending / Submitted / Complete)
- Calls existing `uiUpdateReportStatus()` — finally wired to UI
- Progress bar: X/Y complete

**C. QUE Modules**
- Calls `uiGetQUEModuleStatus(clientId)` — now client-aware
- Shows account count per module + link to open QUE (Medicare only today)
- "Coming Soon" for Life/Annuity (but tasks can still be tracked above)

**D. Notes**
- Reverse-chronological list of timestamped notes
- [+ Add Note] textarea + submit button
- Each note: date, author email, text

---

## Task Templates (Default Tasks by Product Line)

Defined as a constant in `PRODASH_CASEWORK.gs`:

```javascript
const TASK_TEMPLATES_ = {
  medicare: [
    { title: 'Run QUE-Medicare quoting', sort_order: 1 },
    { title: 'Generate Medicare Recommendation', sort_order: 2 },
    { title: 'Client review of Medicare options', sort_order: 3 }
  ],
  annuity: [
    { title: 'Pull current annuity statements', sort_order: 1 },
    { title: 'Run income projections', sort_order: 2 },
    { title: 'Compare FIA/MYGA options', sort_order: 3 },
    { title: 'Build annuity recommendation', sort_order: 4 }
  ],
  life: [
    { title: 'Pull current life policy details', sort_order: 1 },
    { title: 'Run IFI analysis', sort_order: 2 },
    { title: 'Compare carrier options', sort_order: 3 },
    { title: 'Build life recommendation', sort_order: 4 }
  ],
  bdria: [
    { title: 'Pull current investment statements', sort_order: 1 },
    { title: 'Order Gradient reports', sort_order: 2 },
    { title: 'Review Morningstar analysis', sort_order: 3 },
    { title: 'Build portfolio recommendation', sort_order: 4 }
  ],
  general: [
    { title: 'Verify all authorizations signed', sort_order: 1 },
    { title: 'Confirm all data collected', sort_order: 2 },
    { title: 'Assemble Case Central package', sort_order: 3 }
  ]
};
```

When `uiApplyTaskTemplates(oppId)` is called, tasks are created for every product line where the client has accounts, plus `general` always.

---

## Build Phases

### Phase 1: Data + API (RAPID_CORE + RAPID_API)
- Add `_CASE_TASKS` to TABLE_ROUTING + TAB_SCHEMAS in CORE_Database.gs
- Create `API_Task.gs` with full CRUD
- Register route in Code.gs + add SETUP columns
- Deploy RAPID_CORE + RAPID_API
- **Verify:** `callRapidAPI('task', {}, 'POST', { ... })` creates a task row

### Phase 2: Backend (PRODASHX)
- Create `PRODASH_CASEWORK.gs` with all Layer 2/3 functions
- Task templates constant
- Notes management via type_fields
- Product line readiness calculation
- **Verify:** `uiGetMyCases('email')` returns structured data

### Phase 3: Frontend — My Cases (PRODASHX)
- Add "My Cases" sub-tab to Yellow Stage in Index.html
- Stat cards, filter bar, case table
- Make My Cases the default Yellow Stage tab
- **Verify:** Navigate to Yellow Stage, see case list with stats

### Phase 4: Frontend — Case Detail (PRODASHX)
- Case Detail sub-tab with header, readiness strip, 4 section cards
- Task CRUD UI (create, complete, assign)
- Report status toggles (wire existing `uiUpdateReportStatus`)
- Client-aware QUE Modules (wire existing `uiGetQUEModuleStatus`)
- Notes UI
- Apply Templates button
- Stage movement buttons
- **Verify:** Open a case, create tasks, update report statuses, add notes, move stages

### Phase 5: Polish + Deploy
- Smart Lookup on task assignment fields
- Stale case highlighting (7+ days no activity)
- Empty states for all sections
- Full deploy: RAPID_CORE > RAPID_API > PRODASHX
- Verify deploy versions match

---

## Files Modified (Summary)

| File | Action | Lines Est. |
|------|--------|-----------|
| `RAPID_CORE/CORE_Database.gs` | Edit (add schema) | +15 |
| `RAPID_API/Code.gs` | Edit (add route + SETUP) | +10 |
| `RAPID_API/API_Task.gs` | **New file** | ~200 |
| `PRODASHX/PRODASH_CASEWORK.gs` | **New file** | ~350 |
| `PRODASHX/PRODASH_YELLOW_STAGE.gs` | Edit (minor integration) | +20 |
| `PRODASHX/Index.html` | Edit (add sub-tabs + views) | +150 |
| `PRODASHX/Scripts.html` | Edit (add JS functions) | +400 |
| `PRODASHX/Styles.html` | Edit (add styles) | +50 |

---

## Verification

1. **Schema:** Run `SETUP_AddMissingColumns` in RAPID_API to create `_CASE_TASKS` tab in PRODASH_MATRIX
2. **API:** POST/GET/PUT/DELETE tasks via `callRapidAPI` from PRODASHX DevTools
3. **Backend:** Run `DEBUG_GetMyCases('test@retireprotected.com')` in PRODASHX
4. **Frontend:** Navigate to Yellow Stage > My Cases > Open a case > Create task > Complete task > Add note > Update report status > Move to Green
5. **Deploy:** Full 6-step deploy on all 3 projects (RAPID_CORE, RAPID_API, PRODASHX) with version verification

---

## What This Enables

**Immediate:** Team can create, assign, track, and complete casework tasks on every opportunity — organized by product line, with notes and collaboration.

**When QUE-Annuity/Life ship:** They plug into the same Case Detail view. The "QUE Modules" section lights up with live links. Task templates can auto-mark QUE-related tasks as complete when the QUE module produces output.

**The team gets a workbench, not a scoreboard.**
