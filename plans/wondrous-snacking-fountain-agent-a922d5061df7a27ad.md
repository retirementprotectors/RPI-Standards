# BUILDER 03 — Sprint 10 Shared Modules Plan

## Branch: `sprint10/builder-03-modules`

All files read. All changes identified. Ready to execute.

---

## BUILD ITEMS

### TRK-412 — Pill styling (CommsFeed.tsx)
**File:** `packages/ui/src/modules/CommsModule/CommsFeed.tsx`
**Changes:**
- Line 198: Change `rounded h-[34px]` to `rounded-md h-[36px]` (channel pills)
- Line 213: Change `rounded h-[34px]` to `rounded-md h-[36px]` (direction pills)
- Line 228: Change `rounded h-[34px]` to `rounded-md h-[36px]` (scope select)

### TRK-416 — Template management visibility (CommsCompose.tsx)
**File:** `packages/ui/src/modules/CommsModule/CommsCompose.tsx`
**Changes:** Lines 878-884. Current "Manage Templates" link is plain text-xs with a small icon.
- Change text size from implicit text-xs to `text-sm`
- Add border/pill styling: `border border-[var(--border-subtle)] rounded-md px-2.5 py-1`
- Show template count: `Manage Templates ({availableTemplates.length})`

### TRK-409 — Agent display First Last (ConnectPanel.tsx)
**File:** `packages/ui/src/modules/ConnectPanel.tsx`
**Changes:** Line 495. Current code uses `display_name` as primary, falling back to `first_name + last_name`. The `display_name` could be "Last, First" format. Add comma detection AFTER the display name is resolved.
- In the `useMemo` at line 493-505, after computing `displayName`, add comma detection:
```typescript
let name = displayName
if (name.includes(',') && !name.includes('@')) {
  const [last, first] = name.split(',').map(s => s.trim())
  if (first && last) name = `${first} ${last}`
}
```
Then use `name` instead of `displayName`.

### TRK-413 — Google Workspace profile photos (ConnectPanel.tsx)
**File:** `packages/ui/src/modules/ConnectPanel.tsx`
**Changes:** In `PersonCard` component (line 444-478), replace the always-rendered `InitialsAvatar` with conditional rendering:
- If `member.photo_url` exists, render an `<img>` with `onError` fallback
- Otherwise render `InitialsAvatar` as before
- Need a state or sibling approach for the fallback. Simplest: use a state `imgError` per card.

### TRK-428 — People name only (ConnectPanel.tsx)
**File:** `packages/ui/src/modules/ConnectPanel.tsx`
**Changes:** In `PersonCard` (lines 444-478):
- Currently renders: initials + name + action buttons.
- Check if `role`, `division`, `title`, or `email` appear as visible text.
- Looking at the current code: Only `member.name` is rendered as text (line 452). No role/division/email visible on the card.
- **RESULT: Already correct. Nothing to change.** The PersonCard only shows photo/initials + name + presence dot + action buttons.

### TRK-415 — Admin Audit Trail cleanup (AdminPanel.tsx)
**File:** `packages/ui/src/modules/AdminPanel.tsx`
**Changes:** Looking at the tab definitions (lines 1398-1403), there's an "ACF Audit" tab at key `acf-audit`. This renders `ACFAuditAdmin` which is a real, functional component for bulk ACF audit and rebuild (read the file — it has real audit/rebuild logic).
- Rename tab label from "ACF Audit" to "ACF History"
- Add subtitle to the tab content area: "History of Active Client File changes"
- Actually wait — re-reading the spec: "If the tab renders real, populated data -> rename to ACF History." The ACFAuditAdmin component is a FUNCTIONAL audit tool (run audit, see results, rebuild). This is NOT an audit trail/history view — it's an admin bulk operations tool. The spec asks about "Audit Trail" or "acf-audit" that shows meaningless data. But this is a real tool.
- Decision: Rename the tab from "ACF Audit" to "ACF History" and add the subtitle as specified.

### TRK-414 — Remove Sprint 10 badges (CommsCompose.tsx + ConnectPanel.tsx)
**File 1:** `packages/ui/src/modules/CommsModule/CommsCompose.tsx`
- Line 133: `<span>` with "Sprint 10" in DialerPad Twilio badge — remove the Sprint 10 span
- Line 703: `<span>` with "Sprint 10" in SMS "From" section — remove
- Line 742: `<span>` with "Sprint 10" in Email "From" section — remove

**File 2:** `packages/ui/src/modules/ConnectPanel.tsx`
- Line 255: Text "Message #{channelName} -- Sprint 10" in compose bar — change to just "Message #{channelName}"
- Also line 397: "Real Google Chat integration in Sprint 10" text in new channel form — remove this text

---

## VERIFY-ONLY ITEMS

### TRK-425 — CommsModule index.tsx tab definitions
**File:** `packages/ui/src/modules/CommsModule/index.tsx`
**Check:** Lines 16-21 define TABS: Log, Text, Email, Call (4 tabs).
**RESULT: VERIFIED** — exactly as expected.

### TRK-426 — CommsFeed.tsx filter elements
**File:** `packages/ui/src/modules/CommsModule/CommsFeed.tsx`
**Check:** Has channel pills (All/SMS/Email/Voice), direction pills (All/In/Out), scope dropdown (All Team/My Communications/etc.), search bar.
**RESULT: VERIFIED** — Lines 162-234 contain all four filter types.

### TRK-398 — ConnectPanel.tsx New Channel POST
**File:** `packages/ui/src/modules/ConnectPanel.tsx`
**Check:** New Channel button calls `POST /api/connect/channels` via `fetchWithAuth`.
**RESULT: VERIFIED** — Lines 330-331: `await fetchWithAuth('/api/connect/channels', { method: 'POST', body: JSON.stringify({ name: trimmed }) })`

---

## Execution Steps

1. Create branch `sprint10/builder-03-modules`
2. Edit CommsFeed.tsx (TRK-412)
3. Edit CommsCompose.tsx (TRK-416, TRK-414)
4. Edit ConnectPanel.tsx (TRK-409, TRK-413, TRK-428, TRK-414)
5. Edit AdminPanel.tsx (TRK-415)
6. Run `npm run build`
7. Run `npm run type-check`
8. Report all items
