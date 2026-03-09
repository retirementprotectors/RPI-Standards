# RIIMO v3.0 — Four Major Enhancements

## Context

RIIMO v2.2.1 is functional but surface-level. The dashboard shows passive metrics nobody acts on. Authorization is coarse (suite-level toggles). Onboarding is 7 hollow stages with no actual tasks. Job descriptions are manual .xlsx files that take forever and can't be delegated. This plan transforms RIIMO from an operations dashboard into a true operations **command center** — where people, permissions, processes, and positions are all managed from one place.

---

## Phase Order & Dependencies

```
Phase 1: ENTITLEMENTS v2 (foundation — everything else needs "who can do what")
    ↓
Phase 2A: ONBOARDING + TASK SYSTEM (needs entitlements for auto-assigning access)
Phase 2B: JOB DESCRIPTION MODULE (needs org structure, feeds into onboarding)
    ↓
Phase 3: DASHBOARD OVERHAUL (needs all the above to have data worth displaying)
```

---

## Phase 1: Authorization / Entitlements v2

**Problem:** Current model = 4 user levels + suite-level toggles. No per-module control in UI. No action-level permissions (VIEW/EDIT/ADD). No way for admins to entitle specific people to specific things.

**Outcome:** Per-module, action-level entitlements managed in RIIMO, consumed by all platforms.

### Schema Changes

**`_USER_HIERARCHY`** — add 2 columns:
| Column | Type | Purpose |
|--------|------|---------|
| `module_permissions` | JSON | `{"C3": ["VIEW","EDIT","ADD"], "CAM": ["VIEW"]}` |
| `role_template_id` | String | Links to job templates (Phase 2B) |

Migration is additive — no existing data touched.

### Backend (`RIIMO_Core.gs`)

- Add `MODULE_ACTIONS` constant: `{ VIEW, EDIT, ADD }`
- Modify `userHasModuleAccess(email, moduleKey, action)` — add optional action param
- Modify `getUserHierarchy()` — parse new `module_permissions` column
- Add `getUserEntitlements(email)` — full entitlements object for cross-platform use

### Backend (`RIIMO_OrgAdmin.gs`)

- Add `updateUserModulePermissions(userId, modulePermissions)`
- Add `getEntitlementsForPlatform(email, platform)` — what SENTINEL/PRODASH read

### Backend (`Code.gs`)

- `uiGetUserEntitlements(userId)`
- `uiUpdateModulePermissions(userId, modulePermissions)`
- `uiGetModuleActions()`

### Frontend (`Index.html`)

Overhaul Permissions admin tab:
- Expandable user cards (not just a list)
- Per-module toggle chips with VIEW/EDIT/ADD checkboxes
- Smart Lookup for reports_to
- Bulk permission templates (apply same perms to multiple users)

### Cross-Platform Propagation

RIIMO writes → `_USER_HIERARCHY` in RAPID_MATRIX → SENTINEL/PRODASH read via RAPID_CORE. Single source of truth, no sync needed. Add `RAPID_CORE.getUserEntitlements(email)` for platforms to call.

### Files Modified
- `RIIMO_Core.gs` — MODULE_ACTIONS, userHasModuleAccess(), getUserHierarchy()
- `RIIMO_OrgAdmin.gs` — new permission CRUD functions
- `Code.gs` — new uiXxx() endpoints
- `RIIMO_MATRIX_Setup.gs` — migration function for new columns
- `Index.html` — Permissions tab overhaul

---

## Phase 2A: Onboarding + Task System

**Problem:** Current onboarding has 7 abstract stages with no actual tasks. JDM's spreadsheet has ~70 real tasks across 5 categories. No way to track what's done, who's responsible, or what varies by role. LC3 (licensing/contracting) for producers doesn't exist yet.

**Outcome:** Three-level hierarchy (Pipeline → Stages → Tasks), role-based task generation, task ownership, LC3 pipelines for producers.

### Architecture: Pipeline → Stages → Tasks

**Stages** = the 5 spreadsheet categories (replace current 7 abstract stages):

| Stage | Owner | Task Count |
|-------|-------|-----------|
| HR/Payroll/Benefits | Shane (CFO) | 6 |
| Operations/Systems | Matt (COO) | 14 |
| Tech Stack | Jason (CTO) | 4 |
| Branding/Identity | (varies) | 16 |
| Specialist/LC3 | Shane | 21 |

**Tasks** = individual items within each stage, auto-generated based on role type.

**Role types** (from spreadsheet columns): Medicare Sales, Medicare Support, Retirement Sales, Retirement Support, Executive/Leadership

### New Pipelines

| Pipeline | Purpose | Stages |
|----------|---------|--------|
| `ONBOARDING` | Employee onboarding | HR → Systems → Tech → Brand → LC3 |
| `LC3_INTERNAL` | New hires getting licensed | Licensing → Contracting → Certs → Carrier Releases → Activation |
| `LC3_EXTERNAL` | M&A/partnership producers | Intake → License Review → Contracting → BOB Transfer → Carrier Releases → Activation |

### New MATRIX Tabs

**`_TASK_TEMPLATES`** — master list of all possible tasks (seeded from spreadsheet):
- template_id, pipeline_key, stage_id, task_name, task_description, task_order, default_owner, role_applicability (JSON), is_required, status

**`_ONBOARDING_TASKS`** — per-record task instances:
- task_id, queue_id (FK), stage_id, task_name, task_order, owner_email, status (pending/in_progress/completed/skipped), completed_by, completed_at, notes, role_applicability, created_at, updated_at

### _ONBOARDING_QUEUE Schema Additions
- `role_type` — determines which tasks get generated
- `task_count` / `tasks_completed` — denormalized for dashboard speed

### New Backend File: `RIIMO_Tasks.gs`

- `getTaskTemplates(pipelineKey)`
- `generateTasksForQueue(queueId, pipelineKey, roleType)` — creates task records from templates filtered by role
- `getTasksForQueue(queueId)` — returns tasks grouped by stage
- `updateTask(taskId, updates)`
- `completeTask(taskId, completedBy)`
- `skipTask(taskId, reason)`
- `getTaskProgress(queueId)` — completion stats per stage
- `reassignTask(taskId, newOwnerEmail)`

### Code.gs Endpoints
- `uiGetTaskTemplates(pipelineKey)`
- `uiGenerateOnboardingTasks(queueId, roleType)`
- `uiGetQueueTasks(queueId)`
- `uiUpdateTask(taskId, updates)` / `uiCompleteTask(taskId)` / `uiSkipTask(taskId, reason)`
- `uiGetTaskProgress(queueId)`
- `uiSaveTaskTemplate(templateData)` — admin template editing
- `uiGetLC3QueueData(lc3Type)`

### Frontend Changes

1. **Queue detail view** — expandable accordion per stage:
   - Stage header with progress bar (e.g., "HR/Payroll 3/6")
   - Task rows: checkbox, name, owner, status badge, complete/skip buttons
   - Task-level notes
   - Filter by owner/status/stage

2. **Queue form** — add role_type dropdown that drives task generation

3. **LC3 pipeline tabs** — two new admin tabs for LC3 Internal/External

4. **Task Template Admin** — sub-section in Pipeline Config for managing the master task list

5. **Sidebar** — add LC3 Internal + LC3 External under Pipelines

### Seed Data
Load all ~70 tasks from the spreadsheet into `_TASK_TEMPLATES` via `SETUP_SeedTaskTemplates()`:
- Map role applicability from the x-marks in columns B-F
- Map owners from section headers (Shane=HR/LC3, Matt=Ops, Jason=Tech)

### Files Modified/Created
- **NEW:** `RIIMO_Tasks.gs` (~400-500 lines)
- `RIIMO_Pipelines.gs` — reorganize ONBOARDING stages, add LC3 pipelines
- `RIIMO_MATRIX_Setup.gs` — create new tabs, seed task templates
- `Code.gs` — new uiXxx() endpoints
- `Index.html` — task accordion UI, LC3 tabs, queue form updates

---

## Phase 2B: Job Description Module

**Problem:** Job descriptions are manual .xlsx/.docx files — painful to create, time-consuming, impossible to delegate. Structure: role → weekly schedule → pipeline/module/platform ownership → expectations → goals → metrics → rewards. Needs systematization.

**Outcome:** Template-based job description generator tied to org structure. Own module in RIIMO.

### New MATRIX Tab: `_JOB_TEMPLATES`

| Column | Type | Purpose |
|--------|------|---------|
| template_id | UUID | Primary key |
| role_name | String | "Medicare Sales Representative" |
| division_id | String | FK to _COMPANY_STRUCTURE |
| unit_id | String | FK to _COMPANY_STRUCTURE |
| team | String | Team name |
| status | String | active/draft/archived |
| weekly_schedule | JSON | `{"mon":"Office","tue":"Field",...}` |
| pipeline_ownership | JSON | Which pipelines this role manages |
| module_ownership | JSON | Which modules this role uses |
| platform_ownership | JSON | Which platforms |
| minimum_expectations | JSON | Array of expectation items |
| goals | JSON | Array of goal items |
| performance_metrics | JSON | Scoreboard metric definitions |
| rewards | JSON | Benefits, comp, bonus structure |
| description_html | String | Generated output |
| created_by, created_at, updated_at | String | Metadata |

### New Backend File: `RIIMO_JobTemplates.gs`

- `getJobTemplates(filters)` — list with division/unit/status filters
- `getJobTemplate(templateId)` — full detail
- `saveJobTemplate(data)` — create/update
- `deleteJobTemplate(templateId)` — soft delete
- `generateJobDescription(templateId)` — produces formatted output from template data
- `cloneJobTemplate(templateId)` — duplicate for customization
- `linkTemplateToUser(templateId, userId)` — sets role_template_id on _USER_HIERARCHY

### Frontend: New Admin Module

Add "Job Templates" to Admin sidebar:

1. **List View** — table: Role Name, Division, Unit, Status, Last Updated. Actions: Edit, Clone, Generate, Delete.

2. **Template Editor** — multi-section form:
   - **Identity**: Role name, division (Smart Lookup), unit, team
   - **Schedule**: Weekly grid (Mon-Fri) with day-type dropdowns (Office/Field/Remote/Off)
   - **Ownership**: Checkbox lists for pipelines, modules, platforms
   - **Expectations**: Dynamic list builder
   - **Goals**: Dynamic list builder
   - **Metrics**: Scoreboard builder (metric name, target, unit of measure)
   - **Rewards**: Benefits checklist, comp fields, bonus criteria

3. **Preview/Generate**: Formatted job description output. Copy button. Future: export to Google Doc.

### Onboarding Integration
- Queue form optionally links to a job template
- If linked, auto-generates Job Description as first HR task
- Template's `module_ownership` auto-populates the user's `assigned_modules`

### Files Modified/Created
- **NEW:** `RIIMO_JobTemplates.gs` (~300-400 lines)
- `RIIMO_MATRIX_Setup.gs` — create `_JOB_TEMPLATES` tab
- `Code.gs` — new uiXxx() endpoints
- `Index.html` — Job Templates module UI

---

## Phase 3: Dashboard Overhaul

**Problem:** Current dashboard = 12 passive metric cards in a grid. Nobody acts on them. Needs to be a command center that answers "What needs my attention RIGHT NOW?" in 3 seconds.

**Outcome:** Role-based, actionable operations command center.

### Layout (OWNER/EXECUTIVE View)

```
+--------------------------------------------------+
| COMMAND BAR (alerts: overdue tasks, errors, queue)|
+--------------------------------------------------+
| PIPELINE SNAPSHOT      | SYSTEM HEALTH            |
| (Kanban-style counts   | (3 MATRIX status +       |
|  across all queues)    |  error rate indicator)    |
+--------------------------------------------------+
| MY TASKS               | QUICK ACTIONS             |
| (assigned to me,       | (existing 5 + task-based) |
|  overdue highlighted)  |                           |
+--------------------------------------------------+
| OPERATIONS INTELLIGENCE (tabbed: B2C | B2B | Ops) |
| (existing 12 cards reorganized by platform)       |
+--------------------------------------------------+
| MODULE LAUNCHER                                    |
| (grid of accessible modules with open links)      |
+--------------------------------------------------+
```

### Role-Based Views

| Component | OWNER/EXEC | LEADER | USER |
|-----------|-----------|--------|------|
| Command Bar | All alerts | Team alerts | Personal alerts |
| Pipeline Snapshot | All pipelines | Owned pipelines | — |
| System Health | Full | Division | — |
| My Tasks | All assigned | Team tasks | Personal tasks |
| Quick Actions | All | Team-scoped | Basic |
| Ops Intelligence | All 12 cards | Division cards | — |
| Module Launcher | All accessible | Assigned modules | Assigned modules |

### New Dashboard Components

**Command Bar**: Persistent top strip with notification counts. Overdue tasks, queue items needing attention, system errors (24h), upcoming deadlines. Each clickable → navigates to relevant section.

**Pipeline Snapshot**: Mini Kanban for active queues (Onboarding, Offboarding, LC3 Internal, LC3 External). Stage distribution as colored progress segments. Click → pipeline admin tab.

**My Tasks Widget**: Tasks from `_ONBOARDING_TASKS` where `owner_email` = current user. Sorted: overdue → pending → recent. Inline complete button.

**Module Launcher**: Accessible modules as launch cards with icons and "Open" links. Replaces current passive tool suite overview.

**Ops Intelligence**: Existing 12 cards reorganized into 3 tabs (B2C, B2B, Shared Services). Keeps current async loading pattern.

### Backend Changes (`RIIMO_Dashboard.gs`)

- Refactor `getDashboardCards()` into role-aware functions
- Add `_cardPipelineSnapshot()`, `_cardMyTasks(email)`, `_cardAlerts(email)`, `_cardTeamProgress(divisionId)`

### Index.html Size Management

At ~5000 lines, Index.html needs splitting. Use GAS HTML includes:

```javascript
// Code.gs
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}
```

```html
<!-- Index.html -->
<?!= include('TaskManager') ?>
<?!= include('JobTemplates') ?>
<?!= include('DashboardWidgets') ?>
```

New HTML files:
- `TaskManager.html` — task system UI components
- `JobTemplates.html` — job template editor
- `DashboardWidgets.html` — new dashboard components

### Files Modified/Created
- **NEW:** `DashboardWidgets.html`, `TaskManager.html`, `JobTemplates.html`
- `RIIMO_Dashboard.gs` — role-based data, new card functions
- `Code.gs` — modified uiGetDashboardData(), new alert endpoint
- `Index.html` — restructured layout, HTML includes, role-based rendering

---

## Verification Plan

### Phase 1 (Entitlements)
- Create test user with per-module permissions (e.g., C3=VIEW only, CAM=VIEW+EDIT)
- Verify Permissions admin tab shows correct toggles
- Verify `userHasModuleAccess(email, 'C3', 'ADD')` returns false
- Verify `getUserEntitlements(email)` returns complete structured object

### Phase 2A (Onboarding/Tasks)
- Create onboarding record with role_type "medicare_sales"
- Verify ~40 applicable tasks auto-generated (not all 70)
- Complete tasks, verify stage progress updates
- Skip a non-required task, verify it doesn't block stage
- Test LC3 Internal pipeline with separate stages

### Phase 2B (Job Templates)
- Create template for "Medicare Sales Rep"
- Fill all sections (schedule, ownership, expectations, goals, metrics, rewards)
- Generate job description, verify output formatting
- Link template to onboarding record, verify auto-population

### Phase 3 (Dashboard)
- Load dashboard as OWNER — verify all widgets render
- Load as LEADER — verify scoped to division
- Load as USER — verify personal view only
- Click command bar alert — verify navigation
- Click pipeline snapshot — verify opens correct admin tab

---

## Summary

| Phase | New Files | Modified Files | New MATRIX Tabs | Effort |
|-------|-----------|---------------|-----------------|--------|
| 1: Entitlements | — | 4 (Core, OrgAdmin, Code, Setup) + Index.html | — (columns only) | 1-2 sessions |
| 2A: Onboarding/Tasks | RIIMO_Tasks.gs | 4 (Pipelines, Setup, Code, Index) | _TASK_TEMPLATES, _ONBOARDING_TASKS | 2-3 sessions |
| 2B: Job Templates | RIIMO_JobTemplates.gs | 3 (Setup, Code, Index) | _JOB_TEMPLATES | 1-2 sessions |
| 3: Dashboard | 3 HTML includes | 3 (Dashboard, Code, Index) | — | 2-3 sessions |
