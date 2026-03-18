ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# Sprint 8 Polish — Builder Plan

## Context

JDM's UI review identified 54 items across the platform. Quick Wins + Medium Work = 26 items. After thorough code audit, **14 of 26 items are already implemented** by Sprint 8 agents during the merge/audit process. Only the Grid Pages + Global Polish scope (Builder 1) actually needs work.

## Already Done (Confirmed from Current Code)

| Item | What | Evidence |
|------|------|----------|
| C3-1 | Access button moved to tabs | `ClientTabs.tsx:27` — access tab in TABS array |
| C3-2 | Comms first, new tab order | `ClientTabs.tsx:21` — communications first |
| CM-1 | "Log Call" → "Call" | `CommsToolbar.tsx:76` — says "Call" |
| PT-1 | DL Issue Date field | `PersonalTab.tsx:147-150` — dl_issue_date field |
| AV-1 | All/Client/Account sub-tabs | `ActivityTab.tsx:67-71` — 3 sub-tabs |
| TB-1 | Email removed from top bar | `TopBar.tsx:126-128` — first name only |
| DD-2/AT-1 | DeDup button handler real | `AccountsTab.tsx:126-129` — window.open to ddup |
| CT-1 | Agent/BoB/Source dropdowns | `ContactTab.tsx:314-337` — select with Firestore data |
| PS-1 | Portal switcher images | `PortalSwitcher.tsx` — uses text labels now |
| RC-1 | Shield icon removed | `ConnectPanel.tsx` — no shield/fake icon |
| RC-2 | Pill shapes correct | `ConnectPanel.tsx:274` — `rounded-md h-[34px]` |
| AT-3 | Account card → new tab | `AccountsTab.tsx:303-304` — `window.open(_blank)` |
| AD-1 | Team Config active filter | `AdminPanel.tsx:390-393` — filters active status |
| AD-2 | Team Config 3-level redesign | `AdminPanel.tsx:396-548` — Level/User/Entitlements |

## Only Builder 1 Needed

Since all Client 360, ConnectPanel, Admin, and Top Bar items are done, we only need **one builder** for Grid Pages + Global Polish.

---

## Builder 1: Grid Pages + Global Polish

**Branch:** `sprint8/grid-polish`

### Files to Modify

| File | Tasks |
|------|-------|
| `apps/prodash/app/globals.css` | G-1 |
| `apps/prodash/app/(portal)/accounts/page.tsx` | AC-1 through AC-10 |
| `apps/prodash/app/(portal)/clients/components/ClientFilters.tsx` | CG-1, CG-2 |
| `apps/prodash/app/(portal)/clients/page.tsx` | CG-2, DD-1 |

### Files to Read (reference, don't modify)

- `apps/prodash/app/(portal)/clients/components/ColumnSelector.tsx` — column selector pattern
- `apps/prodash/app/(portal)/ddup/page.tsx` — ddup URL pattern (`/ddup?ids=id1,id2&type=client`)

---

### Task Details

#### G-1: Global cursor-pointer
**File:** `globals.css` — Add near top (after existing base resets):
```css
button, a, [role="button"], [tabindex="0"] { cursor: pointer; }
```

#### AC-1: Accounts Row 1 — Search + New button
**File:** `accounts/page.tsx` lines 308-346
- **Restructure header** into 3 distinct rows
- **Row 1 (left):** Search input — change from `rounded-lg` to `rounded-md`, match contacts shape (`h-[34px]`)
- **Row 1 (right):** `+ New` button — rename from "+ New Account" to just have `add` icon + "New", match contacts style: `rounded-md border border-[var(--portal)] bg-[var(--portal)] h-[34px] px-3 text-sm font-medium text-white`

#### AC-2: Accounts Row 2 — Filters as pills
**File:** `accounts/page.tsx` lines 348-384
- Status dropdown (`<select>` line 351): Change from `h-9 rounded-lg` to `h-[34px] rounded-md` with styling matching contacts filter pattern: inactive = `border-[var(--border)] bg-[var(--bg-surface)] text-[var(--text-secondary)]`, active = `border-[var(--portal)] bg-[var(--portal)] text-white`
- Carrier dropdown (line 365): Same treatment
- Columns button (line 328): Change from `rounded-lg` to `rounded-md`, add `h-[34px]`
- All three in same row

#### AC-3: Accounts Row 3 — Type pills + counter
**File:** `accounts/page.tsx` lines 386-405
- Move the filter tabs (All | Annuity | Life | Medicare | Investment) to Row 3
- Add counter on far right: `rounded-full bg-[var(--portal)] px-2.5 py-0.5 text-xs font-semibold text-white`
- Counter shows filtered count (not raw `accounts.length`)

#### AC-4: Accurate account count
**File:** `accounts/page.tsx` line 311-313
- Remove the standalone badge from header (this IS AC-10)
- Counter in Row 3 should show: `${filtered.length.toLocaleString()}${hasMore ? '+' : ''}`
- This handles the "500+" case when `hasMore` is true

#### AC-5: Status/Carrier styled as pills
**File:** `accounts/page.tsx`
- Extract `filterSelectClass` helper matching `ClientFilters.tsx:81-86`:
  ```
  h-[34px] rounded-md border px-3 text-sm font-medium outline-none transition-all cursor-pointer
  Active: border-[var(--portal)] bg-[var(--portal)] text-white
  Inactive: border-[var(--border)] bg-[var(--bg-surface)] text-[var(--text-secondary)]
  ```

#### AC-6: Background deepest black
**File:** `accounts/page.tsx` line 307
- Remove any `bg-[var(--bg-card)]` wrapper
- Container should inherit `bg-[var(--bg-primary)]` (deepest background from layout)
- Check if the table wrapper at line 443 (`bg-[var(--bg-card)]`) is correct — table should still have card background, but the page container should not

#### AC-7 + AC-8: Highlight color text
**File:** `accounts/page.tsx`
- Table column headers (line 466): Change `text-[var(--text-muted)]` to `text-[var(--portal)]`
- "Columns" button text (line 335): Add `text-[var(--portal)]` when inactive (currently `text-[var(--text-muted)]`)
- "Accounts" text in pagination header: apply `text-[var(--portal)]`

#### AC-9: Button height consistency
**File:** `accounts/page.tsx`
- Audit ALL buttons and inputs — every interactive element must be `h-[34px]`
- Search input (line 324): Change `py-2` to match `h-[34px]`
- New button (line 340): Add `h-[34px]`
- Column button (line 330): Add `h-[34px]`
- Status/Carrier selects: Add `h-[34px]`

#### AC-10: Remove "500" badge
**File:** `accounts/page.tsx` lines 310-314
- Remove the `<span>` with `rounded-full bg-[var(--portal)]` that shows `accounts.length`
- Count now lives in Row 3 far-right (see AC-3)

#### CG-1: Contacts filter button styling
**File:** `ClientFilters.tsx`
- Filter buttons already use `bg-[var(--bg-surface)]` base when inactive — this matches accounts
- Verify inactive state uses same gray as accounts redesign
- No changes likely needed if accounts adopts same pattern from contacts

#### CG-2: Contacts column headers in highlight color
**File:** `clients/page.tsx` lines 221, 233
- `renderSortHeader`: Change `text-[var(--text-muted)]` to `text-[var(--portal)]`
- `renderStaticHeader`: Change `text-[var(--text-muted)]` to `text-[var(--portal)]`

#### DD-1: DeDup on contacts grid
**File:** `clients/page.tsx`
- Add `selectedIds` state: `useState<Set<string>>(new Set())`
- Add checkbox column to table (same pattern as accounts page):
  - Header checkbox (select all on page)
  - Row checkbox per client
- When 2+ selected, show "Ddup Selected (N)" button in filters area
- Click opens: `window.open(`/ddup?ids=${ids}&type=client`, '_blank', 'noopener,noreferrer')`
- Pattern reference: `accounts/page.tsx` lines 250-261 (toggleSelect + handleDdup)

---

### Layout Reference (Target Accounts Page Structure)

```
Row 1: [Search input ........]                    [+ New]
Row 2: [All Statuses ▾] [All Carriers ▾] [Columns]
Row 3: [All] [Annuity] [Life] [Medicare] [Investment]    (5,018)
─────────────────────────────────────────────────────────
Table with portal-colored headers...
```

### Styling Constants (copy from contacts)

```typescript
// filterSelectClass helper
const filterSelectClass = (isActive: boolean) =>
  `h-[34px] rounded-md border px-3 text-sm font-medium outline-none transition-all cursor-pointer ${
    isActive
      ? 'border-[var(--portal)] bg-[var(--portal)] text-white'
      : 'border-[var(--border)] bg-[var(--bg-surface)] text-[var(--text-secondary)] hover:border-[var(--portal)] hover:text-[var(--portal)]'
  } focus:border-[var(--portal)]`
```

---

## Verification

1. `npm run dev` in toMachina root
2. Open `localhost:3001/accounts` — verify:
   - 3-row header layout matches spec
   - All buttons are `h-[34px]`
   - Counter on Row 3 far-right with portal color
   - Status/Carrier dropdowns styled as pills
   - Column headers in portal color
   - Background matches contacts page
   - cursor-pointer on all clickable elements
3. Open `localhost:3001/clients` — verify:
   - Column headers in portal color
   - Checkbox column appears
   - Select 2+ → "Ddup Selected" button appears
   - Click opens ddup page in new tab
4. `npm run build` — no TypeScript errors
