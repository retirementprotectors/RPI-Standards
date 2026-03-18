# Sprint 9 Remaining — Builder Plan

## Context

JDM reviewed production UI on 2026-03-14 and found the consolidated tracker has **108 total items**. This plan accounts for every single one.

**Source**: `toMachina/.claude/sprint9/CONSOLIDATED_FEEDBACK_TRACKER.md`

---

## Full Reconciliation: 108 Items → 4 Buckets

| Bucket | Count | Action |
|--------|-------|--------|
| **SHIPPED** (verified in live UI) | 36 | Done — no work needed |
| **BUILD NOW** (this sprint) | 47 | 4 parallel builders |
| **SPRINT 10** (features + decisions) | 22 | Deferred — JDM taking decisions to S10 planner |
| **CONFIRMED SHIPPED** (found during code audit) | 3 | AV-1, ConnectPanel rounded-md, AT-3 — remove from open list |

### Every Item Mapped:

**SHIPPED (36):** PS-1, FIX-19, TB-1, FIX-12, RC-1, slide-out, people populating, DD-1, DD-1b, DD-2b, FIX-6, AC-1, AC-2, AC-3, AC-5, AC-6, AC-7, AC-9, FIX-20, CG-2, C3-1, C3-2, CT-1, PT-1, FIX-10, AT-3, CM-1, FIX-15, zero-fixes, AX-5, FIX-16, connected-matching, bulk-sweep, connect-slideout

**NEWLY CONFIRMED SHIPPED (3):** AV-1 (Activity sub-filters exist in code), ConnectPanel already `rounded-md` on internal buttons, AT-3 (accounts `target="_blank"`)

**BUILD NOW (47):**

| # | Tracker ID | Section | Item |
|---|-----------|---------|------|
| 1 | G-1 | Global | Pointer cursor + hover on all clickable elements |
| 2 | NEW | Global | Page title shows Firestore doc ID |
| 3 | NEW | Global | MyRPI page title "Myrpi" → "My RPI" |
| 4 | NEW | Global | URL references "prodashx" somewhere |
| 5 | NEW | MyRPI | "Goes by" raw JSON bracket |
| 6 | NEW | MyRPI | Aliases raw JSON instead of chips |
| 7 | NEW | MyRPI | Shane Parmenter appears twice |
| 8 | RC-2 | RPI Connect | Top-level tab pills still rounded-full |
| 9 | — | RPI Connect | Buttons below pills too rounded |
| 10 | DD-2 | DeDup | Accounts dedup broken in grid |
| 11 | FIX-4 | DeDup | DeDup comparison NO DATA (accounts) |
| 12 | FIX-5 | DeDup | Merged records still showing as duplicates |
| 13 | FIX-21 | DeDup | Merge doesn't handle associated records |
| 14 | NEW | DeDup | First row = link to contact (new tab) |
| 15 | NEW | DeDup | Second row = link to ACF (new window) |
| 16 | AC-4 | Accounts | Counter not real total (500+) |
| 17 | AC-8 | Accounts | Columns/Accounts text not highlight color |
| 18 | AC-10 | Accounts | Remove 500+ green badge |
| 19 | FIX-1 | Accounts | Columns button wrong color |
| 20 | FIX-2 | Accounts | 500+ pill doesn't match contacts counter |
| 21 | FIX-3 | Accounts | Pagination not real Firestore counts |
| 22 | NEW | Accounts | Row click → new tab |
| 23 | NEW | Accounts | Remove Detail pop-out button |
| 24 | NEW | Accounts | "+New" shows contact intake, not account |
| 25 | CG-1 | Contacts | Match accounts grid styling |
| 26 | FIX-7 | Contacts | Lighter gray filter + darker table bg |
| 27 | FIX-17 | Contacts | Same background treatment as accounts |
| 28 | NEW | Contacts | Carol "jane" Groff quotes in name |
| 29 | NEW | Contacts | Row click → new tab |
| 30 | CT-3 | Client360 Connect | Preferred name quotes |
| 31 | FIX-8 | Client360 Connect | BoB dropdown wrong data source |
| 32 | NEW | Client360 Connect | RPI Relationship BoB wrong data |
| 33 | FIX-9 | Client360 Personal | DL fields not 4 on one row |
| 34 | AT-1 | Client360 Accounts | Dedup button partial (accounts) |
| 35 | AT-4 | Client360 Accounts | Chevron arrow repurpose/remove |
| 36 | FIX-11 | Client360 Comms | Call button color mismatch |
| 37 | FIX-22 | Client360 Connected | Yellow highlighting not verified |
| 38 | FIX-23 | Client360 Connected | Green highlighting not verified |
| 39 | NEW | Client360 Connected | Reciprocal connections not created |
| 40 | AX-1 | Access Center | "Carrier / Service" → "Carrier / Product Type" |
| 41 | AX-2 | Access Center | Status "Connected" → "Active" |
| 42 | AX-3 | Access Center | Verify button = ACF auth status |
| 43 | AX-4 | Access Center | Remove portal URL row |
| 44 | AX-6 | Access Center | Medicare.gov → cms.gov |
| 45 | AX-7 | Access Center | SocialSecurity.gov → ssa.gov |
| 46 | AX-9 | Access Center | Add Authorization field per API |
| 47 | NEW | Contacts | Steve Abernathey duplicate (data dedup) |

**SPRINT 10 — FEATURES (9):**
G-2 (smart search), RC-3 (Google Chat), CT-2 (Maps API), CM-2 (Twilio 888), CM-3 (send flow), AV-2 (audit trail), AX-12 (standalone module), AX-13 (OAuth wiring), Comms module wiring

**SPRINT 10 — DECISIONS (6):**
Enrichment strategy, "+New" Contact UX, Client-level docs, Bulk connection interface, Incoming call ring, DeDup merge impact architecture

**SPRINT 10 — BIGGER FEATURES (7):**
MR-1 (MyDropZone build), MR-2 (Meeting Config build), AD-1/AD-2 (Team Config redesign), Google profiles in Connect, AX-8/10/11 (add irs.gov/MasterCard/Carrier Connect APIs), RI-1 (Rapid Intake FAB), AI-1/AI-2/AI-3 (AI3 report tabs — needs PDF_SERVICE), Portal Switcher gear click target, AT-2 (product type doc schema + admin config)

**Math check: 36 shipped + 3 newly confirmed + 47 build now + 9 features + 6 decisions + 7 bigger features = 108** ✅

---

## 4 Builders, Fully Parallel, Zero File Overlap

```
BUILDER 01 — Contacts Grid + TopBar + Grid Styling     (13 items)
BUILDER 02 — Client360 Tabs + DeDup + Connected        (14 items)
BUILDER 03 — Accounts Grid + MyRPI + ConnectPanel       (12 items)
BUILDER 04 — Access Center + Comms Polish               (8 items)
```

---

## BUILDER 01: Contacts Grid + TopBar + Grid Styling (13 items)

**Files**: `TopBar.tsx`, `contacts/page.tsx`, grid CSS shared patterns

| # | ID | Priority | Fix |
|---|-----|----------|-----|
| 1 | NEW BUG | **HIGH** | TopBar `usePageTitle()` shows Firestore doc ID for `/contacts/[id]`. Fix: Add route-to-title mappings, detect ID segments and fall back to parent title ("Contacts"). |
| 2 | NEW BUG | **HIGH** | TopBar shows "Myrpi" for `/myrpi`. Fix: Add `myrpi: 'My RPI'` + `ddup: 'DeDup'` + `service-centers: 'Service Centers'` to titles map. |
| 3 | NEW | **HIGH** | Contacts row click uses `router.push()` (same window). Fix: `window.open('/contacts/${id}', '_blank')`. |
| 4 | NEW BUG | **HIGH** | `Carol "jane" Groff` — preferred name has literal quotes. Fix: In contacts grid name rendering, strip surrounding quotes from `preferred_name`. |
| 5 | NEW BUG | **MED** | URL/branding references "prodashx" — audit and fix any incorrect casing or old references. |
| 6 | CG-1 | **MED** | Contacts grid styling doesn't match accounts. Fix: Align filter area (lighter gray) + table bg (darker) to match accounts pattern. |
| 7 | FIX-7 | **MED** | Lighter gray filter area + darker table background. |
| 8 | FIX-17 | **MED** | Same background treatment as accounts grid. |
| 9 | G-1 | **MED** | Pointer cursor (`cursor-pointer`) + hover highlight on all clickable elements globally. Audit sidebar links, table rows, buttons, logos. |
| 10 | NEW | **LOW** | Steve Abernathey appears twice — likely a data duplicate. Run dedup detection on this contact or document for manual resolution. |
| 11 | — | **LOW** | "Ddup Selected" button → "DeDup Selected" label. |
| 12 | — | **LOW** | Loading text "Loading clients..." → "Loading contacts..." |
| 13 | — | **LOW** | Search placeholder "Search clients..." → "Search contacts..." |

**Verification**:
- `/contacts/[id]` TopBar shows "Contacts"
- `/myrpi` TopBar shows "My RPI"
- Contact row click opens new tab
- No literal quotes in contact names
- Contacts grid styling matches accounts grid
- All clickable elements have pointer cursor
- `npm run type-check` passes 13/13

---

## BUILDER 02: Client360 Tabs + DeDup + Connected (14 items)

**Files**: `ConnectedTab.tsx`, `ContactTab.tsx`, `ClientHeader.tsx`, `PersonalTab.tsx`, `ddup/page.tsx`, `AccountsTab.tsx`

| # | ID | Priority | Fix |
|---|-----|----------|-----|
| 1 | NEW BUG | **HIGH** | Reciprocal connections: `handleLink()` only writes to current client. Fix: Also write mirror connection to the linked person's doc with inverse relationship (e.g., son→father, spouse→spouse). |
| 2 | NEW BUG | **HIGH** | Reciprocal unlink: `handleUnlink()` must also remove from the other person's doc. |
| 3 | FIX-8 + NEW | **HIGH** | BoB dropdown hardcoded with wrong values. Fix: Pull unique `book_of_business` values from clients collection (same pattern as contacts grid filter). |
| 4 | CT-3 + NEW | **HIGH** | Preferred name `"jane"` with literal quotes. Fix: Strip surrounding quotes from `preferred_name` in `ClientHeader.tsx` display logic. |
| 5 | FIX-21 | **HIGH** | DeDup merge marks loser but does NOT move child collections. Fix: After merge, reassign loser's accounts subcollection to winner. Copy `connected_contacts`. Move comms records. |
| 6 | DD-2 | **HIGH** | Accounts dedup broken in grid. Fix: Verify account ID format passed to `/ddup?ids=...&type=account`. The composite `clientId-accountId` format may be wrong. |
| 7 | FIX-4 | **MED** | DeDup comparison shows NO DATA for accounts. Fix URL param parsing for account subcollection paths. |
| 8 | FIX-5 | **MED** | Merged records still showing as duplicates. Fix: Filter `client_status === 'Merged'` from dedup candidate queries. |
| 9 | NEW | **MED** | DeDup first row = clickable link to contact (opens new tab). |
| 10 | NEW | **MED** | DeDup second row = link to ACF for each record (opens new window). |
| 11 | FIX-9 | **MED** | DL fields 2x2 grid instead of 4 on one row. Fix: Ensure `cols={4}` + add `min-w` to prevent responsive wrapping on desktop. |
| 12 | FIX-22 | **MED** | Yellow highlighting for potential matches — verify it triggers. Add test data if needed. Document how matches are detected. |
| 13 | FIX-23 | **MED** | Green highlighting for auto-created — verify it triggers. Document the `created_via` values that trigger it. |
| 14 | AT-4 | **LOW** | Bottom chevron arrow on account cards — repurpose or remove (if row click works, chevron is redundant). |

**Verification**:
- Link person A to person B → both sides have connection
- Unlink → both sides cleared
- BoB dropdown shows real books from data
- No quotes in preferred name display
- DeDup merge moves child collections
- DeDup comparison loads data for both contacts and accounts
- Merged records hidden from dedup candidates
- DeDup has clickable links
- DL fields on one row
- `npm run type-check` passes 13/13

---

## BUILDER 03: Accounts Grid + MyRPI + ConnectPanel (12 items)

**Files**: `accounts/page.tsx`, `MyRpiProfile.tsx`, `ConnectPanel.tsx`

| # | ID | Priority | Fix |
|---|-----|----------|-----|
| 1 | AC-4/FIX-3 | **HIGH** | Accounts counter stuck at 500. Fix: Add `getCountFromServer(collectionGroup(db, 'accounts'))` for true total. Display "Showing X of Y". |
| 2 | NEW BUG | **HIGH** | "+New" on Accounts routes to contact intake form. Fix: Rename to "+New Contact" with tooltip explaining accounts are added from client detail, OR create account intake form. |
| 3 | NEW BUG | **HIGH** | MyRPI aliases/goes-by raw JSON. Fix: Parse `aliases` if stored as JSON string (`typeof === 'string' ? JSON.parse() : aliases`). Display "Goes by" as comma-separated. Render each alias as individual chip. |
| 4 | NEW BUG | **MED** | Shane Parmenter appears twice in MyRPI switcher. Fix: Deduplicate team list by `email` or `user_id`. |
| 5 | NEW | **MED** | Accounts row click should open detail in new tab. Fix: Add `onClick` on `<tr>` → `window.open()`. |
| 6 | NEW | **MED** | Remove "Detail" pop-out button (redundant if row click works). |
| 7 | AC-10/FIX-2 | **MED** | Remove 500+ green pill. Match contacts counter style (plain text). |
| 8 | AC-8/FIX-1 | **MED** | Columns button wrong color + "Columns"/"Accounts" text not in highlight color. Fix: Apply `text-[var(--portal)]` to Columns button text and section headers. |
| 9 | AT-1 | **MED** | Accounts tab dedup button — verify it actually loads data in comparison page (partial fix from DD-2/FIX-4). |
| 10 | RC-2 | **MED** | ConnectPanel top-level tab pills still `rounded-full`. Fix: Change to `rounded-md h-[34px]`. |
| 11 | — | **MED** | ConnectPanel buttons below pills too rounded. Fix: Align with pill styling. |
| 12 | — | **MED** | Google profiles not showing in Connect header — add avatar images next to team member names (even if placeholder/initials). |

**Verification**:
- Accounts shows real total (not "500+")
- "+New" clearly indicates contact creation
- MyRPI aliases display as individual chips
- Shane appears once in dropdown
- Account row click opens new tab
- No "Detail" button column
- Counter styling matches contacts
- Columns button in portal color
- ConnectPanel pills are `rounded-md`
- `npm run type-check` passes 13/13

---

## BUILDER 04: Access Center + Comms Polish (8 items)

**Files**: `AccessTab.tsx`, `service-centers/access/**/*`, `CommsTab.tsx`

| # | ID | Priority | Fix |
|---|-----|----------|-----|
| 1 | AX-1 | **HIGH** | Column header "Carrier / Service" → "Carrier / Product Type". |
| 2 | AX-2 | **HIGH** | Status label "Connected" → "Active" in AccessStatusBadge. |
| 3 | AX-4 | **HIGH** | Remove raw portal URLs from table cells. Keep "Open" button only. |
| 4 | AX-6 | **MED** | APIs tab: "Medicare.gov" → "cms.gov" with "Original Medicare" subheading. |
| 5 | AX-7 | **MED** | APIs tab: "Social Security" → "ssa.gov" with "Social Security" subheading. |
| 6 | AX-9 | **MED** | Add Authorization field per API: Not Started / Sent / On File. |
| 7 | AX-3 | **MED** | Verify button should reflect ACF authorization status (on file → green, not on file → gray). |
| 8 | FIX-11 | **LOW** | Call button color in Comms tab — verify it matches SMS/Email button color (`bg-[var(--portal)]`). Fix if mismatched. |

**Verification**:
- Access tab says "Carrier / Product Type"
- Status shows "Active" not "Connected"
- No raw URLs in table
- APIs tab shows "cms.gov" and "ssa.gov"
- Authorization field visible per API
- Verify button reflects ACF status
- Call button matches other comms buttons
- `npm run type-check` passes 13/13

---

## Execution

1. Write 4 builder prompt files: `toMachina/.claude/sprint9/BUILDER_01.md` through `BUILDER_04.md`
2. Spawn 4 builders in parallel worktrees
3. Each builder: implement, run `npm run type-check`, commit
4. Auditor reviews each diff against plan
5. Merge sequentially into `main`
6. CI passes → Firebase App Hosting auto-deploys

---

## Full Accounting

| Bucket | Count | Items |
|--------|-------|-------|
| SHIPPED | 36 | PS-1, FIX-19, TB-1, FIX-12, RC-1, slide-out, people-populating, DD-1, DD-1b, DD-2b, FIX-6, AC-1, AC-2, AC-3, AC-5, AC-6, AC-7, AC-9, FIX-20, CG-2, C3-1, C3-2, CT-1, PT-1, FIX-10, AT-3, CM-1, FIX-15, zero-fixes, AX-5, FIX-16, connected-matching, bulk-sweep, connect-slideout, connected-section, RPI-connect-slideout |
| NEWLY CONFIRMED SHIPPED | 3 | AV-1 (Activity sub-filters exist), ConnectPanel internal `rounded-md`, AT-3 `target="_blank"` |
| **BUILD NOW (this sprint)** | **47** | See 4 builders above (13 + 14 + 12 + 8) |
| SPRINT 10 FEATURES | 9 | G-2, RC-3, CT-2, CM-2, CM-3, AV-2, AX-12, AX-13, Comms wiring |
| SPRINT 10 DECISIONS | 6 | Enrichment strategy, New Contact UX, Client-level docs, Bulk connection interface, Incoming call ring, DeDup merge architecture |
| SPRINT 10 BIGGER FEATURES | 7 | MR-1, MR-2, AD-1, AD-2, AX-8 (irs.gov), AX-10 (MasterCard), AX-11 (Carrier Connect), RI-1, AI-1/AI-2/AI-3, Portal gear click, AT-2 (doc schema), Google profiles (Connect), Incoming call notifications |
| **TOTAL** | **108** | ✅ Every item accounted for |
