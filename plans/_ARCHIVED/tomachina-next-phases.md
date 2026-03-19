ARCHIVED: Consolidated into tomachina-epic-roadmap.md on 2026-03-13
# toMachina — Post-Launch Framework

> All 5 migration phases are COMPLETE. This document frames what comes next.
> Created: 2026-03-11 (Auditor session with JDM)

---

## Where We Are

Three portals live. 51 pages. 41 API endpoints. 29K Firestore docs. Auto-deploy. Bridge operational. GAS thinned. Immune system online. CLAUDE.md updated. Hookify pruned.

**But the portals are scaffolds, not finished products.** The structure is right. The data flows. The architecture is proven. What's missing is the **depth** — the rich UI/UX from the GAS era hasn't been rebuilt yet.

---

## The Four Domains

Everything falls into one of four domains. Each has its own timeline, its own builders, and its own priority.

### Domain 1: Portal UI/UX (User-Facing — Highest Priority)

**The problem:** The archived GAS portals had years of UI work. toMachina has functional pages with real data but basic layouts. The team can't use these until they look and feel like real tools.

**The approach:** Two tiers.

#### Tier A: Shared Module Components
Build once in `packages/ui/src/modules/`, deploy to all 3 portals automatically. These are features that look the same everywhere:

| Component | What It Replaces | Reference Code | Complexity |
|-----------|-----------------|---------------|------------|
| `CamDashboard.tsx` | CAM Index.html (2K) + Scripts.html (2.8K) | `archive/CAM/` | HIGH — comp grids, projections, pipeline tracking, revenue breakdown |
| `C3Manager.tsx` | C3 Index.html (10K!) | `archive/C3/` | HIGH — campaign builder, template editor, content blocks, send orchestration |
| `DexDocCenter.tsx` | DEX Index.html (744) + Scripts.html (3K) | `archive/DEX/` | MEDIUM — form library, kit builder, PDF preview, document pipeline |
| `AtlasRegistry.tsx` | ATLAS Index.html + views (2K) | `archive/ATLAS/` | MEDIUM — source registry, tool registry, wire diagrams, pipeline flow |
| `CommandCenter.tsx` | CEO-Dashboard + RPI-Command-Center | `archive/CEO-Dashboard/`, `archive/RPI-Command-Center/` | MEDIUM — leadership metrics, team performance, pipeline health |
| `MyRpiProfile.tsx` | RIIMO MyRPI.html (3.4K) | `archive/RIIMO/MyRPI.html` | MEDIUM — employee profile, meet room/drop zone, team profiles |
| `ConnectPanel.tsx` | RPI_Connect.html (56K across 3 portals) | `archive/PRODASHX/RPI_Connect.html` | HIGH — messaging hub, Twilio/SendGrid/Chat integration |
| `AdminPanel.tsx` | Various admin pages | All 3 archive portals | LOW — user management, org structure (already mostly built) |

**Each portal page becomes 3 lines:**
```tsx
import { CamDashboard } from '@tomachina/ui'
export default function CamPage() {
  return <CamDashboard portal="prodashx" />
}
```

#### Tier B: Portal-Specific Pages
These are unique to each portal and stay as separate page files:

**ProDashX (B2C):**
| Page | Reference | What's Missing |
|------|-----------|---------------|
| CLIENT360 | `archive/PRODASHX/PRODASH_CLIENT360.gs` (1.7K) + Scripts.html (15K) | Full tab depth — current tabs show data but not the rich layouts from GAS |
| RMD Center | `archive/PRODASHX/PRODASH_RMD_CENTER.gs` (381) | IRS RMD calculation logic, distribution tracking |
| Beni Center | `archive/PRODASHX/PRODASH_BENI_CENTER.gs` (219) | Beneficiary management workflow |
| Discovery Kit | `archive/PRODASHX/PRODASH_DISCOVERY_KIT.gs` (1.2K) + `DISCOVERY_PDF.gs` (734) | Client discovery questionnaire + PDF generation |
| Medicare Quoting | `archive/PRODASHX/PRODASH_QUE_MEDICARE.gs` (421) | CSG API integration, plan comparison, recommendation engine |
| Quick Intake | `archive/PRODASHX/PRODASH_QuickIntake.gs` (524) | One-screen client creation form |

**RIIMO (B2E):**
| Page | Reference | What's Missing |
|------|-----------|---------------|
| Dashboard | `archive/RIIMO/RIIMO_Dashboard.gs` (1.3K) + DashboardWidgets.html (1.6K) | Rich widget layouts, health metrics from all 3 platforms |
| Pipelines | `archive/RIIMO/RIIMO_Pipelines.gs` (1.8K) | Pipeline definitions, stage execution, onboarding/offboarding flows |
| Tasks | `archive/RIIMO/RIIMO_Tasks.gs` (748) | Task delegation, status tracking, team assignment |
| Job Templates | `archive/RIIMO/RIIMO_JobTemplates.gs` (631) + JobTemplates.html (2K) | Job description template editor |

**SENTINEL (B2B):**
| Page | Reference | What's Missing |
|------|-----------|---------------|
| Deal Management | `archive/sentinel-v2/SENTINEL_DealManagement.gs` (398) | Deal CRUD, valuation, M&A workflows |
| Market Intelligence | `archive/sentinel-v2/SENTINEL_MarketIntelligence.gs` (1.5K) | Agent search, carrier intel, cross-reference (currently basic) |
| Valuation | `archive/sentinel-v2/SENTINEL_Valuation.gs` (507) | IMO comparison, M-A-P reports, SPH projections |
| DAVID HUB Calculators | `archive/DAVID-HUB/` | MEC, PRP, SPH entry calculators (currently "Coming Soon" cards) |

---

### Domain 2: Data Integrity (Foundation — Do Before UI)

**The problem:** Firestore data was bulk-migrated from Sheets. Field names are inconsistent. FKs don't always resolve. Normalization wasn't applied during migration.

**The tasks:**

| Task | What It Does | Priority |
|------|-------------|----------|
| FK Validation Script | Check every account→client, revenue→agent, opportunity→client FK resolves | HIGH — do first |
| Normalize Firestore Data | Run `normalizeData()` from `@tomachina/core` across all collections | HIGH — fixes carrier name mismatches, phone formats, date formats |
| Field Name Audit | Compare Firestore field names against TAB_SCHEMAS for each collection — find mismatches | MEDIUM |
| Tool Registry Migration | Migrate `_TOOL_REGISTRY` from Sheets to Firestore `tool_registry` collection | MEDIUM — ATLAS UI needs this |
| Activity Log Schema Fix | `_ACTIVITY_LOG` uses `entity_id` (generic), not `client_id`. Need to index or map for per-client views | MEDIUM |
| Missing Data Migration | Any Sheets tabs not yet in Firestore (check TABLE_ROUTING vs Firestore collections) | LOW |

---

### Domain 3: GAS Engine Transition (Background — No Rush)

**The problem:** 8 GAS engines still run. They work. But they're a maintenance burden and they limit what toMachina can do (6-min execution limit, no real-time processing, Sheets as bottleneck).

**The disposition (ranked by ease of migration):**

| Engine | Lines | Move To | Effort | Business Trigger |
|--------|-------|---------|--------|-----------------|
| **RAPID_COMMS** | 1K | `packages/comms/` or Cloud Function | EASY | When campaigns need real-time send from toMachina (not GAS-triggered) |
| **RAPID_FLOW** | 2K | `packages/core/flow/` | EASY | When pipeline management needs sub-second response (Kanban drag-and-drop) |
| **ATLAS** | 5K | Fully toMachina (already has Firestore + UI) | LOW | When Tool Registry migrates and GAS triggers become Cloud Scheduler |
| **C3 backend** | 13K | `services/api/routes/campaigns.ts` expansion | MEDIUM | When campaign builder UI is rebuilt in toMachina |
| **CAM backend** | 8K | Keep GAS long-term (Sheets comp grids are deeply integrated) | MEDIUM | When comp grids move to Firestore |
| **RAPID_CORE** | 17K | Dies naturally | ZERO | When all GAS consumers are gone |
| **DEX backend** | 8K | Keep GAS longest (DriveApp + PDF blobs) | HIGH | When PDF_SERVICE replaces all GAS PDF operations |
| **RAPID_IMPORT** | 106K | Keep GAS indefinitely or major rewrite | MASSIVE | Only if GAS triggers become unreliable or Google deprecates Apps Script |

**Decision framework:** Don't move an engine unless:
1. A user-facing feature needs something the engine can't provide (real-time, sub-second, etc.)
2. The engine breaks and the fix cost exceeds the port cost
3. Google deprecates something the engine depends on

---

### Domain 4: Infrastructure + Operations (Ongoing)

**The problem:** Some plumbing is incomplete or needs ongoing maintenance.

| Task | What It Does | Priority |
|------|-------------|----------|
| RAPID_IMPORT URL swap | Point callRapidAPI_() to Cloud Run API (documented, not applied) | MEDIUM — needs end-to-end testing |
| MCP callCloudRunAPI() | Add Cloud Run routing to MCP-Hub (documented, not applied) | MEDIUM — needs MCP restart |
| BigQuery Export Extension | Install Firestore → BigQuery stream (script ready) | LOW — needs interactive Firebase install |
| Cloud Run API deploy | Deploy `services/api/` to Cloud Run with all 23 route files | MEDIUM — needed before RAPID_IMPORT URL swap |
| Cloud Run Bridge deploy | Deploy `services/bridge/` to Cloud Run | MEDIUM — needed for production dual-write |
| Custom domains (RIIMO/SENTINEL) | Wire `fah-claim` TXT records for App Hosting | LOW — Builder 3 may be doing this now |
| Compliance scanner tuning | Add TypeScript-specific patterns (no `any` types, auth middleware) | LOW |
| MONITORING.md + POSTURE.md update | Reflect new project structure | LOW |

---

## Recommended Execution Order

### Sprint 1: Data + Shared Modules (Next Session)
**Goal:** Clean data + build the 8 shared module components

| Builder | Scope | Est. |
|---------|-------|------|
| Builder 1 | Data integrity: FK validation + normalize Firestore + field audit | 3-4 hrs |
| Builder 2 | Shared modules: CamDashboard + C3Manager + CommandCenter + AdminPanel | 3-4 hrs |
| Builder 3 | Shared modules: DexDocCenter + AtlasRegistry + MyRpiProfile + ConnectPanel | 3-4 hrs |

**Output:** 8 shared module components in `packages/ui/src/modules/`, all portal pages converted to 3-line imports, data validated and normalized.

### Sprint 2: Portal-Specific Depth (Following Session)
**Goal:** Rebuild the rich UX from the GAS era in React

| Builder | Scope | Est. |
|---------|-------|------|
| Builder 1 | ProDashX depth: CLIENT360 rich tabs, RMD Center, Beni Center, Quick Intake | 4-5 hrs |
| Builder 2 | ProDashX depth: Discovery Kit, Medicare Quoting (CSG API), Sales Centers | 4-5 hrs |
| Builder 3 | RIIMO + SENTINEL depth: Dashboard widgets, Pipelines, Deals, Valuation, DAVID HUB calcs | 4-5 hrs |

**Output:** Portals that look and feel like finished products. Team-ready.

### Sprint 3: Infrastructure Cutover (When Ready)
**Goal:** Cut the cord on GAS as the primary API path

| Task | Builder |
|------|---------|
| Deploy API + Bridge to Cloud Run | Builder 2 |
| RAPID_IMPORT URL swap + end-to-end testing | Builder 2 |
| MCP callCloudRunAPI() activation | Builder 2 |
| BigQuery export extension install | JDM (interactive) |
| Remaining GAS engine ports (RAPID_COMMS, RAPID_FLOW) | Builder 3 |

### Sprint 4+: Ongoing
- Feature development driven by business needs
- GAS engine migration as needed (not proactive)
- DAVID M&A onboarding (Operating System as skill pack)
- MyDropZone rebuild in toMachina
- Campaign engine (C3) full rebuild

---

## Decision Points for JDM

| Decision | When | Options |
|----------|------|---------|
| **Sprint 1 priority** | Before next session | Data first? Or UI first? (Recommend: data first — builders need clean data to build good UI) |
| **Team rollout timeline** | Business decision | When do Vince/Nikki/Matt start using toMachina? That drives UI polish urgency. |
| **RAPID_IMPORT cutover** | When API is deployed + tested | Approve the URL swap from GAS Web App to Cloud Run |
| **GAS engine migration** | Only when needed | Don't proactively move engines that work. Move them when business needs demand it. |
| **CSG API integration** | When Medicare quoting is priority | Wire CSG into the Medicare Sales Center — this is new revenue capability |
| **DAVID M&A onboarding** | First acquisition target | Package Operating System for distribution |

---

## Reference Map

When building UI for any module, read the archive first:

```
~/Projects/archive/
├── PRODASHX/          → ProDashX reference (32 .gs, 5 .html, 46K lines)
│   ├── Scripts.html   → 15K lines of client-side JS (THE reference for React components)
│   ├── Styles.html    → 4K lines of CSS (reference for Tailwind conversion)
│   └── PRODASH_*.gs   → Backend logic per module
├── RIIMO/             → RIIMO reference (16 .gs, 7 .html, 28K lines)
│   ├── Index.html     → 5.8K main UI
│   └── RIIMO_*.gs     → Backend logic per module
├── sentinel-v2/       → SENTINEL reference (17 .gs, 4 .html, 14K lines)
│   ├── Index.html     → 6K main UI
│   └── SENTINEL_*.gs  → Backend logic per module
├── DAVID-HUB/         → Calculator reference
├── CEO-Dashboard/     → Executive dashboard reference
└── RPI-Command-Center/→ Leadership visibility reference
```

**Rule for builders:** Before building any toMachina page, `cat` the corresponding archive file. Understand what existed before. Then build the modern version.
