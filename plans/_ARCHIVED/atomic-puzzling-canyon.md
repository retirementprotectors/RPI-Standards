ARCHIVED: Consolidated into tomachina-epic-roadmap.md on 2026-03-13
# Plan: COMMS Center — Shared Module for All Portals

## Context

The team currently uses GHL (GoHighLevel) Lead Connector for daily client communications. The goal is to replace GHL with a native **COMMS Center** shared module that works across all 3 portals (ProDashX, RIIMO, SENTINEL) — same component, CSS variable theming handles branding. Exactly like RPI Connect, AdminPanel, MyRpiProfile.

**Backend is 100% done.** Cloud Run API has send-sms, send-email, send-voice, and communications history endpoints. What's missing is the frontend.

**This is NOT a campaign engine build.** No drips, no templates, no scheduling. Just daily ops: text clients, email clients, log calls.

**Twilio credentials are NOT on Cloud Run yet.** Must deploy env vars to `tm-api` before anything works. Auth Token retrieved from Twilio console: `a04af649d7d36248d1588ff252b6e2df`.

**A2P 10DLC local number (+15155002308) still blocked** — campaign CM62449e...b101 is "In progress" at TCR. Toll-free +18886208587 is the working sender.

---

## Architecture: Shared Module

**Pattern**: Same as `ConnectPanel`, `AdminPanel`, `CamDashboard` — lives in `packages/ui/src/modules/`, exported from index, consumed by all 3 portal apps via wrapper pages.

```
packages/ui/src/modules/CommsCenter.tsx     ← THE shared module
packages/ui/src/modules/comms/              ← Sub-components
  ├── CommsToolbar.tsx                      ← Send SMS | Send Email | Log Call buttons
  ├── CommsTimeline.tsx                     ← Conversation history (replaces current CommsTab guts)
  ├── SendSmsDialog.tsx                     ← SMS compose modal
  ├── SendEmailDialog.tsx                   ← Email compose modal
  └── LogCallDialog.tsx                     ← Call log modal

packages/ui/src/modules/index.ts            ← Add export { CommsCenter }
packages/core/src/api-client.ts             ← Authenticated fetch (shared across portals)
```

**Portal wrappers** (one per portal):
```
apps/prodash/app/(portal)/modules/comms/page.tsx
apps/riimo/app/(portal)/modules/comms/page.tsx
apps/sentinel/app/(portal)/modules/comms/page.tsx
```

**Client360 integration** (ProDashX only — other portals don't have Client360 yet):
- CommsTab imports `CommsTimeline` from the shared module
- CommsToolbar embedded above timeline
- Client data passed as props

---

## Critical Findings

1. **`client_id` not logged by send routes** — `comms.ts` logs `recipient`, `channel`, `status`, `sent_by` but NOT `client_id`. Sent messages won't appear in timeline queries. **Must patch API first.**

2. **Auth required for all API calls** — `requireAuth` middleware demands `Authorization: Bearer <idToken>`. We need a shared `apiFetch()` utility in `packages/core/` that gets the Firebase ID token.

3. **Toast + Modal + Confirm already exist** — `useToast()` wired in all portals, `Modal` in `@tomachina/ui`. No new infrastructure needed.

4. **DNC field inconsistency** — ContactTab writes `dnc_*`, backend reads `dnd_*`. CommsCenter must check both.

5. **Twilio creds not on Cloud Run** — Must deploy TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL to `tm-api`.

---

## Pre-Req: Deploy Env Vars to Cloud Run

Before any COMMS feature works in production:

```bash
gcloud run services update tm-api --region us-central1 --project claude-mcp-484718 \
  --set-env-vars "TWILIO_ACCOUNT_SID=<from Script Properties>" \
  --set-env-vars "TWILIO_AUTH_TOKEN=<from Script Properties>" \
  --set-env-vars "TWILIO_PHONE_NUMBER=<from Script Properties>" \
  --set-env-vars "TWILIO_SMS_NUMBER=<from Script Properties>" \
  --set-env-vars "SENDGRID_API_KEY=<from SendGrid dashboard>" \
  --set-env-vars "SENDGRID_FROM_EMAIL=noreply@retireprotected.com" \
  --set-env-vars "SENDGRID_FROM_NAME=Retirement Protectors"
```

**JDM action needed**: SendGrid API key (check SendGrid dashboard or Twilio Email section).

---

## Files to Modify

### 1. `services/api/src/routes/comms.ts`
- Add `client_id: body.client_id || null` to ALL 6 `logCommunication()` calls (3 dryRun + 3 real send)
- Add new endpoint: `POST /api/comms/log-call` — writes to Firestore `communications` with `{ client_id, channel: 'voice', direction, status: outcome, body: notes, duration, sent_by }`. No Twilio call.

### 2. `packages/ui/src/modules/index.ts`
- Add `export { CommsCenter } from './CommsCenter'`

### 3. `packages/core/src/index.ts`
- Add export for `apiClient` from `./api-client`

### 4. `apps/prodash/app/(portal)/clients/[id]/page.tsx` (line 103-104)
- Change `<CommsTab clientId={id} />` → `<CommsTab client={client!} clientId={id} />`

### 5. `apps/prodash/app/(portal)/clients/[id]/components/tabs/CommsTab.tsx`
- Refactor: import `CommsTimeline` + `CommsToolbar` from `@tomachina/ui`
- Pass `client` to toolbar for DNC checks + contact info
- Keep real-time Firestore listener here, pass `comms` data down

### 6. `apps/prodash/app/(portal)/components/PortalSidebar.tsx`
- Add COMMS Center to nav or app items (if standalone view wanted)

### 7. All 3 portal wrapper pages
- Create `apps/{prodash,riimo,sentinel}/app/(portal)/modules/comms/page.tsx`

---

## Files to Create

### 8. `packages/core/src/api-client.ts` — Authenticated API fetch

Shared utility for all portal apps to call Cloud Run API with Firebase auth.

```typescript
export async function apiFetch<T>(path: string, options?: RequestInit): Promise<ApiResult<T>>
export async function apiPost<T>(path: string, body: Record<string, unknown>): Promise<ApiResult<T>>
export async function apiGet<T>(path: string, params?: Record<string, string>): Promise<ApiResult<T>>
```

Uses `getAuth()` from `firebase/auth` → `currentUser.getIdToken()`.
Reads `NEXT_PUBLIC_API_URL` with fallback to `https://api.tomachina.com`.

### 9. `packages/ui/src/modules/CommsCenter.tsx` — Main shared module

The standalone COMMS view (accessed via `/modules/comms` in any portal).

```typescript
interface CommsCenterProps {
  portal: 'prodashx' | 'riimo' | 'sentinel'
  clientId?: string          // Optional: if provided, scoped to one client
  client?: Client            // Optional: for DNC checks + contact info
}
```

- If `clientId` provided → shows that client's comms (like current CommsTab)
- If no `clientId` → shows all recent comms across all clients (unified inbox view)
- Toolbar + Timeline + Dialogs all rendered here

### 10. `packages/ui/src/modules/comms/CommsToolbar.tsx`

Action bar: **Send SMS** | **Send Email** | **Log Call**

- Material Icons + labels
- DNC enforcement: disabled + tooltip when `dnd_all`/`dnc_all`, `dnd_sms`/`dnc_sms`, `dnd_email`/`dnc_email`
- DNC banner: red banner if any flag set
- Manages dialog open/close state

### 11. `packages/ui/src/modules/comms/CommsTimeline.tsx`

Communication history display (extracted from current CommsTab).

- Channel summary pills
- CommRow items with channel icon, direction, status badge, timestamp, body preview
- Date group headers
- Real-time updates via props (parent manages Firestore listener)

### 12. `packages/ui/src/modules/comms/SendSmsDialog.tsx`

- Recipient: radio buttons for available phone numbers
- Body: `<textarea>` with character counter (green <160, yellow 161-320, red 321+, segment count)
- Send → `apiPost('/api/comms/send-sms', { to, body, client_id })` → toast → close
- Loading state: spinner, inputs disabled

### 13. `packages/ui/src/modules/comms/SendEmailDialog.tsx`

- Recipient: radio buttons for available emails
- Subject: text input
- Body: `<textarea>` (plain text Phase 1)
- Send → `apiPost('/api/comms/send-email', { to, subject, text: body, client_id })` → toast → close

### 14. `packages/ui/src/modules/comms/LogCallDialog.tsx`

- Direction: "Outbound" / "Inbound" radio
- Outcome: Connected, Left Voicemail, No Answer, Busy, Wrong Number
- Duration: optional minutes input
- Notes: `<textarea>`
- Save → `apiPost('/api/comms/log-call', { client_id, direction, outcome, duration, notes })` → toast → close

---

## Data Flow

```
User clicks "Send SMS" → CommsToolbar opens SendSmsDialog
  → User picks recipient, types message
  → DNC check (client-side, instant) — button disabled if blocked
  → apiPost('/api/comms/send-sms', { to, body, client_id })
    → apiFetch gets Firebase ID token via getAuth().currentUser.getIdToken()
    → fetch with Authorization: Bearer <token>
    → API sends via Twilio, logs to Firestore with client_id
  → Toast: "SMS sent" / "Failed: ..."
  → Dialog closes
  → Real-time Firestore listener picks up new doc
  → Timeline updates automatically (no manual refresh)
```

---

## Build Order

| Step | What | Why |
|------|------|-----|
| **0** | Deploy Twilio/SendGrid env vars to Cloud Run | Nothing works without creds |
| **1** | Patch `comms.ts` (client_id + log-call endpoint) | Foundation — sends must link to clients |
| **2** | Create `api-client.ts` in packages/core | Needed by all dialogs, all portals |
| **3** | Create `CommsTimeline` (extract from CommsTab) | Reusable history display |
| **4** | Create `CommsToolbar` + `SendSmsDialog` | Highest value — SMS is GHL killer |
| **5** | Create `CommsCenter` shared module | Wraps toolbar + timeline |
| **6** | Wire into ProDashX CommsTab + portal wrapper | First portal live |
| **7** | Create `SendEmailDialog` | Second channel |
| **8** | Create `LogCallDialog` | Third channel |
| **9** | Wire into RIIMO + SENTINEL wrappers | All 3 portals live |
| **10** | Add to PortalSidebar nav (all portals) | Discoverable in nav |

---

## Verification

1. `npm run build` — full monorepo build passes
2. `npm run dev` — start all 3 portals
3. ProDashX: Clients → pick client → Comms tab → verify toolbar + send works
4. ProDashX: `/modules/comms` → verify standalone view
5. RIIMO: `/modules/comms` → verify same UI, purple branding
6. SENTINEL: `/modules/comms` → verify same UI, green branding
7. Test Send SMS (dryRun) → verify appears in timeline
8. Test Send Email (dryRun) → verify appears in timeline
9. Test Log Call → verify appears in timeline
10. Set `dnd_sms: true` on client → verify SMS button disabled
11. Set `dnd_all: true` → verify all send buttons disabled
12. No `alert()`, `confirm()`, `prompt()` — hookify enforced

---

## Scope Boundary (NOT in this build)

- Campaign enrollment / drip sequences
- Template picker / saved messages
- Inbound SMS display (requires Twilio webhook wiring)
- Rich text email editor
- RPI Connect (internal team chat — separate feature, already exists)
