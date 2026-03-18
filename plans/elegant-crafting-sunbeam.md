# FORGE — The Machine's Build Tracker

## Context

JDM has 60+ UI items across sprints 8-9 tracked in scattered lists, conversations, and an HTML file. Items get partially addressed, nobody tracks completion, and JDM re-requests the same fixes across sessions. The APPA framework was missing its **Process** layer for platform development.

**FORGE is a standalone App** — own brand, cross-portal, leadership+ access. Like Pipeline Studio, it appears in the Apps section of every portal sidebar with its own identity. Select items → create sprint → generate Claude Code prompt → build → audit → confirm. Single source of truth.

---

## Brand

| Property | Value |
|----------|-------|
| **AppKey** | `forge` |
| **Label** | FORGE |
| **Description** | Build Tracker |
| **Color** | `#e07c3e` (copper/forge orange) |
| **Icon** | `construction` |
| **Access** | Leadership+ (OWNER, EXECUTIVE, LEADER) via moduleKey `FORGE` |

4px copper brand bar at top. Portal-themed content below. Same in all 3 portals.

---

## Data Model

### `tracker_items` collection
| Field | Type | Description |
|-------|------|-------------|
| item_id | string | Auto: "TRK-001" |
| title | string | Required |
| description | string | Full details |
| portal | string | PRODASHX / RIIMO / SENTINEL / SHARED / INFRA / DATA |
| scope | string | Module / App / Platform / Data |
| component | string | e.g. "Accounts Grid", "Communications" |
| section | string | e.g. "Header", "Body", "Filters" |
| status | string | not_touched / in_sprint / planned / built / audited / confirmed / deferred / wont_fix |
| sprint_id | string? | Links to sprint |
| plan_link | string? | URL to plan doc |
| notes | string | Free text |
| created_by | string | Email |
| created_at / updated_at | string | ISO timestamps |

### `sprints` collection
| Field | Type | Description |
|-------|------|-------------|
| name | string | e.g. "Sprint 10" |
| description | string | What this sprint covers |
| status | string | draft / active / complete |
| plan_link | string? | URL to plan |
| prompt_text | string | Generated Claude Code prompt |
| created_by | string | Email |
| created_at / updated_at | string | ISO timestamps |

Items link to sprints via `sprint_id`. Filter items by sprint.

---

## Files

### NEW
| File | What |
|------|------|
| `packages/ui/src/modules/Forge.tsx` | Full app UI: grid, edit modal, sprint creation, prompt generator (~600-700 lines) |
| `apps/prodash/app/(portal)/modules/forge/page.tsx` | ProDashX route wrapper (5 lines) |
| `apps/riimo/app/(portal)/modules/forge/page.tsx` | RIIMO route wrapper (5 lines) |
| `apps/sentinel/app/(portal)/modules/forge/page.tsx` | SENTINEL route wrapper (5 lines) |
| `services/api/src/routes/tracker.ts` | CRUD for tracker_items |
| `services/api/src/routes/sprints.ts` | CRUD for sprints + prompt generation |
| `services/api/src/scripts/seed-tracker.ts` | One-time: seed 85 items from tracker.html |

### MODIFIED
| File | Change |
|------|--------|
| `packages/ui/src/apps/brands.ts` | Add `'forge'` to AppKey + APP_BRANDS |
| `packages/ui/src/modules/index.ts` | Export `{ Forge }` |
| `packages/db/src/firestore.ts` | Add `trackerItems` + `sprints` collections |
| `firestore.rules` | Add isRPIUser rules for both collections |
| `services/api/src/server.ts` | Mount tracker + sprint routes |
| `apps/prodash/.../PortalSidebar.tsx` | Add forge to APP_ITEMS with moduleKey `FORGE` |
| `apps/riimo/.../PortalSidebar.tsx` | Add forge to APP_ITEMS with moduleKey `FORGE` |
| `apps/sentinel/.../PortalSidebar.tsx` | Add forge to APP_ITEMS with moduleKey `FORGE` |

---

## UI — Forge.tsx

### Grid (matches Contacts/Accounts pattern exactly)
- **Row 1**: Search + "+ New" button
- **Row 2**: Filters — Status | Portal | Scope | Component | Sprint (dropdowns)
- **Table**: Checkbox | ID | Title | Component | Section | Portal | Status | Sprint
- **Pagination**: Showing X–Y of Z, Previous/Next
- Row click → opens **edit slide-out**
- Multi-select → "Create Sprint" button appears

### Edit Slide-out (row click or hover edit icon)
All fields editable:
- Title, Description
- Portal, Scope, Status (dropdowns)
- Component, Section
- Sprint (dropdown: existing sprints + Unassigned)
- Plan Link (URL)
- Notes (textarea)
- Save / Cancel
- Created/Updated (read-only)

### Sprint Creation Flow
1. Select items via checkboxes
2. Click "Create Sprint"
3. Modal: Sprint Name + Description
4. Click Create → new sprint doc, selected items get `sprint_id`, status → 'in_sprint'

### Prompt Generator
1. Filter by sprint
2. Click "Generate Prompt" (visible when sprint filter active)
3. Generates structured markdown grouped by Component:
```
# Sprint 10 — [Name]
## Accounts Grid
- [TRK-001] Default to Active — description...
- [TRK-002] + New opens Account — description...
## Communications Module
- [TRK-045] Top-level nav — description...
```
4. Opens in copyable textarea modal → paste into Claude Code

### Sprint Summary Bar (when sprint filtered)
- Progress: X of Y confirmed | Progress bar
- Plan link (clickable)
- "Generate Prompt" button

---

## API

### `/api/tracker` (tracker_items CRUD)
```
GET    /api/tracker           ?status=&portal=&scope=&component=&sprint_id=&search=&page=&pageSize=
GET    /api/tracker/:id
POST   /api/tracker           { title, description, portal, scope, component, section }
PATCH  /api/tracker/:id       partial fields
DELETE /api/tracker/:id
PATCH  /api/tracker/bulk      { ids: [], updates: { sprint_id, status } }
```

### `/api/sprints` (sprints CRUD)
```
GET    /api/sprints
POST   /api/sprints           { name, description, item_ids }
PATCH  /api/sprints/:id       partial fields
GET    /api/sprints/:id/prompt   → generated markdown prompt
DELETE /api/sprints/:id          → unassigns items
```

Follows `case-tasks.ts` patterns: `getPaginationParams`, `paginatedQuery`, `successResponse`, `errorResponse`.

---

## Status Workflow

```
not_touched → in_sprint → planned → built → audited → confirmed
                                                        ↓ complete

any → deferred | wont_fix (parallel tracks)
```

| Status | Color | Meaning |
|--------|-------|---------|
| not_touched | red | Nobody looked at this |
| in_sprint | amber | Assigned to a sprint |
| planned | portal blue | Plan exists |
| built | teal | Code shipped |
| audited | purple | Developer verified |
| confirmed | green | JDM verified |
| deferred | gray | Explicitly pushed |
| wont_fix | muted | Decided not to do |

---

## Builders (parallel, zero file conflicts)

### Builder A: Backend + Plumbing
- `services/api/src/routes/tracker.ts` — full CRUD + bulk
- `services/api/src/routes/sprints.ts` — CRUD + prompt gen
- `services/api/src/server.ts` — mount both routes
- `packages/db/src/firestore.ts` — add collections
- `firestore.rules` — add rules
- `packages/ui/src/apps/brands.ts` — add forge brand
- `services/api/src/scripts/seed-tracker.ts` — seed 85 items

### Builder B: Frontend
- `packages/ui/src/modules/Forge.tsx` — full app component
- `packages/ui/src/modules/index.ts` — export
- `apps/prodash/.../modules/forge/page.tsx` — route
- `apps/riimo/.../modules/forge/page.tsx` — route
- `apps/sentinel/.../modules/forge/page.tsx` — route
- All 3 `PortalSidebar.tsx` files — add to APP_ITEMS

---

## Verification
1. Sidebar → FORGE (copper icon) visible in all 3 portals
2. Click → opens with 4px copper brand bar + grid of 85 seeded items
3. Click row → edit slide-out, change fields → saves on refresh
4. Select 5 items → "Create Sprint" → name it → items assigned
5. Filter by sprint → only assigned items show
6. "Generate Prompt" → structured markdown in copyable modal
7. "+ New" → add item → appears in grid
8. Non-leader user → FORGE hidden in sidebar (leadership+ only)
9. Type-check: 13/13 passes
