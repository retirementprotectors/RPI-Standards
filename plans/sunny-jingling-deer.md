# RAPID_FLOW — The Universal Workflow Engine

## Context

Every process across RPI's three platforms has the same structural problem: **five layers of complexity** that humans can't consistently manage without the system encoding and enforcing them.

This was exposed by the Gradient Securities new business crisis (Mark Grams holding all RPI applications due to compliance failures), but it's the same pattern everywhere — sales pipelines, quoting, new business, onboarding, offboarding, service workflows, campaigns. The complexity isn't in any single layer; it's in the fact that there are five layers and they all interact.

**The five layers:**
```
PIPELINE → STAGE → WORKFLOW → STEP → TASK
```

- **Pipeline**: Which process? (NBX-Securities, Medicare Opportunities, Team Onboarding)
- **Stage**: Where in the process? (Kanban columns, left to right)
- **Workflow**: What work happens inside this stage? (Opens when you click a card)
- **Step**: What's the sequence inside the workflow? (Sequential, gate-enforced)
- **Task**: What specific items need to be done? (Checkboxes — manual or system-checked)

**Graceful degradation**: Simple pipelines (like current ProDash opportunity tracking) only use Pipeline + Stage (layers 1-2). The system renders a basic form on card click. Complex pipelines (like NBX-Securities) use all five layers with gates, system checks, and DEX integration. Same engine, same UI — the config determines the depth.

**RAPID_FLOW is the fourth infrastructure library:**
```
RAPID_CORE   → DATA          (MATRIX, routing, users, utilities)
RAPID_FLOW   → WORKFLOWS     (Pipeline → Stage → Workflow → Step → Task)
DEX          → DOCUMENTS     (forms, PDFs, signatures, field mappings)
RAPID_COMMS  → COMMUNICATIONS (SMS, email, calls, templates)
```

Every app on every portal consumes RAPID_FLOW. Improve the engine once → everything gets better.

## Architecture

### RAPID_FLOW as a GAS Library (Headless — No UI)

RAPID_FLOW is a pure GAS library project. No `doGet()`. No HTML. No web app deployment. Consuming apps (NBX, ProDash, SENTINEL, RIIMO) provide their own UI and call RAPID_FLOW functions via library reference.

```
RAPID_FLOW (library)
├── Consumed by: NBX (new business pipelines)
├── Consumed by: PRODASHX (sales/opportunity pipelines, QUE workflows)
├── Consumed by: SENTINEL (M&A/partnership pipelines)
├── Consumed by: RIIMO (onboarding/offboarding/maintenance pipelines)
└── Consumed by: C3 (campaign lifecycle — future)
```

### Library Dependencies
```
RAPID_FLOW depends on:
├── RAPID_CORE (MATRIX read/write, user resolution, entitlements)
└── Nothing else — RAPID_FLOW is domain-agnostic
```

Apps that consume RAPID_FLOW may ALSO consume DEX, RAPID_COMMS, etc. independently. RAPID_FLOW itself has no knowledge of documents, communications, or product-specific logic. It only knows: pipelines, stages, workflows, steps, tasks, and gates.

**Product-specific logic (suitability checks, BI validation, DEX integration) lives in the CONSUMING APP, not in RAPID_FLOW.** RAPID_FLOW provides hook points (check_type, gate_type) that the consuming app implements.

### Capability Integration via Hook Points

RAPID_FLOW defines task `check_type` as a string. The consuming app registers handlers:

```
RAPID_FLOW says: "Task X has check_type = LNW_LIMIT"
NBX registers: LNW_LIMIT → NBX_Suitability.checkLNWLimit(caseData)
RAPID_FLOW calls the registered handler → gets PASS/FAIL → updates task

RAPID_FLOW says: "Task Y has check_type = DEX_KIT_GENERATE"
NBX registers: DEX_KIT_GENERATE → NBX_DEXBridge.generateKit(caseData)
RAPID_FLOW calls the registered handler → gets result → updates task

RAPID_FLOW says: "Task Z has check_type = FIELD_PRESENT"
Any app can handle this — it's generic. RAPID_FLOW includes basic built-in checks.
```

This means DEX, RAPID_COMMS, healthcare-mcps, etc. are integrated at the APP level, not the engine level. The engine is clean and domain-agnostic.

## Data Model (5 Config Tabs + 2 Instance Tabs)

All tabs route to RAPID_MATRIX (platform = 'RAPID').

### Config Tabs (define the framework — edited by admins, rarely change)

#### _FLOW_PIPELINES
```
pipeline_key        — PK. Unique identifier (NBX_SECURITIES, MEDICARE_OPPS, TEAM_ONBOARD)
pipeline_name       — Display name ("NBX - Securities & Advisory")
pipeline_description — What this pipeline is for
portal              — PRODASHX | SENTINEL | RIIMO | ALL
domain              — SECURITIES | LIFE | ANNUITY | MEDICARE | MA | TEAM | CAMPAIGN | GENERAL
platform_carrier    — GS_GWM_GI | RBC | NAC | NASSAU | ALL (for filtering)
product_type        — TAMP | BUFFERED | FIA | MYGA | MAPD | ALL (for filtering)
default_view        — KANBAN | LIST | TABLE
icon                — Material icon name
status              — active | inactive
created_at          — ISO timestamp
updated_at          — ISO timestamp
```

#### _FLOW_STAGES
```
pipeline_key        — FK to _FLOW_PIPELINES
stage_id            — Unique within pipeline (new_no_folder, intake_prep, qc_review)
stage_name          — Display name ("QC Review")
stage_description   — What happens at this stage
stage_order         — Numeric sort (10, 20, 30...) — left to right
stage_color         — CSS variable or hex for Kanban column header
gate_enforced       — Boolean: must complete workflow before advancing?
has_workflow        — Boolean: does this stage have a workflow? (false = simple form on click)
status              — active | inactive
```

#### _FLOW_WORKFLOWS (only for stages where has_workflow = true)
```
pipeline_key        — FK to _FLOW_PIPELINES
stage_id            — FK to _FLOW_STAGES
workflow_key        — Unique identifier (qc_review_workflow)
workflow_name       — Display name
workflow_description — What this workflow accomplishes
status              — active | inactive
```

#### _FLOW_STEPS
```
pipeline_key        — FK
stage_id            — FK
workflow_key         — FK to _FLOW_WORKFLOWS
step_id             — Unique within workflow (document_integrity, data_completeness)
step_name           — Display name ("Data Completeness")
step_description    — What this step verifies/accomplishes
step_order          — Numeric sort (10, 20, 30...) — sequential within workflow
gate_enforced       — Boolean: must complete all tasks before advancing to next step?
execution_type      — auto | manual | gate
status              — active | inactive
```

#### _FLOW_TASK_TEMPLATES
```
pipeline_key        — FK
stage_id            — FK
workflow_key        — FK
step_id             — FK to _FLOW_STEPS
task_id             — Unique within step (net_worth_on_caf, bi_unique)
task_name           — Display name ("Net worth on CAF")
task_description    — What to check/do
task_order          — Numeric sort within step
is_required         — Boolean: must complete to advance? (false = can skip)
is_system_check     — Boolean: system auto-validates? (false = manual checkbox)
check_type          — String: handler key (FIELD_PRESENT, LNW_LIMIT, BI_UNIQUE, DEX_KIT_GENERATE, CUSTOM)
check_config        — JSON: parameters for the check handler
default_owner       — ADVISOR | ASSISTANT | ADMIN | SYSTEM (who typically does this)
role_applicability  — JSON: role filtering (same pattern as RIIMO tasks)
status              — active | inactive
```

### Instance Tabs (track actual cases moving through pipelines)

#### _FLOW_INSTANCES (active cases/items in any pipeline)
```
instance_id         — UUID
pipeline_key        — FK to _FLOW_PIPELINES
current_stage       — Current stage_id
current_step        — Current step_id within workflow (null if no workflow)
entity_type         — CLIENT | DEAL | EMPLOYEE | CAMPAIGN (what's moving through)
entity_id           — FK to the entity (_CLIENT_MASTER.client_id, deal_id, user_email, etc.)
entity_name         — Display name (for rendering without lookups)
entity_data         — JSON: snapshot of relevant entity data (AUM, product, carrier, etc.)
priority            — CRITICAL | HIGH | MEDIUM | LOW
assigned_to         — Owner email
stage_status        — pending | in_progress | complete | blocked
workflow_progress   — JSON: { step_id: { status, tasks_total, tasks_complete } }
custom_fields       — JSON: pipeline-specific data (BI rationale, external_ref, etc.)
created_by          — Email
created_at          — ISO timestamp
updated_at          — ISO timestamp
completed_at        — ISO timestamp
```

#### _FLOW_INSTANCE_TASKS (task instances for active cases)
```
task_instance_id    — UUID
instance_id         — FK to _FLOW_INSTANCES
pipeline_key        — FK (denormalized for fast queries)
stage_id            — FK
step_id             — FK
task_id             — FK to _FLOW_TASK_TEMPLATES (source template)
task_name           — Display name (copied from template)
task_order          — Sort order
owner_email         — Current owner
status              — pending | in_progress | completed | skipped | blocked
is_required         — Boolean (copied from template)
is_system_check     — Boolean
check_type          — String (copied from template)
check_result        — PASS | FAIL | PENDING | SKIPPED
check_detail        — JSON: what failed/passed and why
completed_by        — Email
completed_at        — Timestamp
notes               — Task-specific notes
created_at          — Timestamp
updated_at          — Timestamp
```

#### _FLOW_ACTIVITY (audit trail)
```
activity_id         — UUID
instance_id         — FK to _FLOW_INSTANCES
pipeline_key        — FK
action              — CREATE | ADVANCE_STAGE | ADVANCE_STEP | COMPLETE_TASK | SKIP_TASK | GATE_PASS | GATE_FAIL | ASSIGN | PRIORITY_CHANGE
from_value          — Previous state
to_value            — New state
performed_by        — Email
performed_at        — Timestamp
notes               — Context
```

## GAS File Structure

```
~/Projects/RAPID_TOOLS/RAPID_FLOW/
├── FLOW_Engine.gs              ← Core: createInstance, advanceStage, advanceStep, completeTask
├── FLOW_Gates.gs               ← Gate enforcement: checkStageGate, checkStepGate, validateTransition
├── FLOW_Tasks.gs               ← Task generation from templates, role filtering, system check dispatch
├── FLOW_Config.gs              ← Constants, tab names, built-in check types
├── FLOW_Query.gs               ← Read helpers: getPipeline, getStages, getWorkflow, getSteps, getTasks
├── FLOW_Hooks.gs               ← Hook point registration: registerCheckHandler, dispatchCheck
├── FLOW_DevTools.gs            ← DEBUG_Ping, SETUP_CreateTabs, SETUP_SeedPipeline, DEBUG_TestGate
├── appsscript.json             ← Library config: depends on RAPID_CORE only, executionApi DOMAIN
└── .clasp.json                 ← Script ID
```

**No HTML. No UI. No doGet(). Pure library.**

## Core Engine Functions

### FLOW_Engine.gs
```
createInstance(pipelineKey, entityType, entityId, entityName, entityData, assignedTo)
  → Creates row in _FLOW_INSTANCES at first stage
  → Generates task instances for first stage's workflow (if has_workflow)
  → Returns { success, data: { instance_id, pipeline_key, current_stage } }

advanceStage(instanceId)
  → Validates current stage workflow is complete (if has_workflow + gate_enforced)
  → Gets next stage by stage_order
  → Updates instance.current_stage
  → Generates task instances for new stage's workflow
  → Logs to _FLOW_ACTIVITY
  → Returns { success, data: { new_stage, workflow, steps, tasks } }

advanceStep(instanceId)
  → Validates current step tasks are complete (if gate_enforced)
  → Gets next step by step_order
  → Updates instance.current_step
  → Returns { success } or { success: false, blockers: [...] }

getInstanceState(instanceId)
  → Returns full state: pipeline, stage, workflow, steps, tasks with statuses
  → Used by consuming app's UI to render the card/overlay
```

### FLOW_Gates.gs
```
checkStageGate(instanceId, stageId)
  → If stage.has_workflow = false: return { pass: true }
  → If stage.gate_enforced = false: return { pass: true }
  → Get all steps for this stage's workflow
  → For each step: check if all required tasks are completed/skipped
  → Return { pass: bool, blockers: [{ step_id, task_id, reason }] }

checkStepGate(instanceId, stepId)
  → If step.gate_enforced = false: return { pass: true }
  → Get all tasks for this step
  → Check required tasks: all completed/skipped?
  → Return { pass: bool, blockers: [{ task_id, check_result, check_detail }] }

validateStageTransition(instanceId, targetStageId)
  → Verify target is the NEXT sequential stage (no skipping)
  → Return { valid: bool, error: string }
```

### FLOW_Tasks.gs
```
generateTasksForStage(instanceId, stageId)
  → Get workflow for this stage
  → Get all steps for the workflow
  → Get all task templates for all steps
  → Filter by role_applicability (match against instance.assigned_to role)
  → Create task instance rows in _FLOW_INSTANCE_TASKS
  → Update instance.workflow_progress JSON

completeTask(instanceId, taskInstanceId, completedBy, notes)
  → If is_system_check: dispatch to registered handler via FLOW_Hooks
  → Update task status = 'completed', check_result = PASS/FAIL
  → Recalculate step progress
  → If all tasks in step complete + gate_enforced: try auto-advance step
  → If all steps in workflow complete + stage.gate_enforced: try auto-advance stage
  → Log to _FLOW_ACTIVITY

skipTask(instanceId, taskInstanceId, skippedBy, reason)
  → Only allowed if is_required = false
  → Update task status = 'skipped'
  → Same recalculation + auto-advance logic
```

### FLOW_Hooks.gs
```
var _checkHandlers = {};

registerCheckHandler(checkType, handlerFunction)
  → _checkHandlers[checkType] = handlerFunction
  → Called by consuming app at initialization
  → Example: NBX calls registerCheckHandler('LNW_LIMIT', NBX_Suitability.check)

dispatchCheck(checkType, checkConfig, instanceData)
  → If checkType in _checkHandlers: call handler, return result
  → If checkType is built-in (FIELD_PRESENT, etc.): run built-in logic
  → If no handler found: return { result: 'PENDING', detail: 'No handler registered' }
```

### Built-in Check Types (in FLOW_Config.gs)
```
FIELD_PRESENT     → Verify a field exists and is non-empty in instance.entity_data
FIELD_MATCHES     → Verify a field matches expected value
FIELD_NOT_CONTAINS → Verify a field does NOT contain a string (e.g., "Signal Wealth")
NUMERIC_LIMIT     → Verify a numeric field is within min/max bounds
ALL_FORMS_CHECKED → Verify all items in a JSON checklist are true
MANUAL            → No system check — manual checkbox only
```

Apps register their own custom check types for domain-specific logic.

## How Consuming Apps Use RAPID_FLOW

### NBX (first consumer)
```
NBX/Code.gs:
  // At initialization, register NBX-specific check handlers
  RAPID_FLOW.registerCheckHandler('LNW_LIMIT', NBX_Suitability.checkLNWLimit);
  RAPID_FLOW.registerCheckHandler('BI_UNIQUE', NBX_BestInterest.checkSimilarity);
  RAPID_FLOW.registerCheckHandler('BI_NO_SIGNAL', NBX_BestInterest.checkNoSignal);
  RAPID_FLOW.registerCheckHandler('DEX_KIT_GENERATE', NBX_DEXBridge.generateKit);
  RAPID_FLOW.registerCheckHandler('DEX_DOCUSIGN', NBX_DEXBridge.sendForSignature);
  RAPID_FLOW.registerCheckHandler('CORRECT_CUSTODIAN', NBX_QC.checkCustodian);

NBX/Index.html:
  // Render Kanban board
  const pipeline = RAPID_FLOW.getPipeline('NBX_SECURITIES');
  const stages = RAPID_FLOW.getStages('NBX_SECURITIES');
  const instances = RAPID_FLOW.getInstances('NBX_SECURITIES');
  // Group instances by current_stage → render columns

  // On card click
  const state = RAPID_FLOW.getInstanceState(instanceId);
  if (state.stage.has_workflow) {
    renderWorkflowOverlay(state);  // NBX renders its own UI
  } else {
    renderSimpleForm(state);
  }

  // On task completion
  const result = RAPID_FLOW.completeTask(instanceId, taskInstanceId, userEmail);
  // result tells NBX whether to auto-advance or show blockers
```

### PRODASHX (migrating opportunity pipelines)
```
PRODASHX/PRODASH_Pipeline.gs:
  // Simple pipelines — no custom check handlers needed
  // Just use built-in FIELD_PRESENT and MANUAL check types

  // Read pipeline data
  const pipeline = RAPID_FLOW.getPipeline('LIFE_OPPORTUNITIES');
  const stages = RAPID_FLOW.getStages('LIFE_OPPORTUNITIES');
  // has_workflow = false for all stages → card click opens simple form

  // Move opportunity to next stage
  RAPID_FLOW.advanceStage(instanceId);
  // No gates because gate_enforced = false on these stages
```

### RIIMO (migrating from native pipeline code)
```
RIIMO/RIIMO_Pipelines.gs:
  // Register RIIMO-specific handlers
  RAPID_FLOW.registerCheckHandler('GOOGLE_WORKSPACE_CHECK', RIIMO_Onboard.checkWorkspaceSetup);
  RAPID_FLOW.registerCheckHandler('SLACK_INVITE_CHECK', RIIMO_Onboard.checkSlackInvite);

  // Everything else just calls RAPID_FLOW instead of native code
  // getPipelineDefinitions() → RAPID_FLOW.getStages(pipelineKey)
  // generateTasksForQueue() → RAPID_FLOW.generateTasksForStage()
  // completeTask() → RAPID_FLOW.completeTask()
```

## Migration Path

### Phase 1: Build RAPID_FLOW (the engine) — COMPLETE
- New GAS project: ~/Projects/RAPID_TOOLS/RAPID_FLOW/
- 7 .gs files (Engine, Gates, Tasks, Config, Query, Hooks, DevTools)
- No UI, no HTML — pure headless library
- 8 config/instance tabs registered in RAPID_CORE (TABLE_ROUTING + TAB_SCHEMAS)
- SETUP_CreateTabs() creates all tabs in RAPID_MATRIX
- SETUP_SeedPipeline('NBX_SECURITIES') seeds the Gradient crisis pipeline
- Gate enforcement validated via DEBUG_TestGate()
- Built, audited, pushed + deployed

### Phase 2: Build NBX (first consumer) — COMPLETE
- New GAS project: ~/Projects/RAPID_TOOLS/NBX/
- Libraries: RAPID_CORE + RAPID_FLOW + DEX
- Custom check handlers registered (suitability, BI, DEX integration)
- UI: Kanban board + workflow overlay + admin config
- NBX_SECURITIES pipeline seeded (stages, workflows, steps, tasks)
- NBX_SECURITIES_RBC pipeline seeded
- Live with 38 Gradient cases
- Built, audited, pushed + deployed

### Phase 3: Migrate PRODASHX opportunity pipelines — COMPLETE
- PRODASHX v3.25.0 (@234) — zero UI changes via bridge pattern
- RAPID_FLOW v1.1.0 (@4) — added `moveToStage()` for free-form drag-drop
- 22 pipelines migrated from `_PIPELINES` → `_FLOW_PIPELINES` + `_FLOW_STAGES`
- 608 opportunities migrated from `_OPPORTUNITIES` → `_FLOW_INSTANCES`
- Bridge layer (`PRODASH_FlowBridge.gs`) transforms RAPID_FLOW data → old shapes
- 5 Code.gs functions rewired: uiGetPipelines, uiGetOpportunities, uiCreate/Update/DeleteOpportunity
- `has_workflow = false` on all stages → simple Kanban, no workflows
- Stage colors preserved, category→domain mapping applied
- Legacy `_OPPORTUNITIES` tab preserved as read-only archive
- Built, audited (3/3 approved), pushed + deployed
- **Hardening TODO**: Flip `developmentMode: true` → `false` on RAPID_FLOW lib ref after Phase 5 stabilizes
- **Hardening TODO**: Grep all projects for `_OPPORTUNITIES` references to find orphaned readers

### Phase 4: Product expansion (~40% lift vs Phase 1+2)
- NBX-Medicare, NBX-Life, NBX-Annuity pipeline configs
- **NBX-Medicare has AEP deadline (Oct 15)** — must be ready before enrollment season
- QUE-Medicare internal workflow migrates to RAPID_FLOW
- QUE-Life, QUE-Annuity get built on RAPID_FLOW from day one
- Each product line: configure pipeline, stages, workflows, steps, tasks
- DEX integration per product (carrier-specific form kits)
- Heaviest lift is domain logic (carrier-specific rules, suitability, forms) not engine work

### Phase 5: Migrate RIIMO pipelines to RAPID_FLOW (~30% lift)
- RIIMO adds RAPID_FLOW as library dependency
- Replace native RIIMO_Pipelines.gs logic with RAPID_FLOW calls
- Migrate _PIPELINE_CONFIG data to _FLOW_STAGES
- Migrate _TASK_TEMPLATES to _FLOW_TASK_TEMPLATES
- Migrate _ONBOARDING_TASKS to _FLOW_INSTANCE_TASKS
- Native code becomes thin wrapper around RAPID_FLOW
- Onboarding, offboarding, data/tech/security maintenance all on the engine
- Low risk — internal tooling, team adjusts if anything breaks during migration

### Phase 6: C3 Campaign Lifecycle on RAPID_FLOW (~35% lift)
- **LAST migration — highest blast radius (touches every client)**
- Engine must be battle-tested across Phases 3-5 before touching C3
- Campaign workflows: Draft → Review → Approve → Deploy → Track → Measure
- Content block lifecycle as a pipeline
- AEP blackout enforcement as a gate
- Campaign approval as a workflow with steps (compliance review, manager sign-off)
- Renewal campaigns as recurring pipeline instances
- Risk: 60 active campaigns + 661 templates must be migrated mid-flight without drops
- Mitigation: Run parallel (old + new) during transition, cut over once validated

### Phase 7: Migrate SENTINEL pipelines to RAPID_FLOW (~20% lift)
- **Status: NEXT UP** — research complete, ready to execute
- Lightest lift — 2 files to modify, ~8 functions to rewrite
- SENTINEL_Pipeline.gs: Replace `DEFAULT_PIPELINES` constant + 8 functions with RAPID_FLOW calls
- Index.html: Update `loadPipelineView()` (kanban rendering stays as-is)
- 3 hardcoded pipelines (Prospecting/4 stages, Sales Process/5 stages, Transition/5 stages) → RAPID_FLOW config
- Deal storage stays in `Opportunities` sheet (SENTINEL_MATRIX) — bridge pattern like PRODASHX
- `moveDealToNextPipeline()` cross-pipeline transition → RAPID_FLOW moveToStage
- Low urgency — SENTINEL v2 works, deals are moving

## Critical Files to Modify

| File | Change |
|------|--------|
| `RAPID_CORE/CORE_Database.gs` | Add TABLE_ROUTING + TAB_SCHEMAS for 8 FLOW tabs |
| New: `RAPID_FLOW/*` | All new library project files (7 .gs files) |
| New: `NBX/*` | All new app project files (consumer #1) |
| Future: `RIIMO/RIIMO_Pipelines.gs` | Replace native logic with RAPID_FLOW calls |
| Future: `RIIMO/RIIMO_Tasks.gs` | Replace native logic with RAPID_FLOW calls |
| Future: `sentinel-v2/SENTINEL_Pipeline.gs` | Replace native logic with RAPID_FLOW calls |
| Future: `PRODASHX/PRODASH_Pipeline.gs` | Replace opportunity pipeline with RAPID_FLOW calls |

## Reusable Code (Don't Rebuild)

| Component | Source | Reuse |
|-----------|--------|-------|
| Stage progression + sequential enforcement | `RIIMO/RIIMO_Pipelines.gs` — `validateStageTransition()`, `checkStageGate()`, `_tryAutoAdvance()` | Extract and generalize into FLOW_Engine + FLOW_Gates |
| Task generation from templates with role filtering | `RIIMO/RIIMO_Tasks.gs` — `generateTasksForQueue()`, role_applicability JSON matching | Extract and generalize into FLOW_Tasks |
| Pipeline config admin UI pattern | `RIIMO/Index.html` — admin pipeline config tab | Adapt for 5-layer drill-down in NBX admin |
| Deal pipeline kanban rendering | `sentinel-v2/SENTINEL_Pipeline.gs` — `getPipelineKanban()` | Reference pattern for FLOW_Query |
| Activity logging | `RIIMO/RIIMO_Pipelines.gs` — activity log pattern | Extract into FLOW_Engine activity logging |
| MATRIX tab registration | `RAPID_CORE/CORE_Database.gs` — TABLE_ROUTING + TAB_SCHEMAS | Standard pattern for all 8 new tabs |

## Verification

### After RAPID_FLOW Phase 1:
1. `DEBUG_Ping()` via execute_script — GAS connectivity
2. `SETUP_CreateTabs()` — all 8 tabs created in RAPID_MATRIX
3. `SETUP_SeedPipeline('NBX_SECURITIES')` — full pipeline seeded (7 stages, 7 workflows, ~22 steps, ~54 tasks)
4. `DEBUG_TestGate()` — create test instance, complete some tasks, verify gate blocks advancement when tasks incomplete, allows when complete
5. `RAPID_FLOW.getPipeline('NBX_SECURITIES')` — returns full pipeline definition
6. `RAPID_FLOW.createInstance(...)` — creates instance at first stage
7. `RAPID_FLOW.getInstanceState(id)` — returns full 5-layer state
8. `RAPID_FLOW.completeTask(id, taskId, email)` — completes task, auto-advances if applicable
9. `RAPID_FLOW.advanceStage(id)` — advances with gate check

### After NBX Phase 2:
10. Open NBX web app — Kanban board renders with stages from RAPID_FLOW
11. Create new case (Fisette) — instance created in RAPID_FLOW, tasks generated
12. Click case card — workflow overlay shows steps and tasks
13. Complete tasks — progress updates, auto-advance works
14. Hit gate with incomplete tasks — system blocks with blocker list
15. Register DEX handler — form kit generation fires at correct step
16. Verify all 38 Gradient cases render correctly
