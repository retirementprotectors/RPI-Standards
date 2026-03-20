# Sprint 9 Pre-Production — Implementation Plan

> **Sprint ID:** `nps9wSwgKumZSHBrULvV`
> **Discovery:** `.claude/sprint9-preprod/DISCOVERY.md`
> **27 tickets** | 5 builders | WP2 deferred | WP9 manual

## Context

ProDashX is in beta. The UI is shipped but 5 modules run on mock data. This sprint wires them to real APIs/Firestore, fixes 3 entitlement bugs, makes both FABs draggable, and adds FORGE Reporter enhancements. No new UI pages except the Intake Queue Viewer admin page.

---

## Builder Assignments

### BUILDER 01: BugFixes (WP1) — Size: S

**Tickets:** TRK-13546, TRK-13547, TRK-13548

| File | Action |
|------|--------|
| `packages/core/src/users/modules.ts` | Add `PRODASH_HOUSEHOLDS` module def after PROZONE (~line 458). Add to `TOOL_SUITES.RPI_TOOLS.modules` array (~line 108). |
| `packages/ui/src/modules/AdminPanel.tsx` | Fix `usersWithAccess` filter (~line 284): add `if ((u.level ?? 3) === 0) return true` before perms check. Show "Super Admin" badge when level===0 in user row (~line 362). |
| Firestore script (inline npx tsx) | Set `module_permissions` to ALL module keys with `['VIEW','EDIT','ADD']` for josh@ and john@. |

**Module def pattern:**
```typescript
PRODASH_HOUSEHOLDS: {
  name: 'Households',
  fullName: 'Household Management',
  description: 'Household grouping and family unit management',
  status: 'active',
  suite: 'RPI_TOOLS',
  minUserLevel: 'USER',
},
```

---

### BUILDER 02: FABs + Intake + FORGE (WP3 + WP5 + WP6) — Size: L

**Tickets:** TRK-13551, TRK-13552, TRK-13553, TRK-13558, TRK-13559, TRK-13560, TRK-13561, TRK-13562, TRK-13563

| File | Action |
|------|--------|
| **NEW** `packages/ui/src/components/DraggableFAB.tsx` | Shared wrapper. Pointer-event drag (mouse+touch). Save position to Firestore `users/{email}.employee_profile.fab_positions.{fabId}`. Load on mount, snap to viewport edges, fall back to `defaultPosition` prop. |
| `packages/ui/src/components/ReportButton.tsx` | Remove `fixed bottom-6 right-24` (~line 346). Wrap in `<DraggableFAB fabId="forge-reporter">`. Add `badgeCount` state from `/api/tracker?status=queue&created_by={email}` on mount + 30s interval. Long-press handler opens My Reports popover (last 5 items). |
| `apps/prodash/.../IntakeFAB.tsx` → move to `packages/ui/src/components/IntakeFAB.tsx` | Wire `handleFileSelect` (~line 201): replace toast with `fetchWithAuth('/api/dropzone', { POST file })`. Remove fixed positioning. Wrap in `<DraggableFAB fabId="intake-fab">`. |
| `apps/prodash/.../layout.tsx` | Update IntakeFAB import to `@tomachina/ui`. |
| **NEW** `packages/ui/src/modules/IntakeQueue.tsx` | Firestore query on `intake_queue`. Table: file_name, source, status, created_at. Filter pills. Row click detail panel. Approve/Reject/Skip buttons. |
| **NEW** `apps/prodash/.../admin/intake-queue/page.tsx` | Mount `<IntakeQueue />`. |
| `services/intake/src/commission-intake.ts` | Line 95: `'SPC_INTAKE'` → `'COMMISSION_INTAKE'`. |
| `services/api/src/routes/tracker.ts` | After Firestore set (~line 362): Slack POST to `U09BBHTN8F2` with itemId, title, type, portal. Non-blocking. |

**DraggableFAB interface:**
```typescript
interface DraggableFABProps {
  fabId: string
  defaultPosition: { bottom: number; right: number }
  children: React.ReactNode
}
```

---

### BUILDER 03: MyRPI + Dropzone API (WP4) — Size: M

**Tickets:** TRK-13554, TRK-13555, TRK-13556, TRK-13557

| File | Action |
|------|--------|
| `packages/ui/src/modules/MyRpiProfile.tsx` | **Audio** (~line 477): Replace `setSubmitted(true)` with fetchWithAuth POST to `/api/dropzone` with blob + source `MYRPI_AUDIO`. **Camera** (~line 651): Same, source `MYRPI_DOCUMENT`, canvas→JPEG. **Processing Status** (~lines 770-819): Delete `MOCK_SUBMISSIONS`. Add `useCollection` on `intake_queue` where `created_by == email`. **Agent Status** (~lines 926-980): Delete entire section. |
| **NEW** `services/api/src/routes/dropzone.ts` | `POST /api/dropzone` — multipart file + source field. Upload to Drive. Create `intake_queue` entry: `{ file_id, file_name, source, status: 'pending', created_by }`. Return `{ queue_id, file_id }`. |
| `services/api/src/server.ts` | Register: `import { dropzoneRoutes }` + `app.use('/api/dropzone', requireAuth, dropzoneRoutes)`. |

---

### BUILDER 04: Communications (WP8) — Size: L

**Tickets:** TRK-13568, TRK-13569, TRK-13570, TRK-13571, TRK-13572

| File | Action |
|------|--------|
| `packages/ui/src/modules/CommsModule/CommsCompose.tsx` | **SMS** (~line 409): Replace stub with `fetchWithAuth('/api/comms/send-sms', { to, body, client_id })`. **Email** (~line 418): Replace with `/api/comms/send-email` call. **Call** (~line 427): Replace with `/api/comms/send-voice` call. **Client picker** (~line 37): Replace `MOCK_CLIENTS` with real `/api/clients?search=` type-ahead. |
| `packages/ui/src/modules/CommsModule/CommsFeed.tsx` | Delete `MOCK_COMMS` (~lines 36-57). Add `useCollection` on `communications`, `orderBy('created_at','desc')`, limit 50. Map fields: `channel→type`, `recipient→contactName`. |
| `packages/ui/src/modules/CommsModule/InboundCallCard.tsx` | Delete `MOCK_INBOUND_CALL` export. Render nothing when `call={null}`. |
| `apps/prodash/.../TopBar.tsx` | Remove MOCK_INBOUND_CALL import. Pass `call={null}`. |

**Existing API endpoints** (comms.ts — already built, just need UI wiring):
- `POST /api/comms/send-sms` → Twilio, logs to `communications`
- `POST /api/comms/send-email` → SendGrid, logs to `communications`
- `POST /api/comms/send-voice` → Twilio Voice, logs to `communications`
- `POST /api/comms/log-call` → manual log to `communications`

---

### BUILDER 05: RPI Connect (WP7) — Size: M

**Tickets:** TRK-13564, TRK-13565, TRK-13566, TRK-13567

| File | Action |
|------|--------|
| `packages/ui/src/modules/ConnectPanel.tsx` | **People**: Delete `TEAM_MEMBERS` mock (~lines 49-57). `useCollection` on `users` where `status=='active'`. Presence from `last_active` field (<5min online, 5-30min away, 30+ offline). Mount `useEffect` to update current user's `last_active`. **Meet**: Delete mocks (~lines 67-77). Fetch `/api/connect/calendar`. **Channels**: Delete mock (~lines 59-65). Query `connect_channels` collection. Wire new channel form to POST. |
| **NEW** `services/api/src/routes/connect.ts` | `GET /api/connect/calendar` — Google Calendar API proxy. `POST/GET /api/connect/channels` — CRUD on `connect_channels`. `POST /api/connect/presence` — update `last_active`. |
| `firestore.rules` | Add `connect_channels` with `isRPIUser()` gate. |

**Note:** server.ts registration added by planner during merge (avoids conflict with B03).

---

## File Ownership (Zero Overlaps)

| File | B01 | B02 | B03 | B04 | B05 |
|------|-----|-----|-----|-----|-----|
| modules.ts | X | | | | |
| AdminPanel.tsx | X | | | | |
| DraggableFAB.tsx (new) | | X | | | |
| ReportButton.tsx | | X | | | |
| IntakeFAB.tsx (move) | | X | | | |
| IntakeQueue.tsx (new) | | X | | | |
| intake-queue/page.tsx (new) | | X | | | |
| layout.tsx | | X | | | |
| commission-intake.ts | | X | | | |
| tracker.ts | | X | | | |
| MyRpiProfile.tsx | | | X | | |
| dropzone.ts (new) | | | X | | |
| server.ts | | | X | | |
| CommsCompose.tsx | | | | X | |
| CommsFeed.tsx | | | | X | |
| InboundCallCard.tsx | | | | X | |
| TopBar.tsx | | | | X | |
| ConnectPanel.tsx | | | | | X |
| connect.ts (new) | | | | | X |
| firestore.rules | | | | | X |

---

## Execution Timeline

```
Phase 1: B01 (BugFixes)         ██████ MERGE → main
Phase 2: B02-B05 in parallel    ██████████████████████████
Phase 3: Planner merges all     ██████ + server.ts fixup + type-check
Phase 4: WP9 (A2P manual)      ██████
```

---

## Verification

- [ ] `npm run type-check` passes 13/13
- [ ] Households in sidebar for entitled users
- [ ] OWNER in Permissions Audit with "Super Admin" badge
- [ ] Both FABs draggable, positions persist across reload
- [ ] FORGE badge shows pending count, long-press shows My Reports
- [ ] FORGE submit → Slack DM to JDM
- [ ] MyRPI audio/camera submit → real `intake_queue` entry
- [ ] MyRPI Processing Status → real queue items (or empty)
- [ ] MyRPI Agent Status section gone
- [ ] IntakeFAB Upload → real file upload (no "Sprint 11" toast)
- [ ] Commission intake source = `COMMISSION_INTAKE`
- [ ] Intake Queue Viewer → real items, approve/reject works
- [ ] Comms SMS/Email/Call → real API calls (check Twilio/SendGrid)
- [ ] Comms Log tab → real Firestore `communications` entries
- [ ] No fake "Jane Doe" inbound call
- [ ] Connect People → real Firestore users with presence
- [ ] Connect Meet → real calendar events
- [ ] Connect Channels → Firestore `connect_channels`
- [ ] A2P resubmitted with DBA + compliant opt-in page
