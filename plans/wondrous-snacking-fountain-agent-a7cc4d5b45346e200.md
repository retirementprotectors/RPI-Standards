# BUILDER 03 — Sprint 10 Modules Plan

Branch: `sprint10/builder-03-modules`

## Status: READY TO EXECUTE

All files have been read. All edits are identified with exact old/new strings. Awaiting plan mode exit to execute.

---

## BUILD ITEMS

### TRK-412 — Pill styling (CommsFeed.tsx)
**File**: `packages/ui/src/modules/CommsModule/CommsFeed.tsx`

1. **Channel pills** (line 198): Change `rounded h-[34px]` to `rounded-md h-[36px]`
2. **Direction pills** (line 213): Change `rounded h-[34px]` to `rounded-md h-[36px]`
3. **Scope dropdown** (line 228): Change `rounded h-[34px]` to `rounded-md h-[36px]`

### TRK-416 — Template management visibility (CommsCompose.tsx)
**File**: `packages/ui/src/modules/CommsModule/CommsCompose.tsx`

The "Manage Templates" button at line 878-884 currently has:
```
className="flex items-center gap-1 text-xs font-medium text-[var(--portal)] transition-colors hover:brightness-110"
```
Change to:
```
className="flex items-center gap-1 text-sm font-medium text-[var(--portal)] border border-[var(--border-subtle)] rounded-md px-2.5 py-1 transition-colors hover:brightness-110"
```

### TRK-409 — Agent display First Last (ConnectPanel.tsx)
**File**: `packages/ui/src/modules/ConnectPanel.tsx`

In PeopleTab, line 495, after `displayName` is constructed, add comma-detection logic to flip "Last, First" to "First Last":
```typescript
let displayName = u.display_name || [u.first_name, u.last_name].filter(Boolean).join(' ') || u.email || 'Unknown'
if (displayName.includes(',') && !displayName.includes('@')) {
  const parts = displayName.split(',').map(s => s.trim())
  if (parts.length === 2 && parts[0] && parts[1]) displayName = `${parts[1]} ${parts[0]}`
}
```

### TRK-413 — Google Workspace photos (ConnectPanel.tsx)
**File**: `packages/ui/src/modules/ConnectPanel.tsx`

In PersonCard component (line 444), add `useState` for imgError and replace InitialsAvatar with conditional photo/initials rendering.

### TRK-428 — People name only (ConnectPanel.tsx)
**File**: `packages/ui/src/modules/ConnectPanel.tsx`

PersonCard currently shows only name + presence dot + action buttons. No role/division/title/email text visible. **VERIFIED** — already name-only.

### TRK-415 — Admin Audit Trail cleanup (AdminPanel.tsx)
**File**: `packages/ui/src/modules/AdminPanel.tsx`

The "ACF Audit" tab at line 1402 renders `<ACFAuditAdmin>` which appears to be a real component (imported at line 17). This has real data, so:
- Rename tab label from "ACF Audit" to "ACF History"
- The subtitle/description will be handled within the component or via the info banner

### TRK-414 — Remove Sprint 10 badges
**Files**: `CommsCompose.tsx` and `ConnectPanel.tsx`

**CommsCompose.tsx** — 3 occurrences of "Sprint 10":
1. Line 133: `<span className="rounded bg-[var(--bg-surface)] px-1.5 py-0.5 text-[9px] font-medium text-[var(--text-muted)]">Sprint 10</span>` (Twilio dialer badge)
2. Line 703: `<span className="rounded bg-[var(--bg-surface)] px-1.5 py-0.5 text-[9px] font-medium text-[var(--text-muted)]">Sprint 10</span>` (SMS from line)
3. Line 742: `<span className="rounded bg-[var(--bg-surface)] px-1.5 py-0.5 text-[9px] font-medium text-[var(--text-muted)]">Sprint 10</span>` (Email from line)

**ConnectPanel.tsx** — 2 occurrences of "Sprint 10":
1. Line 255: `Message #{channelName} — Sprint 10` (compose bar stub text)
2. Line 397: `Real Google Chat integration in Sprint 10` (new channel form note)
3. Line 695: `Google Calendar integration in Sprint 10` (Meet tab empty state)

## VERIFY-ONLY

- **TRK-425**: `CommsModule/index.tsx` has 4 tabs (Log/Text/Email/Call) — **VERIFIED** (lines 16-21)
- **TRK-426**: `CommsFeed.tsx` has channel pills + direction pills + scope dropdown + search — **VERIFIED** (lines 162-234)
- **TRK-398**: `ConnectPanel.tsx` New Channel calls `POST /api/connect/channels` — **VERIFIED** (line 330-331)

## EXECUTION ORDER

1. TRK-412 (3 edits in CommsFeed.tsx)
2. TRK-416 (1 edit in CommsCompose.tsx)
3. TRK-414 (3 edits in CommsCompose.tsx + 3 edits in ConnectPanel.tsx)
4. TRK-409 (1 edit in ConnectPanel.tsx)
5. TRK-413 (2 edits in ConnectPanel.tsx — add useState import, modify PersonCard)
6. TRK-415 (1 edit in AdminPanel.tsx)
7. Run `npm run build`
8. Fix any build errors
