# Builder C — ProZone Integration Plan (TRK-242)

## Summary

Wire ProZone into all three portals: route page, sidebar registration, brand definition, and CSS variable. ProZone is an **App** (own brand, not portal-themed), following the exact pattern of Pipeline Studio and Forge.

## Current State

- **ProZone component**: Does NOT exist yet in `packages/ui/src/modules/`. Builder B hasn't delivered.
- **AppKey type**: Does NOT include `'prozone'` yet — needs adding to `brands.ts`.
- **APP_BRANDS**: No prozone entry yet.
- **Sidebars**: All 3 portals have APP_ITEMS arrays. ProZone needs to go after `forge` in each.
- **CSS**: All 3 portals have `--app-*` variables section. None have `--app-prozone`.
- **Module export**: `packages/ui/src/modules/index.ts` does NOT export ProZone.

## Files to Create

### 1. ProDash Route Page
**Create**: `apps/prodash/app/(portal)/modules/prozone/page.tsx`
```typescript
import { ProZone, AppWrapper } from '@tomachina/ui'
export default function ProZonePage() {
  return (
    <AppWrapper appKey="prozone">
      <ProZone portal="prodashx" />
    </AppWrapper>
  )
}
```
Pattern: Matches pipeline-studio/page.tsx exactly (no `'use client'`, uses AppWrapper, imports from @tomachina/ui).

### 2. RIIMO Route Page
**Create**: `apps/riimo/app/(portal)/modules/prozone/page.tsx`
```typescript
import { ProZone, AppWrapper } from '@tomachina/ui'
export default function ProZonePage() {
  return (
    <AppWrapper appKey="prozone">
      <ProZone portal="riimo" />
    </AppWrapper>
  )
}
```

### 3. SENTINEL Route Page
**Create**: `apps/sentinel/app/(portal)/modules/prozone/page.tsx`
```typescript
import { ProZone, AppWrapper } from '@tomachina/ui'
export default function ProZonePage() {
  return (
    <AppWrapper appKey="prozone">
      <ProZone portal="sentinel" />
    </AppWrapper>
  )
}
```

## Files to Edit

### 4. App Brand Registration
**Edit**: `packages/ui/src/apps/brands.ts`

Add `'prozone'` to the AppKey union type:
```
export type AppKey = 'atlas' | 'cam' | 'comms' | 'dex' | 'c3' | 'command-center' | 'david-hub' | 'forge' | 'leadership-center' | 'pipeline-studio' | 'pipelines' | 'prozone'
```

Add entry to APP_BRANDS object (after `pipelines`):
```
prozone:             { color: '#0ea5e9', icon: 'explore',     label: 'ProZone',          description: 'Prospecting Hub' },
```
Color `#0ea5e9` (sky-500) as specified. Icon `explore` (globe with compass — fits prospecting/territory).

### 5. ProDash Sidebar
**Edit**: `apps/prodash/app/(portal)/components/PortalSidebar.tsx`

Add to APP_ITEMS array after the forge entry (line 92):
```typescript
  { key: 'prozone', href: '/modules/prozone', moduleKey: 'PROZONE' },
```

### 6. RIIMO Sidebar
**Edit**: `apps/riimo/app/(portal)/components/PortalSidebar.tsx`

Add to APP_ITEMS array after the forge entry (line 92):
```typescript
  { key: 'prozone', href: '/modules/prozone', moduleKey: 'PROZONE' },
```

### 7. SENTINEL Sidebar
**Edit**: `apps/sentinel/app/(portal)/components/PortalSidebar.tsx`

Add to APP_ITEMS array after the forge entry (line 92):
```typescript
  { key: 'prozone', href: '/modules/prozone', moduleKey: 'PROZONE' },
```

### 8. ProDash globals.css
**Edit**: `apps/prodash/app/globals.css`

Add after `--app-cc: #718096;` (line 50):
```css
  --app-prozone: #0ea5e9;
```

### 9. RIIMO globals.css
**Edit**: `apps/riimo/app/globals.css`

Add after `--app-cc: #718096;` (line 46):
```css
  --app-prozone: #0ea5e9;
```

### 10. SENTINEL globals.css
**Edit**: `apps/sentinel/app/globals.css`

Add after `--app-cc: #718096;` (line 46):
```css
  --app-prozone: #0ea5e9;
```

### 11. Module Export (if Builder B hasn't)
**Edit**: `packages/ui/src/modules/index.ts`

Add after the Forge exports:
```typescript
export { ProZone } from './ProZone/ProZone'
```

## Type-check Expectation

The route pages import `ProZone` from `@tomachina/ui`. If Builder B hasn't created the ProZone component yet, `npm run type-check` will fail on the import. The brands.ts and sidebar changes will pass type-check independently.

**If ProZone component doesn't exist yet**: I will still add the module export line and create the pages. The type error will be a clear signal that Builder B's deliverable is needed. The sidebar + brands + CSS changes will all be correct regardless.

## Verification

After all edits:
```bash
cd ~/Projects/toMachina && npm run type-check 2>&1 | tail -20
```

Expected: Pass if Builder B has delivered ProZone component. Fail on import if not.
