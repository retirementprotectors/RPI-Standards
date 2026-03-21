# Sprint 10 Build Plan: Production Polish + Calendar Wiring

**Sprint ID:** `oEShROoQPrTi5xsbIzTR`
**Items:** TRK-393 through TRK-430 (38 items)
**Builders:** 4 parallel, zero file overlap
**Discovery audit:** PASSED 2026-03-20

---

## Context

Sprint 9 shipped Communications + RPI Connect wired to real APIs, but the production API proxy was broken (fixed in PRs #2 and #3). Research reveals **10 of 38 items are already implemented** from Sprint 9 — they just need verification. The remaining 28 items are real code changes across sidebar layout, Calendar API wiring, grid polish, and shared module cleanup.

---

## BUILDER 01: Sidebar + Portal Chrome (11 items)

**Worktree branch:** `sprint10/builder-01-sidebar`
**Files (zero overlap with other builders):**
- `apps/prodash/app/(portal)/components/PortalSidebar.tsx` (lines 493-695: bottom zone)
- `apps/riimo/app/(portal)/components/PortalSidebar.tsx` (equivalent section)
- `apps/sentinel/app/(portal)/components/PortalSidebar.tsx` (equivalent section)
- `packages/ui/src/components/PortalSwitcher.tsx` (128 lines)

### Build (6 items)

**TRK-402 — Compact action bar.** Replace the 4 stacked full-width buttons (Comms at line 554, Connect at line 590, Notifications at line 626, Admin at line 662 in ProDash) with a single `<div className="border-t ... flex items-center justify-around px-2 py-1.5">` containing 4 icon buttons. Each button: 36x36px, `rounded-lg`, same onClick handlers. When expanded (240px sidebar): icon + 10px label below. When collapsed (60px): icon only, vertical stack. Active state: `bg-[rgba(color,0.15)]` + `var(--portal)` color on icon. Notification badge: absolute-positioned red dot with count on bell. Admin stays a `<Link>`, others stay `<button>`. Replicate identically in RIIMO and SENTINEL sidebars.

**TRK-411 — Sidebar label renames.** Verify NAV_SECTIONS in all 3 sidebars. The labels should be: `Workspaces` (not Workspace), `Sales` (not Sales Centers), `Service` (not Service Centers). Also check `AdminPanel.tsx` MODULE_SECTIONS for consistency.

**TRK-422 — Platform switcher three gears.** `PortalSwitcher.tsx` line 70 currently renders `<img src={TOMACHINA_MARK}>` — this IS the three-gear toMachina mark. JDM wants three separate gear icons in portal colors (blue/purple/green) instead of the monochrome PNG, with the current portal's gear highlighted. Replace the `<img>` with three `<span className="material-icons">settings</span>` inline, each styled with the portal theme color, current portal gear is 20px and bright, others are 14px and muted.

**TRK-423 — Remove footer from platform switcher.** Verify `PortalSwitcher.tsx` dropdown has no footer/powered-by text. Remove trailing `border-b` on last item if creating visual clutter. May be verify-only.

**TRK-424 — Apps section collapsible.** ProDash already has `appsExpanded` state + `APPS_EXPANDED_KEY` localStorage + toggle button (line 497-510). Verify RIIMO and SENTINEL have the same pattern. If missing, add it.

**TRK-414 — NOTE:** The access/page.tsx Sprint 10 badge (line 412) is handled by **Builder 02** (who owns that file). Builder 01 has no TRK-414 work.

### Verify-Only (5 items)

| TRK | What to verify | Expected |
|-----|----------------|----------|
| TRK-405 | `accounts/page.tsx` line 446 | `useState('Active')` |
| TRK-406 | `contacts/page.tsx` line 111 | `useState('Active')` |
| TRK-408 | `ClientTabs.tsx` — no Communications tab | Removed Sprint 9 |
| TRK-410 | `ActivityTab.tsx` — filter pills exist | All/Calls/Emails/SMS/Status Changes/Notes |
| TRK-417 | `accounts/page.tsx` line 674 | Opens `NewAccountModal`, not intake |

---

## BUILDER 02: Grids, DeDup, Contact Detail, Access Center (11 items)

**Worktree branch:** `sprint10/builder-02-grids`
**Files (zero overlap with other builders):**
- `apps/prodash/app/(portal)/contacts/page.tsx`
- `apps/prodash/app/(portal)/contacts/[id]/components/ClientHeader.tsx`
- `apps/prodash/app/(portal)/ddup/page.tsx`
- `apps/prodash/app/(portal)/service-centers/access/page.tsx`
- `apps/prodash/app/(portal)/intake/page.tsx`

### Build (9 items)

**TRK-394 — DeDup ID parsing.** `ddup/page.tsx` line 277: Remove the `|| id.includes('-')` fallback. The `::` separator is the only valid format. Change line 277 from `if (type === 'account' && (id.includes('::') || id.includes('-')))` to `if (type === 'account' && id.includes('::'))`. Remove the `const sep = id.includes('::') ? '::' : '-'` ternary on line 278 — hardcode `const sep = '::'`.

**TRK-395 — Access Center lookup.** `access/page.tsx` lines 70-139: Has 3-field search (email exact, phone range, name prefix). Verify Firestore case-sensitivity: name search at line 100 does `q.charAt(0).toUpperCase() + q.slice(1).toLowerCase()` — correct per CLAUDE.md rules. Test by calling the search function with a known client name. If the issue is the page itself (not loading, UI bug), investigate the page mount flow.

**TRK-396 — Quick Intake prefill.** `intake/page.tsx` lines 50-72: Prefill param parses `JSON.parse(decodeURIComponent(searchParams.get('prefill')))`. Check if `IntakeFAB.tsx` (in `packages/ui/src/components/`) correctly encodes the data as `encodeURIComponent(JSON.stringify(data))`. If IntakeFAB doesn't pass prefill, that's the bug.

**TRK-399 — agent_name empty.** The contacts grid resolves agent via `assigned_user_id` → `agent_id` → `agent_name` fallback chain. Check if these fields exist on client docs in Firestore. If `assigned_user_id` is empty across all clients, this is a data migration issue — flag for Builder 04 to write a backfill script.

**TRK-401 — 0 ACFs showing.** The DeDup page checks 3 fields: `gdrive_folder_url || acf_link || acf_url`. Verify the contacts grid and ClientHeader also check all 3 fields (not just `acf_link`). If they only check one, update to check all 3.

**TRK-407 — Remove Business column.** `contacts/page.tsx` line 488: Remove the `book_of_business` column entry from the column definitions and the default visible columns set.

**TRK-418 — Move ACF closer to Status.** `contacts/page.tsx` column order at lines 484-498. Currently ACF is at position 9. Move it to position 8 (right after Status, before Household).

**TRK-419 — MyRPI header on browser tab only.** JDM's feedback: "MyRPI label on window header only, NOT on screen header (don't show location twice)." Ensure the contact detail page doesn't render a visible "MyRPI" label in the page body. It should only appear in the `<title>` tag / browser tab. Check `ClientHeader.tsx` and the page metadata.

**TRK-420 + TRK-421 — DeDup row links.** `ddup/page.tsx` lines 729-776: The `<th>` per record already shows record name as a link (lines 735-755) and ACF link (lines 761-773). Verify both account and client types render correctly. For accounts: Row 1 should link to `/accounts/{clientId}/{accountId}`, Row 2 to ACF folder. For clients: Row 1 links to `/contacts/{clientId}`, Row 2 to ACF. Fix any missing links.

**TRK-429 + TRK-430 — Access Center title.** `access/page.tsx` lines 560-582: Currently shows "Access items for {clientName}" with a back arrow. Add an `<h1>Access Center</h1>` title. Ensure it appears once, not duplicated with the description text.

**TRK-414 (access center badge) — Remove Sprint 10 badge.** `access/page.tsx` line 412: Remove "Sprint 10" from the OAuth toast message text.

### Verify-Only (2 items)

| TRK | What to verify | Expected |
|-----|----------------|----------|
| TRK-393 | SmartSearch uses `/api/search` via proxy | Fixed in PR #3 |
| TRK-400 | `ddup/page.tsx` lines 291-296 filter exists | Excludes merged/deleted/terminated |

---

## BUILDER 03: Shared Modules — Comms + Connect + Admin (10 items)

**Worktree branch:** `sprint10/builder-03-modules`
**Files (zero overlap with other builders):**
- `packages/ui/src/modules/CommsModule/CommsFeed.tsx`
- `packages/ui/src/modules/CommsModule/CommsCompose.tsx`
- `packages/ui/src/modules/ConnectPanel.tsx`
- `packages/ui/src/modules/AdminPanel.tsx`

### Build (7 items)

**TRK-412 — Pill styling.** `CommsFeed.tsx` lines 191-235: Current channel pills use `rounded h-[34px]`. JDM wants taller, less round edges — change to `rounded-md h-[36px]` (taller with rectangular slight rounding, not fully rounded). Apply same to direction pills at lines 210-223.

**TRK-416 — Template management visibility.** `CommsCompose.tsx` lines 873-897: Has dropdown + "Manage Templates" link. The link is small (text-xs, 14px icon). Make it more prominent: increase to `text-sm`, add a border/pill around the button, or surface the template count next to it.

**TRK-409 — Agent display First Last.** `ConnectPanel.tsx` People tab: `displayName` at line 495 already produces "First Last" via `[u.first_name, u.last_name].filter(Boolean).join(' ')`. Check if any `display_name` values contain commas (Last, First format). If so, add: `if (name.includes(',')) { const [last, first] = name.split(',').map(s => s.trim()); return first + ' ' + last; }`.

**TRK-413 — Google Workspace photos.** `ConnectPanel.tsx` PersonCard at line 444: Always renders `InitialsAvatar`. The `TeamMember` interface has `photo_url` (line 29). Update PersonCard: if `member.photo_url` exists, render `<img src={member.photo_url} className="w-9 h-9 rounded-full object-cover" />` instead of `<InitialsAvatar>`.

**TRK-428 — People name only.** `ConnectPanel.tsx` PersonCard: Verify only `member.name` is rendered as text. If `role` or `division` is shown below the name, remove it. Cards should show: photo/initials + name + presence dot + action buttons. Nothing else.

**TRK-415 — Admin Audit Trail cleanup.** `AdminPanel.tsx`: JDM "didn't ask for it, doesn't know what it is." The panel has tabs including `acf-audit`. **Default action: if the tab renders real, populated data → rename to "ACF History" and add a one-line subtitle explaining what it shows. If the tab is empty or shows meaningless/placeholder data → remove the tab entirely.** Do not leave an unexplained tab.

**TRK-414 (shared modules) — Remove Sprint 10 badges.** Remove from:
- `CommsCompose.tsx` line 133: "Sprint 10" badge span
- `CommsCompose.tsx` line 703: "Sprint 10" badge span
- `CommsCompose.tsx` line 742: "Sprint 10" badge span
- `ConnectPanel.tsx` line 255: "Sprint 10" text in channel compose

### Verify-Only (3 items)

| TRK | What to verify | Expected |
|-----|----------------|----------|
| TRK-425 | `CommsModule/index.tsx` lines 16-21 | 4 tabs: Log, Text, Email, Call |
| TRK-426 | `CommsFeed.tsx` lines 162-234 | Channel pills + direction pills + scope dropdown + search |
| TRK-398 | `ConnectPanel.tsx` lines 323-342 | New Channel POST works via proxy |

---

## BUILDER 04: API + Calendar (4 Day 1 items + 2 conditional Day 2 items)

**Worktree branch:** `sprint10/builder-04-api`
**Files (zero overlap with other builders):**
- `services/api/src/routes/connect.ts` (lines 22-33: calendar stub)
- `services/api/src/routes/ai3.ts` (or wherever AI3 is handled)
- New: `services/api/src/lib/calendar-client.ts`

### Build — Day 1 (4 items)

**TRK-403 — Wire Calendar API.** `connect.ts` lines 22-33: Replace the stub. `googleapis` ^171.4.0 is installed. Create `services/api/src/lib/calendar-client.ts`:
1. Initialize `google.calendar('v3')` with service account + domain-wide delegation
2. Accept user email from `req.user.email` (set by auth middleware)
3. Impersonate user: `auth.subject = userEmail`
4. Call `calendar.events.list({ calendarId: 'primary', timeMin: now, timeMax: endOfDay, singleEvents: true, orderBy: 'startTime', conferenceDataVersion: 1 })`
5. Map to `MeetingData` shape: `{ title: event.summary, participants: event.attendees?.map(a => a.displayName || a.email), timeLabel: formatTime(event.start), joinable: Boolean(event.hangoutLink) }`
6. Return `{ success: true, data: { meetings, recordings: [] } }` (recordings is future — Google Meet API separate)

**TRK-404 — Wire Quick Meet.** New route `POST /api/connect/meet` in `connect.ts`:
1. Create Calendar event with `conferenceDataVersion: 1`, `conferenceData: { createRequest: { requestId: uuid(), conferenceSolutionKey: { type: 'hangoutsMeet' } } }`
2. Return `{ success: true, data: { meetLink: event.hangoutLink, eventId: event.id } }`

**TRK-397 — AI3 invalid_grant.** The AI3 route uses Google auth that can expire. Add try/catch around the Google API call. On `invalid_grant` error, return `{ success: false, error: 'Google session expired. Please sign out and sign back in.' }` instead of crashing. The portal should display this as a toast.

**TRK-427 — Content blocks search.** Content blocks are part of C3 campaign engine (`services/api/src/routes/content-blocks.ts`). Check if content blocks are surfaced in CommsCompose. **If the content blocks UI does not exist in the Comms compose flow, mark TRK-427 as `deferred` in Firestore with note "Content blocks not yet surfaced in Comms UI — needs new feature build, not a fix" and move on. Do not build a new feature.**

**TRK-395 and TRK-399 are NOT Day 1 Builder 04 tasks.** Builder 02 owns the investigation for both. If Builder 02 flags a backend issue (missing Firestore index for TRK-395, or empty data needing backfill for TRK-399), Builder 04 picks these up during the **Day 2 audit phase** — not Day 1.

---

## Execution Timeline

| Phase | Builders | What |
|-------|----------|------|
| Day 1 | 4 parallel | All 4 builders launch simultaneously. Zero file overlap means zero merge conflicts. |
| Day 2 | Audit | GA reads all builder reports, runs `npm run build`, validates each TRK item. |
| Day 3 | Ship | Merge all worktrees → main. CI passes. Firebase App Hosting auto-deploys. |

---

## Verification Checklist

### Phase 0 — Bugs
- [ ] SmartSearch returns results (TRK-393)
- [ ] DeDup works from Accounts grid — no UUID false matches (TRK-394)
- [ ] Access Center lookup returns clients (TRK-395)
- [ ] Quick Intake prefill persists data (TRK-396)
- [ ] AI3 shows friendly error on invalid_grant, not console crash (TRK-397)
- [ ] New Channel button works in Connect (TRK-398)
- [ ] agent_name shows on client records (TRK-399)
- [ ] Deleted accounts excluded from dedup (TRK-400)
- [ ] ACF links showing for contacts (TRK-401)

### Phase 1 — Sidebar
- [ ] Compact icon bar renders correctly — expanded + collapsed (TRK-402)
- [ ] Labels: Workspaces, Sales, Service (TRK-411)
- [ ] Platform switcher = three colored gears (TRK-422)
- [ ] No footer on platform switcher (TRK-423)
- [ ] Apps section collapses/expands with persistence (TRK-424)

### Phase 2 — Calendar
- [ ] Calendar events appear in Connect Meet tab (TRK-403)
- [ ] Quick Meet creates real Google Meet link (TRK-404)

### Phase 3 — UI/UX
- [ ] Grids default to Active (TRK-405, TRK-406)
- [ ] Business column gone from Contacts (TRK-407)
- [ ] Communications tab gone from Contact Detail (TRK-408)
- [ ] People tab: First Last, photos, name only (TRK-409, TRK-413, TRK-428)
- [ ] ACF column near Status (TRK-418)
- [ ] DeDup rows: account/client + ACF links (TRK-420, TRK-421)
- [ ] Comms pills less round (TRK-412)
- [ ] Template management prominent (TRK-416)
- [ ] No Sprint 10 badges anywhere (TRK-414)
- [ ] Access Center title correct (TRK-429, TRK-430)
- [ ] + New on Accounts opens Account modal (TRK-417)
- [ ] Activity tab has sub-filters (TRK-410)

### Build Gate
- [ ] `npm run build` passes 11/11
- [ ] `npm run type-check` passes 13/13
- [ ] CI smoke test passes post-deploy

---

## FORGE Artifact Links

| Artifact | Path |
|----------|------|
| Discovery | `.claude/sprint10-production-polish/DISCOVERY.md` |
| Plan | `.claude/sprint10-production-polish/SPRINT_PLAN.md` (this file, copied after approval) |
| HTML Plan | `apps/prodash/public/plans/sprint-10-production-polish-calendar-wiring.html` (generated after approval) |
| Builder 01 prompt | `.claude/sprint10-production-polish/BUILDER_01.md` |
| Builder 02 prompt | `.claude/sprint10-production-polish/BUILDER_02.md` |
| Builder 03 prompt | `.claude/sprint10-production-polish/BUILDER_03.md` |
| Builder 04 prompt | `.claude/sprint10-production-polish/BUILDER_04.md` |
