# Plan: RIIMO Dashboard/Intelligence Restructure

## Context

JDM's feedback: **Dashboard = "What's the progress on shit?"** — not metrics, not health checks, not "how many X's do we have." The Dashboard is currently stuffed with Intelligence content (B2C/B2B metrics, System Health, Quick Actions diagnostics, Platform Overview). All of that belongs in the Intelligence section. Dashboard should be lean: progress, tasks, tools.

---

## What Moves WHERE

### STAYS on Dashboard (progress + action)
| Widget | Why |
|--------|-----|
| Command Bar | "Things needing my attention right now" |
| Pipeline Snapshot | Progress through onboarding/offboarding stages |
| My Tasks | My assigned work items |
| Module Launcher | Tool navigation |

### MOVES to Intelligence (metrics + health + diagnostics)
| Widget | Currently | Moving To |
|--------|-----------|-----------|
| System Health (platform connectivity) | Dashboard Row 3, Col 2 | Intelligence — top |
| Quick Actions (error report, deploy health, queue status, GHL sync, data quality scan) | Dashboard Row 4, Col 2 | Intelligence — as "Diagnostic Tools" |
| Platform Overview / B2C+B2B tabs (client counts, data quality, RMD, GHL, producers, revenue, commissions) | Dashboard Row 5 | Intelligence — as "Platform Overview" |

---

## New Dashboard Layout

```
Row 1: Command Bar (full width) — alert chips
Row 2: Pipeline Snapshot + My Tasks (2-col for LEADER+, tasks-only for USER)
Row 3: Module Launcher (full width)
```

3 rows. Clean. Fast. Dashboard drops from 5 async loaders to 3 (no more `dwLoadQuickActionsV3`, no more `dwLoadOpsIntelCards` which called the heavy `uiGetDashboardCards()`).

## New Intelligence Layout

```
1. System Health — platform connectivity status
2. Platform Overview — B2C/B2B tabbed cards (reuse renderOpsIntelTabs)
3. Diagnostic Tools — 5 quick action buttons with execute capability
4. AI Analytics — existing hero stats, MCP breakdown, machines, trends
5. Operations Intelligence — existing 4 cards
6. Integration Hub — existing 13 integrations table
```

---

## File Changes

### 1. `Code.gs` — Expand `uiGetIntelligenceData()`

Currently bundles: AI analytics + opsCards + integrationHub

**Add:**
- `data.allCards` = full `getDashboardCards()` result (feeds B2C/B2B tabs + system health)
- `data.quickActions` = `getQuickActions(userLevel)` result
- `data.userLevel` + `data.isAdmin` for role-gated rendering

Dashboard no longer calls `uiGetDashboardCards()` at all — performance win.

### 2. `DashboardWidgets.html` — Simplify `renderDashboardV3()`

**Remove from layout:**
- Row 3 Col 2: System Health card (`dw-system-health-card`)
- Row 4 Col 2: Quick Actions card (`dw-quick-actions-grid`)
- Row 5: Platform Overview (`dw-ops-intel-container`, `isExecPlus` block)

**Remove async loader calls:**
- `dwLoadQuickActionsV3()`
- `dwLoadOpsIntelCards()`

**Restructure layout:**
- Row 2 becomes: Pipeline Snapshot (left) + My Tasks (right) for LEADER+, or just My Tasks (full) for USER
- Row 3 becomes: Module Launcher (full width)

**Keep these functions** (still used by Intelligence via `<?!= include('DashboardWidgets') ?>`):
- `renderOpsIntelTabs()`, `dwSwitchIntelTab()`, `dwRenderIntelB2C()`, `dwRenderIntelB2B()`
- `dwRenderMatrixHealth()`
- `dwEscape()`

### 3. `Index.html` — Expand `renderIntelligence()`

Add 3 new sections before existing AI Analytics:

**Section 1: System Health** — Reuse `dwRenderMatrixHealth()` from DashboardWidgets (already in scope via include)

**Section 2: Platform Overview** — Render container div, then post-render call `renderOpsIntelTabs(container, data.allCards)` to populate B2C/B2B tabs

**Section 3: Diagnostic Tools** — Render quick action buttons using `data.quickActions` array. Reuse existing `runQuickAction()` handler (already in Index.html)

Existing sections (AI Analytics, Ops Intelligence, Integration Hub) shift down but remain unchanged.

---

## No Changes Needed
- `RIIMO_Dashboard.gs` — all `_card*()` functions stay as-is, `getDashboardCards()` now called from Intelligence instead of Dashboard
- `RIIMO_Actions.gs` — `getQuickActions()` and `executeQuickAction()` stay as-is
- `RIIMO_Intelligence.gs` — `getIntelligenceData()` stays as-is

---

## Deployment

| # | What | Type |
|---|------|------|
| 1 | Edit Code.gs, DashboardWidgets.html, Index.html | Code changes |
| 2 | `clasp push` → `clasp version` → `clasp deploy` to fresh ID | GAS deploy |
| 3 | `clasp deployments` verify @version | Verification |
| 4 | `git add` → `git commit` → `git push` | Git |

**Deploy ID:** `AKfycbwxf-Wav8GRWDFGmt6iBV4-f9azAtyzzhyaEhAz1AArhZuGtoXId8rcH_cmV6yjFH7V`

---

## Verification

1. **Dashboard** — Load RIIMO → Dashboard shows only: Command Bar, Pipeline Snapshot, My Tasks, Module Launcher. No metrics cards, no B2C/B2B tabs, no quick actions. Fast load (3 async calls, not 5).
2. **Intelligence** — Click Intelligence in sidebar → Shows: System Health, Platform Overview (B2C/B2B tabs), Diagnostic Tools (5 action buttons), AI Analytics, Operations Intelligence, Integration Hub.
3. **Quick Actions** — Click any diagnostic tool button in Intelligence → executes and shows result modal.
4. **B2C/B2B tabs** — Switch between B2C and B2B tabs in Intelligence → cards render correctly.
