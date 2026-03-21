# BUILDER 04 — Sprint 10 API Wiring Plan

## Status: READY TO EXECUTE

All files have been read. All patterns confirmed. Four tasks below.

---

## TRK-403 — Wire Calendar API

### Step 1: Create `services/api/src/lib/calendar-client.ts`
- New file using `google.auth.GoogleAuth` from `googleapis` (matching existing `drive-client.ts` pattern — NOT `google-auth-library`)
- Exports: `getCalendarEvents(userEmail)`, `createInstantMeeting(userEmail)`
- Uses service account with domain-wide delegation to read user calendars
- Returns `{ meetings, recordings }` shape matching existing stub contract

### Step 2: Edit `services/api/src/routes/connect.ts`
- Add import for `getCalendarEvents, createInstantMeeting` from `../lib/calendar-client.js`
- Replace the stub `GET /calendar` route (lines 26-33) with live implementation that:
  - Extracts `req.user?.email` (same pattern as `presence` route at line 157)
  - Calls `getCalendarEvents(userEmail)`
  - Returns structured response via `successResponse(data)`
  - Handles errors via `errorResponse()`

---

## TRK-404 — Wire Quick Meet

### Edit `services/api/src/routes/connect.ts`
- Add `POST /meet` route AFTER the calendar GET route (after line 33 replacement)
- Calls `createInstantMeeting(userEmail)`
- Returns `{ meetLink, eventId }` via `successResponse(data)`

---

## TRK-397 — AI3 invalid_grant Error Handling

### Edit `services/api/src/routes/ai3.ts`
- Two catch blocks to modify:
  1. Household route catch (lines 147-150)
  2. Client route catch (lines 218-221)
- In each: add `invalid_grant` / `invalid_rapt` detection BEFORE the generic error response
- Pattern: check `(err instanceof Error) && (err.message?.includes('invalid_grant') || err.message?.includes('invalid_rapt'))`
- Returns user-friendly message: "Google session expired. Please sign out and sign back in to refresh your session."

---

## TRK-427 — Content Blocks Search (DEFER)

- Grep confirmed: NO `content_block` or `ContentBlock` references exist in `packages/ui/src/modules/CommsModule/`
- This is a new feature, not a fix. DEFERRED.

---

## Verification

After all edits: run `npm run build 2>&1 | tail -30` to confirm clean build.

## Key Decisions
- Use `google.auth.GoogleAuth` (not `google-auth-library`) to match `drive-client.ts` pattern
- Use `.js` extension in import path (NodeNext module resolution requires it)
- Cast auth client properly to avoid `any` types
- Use existing `successResponse`/`errorResponse` helpers (not raw `res.json`)
