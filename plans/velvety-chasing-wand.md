# Sprint 9 — 5-Builder Plan

## Context

Sprint 8 delivered COMMS Center, Access Center (UI shell), DeDup Overhaul, Document Buttons, and a 47-item design polish. Sprint 8 Polish (3 builders) is currently executing grid fixes, Client360 tab restructure, and shared component cleanup.

Sprint 9 brings the platform from "looks great" to "works for real." Five features that turn demo-quality UI into production-grade tools.

**Full punch list source**: `.claude/sprint8/SPRINT8_PUNCHLIST.md` (deferred items)
**JDM decisions**: AI3 = PDF download. MyDropZone = replicate old GAS version (already built, needs data). Search = multi-field. Builders = as many as safely parallel.

---

## Builder 1: Access Center Redesign (MAJOR)

**Branch**: `sprint9/access-center-v2`

### Context
Access Center exists as a UI shell with 100% hardcoded seed data. No Firestore. No API. JDM reviewed it and gave detailed redesign specs — carrier/product type instead of carrier/service, new API providers, authorization tracking separate from connection status.

### Files Owned
- `apps/prodash/app/(portal)/service-centers/access/page.tsx` (rewrite)
- `apps/prodash/app/(portal)/service-centers/access/components/*.tsx` (rewrite all 4)
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/AccessTab.tsx` (update)
- `services/api/src/routes/access.ts` (CREATE — new API route)
- `packages/core/src/types/index.ts` (add AccessItem type)

### Tasks

**AX-1: Carrier/Product Type** — Replace "Carrier / Service" column with "Carrier / Product Type". Athene has separate portals for Life vs Annuity. Each row: carrier name (bold), product type underneath (annuity/life/investment/medicare).

**AX-2: Status values** — Change from Connected/Pending/Expired/Not Started to **Active** (green) / **Pending** (yellow) / **Expired** (red) / **Not Started** (gray). "Active" replaces "Connected".

**AX-3: Verify = 3rd Party Authorization** — "Verify" button on Portals tab becomes authorization status:
- No auth on file → gray "No Auth" label
- Auth on file → green "Auth on File" button, click opens ACF location
- Track `auth_status: 'none' | 'sent' | 'on_file'` + `auth_doc_url` (link to ACF doc)

**AX-4: Remove portal URL row** — The "Open" button handles navigation. Remove the displayed URL text under carrier name.

**AX-5: Only show client's carriers** — Query client's accounts subcollection, extract unique carrier+product_type combos, only show those in the Portals tab. No more hardcoded seed list.

**AX-6 through AX-8: API providers** — Replace current 3 with:
| Provider | URL | Subheading |
|----------|-----|-----------|
| cms.gov | cms.gov | Original Medicare |
| ssa.gov | ssa.gov | Social Security |
| irs.gov | irs.gov | Tax Records |

**AX-9: Authorization field on APIs** — Separate from connection status. Values: `Not Started` / `Sent` / `On File`. This tracks OAuth consent (ID.me for CMS/SSA/IRS). Display as a second status badge per row.

**AX-10: MasterCard API** — Add row: MasterCard API, subheading "Financial and Insurance"

**AX-11: Carrier Connect** — Add rows per MAPD carrier the client has. E.g., "Carrier Connect Aetna" → subheading "MAPD" → "Blue Button Data". Dynamically generated from client's Medicare accounts.

**AX-12: Backend** — Create `services/api/src/routes/access.ts`:
- `GET /api/access/:clientId` — returns access items for client (reads from `clients/{id}/access_items` subcollection + generates dynamic entries from accounts)
- `PUT /api/access/:clientId/:accessId` — update status, auth_status, credentials
- `POST /api/access/:clientId/verify/:accessId` — mark as verified, update last_verified timestamp

**Firestore data model** (`clients/{clientId}/access_items/{accessId}`):
```typescript
interface AccessItem {
  access_id: string
  type: 'api' | 'portal'
  service_name: string
  carrier?: string
  product_type?: string
  category: 'annuity' | 'life' | 'medicare' | 'investment' | 'government' | 'financial'
  subheading?: string
  status: 'active' | 'pending' | 'expired' | 'not_started'
  auth_status: 'none' | 'sent' | 'on_file'
  auth_doc_url?: string
  portal_url?: string
  username?: string
  last_verified?: string
  notes?: string
  created_at: string
  updated_at: string
}
```

### Reference Files (read, don't modify)
- `services/api/src/routes/comms.ts` — pattern for new API routes
- `packages/core/src/types/index.ts` — where to add AccessItem type

---

## Builder 2: AI3 Report (PDF Generation)

**Branch**: `sprint9/ai3-report`

### Context
AI3 = Assets, Income, Insurance, Inventory. The button exists on Client360 header but just spins for 2 seconds. JDM wants a real PDF download — generate report, save to ACF in Drive, download to browser.

### Files Owned
- `apps/prodash/app/(portal)/clients/[id]/components/ClientHeader.tsx` (wire handleAI3)
- `apps/prodash/app/(portal)/clients/[id]/components/AI3Report.tsx` (CREATE)
- `services/api/src/routes/ai3.ts` (CREATE — report data aggregation endpoint)

### Tasks

**AI3 Data Aggregation** — Create `GET /api/ai3/:clientId` that returns all data needed for the report:
```typescript
{
  client: { /* full client record */ },
  accounts: { /* all accounts with subcollections */ },
  connected_contacts: [ /* linked contacts */ ],
  access_items: [ /* from access_items subcollection */ ],
  rmd_data: { /* RMD calculations if applicable */ },
  beni_data: { /* beneficiary info */ },
  generated_at: string,
  generated_by: string
}
```

**AI3 Report Sections** (per JDM spec):
1. **Connect** — contact info, addresses, DNC status
2. **Personal** — demographics, employment, Medicare card, DL
3. **Estate** — beneficiaries, trusts, POA, healthcare proxy
4. **Accounts** — all accounts grouped by type with key fields
5. **Connected** — linked contacts/relationships
6. **Access** — portal/API access status summary
7. **Service Center** — RMD status, Beni Center data

**NOT included**: Comms (has its own section)

**PDF Generation Approach**:
- Build report as a React component (`AI3Report.tsx`) with print-optimized CSS
- Use `@react-pdf/renderer` (or similar) to generate PDF client-side from the aggregated data
- Alternative: call PDF_SERVICE with an HTML-to-PDF endpoint (would need to add that endpoint)
- Simplest production path: render HTML, use `window.print()` with `@media print` styles, plus a dedicated "Download PDF" button that calls a server endpoint

**Recommended**: Use `jspdf` + `html2canvas` for client-side PDF generation. No server dependency. Render the AI3Report component in a hidden div, capture to canvas, output PDF.

**ACF Save**: After PDF is generated, use `apiPost('/api/ai3/save', { clientId, pdfBase64 })` to upload to the client's ACF folder in Drive via gdrive MCP or Drive API.

**Wire handleAI3**: Replace the placeholder spinner with:
1. Fetch data from `/api/ai3/:clientId`
2. Render AI3Report with data
3. Generate PDF
4. Download to browser
5. Upload to ACF in background

### Reference Files
- `services/PDF_SERVICE/index.js` — existing PDF service (fill/merge, not HTML-to-PDF)
- `services/api/src/routes/dex-pipeline.ts` — pattern for calling PDF_SERVICE
- `apps/prodash/app/(portal)/clients/[id]/components/ClientHeader.tsx` — handleAI3 placeholder

---

## Builder 3: Activity Audit Trail

**Branch**: `sprint9/audit-trail`

### Context
ActivityTab UI exists and reads from `clients/{id}/activities` subcollection. But nothing WRITES to it. Need API middleware that auto-logs every client/account mutation with datetime + user stamp.

### Files Owned
- `services/api/src/middleware/audit.ts` (CREATE — audit logging middleware)
- `services/api/src/routes/activities.ts` (CREATE — manual activity logging endpoint)
- `services/api/src/index.ts` (wire middleware)

### Tasks

**Audit Middleware** — Express middleware that intercepts POST/PUT/PATCH/DELETE on client/account routes:
```typescript
function auditMiddleware(req, res, next) {
  // Capture original json method
  const originalJson = res.json.bind(res)
  res.json = (body) => {
    // After successful mutation, log activity
    if (res.statusCode < 400 && ['POST','PUT','PATCH','DELETE'].includes(req.method)) {
      logActivity({
        client_id: req.params.clientId || body?.data?.client_id,
        activity_type: mapMethodToType(req.method), // create/update/delete
        description: buildDescription(req),
        user_email: req.user?.email,
        entity_type: detectEntityType(req.path), // 'client' | 'account' | 'access'
        entity_id: req.params.id || body?.data?.id,
        changes: req.body, // what was changed
      })
    }
    return originalJson(body)
  }
  next()
}
```

**logActivity helper** — writes to both:
1. `clients/{client_id}/activities/{activity_id}` (subcollection — for ActivityTab)
2. `activities/{activity_id}` (top-level — for platform-wide audit queries)

**Activity record shape**:
```typescript
{
  activity_id: string,
  client_id: string,
  activity_type: 'create' | 'update' | 'delete' | 'access_change' | 'status_change',
  entity_type: 'client' | 'account' | 'access' | 'communication',
  entity_id: string,
  description: string, // "Updated client phone from (515) 555-1234 to (515) 555-5678"
  user_email: string,
  changes: Record<string, { old: unknown, new: unknown }>,
  created_at: string
}
```

**Manual logging endpoint** — `POST /api/activities` for logging events that don't go through API mutations (e.g., UI-only actions like "viewed client record"):
```typescript
{ client_id, activity_type, description, entity_type?, entity_id? }
```

**Wire to existing routes** — Apply middleware to:
- `services/api/src/routes/clients.ts`
- `services/api/src/routes/accounts.ts`
- `services/api/src/routes/access.ts` (new from Builder 1)
- `services/api/src/routes/comms.ts` (already logs, but add to audit trail too)

### Reference Files
- `services/api/src/index.ts` — where middleware is registered
- `services/api/src/routes/clients.ts` — existing client mutation routes
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/ActivityTab.tsx` — consumer of this data

---

## Builder 4: Smart Search (TopBar Type-ahead)

**Branch**: `sprint9/smart-search`

### Context
TopBar has a search input that currently redirects to `/clients?q=` on Enter. JDM wants a real-time type-ahead dropdown searching across clients AND accounts by name, email, phone, account number, carrier.

### Files Owned
- `apps/prodash/app/(portal)/components/TopBar.tsx` (replace search input with SmartSearch)
- `apps/prodash/app/(portal)/components/SmartSearch.tsx` (CREATE)
- `services/api/src/routes/search.ts` (CREATE — search endpoint)

### Tasks

**Search API** — `GET /api/search?q=smith&limit=10`:
- Query Firestore `clients` collection:
  - `last_name` prefix match (>= / <)
  - `first_name` prefix match
  - `email` exact or prefix match
  - `phone` contains match
- Query Firestore `accounts` collectionGroup:
  - `account_number` prefix
  - `policy_number` prefix
  - `carrier_name` prefix
- Return unified results: `{ clients: [...], accounts: [...] }`
- Each result: `{ id, type, label, sublabel, href }`

**SmartSearch Component**:
- Replaces current `<input>` in TopBar
- Debounced (300ms) type-ahead
- Dropdown shows grouped results: "Clients" section + "Accounts" section
- Each result row: icon + label + sublabel + click navigates
- Keyboard navigation (up/down arrows, Enter to select)
- Close on blur/Escape
- Min 2 chars before querying
- Loading spinner while fetching

**Existing pattern to follow**: ConnectedTab already has a Firestore smart search with debounce + results dropdown (lines 190-252 of ConnectedTab.tsx). Reuse that pattern.

### Reference Files
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/ConnectedTab.tsx` — smart search pattern
- `services/api/src/routes/booking.ts` — existing `search-clients` endpoint (basic prefix)

---

## Builder 5: MyDropZone Data + Rapid Intake FAB

**Branch**: `sprint9/dropzone-intake`

### Context
MyDropZone UI is ALREADY BUILT in MyRpiProfile.tsx (lines 786-830) — Meet Link, Intake Folder, Booking Pages with QR codes. JDM sees the empty state because Firestore `employee_profile` data isn't populated. This builder populates the data AND builds the Rapid Intake floating action button.

### Files Owned
- `apps/prodash/app/(portal)/components/IntakeFAB.tsx` (CREATE — floating action button)
- `apps/prodash/app/(portal)/layout.tsx` (add IntakeFAB to portal layout)
- `services/api/src/routes/dropzone.ts` (CREATE — MyDropZone config endpoint)

### Tasks

**MyDropZone Data Population**:
- Create `GET /api/dropzone/setup/:userEmail` — returns current employee_profile config
- Create `PUT /api/dropzone/setup` — saves meet_room, booking_slug, drive_folder_url to user's `employee_profile` in Firestore
- Create a setup wizard in MyRpiProfile that guides first-time configuration: enter Meet link → enter Drive folder URL → enter booking slug → save

**Rapid Intake FAB** — Floating action button on all ProDash pages:
- Fixed position bottom-right: lightning bolt icon (`electric_bolt`)
- Click expands to 3 options:
  1. **Quick Client** — navigates to `/intake` (existing form)
  2. **Upload Document** — opens file picker, uploads PDF to client's ACF folder
  3. **Paste Portal Data** — opens modal with textarea to paste carrier portal data, parses and maps to client record
- Style: `rounded-full w-14 h-14 bg-[var(--portal)] text-white shadow-lg`, with expand animation
- Collapsed: single lightning bolt icon
- Expanded: 3 mini-FABs with labels

**Paste Portal Data modal**:
- Large textarea for pasting copied text from carrier portals
- "Parse" button that attempts to extract: client name, DOB, policy number, carrier, product, effective date, premium, value
- Preview parsed fields before saving
- "Save to Client" button writes to Firestore

### Reference Files
- `packages/ui/src/modules/MyRpiProfile.tsx` (lines 786-830) — existing MyDropZone UI
- `apps/prodash/app/(portal)/intake/page.tsx` — existing quick intake form
- `apps/prodash/app/(portal)/layout.tsx` — where to add FAB to all pages

---

## File Ownership Matrix (No Conflicts)

| File/Directory | Builder |
|---------------|---------|
| `service-centers/access/` | 1 |
| `services/api/src/routes/access.ts` | 1 |
| `ClientHeader.tsx` (handleAI3 only) | 2 |
| `AI3Report.tsx` (new) | 2 |
| `services/api/src/routes/ai3.ts` | 2 |
| `services/api/src/middleware/audit.ts` | 3 |
| `services/api/src/routes/activities.ts` | 3 |
| `TopBar.tsx` (search only) | 4 |
| `SmartSearch.tsx` (new) | 4 |
| `services/api/src/routes/search.ts` | 4 |
| `IntakeFAB.tsx` (new) | 5 |
| `layout.tsx` (add FAB) | 5 |
| `services/api/src/routes/dropzone.ts` | 5 |

**Builder 3 (audit middleware)** touches `services/api/src/index.ts` to register middleware. No other builder modifies this file.

---

## Build Verification

Each builder: `npm run build` must pass 11/11.

## Visual Verification (Auditor)

After merge:
- `/service-centers/access` — carrier/product type layout, dynamic from client accounts, auth status badges
- `/clients/[id]` → click AI3 → PDF downloads with all sections
- `/clients/[id]` → Activity tab → shows real logged changes after editing a field
- TopBar search → type "smith" → dropdown shows clients + accounts
- MyRPI → MyDropZone → setup wizard works, links + QR codes display
- Lightning bolt FAB → bottom-right all pages → 3 options expand
- `/clients/[id]` → Access tab → matches service center but scoped to client

## Sprint 10 Deferred
- OAuth integrations (ID.me, MasterCard, Carrier Connect) — needs JDM to configure API credentials
- Google Maps Places API for address autocomplete — needs API key
- RPI Connect Google Chat wiring — needs Google Chat API setup
- COMMS live send (remove dryRun) — needs Twilio env vars on Cloud Run
- Access Center Service Center admin module (carrier/product config UI)

## Context

Sprint 8 agents delivered COMMS Center, Access Center, DeDup Overhaul, and Document Buttons. JDM's 6-hour design session established the visual foundation. After surgical merge + audit, JDM did a full UI review and identified 54 items across the platform. This plan covers the **Quick Wins + Medium Work** (26 items). Feature Work (Access Center redesign, AI3, Activity audit trail, OAuth integrations) is deferred to Sprint 9.

**Full punch list**: `.claude/sprint8/SPRINT8_PUNCHLIST.md`

---

## Builder 1: Grid Pages + Global Polish

**Branch**: `sprint8/grid-polish`

### Files Owned
- `apps/prodash/app/(portal)/accounts/page.tsx`
- `apps/prodash/app/(portal)/clients/page.tsx`
- `apps/prodash/app/(portal)/clients/components/ClientFilters.tsx`
- `apps/prodash/app/globals.css` (cursor rule only)

### Tasks

**G-1: Global cursor-pointer** — Add to `globals.css`:
```css
button, a, [role="button"], [tabindex="0"] { cursor: pointer; }
```

**AC-1: Accounts Row 1** — Search (left, `rounded-md`, matching contacts shape) + `+ New` button (right, matching contacts style — not "+ New Account", same button as contacts `+ New`)

**AC-2: Accounts Row 2** — All Statuses + All Carriers dropdowns + Columns button. All styled as pills: `rounded-md h-[34px]` with same font/color as Row 3 pills. Status/Carrier dropdowns: replace `<select>` with styled pill-buttons matching the Annuity/Life/etc pills.

**AC-3: Accounts Row 3** — All | Annuity | Life | Medicare | Investment pills (already exist) + counter on far right. Counter must match contacts grid counter style: `rounded-full bg-[var(--portal)] px-2.5 py-0.5 text-xs font-semibold text-white`.

**AC-4: Accurate account count** — The current approach loads 500 via collectionGroup with `limit(500)`. The counter shows `accounts.length` (loaded count). Fix: run a separate `getCountFromServer()` query (Firestore v10+) or `getDocs` without limit to get total, OR show "500+" when `hasMore` is true. Simplest: show `{accounts.length.toLocaleString()}${hasMore ? '+' : ''}`.

**AC-5: Status/Carrier styled as pills** — Replace native `<select>` elements with custom pill-style dropdowns or at minimum style them with `h-[34px] rounded-md` matching other pills, with `bg-[var(--bg-surface)]` base and `border-[var(--portal)]` when active.

**AC-6: Background deepest black** — The accounts page container should use `bg-[var(--bg-deepest)]` or remove any `bg-[var(--bg-card)]` wrapper that lightens the background. Match contacts page.

**AC-7 + AC-8: Highlight color text** — Table column headers: `text-[var(--portal)]`. "Columns" button text: `text-[var(--portal)]`.

**AC-9: Button height consistency** — Every button on the accounts page must be `h-[34px]`. Search input: `h-[34px]`. + New button: `h-[34px]`. Columns: `h-[34px]`. Pills: `h-[34px]`.

**AC-10: Remove "500" badge** — Currently line 312-314 shows a badge with account count next to h1. Remove the h1 (already done) AND this badge. Count goes to Row 3 far-right.

**CG-1 + CG-2: Contacts grid match** — Update `ClientFilters.tsx`:
- Filter buttons should use `bg-[var(--bg-surface)]` base (the nice gray from accounts)
- Table column titles: `text-[var(--portal)]` for header text

**DD-1: DeDup on contacts grid** — Add checkbox column to contacts table (same pattern as accounts page). When 2+ selected, show "Ddup Selected (N)" button. Click opens `/ddup?ids=id1,id2&type=client`.

### Reference Files (read, don't modify)
- `apps/prodash/app/(portal)/clients/components/ColumnSelector.tsx` — existing column selector pattern
- `apps/prodash/app/(portal)/ddup/page.tsx` — ddup URL pattern

---

## Builder 2: Client360 Tabs + Behavior

**Branch**: `sprint8/client360-polish`

### Files Owned
- `apps/prodash/app/(portal)/clients/[id]/components/ClientTabs.tsx`
- `apps/prodash/app/(portal)/clients/[id]/components/ClientHeader.tsx`
- `apps/prodash/app/(portal)/clients/[id]/page.tsx`
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/AccountsTab.tsx`
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/PersonalTab.tsx`
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/ContactTab.tsx`
- `apps/prodash/app/(portal)/clients/[id]/components/tabs/ActivityTab.tsx`
- `packages/ui/src/modules/comms/CommsToolbar.tsx`

### Tasks

**C3-2: Tab reorder** — In `ClientTabs.tsx`, change TABS array order to:
```
Comms → Connect → Personal → Estate → Accounts → Connected → Access → Activity
```
Add `'access'` to `TabKey` union. Add `{ key: 'access', label: 'Access', icon: 'security' }` tab.

**C3-1: Move Access from header to tabs** — In `ClientHeader.tsx`: remove `AccessButton` import and usage. In `page.tsx`: add Access tab case in `renderTabContent()`. Import `AccessButton` component and render it as the Access tab content (or create a thin `AccessTab` wrapper that renders the Access Center page scoped to the client). The Access Center page already accepts `?clientId=` param — reuse that.

**CT-1: Agent/BoB/Source dropdowns** — In `ContactTab.tsx`, replace the 3 `InlineField` (free text) fields with `InlineField type="select"`:
- Agent: `options` from Firestore users query (add a `useCollection` for users, map to `{label: 'Last, First', value: email}`)
- Book of Business: static options `['RPI', 'Signal', 'Gradient', 'Sprenger', 'Transfer', 'Other']`
- Source: static options `['Referral', 'Marketing', 'Website', 'Walk-In', 'Transfer', 'Seminar', 'Mailer', 'Other']`

**PT-1: DL Issue Date** — In `PersonalTab.tsx`, add a new `InlineField` in the Driver's License section:
```tsx
<InlineField
  label="DL Issue Date"
  value={str(client.dl_issue_date)}
  fieldKey="dl_issue_date"
  docPath={docPath}
  type="date"
  formatDisplay={formatDLDate}
/>
```

**AT-1/DD-2: Wire ddup handler** — In `AccountsTab.tsx`, replace the placeholder `handleDdupSelected`:
```tsx
const handleDdupSelected = useCallback(() => {
  const ids = Array.from(selected).join(',')
  window.open(`/ddup?ids=${ids}&type=account`, '_blank', 'noopener,noreferrer')
}, [selected])
```

**AT-3: Account card opens new tab** — In `AccountSummaryCard`, change `handleCardClick`:
```tsx
const handleCardClick = useCallback(() => {
  window.open(`/accounts/${clientId}/${acctId}`, '_blank', 'noopener,noreferrer')
}, [clientId, acctId])
```
Remove `useRouter` import if no longer used.

**AT-4: Remove bottom chevron** — Remove the "Navigation indicator" div with the `chevron_right` icon from `AccountSummaryCard`. Card click handles navigation now.

**CM-1: Rename "Log Call"** — In `packages/ui/src/modules/comms/CommsToolbar.tsx`, change button label from "Log Call" to "Call".

**AV-1: Activity tab sub-filters** — In `ActivityTab.tsx`, change sub-tabs from `['Client', 'Account', 'Comms']` to `['All', 'Client', 'Account']`. Remove Comms filter (Comms has its own tab now). "All" shows everything. "Client" filters to client-level changes. "Account" filters to account-level changes.

### Reference Files (read, don't modify)
- `apps/prodash/app/(portal)/service-centers/access/page.tsx` — Access Center page (reuse for tab)
- `apps/prodash/app/(portal)/clients/[id]/components/AccessButton.tsx` — existing component
- `apps/prodash/app/(portal)/clients/[id]/lib/formatters.ts` — date formatters

---

## Builder 3: Shared Components (Admin + TopBar + PortalSwitcher + ConnectPanel)

**Branch**: `sprint8/shared-polish`

### Files Owned
- `packages/ui/src/modules/AdminPanel.tsx`
- `packages/ui/src/components/PortalSwitcher.tsx`
- `apps/prodash/app/(portal)/components/TopBar.tsx`
- `packages/ui/src/modules/ConnectPanel.tsx`

### Tasks

**TB-1: TopBar user area** — Remove email display. Show only Google photo + first name. Currently lines 116-123 show `displayName` + `email`. Change to just show first name:
```tsx
<span className="text-sm font-medium text-[var(--text-primary)]">
  {(user.displayName || 'User').split(' ')[0]}
</span>
```
Remove the email `<span>` entirely.

**PS-1: Portal Switcher broken PNGs** — The files `/prodashx-on-dark.png`, `/riimo-on-dark.png`, `/sentinel-on-dark.png`, `/tomachina-on-dark.png` don't exist. Fix: Replace PNG `<img>` tags with styled text labels using portal colors. Per JDM's PL2-6-9 spec: "just the portal NAME TEXT as clickable buttons — no borders/cards around logos. Clean, just text logos floating in the dropdown."

Replace each portal entry with:
```tsx
<span style={{ color: portalColor, fontWeight: 700, fontSize: '18px' }}>
  {portalName}
</span>
```
Portal names: "ProDashX" (#4a7ab5), "RIIMO" (#a78bfa), "SENTINEL" (#40bc58)
Footer: "toMachina" text in muted color, small font.
Keep the check icon for current portal, external-link icon for others, and new-tab behavior.

**RC-1: ConnectPanel title cleanup** — Remove the redundant header with shield icon + "Connect" text at the top of `ConnectPanel.tsx`. The sidebar already identifies this as RPI Connect.

**RC-2: ConnectPanel pill shapes** — Change Channels/Chat/Meet tab pills from `rounded-full` or `rounded-lg` to `rounded-md h-[34px]`. Same for "+ New Channel" button.

**AD-1: Active team members only** — In `AdminPanel.tsx` `TeamConfigTab`, filter the user list:
```tsx
const activeUsers = users.filter(u => !u.status || u.status.toLowerCase() === 'active')
```
Use `activeUsers` instead of `users` throughout TeamConfigTab.

**AD-2: Team Config 3-level redesign** — Restructure `TeamConfigTab`:
- **Level 1**: User Type groups (Owner, Executive, Leader, User) — expandable sections with user type as header, user count badge
- **Level 2**: Individual users within each type — expandable rows showing name, division, unit
- **Level 3**: Their entitlements organized by MODULE_SECTIONS — section headers (Workspace, Sales Centers, etc.) with individual module rows showing VIEW/EDIT/ADD badges

Current structure groups by Division (Sales/Service/Leadership/Other). Change grouping to use user level:
```typescript
const levelGroups = useMemo(() => {
  const groups: Record<string, UserRecord[]> = {
    Owner: [],
    Executive: [],
    Leader: [],
    User: [],
  }
  for (const u of activeUsers) {
    const level = (u.user_level || 'User').charAt(0).toUpperCase() + (u.user_level || 'User').slice(1).toLowerCase()
    if (level in groups) groups[level].push(u)
    else groups.User.push(u)
  }
  return groups
}, [activeUsers])
```

Level 3 (expanded user) should show module entitlements grouped by section:
```
▼ Josh Millang — Owner — Leadership
  ▼ Workspace
    Clients: VIEW EDIT ADD
    Accounts: VIEW EDIT ADD
  ▼ Sales Centers
    Medicare: VIEW EDIT
    Life: VIEW
  ▼ Apps
    ATLAS: VIEW EDIT ADD
```

### Reference Files (read, don't modify)
- `packages/ui/src/logos/` — check what SVGs/PNGs actually exist
- `apps/prodash/public/` — check what's in public directory

---

## Build Verification

Each builder:
```bash
cd ~/Projects/toMachina-agent{N}
npm run build   # Must pass 11/11
```

## Visual Verification (Auditor)

After merge:
- `/clients` — grid header matches accounts styling, ddup checkboxes work
- `/accounts` — 3-row header, accurate count, consistent pills
- `/clients/[id]` — Comms first tab, Access in tabs (not header), card opens new tab
- `/clients/[id]` → Accounts tab → select 2+ → Ddup Selected → opens /ddup
- `/clients/[id]` → Personal tab → DL section has Issue Date
- `/clients/[id]` → Connect tab → Agent/BoB/Source are dropdowns
- `/clients/[id]` → Activity tab → All | Client | Account filters
- `/admin` → Team Config → grouped by user type, 3 levels
- Portal Switcher → text labels, no broken images
- TopBar → first name only, no email
- RPI Connect → no redundant title, correct pill shapes
- Global: pointer cursor on all clickable elements

## Deferred to Sprint 9
- Access Center major redesign (carrier/product type, OAuth, Carrier Connect, Blue Button)
- AI3 report generation
- Activity audit trail (datetime + user stamp logging)
- Google Maps API for address autocomplete
- COMMS live send flow (888 number)
- Rapid Intake FAB (lightning bolt)
- Smart search type-ahead in TopBar
- RPI Connect actual Google Chat wiring
