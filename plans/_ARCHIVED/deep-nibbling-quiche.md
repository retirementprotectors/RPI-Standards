ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# Portal Overhaul — Sessions E + F Plan

> **Context**: Sessions A-D complete and audited clean. RIIMO v3.20 @96, SENTINEL v3.19 @48, PRODASHX v3.23 @226, RAPID_CORE v1.14.0 (lib v92). This plan covers the final two sessions: pipeline automation promotion and SENTINEL pipeline CRUD.

---

## Session E: Pipeline Automation Promotion + Refactor

**Scope**: RAPID_CORE + RIIMO + ATLAS registration. No portal UI changes.

**Why**: 13 pipeline automation functions in RIIMO_Pipelines.gs — 4 are cross-platform and belong in RAPID_CORE, 4 need refactoring to use existing RAPID_CORE functions, 4 are stubs to kill, 1 stays as-is (Compliance depends on RIIMO PROJECT_REGISTRY).

### E-0: Fix `_buildColIndex` Critical Bug

**Problem**: `_buildColIndex(headers)` is called 30+ times across RIIMO files but never defined. Every queue/task/offboarding operation silently fails.

**Fix**: Add to `/Users/joshd.millang/Projects/RAPID_TOOLS/RIIMO/RIIMO_Core.gs`:
```javascript
function _buildColIndex(headers) {
  var idx = {};
  for (var i = 0; i < headers.length; i++) {
    if (headers[i] && !(headers[i] in idx)) idx[headers[i]] = i;
  }
  return idx;
}
```

**Acceptance**: `grep "_buildColIndex" RIIMO_Core.gs` → definition found. Pipeline stage executions no longer throw.

---

### E-1: Promote 4 Functions to RAPID_CORE

**File**: `/Users/joshd.millang/Projects/RAPID_TOOLS/RAPID_CORE/CORE_OrgAdmin.gs` (new section at bottom)
**Exports**: `/Users/joshd.millang/Projects/RAPID_TOOLS/RAPID_CORE/Code.gs` (add to exports object)

| Function | What It Does | Source Lines |
|----------|-------------|-------------|
| `backupMatrices()` | Copies all 3 MATRIXes to `_RIIMO_BACKUPS` Drive folder with timestamp | 822-890 |
| `getErrorLogSummary()` | Reads `_ERROR_LOG`, aggregates by severity + time windows (24h/7d/30d) | 994-1061 |
| `auditUserAccess()` | Reads `_USER_HIERARCHY`, aggregates by level, flags inactive users | 1086-1150 |
| `getBackupStatus()` | Inventories `_RIIMO_BACKUPS` folder, checks backup freshness (7-day threshold) | 1230-1299 |

**Adjustments**: Replace RIIMO's `getRAPID_MATRIX()` with RAPID_CORE internal `getMATRIX_SS('RAPID')`. All 4 functions use only DriveApp/SpreadsheetApp — zero RIIMO dependencies.

**Acceptance**: Each callable via `execute_script` on any project using RAPID_CORE. Returns `{ status, message, details }`.

---

### E-2: Refactor RIIMO Pipeline Functions

**File**: `/Users/joshd.millang/Projects/RAPID_TOOLS/RIIMO/RIIMO_Pipelines.gs`

| Function | Action | Detail |
|----------|--------|--------|
| `executeBackup` | **Delegate** | → `RAPID_CORE.backupMatrices()` |
| `executeMonitoring` | **Delegate** | → `RAPID_CORE.getErrorLogSummary()` |
| `executeAccessControl` | **Delegate** | → `RAPID_CORE.auditUserAccess()` |
| `executeBackupDR` | **Delegate** | → `RAPID_CORE.getBackupStatus()` |
| `executeCleanup` | **Rewire** | → `RAPID_CORE.reconcileClients({ dryRun: true })` |
| `executeValidation` | **Rewire** | → `RAPID_CORE.reconcileClients` + `reconcileAccounts` (both dryRun) |
| `executeOffboardingAccessRevoke` | **Refactor** | Use `RAPID_CORE.resolveUser()` → `RAPID_CORE.deleteUser(userId)` instead of manual sheet writes. Keep `_addPendingAction` calls. |
| `executeAuditLog` | **Kill** | → redirect to `executeMonitoring()` |
| `executeMatrixSync` | **Kill** | → return `{ status: 'skipped' }` |
| `executeTesting` | **Kill** | → redirect to `executeValidation()` |

**Stays as-is**: `executeCompliance` (RIIMO PROJECT_REGISTRY dependency), `executeOnboardingSystemSetup` (heavy RIIMO compose), `executeOnboardingActivation` (RIIMO pending actions).

**Acceptance**: All pipeline stages callable via `executePipelineStage()`. Delegates return RAPID_CORE results. Killed stubs return clean status.

---

### E-3: ATLAS Registration

**Tool**: `execute_script` against ATLAS (script ID: `1dLLKTyOIOSN8W3X6oxn57FwbMHNCKDrI4HMdGojMRGfYAZpSNPHknUU_`)

Register 9 real functions in `_SOURCE_REGISTRY`:

| # | Source | Location | Type | Status |
|---|--------|----------|------|--------|
| 1 | backupMatrices | RAPID_CORE/CORE_OrgAdmin | automation | active |
| 2 | getErrorLogSummary | RAPID_CORE/CORE_OrgAdmin | automation | active |
| 3 | auditUserAccess | RAPID_CORE/CORE_OrgAdmin | automation | active |
| 4 | getBackupStatus | RAPID_CORE/CORE_OrgAdmin | automation | active |
| 5 | executeCompliance | RIIMO/RIIMO_Pipelines | automation | active |
| 6 | executeCleanup | RIIMO/RIIMO_Pipelines (→ RAPID_CORE reconcile) | automation | active |
| 7 | executeOnboardingSystemSetup | RIIMO/RIIMO_Pipelines | workflow | active |
| 8 | executeOnboardingActivation | RIIMO/RIIMO_Pipelines | workflow | active |
| 9 | executeOffboardingAccessRevoke | RIIMO/RIIMO_Pipelines (→ RAPID_CORE deleteUser) | workflow | active |

**NOT registered**: MatrixSync (skipped), AuditLog (redirect), Testing (redirect), Validation (redirect to reconcile — not a standalone source).

---

### E Deploy Sequence

1. RAPID_CORE: `clasp push` + `clasp version` + git (library, no web deploy)
2. RIIMO: full 6-step deploy
3. ATLAS: `execute_script` (no deploy)

---

## Session F: SENTINEL Pipeline Config CRUD

**Scope**: SENTINEL v2 only. Port RIIMO's Pipeline Config CRUD pattern.

**Why**: SENTINEL Pipeline Config is display-only. RIIMO has full add/edit/delete/reorder. SENTINEL backend already exists (`uiSavePipelineConfigForUI`), just needs frontend wiring + individual stage operation wrappers.

### F-1: Add Backend Wrappers

**File**: `/Users/joshd.millang/Projects/SENTINEL_TOOLS/sentinel-v2/SENTINEL_OrgAdmin.gs`

Add after `uiSavePipelineConfigForUI` (line 98):

| Function | What It Does |
|----------|-------------|
| `uiAddPipelineStageForUI(pipelineKey, stageData)` | Read config, append new stage, write back via `RAPID_CORE.savePipelineConfig('SENTINEL', ...)` |
| `uiUpdatePipelineStageForUI(pipelineKey, stageId, updates)` | Read config, update matching stage, write back |
| `uiRemovePipelineStageForUI(pipelineKey, stageId)` | Read config, set stage status='inactive', write back |
| `uiReorderPipelineStagesForUI(pipelineKey, orderedStageIds)` | Read config, update stage_order values, write back |

All use `RAPID_CORE.getPipelineConfig('SENTINEL')` to read, `RAPID_CORE.savePipelineConfig('SENTINEL', config)` to write.

---

### F-2: Replace Pipeline Config Frontend

**File**: `/Users/joshd.millang/Projects/SENTINEL_TOOLS/sentinel-v2/Index.html`

Replace `loadPipelineConfig()` (lines 3203-3235) + `pipelineConfigContent` area with full CRUD UI adapted from RIIMO (lines 4655-5180).

**Features to port**:
- Pipeline selector tabs (Prospecting, Sales Process, Transition)
- Stage list with order, name, execution type, status
- Move Up / Move Down buttons per stage
- Remove Stage button (soft delete with confirmation)
- Add Stage form (name, description, exit criteria, execution type)
- Edit Stage side panel (all fields editable)
- Add Pipeline button

**Key adaptation**: SENTINEL uses `async/await` + `runServerFunction()` pattern (not `google.script.run` callbacks). All server calls must use:
```javascript
var result = await runServerFunction('uiAddPipelineStageForUI', pipelineKey, stageData);
```

**Styling**: Use SENTINEL CSS variables (`--portal`, `--pipeline-color`, `--bg-card`, `--border`, `--text-primary`). No hardcoded colors.

**Acceptance**:
- Pipeline Config shows 3 pipelines with stages
- Add/Edit/Delete/Reorder all work and persist
- `grep "addPipeline\|editStage\|deleteStage\|removeStage" Index.html` → matches

---

### F Deploy

Full 6-step deploy for SENTINEL.

---

## Critical Files

| File | Session | Changes |
|------|---------|---------|
| `RAPID_CORE/CORE_OrgAdmin.gs` | E | +4 promoted pipeline functions |
| `RAPID_CORE/Code.gs` | E | +4 exports |
| `RIIMO/RIIMO_Core.gs` | E | +`_buildColIndex` bug fix |
| `RIIMO/RIIMO_Pipelines.gs` | E | Refactor 10 functions (delegates/rewires/kills) |
| `SENTINEL/SENTINEL_OrgAdmin.gs` | F | +4 pipeline CRUD wrappers |
| `SENTINEL/Index.html` | F | Replace read-only pipeline config with full CRUD |

## Execution Order

```
E-0: _buildColIndex fix (RIIMO_Core.gs)
E-1: Promote 4 functions (RAPID_CORE)
E-2: Refactor 10 functions (RIIMO_Pipelines.gs)
E-3: ATLAS registration (execute_script, parallel with deploys)
     Deploy: RAPID_CORE → RIIMO
--- Session E checkpoint ---
F-1: Backend wrappers (SENTINEL_OrgAdmin.gs)
F-2: Frontend CRUD (SENTINEL Index.html)
     Deploy: SENTINEL
--- Session F checkpoint ---
```
