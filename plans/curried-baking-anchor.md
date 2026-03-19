# ProZone — Build Plan

## Context

ProZone is the prospecting hub App for toMachina. It organizes ALL prospecting opportunities by territory/zone/specialist schedule so Vince can select a specialist, hammer calls, and book appointments. 6 Iowa territories already defined from real client data (2,604 clients, 99.8% county coverage). Architecture fully designed in the Shared Drive doc.

This is an **App** (own brand, like Pipeline Studio) — NOT a Module. It appears in the Apps section of the ProDash sidebar.

## Build Order

### Phase 1: Data Layer (Types + Firestore + API)

**1a. Type Definitions** — `packages/core/src/types/index.ts`
- `Territory` — territory_id, name, state, region, counties[], zones[], status
- `Zone` — zone_id, territory_id, name, resolution_type (county|zip), assignments[] ({county?, zip?, zone_id})
- `SpecialistConfig` — config_id, user_id, name, territory_id, origin_zip, tier_map[], office_days, field_days, slot_templates, meeting_criteria, zone_lead_criteria, calendar_booking_url, team[]
- `TierMap` — zone_id, tier (I|II|III|IV), drive_minutes, slots_per_day, first_slot, last_slot

**1b. API Routes** — `services/api/src/routes/`
- `territories.ts` — CRUD for territories collection (GET list, GET :id, POST, PATCH)
- `specialist-configs.ts` — CRUD for specialist_configs collection
- `prozone.ts` — Aggregation endpoints:
  - `GET /api/prozone/prospects/:specialist_id` — prospects by zone for a specialist
  - `GET /api/prozone/schedule/:specialist_id/:week` — weekly schedule with tier slots
  - `GET /api/prozone/zone-leads/:specialist_id/:zone_id` — opportunistic leads in a zone

Register all 3 in `services/api/src/server.ts`

**1c. Seed Script** — `services/api/src/scripts/seed-prozone.ts`
- Seed 6 territories with county assignments from the ProZone doc
- Seed zone definitions within each territory
- Seed 4 specialist configs (Arch, Shane, Matt, JDM) with origin ZIPs and tier maps
- Update client records with territory_id + zone_id based on county/zip lookup

### Phase 2: UI Components

**2a. ProZone App Component** — `packages/ui/src/modules/ProZone/`
- `ProZone.tsx` — Main app wrapper with specialist selector + tab navigation
- `TerritoryView.tsx` — County grid color-coded by tier (not a map — data grid with tier badges)
- `ScheduleView.tsx` — Weekly Tue/Wed/Thu grid with tier-appropriate time slots, prospect cards
- `ProspectQueue.tsx` — Filterable list aggregated from pipelines, sorted by zone priority
- `ZoneLeadPanel.tsx` — "You're already going to Tier II Tuesday — here are 3 more leads"
- `SpecialistSelector.tsx` — Dropdown/card picker for switching between specialists

**2b. Admin Components** (for Settings/Admin section)
- `TerritoryBuilder.tsx` — Territory CRUD with county assignment drag/drop or checklist
- `SpecialistConfigEditor.tsx` — Config form (origin ZIP, schedule, criteria, booking link)

### Phase 3: Integration

**3a. ProDash Route** — `apps/prodash/app/(portal)/modules/prozone/page.tsx`
- Standard App wrapper pattern (like Pipeline Studio)

**3b. Sidebar Registration** — `apps/prodash/app/(portal)/components/PortalSidebar.tsx`
- Add to `APP_ITEMS`: `{ key: 'prozone', href: '/modules/prozone', moduleKey: 'PROZONE' }`

**3c. App Brand** — ProZone gets its own brand color (suggest: `--app-prozone: #0ea5e9` — sky blue, distinct from teal Pipeline Studio)

## Critical Files

| File | Action |
|------|--------|
| `packages/core/src/types/index.ts` | Add Territory, Zone, SpecialistConfig types |
| `packages/db/src/firestore.ts` | Add territories, specialist_configs collections |
| `services/api/src/routes/territories.ts` | NEW — Territory CRUD |
| `services/api/src/routes/specialist-configs.ts` | NEW — Specialist Config CRUD |
| `services/api/src/routes/prozone.ts` | NEW — Prospect aggregation + zone leads |
| `services/api/src/server.ts` | Register 3 new route files |
| `services/api/src/scripts/seed-prozone.ts` | NEW — Seed 6 territories + 4 specialists |
| `packages/ui/src/modules/ProZone/ProZone.tsx` | NEW — Main App component |
| `packages/ui/src/modules/ProZone/TerritoryView.tsx` | NEW — Territory grid |
| `packages/ui/src/modules/ProZone/ScheduleView.tsx` | NEW — Weekly schedule |
| `packages/ui/src/modules/ProZone/ProspectQueue.tsx` | NEW — Prospect list |
| `packages/ui/src/modules/ProZone/ZoneLeadPanel.tsx` | NEW — Zone lead surfacing |
| `packages/ui/src/modules/ProZone/SpecialistSelector.tsx` | NEW — Specialist picker |
| `packages/ui/src/modules/index.ts` | Export ProZone |
| `apps/prodash/app/(portal)/modules/prozone/page.tsx` | NEW — Route page |
| `apps/prodash/app/(portal)/components/PortalSidebar.tsx` | Add to APP_ITEMS |
| `apps/prodash/app/globals.css` | Add --app-prozone color |

## Reusable Patterns

- API: Follow `services/api/src/routes/clients.ts` pattern (successResponse, errorResponse, getPaginationParams)
- UI: Reuse `DataTable`, `SmartLookup`, `Modal`, `ConfirmDialog` from `@tomachina/ui`
- Hooks: Use `useCollection`, `useDocument` from `@tomachina/db`
- Theming: `var(--portal)` for portal-branded elements, `var(--app-prozone)` for App brand
- Page: Follow Pipeline Studio page.tsx pattern with `AppWrapper`

## Execution Strategy

**Parallel builders (3 agents in worktree isolation):**

1. **Builder A — Data Layer**: Types + API routes (territories, specialist-configs, prozone) + server.ts registration + seed script
2. **Builder B — UI Components**: ProZone module folder with all 6 components + module export
3. **Builder C — Integration**: ProDash route page + sidebar registration + globals.css brand color

Builders B+C depend on types from Builder A, but can scaffold with local type definitions and merge.

## Verification

1. `npm run type-check` — all 13 workspaces pass
2. `npm run dev` — ProDash loads, ProZone appears in sidebar
3. Navigate to `/modules/prozone` — App renders with specialist selector
4. Run seed script — 6 territories + 4 specialists in Firestore
5. Select a specialist — see territory view with county data
6. Switch to schedule view — see Tue/Wed/Thu with tier slots
7. Prospect queue populates from client data
