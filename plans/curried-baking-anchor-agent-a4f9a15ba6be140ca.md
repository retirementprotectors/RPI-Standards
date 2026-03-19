# ProZone UI Components — Builder B Plan

## Summary
Build 8 React components for the ProZone prospecting hub App in `packages/ui/src/modules/ProZone/`.

## Research Complete
- Read `CommandCenter.tsx` — App pattern with `portal` prop, CSS variable theming, `fetchWithAuth`, loading/error states
- Read `PipelineStudio/` — Directory-based module with `index.ts` re-export, `PipelineStudioApp.tsx` main shell
- Read `QueWorkbench/` — Multi-view pattern with `ViewMode` state, sub-components in subdirectories
- Read `fetchWithAuth.ts` — Shared auth helper for API calls
- Read `globals.css` — Full CSS variable catalog (backgrounds, text, borders, semantic colors, badges, buttons, table-premium)
- Read `tsconfig.json` — strict mode, ES2022 target, react-jsx
- Read `packages/ui/src/modules/index.ts` — Module barrel exports

## Key Patterns to Follow
1. **'use client'** directive on every component
2. **Props interfaces** defined in-file
3. **CSS variables** for all colors: `var(--bg-card)`, `var(--text-primary)`, `var(--border-subtle)`, etc.
4. **App branding**: ProZone uses `var(--app-prozone)` (#0ea5e9 sky blue) — needs to be added to globals.css in all 3 portals
5. **fetchWithAuth** for API calls
6. **Loading/error states** on all data fetches
7. **Tailwind v4 classes** for layout (flex, grid, gap, padding)
8. **No alert/confirm/prompt** — would use Toast if needed
9. **Directory structure**: `ProZone/` folder with `index.ts` barrel export

## Files to Create

### 1. `packages/ui/src/modules/ProZone/index.ts`
Barrel export: `export { default as ProZone } from './ProZoneApp'`

### 2. `packages/ui/src/modules/ProZone/types.ts`
Local interfaces: `SpecialistConfig`, `Territory`, `TerritoryCounty`, `Zone`, `TierMap`, `TeamMember`, `Prospect`, `ZoneLead`, `ScheduleSlot`, `WeekSchedule`

### 3. `packages/ui/src/modules/ProZone/ProZoneApp.tsx`
Main App shell. Manages:
- Specialist list fetch from `/api/specialist-configs`
- Selected specialist state
- Active tab state (territory | schedule | queue | zone-leads)
- Renders SpecialistSelector + tab nav + active view
- Brand accent: `var(--app-prozone)`

### 4. `packages/ui/src/modules/ProZone/SpecialistSelector.tsx`
Card picker for specialists. Shows name, territory, origin city. Highlighted active card.

### 5. `packages/ui/src/modules/ProZone/TerritoryView.tsx`
Data grid with county rows. Tier-colored badges. Expandable rows. Uses `table-premium` CSS classes from globals.

### 6. `packages/ui/src/modules/ProZone/ScheduleView.tsx`
3-column weekly grid (Tue/Wed/Thu). Tier-appropriate slot counts. Week navigation arrows.

### 7. `packages/ui/src/modules/ProZone/ProspectQueue.tsx`
Filterable prospect list. Filter bar with dropdowns + search. Expandable rows with action buttons.

### 8. `packages/ui/src/modules/ProZone/ZoneLeadPanel.tsx`
Alert banner + zone lead list. Contextual to selected zone + existing meetings.

### 9. `packages/ui/src/modules/ProZone/TerritoryBuilder.tsx`
Admin form: territory name, state, status. County checklist with zone grouping. ZIP override section.

### 10. `packages/ui/src/modules/ProZone/SpecialistConfigEditor.tsx`
Admin form with 6 sections: Basic, Schedule, Tiers, Criteria, Calendar, Team.

## Modifications to Existing Files

### `packages/ui/src/modules/index.ts`
Add: `export { ProZone } from './ProZone'`

## Execution Order
1. Create `ProZone/` directory
2. Write `types.ts` (shared types used by all components)
3. Write all 8 components in parallel (no cross-dependencies beyond types)
4. Write `index.ts` barrel
5. Update `modules/index.ts`
6. Run `npm run type-check`

## Risk: CSS Variable
`var(--app-prozone)` doesn't exist in globals.css yet. Two options:
- **Option A**: Add it to all 3 portal globals.css files (correct long-term)
- **Option B**: Define it as a fallback in each component: `style={{ color: 'var(--app-prozone, #0ea5e9)' }}`

Going with **Option B** (fallback) since this is UI-only builder work and the CSS var can be added by the planner/auditor across portals. This avoids touching files outside my deliverable scope.

## Ready to Execute
All patterns understood. All files scoped. No blocking questions.
