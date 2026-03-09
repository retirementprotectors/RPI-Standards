# RIIMO Production Build Plan

## Context

RIIMO is RPI's B2E Operations Hub — the control plane for all shared services across SENTINEL, PRODASH, and RAPID. It's currently ~15-20% built: clean dark theme, sound data models, but fundamentally a decorated placeholder. 9 project audits revealed it needs to be the central nervous system for 14+ GAS projects, 3 MCP servers, and 179 MCP tools.

**Full audit reference:** `RIIMO/_audit/RIIMO_BUILD_PLAN.md` (618 lines, all findings + decision points)
**Individual audits:** `RIIMO/_audit/*.md` (9 files)

---

## Phase 0: Security + Cleanup (MUST DO FIRST)

### JDM Decisions (Resolved)
- **RAPID_API**: Stays `ANYONE_ANONYMOUS` — SPARK (Optum external SaaS) → SPARK_WEBHOOK_PROXY (Cloudflare Worker) → RAPID_API. Can't use DOMAIN or SPARK breaks. Security: API key on all non-SPARK routes (already done), `/pipeline` route needs API key added (currently public).
- **Timezone**: Standardize ALL projects to `America/Chicago`.
- **Healthcare API**: JDM is deploying QUE-Medicare + PRODASH on another machine. Write setup doc for healthcare-mcps deployment → Desktop + RIIMO repo.
- **Data Isolation**: NO direct access to data sources (MATRIX sheets, script IDs, deploy IDs, direct links) from ANY UI except RIIMO. Only RIIMO admins can see actual infrastructure. Downstream UIs never expose spreadsheet IDs, code locations, or database references. All data access goes through API layers, never direct sheet access from end users.

### Critical Files to Modify
| File | Change |
|------|--------|
| `RIIMO/appsscript.json` | `ANYONE_ANONYMOUS` → `DOMAIN` + add `executionApi` + fix timezone |
| `RAPID_API/appsscript.json` | **LEAVE AS ANYONE_ANONYMOUS** (approved exception — SPARK webhooks from external Optum platform require it). Fix timezone only. Clean up: make `/pipeline` route require API key (currently public, marked "temporary"). |
| `RPI-Command-Center/appsscript.json` | `ANYONE` → `DOMAIN` + fix timezone |
| `sentinel/appsscript.json` | `ANYONE` → `DOMAIN` + fix timezone |
| `RIIMO/RIIMO_MATRIX_Setup.gs` | Remove 310 lines deprecated code (lines 492-803), remove duplicate `getMATRIX()` (line 886) |
| `RIIMO/RIIMO_Core.gs` | Remove duplicate `getModuleLastSync()` fake return, fix `getModuleMetrics()` to return "not tracked" |
| `RIIMO/RIIMO_Pipelines.gs` | Replace all fake `execute*()` returns with honest "Not implemented" |
| `RIIMO/Index.html` | Fix `event.currentTarget` capture (line 1328), add `.modal-overlay` CSS, fix default permissions |
| `RIIMO/Code.gs` | Remove dead `include()` function |
| ALL projects with wrong timezone | Fix `appsscript.json` timezone to `America/Chicago` |

**Also across 7+ projects:** Add `"executionApi": { "access": "DOMAIN" }` to appsscript.json for DEX, C3, CAM, CEO-Dashboard, RPI-Command-Center, SENTINEL v2, DAVID-HUB — this unblocks MCP execute_script for RIIMO to call them.

**Immediate action:** Write healthcare-mcps setup doc to JDM's Desktop + RIIMO repo (JDM is setting up another machine RIGHT NOW).

Deploy + verify each changed project.

---

## Cascading Permission Model (JDM's Design)

RIIMO is THE master permission source. Permissions cascade top-down:

```
Tier 1: RIIMO
├── OWNER (JDM) — all access, final authority
└── SUPER ADMIN (John Behn) — creates admins, assigns RIIMO modules
    └── Assigns Admin to modules → TWO things happen:
        1. Admin gets view/edit in RIIMO for those modules
        2. Admin gets ADMIN role inside that module's actual UI

Tier 2: Module UIs (PRODASH, SENTINEL, CAM, DEX, C3, etc.)
├── Admin (pushed from RIIMO assignment) — manages their team's access
└── Creates user entitlements: view-only, agent, service, etc.
    └── Controls which sub-modules their team sees + can edit

Tier 3: End Users (sales/service team)
└── Access determined by their admin in the module UI
```

**Example flow:**
- Behn assigns Nikki as admin for PRODASH + RAPID_IMPORT in RIIMO
- Nikki now sees PRODASH + RAPID_IMPORT modules in RIIMO (view/edit)
- Nikki is ALSO automatically an admin inside PRODASH itself
- Inside PRODASH, Nikki can grant Susan access to Medicare Center (view), RMD Center (edit)
- Susan sees only what Nikki authorized

**Data Isolation Rule (NON-NEGOTIABLE):**
- NO spreadsheet IDs, script IDs, deploy IDs, or direct MATRIX links exposed in any UI except RIIMO
- Only RIIMO admins can see the actual infrastructure (project registry, MATRIX connections, deploy status)
- Downstream UIs (PRODASH, SENTINEL, CAM, etc.) access data ONLY through API layers (RAPID_API, RAPID_CORE functions) — never direct sheet access from end users
- No one touches actual code or data itself unless they are admins of RIIMO
- This means: scrub any existing MATRIX ID references from downstream UI HTML, move all direct sheet access behind server-side functions

**Implication for the build:**
- RIIMO's `_USER_HIERARCHY` is the master source
- Each downstream UI needs an admin panel that reads from RIIMO's assignments (or syncs via RAPID_CORE/RAPID_API)
- Phase 1 builds RIIMO's admin CRUD + the push mechanism
- Phase 2-3 builds the receiving admin panels in each downstream UI (or enhances existing ones)
- Phase 0 must audit all downstream UIs for exposed MATRIX IDs in rendered HTML (PRODASH, SENTINEL, etc.)

---

## Phase 1: Foundation (Session 2-3)

### Core Infrastructure
1. **GAS Project Registry** — `_GAS_PROJECTS` tab in RAPID_MATRIX tracking all 13+ projects (script ID, deploy version, RAPID_CORE version, GCP linked, access setting)
2. **Real MATRIX health checks** — replace hardcoded "Connected" with actual SpreadsheetApp.openById() try/catch
3. **Remove hardcoded MATRIX_IDS** — use RAPID_CORE.getMATRIX_IDS() exclusively
4. **Dynamic sidebar** — render from `uiGetToolSuites()` respecting cascading permissions
5. **showToast()** — transient feedback component (success/error/info)
6. **Module pages with real links** — each module links to its actual GAS web app URL + shows deploy health from registry
7. **Error feed card** — read RAPID_CORE `_ERROR_LOG`, show last 24h grouped by source + severity
8. **API caller utility** — centralized `callRapidAPI()` for all backend calls
9. **Populate _USER_HIERARCHY** — JDM=OWNER, Behn=SUPER_ADMIN
10. **Admin CRUD (Tier 1)** — Behn can: create admins, assign them to RIIMO modules (view/edit), which simultaneously grants them admin role in downstream UIs
11. **Permission sync mechanism** — when RIIMO assigns admin for a module, push that role to the module's `_USER_HIERARCHY` (or equivalent) via RAPID_API

### Key Patterns to Reuse
- `PRODASH/PRODASH_Core.gs` → `callRapidAPI_()` pattern (line ~50)
- `CAM/Code.gs` → structured `ui*` wrapper pattern
- `CEO-Dashboard/_GAS_PROJECTS` → project registry schema already designed
- Existing CSS design tokens in `Index.html` `:root` block
- Existing card grid, sidebar dropdown, pipeline stage components

---

## Phase 2: Visibility (Session 4-7)

12 dashboard cards pulling real data from across the ecosystem. Priority order:
1. System Health Panel (deploy versions, API pings, MATRIX connectivity)
2. Data Pipeline Card (RAPID_IMPORT intake/approval queues)
3. Error Feed (aggregated from _ERROR_LOG)
4. Commission/Revenue Card (from CAM)
5. B2C Client Health (RMDs, beneficiary gaps, Medicare alerts)
6. MCP-Hub Status (server health, token expiry, CMS data age)
7. B2B Pipeline Card (SENTINEL deals, DAVID-HUB leads)
8. GHL Sync Status
9. Config Drift Monitor
10. CEO Commitments Card
11. Campaign Readiness
12. Document Pipeline (DEX)

---

## Phase 3: Control (Session 8-11)

Operations console with trigger buttons + real pipeline implementations:
- One-click triggers: GHL Sync, Reconciliation, Config Audit, Cache Clear, Comp Cycle
- Reconciliation Queue UI (resolve 19 client dupes)
- Real Data Maintenance pipeline (actual cleanup + backup)
- On-boarding/Off-boarding pipeline tracking
- Security pipeline connected to real audit tools
- Log viewer with filters

---

## Phase 4: Intelligence (Session 12-16)

Cross-platform analytics + TDM scoring:
- TDM Level scoring (Levels 0-5 per client)
- Data quality KPIs (orphans, dupes, normalization coverage)
- Revenue + Pipeline analytics
- MDJ Instance dashboard
- Carrier intelligence

---

## Today's Session Scope

### Immediate (before Phase 0)
1. Copy to JDM's Desktop: `RIIMO_BUILD_PLAN.md` + `riimo-self-audit.md` + this plan file
2. Write healthcare-mcps setup doc to Desktop + RIIMO repo (JDM is setting up another machine NOW)

### Phase 0 (security + cleanup)
All 13 tasks — security fixes, cleanup, bug fixes, honest returns, timezone standardization. Deploy and verify every changed project.

### Phase 1 start (if time remains)
Foundation items: registry, health checks, dynamic sidebar, showToast, cascading permission CRUD.

---

## Verification

After Phase 0:
1. Open RIIMO in incognito — should require RPI org login
2. Open RPI-Command-Center in incognito — should require org login
3. Open Legacy SENTINEL in incognito — should require org login
4. `clasp deployments` on each project — verify @version matches
5. Confirm no fake metrics in RIIMO UI — should show "Not tracked" or "Not implemented"
6. Test pipeline stage execution — DOM should update correctly after confirmation modal

After Phase 1:
1. Sidebar shows only permitted modules for logged-in user
2. Module pages link to real web app URLs
3. Error feed shows actual errors from _ERROR_LOG
4. Admin panel has working user CRUD
5. GAS Project Registry tab exists with real data
