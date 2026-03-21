# Builder 02 — Sprint 10: Grids, DeDup, Contact Detail, Access Center

## Branch: `sprint10/builder-02-grids`

---

## TRK-394 — DeDup ID parsing fix
**Status: BUILD**
**File:** `apps/prodash/app/(portal)/ddup/page.tsx` line 277

**Current code (line 277):**
```ts
if (type === 'account' && (id.includes('::') || id.includes('-'))) {
```
**Change to:**
```ts
if (type === 'account' && id.includes('::')) {
```

**Current code (line 278):**
```ts
const sep = id.includes('::') ? '::' : '-'
```
**Change to:**
```ts
const sep = '::'
```

**Rationale:** The `-` fallback was matching ALL UUIDs (which contain hyphens), breaking account ID parsing. `::` is the ONLY valid composite separator.

---

## TRK-395 — Access Center Client Lookup
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/service-centers/access/page.tsx` lines 63-138

**Findings:**
1. Name search title-cases input correctly at line 100: `q.charAt(0).toUpperCase() + q.slice(1).toLowerCase()`
2. Search results render correctly in `ClientSearch` component (lines 192-216) — button for each result, shows name/status/location/email
3. Page mounts correctly — `Suspense` wrapper present, all imports valid, hooks used properly
4. Three-strategy search is correct: email (exact match), phone (prefix match), name (last_name + first_name prefix with title-casing)

**Verdict:** Frontend logic verified — if still broken, likely Firestore index or data issue (Builder 04 Day 2).

---

## TRK-396 — Quick Intake paste/upload
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/intake/page.tsx` lines 50-72 AND `packages/ui/src/components/IntakeFAB.tsx`

**Findings:**
1. `intake/page.tsx` correctly reads `?prefill=<encoded JSON>` and applies to form (lines 50-72)
2. `IntakeFAB.tsx` (line 247) correctly encodes: `const prefill = encodeURIComponent(JSON.stringify(parsed))`
3. `IntakeFAB.tsx` (line 254) correctly navigates: `router.push('/intake?prefill=${prefill}')`
4. The paste parsing is comprehensive — supports key-value, tab-delimited, CSV, and heuristic strategies

**Verdict:** VERIFIED — IntakeFAB correctly encodes and passes prefill data. The flow is: paste text -> parse -> encode JSON -> navigate to `/intake?prefill=...` -> intake page reads and populates form.

---

## TRK-399 — agent_name empty
**Status: VERIFY/DATA_ISSUE**
**File:** `apps/prodash/app/(portal)/contacts/page.tsx` lines 122-136

**Findings:**
The resolution chain is correct (lines 124-134):
1. `assigned_user_id` -> look up in `userMap` (UUID-keyed)
2. `agent_id` (legacy) -> look up in `userMap` (UUID-keyed)
3. `agent_id` (legacy) -> look up in `userDocIdMap` (email-keyed)
4. Fall back to `agent_name` raw field

The code is correct. If agent_name is still showing empty, the issue is that:
- Client docs have empty `assigned_user_id`, `agent_id`, AND `agent_name` fields
- Or the user docs don't have matching `user_id` values

**Verdict:** DATA_ISSUE — fields empty on client docs. Needs Builder 04 backfill script on Day 2.

---

## TRK-401 — 0 ACFs showing
**Status: BUILD**

### File 1: `contacts/page.tsx`
**ACF column (line 693-700):** Uses `ACFStatusIcon` component which receives `client.gdrive_folder_url`. The `ACFStatusIcon` only checks `gdriveFolderUrl` prop — it does NOT check `acf_link` or `acf_url`.

**ACF filter (lines 196-200):** Only checks `c.gdrive_folder_url` — does NOT check `acf_link` or `acf_url`.

**Fix for contacts/page.tsx:**
1. ACF filter (line 197): Change `Boolean(c.gdrive_folder_url)` to `Boolean(c.gdrive_folder_url || c.acf_link || c.acf_url)`
2. ACF filter (line 199): Change `!c.gdrive_folder_url` to `!(c.gdrive_folder_url || c.acf_link || c.acf_url)`
3. ACFStatusIcon prop (line 697): Change `gdriveFolderUrl={client.gdrive_folder_url ? String(client.gdrive_folder_url) : null}` to pass the first truthy value from all 3 fields

Also need to add `acf_link` and `acf_url` to the `ClientRow` interface (around line 63).

### File 2: `contacts/[id]/components/ClientHeader.tsx`
**ACF link (line 50):** Only checks `client.acf_link` — does NOT check `gdrive_folder_url` or `acf_url`.

**Fix:** Change line 50 from:
```ts
const acfLink = client.acf_link as string | undefined
```
to:
```ts
const acfLink = (client.gdrive_folder_url || client.acf_link || client.acf_url) as string | undefined
```

---

## TRK-407 — Remove Business column from Contacts grid
**Status: BUILD**
**File:** `apps/prodash/app/(portal)/contacts/page.tsx`

### Changes needed:
1. **SortKey type (line 49):** Remove `'book_of_business'` from union
2. **Column header (line 488):** Remove `{col('book') && renderSortHeader('Book', 'book_of_business')}`
3. **Sort logic (lines 223-225):** Remove the `case 'book_of_business':` block
4. **Grouped row rendering (line 553):** Remove `{col('book') && (<td ...>...</td>)}`
5. **Flat row rendering (lines 647-655):** Remove the entire `{col('book') && ...}` block
6. **visibleColCount (line 275):** Remove `'book'` from the toggleable array
7. **Filter-related code:** Remove `bookFilter` state, `handleBookChange`, and book filter from `ClientFilters` props. Actually — looking more carefully, the `bookFilter` and its state/handler remain useful for filtering even if the column is hidden. But the instructions say to remove the column. I'll remove the column but keep the filter dropdown (the filter is separate from the column visibility).

Wait, the instructions say "Remove it from: 1. The column definitions array, 2. The default visible columns set, 3. The header rendering, 4. The row cell rendering."

The column definitions are in `ColumnSelector.tsx` (line 20): `{ key: 'book', label: 'Book', defaultVisible: true }`. I need to remove this entry.

### ColumnSelector.tsx changes:
- Remove `{ key: 'book', label: 'Book', defaultVisible: true }` from `ALL_COLUMNS` array

### contacts/page.tsx changes:
- Remove `{col('book') && renderSortHeader('Book', 'book_of_business')}` from header
- Remove `case 'book_of_business':` from sort switch
- Remove `'book_of_business'` from SortKey union type
- Remove `{col('book') && ...}` from both flat and grouped row rendering
- Remove `'book'` from `visibleColCount` toggleable array

**Note:** Keep `bookFilter` state and `books` extraction — the filter dropdown can remain even without the column visible.

---

## TRK-418 — Move ACF column closer to Status
**Status: BUILD**
**File:** `apps/prodash/app/(portal)/contacts/page.tsx` AND `contacts/components/ColumnSelector.tsx`

Current column order in ColumnSelector.tsx:
```
name, location, phone, email, book, agent, status, household, acf, age, dob, ...
```

After removing 'book' and moving ACF after Status:
```
name, location, phone, email, agent, status, acf, household, age, dob, ...
```

### ColumnSelector.tsx changes:
Reorder `ALL_COLUMNS` array: move `acf` entry to be right after `status` (before `household`).

### contacts/page.tsx changes:
Reorder header `<th>` elements and row `<td>` elements so ACF comes after Status and before Household. Both in the grouped rendering and flat rendering sections.

---

## TRK-419 — MyRPI label on browser tab only
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/contacts/[id]/page.tsx` and `ClientHeader.tsx`

**Findings:**
- Searched for "MyRPI" across the entire prodash app — only found in `apps/prodash/app/(portal)/myrpi/page.tsx` (which is a different page entirely)
- The contact detail page (`contacts/[id]/page.tsx`) has no "MyRPI" heading or label in its body
- `ClientHeader.tsx` shows the client's name as `<h1>`, no "MyRPI" label
- The browser tab title would come from the page's metadata or layout, not visible in these files

**Verdict:** VERIFIED — No "MyRPI" heading appears on the contact detail page body. The only "MyRPI" reference is in the separate `/myrpi/` route. If there's a visible "MyRPI" label, it's coming from the sidebar navigation, not this page.

---

## TRK-420 + TRK-421 — DeDup row links
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/ddup/page.tsx` lines 729-776

**Findings:**
- Lines 729-776 are the `<thead>` section with column headers for each record
- **Client type (line 735-741):** Row 1 links to `/contacts/${rec.id}` — CORRECT
- **Account type (line 744-752):** Row 1 links to `/contacts/${parentClientId}` — links to parent client, which is reasonable
- **ACF link (lines 760-773):** Row 2 shows ACF folder link using `gdrive_folder_url || acf_link || acf_url` from client doc (or parent client for accounts) — CORRECT

For account type, the link goes to the parent client detail page. The account ID isn't being used for a direct account link like `/accounts/{clientId}/{accountId}`. However, the instructions say "Row 1 = link to `/accounts/{clientId}/{accountId}`" for account type.

Actually, looking more closely at lines 744-752, for account type it links to `/contacts/${parentClientId}` which is the parent client. The task says it should link to `/accounts/{clientId}/{accountId}`. Let me check what the account detail page URL structure looks like.

Actually, looking at the record structure: for account comparisons, each `rec` has `rec.path = clients/{clientId}/accounts/{accountId}` and `rec.id = accountId`. The `parentClientId` is extracted from the path. The current link goes to `/contacts/${parentClientId}` which shows the client, not the specific account.

**Fix needed for account type:** The route `/accounts/{clientId}/{accountId}` exists at `apps/prodash/app/(portal)/accounts/[clientId]/[accountId]/page.tsx`.

Change line 746-750 from:
```tsx
<a href={`/contacts/${parentClientId}`} ...>
```
to:
```tsx
<a href={`/accounts/${parentClientId}/${rec.id}`} ...>
```

- Row 2 (ACF link): Already correct — checks all 3 fields via `gdrive_folder_url || acf_link || acf_url`

---

## TRK-429 + TRK-430 — Access Center title
**Status: BUILD**
**File:** `apps/prodash/app/(portal)/service-centers/access/page.tsx` lines 558-582

**Current header (lines 561-582):** Has back arrow + pending badge but NO `<h1>Access Center</h1>` title. Just a subtitle: "Access items for {clientName}".

**Fix:** Add `<h1 className="text-2xl font-bold text-[var(--text-primary)]">Access Center</h1>` in the header section, between the back arrow line and the subtitle.

---

## TRK-414 — Remove Sprint 10 badge
**Status: BUILD**
**File:** `apps/prodash/app/(portal)/service-centers/access/page.tsx`

**Found at line 412:** In `OAuthIntegrations` component, the toast message says:
```ts
setToastMessage(`OAuth integration for ${serviceName} coming in Sprint 10`)
```

**Fix:** Change to:
```ts
setToastMessage(`OAuth integration for ${serviceName} coming soon`)
```

---

## VERIFY-ONLY TRK-393 — SmartSearch uses `/api/search` path
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/components/SmartSearch.tsx`

**Found at line 150:**
```ts
const url = `/api/search?q=${encodeURIComponent(searchQuery)}&limit=10`
```

**Verdict:** VERIFIED — Uses relative `/api/search` path (proxied through Next.js server-side), NOT `api.tomachina.com`.

---

## VERIFY-ONLY TRK-400 — DeDup filter excludes merged/deleted/terminated
**Status: VERIFY**
**File:** `apps/prodash/app/(portal)/ddup/page.tsx` lines 291-296

**Found at lines 291-296:**
```ts
const clientStatus = str(data.client_status).toLowerCase()
const status = str(data.status).toLowerCase()
const excludeStatuses = ['merged', 'deleted', 'terminated']
if (excludeStatuses.includes(clientStatus) || excludeStatuses.includes(status) || data._merged_into) {
  continue
}
```

**Verdict:** VERIFIED — Correctly filters out merged, deleted, and terminated records, plus any record with `_merged_into` set.

---

## Execution Order

1. Create branch `sprint10/builder-02-grids`
2. Edit `ColumnSelector.tsx` — remove 'book' column, reorder ACF after Status
3. Edit `contacts/page.tsx` — remove Book column refs, reorder ACF after Status, fix ACF 3-field check
4. Edit `ClientHeader.tsx` — fix ACF to check all 3 fields
5. Edit `ddup/page.tsx` — fix ID parsing (remove `-` fallback), fix account links
6. Edit `access/page.tsx` — add h1 title, remove "Sprint 10" text
7. Run `npm run build` to verify
8. Run `npm run type-check` to verify

## Files Modified (Summary)

| File | Changes |
|------|---------|
| `apps/prodash/app/(portal)/contacts/components/ColumnSelector.tsx` | Remove 'book', reorder ACF after status |
| `apps/prodash/app/(portal)/contacts/page.tsx` | Remove book column, reorder ACF, fix ACF 3-field check |
| `apps/prodash/app/(portal)/contacts/[id]/components/ClientHeader.tsx` | ACF: check all 3 fields |
| `apps/prodash/app/(portal)/ddup/page.tsx` | Remove `-` fallback in ID parsing, fix account row links |
| `apps/prodash/app/(portal)/service-centers/access/page.tsx` | Add h1 title, remove "Sprint 10" text |
