# Builder A — ProZone Data Layer Plan

## Deliverables (5 files to edit, 4 files to create)

### 1. Type Definitions — EDIT `packages/core/src/types/index.ts`
- Append ProZone types after the AccessItem interface (line ~498)
- 13 new interfaces/types: Territory, TerritoryCounty, Zone, ZoneAssignment, SpecialistConfig, TierMapEntry, SlotTemplate, MeetingCriteria, ZoneLeadCriteria, TeamMember

### 2. Collections — EDIT `packages/db/src/firestore.ts`
- Add `territories` and `specialistConfigs` to the collections object (before `} as const`)

### 3. API Route: territories.ts — CREATE `services/api/src/routes/territories.ts`
- Pattern: follows households.ts (same import style, same helpers, same error handling)
- `GET /` — list territories, optional `?state=` and `?status=` filters
- `GET /:id` — single territory with zones
- `POST /` — create territory (required: territory_name, state)
- `PATCH /:id` — update territory

### 4. API Route: specialist-configs.ts — CREATE `services/api/src/routes/specialist-configs.ts`
- `GET /` — list configs, optional `?territory_id=` and `?status=` filters
- `GET /:id` — single config
- `POST /` — create config (required: specialist_name, territory_id)
- `PATCH /:id` — update config

### 5. API Route: prozone.ts — CREATE `services/api/src/routes/prozone.ts`
- `GET /prospects/:specialist_id` — load specialist config, query clients in territory by county+state, apply meeting criteria, group by zone, sort by priority
- `GET /schedule/:specialist_id/:week` — parse YYYY-WNN week format, generate tier-appropriate time slots per day of week (office vs field days)
- `GET /zone-leads/:specialist_id/:zone_id` — load zone's counties, query clients matching zone lead criteria (active Medicare, active LA 80+, no core under 80)

### 6. Register Routes — EDIT `services/api/src/server.ts`
- Add 3 imports at the import block
- Add 3 `app.use()` lines before the 404 handler

### 7. Seed Script — CREATE `services/api/src/scripts/seed-prozone.ts`
- 6 territories with full county lists
- 4 specialist configs (Arch, Shane, Matt, JDM) with tier maps and slot templates
- Client update: query Iowa Active/Active- INTERNAL clients, match county to territory+zone
- Excluded from type-check via existing `"exclude": ["src/scripts/**/*"]` in tsconfig

## Execution Order
1. Edit types/index.ts (add ProZone interfaces)
2. Edit firestore.ts (add collections)
3. Create territories.ts route
4. Create specialist-configs.ts route
5. Create prozone.ts route
6. Edit server.ts (register routes)
7. Create seed-prozone.ts script
8. Run `npm run type-check` to verify 13/13 pass

## Key Patterns Observed
- All routes use `Router()` from express
- All routes export a named `*Routes` constant
- Helpers: `successResponse`, `errorResponse`, `stripInternalFields`, `param` from `../lib/helpers.js`
- `getFirestore()` from `firebase-admin/firestore` (NOT the client SDK)
- No `any` types — use `unknown` + type narrowing
- Typed req.user access: `(req as unknown as Record<string, unknown> & { user?: { email?: string } }).user?.email || 'api'`
- `.js` extension in imports (NodeNext module resolution)
- Collection names: snake_case in Firestore, camelCase in the collections object
