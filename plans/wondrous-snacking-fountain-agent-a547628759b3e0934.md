# BUILDER 01 — Sprint 10 Sidebar Plan

## Status: READY TO EXECUTE (all files read, all edits defined)

I have read all 5 files. Here is the exact execution plan:

---

## TRK-402 — Compact Action Bar (ALL 3 PORTALS)

### ProDash (`apps/prodash/app/(portal)/components/PortalSidebar.tsx`)
**Lines 554-693**: Replace the 4 separate `<div className="border-t ...">` blocks (Communications, Connect, Notifications, Admin) with a single compact action bar.

**Old string** starts at line 554: `{/* Communications — portal-tinted, opens slide-out */}` and ends at line 693: closing `)}` of the Admin block.

**New**: Single `<div className="border-t border-[var(--border-subtle)] px-2 py-1.5">` with flex layout containing all 4 buttons as compact icon+label columns.

### RIIMO (`apps/riimo/app/(portal)/components/PortalSidebar.tsx`)
**Lines 439-577**: Same pattern. RIIMO uses purple tints (`rgba(167,139,250,...)`) for comms/notifications. Connect uses green. Connect icon uses `CONNECT_ITEM.icon` (`settings_input_composite`) instead of an image.

### SENTINEL (`apps/sentinel/app/(portal)/components/PortalSidebar.tsx`)
**Lines 439-577**: Same pattern. SENTINEL uses green tints (`rgba(64,188,88,...)`) for comms/notifications. Connect icon uses `CONNECT_ITEM.icon` (`settings_input_composite`).

**Key differences between portals:**
- ProDash: Connect button uses `<img src="/rpi-shield.png">`, comms/notifications use blue `rgba(74,122,181,...)`
- RIIMO: Connect button uses `<span className="material-icons-outlined">{CONNECT_ITEM.icon}</span>`, comms/notifications use purple `rgba(167,139,250,...)`
- SENTINEL: Connect button uses `<span className="material-icons-outlined">{CONNECT_ITEM.icon}</span>`, comms/notifications use green `rgba(64,188,88,...)`

---

## TRK-411 — Label Renames

### All 3 sidebars: Already have correct labels!
- ProDash line 52: `label: 'Workspaces'` -- CORRECT
- ProDash line 64: `label: 'Sales'` -- CORRECT
- ProDash line 73: `label: 'Service'` -- CORRECT
- RIIMO line 49: `label: 'Workspaces'` -- CORRECT
- RIIMO line 63: `label: 'Service'` -- CORRECT
- SENTINEL line 49: `label: 'Workspaces'` -- CORRECT
- SENTINEL line 63: `label: 'Service'` -- CORRECT

### AdminPanel.tsx (`packages/ui/src/modules/AdminPanel.tsx`)
Line 95: `label: 'Workspace'` --> needs to change to `label: 'Workspaces'`

---

## TRK-422 — Platform Switcher Three Gears

### `packages/ui/src/components/PortalSwitcher.tsx`
**Lines 64-77**: Replace the trigger button (uses `<img src={TOMACHINA_MARK}>`) with three gear icons sized/colored per portal.

The component receives `currentPortal` prop (line 34). Need to alias it for the template. The `toggle` function is `() => setOpen(!open)`, and `open` state is used for dropdown.

Also need to handle: The component uses `TOMACHINA_MARK` constant (line 5) -- can remove it after replacing the trigger since it's no longer used.

---

## TRK-423 — Remove Footer from Platform Switcher

Looking at the dropdown (lines 80-124): The last portal link has `border-b` class on line 108. This creates a trailing border at the bottom. Need to remove the `border-b` from the `<a>` elements for the other portals (or at least from the last one). Actually, looking more carefully, ALL `<a>` tags have `border-b` (line 108). The last one creates a visible bottom border. Should remove `border-b` from the other portal links, or conditionally remove it from the last one.

Actually, the simplest fix: change the `border-b` on the `<a>` tags so the last one doesn't have it. Or just remove `border-b` from the anchor className since the visual separator between portals can come from the overall design.

---

## TRK-424 — Apps Collapsible

### ProDash: Has `appsExpanded` state (line 174) + `toggleApps` (line 327) + `APPS_EXPANDED_KEY` (line 115). DONE.
### RIIMO: Has `appsExpanded` state (line 168) + `toggleApps` (line 226) + `APPS_EXPANDED_KEY` (line 114). DONE.
### SENTINEL: Has `appsExpanded` state (line 168) + `toggleApps` (line 226) + `APPS_EXPANDED_KEY` (line 114). DONE.

All 3 portals already have the apps collapsible pattern. NO CHANGES NEEDED.

---

## Verify-Only Items — ALL CONFIRMED

- `accounts/page.tsx` line 132+446: `useState('Active')` -- VERIFIED
- `contacts/page.tsx` line 111: `useState('Active')` -- VERIFIED
- `ClientTabs.tsx` line 22: Comment confirms Communications tab removed (TRK-024) -- VERIFIED
- `ActivityTab.tsx` lines 31,72,84,86: Filter pills present -- VERIFIED
- `accounts/page.tsx` lines 113-276,677,920-922: NewAccountModal exists and opens -- VERIFIED

---

## EXECUTION ORDER

1. Edit ProDash sidebar (TRK-402 compact bar)
2. Edit RIIMO sidebar (TRK-402 compact bar)
3. Edit SENTINEL sidebar (TRK-402 compact bar)
4. Edit AdminPanel.tsx (TRK-411 label rename)
5. Edit PortalSwitcher.tsx (TRK-422 three gears + TRK-423 remove footer)
6. Read verify-only files
7. Run `npm run build`
8. Fix any build errors
9. Report results
