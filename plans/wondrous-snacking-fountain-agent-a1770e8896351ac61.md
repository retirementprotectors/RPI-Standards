# Builder 01 Plan: Sidebar + Portal Chrome (Sprint 10)

**Branch:** `sprint10/builder-01-sidebar`
**Worktree:** `/Users/joshd.millang/Projects/toMachina/.claude/worktrees/agent-a1770e88`

---

## Current State Analysis (Read-Only Phase Complete)

### Files Read:
1. `apps/prodash/app/(portal)/components/PortalSidebar.tsx` (697 lines)
2. `apps/riimo/app/(portal)/components/PortalSidebar.tsx` (581 lines)
3. `apps/sentinel/app/(portal)/components/PortalSidebar.tsx` (581 lines)
4. `packages/ui/src/components/PortalSwitcher.tsx` (129 lines)
5. `packages/ui/src/modules/AdminPanel.tsx` (lines 88-107 checked)
6. Verification files: accounts/page.tsx, contacts/page.tsx, ClientTabs.tsx, ActivityTab.tsx

---

## BUILD ITEMS

### TRK-402 — Compact sidebar action bar
**Current state:** 4 separate `<div className="border-t ...">` blocks (lines 554-693 in ProDash, ~439-577 in RIIMO, ~439-577 in SENTINEL). Each block has its own border-t and contains a full-width button. ~176px total vertical space.

**Plan:**
Replace all 4 bottom action blocks (Communications, Connect, Notifications, Admin) in each sidebar with a single compact `<div>` containing an icon row.

For ProDash (lines 553-693), RIIMO (lines 438-577), SENTINEL (lines 438-577):
- Delete the 4 separate `<div className="border-t ...">` blocks for Comms/Connect/Notifications/Admin
- Replace with single `<div className="border-t border-[var(--border-subtle)] px-2 py-1.5">`
- Inside: `{collapsed ? 'flex flex-col items-center gap-1' : 'flex items-center justify-around'}` row
- 4 icon buttons, each 36x36px `rounded-lg` with:
  - Communications: `forum` icon, portal-tinted, onClick={onCommsToggle}
  - Connect: `<img src="/rpi-shield.png">` at 20px, onClick={onConnectToggle}
  - Notifications: `notifications` icon, portal-tinted, onClick={onNotificationsToggle}, badge when count > 0
  - Admin: `admin_panel_settings` icon, red-tinted, `<Link href={ADMIN_ITEM.href}>`
- Active state: `bg-[rgba(color,0.15)]` + brighter icon + 3px left vertical bar on icon container
- Tiny 9px label below each icon when expanded, no labels when collapsed
- Need to add `notificationCount` prop to PortalSidebarProps (number, default 0) — currently no such prop exists in any portal. Will add it and use it for the badge.
- Keep `showAdmin` gating on the Admin icon

### TRK-411 — Sidebar label renames
**Current state (verified by reading):**
- ProDash: `Workspaces` (correct), `Sales` (correct), `Service` (correct)
- RIIMO: `Workspaces` (correct), `Service` (correct) — no Sales section
- SENTINEL: `Workspaces` (correct), `Service` (correct) — no Sales section
- AdminPanel: `Workspace` (line 95) — SINGULAR, needs to be `Workspaces`

**Plan:** Only fix AdminPanel line 95: `'Workspace'` -> `'Workspaces'`

### TRK-422 — Platform switcher three gears
**Current state:** `<img src={TOMACHINA_MARK}>` as the trigger button (line 70).

**Plan:**
- Remove the `<img>` tag
- Replace with 3 inline `<span className="material-icons">settings</span>` icons
- Each tinted with portal color: ProDashX `#4a7ab5`, RIIMO `#a78bfa`, SENTINEL `#40bc58`
- Current portal's gear: 20px, opacity 1. Others: 14px, opacity 0.4
- Rename `currentPortal` prop to `portal` — wait, it already receives `currentPortal`. The spec says "The component receives a `portal` prop". Check how it's used... The prop is `currentPortal: string`. I'll use that.
- Keep the `expand_more` chevron after the gears
- Can remove `TOMACHINA_MARK` constant if no longer used

### TRK-423 — Remove footer from platform switcher
**Current state:** The dropdown has 3 items (current portal + 2 others). The last `<a>` tag has `border-b` on it (line 108: `className="flex items-center px-4 py-3 transition-colors hover:bg-[var(--bg-hover)] border-b"`). This creates an unnecessary trailing border on the last item.

**Plan:** Remove `border-b` from the last portal link. Since it's in a `.map()`, I'll add a conditional to only add `border-b` to non-last items, or better, move the `border-b` styling to only appear on the first "other" portal (when there are 2 others, first gets border-b, second doesn't). Actually simplest: remove `border-b` from the `others.map()` items entirely and let the container border handle separation — or add it only to items that aren't the last. I'll use index check.

### TRK-424 — Apps section collapsible
**Current state (verified by reading):**
- ProDash: Has `appsExpanded` state, `APPS_EXPANDED_KEY`, `toggleApps()`, collapse/expand button, and `(collapsed || appsExpanded)` guard. COMPLETE.
- RIIMO: Has `appsExpanded` state (line 168), `APPS_EXPANDED_KEY` (line 114), `toggleApps()` (line 226-231), collapse/expand button (lines 381-398), and `(collapsed || appsExpanded)` guard (line 400). COMPLETE.
- SENTINEL: Has `appsExpanded` state (line 168), `APPS_EXPANDED_KEY` (line 114), `toggleApps()` (line 226-231), collapse/expand button (lines 381-398), and `(collapsed || appsExpanded)` guard (line 400). COMPLETE.

**Result:** All 3 portals already have Apps section collapsible. VERIFY-ONLY.

---

## VERIFY-ONLY ITEMS

| TRK | File | Expected | Actual | Result |
|-----|------|----------|--------|--------|
| TRK-405 | accounts/page.tsx | `useState('Active')` | Line 132: `useState('Active')`, Line 446: `useState('Active')` | PASS |
| TRK-406 | contacts/page.tsx | `useState('Active')` | Line 111: `useState('Active')` | PASS |
| TRK-408 | ClientTabs.tsx | No Communications tab | Line 22 comment: "Removed Communications tab" | PASS |
| TRK-410 | ActivityTab.tsx | Filter pills: All/Calls/Emails/SMS/Status Changes/Notes | Lines 74-80: all 6 pills present | PASS |
| TRK-417 | accounts/page.tsx | "+ New" opens NewAccountModal | Line 116-121: NewAccountModal defined; Line 922: `<NewAccountModal` rendered | PASS |

---

## Execution Order

1. **Create branch** `sprint10/builder-01-sidebar`
2. **TRK-411** — Fix AdminPanel `Workspace` -> `Workspaces` (1 line change)
3. **TRK-422 + TRK-423** — Rewrite PortalSwitcher.tsx (three gears trigger + remove trailing border)
4. **TRK-402** — Replace bottom action bars in all 3 PortalSidebar files (biggest change)
5. **Run `npm run build`** to verify compilation
6. **Run `npm run type-check`** to verify 13/13
7. **Report** all items

---

## Risk Notes

- `notificationCount` prop doesn't exist yet. I'll add it as optional `notificationCount?: number` to `PortalSidebarProps` in all 3 portals. The parent layout doesn't pass it yet, but it defaults to 0 so the badge won't show until it's wired.
- The Connect icon uses `<img src="/rpi-shield.png">` — need to verify this static asset exists in all 3 portal public dirs. If not, the shield already works in ProDash (line 617-621) so it likely exists.
- AdminPanel label fix (`Workspace` -> `Workspaces`) — spec says "Only fix the label if it exists" and "do NOT make other changes to AdminPanel (that's Builder 03 territory)."
