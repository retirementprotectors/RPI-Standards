# FORGE Sprint Detail Panel + Auto HTML Plan Generation

## Context

JDM has zero visibility into sprint entities after creation. Clicking a sprint card just filters the backlog — there's no way to view/edit sprint metadata (name, description, discovery doc, plan doc, audit rounds, phase). Additionally, the #LetsPlanIt and #LetsBuildIt prompt phases should auto-generate an HTML plan document, save it to `public/plans/`, write the URL to the sprint's `plan_link`, and open it in the browser — this is how JDM aligns vision with execution.

## What We're Building

### 1. Sprint Detail View (inside Forge.tsx)

**New view state:** `view === 'sprint-detail'`

**Navigation:**
- Click sprint card → `setSelectedSprintId(sp.id); setView('sprint-detail')` (replaces current filter-to-grid behavior)
- Back button → `setView('sprints')` (returns to Kanban)

**Layout (top to bottom):**

```
┌─ Header ─────────────────────────────────────────┐
│ ← Back to Sprints    [Phase Badge]    [Action Btn]│
│ Sprint Name (editable)                            │
│ Description (editable)                            │
├─ Doc Links ──────────────────────────────────────┤
│ 📄 Discovery Doc: [url] (editable, click to open) │
│ 📋 Plan Doc:      [url] (editable, click to open) │
├─ Metadata ───────────────────────────────────────┤
│ Created by: josh@  |  Created: Mar 18  |  Phase  │
├─ Progress ───────────────────────────────────────┤
│ ████████░░ 6/11 confirmed  (3 bug, 5 enh, 3 feat)│
├─ Audit Round ────────────────────────────────────┤
│ Round 2: 4 passed, 2 failed, 5 pending           │
├─ Items ──────────────────────────────────────────┤
│ [Compact table of sprint items with status pills] │
│ TRK-224  Household migration  built   bug         │
│ TRK-225  DeDup fix            confirmed enh       │
│ ...                                                │
└──────────────────────────────────────────────────┘
```

**New state variables:**
- `selectedSprintId: string | null` — which sprint is open
- `sprintEditField: string | null` — which field is being edited (name, description, discovery_url, plan_link)
- `sprintEditValue: string` — temp edit value
- `auditRound: AuditRoundInfo | null` — loaded from GET /api/sprints/:id/audit-round

**Inline editing pattern:**
- Click field text → shows input/textarea
- Enter/blur → PATCH /api/sprints/:id with changed field → reload sprints
- Escape → cancel

**Audit round:** Loaded on detail open via `GET /api/sprints/:id/audit-round`. Shows current round number, pass/fail/pending counts with color-coded badges.

**Item list:** Filter `allItems` by `sprint_id === selectedSprintId`. Show compact rows: item_id, title, status pill, type pill. Click row → opens item edit modal (existing `setEditItem` pattern).

### 2. Auto HTML Plan Generation (prompt flow enhancement)

**Current flow:** #LetsPlanIt → `generatePrompt(sprintId, 'discovery')` → shows markdown in modal → user copies to clipboard

**New flow:** The prompt instructions (in `GET /api/sprints/:id/prompt`) will include a directive telling the builder agent to:

1. Generate an HTML plan document at `apps/riimo/public/plans/{sprint-slug}.html`
2. Follow the established HTML plan format (dark theme, sections, branded)
3. Return the URL in the response

**On the FORGE UI side**, after the prompt is generated and copied:
- Add instruction text in the prompt modal: "Builder: create HTML plan at `apps/riimo/public/plans/{slug}.html` and return the URL"
- When plan_link is set on the sprint (via PATCH from builder or manually), the Sprint Detail view shows it as a clickable link

**This is NOT automated code generation** — it's prompt language that tells the BUILDER AGENT to create the HTML as part of its plan phase output. The instruction goes in the markdown prompt that gets copied to the builder session.

## Files to Modify

| File | Change |
|------|--------|
| `packages/ui/src/modules/Forge.tsx` | Add `sprint-detail` view, new state vars, Sprint Detail render block, update card onClick |
| `services/api/src/routes/sprints.ts` | Add HTML plan generation directive to prompt output for `phase=discovery` and `phase=building` |

## Implementation Steps

1. Add state: `selectedSprintId`, `sprintEditField`, `sprintEditValue`, `auditRound`
2. Update sprint card onClick: `setSelectedSprintId(sp.id); setView('sprint-detail')`
3. Build Sprint Detail view (~200 lines):
   - Header with back button + phase badge + action button
   - Editable fields (name, description, discovery_url, plan_link)
   - Metadata row (created_by, created_at, phase)
   - Progress bar + type pills
   - Audit round summary (fetched on mount)
   - Filtered item table
4. Add `saveSprint` function: PATCH /api/sprints/:id + reload
5. Update prompt generation to include HTML plan directive
6. Wire "View Items" from detail → still works (setView('grid') with sprint filter)

## Verification
- Click sprint card → opens detail (not grid filter)
- Edit name → saves via PATCH → refreshes
- Edit plan_link → saves → shows as clickable link
- Back button → returns to Kanban
- Phase action button works from detail view
- Audit round data loads and displays
- Item table shows correct items for sprint
- #LetsPlanIt prompt includes HTML plan generation instructions
- 13/13 type-check passes
