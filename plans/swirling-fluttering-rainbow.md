# Householding Sprint — Wave 2 Build Plan

## Context

The household becomes the primary unit of work across ProDashX. Wave 1 (8 items) shipped the foundation: Firestore collection, API routes, migration script, types, UI pages, ConnectedTab promotion, household badge, sidebar nav — all on branch `wave1/householding`. Wave 2 builds every remaining integration: contacts grid, DeDup, import pipeline, flow engine, Kanban, beneficiary engine, AI documents, activity feed, pipeline status, ACF Drive folders, and ACF migration.

**Sprint ID:** `j5E2ONDRLKwuTlT9HH68` | **22 total items** | **8 done** | **14 to build** | **0 deferred**

## Open Question Resolutions

| Question | Decision |
|----------|----------|
| Single-person households? | Yes — every active client gets a household_id. Simplifies the model. |
| Multi-generational? | Separate household once they're a client in their own right. |
| Blended families / ex-spouses? | Cross-household links via ConnectedTab. Not household membership. |
| Household naming? | Auto-generated "{LastName} Household" with manual override via PATCH. |
| Primary contact rotation? | Yes — "Set as Primary" button in Members tab. API already supports it. |

---

## Wave 1 — DONE (branch: wave1/householding)

| TRK | Item | Status |
|-----|------|--------|
| TRK-13297 | Household Firestore collection + types | Done |
| TRK-13298 | API routes (8 endpoints) | Done |
| TRK-13299 | Migration script (ConnectedTab + address) | Done |
| TRK-13300 | Household Detail page | Done |
| TRK-13301 | Households List page | Done |
| TRK-13302 | ConnectedTab "Create Household" | Done |
| TRK-13303 | Contact Detail household badge | Done |
| TRK-13305 | Sidebar Households nav | Done |

---

## Wave 2 — 6 Parallel Builders (14 items, 0 deferred)

### BUILDER 01 — Contacts Grid + Migration Enhancement

**Items:** TRK-13304, TRK-13317 | **Complexity:** MEDIUM

**TRK-13304: Contacts grid household column + grouping toggle**
- `apps/prodash/app/(portal)/contacts/components/ColumnSelector.tsx` — Add `{ key: 'household', label: 'Household', defaultVisible: true }` to `ALL_COLUMNS`
- `apps/prodash/app/(portal)/contacts/page.tsx`:
  - Add `'household'` to `SortKey` union type (line 47)
  - Load `households` collection via `useCollection`, build `Map<household_id, household_name>`
  - Resolve `household_name` on each client row
  - Add household column header + sort case + cell renderer (clickable link to `/households/{id}`)
  - Add grouping toggle in filter bar: ON = group rows by household with section headers, OFF = flat list (default)

**TRK-13317: Migration enhancement — MFJ + same-phone**
- `services/api/src/scripts/migrate-households.ts`:
  - Add step 3.5: MFJ filing_status detection (scan for "married"/"MFJ" clients, pair with same last_name + same address)
  - Add step 3.6: Same-phone detection (shared phone + same last_name = household)
  - Log counts per detection method

---

### BUILDER 02 — DeDup Merge + Import Auto-Detect

**Items:** TRK-13315, TRK-13316 | **Complexity:** MEDIUM-HIGH

**TRK-13315: DeDup household-aware merge**
- `apps/prodash/app/(portal)/ddup/page.tsx` — In `handleMerge()` (lines 424-514), add step 5 after existing subcollection moves:
  - If loser has `household_id` and winner doesn't: transfer household_id to winner, update household members array (replace loser's client_id with winner's)
  - If both have same `household_id`: remove loser from members array
  - If both have different `household_id`: remove loser from their household (soft-delete household if now empty after removal)
  - If neither has household: no-op

**TRK-13316: Import auto-detect households**
- `services/api/src/routes/import.ts` — In `POST /import/batch`, insert Phase 1.5 between client commit (line 473) and account import (line 476):
  - Build address-group map from imported clients: `lastNameLower_addressLower_zip -> client_id[]`
  - Detect spouse-field matches (spouse_name, spouse_dob, spouse_phone)
  - Check MFJ filing_status on imported clients
  - Create household records for detected groups
  - Check against existing households in Firestore (add member vs. create new)
  - Track results: `results.households = { detected: N, created: N }`
  - Separate batch for household writes (avoids exceeding 500-op limit)

---

### BUILDER 03 — Flow Engine + Pipeline + Kanban

**Items:** TRK-13310, TRK-13311, TRK-13312 | **Complexity:** MEDIUM

**TRK-13310: Flow engine entity_type household**
- `packages/core/src/flow/constants.ts` — Add `HOUSEHOLD_ENTITY_TYPE = 'HOUSEHOLD'`
- `packages/core/src/flow/types.ts` — JSDoc on `entity_type` documenting `'CLIENT' | 'HOUSEHOLD'`
- `services/api/src/routes/flow.ts` — Add `entity_id` query filter (alongside existing `entity_type` filter)

**TRK-13311: Kanban household cards**
- `packages/ui/src/modules/PipelineKanban/KanbanCard.tsx`:
  - When `entity_type === 'HOUSEHOLD'`: show home icon badge + member names from entity_data
  - Card dynamically reads household doc for live member count (so adding a spouse mid-pipeline updates the card without needing to patch the instance)
  - Parse `entity_data` (JSON string) safely via useMemo for household_id reference
  - Fetch household doc via `useDocument` when entity_type is HOUSEHOLD to get current members

**TRK-13312: Prospect pipeline household config**
- Create `packages/core/src/flow/configs/prospect-household.ts` — follows `prospect-retirement.ts` pattern exactly
  - `pipeline_key: 'PROSPECT_HOUSEHOLD'`, same 7 stages (New Lead, Engaged, Connect 1/2/3, Outcome Yes/No)
  - `default_entity_type: 'HOUSEHOLD'` in pipeline definition
  - Handoff: Outcome Yes creates SALES_RETIREMENT instance
- `packages/core/src/flow/configs/index.ts` — import + export + add to `ALL_PIPELINE_CONFIGS`

---

### BUILDER 04 — Household Detail Enhancements

**Items:** TRK-13306, TRK-13307, TRK-13314 | **Complexity:** MEDIUM-HIGH

**TRK-13306: Household activity feed tab**
- `services/api/src/routes/activities.ts` — New endpoint: `GET /api/activities/household/:householdId`
  - Look up household members, query each member's `clients/{cid}/activities` (limit 50 per member)
  - Merge-sort by `created_at` desc, return top 100
  - Each activity tagged with `member_name` for display context
- `apps/prodash/app/(portal)/households/[id]/page.tsx`:
  - Add `'activity'` tab with icon `history`
  - `ActivityTab` component: fetch from endpoint, render timeline with member name badge per entry

**TRK-13307: Household pipeline status tab**
- `apps/prodash/app/(portal)/households/[id]/page.tsx`:
  - Add `'pipelines'` tab with icon `route`
  - `PipelinesTab` component: fetch `GET /api/flow/instances?entity_type=HOUSEHOLD&entity_id={householdId}` + fetch member-level instances for each member client_id
  - Two sections: "Household Pipelines" (entity_type=HOUSEHOLD) + "Member Pipelines" (individual member instances)
  - Cards: pipeline name, current stage, priority badge, link to Kanban

**TRK-13314: Beneficiary engine household context**
- `packages/core/src/financial/beneficiary.ts`:
  - Add `HouseholdBeneficiaryContext` interface (householdId, householdName, members with accounts)
  - Add `HouseholdBeneficiaryReport` interface (memberReports, householdSummary, crossMemberIssues)
  - Add `analyzeHouseholdBeneficiaries()`: runs existing `analyzeBeneficiary()` per member per account, aggregates into household summary
  - Cross-member analysis: detect if spouses properly name each other as beneficiaries, flag gaps where neither names the other

**Also in Builder 04 — gap fixes from audit:**

**Household Accounts tab (gap from discovery: "all accounts across members")**
- `apps/prodash/app/(portal)/households/[id]/page.tsx`:
  - Add `'accounts'` tab with icon `account_balance`
  - `AccountsTab` component: for each member, query `clients/{cid}/accounts`, merge all accounts
  - Grid columns: Owner Name, Carrier, Product, Type, Policy #, Status, Premium, Face Amount
  - Tagged by owner name so you see Stephen's and Joyce's accounts in one view
  - Clickable rows link to `/contacts/{client_id}` accounts tab

**"Set as Primary" button (gap from discovery: primary contact rotation)**
- In existing `MembersTab` on the household detail page:
  - Add "Set as Primary" button on non-primary member cards
  - On click: PATCH `/api/households/{id}` with `{ primary_contact_id: newId, primary_contact_name: newName }`, update member roles (old primary → spouse/other, new member → primary)

---

### BUILDER 05 — AI Documents + Household Intelligence

**Items:** TRK-13313 | **Complexity:** MEDIUM

**TRK-13313: AI Documents — Household-scoped generation**

The discovery lists 5 document types that go household-aware. AI3 is the only one with an existing API endpoint. The other 4 (Discovery Meeting Prep, Review Meeting Agenda, Casework, New Business Proposals) currently exist only as manual processes. This builder creates the household data aggregation layer that ALL document types will consume, plus the AI3 endpoint and a household meeting prep endpoint.

- `services/api/src/routes/ai3.ts` — New endpoint: `GET /api/ai3/household/:householdId`
  - Fetch household doc + all members' client docs + accounts + access_items + connected_contacts + recent activities
  - Aggregate into household report structure:
    ```
    { household, members: [{ client, accounts, access_items, connected_contacts, recent_activities }],
      combined_totals: { total_accounts, total_premium, total_face_amount, by_category },
      beneficiary_summary: { completeness_rate, cross_member_issues },
      generated_at, generated_by }
    ```
  - Uses existing `deriveCategory()` helper
  - Same `{ success, data }` response pattern

- `services/api/src/routes/households.ts` — New endpoint: `GET /api/households/:id/meeting-prep`
  - Generates household-scoped meeting preparation data:
    - Household summary (members, address, aggregate financials)
    - Per-member asset inventory (accounts by category with totals)
    - Opportunity identification: income/SS optimization, annuity review, life coverage gaps, Medicare coordination, estate planning gaps
    - Beneficiary cross-check (calls `analyzeHouseholdBeneficiaries()` from Builder 04)
    - Action items / conversation starters
  - Returns structured JSON that can drive: Discovery Meeting Prep, Review Meeting Agenda, Casework context, New Business Proposals
  - This is the **data layer** — rendering to PDF/HTML comes in Sprint 11 (DEX modernization). But the data is available now for any consumer.

---

### BUILDER 06 — ACF Drive Folders

**Items:** TRK-13308, TRK-13309 | **Complexity:** MEDIUM

These are NOT deferred. The discovery is explicit about household-level ACF structure.

**TRK-13308: ACF household-level Drive folder creation**
- `gas/RAPID_CORE/CORE_Drive.gs` — New function: `createHouseholdACFFolder(householdId, householdInfo)`
  - Creates folder structure:
    ```
    ACF/
    └── {HouseholdName} ({householdId-first8})/
        ├── 1. Discovery & Intake
        ├── 2. Statements & Documents
        │   ├── {Member1Name}/
        │   └── {Member2Name}/
        ├── 3. Analysis & Planning
        ├── 4. Proposals & Presentations
        ├── 5. Paperwork & Compliance
        └── Accounts/
    ```
  - Uses existing `getOrCreateFolder()` helper (idempotent)
  - Stores folder URL back to household doc via `updateRow()` or direct Firestore write
  - Parameters: `householdId`, `{ householdName, members: [{ firstName, lastName }] }`
- Also update existing `createACFFolder()`: if client has `household_id`, nest the client folder under the household folder instead of at ACF root
- Also update existing `createAccountFolder()`: tag account folders with owner name: `"{MemberName} - {Carrier} {ProductType} ({accountId})"`
- Deploy: `clasp push --force` (GAS maintenance deploy)

**TRK-13309: ACF migration — restructure existing individual folders into household structure**
- New script: `services/api/src/scripts/migrate-acf-households.ts`
  - Query all households with 2+ members
  - For each household: check if members have existing individual ACF folders (`gdrive_folder_url`)
  - If yes: create household root folder, move individual member folders under `2. Statements & Documents/{MemberName}/`
  - Create shared phase folders (1. Discovery, 3. Analysis, 4. Proposals, 5. Paperwork)
  - Update household doc with new `acf_folder_url`
  - Update member client docs to point to the restructured location
  - Supports `--dry-run` (report what would move without moving)
  - Uses gdrive MCP tools (`mcp__gdrive__createFolder`, `mcp__gdrive__moveItem`, `mcp__gdrive__listFolder`) or GAS DriveApp
- **Risk**: Moving Drive folders is destructive. Dry-run first. JDM approves before live run.

---

## File Ownership (No Conflicts)

| Builder | Exclusive Files |
|---------|----------------|
| 01 | `contacts/page.tsx`, `contacts/components/ColumnSelector.tsx`, `migrate-households.ts` |
| 02 | `ddup/page.tsx`, `import.ts` |
| 03 | `packages/core/src/flow/*`, `PipelineKanban/KanbanCard.tsx`, new `prospect-household.ts` |
| 04 | `households/[id]/page.tsx`, `beneficiary.ts`, `activities.ts` |
| 05 | `ai3.ts`, `households.ts` (meeting-prep endpoint only — no conflict with Builder 04 which touches the detail page) |
| 06 | `gas/RAPID_CORE/CORE_Drive.gs`, new `migrate-acf-households.ts` |

---

## Execution

1. All 6 builders run in parallel with worktree isolation (Builders 01-05 in toMachina monorepo, Builder 06 in gas/RAPID_CORE)
2. Each builder commits on its own branch (`wave2/householding-builder-NN`)
3. Audit: type-check 13/13 + build clean + code review checklist
4. Merge all builder branches into `wave1/householding`
5. Builder 06: separate `clasp push` for GAS deploy + ACF migration dry-run → JDM approval → live run
6. FORGE transition: 14 items built → audited → JDM #SendIt

## Verification

- `npm run type-check` — 13/13 workspaces
- `npm run build` — clean build
- Manual: `/contacts` — household column visible, grouping toggle works
- Manual: `/households/{id}` — all 6 tabs render (Overview, Members, Accounts, Financials, Activity, Pipelines)
- Manual: `/households/{id}` Members tab — "Set as Primary" button works
- Manual: DeDup merge two clients in same household — household membership updates correctly
- API: `GET /api/ai3/household/{id}` — aggregated report with all members
- API: `GET /api/households/{id}/meeting-prep` — structured meeting prep data returns
- API: `GET /api/activities/household/{id}` — merged activity feed across members
- API: `GET /api/flow/instances?entity_type=HOUSEHOLD` — filter works
- GAS: `createHouseholdACFFolder()` — creates correct folder structure in Drive
- Script: `migrate-acf-households.ts --dry-run` — reports accurate restructure plan
