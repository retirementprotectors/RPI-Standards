ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# Phase 4: GAS Engine Thinning — Execution Plan

> Depends on: Phases 0-3 complete (all three portals live on toMachina)
> Analysis: `~/Projects/toMachina/PHASE_4_ANALYSIS_2026-03-10.md`
> Master plan: `~/.claude/plans/valiant-napping-waterfall.md` (lines 389-421)

---

## Pre-Execution Status

Several Phase 4 items are already partially or fully complete from earlier phases:

| Sub-Phase | Plan Item | Current Status |
|-----------|-----------|----------------|
| 4a — Archive portals | Tag + disable PRODASHX, RIIMO, SENTINEL v2 | NOT STARTED |
| 4b — Port RAPID_API → services/api/ | 20 GAS endpoint files → Express routes | ~60% — Builder 2 built 21 endpoints covering clients, accounts, agents, revenue, opportunities, users, carriers, products, campaigns, case-tasks, communications, org, pipelines, health |
| 4c — Extract RAPID_CORE business logic | Pure functions → packages/core + auth | **DONE** — Builder 3 Round 1 (3,787 lines: normalizers, financial, matching, entitlements, resolveUser, 39 modules, TABLE_ROUTING) |
| 4d — Thin RAPID_CORE | Remove moved functions, update exports | NOT STARTED — depends on 4c verification |
| 4e — Archive app UIs | Delete HTML from CAM, DEX, C3, ATLAS | NOT STARTED |
| 4f — RAPID_IMPORT bridge | Point callRapidAPI_() to Cloud Run | NOT STARTED — depends on 4b |
| MCP adaptation | gas-tools.js + callCloudRunAPI() | NOT STARTED |

---

## Sub-Phase 4a: Archive Portals

**Risk: ZERO** — toMachina portals are the replacements.

### Steps
1. For each repo (PRODASHX, RIIMO, sentinel-v2):
   - `git tag pre-migration-archive` on current HEAD
   - `git push origin pre-migration-archive`
2. In each GAS project editor (or via clasp):
   - Deploy → Manage Deployments → Edit → Who has access → "No one" (disable web app)
   - Or: set `"access": "MYSELF"` in appsscript.json + clasp push
3. Move local repos:
   ```bash
   mkdir -p ~/Projects/archive
   mv ~/Projects/PRODASHX_TOOLS/PRODASHX ~/Projects/archive/PRODASHX
   mv ~/Projects/RAPID_TOOLS/RIIMO ~/Projects/archive/RIIMO
   mv ~/Projects/SENTINEL_TOOLS/sentinel-v2 ~/Projects/archive/sentinel-v2
   ```
4. Also archive these (no toMachina replacement, superseded by inline modules):
   - `sentinel-v1` → archive
   - `DAVID-HUB` → archive (calculators now inline in SENTINEL portal)
   - `CEO-Dashboard` → archive (Command Center module replaces it)
   - `RPI-Command-Center` → archive (Command Center module replaces it)

### Verification
- [ ] All 7 repos tagged `pre-migration-archive`
- [ ] All GAS web app deployments disabled
- [ ] Repos moved to `~/Projects/archive/`
- [ ] toMachina portals still accessible (no dependency on archived projects)

### Builder Assignment: **Builder 1** (owns main, knows the repo structure)
**Effort: ~30 minutes**

---

## Sub-Phase 4b: Complete RAPID_API → services/api/ Port

**Risk: MEDIUM** — need to verify coverage gap between 20 GAS endpoint files and 21 existing Express routes.

### Gap Analysis

Builder 2's existing routes vs. RAPID_API files:

| RAPID_API File | Express Route | Status |
|---------------|---------------|--------|
| API_Client.gs | routes/clients.ts | ✅ Done |
| API_Account.gs | routes/accounts.ts | ✅ Done |
| API_Agent.gs | routes/agents.ts | ✅ Done |
| API_Revenue.gs | routes/revenue.ts | ✅ Done |
| API_Opportunity.gs | routes/opportunities.ts | ✅ Done |
| API_Pipeline.gs | routes/pipelines.ts | ✅ Done |
| API_User.gs | routes/users.ts | ✅ Done |
| API_Task.gs | routes/case-tasks.ts | ✅ Done |
| API_Comms.gs | routes/communications.ts | ✅ Done |
| API_Reference.gs | routes/carriers.ts + routes/products.ts | ✅ Done |
| API_Activity.gs | (via clients/:id/activities) | ✅ Done |
| API_Relationship.gs | (via clients/:id/relationships) | ✅ Done |
| API_Producer.gs | (covered by agents) | ✅ Done |
| **API_Campaign.gs** (1,206 lines) | routes/campaigns.ts (basic) | ⚠️ PARTIAL — GAS has full campaign management + send orchestration |
| **API_CampaignSend.gs** (755 lines) | — | ❌ NOT PORTED |
| **API_Booking.gs** (570 lines) | — | ❌ NOT PORTED |
| **API_Compliance.gs** (959 lines) | — | ❌ NOT PORTED |
| **API_Import.gs** (856 lines) | — | ❌ NOT PORTED |
| **API_Spark.gs** (550 lines) | — | ❌ NOT PORTED — webhook handler for carrier data |
| **API_Sync.gs** (334 lines) | — | ❌ NOT PORTED |
| **API_Analytics.gs** (296 lines) | — | ❌ NOT PORTED |
| **API_Webhook.gs** (311 lines) | — | ❌ NOT PORTED |
| **API_Rules.gs** (126 lines) | — | ❌ NOT PORTED |
| API_GHL_Sync.gs (1,661 lines) | — | SKIP — retained for M&A, not actively used |

**9 endpoint files still need porting** (~4,807 lines of GAS → Express routes).

### Steps
1. Read each unported GAS file
2. Port the endpoint logic to Express routes in `services/api/src/routes/`
3. Each route reads/writes Firestore (primary) + bridge dual-write
4. Maintain same endpoint paths where possible (makes RAPID_IMPORT URL swap easier)
5. Add validation middleware to all new write routes

### New Route Files Needed

| Route File | GAS Source | Priority | Notes |
|-----------|-----------|----------|-------|
| `routes/campaign-send.ts` | API_CampaignSend.gs | HIGH | Campaign execution engine — sends emails/SMS via RAPID_COMMS |
| `routes/compliance.ts` | API_Compliance.gs | MEDIUM | Quarterly audit, offboarding checks |
| `routes/booking.ts` | API_Booking.gs | MEDIUM | Meeting/appointment booking |
| `routes/import.ts` | API_Import.gs | HIGH | Data import endpoints (RAPID_IMPORT calls these) |
| `routes/spark.ts` | API_Spark.gs | LOW | Carrier data webhook — only fires on inbound carrier feeds |
| `routes/sync.ts` | API_Sync.gs | MEDIUM | Reconciliation endpoints |
| `routes/analytics.ts` | API_Analytics.gs | LOW | AI analytics push/query |
| `routes/webhooks.ts` | API_Webhook.gs | LOW | Generic webhook handler |
| `routes/rules.ts` | API_Rules.gs | LOW | Automation rules — small file |

### Verification
- [ ] All 9 new route files created and compiling
- [ ] Auth middleware applied to all routes
- [ ] Validation middleware on all write routes
- [ ] `turbo run build` passes for services/api
- [ ] Endpoint paths match RAPID_API paths (for URL swap compatibility)

### Builder Assignment: **Builder 2** (owns services/api/, built the existing routes)
**Effort: ~2-3 hours**

---

## Sub-Phase 4c: Verify RAPID_CORE Business Logic Port

**Status: DONE** (Builder 3 Round 1)

### What Was Ported
- 16 normalizer types, 123 field mappings → `packages/core/src/normalizers/`
- 14 financial functions → `packages/core/src/financial/`
- 10 matching functions → `packages/core/src/matching/`
- 39 module definitions + entitlement evaluation → `packages/core/src/users/`
- resolveUser sync + async → `packages/core/src/users/`
- TABLE_ROUTING + FIRESTORE_COLLECTIONS → `packages/core/src/collections/`
- 11 validators → `packages/core/src/validators/`

### Verification (confirm before 4d)
- [ ] Every function in CORE_Normalize.gs has a TypeScript equivalent in packages/core
- [ ] Every function in CORE_Financial.gs has a TypeScript equivalent
- [ ] Every function in CORE_Match.gs (pure algorithm functions) has a TypeScript equivalent
- [ ] All 39 MODULES from CORE_Entitlements.gs are in packages/core/src/users/modules.ts
- [ ] `turbo run build --filter=@tomachina/core` passes

### Builder Assignment: **Auditor verifies** (cross-reference GAS source vs TypeScript port)
**Effort: ~30 minutes**

---

## Sub-Phase 4d: Thin RAPID_CORE

**Risk: MEDIUM-HIGH** — RAPID_CORE is a library dependency for 8+ GAS projects. Breaking it breaks everything.

### Strategy
RAPID_CORE keeps ALL Sheets-specific functions. We only remove pure business logic functions that now live in packages/core and packages/auth.

**CRITICAL DECISION: normalizeData_() pipeline**

The `normalizeData_()` function in CORE_Database.gs is called on every `insertRow()` and `updateRow()`. It calls normalizer functions from CORE_Normalize.gs. Options:

| Option | Approach | Risk |
|--------|----------|------|
| **A: Keep normalizers in both places** | RAPID_CORE keeps its own copy of normalizers. packages/core has the TypeScript version. They drift over time. | LOW risk now, MEDIUM maintenance burden |
| **B: Remove normalizers from RAPID_CORE** | normalizeData_() stops auto-normalizing on Sheets writes. Bridge writes from toMachina arrive pre-normalized. GAS-direct writes (RAPID_IMPORT) lose auto-normalization. | HIGH risk — data quality regression |
| **C: RAPID_CORE calls bridge for normalization** | normalizeData_() calls the bridge service to normalize, then writes to Sheets. Adds network hop to every write. | MEDIUM risk — latency, complexity |

**RECOMMENDATION: Option A.** Keep normalizers in RAPID_CORE for now. The GAS versions are frozen — they don't change. The TypeScript versions in packages/core are the "living" copies. When RAPID_IMPORT eventually routes all writes through the bridge (Phase 4f), the GAS normalizers become dead code and can be removed.

### What Gets Removed From RAPID_CORE

| File | Action | Lines Removed |
|------|--------|---------------|
| CORE_Financial.gs | DELETE entire file | 544 |
| CORE_Compliance.gs | DELETE entire file | 363 |
| CORE_Entitlements.gs | THIN — remove pure logic functions, keep getUserHierarchy() (reads Sheets) | ~1,200 of 1,798 |
| CORE_Match.gs | THIN — remove pure algorithm functions (levenshtein, fuzzyMatch, calculateMatchScore). Keep matchClient/matchAccount/matchAgent (they call getTabData). | ~200 of 565 |
| CORE_OrgAdmin.gs | THIN — remove business logic. Keep getAllUsersForPlatform (reads Sheets). | ~300 of 674 |
| CORE_Validation_API.gs | THIN — remove functions that moved to packages/core. Keep UrlFetchApp wrappers. | ~400 of 717 |
| Code.gs | UPDATE — remove exports for deleted/thinned functions | ~200 of 564 |

**Total removed: ~3,200 lines** (RAPID_CORE goes from 17,172 → ~13,972)
**CORE_Normalize.gs: STAYS** (Option A — frozen copy for GAS consumers)

### Steps
1. Create a verification script that calls every remaining RAPID_CORE function from each consumer project
2. Delete CORE_Financial.gs, CORE_Compliance.gs
3. Thin CORE_Entitlements.gs, CORE_Match.gs, CORE_OrgAdmin.gs, CORE_Validation_API.gs
4. Update Code.gs exports
5. `clasp push --force` to RAPID_CORE
6. Run verification script — all consumer projects must still work
7. Deploy new RAPID_CORE version

### Verification
- [ ] RAPID_IMPORT DEBUG_Ping succeeds
- [ ] RAPID_FLOW DEBUG_Ping succeeds
- [ ] ATLAS DEBUG_Ping succeeds
- [ ] CAM DEBUG_Ping succeeds
- [ ] DEX DEBUG_Ping succeeds
- [ ] C3 DEBUG_Ping succeeds (minimal dependency)
- [ ] RAPID_API still works (until fully retired)
- [ ] All consumer projects can still call getTabData, insertRow, updateRow
- [ ] normalizeData_() pipeline still runs on insertRow/updateRow

### Builder Assignment: **Builder 3** (ported the business logic, knows what moved and what stays)
**Effort: ~2 hours**

---

## Sub-Phase 4e: Archive App UIs

**Risk: LOW** — backends stay, only HTML files removed.

### Steps
For CAM, DEX, C3, ATLAS:
1. Delete all .html files (Index.html, Scripts.html, Styles.html, docs/*.html)
2. Update Code.gs `doGet()` to return a JSON status page instead of HtmlService:
   ```javascript
   function doGet(e) {
     return ContentService.createTextOutput(
       JSON.stringify({ status: 'active', mode: 'headless', ui: 'archived — use toMachina portals' })
     ).setMimeType(ContentService.MimeType.JSON);
   }
   ```
3. `clasp push --force` each project
4. Verify backend functions still work via `execute_script`

### Verification
- [ ] CAM: `DEBUG_Ping` succeeds, doGet returns JSON status
- [ ] DEX: `DEBUG_Ping` succeeds, doGet returns JSON status
- [ ] C3: `DEBUG_Ping` succeeds, doGet returns JSON status (note: C3 is almost all HTML — this effectively guts it)
- [ ] ATLAS: `DEBUG_Ping` succeeds, doGet returns JSON status

### Builder Assignment: **Builder 1** (owns GAS deployments, knows the 6-step deploy process)
**Effort: ~1 hour**

---

## Sub-Phase 4f: RAPID_IMPORT Bridge Adaptation

**Risk: MEDIUM** — RAPID_IMPORT is the largest GAS project (106K LOC) and the primary data ingestion engine.

### Strategy
Minimal changes. Two adaptations:

**Adaptation 1: Redirect callRapidAPI_() to Cloud Run**
In RAPID_IMPORT `Code.gs`, change `RAPID_API_CONFIG.URL` from the GAS Web App URL to the Cloud Run `api.tomachina.com` URL. Since callRapidAPI_() uses UrlFetchApp with JSON, and the Cloud Run API maintains compatible endpoint paths and response format, this should be nearly transparent.

**Adaptation 2: Verify all paths still work**
RAPID_IMPORT has multiple intake channels (Drive, Gmail, Meet, manual) that all eventually call RAPID_CORE or RAPID_API. Each path must be verified after the URL change.

### Steps
1. Update `RAPID_API_CONFIG.URL` in Code.gs to `https://api.tomachina.com`
2. Add Firebase/Cloud Run auth token to callRapidAPI_() (the Cloud Run API requires Bearer token auth)
   - Use `ScriptApp.getIdentityToken()` for OIDC (same pattern as QUE-API)
3. Test each intake channel:
   - Manual import trigger
   - Approval pipeline flow
   - Client/Account/Revenue import functions
4. Verify MCP-Hub watcher.js still works (it calls RAPID_IMPORT functions via execute_script)

### Verification
- [ ] callRapidAPI_() successfully hits Cloud Run API
- [ ] Auth token accepted by Cloud Run
- [ ] Client import end-to-end works
- [ ] Account import end-to-end works
- [ ] Approval pipeline flow works
- [ ] watcher.js functions still execute

### Builder Assignment: **Builder 2** (owns services/api/, built the bridge, understands the API contract)
**Effort: ~1-2 hours**

---

## MCP Adaptation

### Steps
1. In `MCP-Hub/rpi-workspace-mcp/gas-tools.js`, add `callCloudRunAPI(url, method, body)` function alongside `execute_script`
2. For any MCP tool that currently calls a RAPID_API GAS function, add a Cloud Run fallback:
   ```javascript
   async function getTeam() {
     try {
       return await callCloudRunAPI('https://api.tomachina.com/api/users', 'GET');
     } catch {
       return await execute_script(RAPID_API_SCRIPT_ID, 'getTeamForUI');
     }
   }
   ```
3. Gradually shift MCP tools from GAS execution to Cloud Run HTTP calls
4. Update MCP-Hub CLAUDE.md with the new routing pattern

### Builder Assignment: **Builder 2** (owns services, understands API routing)
**Effort: ~1 hour**

---

## Builder Lane Assignments (Summary)

| Builder | Sub-Phases | Est. Time |
|---------|-----------|-----------|
| **Builder 1** | 4a (archive portals) + 4e (archive app UIs) | 1.5 hours |
| **Builder 2** | 4b (complete API port) + 4f (RAPID_IMPORT bridge) + MCP adaptation | 3-4 hours |
| **Builder 3** | 4d (thin RAPID_CORE) + 4c verification | 2.5 hours |

**Total: One session with 3 builders. Phase 4 done.**

---

## JDM Manual Steps

| Step | When | Duration |
|------|------|----------|
| Approve RAPID_CORE thinning approach (Option A: keep normalizers in both places) | Before 4d starts | Business decision |
| First-time auth for any GAS project that hasn't been deployed recently | If clasp push fails on auth | 2 minutes per project |
| Verify toMachina portals still work after all archival | After Phase 4 complete | 5 minutes |
