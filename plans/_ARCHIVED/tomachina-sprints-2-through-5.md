ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# toMachina — Sprints 2-5 Execution Plans

> **Operating Model:** Up to 6 Builder Agents (parallel, worktree isolation) + 1 Planner/Auditor Agent
> **Sprint 1 (Data Integrity):** COMPLETE (2026-03-11)
> **Sprint 2 (Shared Modules):** COMPLETE (2026-03-11)
> **Sprint 3 (Portal Depth):** COMPLETE (2026-03-11)
> **Sprint 4 (GAS Migration):** NEXT
> **Architecture Reference:** `~/Projects/toMachina/ARCHITECTURE.md`
> **Framework:** `~/.claude/plans/tomachina-next-phases.md`

---

## Sprint 2: Shared Module Components

**Goal:** Build the 8 shared module components in `packages/ui/src/modules/`. Every module renders in all 3 portals. Replace 24 duplicated portal pages with 3-line imports.

**Depends on:** Sprint 1 (clean data in Firestore)

### Builder Assignments

**Builder 1 — Revenue + Leadership Modules**

| Module | Component | Reference Code | Firestore | Complexity |
|--------|-----------|---------------|-----------|------------|
| CAM Dashboard | `CamDashboard.tsx` | `archive/CAM/Index.html` (2K), `Scripts.html` (2.8K), `CAM_Analytics.gs` (2K), `CAM_Commission.gs` (1.3K) | `revenue`, `agents`, `carriers`, `comp_grids` (pending migration) | HIGH |
| Command Center | `CommandCenter.tsx` | `archive/CEO-Dashboard/`, `archive/RPI-Command-Center/` | All collections (aggregates) | MEDIUM |
| Admin Panel | `AdminPanel.tsx` | Current portal admin pages (already similar across portals) | `users`, `org` | LOW |

Scope:
- `packages/ui/src/modules/CamDashboard.tsx` — Full CAM: revenue breakdown by carrier/agent/type, comp grid viewer, commission projections, pipeline tracking
- `packages/ui/src/modules/CommandCenter.tsx` — Leadership dashboard: cross-platform metrics, team performance cards, pipeline health, revenue trends
- `packages/ui/src/modules/AdminPanel.tsx` — User management: user list with search/filter, org tree, level badges, entitlement viewer
- Replace all 9 portal page files (3 modules x 3 portals) with 3-line imports
- Read archive files FIRST — bring over the UX patterns and workflows

Files owned: `packages/ui/src/modules/{CamDashboard,CommandCenter,AdminPanel}.tsx`, all `apps/*/modules/{cam,command-center}/page.tsx`, all `apps/*/admin/page.tsx`

**Builder 2 — Campaign + Document Modules**

| Module | Component | Reference Code | Firestore | Complexity |
|--------|-----------|---------------|-----------|------------|
| C3 Manager | `C3Manager.tsx` | `archive/C3/Index.html` (10K!) | `campaigns`, `templates`, `content_blocks` | HIGH |
| DEX Doc Center | `DexDocCenter.tsx` | `archive/DEX/Index.html` (744), `Scripts.html` (3K) | `communications`, `case_tasks` + DEX collections (pending migration) | MEDIUM |
| ATLAS Registry | `AtlasRegistry.tsx` | `archive/ATLAS/Index.html` + `_VIEW_*.html` (2K) | `source_registry`, `tool_registry` (pending) | MEDIUM |

Scope:
- `packages/ui/src/modules/C3Manager.tsx` — Full C3: campaign list with status/type filters, campaign detail view, template browser, content block editor, send history
- `packages/ui/src/modules/DexDocCenter.tsx` — Document center: form library browser, kit builder interface, document pipeline status (Intake → Processing → Filing), PDF preview placeholder
- `packages/ui/src/modules/AtlasRegistry.tsx` — Full ATLAS: source registry table with status/type filters, source detail modal, tool registry tab, automation health indicators, wire diagram placeholder
- Replace all 9 portal page files with 3-line imports
- Read archive files FIRST

Files owned: `packages/ui/src/modules/{C3Manager,DexDocCenter,AtlasRegistry}.tsx`, all `apps/*/modules/{c3,dex,atlas}/page.tsx`

**Builder 3 — People + Communications Modules**

| Module | Component | Reference Code | Firestore | Complexity |
|--------|-----------|---------------|-----------|------------|
| MyRPI Profile | `MyRpiProfile.tsx` | `archive/RIIMO/RIIMO_MyRPI.gs` (1.6K), `MyRPI.html` (3.4K) | `users` | MEDIUM |
| RPI Connect | `ConnectPanel.tsx` | `archive/PRODASHX/RPI_Connect.html` (1.4K), `archive/RIIMO/RPI_Connect.html` (1.4K) | `communications` | HIGH |

Scope:
- `packages/ui/src/modules/MyRpiProfile.tsx` — Employee profile: personal info card, contact details, team/division, aliases, employee_profile fields (meet_room/drop_zone, roadmap_doc_id, team_folders). LEADER+ gets profile switcher (view other team members). MyDropZone UI placeholder (capture interface — recording + doc photos).
- `packages/ui/src/modules/ConnectPanel.tsx` — Communications hub: unified message timeline (SMS, email, call, meeting, chat), compose message (select channel: SMS/Email), contact card with DND flags, recent activity. Reads from `communications` collection. Send actions call MCP comms tools or API routes.
- Create `packages/ui/src/modules/index.ts` — barrel export for all 8 modules
- Replace all portal page files with 3-line imports
- Add MyRPI route to ProDashX and SENTINEL sidebars (currently RIIMO only)
- Read archive files FIRST

Files owned: `packages/ui/src/modules/{MyRpiProfile,ConnectPanel}.tsx`, `packages/ui/src/modules/index.ts`, all `apps/*/myrpi/page.tsx`, all Connect-related pages

### Sprint 2 Verification
- [ ] 8 shared module components in `packages/ui/src/modules/`
- [ ] All portal pages converted to 3-line imports
- [ ] `turbo run build` — 9/9 workspaces pass
- [ ] Each module renders correctly in all 3 portals with correct theming
- [ ] Archive UX patterns preserved (not just data tables — actual workflows)

### Sprint 2 Estimated Time: 1 session (3-4 hours per builder)

---

## Sprint 3: Portal-Specific Depth

**Goal:** Rebuild the unique, portal-specific features from the GAS era in React. Make the portals team-ready.

**Depends on:** Sprint 2 (shared modules built)

### Builder Assignments

**Builder 1 — ProDashX Client Experience**

| Feature | Route | Reference | Firestore | Priority |
|---------|-------|-----------|-----------|----------|
| CLIENT360 rich tabs | `/clients/[id]` | `archive/PRODASHX/PRODASH_CLIENT360.gs` (1.7K) + `Scripts.html` (15K) | `clients`, `clients/*/accounts`, `communications`, `activities` | HIGH |
| RMD Center | `/service-centers/rmd` | `archive/PRODASHX/PRODASH_RMD_CENTER.gs` (381) | `clients`, `clients/*/accounts` (annuity/bdria) | HIGH |
| Beni Center | `/service-centers/beni` | `archive/PRODASHX/PRODASH_BENI_CENTER.gs` (219) | `clients` | MEDIUM |
| Quick Intake | New route | `archive/PRODASHX/PRODASH_QuickIntake.gs` (524) | `clients` (bridge write) | MEDIUM |
| Casework depth | `/casework` | `archive/PRODASHX/PRODASH_CASEWORK.gs` (745) + `CASE_CENTRAL.gs` (910) | `case_tasks` | MEDIUM |

Scope:
- CLIENT360: Enrich all 11 tabs with the layout/workflow patterns from archive Scripts.html. Not just data display — action buttons, inline editing depth, relationship visualization, account drill-down.
- RMD Center: IRS Required Minimum Distribution calculator. Port RMD logic to `packages/core/financial/rmd.ts`. Show RMD schedule, distribution tracking, alerts for approaching deadlines.
- Beni Center: Beneficiary review workflow. Show beneficiary designations per account, flag missing/outdated designations.
- Quick Intake: One-screen client creation form. Minimal fields (name, phone, email, source). Writes through bridge. Auto-dedup check before create.
- Casework: Full case management — task creation, delegation, status workflow, timeline, attached documents.

Files owned: `apps/prodash/**` (portal-specific pages only, NOT shared modules)

**Builder 2 — ProDashX Sales + Quoting**

| Feature | Route | Reference | Backend | Priority |
|---------|-------|-----------|---------|----------|
| Medicare Quoting | `/sales-centers/medicare` | `archive/PRODASHX/PRODASH_QUE_MEDICARE.gs` (421) + `PRODASH_MEDICARE_REC.gs` (637) | `services/MCP-Hub/healthcare-mcps/` (QUE-API on Cloud Run) | HIGH |
| Discovery Kit | New route | `archive/PRODASHX/PRODASH_DISCOVERY_KIT.gs` (1.2K) + `DISCOVERY_PDF.gs` (734) | `gas/DEX/` for PDF generation | MEDIUM |
| Pipelines depth | `/pipelines` | `archive/PRODASHX/PRODASH_FlowBridge.gs` (138) + `FlowSetup.gs` (259) | Firestore `flow/config/*` | MEDIUM |
| Life/Annuity/Advisory | `/sales-centers/*` | Minimal — these are future features | None | LOW (placeholders with real structure) |

Scope:
- Medicare Quoting: Wire CSG Actuarial API (`api.csgactuarial.com`) for Med Supp quotes. Plan comparison table, recommendation logic, carrier/plan filtering by ZIP+age+gender+tobacco. Reference QUE-API docs in MEMORY.md.
- Discovery Kit: Client discovery questionnaire (multi-step wizard). Collect financial goals, risk tolerance, existing coverage. Generate summary PDF via DEX backend or new Cloud Function.
- Pipelines: Add stage execution — drag card between stages triggers workflow actions. Read/write `flow/config/instances`.
- Sales Center shells: Real page structure (search, filters, placeholder content) even if quoting isn't wired yet.

Files owned: `apps/prodash/sales-centers/**`, `apps/prodash/pipelines/`, new Discovery Kit route

**Builder 3 — RIIMO + SENTINEL Depth**

| Feature | Portal | Route | Reference | Priority |
|---------|--------|-------|-----------|----------|
| Dashboard widgets | RIIMO | `/dashboard` | `archive/RIIMO/RIIMO_Dashboard.gs` (1.3K) + `DashboardWidgets.html` (1.6K) | HIGH |
| Pipeline execution | RIIMO | `/pipelines` | `archive/RIIMO/RIIMO_Pipelines.gs` (1.8K) | HIGH |
| Task delegation | RIIMO | `/tasks` | `archive/RIIMO/RIIMO_Tasks.gs` (748) | MEDIUM |
| Deal management | SENTINEL | `/deals` | `archive/sentinel-v2/SENTINEL_DealManagement.gs` (398) | MEDIUM |
| Valuation tools | SENTINEL | `/modules/david-hub` | `archive/sentinel-v2/SENTINEL_Valuation.gs` (507) + `archive/DAVID-HUB/` | HIGH |
| Intelligence depth | RIIMO | `/intelligence` | `archive/RIIMO/RIIMO_Intelligence.gs` (162) | LOW |

Scope:
- RIIMO Dashboard: Rich widget cards with sparklines, trend indicators, health scores. Cross-platform data (reads all 3 portals' data). Quick action buttons.
- Pipeline execution: Drag-and-drop stage progression. Onboarding/offboarding pipeline templates. Stage gates with required fields.
- DAVID HUB calculators: MEC Calculator (Modified Endowment Contract), PRP Evaluator (Producer Revenue Projection), SPH Projections (Single Premium Hybrid), Deal Valuation. Port calc logic to `packages/core/financial/`.
- Deal management: CRUD for deals, attach documents, valuation comparison, M&A workflow stages.

Files owned: `apps/riimo/**` (portal-specific), `apps/sentinel/**` (portal-specific), `packages/core/financial/` (new calc files)

### Sprint 3 Verification
- [ ] ProDashX: CLIENT360 matches archive UX depth, RMD Center functional, Quick Intake works
- [ ] ProDashX: Medicare quoting renders plans from CSG API
- [ ] RIIMO: Dashboard has rich widgets, Pipeline drag-and-drop works
- [ ] SENTINEL: DAVID HUB calculators functional, Deal management CRUD works
- [ ] All `turbo run build` passes
- [ ] No regressions in shared modules from Sprint 2

### Sprint 3 Estimated Time: 1-2 sessions (4-5 hours per builder)

---

## Sprint 4: GAS Engine Migration

**Goal:** Move the GAS engines that keep breaking or limiting functionality to modern infrastructure. Stop the reactive maintenance cycle.

**Depends on:** Sprint 2 (shared modules need the backends), Sprint 3 (portal depth exercises the backends)

### What Moves vs What Stays

| Engine | Decision | Reason |
|--------|----------|--------|
| **RAPID_COMMS** (1K lines) | **MOVE NOW** | Easiest port. Just HTTP calls. MCP already does the same thing. Eliminates GAS dependency for all communications. |
| **RAPID_FLOW** (2K lines) | **MOVE NOW** | Small, mostly pure logic. Pipeline drag-and-drop (Sprint 3) needs sub-second response that GAS can't provide. |
| **C3 backend** (13K lines) | **MOVE** | Campaign builder UI (Sprint 2) needs a real backend, not a 10K-line HTML file with embedded google.script.run calls. |
| **ATLAS backend** (5K lines) | **MOVE** | Clean code, already has Firestore data + toMachina UI. Triggers → Cloud Scheduler. |
| **CAM backend** (8K lines) | **PARTIAL MOVE** | Commission calcs already in `packages/core/financial/`. Comp grid Sheets I/O stays GAS until grids migrate to Firestore. |
| **DEX backend** (8K lines) | **STAYS GAS** | DriveApp + PDF blob handling. Deeply tied to Google APIs. Move only when PDF_SERVICE (Cloud Run) replaces all GAS PDF operations. |
| **RAPID_CORE** (17K lines) | **STAYS** (dies naturally) | Only exists for remaining GAS consumers. As consumers move, RAPID_CORE shrinks. |
| **RAPID_IMPORT** (106K lines) | **STAYS GAS** | Too large, too many GAS triggers, too many Google API dependencies. Adapt via bridge, don't rewrite. |

### Builder Assignments

**Builder 1 — RAPID_COMMS + RAPID_FLOW → toMachina**

RAPID_COMMS (1K lines):
- Port `COMMS_Email.gs` (288 lines) → `packages/comms/email.ts` or `services/api/routes/comms.ts`
- Port `COMMS_SMS.gs` (122 lines) → same
- Port `COMMS_Voice.gs` (125 lines) → same
- Port `COMMS_Helpers.gs` (148 lines) → shared HTTP helper
- Replace UrlFetchApp with node-fetch
- Wire into existing API routes or create `services/api/src/routes/comms.ts`
- Test: send a real SMS, send a real email via the new routes

RAPID_FLOW (2K lines):
- Port `FLOW_Engine.gs` (314 lines) → `packages/core/flow/engine.ts`
- Port `FLOW_Gates.gs` (148 lines) → `packages/core/flow/gates.ts`
- Port `FLOW_Hooks.gs` (60 lines) → `packages/core/flow/hooks.ts`
- Port `FLOW_Query.gs` (230 lines) → `packages/core/flow/query.ts`
- Port `FLOW_Tasks.gs` (340 lines) → `packages/core/flow/tasks.ts`
- Replace all RAPID_CORE.getTabData/insertRow/updateRow calls with Firestore reads/writes
- Test: create a pipeline instance, advance through stages, verify gate enforcement

Files owned: `packages/core/flow/`, `services/api/src/routes/comms.ts`, `packages/comms/` (if separate package)

**Builder 2 — C3 Backend → toMachina**

C3 is unusual — almost all logic is embedded in a 10K-line Index.html. The backend needs extraction:
- Read `archive/C3/Index.html` — extract all google.script.run call targets
- Map each backend call to an API route in `services/api/src/routes/`
- Campaign CRUD already exists in `routes/campaigns.ts` and `routes/campaign-send.ts`
- Add missing endpoints: template CRUD, content block CRUD, campaign assembly (builds final email/SMS from template + blocks), schedule management
- Wire campaign send to use the new RAPID_COMMS routes (Builder 1) instead of GAS RAPID_COMMS library
- Migrate C3's spreadsheet backend data to Firestore (if not already in `campaigns`/`templates`/`content_blocks`)

Files owned: `services/api/src/routes/campaigns.ts` (expand), `services/api/src/routes/campaign-send.ts` (expand), `services/api/src/routes/templates.ts` (new), `services/api/src/routes/content-blocks.ts` (new)

**Builder 3 — ATLAS Backend → toMachina + CAM Partial Move**

ATLAS (5K lines):
- Port `ATLAS_Registry.gs` (238 lines) → `services/api/src/routes/atlas.ts` (expand existing)
- Port `ATLAS_Tasks.gs` (425 lines) → API route
- Port `ATLAS_Analytics.gs` (296 lines) → API route
- Port `ATLAS_Audit.gs` (332 lines) → API route
- Port `ATLAS_Slack.gs` (225 lines) → API route (uses MCP Slack tools or direct Slack API)
- Port `ATLAS_Triggers.gs` (112 lines) → Cloud Scheduler calling API endpoints
- Migrate `_TOOL_REGISTRY` to Firestore `tool_registry` collection
- Test: CRUD a source, verify audit trail, verify Slack digest fires

CAM partial:
- Comp grid viewer API: read comp grids from Sheets via bridge (not direct Sheets API)
- Commission calculation already in `packages/core/financial/` — verify it matches CAM backend output
- Commission pipeline tracking → API route reading from Firestore `revenue`
- CAM's Sheets writes STAY GAS for now (comp grid management is too deeply tied)

Files owned: `services/api/src/routes/atlas.ts`, `services/api/src/routes/atlas-*.ts` (new), scripts for Tool Registry migration, `services/api/src/routes/cam.ts` (new)

### Sprint 4 Verification
- [ ] RAPID_COMMS: SMS + email send works via toMachina API (not GAS)
- [ ] RAPID_FLOW: Pipeline creation, stage advancement, gate enforcement works via Firestore (not Sheets)
- [ ] C3: Campaign CRUD, template management, send orchestration works via API
- [ ] ATLAS: Registry CRUD, audit trail, Slack digest works via API
- [ ] All GAS engine .gs files still exist (don't delete yet) but are no longer called by toMachina
- [ ] MCP tools updated to call Cloud Run instead of execute_script for migrated functions

### Sprint 4 Estimated Time: 2 sessions (4-5 hours per builder per session)

---

## Sprint 5: Infrastructure Cutover + Cleanup

**Goal:** Flip the switches. Deploy the API + Bridge to Cloud Run. Point RAPID_IMPORT to Cloud Run. Activate BigQuery streaming. Clean up dead code.

**Depends on:** Sprint 4 (all migrated engines running on toMachina)

### Builder Assignments

**Builder 1 — Production Deploy + Monitoring**

Deploy to Cloud Run:
- `services/api/` → `tm-api` Cloud Run service at `api.tomachina.com`
- `services/bridge/` → `tm-bridge` Cloud Run service (internal, no public URL)
- Create Cloud Build configs (or use Firebase App Hosting if applicable for services)
- Verify health checks pass
- Set up Cloud Monitoring alerts: error rate > 1%, latency > 2s, instance count
- Set up Cloud Logging export to BigQuery for API analytics

BigQuery streaming:
- Build Cloud Function with `onDocumentWritten("{document=**}")` trigger (Builder 3's recommendation from cleanup report)
- Deploy to GCP project `claude-mcp-484718`
- Streams all Firestore changes to `toMachina.firestore_changes` BigQuery table
- Verify: write a test doc → appears in BigQuery within 60 seconds
- Disable `com.rpi.analytics-push` launchd agent (replaced by real-time stream)

Files owned: Cloud Build configs, Cloud Functions, monitoring setup, launchd agent management

**Builder 2 — RAPID_IMPORT Cutover + MCP**

RAPID_IMPORT URL swap:
- Apply the documented code change in `gas/RAPID_IMPORT/Code.gs` (Builder 2 Phase 4+5 report has exact diff)
- Change `RAPID_API_CONFIG.URL` from GAS Web App to `https://api.tomachina.com/api`
- Add OIDC auth token via `ScriptApp.getIdentityToken()`
- Change URL construction from `?path=endpoint` to direct path `/endpoint`
- `clasp push --force`
- Test EVERY intake channel: manual import, approval pipeline, client import, account import, revenue import
- Verify watcher.js still works

MCP adaptation:
- Add `callCloudRunAPI()` to `services/MCP-Hub/rpi-workspace-mcp/src/gas-tools.js`
- Migrate MCP tools from `execute_script` → `callCloudRunAPI()` for all functions that now live on Cloud Run
- Keep `execute_script` as fallback for functions still in GAS
- Restart MCP servers to pick up changes
- Test: run MCP tools that were migrated, verify they call Cloud Run (not GAS)

Files owned: `gas/RAPID_IMPORT/Code.gs`, `services/MCP-Hub/rpi-workspace-mcp/`, MCP config

**Builder 3 — Dead Code Cleanup + Final OS Update**

GAS cleanup:
- In `gas/RAPID_CORE/`: remove any remaining dead exports in Code.gs for functions that no longer exist
- In `gas/CAM/`, `gas/C3/`, `gas/ATLAS/`: verify headless doGet() is deployed, remove any lingering HTML references in .gs files
- Archive `gas/RAPID_COMMS/` and `gas/RAPID_FLOW/` → move to `~/Projects/archive/` (they're fully replaced now)
- Run DEBUG_Ping on all remaining GAS consumers to verify nothing broke

Operating System update:
- Update `~/.claude/CLAUDE.md` — remove references to RAPID_COMMS and RAPID_FLOW as active GAS engines
- Update `ARCHITECTURE.md` — mark RAPID_COMMS and RAPID_FLOW as archived
- Update `knowledge-promote.js` PROJECT_DIRS — remove RAPID_COMMS and RAPID_FLOW paths
- Run compliance sweep — verify 0 violations
- Update `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` — remove RAPID_COMMS and RAPID_FLOW
- Update `_RPI_STANDARDS/scripts/clone-all-repos.sh` — move RAPID_COMMS and RAPID_FLOW to archive section

Document watcher migration (if time):
- Build Cloud Function to replace `com.rpi.document-watcher` launchd agent
- Trigger: Google Drive webhook or Pub/Sub on Drive changes
- Logic: same as current watcher.js but runs on Cloud Run
- This eliminates the last local always-on process

Files owned: `gas/` cleanup, `~/.claude/CLAUDE.md`, `ARCHITECTURE.md`, `_RPI_STANDARDS/`, `knowledge-promote.js`, Cloud Function for document watcher

### Sprint 5 Verification
- [ ] `api.tomachina.com` returns 200 on health check
- [ ] Bridge service running on Cloud Run
- [ ] RAPID_IMPORT successfully calls Cloud Run API (not GAS Web App)
- [ ] MCP tools call Cloud Run for migrated functions
- [ ] BigQuery receives Firestore changes in real-time
- [ ] `com.rpi.analytics-push` disabled
- [ ] RAPID_COMMS and RAPID_FLOW archived
- [ ] Compliance sweep: 0 violations
- [ ] All remaining GAS consumers still pass DEBUG_Ping

### Sprint 5 Estimated Time: 1-2 sessions (3-4 hours per builder)

---

## Sprint Summary

| Sprint | Goal | Builders | Sessions | Key Deliverable |
|--------|------|----------|----------|----------------|
| 1 | Data Integrity | 3 | 1 (RUNNING) | Clean Firestore data (29K docs normalized, FKs validated) |
| 2 | Shared Modules | 3 | 1 | 8 shared components, 24 portal pages → 3-line imports |
| 3 | Portal Depth | 3 | 1-2 | Team-ready UX: CLIENT360, RMD, Medicare quoting, DAVID HUB calcs, dashboards |
| 4 | GAS Migration | 3 | 2 | RAPID_COMMS + FLOW + C3 + ATLAS moved to toMachina |
| 5 | Infrastructure | 3 | 1-2 | Cloud Run live, RAPID_IMPORT bridged, BigQuery streaming, dead code cleaned |

**Total remaining: 6-8 sessions with 3 builders each.**

---

## JDM Decision Points

| Decision | When | Impact |
|----------|------|--------|
| Sprint 2 start | After Sprint 1 reports audited | Fires 3 builders on shared modules |
| Team rollout date | Before Sprint 3 | Drives urgency of portal depth work |
| CSG API integration scope | Sprint 3 | How deep does Medicare quoting go? |
| RAPID_IMPORT cutover approval | Sprint 5 | Production switch from GAS to Cloud Run API |
| Document watcher migration | Sprint 5 (optional) | Eliminates last local always-on process |
| MyDropZone scope | Sprint 3 (in MyRPI module) | UI placeholder now, full pipeline later? |
