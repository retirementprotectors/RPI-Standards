# toMachina EPIC Roadmap — The Machine

> Single source of truth for everything built, in progress, and planned.
> Consolidates 14 prior plans into one master document.
> Updated: 2026-03-13

---

## How to Read This

- **BUILT** = shipped to production, live at tomachina.com
- **MOCKUP** = UI built with mock data, needs API wiring
- **PLANNED** = scoped and understood, not started
- **BLOCKED** = waiting on external action (JDM, vendor, API key)

---

## Platform Status

| Sprint | Status | What Shipped |
|--------|--------|-------------|
| 1 | COMPLETE | 26,889 Firestore docs normalized + FK-validated |
| 2 | COMPLETE | 8 shared components, 24 portal pages |
| 3 | COMPLETE | CLIENT360, RMD, Beni, Medicare quoting, DAVID HUB |
| 4 | COMPLETE | COMMS, FLOW, C3, ATLAS, CAM backends → Cloud Run |
| 5 | COMPLETE | Cloud Run live, approval engine, intake functions, 6 GAS archived |
| 6 | COMPLETE | 6 parallel builders, 34 API routes, 9 shared UI modules |
| 7a | COMPLETE | Pipeline Factory — 13 pipelines, Kanban, dynamic sidebar |
| 7b | COMPLETE | Pipeline Studio — full builder app, admin CRUD, 16K lines |
| 8+8p | COMPLETE | COMMS Center, Access Center, DeDup, 47-item polish, 3 polish builders |
| 9 | IN PROGRESS | 23 bug fixes (~16 shipped), Communications + RPI Connect mockups |

**Production**: prodash.tomachina.com, riimo.tomachina.com, sentinel.tomachina.com — ALL LIVE
**CI**: 13/13 type-check, Firebase App Hosting auto-deploying

---

## PORTALS

### ProDashX (B2C — prodash.tomachina.com)

| Feature | Status | Notes |
|---------|--------|-------|
| Contacts grid (/contacts) | BUILT | Renamed from /clients. Filters, checkboxes, DeDup |
| Accounts grid | BUILT | 3-row header, pills, accurate counts, DeDup |
| CLIENT360 | BUILT | 8 tabs: Comms, Connect, Personal, Estate, Accounts, Connected, Access, Activity |
| Quick Intake | BUILT | Basic form. Custom fields + screenshot paste PLANNED |
| Service Centers (RMD, Beni, Access) | BUILT | Access Center needs redesign (Sprint 9 scope) |
| Sales Centers (Medicare, Life, Annuity, Advisory) | BUILT | QUE modules surfaced as ProDash views |
| Medicare Quoting (CSG API) | BUILT | 4 API endpoints, QuickQuote cached |
| MyRPI | BUILT | Employee profiles, org nav, Google photos |
| Admin | BUILT | Team Config (3-level: Type→User→Entitlements) |
| DeDup Comparison | BUILT | Opens, needs data fix (FIX-4) + merge handling (FIX-21) |
| Pipeline Factory | BUILT | 13 pipelines in sidebar, Kanban boards |
| Pipeline Studio | BUILT | Full builder app (teal brand) |
| Communications Module | MOCKUP | Slide-out: feed + compose + dialer + inbound call |
| RPI Connect | MOCKUP | Slide-out: Channels + People + Meet |
| Smart Search (TopBar) | PLANNED | Type-ahead across clients + accounts |
| AI3 Report (PDF) | PLANNED | Generate + download + save to ACF |
| Activity Audit Trail | PLANNED | Middleware auto-logging all mutations |
| Access Center Redesign | PLANNED | Carrier/product type, auth tracking, dynamic |
| MyDropZone + Intake FAB | PLANNED | Rapid intake floating action button |

### RIIMO (B2E — riimo.tomachina.com)

| Feature | Status | Notes |
|---------|--------|-------|
| Dashboard | BUILT | System health, pipeline, data quality views |
| MyRPI | BUILT | Shared module, same as ProDash |
| Admin/Org Admin | BUILT | User hierarchy, module permissions |
| Leadership Center | BUILT | Meeting extractions + team roadmaps (RIIMO exclusive) |
| Pipeline Factory | BUILT | Same shared module |
| Control Phase (triggers, reconciliation, onboarding) | PLANNED | Phase 3 of RIIMO roadmap |
| Intelligence Phase (KPIs, revenue analytics, scoring) | PLANNED | Phase 4 of RIIMO roadmap |
| Team Availability Dashboard | PLANNED | Calendar free/busy, presence |
| Unit-based Auto-assignment | PLANNED | Leader defaults for routing |

### SENTINEL (B2B — sentinel.tomachina.com)

| Feature | Status | Notes |
|---------|--------|-------|
| Navigation + Auth | BUILT | Basic scaffold |
| Deal Management | BUILT | Stub only |
| DAVID HUB (M&A workflows) | PLANNED | Valuation, agent search, market intelligence |
| Deal Pipeline | PLANNED | Stage tracking, M&A pipeline |
| Acquisition Tooling | PLANNED | Book migration, OS distribution |

**SENTINEL priority driven by first M&A opportunity (Sprenger ~April 2026)**

---

## APPS (Own Brand, Cross-Portal)

### ATLAS — Data Intelligence
| Item | Status |
|------|--------|
| Source Registry (54 sources, RED/YELLOW/GREEN scoring) | BUILT |
| Tool Registry (~150 data tools categorized) | PLANNED |
| Automation Dashboard (launchd + GAS trigger health) | PLANNED |
| Pipeline Map (horizontal flow diagram) | PLANNED |
| Wire Diagram (source-to-UI paths per product line) | PLANNED |

### CAM — Compensation Management
| Item | Status |
|------|--------|
| Comp grids per channel + carrier + rates | BUILT (data) |
| Commission scoring in RIIMO | BUILT |
| Full CAM UI (grid editor, reconciliation, onboarding) | PLANNED |

### DEX — Documents + Forms
| Item | Status |
|------|--------|
| 300+ field mappings, PDF templates, intake pipeline | BUILT (GAS) |
| React rebuild OR GAS wrapper | PLANNED (keep GAS — DriveApp too complex for React) |

### C3 — Campaign Engine
| Item | Status |
|------|--------|
| 60 campaigns, 661 templates, send orchestration | BUILT (backend) |
| Campaign builder UI | PLANNED |
| Template editor + content blocks | PLANNED |
| AEP blackout enforcement (Oct-Dec) | PLANNED |

### Command Center — Accountability Hub
| Item | Status |
|------|--------|
| 7 document types with CRUD | BUILT |
| Meeting transcript processing (Claude extraction) | BUILT |
| Action Item Tracker | PLANNED |
| Auto-route meetings → roadmaps | PLANNED |
| Google Meet auto-detect + recording watcher | PLANNED |
| Weekly scorecard (John Behn defining metrics) | PLANNED |

### Pipeline Studio — Pipeline Builder (Teal Brand)
| Item | Status |
|------|--------|
| Full-screen pipeline editor | BUILT |
| Admin CRUD API (23 endpoints) | BUILT |
| Dynamic sidebar wiring | BUILT |
| 13 pipeline configs seeded | BUILT |
| Steps/tasks API (400 errors) | BUG — needs fix |

---

## MODULES (Portal-Branded, Cross-Portal)

### Communications Module
| Item | Status |
|------|--------|
| Slide-out panel (feed + compose + dialer) | MOCKUP |
| CommsFeed (20 entries, filters, search, expand) | MOCKUP |
| CommsCompose (SMS/Email/Call modes, templates) | MOCKUP |
| InboundCallCard (TopBar notification) | MOCKUP |
| Twilio 888 wiring (live calls/SMS) | PLANNED — needs env vars on Cloud Run |
| Firestore comms collection for real feed | PLANNED |
| Sidebar collapse UX (real estate fix) | PLANNED |

### RPI Connect
| Item | Status |
|------|--------|
| Slide-out panel (Channels + People + Meet) | MOCKUP |
| Channels tab (pinned/all, unread, previews) | MOCKUP |
| People tab (presence, profile photos, Chat/Meet/Call) | MOCKUP |
| Meet tab (instant, schedule, recordings) | MOCKUP |
| Google Chat API wiring | PLANNED |
| Google Calendar API wiring | PLANNED |
| Inline conversation (no new windows) | PLANNED |
| Sidebar collapse UX | PLANNED |

### Admin
| Item | Status |
|------|--------|
| Team Config (Owner/Executive/Leader/User grouping) | BUILT |
| Module permission assignment | BUILT |
| Audit trail viewer | PLANNED |

### MyRPI
| Item | Status |
|------|--------|
| Employee profiles, org navigation | BUILT |
| Google profile photos | BUILT |
| MyDropZone (Meet link, intake folder, booking) | BUILT (empty — needs data population) |
| Downline navigation | BUILT |

---

## TOOLS (Backend, No Direct UI)

### Cloud Run API (services/api/)
| Item | Status |
|------|--------|
| 38+ route files, Express/TypeScript | BUILT |
| Firebase Auth middleware | BUILT |
| Flow admin CRUD (23 endpoints) | BUILT |
| RAPID_IMPORT URL swap | PLANNED — needs end-to-end testing |

### Bridge Service (services/bridge/)
| Item | Status |
|------|--------|
| Dual-write Firestore + Sheets (toggleable) | BUILT |
| Cloud Run deployment | PLANNED |

### Intake (services/intake/)
| Item | Status |
|------|--------|
| 4 Cloud Functions for intake channels | BUILT |

### BigQuery Stream
| Item | Status |
|------|--------|
| 2 Cloud Functions (top-level + subcollection) | BUILT |

### RAPID_CORE (GAS Library)
| Item | Status |
|------|--------|
| Normalizers, dedup, quality gates, MATRIX routing | BUILT |
| 17K lines, core dependency for all GAS | BUILT |
| No deprecation plan — stays indefinitely | STABLE |

### RAPID_IMPORT (GAS Data Ingestion)
| Item | Status |
|------|--------|
| Medicare import (4,638 records) | BUILT |
| Life/Annuity/BD-RIA import | PLANNED (Phase 3b) |
| Signal revenue import | PLANNED (Phase 3b) |
| Commission PDF intake | PLANNED (Phase 3b) |
| Carrier XLSX import | PLANNED (Phase 3b) |
| Integration framework (DTCC, Schwab, Gradient, Blue Button) | BLOCKED — JDM vendor enrollments |

### PDF_SERVICE
| Item | Status |
|------|--------|
| Fill + merge templates | BUILT |
| AI3 report generation | PLANNED |

### MCP-Hub
| Item | Status |
|------|--------|
| rpi-workspace, rpi-business, rpi-healthcare | CONFIGURED (3 failing to connect — investigate) |
| rpi-comms | BUILT |
| gdrive, google-calendar, gmail, slack | BUILT |

---

## DATA OPS

| Phase | Status | What |
|-------|--------|------|
| Data Foundation Phase 1 (secure data) | COMPLETE | 58 folders, 153 files organized |
| Data Foundation Phase 2 (RAPID_CORE knowledge) | COMPLETE | Carrier/product masters seeded |
| Phase 3a (PRODASHX MATRIX audit) | COMPLETE | 18,415 records audited |
| Phase 3b Medicare | COMPLETE | 4,638 records imported |
| Phase 3b Life/Annuity/BDRIA | PLANNED | Next priority — biggest data gaps |
| Phase 3d Commission mapping | PLANNED | Revenue tracking for ATLAS |
| Phase 4 Enrichment (WhitePages, NeverBounce, USPS) | PLANNED | After Phase 3b |
| FK Migration | COMPLETE | 4,649 clients normalized, 270 dupes merged |
| Quality Phases A-E | COMPLETE | Normalizers, quality gates, health checks |

---

## BLOCKERS

| Blocker | Unblocked By | Priority |
|---------|-------------|----------|
| COMMS env vars on Cloud Run | JDM deploys Twilio/SendGrid keys | P0 |
| A2P 10DLC local number | Campaign approval (resubmitted 3/12) | P1 |
| Phase 3b data imports | GAS connectivity verified (done) | P1 |
| DTCC/Schwab/Gradient/Blue Button integrations | JDM vendor enrollments | P3 |
| CoF policy enrichment | JDM provides dataset | P3 |
| ~~Pipeline Studio 400 errors~~ | ~~Fix steps/tasks API routes~~ | ~~FIXED 2026-03-14~~ |
| Slide-out panel real estate | UX decision (sidebar collapse?) | P2 |

---

## DECISIONS NEEDED (JDM)

6 open decisions blocking Sprint 10+ scope:

| # | Decision | Context | Impacts |
|---|----------|---------|---------|
| 1 | **Enrichment strategy** — WhitePages/USPS: where does address/phone enrichment live? | Client records have gaps (no address, incomplete phone). Need a data enrichment source and where it runs (Cloud Function? Import pipeline? On-demand per client?) | Sprint 10 (Smart Search accuracy), Sprint 12 (Data Ops) |
| 2 | **New Contact UX** — What does "add a new contact" look like? | No "New Contact" form exists yet. Is it a modal? Full page? Wizard? What required fields? Does it trigger duplicate detection before saving? | Sprint 10 (ProDashX features) |
| 3 | **Client-level docs** — Where do per-client documents live (2-4 near AI3/ACF)? | AI3 generates a PDF. ACF is the client folder in Drive. Are there 2-4 additional document types that need buttons on Client360? What are they? | Sprint 10 (AI3 Report), Sprint 14 (DEX) |
| 4 | **Bulk connection creation** — What's the interface for mass-linking connected contacts? | Connected tab has manual search+link. For bulk (e.g., importing spouse/beneficiary data from a spreadsheet), what's the UX? Upload CSV? Paste from clipboard? Auto-detect from account beneficiaries? | Sprint 10 (ProDashX), Sprint 12 (Data Ops) |
| 5 | **Incoming call ring mechanism** — How does the dialer ring when a call comes in? | InboundCallCard mockup exists in TopBar. But: does the browser tab flash? Audio alert? Push notification? What's the ring order if multiple agents are assigned? Who picks up first? | Sprint 13 (Module Firming — Communications) |
| 6 | **DeDup merge impact on associated records** — What happens to accounts, access, connected contacts, and communications when a record is merged? | Asked multiple times. When Record B merges into Record A: do B's accounts move to A? Do B's connected contacts re-link? Do B's comms history merge? Or just the client-level fields? | Sprint 10 (DeDup completion) |

---

## GO-FORWARD SPRINTS

### Sprint 10: ProDashX Features + PDF_SERVICE + Blockers
- **ProDashX remaining features**: Smart Search (TopBar type-ahead), Access Center Redesign, MyDropZone + Intake FAB, Activity Audit Trail
- **AI3 Report**: PDF generation via PDF_SERVICE → download + save to ACF in Drive
- **Clear ALL blockers**: COMMS env vars on Cloud Run, slide-out real estate (sidebar collapse), A2P 10DLC campaign follow-up
- **Resolve 6 DECISIONS** (see above) — these gate multiple sprint items
- Deploy COMMS env vars (Twilio/SendGrid keys) to Cloud Run

### Sprint 11: RIIMO — Platform Permissions Cascade Firming
- Entitlements cascade: Owner → Executive → Leader → User permission inheritance
- Module permission assignment validation (RIIMO controls what shows in all portals)
- Unit-based auto-assignment (leader defaults for routing)
- Control Phase: triggers, reconciliation queue, onboarding/offboarding tracking
- Pipeline permission governance (Leaders build, Users propose)

### Sprint 12: Data Ops Depth (RAPID_IMPORT + Cloud Run API)
- Phase 3b imports: Life, Annuity, BD/RIA, commissions (biggest data gaps)
- Signal revenue import + commission PDF intake
- Carrier XLSX import + client demographic backfill
- RAPID_IMPORT URL swap to Cloud Run (end-to-end testing)
- Bridge service deployment (dual-write Firestore + Sheets)
- Phase 3d commission stream mapping (revenue tracking for ATLAS)

### Sprint 13: Module Firming (Communications + RPI Connect + Admin + MyRPI)
- Wire Communications Module to Twilio 888 (live calls/SMS/email)
- Wire RPI Connect to Google Chat + Calendar + People APIs
- Solve slide-out UX (sidebar collapse, inline conversations, no new windows)
- Admin: audit trail viewer, full permission CRUD
- MyRPI: MyDropZone data population, setup wizard, downline depth
- All 4 modules production-grade across all 3 portals

### Sprint 14: Apps Firming (C3 + ATLAS + CAM + DEX + Command Center)
- C3: Campaign builder UI, template editor, content block system, AEP blackout
- ATLAS v1.3: Tool Registry, Automation Dashboard, Pipeline Map, Wire Diagrams
- CAM: Full UI rebuild (grid editor, reconciliation, agent onboarding)
- DEX: Form library depth, React wrapper or GAS preservation decision
- Command Center: Action Item Tracker, auto-route meetings → roadmaps, weekly scorecard

### Sprint 15: RIIMO Depth
- Intelligence Phase: KPI dashboards, revenue analytics, TDM scoring
- Team Availability Dashboard (calendar free/busy, presence)
- Leadership Center depth (meeting extractions → action items → roadmaps)
- EP onboarding workflow
- Job Description Module

### Sprint 16: SENTINEL — DAVID M&A Platform
- DAVID HUB rebuild (M&A workflows, valuation calculators, agent search)
- Deal pipeline (stage tracking, market intelligence)
- Acquisition tooling (book migration framework)
- Operating System distribution to acquired practices
- Carrier + advisor intelligence views

---

## Source Plans (Consolidated Into This Document)

These 14 plans were consolidated on 2026-03-13. Originals archived in `_ARCHIVED/`:

1. prodashx-platform-roadmap.md → PORTALS > ProDashX
2. riimo-platform-roadmap.md → PORTALS > RIIMO
3. rapid-import-platform-roadmap.md → TOOLS > RAPID_IMPORT
4. rpi-standards-governance-roadmap.md → INFRASTRUCTURE
5. adaptive-sauteeing-bird.md → APPS > Command Center
6. atomic-puzzling-canyon.md → MODULES > Communications
7. drifting-snuggling-crystal.md → DATA OPS
8. phase-3b-life-annuity-bdria-agent-brief.md → DATA OPS
9. polymorphic-twirling-hopper.md → APPS > ATLAS
10. sharded-stargazing-kite.md → DATA OPS
11. snoopy-wobbling-sifakis.md → MODULES > RPI Connect
12. sunny-jingling-deer.md → TOOLS > Flow Engine
13. tomachina-next-phases.md → GO-FORWARD SPRINTS
14. velvety-chasing-wand.md → Sprint 9 (active)
