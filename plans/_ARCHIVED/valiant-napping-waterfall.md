ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# toMachina — Platform Launch Plan

> *"to The Machine"* — the enterprise platform for Retirement Protectors, Inc.
> Domains secured: `tomachina.ai` · `tomachina.com` · `tomachina.io`

## Context

RPI's three portals (PRODASHX, RIIMO, SENTINEL) are built on Google Apps Script HtmlService — sandboxed iframes with 30-60 second load times, serialization bugs, and a 6-step deploy process. ~40% of the global CLAUDE.md (260 lines), 15 of 28 hookify rules, and all 14 GAS Gotchas exist solely to prevent GAS from breaking things. Zero users are on any portal yet — this is a clean-slate opportunity to launch toMachina on a modern stack instead of retrofitting GAS.

**Goal:** Launch toMachina — Next.js portals, Firestore database, Cloud Run services — while keeping GAS engines (RAPID_FLOW, RAPID_IMPORT, RAPID_COMMS) for what they're good at (Sheets automation, triggers, background jobs).

**What already exists on the modern side:**
- GCP project `claude-mcp-484718` with Cloud Run, BigQuery, Artifact Registry
- 3 Cloud Run services running: `que-api`, `rpi-pdf-service`, `prodash-api`
- Cloud Build configs proven (Docker → Artifact Registry → Cloud Run deploy)
- `prodash-api/server.js` — Express + BigQuery pattern (722 lines, production)
- Google OAuth with 33 scopes via MCP-Hub
- BigQuery datasets (SERFF_MedSupp, PRODASH_Data)

---

## Phase 0: Foundation

**Goal:** Monorepo scaffold, Firestore, Firebase Auth, Cloud Build pipeline, custom domains.

### 0.1 — New GitHub Repo + Monorepo

Create `retirementprotectors/toMachina`:

```
toMachina/
├── apps/
│   ├── prodash/              # Next.js 15 (App Router)
│   ├── riimo/                # Next.js 15 (App Router)
│   └── sentinel/             # Next.js 15 (App Router)
├── packages/
│   ├── ui/                   # Shared component library (from PortalStandard.html)
│   ├── core/                 # Business logic (from RAPID_CORE non-Sheets functions)
│   ├── auth/                 # Firebase Auth + entitlement engine
│   └── db/                   # Typed Firestore client + normalizers
├── services/
│   ├── api/                  # Cloud Run unified REST API (expands prodash-api pattern)
│   └── bridge/               # Dual-write bridge (Firestore + Sheets during transition)
├── turbo.json                # Turborepo incremental builds
├── package.json              # Workspace root
├── cloudbuild.yaml           # Monorepo Cloud Build config
├── CLAUDE.md                 # Project-specific rules (modern stack only)
└── .github/
```

**Tooling:** Turborepo for monorepo management. Each app/service builds independently. `turbo run build --filter=...[HEAD~1]` for incremental builds.

### 0.2 — Firestore Setup

In GCP project `claude-mcp-484718`:
- Enable Firestore in Native mode (us-central1)
- Security rules: require `@retireprotected.com` domain in auth token

**Collection design (maps from TABLE_ROUTING in CORE_Database.gs):**

| Firestore Collection | Source Sheet Tab | Key Design Decision |
|---------------------|-----------------|-------------------|
| `/clients/{client_id}` | `_CLIENT_MASTER` | 107 fields, JSON columns become native objects |
| `/clients/{id}/accounts/{account_id}` | `_ACCOUNT_*` (5 types) | Subcollection — most queries are "accounts for client X" |
| `/clients/{id}/activities/{activity_id}` | `_ACTIVITY_LOG` | Subcollection for per-client history |
| `/clients/{id}/relationships/{rel_id}` | `_RELATIONSHIPS` | Subcollection |
| `/agents/{agent_id}` | `_AGENT_MASTER` | Top-level, FK to producers/accounts |
| `/producers/{producer_id}` | `_PRODUCER_MASTER` | Top-level |
| `/opportunities/{opp_id}` | `_OPPORTUNITIES` / `Opportunities` | Both PRODASH + SENTINEL deals |
| `/revenue/{revenue_id}` | `_REVENUE_MASTER` | Top-level, FKs to accounts + agents |
| `/carriers/{carrier_id}` | `_CARRIER_MASTER` | Reference data |
| `/products/{product_id}` | `_PRODUCT_MASTER` | Reference data |
| `/users/{email}` | `_USER_HIERARCHY` | Auth + entitlements, JSON fields native |
| `/org/{unit_id}` | `_COMPANY_STRUCTURE` | Org hierarchy |
| `/campaigns/{campaign_id}` | `_CAMPAIGNS` | Campaign engine |
| `/templates/{template_id}` | `_TEMPLATES` | 661 templates |
| `/content_blocks/{block_id}` | `_CONTENT_BLOCKS` | Campaign building blocks |
| `/flow/pipelines/{pipeline_key}` | `_FLOW_PIPELINES` | RAPID_FLOW config |
| `/flow/instances/{instance_id}` | `_FLOW_INSTANCES` | RAPID_FLOW runtime |
| `/atlas/sources/{source_id}` | `_SOURCE_REGISTRY` | ATLAS registry |
| `/comp_grids/{type}/{grid_id}` | `_*_COMP_GRID` | 4 compensation grids |
| `/case_tasks/{task_id}` | `_CASE_TASKS` | Case management |
| `/communications/{comm_id}` | `_COMMUNICATION_LOG` | Comms audit trail |

**Schema mapping rules:**
- Column names → field names (already snake_case)
- `created_at`/`updated_at` → Firestore Timestamps (native, no serialization bugs)
- Date fields (16 types in FIELD_NORMALIZERS) → Firestore Timestamps
- Amount fields (22 types) → Firestore numbers
- JSON columns (aliases, employee_profile, beneficiaries, riders, custom_fields) → native nested objects
- FK columns → string UUIDs (no Firestore references needed)
- PK is always `schema[0]` → becomes document ID

### 0.3 — Firebase Auth

- Enable Firebase Auth in GCP project `claude-mcp-484718`
- Configure Google as OIDC provider, restrict to `retireprotected.com` domain
- Port entitlement engine from `CORE_Entitlements.gs` to `packages/auth/`:
  - USER_LEVELS (OWNER=0, EXECUTIVE=1, LEADER=2, USER=3)
  - TOOL_SUITES (5 suites: RAPID, RPI, DAVID, PIPELINES, ADMIN)
  - MODULES (46 module definitions with minUserLevel, suite, status)
  - `evaluateAccess(email, moduleKey, action)` → boolean

### 0.4 — Cloud Build Pipeline

Expand proven `cloudbuild.yaml` pattern (from QUE-API):
- Trigger on push to `main` branch of `toMachina`
- Turborepo incremental build
- Each app → separate Cloud Run service (`tm-prodash`, `tm-riimo`, `tm-sentinel`)
- Each service → separate Cloud Run service (`tm-api`, `tm-bridge`)
- Health check after deploy
- Slack notification to JDM DM (`U09BBHTN8F2`)

### 0.5 — Custom Domains (toMachina)

**Primary domain: `tomachina.com`**

| URL | Cloud Run Service | Purpose |
|-----|------------------|---------|
| `prodash.tomachina.com` | `tm-prodash` | B2C portal (team + clients) |
| `riimo.tomachina.com` | `tm-riimo` | B2E portal (operations) |
| `sentinel.tomachina.com` | `tm-sentinel` | B2B portal (M&A + partnerships) |
| `api.tomachina.com` | `tm-api` | Unified REST API |
| `tomachina.com` | Static / marketing | Landing page (future) |

**Future domains:**
- `tomachina.ai` — AI/intelligence features, public-facing tools
- `tomachina.io` — Developer docs, API documentation, partner integrations

DNS CNAME records in domain registrar → Cloud Run custom domain mapping.

### JDM Manual Steps (One-Time)
1. Enable Firestore in GCP Console (`claude-mcp-484718`) — 2 clicks
2. Enable Firebase Auth in GCP Console — 2 clicks
3. Add DNS records for `tomachina.com` subdomains (prodash, riimo, sentinel, api)
4. Create GitHub repo `retirementprotectors/toMachina`

### Verification
- `turbo run build` succeeds for all apps (empty shells)
- Firestore console accessible, security rules deployed
- Firebase Auth test login with `@retireprotected.com` works
- Cloud Build triggers on push to main
- `prodash.tomachina.com`, `riimo.tomachina.com`, `sentinel.tomachina.com`, `api.tomachina.com` all resolve

---

## Phase 1: PRODASHX Portal (First Portal)

**Why PRODASHX first:** Largest portal (~12K lines frontend, 35 .gs backend files), most pain (30-60s load times), and JDM explicitly said "There's literally no way I can hand ProDashX to my Team next week." Proving the pattern on the hardest portal de-risks everything. Zero users = zero disruption.

### 1.1 — Shared UI Package (`packages/ui`)

Convert `PortalStandard.html` (23.5KB shared design system) to React:

| GAS Component | React Component | Source File |
|--------------|----------------|------------|
| CSS variables (dark theme) | `styles/tokens.css` + Tailwind config | PortalStandard.html lines 27-60 |
| Sidebar (collapsible sections) | `Sidebar.tsx` + `SidebarSection.tsx` + `SidebarItem.tsx` | PortalStandard.html + Scripts.html `renderSidebar()` |
| Modal (flexbox scroll) | `Modal.tsx` | PortalStandard.html `.std-modal` |
| Toast notifications | `Toast.tsx` + `useToast()` hook | `showToast()` in each portal |
| Confirmation dialog | `ConfirmDialog.tsx` + `useConfirm()` hook | `showConfirmation()` in each portal |
| Loading overlay | `LoadingOverlay.tsx` | `showLoading()`/`hideLoading()` |
| Smart Lookup | `SmartLookup.tsx` | `buildSmartLookup()` pattern |
| Data Table | `DataTable.tsx` (sortable, filterable) | Custom table rendering in each portal |
| Kanban Board | `KanbanBoard.tsx` | Pipeline board in PRODASHX/RIIMO |
| RPI Connect | `ConnectPanel.tsx` | `RPI_Connect.html` (56KB, all 3 portals) |

Each portal sets its theme via CSS variable overrides in layout:
- PRODASHX: `--portal: #3d8a8f` (teal)
- RIIMO: `--portal: #276749` (dark green)
- SENTINEL: `--portal: #3CB371` (green)

### 1.2 — Auth Package (`packages/auth`)

- Firebase Auth provider wrapper with Google Workspace SSO
- `useAuth()` hook → `{ user, loading, entitlements }`
- Middleware for protected routes (redirect to Google sign-in if unauthenticated)
- Entitlement engine ported from `CORE_Entitlements.gs`
- Role-based sidebar rendering (same as current `hasModuleAccess()` pattern)

### 1.3 — DB Package (`packages/db`)

- Typed Firestore client with collection references
- TypeScript interfaces matching TAB_SCHEMAS from `CORE_Database.gs`
- `useDocument()` and `useCollection()` hooks with realtime listeners
- Write functions that run normalizers before writing (ported from `CORE_Database.gs` FIELD_NORMALIZERS — 90+ fields, 16 normalizer types)
- Dedup logic for 7 tables (clients, agents, 5 account types)

### 1.4 — Core Package (`packages/core`)

Business logic extracted from RAPID_CORE (non-Sheets functions):
- `normalizers/` — name, phone, email, date, state, zip, carrier, product, amount (from CORE_Database.gs lines 1278-1369)
- `validators/` — field validation (from CORE_Validation_API.gs)
- `matching/` — fuzzy match, dedup logic (from CORE_Match.gs)
- `financial/` — FYC, NPV, DCF calculations (from CORE_Financial.gs)
- `resolveUser()` — universal name/alias resolver (from CORE_Entitlements.gs)

### 1.5 — PRODASHX App

Route structure mapping current sidebar:

```
apps/prodash/app/
├── layout.tsx                  # TopBar + Sidebar + auth guard + teal theme
├── page.tsx                    # Redirect to /clients
├── clients/
│   ├── page.tsx                # Client grid (from uiGetClientsForGrid)
│   └── [id]/
│       ├── page.tsx            # CLIENT360 (from uiGetClient360Data)
│       ├── accounts/page.tsx   # Account tabs
│       └── activities/page.tsx # Activity feed
├── accounts/page.tsx           # Account grid (from uiGetAccountsPage)
├── pipelines/page.tsx          # Kanban boards (from uiGetPipelineData)
├── casework/page.tsx           # Case management
├── sales-centers/
│   ├── medicare/page.tsx       # QUE-Medicare (from PRODASH_QUE_MEDICARE.gs)
│   ├── life/page.tsx
│   ├── annuity/page.tsx
│   └── advisory/page.tsx
├── service-centers/
│   ├── rmd/page.tsx            # RMD Center (from uiGetRMDDashboard)
│   └── beni/page.tsx           # Beni Center (from uiGetBeniDashboard)
├── modules/
│   ├── cam/page.tsx            # Commission dashboard (CAM UI)
│   ├── dex/page.tsx            # Document efficiency (DEX UI)
│   ├── c3/page.tsx             # Campaign management (C3 UI)
│   ├── atlas/page.tsx          # Source registry (ATLAS UI)
│   └── command-center/page.tsx # Leadership visibility
├── admin/page.tsx              # Org admin
└── api/                        # Next.js API routes (server-side)
```

**All "Apps" (CAM, DEX, C3, ATLAS, Command Center) become inline modules** — no more orange dashed borders, no more `window.open()` pop-out tabs. Everything renders inside the portal.

### 1.6 — Unified API Service (`services/api`)

Expand `prodash-api/server.js` (722 lines, proven Express pattern):

```
services/api/
├── routes/
│   ├── clients.ts        # CRUD (from API_Client.gs)
│   ├── accounts.ts       # CRUD (from API_Account.gs)
│   ├── agents.ts         # CRUD (from API_Agent.gs)
│   ├── revenue.ts        # CRUD (from API_Revenue.gs)
│   ├── users.ts          # Auth + entitlements (from API_User.gs)
│   ├── flow.ts           # Workflow engine (calls RAPID_FLOW via bridge)
│   ├── campaigns.ts      # Campaign CRUD
│   └── analytics.ts      # Dashboard aggregations
├── middleware/
│   ├── auth.ts           # Firebase Auth token verification
│   └── normalize.ts      # Data normalizers (from packages/core)
├── Dockerfile
├── cloudbuild.yaml
└── server.ts
```

Reads from Firestore. Writes through bridge service (during transition) or direct to Firestore (post-transition).

### 1.7 — Bridge Service (`services/bridge`)

Dual-write service for the transition period:
- `POST /write` accepts `{ collection, operation, id, data }`
- Writes to Firestore (primary) AND Sheets via Sheets API (secondary)
- If Sheets write fails, logs error but does NOT rollback Firestore
- GAS engines call this via `UrlFetchApp.fetch()` (same pattern as `callProdashAPI_()`)

RAPID_CORE gets a thin wrapper (`CORE_Bridge.gs`):
```javascript
function insertRow(tabName, data) {
  var bridgeResult = callBridge_('insert', tabName, data);
  if (bridgeResult && bridgeResult.success) return bridgeResult;
  return insertRow_sheets_(tabName, data);  // Fallback
}
```

This means ZERO changes to RAPID_IMPORT, C3, CAM, DEX, or any other GAS consumer of RAPID_CORE. They call `insertRow()` and it just works — the bridge handles both stores.

### Minimal Viable First Feature

**Client List + CLIENT360** — proves the full stack end-to-end:
1. Login via Firebase Auth (Google SSO)
2. Sidebar renders based on entitlements
3. Client list loads from Firestore (4,649 clients) with search + pagination
4. Click client → CLIENT360 with tabs (Profile, Accounts, Activity, Relationships)
5. Edit client → write persists to Firestore + Sheets via bridge
6. Page loads in < 2 seconds (vs. 30-60 seconds today)

### Verification
- `prodash.tomachina.com` loads, Google SSO works
- Client list shows 4,649 clients, search works
- CLIENT360 renders all tabs with correct data
- Write operations persist to both Firestore and Sheets
- Load time < 2 seconds
- Sidebar shows correct modules based on user entitlements

---

## Phase 2: Data Migration (Parallel with Phase 1)

**Strategy:** Bulk load Sheets → Firestore, then dual-write bridge keeps them in sync.

### Migration Order (FK dependency chain)

**Batch 1 — Reference Data (no FKs):**
`_CARRIER_MASTER`, `_PRODUCT_MASTER`, `_IMO_MASTER`, `_ACCOUNT_TYPE_MASTER`, `_USER_HIERARCHY`, `_COMPANY_STRUCTURE`, `_PIPELINE_CONFIG`, `_DOCUMENT_TAXONOMY`, comp grids (4 tabs)

**Batch 2 — Core Entities (FKs to Batch 1):**
`_CLIENT_MASTER` (107 cols), `_AGENT_MASTER`, `_PRODUCER_MASTER`, `_PIPELINES`

**Batch 3 — Dependent Data (FKs to Batch 2):**
`_ACCOUNT_*` (5 types → subcollections under clients), `_OPPORTUNITIES`, `_RELATIONSHIPS`, `_REVENUE_MASTER`

**Batch 4 — Operational Data:**
Campaign tabs (8), ATLAS tabs (7), FLOW tabs (8), communication logs, activity logs, case tasks

**Batch 5 — SENTINEL-specific:**
`Opportunities` (SENTINEL), deal valuations

### Bulk Loader

Adapt existing `prodash-loader/load-prodash.js` pattern (already reads Sheets via API, loads to BigQuery). Change target from BigQuery to Firestore. Run normalizers during load.

### Feed-Forward to BigQuery

Firestore change streams → BigQuery export (native GCP feature, one toggle). Replaces the `com.rpi.analytics-push` cron with real-time data flow.

### Verification
- Firestore document counts match Sheets row counts for all collections
- FK integrity verified (every account's `client_id` exists in `/clients/`)
- Normalizer output matches (spot-check 100 records per collection)
- Bridge dual-write: create a test client → appears in both Firestore and Sheets
- BigQuery feed-forward shows data within seconds of Firestore write

---

## Phase 3: Remaining Portals

### 3.1 — RIIMO (Second)

Smaller (~5,800 lines), reads from all 3 platforms (proves cross-collection queries), internal operations team (more forgiving).

```
apps/riimo/app/
├── layout.tsx              # Dark green theme
├── dashboard/page.tsx      # 9-card command center
├── tasks/page.tsx          # Task system
├── myrpi/page.tsx          # Employee profile
├── pipelines/page.tsx      # Ops pipelines (ON/OFF boarding)
├── org-admin/page.tsx      # Company structure
├── intelligence/page.tsx   # AI analytics
├── modules/
│   ├── cam/page.tsx        # Commission dashboard
│   ├── dex/page.tsx        # Document efficiency
│   ├── c3/page.tsx         # Campaign management
│   ├── atlas/page.tsx      # Source registry
│   └── command-center/page.tsx
└── admin/page.tsx
```

### 3.2 — SENTINEL (Third)

Smallest (~6,000 lines), cleanest separation (calcs already in MCP-Hub), fewest MATRIX tabs.

```
apps/sentinel/app/
├── layout.tsx              # Green theme
├── deals/page.tsx          # Deal pipeline kanban
├── producers/page.tsx      # Producer management
├── analysis/page.tsx       # Business/MEC/PRP/SPH analysis
├── market-intel/page.tsx   # Agent search, carrier intel, cross-ref
├── modules/
│   ├── david-hub/page.tsx  # Entry calculators (inline, no pop-out)
│   ├── cam/page.tsx
│   ├── dex/page.tsx
│   ├── atlas/page.tsx
│   └── command-center/page.tsx
└── admin/page.tsx
```

### Verification
- All 3 portals live at their subdomains
- Cross-portal data works (RIIMO reads PRODASH client counts)
- Entitlement-gated nav works per user level
- MCP tools unchanged

---

## Phase 4: GAS Engine Thinning

### What Changes

| GAS Project | Before | After |
|-------------|--------|-------|
| **RAPID_CORE** | Full library (data + business logic + entitlements) | Sheets-only functions. Business logic → `packages/core`, entitlements → `packages/auth` |
| **RAPID_API** | GAS Web App serving REST | Retired. Replaced by `services/api/` (Cloud Run) |
| **RAPID_IMPORT** | Data ingestion + triggers | Stays GAS. Calls bridge for writes instead of direct Sheets |
| **RAPID_FLOW** | Workflow engine library | Stays GAS short-term. Long-term candidate for `packages/core/flow` |
| **RAPID_COMMS** | Twilio + SendGrid via GAS | Stays GAS short-term. Long-term → Cloud Functions |
| **CAM** | Backend + UI | Backend stays GAS (commission processing). UI → portal modules |
| **DEX** | Backend + UI | Backend stays GAS (PDF/Drive ops). UI → portal modules |
| **C3** | Backend + UI | Backend stays GAS (campaign assembly). UI → portal modules |
| **ATLAS** | Backend + UI | Backend stays GAS (registry CRUD). UI → portal modules |
| **PRODASHX** | GAS Web App | Archived. Replaced by `apps/prodash/` |
| **RIIMO** | GAS Web App | Archived. Replaced by `apps/riimo/` |
| **SENTINEL v2** | GAS Web App | Archived. Replaced by `apps/sentinel/` |

### MCP Adaptation

MCP tools are stack-agnostic. Changes:
- `gas-tools.js` gains `callCloudRunAPI()` alongside `execute_script`
- As functions move to Cloud Run, MCP tool routing shifts from GAS execution to HTTP calls
- `rpi-business-mcp` already lazy-loads team from RAPID_API `/team` endpoint — when that moves to Cloud Run, only the URL changes in MCP config

### Bridge Simplification

Once all consumers read from Firestore:
- Bridge drops Sheets writes
- Becomes thin Firestore API layer
- Eventually folds into `services/api/`
- Sheets become read-only archives, then eventually decommissioned

---

## Phase 5: Cleanup

### Archive
- GAS Web App deployments disabled (access → "No one")
- Git tag `pre-migration-archive` on portal repos
- Repos stay on GitHub (never delete history)
- MATRIX spreadsheets → read-only (then archive)

### CLAUDE.md Reduction
**Remove (~260 lines):**
- GAS Gotchas section (all 14 items)
- 6-Step Deploy process
- clasp-specific rules
- `appsscript.json` access control rules
- GAS Self-Check checklists (both commit and deploy)

**Keep:**
- Business context, team, terminology
- PHI rules, code standards
- MCP tools documentation
- Communication style, golden rules

### Hookify Rule Pruning
**Remove (15 rules):**
- `block-forui-no-json-serialize`
- `block-let-module-caching`
- `block-hardcoded-colors` (Tailwind handles this)
- `warn-date-return-no-serialize`
- `warn-modal-no-flexbox`
- `block-alert-confirm-prompt`
- `warn-plain-person-select` (SmartLookup is a React component now)
- `warn-missing-structured-response` (TypeScript enforces this)
- `block-direct-matrix-write`
- `block-hardcoded-matrix-ids`
- `block-anyone-anonymous-access`
- `block-drive-url-external`
- `quality-gate-deploy-verify`
- `quality-gate-commit-remind`
- `intent-sendit` (simplified deploy)

**Keep (13 rules):**
- `block-hardcoded-secrets`
- `block-credentials-in-config`
- `block-phi-in-logs`
- `warn-phi-in-error-message`
- `warn-inline-pii-data`
- `intent-session-start`
- `intent-immune-system-check`
- `intent-plan-mode`
- `intent-execute-plan`
- `intent-atlas-consult`
- `quality-gate-phase-complete`
- `quality-gate-audit-verify`
- `quality-gate-plan-format`

### Launchd Agent Migration
| Agent | Current | After |
|-------|---------|-------|
| `com.rpi.document-watcher` | Local polling | Cloud Run + Pub/Sub trigger |
| `com.rpi.analytics-push` | Local cron | Firestore → BigQuery change stream (automatic) |
| `com.rpi.mcp-analytics` | Local cron | Keep (MCP analytics are local) |
| `com.rpi.claude-cleanup` | Local cron | Keep (local session cleanup) |
| `com.rpi.knowledge-promote` | Local cron | Keep (local MEMORY promotion) |

---

## Folder Structure (Final State)

```
~/Projects/
├── _RPI_STANDARDS/              # Standards + governance (unchanged)
├── toMachina/                   # MONOREPO — the platform
│   ├── apps/
│   │   ├── prodash/             # Next.js B2C portal — prodash.tomachina.com
│   │   ├── riimo/               # Next.js B2E portal — riimo.tomachina.com
│   │   └── sentinel/            # Next.js B2B portal — sentinel.tomachina.com
│   ├── packages/
│   │   ├── ui/                  # Shared component library
│   │   ├── core/                # Business logic (from RAPID_CORE)
│   │   ├── auth/                # Firebase Auth + entitlements
│   │   └── db/                  # Firestore client + normalizers
│   ├── services/
│   │   ├── api/                 # Unified REST API — api.tomachina.com
│   │   └── bridge/              # Dual-write (transition only)
│   └── CLAUDE.md
├── gas/                         # GAS engines (Sheets automation only)
│   ├── RAPID_CORE/
│   ├── RAPID_FLOW/
│   ├── RAPID_IMPORT/
│   ├── RAPID_COMMS/
│   ├── ATLAS/
│   ├── CAM/
│   ├── DEX/
│   └── C3/
├── services/                    # Standalone backend services
│   ├── MCP-Hub/
│   ├── PDF_SERVICE/
│   ├── QUE-API/
│   └── Marketing-Hub/
└── archive/                     # Pre-toMachina projects
    ├── PRODASHX/
    ├── RIIMO/
    ├── sentinel-v2/
    ├── sentinel-v1/
    ├── DAVID-HUB/
    ├── CEO-Dashboard/
    └── RPI-Command-Center/
```

**27 repos → ~14 active repos.** Half the maintenance surface. One platform name: **toMachina.**

---

## Critical Files Reference

| File | Why It Matters |
|------|---------------|
| `RAPID_CORE/CORE_Database.gs` | TABLE_ROUTING (all 149+ tabs), TAB_SCHEMAS (column definitions), FIELD_NORMALIZERS (90+ fields), write pipeline. **The entire Firestore schema derives from this file.** |
| `RAPID_CORE/CORE_Entitlements.gs` | USER_LEVELS, TOOL_SUITES, MODULES (46 defs), resolveUser(). **The entire auth/permissions model derives from this file.** |
| `PRODASHX/PortalStandard.html` | 23.5KB shared design system. **The entire `packages/ui` derives from this file.** |
| `MCP-Hub/prodash-api/api/server.js` | 722-line Express + BigQuery Cloud Run service. **The pattern for `services/api/`.** |
| `PRODASHX/PRODASH_BQ_API.gs` | Proven dual-source bridge (Cloud Run + Sheets fallback). **Validates the bridge architecture.** |
| `QUE-API/cloudbuild.yaml` | Proven Cloud Build → Docker → Artifact Registry → Cloud Run deploy. **The template for all new deploys.** |

---

## Parallel Execution Strategy

Phases 0 → 1 → 3 → 4 → 5 are sequential.
**Phase 2 (data migration) runs in parallel with Phase 1** — monorepo scaffold enables both. Phase 1 builds the UI while Phase 2 loads the data. They converge when PRODASHX connects to Firestore.

Within each phase, sub-agents parallelize independent work (scaffold 3 app shells simultaneously, migrate 5 reference data collections simultaneously, etc.).

---

## What JDM Needs To Do (Total Across All Phases)

| Step | When | Duration |
|------|------|----------|
| Enable Firestore in GCP Console | Phase 0 | 2 minutes |
| Enable Firebase Auth in GCP Console | Phase 0 | 2 minutes |
| Create GitHub repo `retirementprotectors/toMachina` | Phase 0 | 1 minute |
| Point `tomachina.com` DNS to Cloud Run (4 CNAME records) | Phase 0 | 5 minutes |
| Review + approve each phase before execution | Each phase | Business decision |

**Everything else: Claude Code executes.**

---

## The Name

**toMachina** — Latin: "to The Machine."

| Domain | Purpose | Status |
|--------|---------|--------|
| `tomachina.com` | Primary platform domain | Secured |
| `tomachina.ai` | AI/intelligence branding | Secured |
| `tomachina.io` | Developer/API docs | Secured |

The internal names stay (PRODASHX, RIIMO, SENTINEL) — they're the portal identities within toMachina. The platform itself is toMachina. The repo is toMachina. The URLs are `*.tomachina.com`. When JDM pitches to investors: *"The platform is called toMachina."*
