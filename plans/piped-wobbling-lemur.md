# Firestore Config Admin Panel — FORGE Sprint

## Context

Firestore is a black box for JDM. We built a v1 Firestore Config tab in the Admin Panel that provides visibility into 12 system config collections with a health dashboard. But CRUD capabilities are inconsistent — some field types have add/edit/delete, others are read-only or missing operations entirely. This sprint completes the feature with uniform CRUD at every level + wiring status indicators.

## Current State (v1 — already shipped)

- Health bar: active clients, households, users, active accounts, queues, data gaps
- Collection picker dropdown with 12 whitelisted collections
- Expandable document cards with field type detection
- Partial CRUD (see gap matrix below)

## CRUD Gap Matrix

| Level | Add | Edit | Delete | Gap |
|-------|-----|------|--------|-----|
| Collection | ✅ | — | ❌ | Need delete w/ confirmation |
| Document | ✅ | ✅ (via fields) | ❌ | Need delete w/ confirmation |
| String field | ❌ | ✅ | ❌ | Need add new field + delete field |
| Number field | ❌ | ✅ | ❌ | Need add new field + delete field |
| Boolean field | ❌ | ✅ toggle | ❌ | Need add new field + delete field |
| String array items | ✅ | ❌ | ✅ | Need inline edit of existing items |
| Object array rows | ✅ | ❌ read-only | ✅ | Need inline cell editing |
| Nested objects | ❌ | ❌ read-only | ❌ | Need add key, edit value, delete key |

## Collection Wiring Status (to show in UI)

| Collection | Status | Backend | Frontend | Notes |
|-----------|--------|---------|----------|-------|
| acf_config | FULL STACK | acf.ts (8 endpoints) | ACFConfigAdmin.tsx | Fully dynamic — changes take immediate effect |
| specialist_configs | FULL STACK | specialist-configs.ts | ProZone/SpecialistConfigEditor.tsx | CRUD complete |
| territories | FULL STACK | territories.ts | ProZone/TerritoryBuilder.tsx | CRUD complete |
| comp_grids | BACKEND ONLY | cam.ts (4 endpoints) | — | CAM writes grids, no UI reads yet |
| comp_grid_history | BACKEND ONLY | cam.ts (auto-audit) | — | Auto-populated on grid updates |
| spark_config | BACKEND ONLY | spark.ts (webhook status) | — | Webhook handler writes status |
| wire_definitions | CODE ONLY | Hardcoded in atlas.ts | — | 16 wires as code constants |
| source_registry | PLACEHOLDER | — | — | Collection exists, no code reads it |
| tool_registry | PLACEHOLDER | — | — | Collection exists, no code reads it |
| atlas_formats | TYPE ONLY | Type imports in import.ts | — | Schema types, no collection queries |
| format_library | TYPE ONLY | Type imports | — | Schema types, no collection queries |
| org | PLACEHOLDER | — | — | Empty placeholder |

## Files to Modify

### services/api/src/routes/firestore-config.ts (rewrite ~250 lines)
- GET /collections — add wiring status metadata per collection
- PUT /:collection/:docId — already handles create + update (done)
- DELETE /:collection/:docId — NEW: delete a document
- DELETE /:collection — NEW: delete all docs in a collection (with safety check)
- POST /:collection/:docId/field — NEW: add a field to a document
- DELETE /:collection/:docId/field/:fieldName — NEW: remove a field from a document

### packages/ui/src/modules/FirestoreConfig.tsx (rewrite ~700 lines)
Complete rewrite with uniform CRUD at every level:

**1. Wiring Status Badge per Collection**
- Dropdown shows colored badge: green (Full Stack), amber (Backend Only), gray (Placeholder)
- Tooltip explains what wiring status means

**2. Collection-Level CRUD**
- Add Collection: inline form (already built)
- Delete Collection: button w/ confirmation dialog ("Type collection name to confirm")

**3. Document-Level CRUD**
- Add Document: inline form (already built, move to top)
- Delete Document: trash icon on doc header w/ confirmation
- Expand/collapse document to see fields

**4. Field-Level CRUD (uniform for all types)**
- "Add Field" button at top of expanded doc → pick type (string/number/boolean/array/object) → enter name → create
- Delete Field: X button on every field label
- Edit Field: type-specific inline editors (see below)

**5. Field Editors (complete)**
- String: text input (already works)
- Number: number input (already works)
- Boolean: toggle switch (already works)
- String array: tag chips — click to edit inline, X to remove, + to add (upgrade from current)
- Object array: table rows — click cell to edit inline, X to remove row, + Add row at top (upgrade from current)
- Nested object: key-value pairs — click value to edit, X to remove key, + Add key (NEW)

**6. Collapsible Sections**
- Each array/object field section has a chevron toggle to collapse/expand
- Collapsed state shows count badge only

### packages/ui/src/modules/AdminPanel.tsx (minor)
- Already wired — no changes needed

### services/api/src/server.ts (no changes)
- Already registered

## Phase Breakdown (FORGE Tickets)

### Phase 1: API Completeness (3 tickets)
- TRK-A: API — Add DELETE /:collection/:docId endpoint
- TRK-B: API — Add DELETE /:collection endpoint (full collection delete w/ safety)
- TRK-C: API — Add wiring status metadata to GET /collections response

### Phase 2: Collection + Document CRUD (3 tickets)
- TRK-D: UI — Wiring status badges on collection dropdown (green/amber/gray + tooltip)
- TRK-E: UI — Delete Collection button with type-to-confirm dialog
- TRK-F: UI — Delete Document button with confirmation on each doc card

### Phase 3: Field-Level Add/Delete (3 tickets)
- TRK-G: UI — "Add Field" button → type picker → name input → creates field
- TRK-H: UI — Delete Field (X button) on every field label with confirmation
- TRK-I: API — Add POST/DELETE field endpoints for granular field ops

### Phase 4: Field Editor Upgrades (4 tickets)
- TRK-J: UI — String array: click-to-edit existing items (not just add/remove)
- TRK-K: UI — Object array: inline cell editing (click cell → input → blur saves)
- TRK-L: UI — Nested object: editable key-value pairs with add/remove keys
- TRK-M: UI — Collapsible sections for array/object fields (chevron toggle)

### Phase 5: UX Polish (3 tickets)
- TRK-N: UI — Reorder buttons (Add Collection first, then Add Document, Refresh right-aligned green)
- TRK-O: UI — Loading/saving states consistent across all operations (skeleton, spinners, success feedback)
- TRK-P: UI — Empty state improvements (new collection empty, new doc empty, helpful prompts)

### Phase 6: Health Bar Refinements (2 tickets)
- TRK-Q: UI — Health bar responsive wrapping for smaller screens
- TRK-R: API — Health endpoint error resilience (individual query failures don't break entire response)

## Total: 18 tickets across 6 phases

## Verification
1. npm run build passes (11/11)
2. npm run type-check passes (13/13)
3. Every CRUD operation works end-to-end:
   - Create collection → appears in dropdown
   - Create document → appears in card list
   - Add field → appears in expanded doc
   - Edit every field type → saves to Firestore
   - Delete field → removed from doc
   - Delete document → removed from list
   - Delete collection → removed from dropdown
4. Wiring status badges show correctly for all 12 collections
5. Collapsible sections work for all array/object fields
6. Confirmation dialogs prevent accidental deletes
