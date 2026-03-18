# Sprint 4 — Sidebar Overhaul (TRK-044 through TRK-051)

## Context

The sidebar navigation across all 3 portals needs cleanup: label renames, archiving replaced modules, and bringing RIIMO/SENTINEL to feature parity with ProDash's fixed bottom zone (Comms/Connect slide-outs). ProDash is the reference implementation — RIIMO and SENTINEL are structurally behind.

---

## Builder Strategy: 2 Parallel Builders (Worktree Isolation)

| Builder | Scope | Files |
|---------|-------|-------|
| **A** | Shared component + ProDash | `packages/ui/src/components/PortalSwitcher.tsx`, `apps/prodash/.../PortalSidebar.tsx` |
| **B** | RIIMO + SENTINEL | `apps/riimo/.../PortalSidebar.tsx`, `apps/riimo/.../layout.tsx`, `apps/sentinel/.../PortalSidebar.tsx`, `apps/sentinel/.../layout.tsx` |

No file overlap. Run in parallel.

---

## Item-by-Item Changes

### TRK-044: Remove footer from PortalSwitcher popup
**Builder A** | `packages/ui/src/components/PortalSwitcher.tsx`

Delete lines 131-142 — the `{/* Footer — toMachina gear mark */}` block containing the toMachina mark image at the bottom of the dropdown. Keep the `TOMACHINA_MARK` constant (it's also used for fallback mark on line 46).

### TRK-045: Workspace → Workspaces
**Builder A** (ProDash) + **Builder B** (RIIMO, SENTINEL)

String swap `label: 'Workspace'` → `label: 'Workspaces'` in NAV_SECTIONS:
- `apps/prodash/.../PortalSidebar.tsx` line 51
- `apps/riimo/.../PortalSidebar.tsx` line 49
- `apps/sentinel/.../PortalSidebar.tsx` line 49

### TRK-046: Sales Centers → Sales
**Builder A** | ProDash only (RIIMO/SENTINEL don't have this section)

`apps/prodash/.../PortalSidebar.tsx` line 63: `label: 'Sales Centers'` → `label: 'Sales'`

### TRK-047: Service Centers → Service
**Builder A** (ProDash) + **Builder B** (RIIMO, SENTINEL)

String swap `label: 'Service Centers'` → `label: 'Service'` in NAV_SECTIONS:
- `apps/prodash/.../PortalSidebar.tsx` line 76
- `apps/riimo/.../PortalSidebar.tsx` line 62
- `apps/sentinel/.../PortalSidebar.tsx` line 63

### TRK-048: Archive Sales Center static modules
**Builder A** | `apps/prodash/.../PortalSidebar.tsx`

Remove all 4 static items from the `sales-centers` section (lines 67-72):
```
items: [
  // Medicare, Life, Annuity, Advisory — ALL REMOVED
],
```

Set `items: []`. The section stays as a container for dynamic pipeline injection (lines 207-221 append pipelines with `assigned_section: 'sales'`). The existing `filterSections()` on line 142 removes empty sections, so "Sales" only appears when active sales pipelines exist. This is correct behavior.

**No route deletions** — `/sales-centers/medicare`, etc. stay in the filesystem. They just lose their sidebar nav links.

### TRK-049: Fixed bottom sections (Apps/Comms/Connect/Admin) in every portal
**Builder B** | RIIMO + SENTINEL layouts and sidebars

ProDash already has this. RIIMO and SENTINEL need:

**Layout changes** (`apps/{riimo,sentinel}/app/(portal)/layout.tsx`):
Copy the ProDash layout pattern:
1. Add `import { useState, useCallback } from 'react'`
2. Add `import { CommsModule } from '@tomachina/ui/src/modules/CommsModule'`
3. Add `import { ConnectPanel } from '@tomachina/ui/src/modules/ConnectPanel'`
4. Add state: `commsOpen`, `connectOpen`, derived `panelOpen`
5. Add callbacks: `toggleComms`, `closeComms`, `toggleConnect`, `closeConnect`
6. Pass all as props to `<PortalSidebar>`
7. Render `<CommsModule>` and `<ConnectPanel portal="{riimo|sentinel}">` after main content

**Sidebar changes** (`apps/{riimo,sentinel}/.../PortalSidebar.tsx`):
1. Add `PortalSidebarProps` interface (matching ProDash: `onCommsToggle`, `commsOpen`, `onConnectToggle`, `connectOpen`, `panelOpen`)
2. Update function signature from `PortalSidebar()` to `PortalSidebar({ onCommsToggle, commsOpen, ... }: PortalSidebarProps)`
3. Add auto-collapse `useEffect` watching `panelOpen` (copy ProDash lines 277-295)
4. **Replace** Connect `<Link>` (lines 377-405) with toggle `<button>` matching ProDash pattern (lines 552-585)
5. **Add** Communications button (matching ProDash lines 517-550) between Apps section and Connect button
6. Use portal CSS variables for Comms button colors — NOT hardcoded ProDash blue `rgba(74,122,181,...)`. Use `var(--portal)` for the tint.

**Bottom zone order** (all portals, after changes):
```
Apps (collapsible — TRK-050)
Communications (slide-out toggle)
RPI Connect (slide-out toggle)
Admin (link to /admin, conditional)
```

### TRK-050: Apps section collapsible
**Builder A** (ProDash) + **Builder B** (RIIMO, SENTINEL)

Add expand/collapse toggle to the Apps section in all 3 sidebars:

1. New localStorage key: `{portal}-apps-expanded` (e.g., `prodash-apps-expanded`)
2. New state: `const [appsExpanded, setAppsExpanded] = useState(true)` (default expanded)
3. Load saved state in the existing `useEffect` that reads localStorage
4. Convert the "Apps" label from static `<span>` to clickable `<button>` with chevron arrow (matching nav section header pattern)
5. Wrap app items list in `{appsExpanded && ( ... )}`
6. In collapsed sidebar mode: ignore toggle, always show app icons (current behavior)

**ProDash** (lines 474-515): Convert the header div (lines 477-482) to a toggle button. Wrap items (lines 484-513) in conditional.

**RIIMO** (lines 333-375): Same pattern. Header (lines 336-338) → toggle button. Items (lines 340-373) → conditional.

**SENTINEL** (lines 333-375): Identical to RIIMO.

### TRK-051: Comms/Connect = slider, Admin = section
**Fully covered by TRK-049.** After those changes:
- Communications = `<button>` that triggers `onCommsToggle()` → slide-out panel
- RPI Connect = `<button>` that triggers `onConnectToggle()` → slide-out panel
- Admin = `<Link href="/admin">` → navigates to admin page

Already correct in ProDash. RIIMO/SENTINEL get this behavior via TRK-049 changes.

---

## Files Modified (Complete List)

| File | Builder | Items |
|------|---------|-------|
| `packages/ui/src/components/PortalSwitcher.tsx` | A | TRK-044 |
| `apps/prodash/app/(portal)/components/PortalSidebar.tsx` | A | TRK-045, 046, 047, 048, 050 |
| `apps/riimo/app/(portal)/components/PortalSidebar.tsx` | B | TRK-045, 047, 049, 050, 051 |
| `apps/riimo/app/(portal)/layout.tsx` | B | TRK-049 |
| `apps/sentinel/app/(portal)/components/PortalSidebar.tsx` | B | TRK-045, 047, 049, 050, 051 |
| `apps/sentinel/app/(portal)/layout.tsx` | B | TRK-049 |

**No new files created.** All edits to existing files.

---

## Gotchas

1. **Comms button colors**: RIIMO uses `var(--portal)` = `#a78bfa` (purple), SENTINEL = `#40bc58` (green). The Comms button `rgba()` background must use the portal's color, not ProDash's blue.
2. **Pipeline injection**: After removing Sales Center static items, the `section.key === 'sales-centers'` check on ProDash line 208 still works — the section key stays `'sales-centers'` even though the label changes to `'Sales'`.
3. **Connect icon**: ProDash uses `rpi-shield.png` image for Connect. RIIMO/SENTINEL currently use `settings_input_composite` material icon. Keep each portal's existing icon for now.
4. **rpi-shield.png**: Verify this asset exists in RIIMO/SENTINEL `public/` dirs if we want to match ProDash. If not, keep the material icon approach.
5. **Empty Sales section**: With zero static items AND zero sales pipelines, the Sales section disappears entirely (filtered by `section.items.length > 0`). Correct behavior.

---

## Verification

1. `npm run type-check` — must pass 13/13 workspaces
2. `npm run dev` — start all 3 portals
3. **ProDash (localhost:3001)**: Verify sidebar shows "Workspaces", "Sales" (only if pipelines exist), "Service". Apps section has toggle. Comms/Connect open slide-outs. Platform switcher has no footer.
4. **RIIMO (localhost:3002)**: Verify sidebar shows "Workspaces", "Service", "Pipelines". Bottom zone has Apps (collapsible) + Communications + RPI Connect + Admin. Comms/Connect open slide-outs.
5. **SENTINEL (localhost:3003)**: Same as RIIMO verification.
6. Test sidebar auto-collapse when Comms/Connect panels open (all 3 portals).
7. Test Apps section expand/collapse persists across page navigations.
