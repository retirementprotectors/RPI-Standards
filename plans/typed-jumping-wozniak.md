# ProZone Single-Pane Consolidation — Build Plan

## Context

ProZone's 4-tab UI shows overlapping data. Plan audit revealed 10 operational gaps. This sprint consolidates the UI AND wires the operational core.

**Sprint scope:** 19 items (TRK-13494 through TRK-13512)
- Phase A-C: Single-pane consolidation (TRK-13494–13502)
- Phase D-E: Operational wiring + data fixes (TRK-13503–13512)

---

## Key Discoveries from Exploration

1. **Household collection already exists** — full CRUD API (`services/api/src/routes/households.ts`, 410 lines), type definitions in `packages/core/src/types/index.ts` (lines 347-384), migration script, meeting-prep endpoint. TRK-13509 is partially solved.
2. **Client docs have `has_medicare`, `has_life`, `has_annuity`, `account_types`** in Firestore but NOT in the TS type def (falls under `[key: string]: unknown`). The zone-leads endpoint already reads these fields.
3. **REASON_STYLES pattern** in `ZoneLeadPanel.tsx` (lines 17-24) is the exact pattern to reuse for InventoryBadge.
4. **Tier color system** is consistent across all views: emerald=I, sky=II, amber=III, red=IV.
5. **fetchWithAuth** (shared module helper) injects Firebase Auth token. All API calls use it.

---

## Build Order + Builder Assignment

### Phase A: API + Types (sequential — unblocks everything)

**Builder 1 — API + Types** (no worktree needed, single builder)

#### TRK-13494: Prospects API — add inventory flags
**File:** `services/api/src/routes/prozone.ts`

In the `/prospects/:specialist_id` route (lines 143-165), after grouping clients by zone, add inventory computation to each prospect:

```typescript
// After line 163 (client_status: client.client_status)
// Add inventory fields — same logic as zone-leads endpoint (lines 398-422)
const hasM = !!(client.has_medicare) || ((client.account_types as string) || '').toLowerCase().includes('medicare')
const hasL = !!(client.has_life) || ((client.account_types as string) || '').toLowerCase().includes('life')
const hasA = !!(client.has_annuity) || ((client.account_types as string) || '').toLowerCase().includes('annuity')
const hasRIA = ((client.account_types as string) || '').toLowerCase().includes('ria')
const hasBD = ((client.account_types as string) || '').toLowerCase().includes('bd')

const inventory = { has_medicare: hasM, has_life: hasL, has_annuity: hasA, has_ria: hasRIA, has_bd: hasBD }
const flags: string[] = []
if (hasM) flags.push('Active Medicare')
if ((hasL || hasA) && age !== null && age >= 80) flags.push('L&A 80+')
if (age !== null && age < 80 && !hasL && !hasA && !hasM && !hasRIA && !hasBD) flags.push('No Core Product')
```

Add to each prospect object: `inventory`, `flags`

Add to each zone result: `flagged_count` (count of prospects with flags.length > 0), `flag_summary` (Record<string, number> counting each flag type)

Add to top-level response: `total_flagged`

**Do NOT delete the zone-leads endpoint** — just add a comment marking it deprecated.

#### TRK-13495: Types update
**File:** `packages/ui/src/modules/ProZone/types.ts`

Add:
```typescript
export interface InventoryFlags {
  has_medicare: boolean
  has_life: boolean
  has_annuity: boolean
  has_ria: boolean
  has_bd: boolean
}

export interface ProspectWithInventory extends Omit<Prospect, 'prospect_id'> {
  client_id: string
  inventory: InventoryFlags
  flags: string[]
}

export interface ZoneWithProspects {
  zone_id: string
  zone_name: string
  tier: 'I' | 'II' | 'III' | 'IV'
  prospects: ProspectWithInventory[]
  prospect_count: number
  flagged_count: number
  flag_summary: Record<string, number>
}
```

Keep `ZoneLead` and `CountyRow` for now (ScheduleView and admin components may still reference them). Delete when TRK-13502 removes the old components.

---

### Phase B: Leaf Components (parallel — 3 builders in worktree isolation)

**Builder 2 — InventoryBadge + ProspectRow**

#### TRK-13496: InventoryBadge
**File:** `packages/ui/src/modules/ProZone/InventoryBadge.tsx` (NEW, ~40 lines)

Reuse REASON_STYLES pattern from `ZoneLeadPanel.tsx` lines 17-28:
```typescript
const FLAG_STYLES: Record<string, { bg: string; text: string }> = {
  'Active Medicare': { bg: 'bg-sky-500/10', text: 'text-sky-400' },
  'L&A 80+':        { bg: 'bg-amber-500/10', text: 'text-amber-400' },
  'No Core Product': { bg: 'bg-red-500/10', text: 'text-red-400' },
}
```

Props: `{ flag: string; count?: number }` — if count provided, renders `"{flag} ({count})"`, otherwise just `"{flag}"`.

Badge class: `rounded-full px-2.5 py-0.5 text-[10px] font-medium ${style.bg} ${style.text}`

Also export a product pill component for inventory display:
```typescript
const PRODUCT_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  has_medicare: { bg: 'bg-sky-500/10', text: 'text-sky-400', label: 'MA' },
  has_life:     { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: 'Life' },
  has_annuity:  { bg: 'bg-violet-500/10', text: 'text-violet-400', label: 'Ann' },
  has_ria:      { bg: 'bg-cyan-500/10', text: 'text-cyan-400', label: 'RIA' },
  has_bd:       { bg: 'bg-orange-500/10', text: 'text-orange-400', label: 'BD' },
}
```

#### TRK-13497: ProspectRow
**File:** `packages/ui/src/modules/ProZone/ProspectRow.tsx` (NEW, ~80 lines)

Props: `{ prospect: ProspectWithInventory }`

Layout (single row, no wrapping):
```
[person icon] Name (first last) | County, City | Age | [MA] [Life] [Ann] | [Active Medicare badge] [No Core badge]
```

- Product pills from inventory (only show products the client HAS)
- Flag badges from flags array (only show if non-empty)
- Age right-aligned
- Hover: `hover:bg-[var(--bg-surface)]` subtle highlight
- Row padding: `px-4 py-2.5`

---

**Builder 3 — StatsBar**

#### TRK-13498: StatsBar
**File:** `packages/ui/src/modules/ProZone/StatsBar.tsx` (NEW, ~100 lines)

Props:
```typescript
interface StatsBarProps {
  zoneCount: number
  clientCount: number
  flaggedCount: number
  searchQuery: string
  onSearchChange: (q: string) => void
  tierFilter: string  // 'all' | 'I' | 'II' | 'III' | 'IV'
  onTierFilterChange: (t: string) => void
  flaggedOnly: boolean
  onFlaggedOnlyChange: (v: boolean) => void
}
```

Layout:
```
[3 stat cards: Zones | Clients | Flagged] [Search input] [Tier dropdown] [Flagged Only toggle]
```

- Stat cards: same style as TerritoryView summary cards (line 118-136)
- Search: text input with search icon, `placeholder="Search by name..."`
- Tier dropdown: `<select>` with All Tiers, Tier I, II, III, IV options
- Flagged toggle: button/switch that highlights when active
- Responsive: stats + filters wrap on mobile

---

**Builder 4 — ZoneAccordion + WeekStrip**

#### TRK-13499: ZoneAccordion
**File:** `packages/ui/src/modules/ProZone/ZoneAccordion.tsx` (NEW, ~180 lines)

Props:
```typescript
interface ZoneAccordionProps {
  zone: ZoneWithProspects
  isOpen: boolean
  onToggle: () => void
  searchQuery: string  // for highlighting matches
}
```

**Collapsed header:**
```
[chevron_right] Zone Name [Tier I badge] 142 clients | [Active Medicare (12)] [L&A 80+ (8)] [No Core (4)]
```

- Tier badge: same emerald/sky/amber/red system
- Flag summary uses InventoryBadge with count
- Client count right-aligned
- Click header to toggle

**Expanded body:**
- Table header: Name | Location | Age | Products | Flags
- Map `zone.prospects` through `<ProspectRow>` components
- If `searchQuery` is active, filter prospects by name match
- Smooth expand/collapse transition: `max-h-0 overflow-hidden transition-all` → `max-h-[2000px]`

#### TRK-13500: WeekStrip
**File:** `packages/ui/src/modules/ProZone/WeekStrip.tsx` (NEW, ~120 lines)

Props:
```typescript
interface WeekStripProps {
  specialistId: string
  onFieldDayClick?: (tier: string) => void  // auto-open matching zone
}
```

Fetches: `/api/prozone/schedule/${specialistId}/${currentWeekKey}`

**Compact mode (default):**
```
[< prev] Week 12 • Mar 16-20 [next >]
Mon: Office (6)  |  Tue: Field II (5)  |  Wed: Field I (6)  |  Thu: Field III (4)  |  Fri: Off
```

- Each day is a clickable cell
- Field days show tier + slot count, colored by tier
- Office days show "Office" + slot count in neutral
- Off days grayed out
- Click a field day → calls `onFieldDayClick(tier)` to auto-open the matching zone accordion

**Expanded mode (toggle):**
- Shows the full ScheduleView component with pre-fetched data
- Toggle button: "Expand Schedule ↓" / "Collapse Schedule ↑"

---

### Phase C: Assembly (sequential — single builder on main)

**Builder 1 (same as Phase A) — or GA directly**

#### TRK-13501: ProZoneApp rewrite
**File:** `packages/ui/src/modules/ProZone/ProZoneApp.tsx` (REWRITE)

Remove: Tab system (TABS constant, activeTab state, tab navigation bar, conditional tab rendering)

New state:
```typescript
const [specialists, setSpecialists] = useState<SpecialistConfig[]>([])
const [selectedId, setSelectedId] = useState<string | null>(null)
const [zones, setZones] = useState<ZoneWithProspects[]>([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)

// Filter state (lifted from StatsBar)
const [searchQuery, setSearchQuery] = useState('')
const [tierFilter, setTierFilter] = useState('all')
const [flaggedOnly, setFlaggedOnly] = useState(false)

// Accordion state
const [openZones, setOpenZones] = useState<Set<string>>(new Set())
```

Data fetch (when specialist changes):
```typescript
const [territoryRes, prospectsRes] = await Promise.all([
  fetchWithAuth(`/api/territories/${spec.territory_id}`),
  fetchWithAuth(`/api/prozone/prospects/${selectedId}`),
])
```

Merge territory zone names with prospect zone data. Compute totals for StatsBar.

Filtering logic (useMemo):
```typescript
const filteredZones = useMemo(() => {
  let filtered = zones
  if (tierFilter !== 'all') filtered = filtered.filter(z => z.tier === tierFilter)
  if (flaggedOnly) filtered = filtered.filter(z => z.flagged_count > 0)
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase()
    filtered = filtered.map(z => ({
      ...z,
      prospects: z.prospects.filter(p =>
        `${p.first_name} ${p.last_name}`.toLowerCase().includes(q)
      ),
    })).filter(z => z.prospects.length > 0)
  }
  return filtered
}, [zones, tierFilter, flaggedOnly, searchQuery])
```

Layout:
```jsx
<SpecialistSelector ... />
{selectedId && (
  <>
    <StatsBar
      zoneCount={filteredZones.length}
      clientCount={filteredZones.reduce((s, z) => s + z.prospects.length, 0)}
      flaggedCount={filteredZones.reduce((s, z) => s + z.flagged_count, 0)}
      searchQuery={searchQuery}
      onSearchChange={setSearchQuery}
      tierFilter={tierFilter}
      onTierFilterChange={setTierFilter}
      flaggedOnly={flaggedOnly}
      onFlaggedOnlyChange={setFlaggedOnly}
    />
    <WeekStrip
      specialistId={selectedId}
      onFieldDayClick={(tier) => {
        const zone = filteredZones.find(z => z.tier === tier)
        if (zone) setOpenZones(prev => new Set(prev).add(zone.zone_id))
      }}
    />
    {filteredZones.map(zone => (
      <ZoneAccordion
        key={zone.zone_id}
        zone={zone}
        isOpen={openZones.has(zone.zone_id)}
        onToggle={() => toggleZone(zone.zone_id)}
        searchQuery={searchQuery}
      />
    ))}
  </>
)}
```

#### TRK-13502: Delete obsolete components
- Delete `TerritoryView.tsx`, `ProspectQueue.tsx`, `ZoneLeadPanel.tsx`
- Update `index.ts`: keep ProZone, TerritoryBuilder, SpecialistConfigEditor exports
- Remove `ZoneLead` and `CountyRow` from `types.ts` if no remaining references
- Verify: `npm run type-check` 13/13

---

### Phase D: Operational Wiring (3 parallel builders, worktree)

**Builder 5: Meeting Criteria + Pipeline Aggregation**

#### TRK-13503: Meeting Criteria Engine
**File:** `services/api/src/routes/prozone.ts`

In client loop, after computing inventory, determine meeting type:
- Use `account_types` array (pattern from `campaigns/audience.ts:135-144`)
- `hasLA = accountTypes.some(t => t.includes('life') || t.includes('annuity'))`
- Field: hasLA AND age < 80. Office: hasLA AND (age >= 80 OR outer zone).
- Add `meeting_type: 'field' | 'office' | 'none'` to each prospect

#### TRK-13504: Pipeline Aggregation
**File:** `services/api/src/routes/prozone.ts`

Query `flow_instances` WHERE entity_type IN ['CLIENT','HOUSEHOLD'] AND stage_status IN ['pending','in_progress']. Build entity_id map. Add `pipeline?: { pipeline_key, stage, priority }` to each prospect. ProspectRow shows pipeline badge.

**Builder 6: Call Workflow + Contextual Leads**

#### TRK-13505: Click-to-call + Disposition + Booking
**Files:** `CallPanel.tsx` (NEW ~200 lines), `ProspectRow.tsx` (MODIFY), `households.ts` (MODIFY)

CallPanel: phone click -> `POST /api/comms/send-voice { to, from: '+18886208587' }` (existing in comms.ts:253-304) -> timer + status poll -> disposition form (Booked/Callback/No Answer/Not Interested + notes) -> `POST /api/comms/log-call` (existing in comms.ts:310-339) -> if Booked: open calendar_booking_url + create appointment.

New endpoint in households.ts: `POST /:id/appointments { date, time, specialist_id, zone_id, tier, type, notes }`. Firestore rules already permit subcollections (line 136-141).

#### TRK-13506: Contextual Zone Leads from Schedule
**Files:** `ZoneAccordion.tsx` (MODIFY), `ProZoneApp.tsx` (MODIFY)

WeekStrip extracts zone_ids from field day slots -> passes up via `onScheduleLoaded` callback -> ProZoneApp builds scheduledZones Map -> passes to ZoneAccordion as `scheduledMeetings` prop. Header shows: "[calendar] 2 meetings Tue".

**Builder 7: Data Fixes + Remaining Features**

#### TRK-13507: Drag-and-Drop
**Files:** `ProspectRow.tsx` (MODIFY), `WeekStrip.tsx` (MODIFY)

Native HTML5 drag-and-drop. ProspectRow: draggable + onDragStart with JSON payload. Schedule slots: onDragOver + onDrop -> create appointment via households API.

#### TRK-13508: ZIP-level Zone Resolution
**Files:** `seed-prozone.ts` (MODIFY), `prozone.ts` (MODIFY)

Add ZIP entries for Polk County in seed. In prospects endpoint: build zipZoneMap + countyZoneMap. ZIP takes precedence: `zipZoneMap.get(client.zip) || countyZoneMap.get(county)`.

#### TRK-13509: Household Territory Enrichment
**File:** `households.ts` (MODIFY)

Batch enrichment: copy territory_id + zone_id from primary contact's client record to household doc. Appointments endpoint covered in TRK-13505.

#### TRK-13510: Age Buckets + BoB Breakdown
**Files:** `prozone.ts` (MODIFY), `ZoneAccordion.tsx` (MODIFY)

Compute per zone: under_60, 60_64, 65_80, 80_plus buckets. BoB from client.source. Add to zone response. ZoneAccordion header shows mini age bar + BoB pills.

#### TRK-13511: Mason City Territory
**File:** `seed-prozone.ts` (MODIFY)

Add T7: Cerro Gordo, Floyd, Worth, Winnebago, Howard, Mitchell. 2 zones (T7-Z1 Core, T7-Z2 Outer). Add to Arch's tier_map as III/IV (150-180 min from Oskaloosa). Re-run seed.

#### TRK-13512: Dexter Cross-Sell
**File:** `prozone.ts` (MODIFY)

When loading Arch's territory, also query clients with source == 'Dexter' in same counties. Flag as `cross_sell_from: "Dexter"`. ZoneAccordion shows distinct cross-sell section.

---

### Phase E: Final Assembly (GA, main)

Merge all Phase D builders. Run full verification.

---

## Builder Execution Strategy

| Phase | Builder | Items | Depends On |
|-------|---------|-------|------------|
| A | Builder 1 | TRK-13494, TRK-13495 | nothing |
| B | Builder 2 | TRK-13496, TRK-13497 | Phase A |
| B | Builder 3 | TRK-13498 | nothing |
| B | Builder 4 | TRK-13499, TRK-13500 | Phase A |
| C | GA | TRK-13501, TRK-13502 | A + B |
| D | Builder 5 | TRK-13503, TRK-13504 | Phase C |
| D | Builder 6 | TRK-13505, TRK-13506 | Phase C |
| D | Builder 7 | TRK-13507 to TRK-13512 | Phase C |
| E | GA | Final merge + verification | Phase D |

---

## Critical Files

| File | Action |
|------|--------|
| `services/api/src/routes/prozone.ts` | Modify: inventory, criteria, pipeline, age buckets, cross-sell |
| `services/api/src/routes/comms.ts` | Reference: Twilio voice/log already exist |
| `services/api/src/routes/households.ts` | Modify: appointments endpoint, territory enrichment |
| `services/api/src/routes/flow.ts` | Reference: flow_instances query |
| `services/api/src/scripts/seed-prozone.ts` | Modify: T7 Mason City, ZIP zones |
| `packages/ui/src/modules/ProZone/types.ts` | Modify: new types |
| `packages/ui/src/modules/ProZone/InventoryBadge.tsx` | NEW |
| `packages/ui/src/modules/ProZone/ProspectRow.tsx` | NEW: draggable + call button |
| `packages/ui/src/modules/ProZone/StatsBar.tsx` | NEW |
| `packages/ui/src/modules/ProZone/ZoneAccordion.tsx` | NEW: meetings context + age buckets |
| `packages/ui/src/modules/ProZone/WeekStrip.tsx` | NEW: drop targets |
| `packages/ui/src/modules/ProZone/CallPanel.tsx` | NEW: call + disposition + booking |
| `packages/ui/src/modules/ProZone/ProZoneApp.tsx` | REWRITE |
| `packages/ui/src/modules/ProZone/index.ts` | Modify |
| `TerritoryView.tsx, ProspectQueue.tsx, ZoneLeadPanel.tsx` | DELETE |

---

## Reusable Patterns (from existing code)

| Pattern | Source | Reuse In |
|---------|--------|----------|
| REASON_STYLES badge map | `ZoneLeadPanel.tsx:17-24` | InventoryBadge |
| TIER_BADGE_STYLES | `ProspectQueue.tsx:16-21` | ZoneAccordion header |
| Summary stat cards | `TerritoryView.tsx:118-136` | StatsBar |
| fetchWithAuth | `modules/fetchWithAuth.ts` | WeekStrip |
| Zone-leads inventory logic | `prozone.ts:393-435` | prospects endpoint (TRK-13494) |
| SpecialistSelector | `SpecialistSelector.tsx` (keep as-is) | ProZoneApp |

---

## Verification

### Phase A-C (Single-Pane)
1. `npm run type-check` 13/13
2. Zone accordion with inventory flags + filter/search/flagged toggle
3. Week strip with field day click auto-opens zone

### Phase D-E (Operational)
4. Meeting type badges (field/office) on each prospect
5. Pipeline badges on prospects in active flows
6. Click phone icon: Twilio call initiates, disposition, appointment logged
7. Drag prospect onto schedule slot: creates appointment
8. Zone headers show "2 meetings scheduled Tue" context
9. Age buckets + BoB in zone headers
10. T7 Mason City in Arch territory
11. Dexter cross-sell prospects in Arch zones
12. Polk County clients resolve to ZIP-level zones
