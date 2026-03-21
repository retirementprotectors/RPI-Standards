# BUILDER 02 — Sprint 10 Grid Fixes Plan

Branch: `sprint10/builder-02-grids`

All files read. Every edit below is exact — old_string / new_string pairs ready for execution.

---

## TRK-394 — DeDup ID parsing (READY)

**File:** `apps/prodash/app/(portal)/ddup/page.tsx`

**Edit 1 (line 277):** Remove hyphen fallback from the composite ID check.
- OLD: `if (type === 'account' && (id.includes('::') || id.includes('-'))) {`
- NEW: `if (type === 'account' && id.includes('::')) {`

**Edit 2 (line 278):** Remove hyphen fallback from separator detection.
- OLD: `const sep = id.includes('::') ? '::' : '-'`
- NEW: `const sep = '::'`

---

## TRK-401 — ACF 3-field check (READY)

### File 1: `apps/prodash/app/(portal)/contacts/page.tsx`

**ACF filter (line 197):** Only checks `gdrive_folder_url`. Needs to check all 3 fields.
- OLD: `result = result.filter((c) => Boolean(c.gdrive_folder_url))`
- NEW: `result = result.filter((c) => Boolean(c.gdrive_folder_url || c.acf_link || c.acf_url))`

**ACF filter negative (line 199):**
- OLD: `result = result.filter((c) => !c.gdrive_folder_url)`
- NEW: `result = result.filter((c) => !(c.gdrive_folder_url || c.acf_link || c.acf_url))`

**ClientRow interface needs acf_link and acf_url fields (around line 63):**
- OLD:
```
  gdrive_folder_url?: string
```
- NEW:
```
  gdrive_folder_url?: string
  acf_link?: string
  acf_url?: string
```

**ACF column cell in flat rows (line 697):** Only checks `gdrive_folder_url`. Need to also check `acf_link` / `acf_url`.
- OLD: `gdriveFolderUrl={client.gdrive_folder_url ? String(client.gdrive_folder_url) : null}`
- NEW: `gdriveFolderUrl={client.gdrive_folder_url ? String(client.gdrive_folder_url) : client.acf_link ? String(client.acf_link) : client.acf_url ? String(client.acf_url) : null}`

**ACF column cell in grouped rows (line 557):** Same issue — only checks `gdrive_folder_url`.
- OLD: `{client.gdrive_folder_url ? <a href={String(client.gdrive_folder_url)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()} className="inline-flex items-center justify-center text-[var(--portal)] hover:brightness-110 transition-colors" title="Open Active Client File"><span className="material-icons-outlined text-[18px]">folder_open</span></a> : dash}`
- NEW: `{(client.gdrive_folder_url || client.acf_link || client.acf_url) ? <a href={String(client.gdrive_folder_url || client.acf_link || client.acf_url)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()} className="inline-flex items-center justify-center text-[var(--portal)] hover:brightness-110 transition-colors" title="Open Active Client File"><span className="material-icons-outlined text-[18px]">folder_open</span></a> : dash}`

### File 2: `apps/prodash/app/(portal)/contacts/[id]/components/ClientHeader.tsx`

**ACF link variable (line 50):** Only checks `acf_link`. Needs to check all 3.
- OLD: `const acfLink = client.acf_link as string | undefined`
- NEW: `const acfLink = (client.acf_link || client.gdrive_folder_url || client.acf_url) as string | undefined`

---

## TRK-407 — Remove Business/Book column (READY)

### File: `apps/prodash/app/(portal)/contacts/page.tsx`

**Remove from SortKey type (line 49):**
- OLD: `type SortKey = 'name' | 'location' | 'book_of_business' | 'agent_name' | 'client_status' | 'household' | null`
- NEW: `type SortKey = 'name' | 'location' | 'agent_name' | 'client_status' | 'household' | null`

**Remove column header (line 488):**
- OLD: `{col('book') && renderSortHeader('Book', 'book_of_business')}`
- NEW: (remove entirely)

**Remove from sort logic (lines 223-225):**
- OLD:
```
        case 'book_of_business':
          av = (a.book_of_business || '').toLowerCase()
          bv = (b.book_of_business || '').toLowerCase()
          break
```
- NEW: (remove entirely)

**Remove grouped row book cell (line 553):**
- OLD: `{col('book') && (<td className="px-3 py-3">{client.book_of_business ? <span className="text-[var(--text-secondary)] text-xs">{String(client.book_of_business)}</span> : dash}</td>)}`
- NEW: (remove entirely)

**Remove flat row book cell (lines 647-655):**
- OLD:
```
                      {/* Book */}
                      {col('book') && (
                        <td className="px-3 py-3">
                          {client.book_of_business ? (
                            <span className="text-[var(--text-secondary)] text-xs">
                              {String(client.book_of_business)}
                            </span>
                          ) : dash}
                        </td>
                      )}
```
- NEW: (remove entirely)

**Remove from visibleColCount toggleable list (line 275):**
- OLD: `const toggleable = ['location', 'phone', 'email', 'book', 'agent', 'status', 'household', 'acf', 'age', 'dob', 'ssn', 'gender', 'marital', 'timezone', 'employment']`
- NEW: `const toggleable = ['location', 'phone', 'email', 'agent', 'status', 'household', 'acf', 'age', 'dob', 'ssn', 'gender', 'marital', 'timezone', 'employment']`

### File: `apps/prodash/app/(portal)/contacts/components/ColumnSelector.tsx`

**Remove Book from ALL_COLUMNS (line 20):**
- OLD: `  { key: 'book', label: 'Book', defaultVisible: true },`
- NEW: (remove entirely)

---

## TRK-418 — Move ACF after Status (READY)

### File: `apps/prodash/app/(portal)/contacts/page.tsx`

**Column headers — move ACF header after Status (lines 490-492):**
Current order: ...agent, status, household, acf...
New order: ...agent, status, acf, household...

- OLD:
```
                  {col('status') && renderSortHeader('Status', 'client_status')}
                  {col('household') && renderSortHeader('Household', 'household')}
                  {col('acf') && renderStaticHeader('ACF', 'text-center')}
```
- NEW:
```
                  {col('status') && renderSortHeader('Status', 'client_status')}
                  {col('acf') && renderStaticHeader('ACF', 'text-center')}
                  {col('household') && renderSortHeader('Household', 'household')}
```

**Flat row cells — move ACF cell after Status cell (lines 668-700):**
Reorder: Status, then ACF, then Household

**Grouped row cells — same reorder (line 555-557):**
Reorder: Status, then ACF, then Household

### File: `apps/prodash/app/(portal)/contacts/components/ColumnSelector.tsx`

**Reorder in ALL_COLUMNS (lines 22-24):**
- OLD:
```
  { key: 'status', label: 'Status', defaultVisible: true },
  { key: 'household', label: 'Household', defaultVisible: true },
  { key: 'acf', label: 'ACF', defaultVisible: true },
```
- NEW:
```
  { key: 'status', label: 'Status', defaultVisible: true },
  { key: 'acf', label: 'ACF', defaultVisible: true },
  { key: 'household', label: 'Household', defaultVisible: true },
```

---

## TRK-420 + TRK-421 — DeDup row links (READY)

**File:** `apps/prodash/app/(portal)/ddup/page.tsx`

The account link at lines 744-752 currently goes to `/contacts/${parentClientId}`. For accounts, it should link to `/accounts/${parentClientId}/${rec.id}` to go to the actual account detail.

- OLD:
```
                        ) : type === 'account' && parentClientId ? (
                          <a
                            href={`/contacts/${parentClientId}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[var(--portal)] hover:underline normal-case"
                          >
                            {recName}
                          </a>
```
- NEW:
```
                        ) : type === 'account' && parentClientId ? (
                          <a
                            href={`/accounts/${parentClientId}/${rec.id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[var(--portal)] hover:underline normal-case"
                          >
                            {recName}
                          </a>
```

ACF link for both types already renders at lines 760-773 (checked). VERIFIED for both client and account types.

---

## TRK-429 + TRK-430 — Access Center title (READY)

**File:** `apps/prodash/app/(portal)/service-centers/access/page.tsx`

**Add h1 title above the description text (after the back arrow, around line 563-575):**
- OLD:
```
          <div>
          <div className="flex items-center gap-2">
            <Link
              href={urlClientId ? `/contacts/${clientId}` : '/service-centers'}
              className="text-[var(--text-muted)] hover:text-[var(--portal)] transition-colors"
            >
              <span className="material-icons-outlined text-[20px]">arrow_back</span>
            </Link>
            {pendingCount > 0 && (
              <span className="rounded-full bg-amber-500 px-2.5 py-0.5 text-xs font-semibold text-white">
                {pendingCount} need attention
              </span>
            )}
          </div>
```
- NEW:
```
          <div>
          <div className="flex items-center gap-2">
            <Link
              href={urlClientId ? `/contacts/${clientId}` : '/service-centers'}
              className="text-[var(--text-muted)] hover:text-[var(--portal)] transition-colors"
            >
              <span className="material-icons-outlined text-[20px]">arrow_back</span>
            </Link>
            <h1 className="text-xl font-semibold text-[var(--text-primary)]">Access Center</h1>
            {pendingCount > 0 && (
              <span className="rounded-full bg-amber-500 px-2.5 py-0.5 text-xs font-semibold text-white">
                {pendingCount} need attention
              </span>
            )}
          </div>
```

---

## TRK-414 — Remove Sprint 10 badge (READY)

**File:** `apps/prodash/app/(portal)/service-centers/access/page.tsx`

**Line 412 area — OAuth toast message:**
- OLD: `setToastMessage(`OAuth integration for ${serviceName} coming in Sprint 10`)`
- NEW: `setToastMessage(`OAuth integration for ${serviceName} coming soon`)`

---

## VERIFY-ONLY Items (Read-Only Analysis)

### TRK-393: SmartSearch uses `/api/search` -- VERIFIED
Line 150: `const url = '/api/search?q=${encodeURIComponent(searchQuery)}&limit=10'`
Uses relative `/api/search` path (proxied through portal), NOT `api.tomachina.com`. PASS.

### TRK-400: DeDup merged/deleted/terminated filter -- VERIFIED
Lines 291-296 in `ddup/page.tsx`:
```javascript
const clientStatus = str(data.client_status).toLowerCase()
const status = str(data.status).toLowerCase()
const excludeStatuses = ['merged', 'deleted', 'terminated']
if (excludeStatuses.includes(clientStatus) || excludeStatuses.includes(status) || data._merged_into) {
  continue
}
```
PASS.

### TRK-395: Frontend search logic
Frontend search logic verified -- 3-field search with case normalization (SmartSearch lines 52-87). If still broken, Firestore index or data issue for Day 2. PASS (frontend OK).

### TRK-396: Intake prefill param flow -- VERIFIED
- `IntakeFAB.tsx` line 254: `router.push('/intake?prefill=${prefill}')`
- `intake/page.tsx` lines 50-72: Reads `searchParams.get('prefill')`, JSON.parse, maps to form fields.
Complete pipeline: FAB paste -> parse -> encode JSON -> query param -> intake page -> decode -> prefill form. PASS.

### TRK-399: agent_name resolution
agent_name resolution chain exists in `contacts/page.tsx` lines 124-136: `assigned_user_id -> agent_id -> userDocIdMap -> raw agent_name`. Empty values = empty data on docs. Needs Day 2 backfill. DATA_ISSUE.

### TRK-419: No "MyRPI" heading in ClientHeader -- VERIFIED
`ClientHeader.tsx` displays `{displayName}` (client name) in h1, never "MyRPI". The page body has no "MyRPI" heading. PASS.

---

## Summary

| Item | Status | Action |
|------|--------|--------|
| TRK-394 | READY | 2 edits in ddup/page.tsx |
| TRK-401 | READY | 5 edits in contacts/page.tsx, 1 edit in ClientHeader.tsx |
| TRK-407 | READY | 6 removals in contacts/page.tsx, 1 removal in ColumnSelector.tsx |
| TRK-418 | READY | 3 reorders in contacts/page.tsx, 1 reorder in ColumnSelector.tsx |
| TRK-420/421 | READY | 1 edit in ddup/page.tsx |
| TRK-429/430 | READY | 1 edit in access/page.tsx |
| TRK-414 | READY | 1 edit in access/page.tsx |
| TRK-393 | VERIFIED | No edit needed |
| TRK-400 | VERIFIED | No edit needed |
| TRK-395 | VERIFIED | Frontend OK, Day 2 data |
| TRK-396 | VERIFIED | No edit needed |
| TRK-399 | DATA_ISSUE | Day 2 backfill |
| TRK-419 | VERIFIED | No edit needed |

After all edits: run `npm run build 2>&1 | tail -30` and fix any errors.
