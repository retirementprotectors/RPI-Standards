# BUILDER 04 — API + Calendar Wiring Plan

## Branch: `sprint10/builder-04-api`

## Summary

4 TRK items. 3 code changes, 1 deferral.

---

## TRK-403 — Wire Connect Calendar to Google Calendar API

**Status: READY TO BUILD**

### What exists
- `services/api/src/routes/connect.ts` — lines 22-33 are a stub returning `{ meetings: [], recordings: [] }`
- `services/api/src/lib/drive-client.ts` — existing pattern using `google.auth.GoogleAuth` from `googleapis` package (NOT separate `google-auth-library` import)
- `googleapis` is in `services/api/package.json` dependencies (v171.4.0) and resolvable from monorepo root

### Plan
1. **Create** `services/api/src/lib/calendar-client.ts`
   - Follow the same auth pattern as `drive-client.ts` (uses `new google.auth.GoogleAuth()` from `googleapis`, NOT separate `GoogleAuth` import from `google-auth-library`)
   - Export `getCalendarEvents(userEmail: string)` — uses domain-wide delegation to impersonate user, fetches today's events
   - Export `createInstantMeeting(userEmail: string)` — creates a 30-min meeting with Google Meet conference
   - Helper `formatEventTime()` for time labels
   - Calendar client singleton pattern matching drive-client.ts

2. **Edit** `services/api/src/routes/connect.ts`
   - Add import for `getCalendarEvents` from `../lib/calendar-client.js`
   - Replace lines 22-33 (the stub GET /calendar handler) with real implementation that:
     - Extracts `userEmail` from `(req as any).user?.email` (matches existing pattern at line 157)
     - Calls `getCalendarEvents(userEmail)`
     - Returns `successResponse(data)` on success
     - Returns `errorResponse(err.message)` on failure

### Key decisions
- Use `google.auth.GoogleAuth` from `googleapis` (matches drive-client.ts), NOT `GoogleAuth` from `google-auth-library`
- Auth uses ADC (Application Default Credentials) with domain-wide delegation — no hardcoded creds
- Read-only scope `calendar.readonly` for listing events
- Full `calendar` scope only for createInstantMeeting
- No `any` types — use `unknown` + type narrowing per code standards
- Use `successResponse` / `errorResponse` from helpers (matches existing pattern)

---

## TRK-404 — Wire Quick Meet

**Status: READY TO BUILD**

### What exists
- No POST /meet route in connect.ts currently

### Plan
1. **Edit** `services/api/src/routes/connect.ts`
   - Add import for `createInstantMeeting` (already imported with TRK-403 work)
   - Add new route: `connectRoutes.post('/meet', ...)`
   - Extract user email, call `createInstantMeeting(userEmail)`, return structured response
   - Place the route after the GET /calendar route (before channels routes)

---

## TRK-397 — AI3 invalid_grant error handling

**Status: READY TO BUILD**

### What exists
- `services/api/src/routes/ai3.ts` — two route handlers:
  1. `GET /api/ai3/household/:householdId` (line 27-151) — catch block at line 147-150
  2. `GET /api/ai3/:clientId` (line 158-222) — catch block at line 219-221
- Both catch blocks just `console.error` + `res.status(500).json(errorResponse(String(err)))`
- No Google API calls in this file — it's purely Firestore reads
- The seed-tracker.ts mentions "AI3 generation throws invalid_grant error. OAuth token expired."

### Analysis
The AI3 routes themselves don't make Google API calls — they read from Firestore. The `invalid_grant` error likely occurs when the frontend's auth token expires and the Firebase Auth middleware rejects the request, or when some downstream service (like PDF generation) hits an OAuth error. However, the task says to wrap "Google API call(s)" in a try/catch with specific error handling.

Since there are no Google API calls in ai3.ts, I'll add the `invalid_grant`/`invalid_rapt` check to both existing catch blocks. If a Firestore operation throws with an auth-related message (unlikely but possible), or if a future Google API call is added, the error will be caught gracefully.

### Plan
1. **Edit** `services/api/src/routes/ai3.ts`
   - In both catch blocks (household route at line 147 and client route at line 219):
     - Type the caught error as `unknown`, narrow to check message
     - Add check: if error message includes `invalid_grant` or `invalid_rapt`, return user-friendly message
     - Otherwise fall through to existing error handling

---

## TRK-427 — Content blocks search

**Status: DEFERRED**

### Finding
- Searched `packages/ui/src/modules/CommsModule/` for `content_block`, `ContentBlock`, `content.block` — **zero matches**
- Content blocks exist only in `C3Manager.tsx` (the campaign engine module), NOT in CommsModule
- `CommsCompose.tsx` has templates (TRK-064) but no content blocks section
- Content blocks are a C3/campaign feature, not yet surfaced in the Communications compose UI

### Resolution
Content blocks UI does not exist in CommsCompose. This is a new feature, not a fix. Will defer the ticket.

---

## Files Modified (Summary)

| File | Action | TRK |
|------|--------|-----|
| `services/api/src/lib/calendar-client.ts` | CREATE | TRK-403 |
| `services/api/src/routes/connect.ts` | EDIT (replace stub + add POST /meet) | TRK-403, TRK-404 |
| `services/api/src/routes/ai3.ts` | EDIT (add error handling in 2 catch blocks) | TRK-397 |

## Build Verification
- `npm run build` — 11/11 workspaces
- `npm run type-check` — 13/13 workspaces
