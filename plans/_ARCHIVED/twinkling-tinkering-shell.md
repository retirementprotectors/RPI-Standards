# RIIMO Autonomous Build — Full Send (Phase 0 → 1 → 2)

## Context

RIIMO v1.8.2 has solid scaffolding but 9 fake metric functions, dead code, bugs, and no real operational data. JDM gave all decisions and is going to sleep. Full autonomous execution.

---

## Resolved Decisions

### From JDM

**User Hierarchy:**
| Person | RIIMO Level | Platform Access |
|--------|-------------|-----------------|
| JDM (josh@retireprotected.com) | OWNER (0) | All |
| John Behn (john@retireprotected.com) | EXECUTIVE (1) | All |
| Matt McCormick | LEADER (2) | DAVID Tools + RAPID Tools |
| Vince Vazquez | LEADER (2) | RPI Tools + RAPID Tools |
| Nikki Gray | LEADER (2) | RPI Tools + RAPID Tools |
| Dr. Aprille Trupiano | LEADER (2) | RPI Tools + RAPID Tools |
| Shane Parmenter | NOT in RIIMO | N/A |
| Jason Moran | NOT in RIIMO | N/A |

**Medicare Platform:** QUE-Medicare stays standalone as middleware. PRODASH embeds/wraps it for client context. Same pattern for future QUE-Annuity, QUE-Life. These are MDJ middleware tools. Can also be client-facing (self-service MDJ).

**Healthcare-mcps:** Cloud Run (~$20/mo) via GCP project 90741179392. Deploying TONIGHT after RIIMO Phase 2. gcloud CLI installed + authenticated. Local CMS data files (~2.7GB) are necessary (no API replacement). Monthly automated rebuild via Cloud Scheduler + Cloud Build.

**Scope:** SEND IT. Phase 0 → 1 → 2, as much as possible.

### Technical Calls (GA decisions)

| Decision | Call | Reasoning |
|----------|------|-----------|
| Timezone | America/Chicago | RPI is in Iowa. Just RIIMO tonight. |
| Default permissions | Empty = USER (minimal) | Security. Current empty=OWNER is dangerous. |
| Fake metrics | Replace with honest "not_implemented" | No more lies. |
| Pipeline priority | DATA_MAINTENANCE → SECURITY → ONBOARDING | Data quality first. |

---

## Execution Plan

### Phase 0: Cleanup (v1.9.0)

| # | Task | File(s) | Details |
|---|------|---------|---------|
| 0.8 | Remove deprecated migration code | `RIIMO_MATRIX_Setup.gs` | Delete dead migration functions (~310 lines) |
| 0.9 | Remove duplicate `getMATRIX()` | `RIIMO_MATRIX_Setup.gs` | Keep only `RIIMO_Core.gs` version |
| 0.10 | Replace 9 fake metric functions | `RIIMO_Pipelines.gs`, `RIIMO_Dashboard.gs` | Return honest `{ status: 'not_implemented' }` |
| 0.11 | Fix event.currentTarget bug | `Index.html` | Capture button reference BEFORE `await showConfirmation()` |
| 0.12 | Add .modal-overlay CSS | `Index.html` | Backdrop + centering for confirmation modals |
| 0.13 | Fix default permissions | `RIIMO_Core.gs` | Empty _USER_HIERARCHY → USER level (not OWNER) |

**Deploy:** v1.9.0 → clasp push/version/deploy → verify → git commit/push

### Phase 1: Foundation (v2.0.0)

| # | Task | File(s) | Details |
|---|------|---------|---------|
| 1.2 | Real MATRIX health checks | `RIIMO_Dashboard.gs` | Actually try opening each spreadsheet, return real status |
| 1.3 | Remove hardcoded MATRIX_IDS | `RIIMO_MATRIX_Setup.gs`, `RIIMO_Core.gs` | Use `RAPID_CORE.getMATRIX_IDS()` with Script Properties fallback |
| 1.5 | Build showToast() | `Index.html` | Toast notification component: success/error/info/warning, auto-dismiss |
| 1.6 | Module pages with real links | `Index.html`, `RIIMO_Core.gs` | Each module links to actual GAS web app + shows deploy info |
| 1.7 | Error feed dashboard card | `RIIMO_Dashboard.gs`, `Index.html` | Read _ERROR_LOG, show last 24h grouped by source + severity |
| 1.9 | Seed _USER_HIERARCHY | `RIIMO_OrgAdmin.gs` (SETUP_ function) | 6 users per JDM's assignments above |
| 1.4 | Dynamic sidebar | `Index.html` | Render from user permissions + tool suites, not static HTML |

**Deploy:** v2.0.0 → clasp push/version/deploy → verify → git commit/push

### Phase 2: Visibility Dashboards (v2.1.0)

| # | Task | Data Source | Card Shows |
|---|------|------------|------------|
| 2.1 | System Health Panel | MATRIX connectivity + _ERROR_LOG rate | Green/yellow/red per dependency, error rate trend |
| 2.2 | Data Pipeline Card | RAPID_MATRIX _INTAKE_QUEUE | Queue depth by status, oldest pending age |
| 2.3 | Data Quality Card | Reconciliation stats | Dupe count, orphan count, last reconciliation |
| 2.7 | Error Feed (enhanced) | _ERROR_LOG | Last 24h errors, severity chart, source breakdown |
| 2.4 | Commission/Revenue Card | RAPID_MATRIX comp grids | Pipeline value, FYC/REN counts |
| 2.5 | B2B Pipeline Card | SENTINEL_MATRIX Opportunities | Deal count, stage distribution, pipeline value |
| 2.6 | B2C Client Health Card | PRODASH_MATRIX _CLIENT_MASTER + accounts | Client count, account totals, basic stats |

All cards read directly from MATRIX sheets (RIIMO already connects to all 3).

**Deploy:** v2.1.0 → clasp push/version/deploy → verify → git commit/push

---

## Key Files to Modify

| File | Changes |
|------|---------|
| `RIIMO_MATRIX_Setup.gs` | Remove dead code, remove duplicate getMATRIX(), remove hardcoded IDs |
| `RIIMO_Core.gs` | Fix default permissions, remove hardcoded IDs, add web app URLs to modules |
| `RIIMO_Dashboard.gs` | Replace fake metrics with real MATRIX reads, add all dashboard cards |
| `RIIMO_Pipelines.gs` | Replace fake execute functions with honest returns |
| `RIIMO_OrgAdmin.gs` | Add SETUP_SeedUserHierarchy() function |
| `Index.html` | Fix event bug, add modal CSS, add toast, dynamic sidebar, dashboard card rendering |
| `Code.gs` | Add ui* wrappers for new dashboard data endpoints |
| `CLAUDE.md` | Update version after each deploy |

## Verification

After each deploy:
1. Load RIIMO web app → dashboard loads without errors
2. MATRIX indicators show real green/red (not hardcoded)
3. Error feed shows real _ERROR_LOG entries (or "No errors" if clean)
4. JDM sees all modules (OWNER), other users see only their assigned suites
5. Toast notifications fire on actions
6. Module pages link to actual GAS web apps
7. No fake "99.9% uptime" or "3 backups verified" anywhere

---

### Healthcare-mcps Cloud Run Deployment

**Prerequisites (all confirmed):**
- gcloud CLI: ✅ installed, authenticated as Josh@retireprotected.com
- GCP project: ✅ my-project-rpi-mdj-platform (90741179392)
- Cloud Run API: ✅ enabled
- Cloud Build API: ✅ enabled
- Artifact Registry API: ✅ enabled

**Steps:**
1. Create `Dockerfile` in healthcare-mcps/ — Node.js image, copy CMS data setup script, install deps
2. Create `cloudbuild.yaml` — build + deploy pipeline
3. Run `npm run setup:cms` locally first to download CMS data (~2.7GB)
4. Build container with `gcloud builds submit` (remote build, no local Docker needed)
5. Deploy to Cloud Run: `gcloud run deploy que-api --region us-central1 --memory 4Gi --min-instances 1`
6. Get the Cloud Run URL (e.g., `https://que-api-XXXXX-uc.a.run.app`)
7. Update QUE-Medicare Script Property `QUE_API_URL` to Cloud Run URL
8. Update PRODASH `HEALTHCARE_MCPS_BASE_URL_` constant to Cloud Run URL
9. Set up Cloud Scheduler for monthly CMS data refresh + container rebuild

**gcloud path:** `/opt/homebrew/bin/gcloud`

**Deploy after RIIMO Phase 2** — this is independent work that doesn't block RIIMO.

---

## Future Sessions

| Session | Work |
|---------|------|
| RAPID_API access model | Add API key to sensitive endpoints. Separate from RIIMO. |
| RAPID_CORE secrets | Move plaintext keys to Script Properties, rotate. |
| Phase 3 (Control) | Operations console, reconciliation queue UI, real pipeline execution. |
| Phase 4 (Intelligence) | TDM scoring, cross-platform analytics. |
