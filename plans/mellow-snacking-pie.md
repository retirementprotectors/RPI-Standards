# ATLAS Frontend + TOOL_FIELD_INTROSPECT + WIRE_MEDICARE_ACCOUNTS

## Context

JDM delivered 5 GHL CSV exports (~16K rows: clients, medicare, life, investment, annuity accounts). Consulting the ATLAS registry exposed three gaps: no Medicare account data wire, no field introspection tool, and no ATLAS frontend for data intake. This sprint fills those gaps and makes ATLAS the single front door for all data entering The Machine. Nobody touches a database.

**Sprint ID:** `131mgk5pOoNx3AvRL0Z4`
**Items:** TRK-170 through TRK-187 (18 items)
**Discovery Doc:** `.claude/discovery/ATLAS_FRONTEND_AND_FIELD_INTROSPECT.md`

---

## Build Strategy: 3 Parallel Builders

| Builder | Scope | Items | Est. Lines |
|---------|-------|-------|-----------|
| **A: ATLAS Backend** | Wire #17, Format Library, Introspection Engine, API endpoints | TRK-170 — TRK-177 (8) | ~800 new |
| **B: ATLAS Frontend** | Reorganize AtlasRegistry into 3 sections + build Import section | TRK-178 — TRK-184 (7) | ~700 new |
| **C: FORGE Polish** | Verify discovery_url, verify Discovery Import API, build Discovery Import UI | TRK-185 — TRK-187 (3) | ~150 new |

**Merge order:** C first (smallest), then A, then B (B depends on A's types).

---

## Firestore Schemas (New Collections)

### `atlas/formats/{format_id}`
```
format_id: string               // "FMT_xxxxxxxx"
carrier_export_type: string     // "north_american_fia", "ghl_medicare_accounts"
carrier_name: string
header_fingerprint: string      // SHA-256 of sorted, lowercased headers
column_map: { [csv_header]: firestore_field }
value_patterns: { [column]: { distinct_count, sample_values[], dominant_type, null_rate } }
dedup_keys: string[]
default_category: string        // "medicare" | "annuity" | "life" | "bdria"
times_used: number
last_used_at: string
created_by, created_at, updated_at: string
```

### `atlas/introspect_runs/{run_id}`
```
run_id: string                  // "INTR_xxxxxxxx"
format_id: string | null
header_fingerprint: string
headers: string[]
target_category: string
match_method: "fingerprint_exact" | "fingerprint_partial" | "carrier_detect" | "full_introspect"
overall_confidence: number
column_mappings: [{ csv_header, firestore_field, confidence, status, alternatives[] }]
triggered_by, created_at: string
```

Both live under `atlas/` — already covered by existing Firestore rules (leader+ write, RPI read).

---

## API Contracts (Builder A implements, Builder B consumes)

### POST /api/atlas/introspect
```
Request:  { headers: string[], sample_rows: Record[], target_category?: string }
Response: { success, data: { run_id, match_method, format_id?, overall_confidence,
            column_mappings: [{ csv_header, firestore_field, confidence, status, alternatives[] }],
            carrier_detection: { detected_carrier, carrier_confidence, default_category },
            sample_normalized: Record[] } }
```

### POST /api/atlas/introspect/confirm
```
Request:  { run_id, confirmed_mappings: [{ csv_header, firestore_field }],
            carrier_export_type?, save_to_format_library: boolean }
Response: { success, data: { format_id, mappings_confirmed, ready_for_import } }
```

### GET/POST/PATCH /api/atlas/formats
```
GET:   ?carrier_name, default_category, limit → AtlasFormat[]
POST:  { carrier_export_type, carrier_name, column_map, ... } → { format_id, ... }
PATCH: /:id + partial body → { id, updated_at }
```

---

## Builder A: ATLAS Backend

### Files to CREATE
| File | Contents |
|------|----------|
| `packages/core/src/atlas/introspect.ts` | 5 pure functions: `hashHeaderFingerprint()`, `profileCsvColumns()`, `profileCollection()`, `matchProfiles()`, `matchFingerprint()` |

### Files to MODIFY
| File | Changes |
|------|---------|
| `packages/core/src/atlas/types.ts` | Add interfaces: `AtlasFormat`, `IntrospectRun`, `ColumnMapping`, `FieldProfile` |
| `packages/core/src/atlas/wires.ts` | Add `WIRE_MEDICARE_ACCOUNTS` to WIRE_DEFINITIONS array (wire #17, product_line: MAPD, data_domain: ACCOUNTS, 8 stages) |
| `packages/core/src/atlas/index.ts` | Export new types + introspect functions |
| `services/api/src/routes/atlas.ts` | Add wire #17 to API WIRE_DEFINITIONS. Add 5 endpoints: GET/POST/PATCH `/formats`, POST `/introspect`, POST `/introspect/confirm` |

### WIRE_MEDICARE_ACCOUNTS Definition
```
wire_id: 'WIRE_MEDICARE_ACCOUNTS'
name: 'Medicare Account Processing'
product_line: 'MAPD', data_domain: 'ACCOUNTS'
stages:
  1. EXTERNAL: Carrier Medicare Export (CSV from carrier/IMO)
  2. API_ENDPOINT: POST /api/atlas/introspect (column mapping)
  3. SCRIPT: normalizeData() (all mapped fields)
  4. API_ENDPOINT: POST /api/import/validate-full (dry run)
  5. SCRIPT: matchClient() + matchAccount() (dedup)
  6. API_ENDPOINT: POST /api/import/accounts (batch write)
  7. MATRIX_TAB: _ACCOUNT_MEDICARE (account_category: medicare)
  8. FRONTEND: CLIENT360 Accounts (ProDashX)
```

### Introspection Engine Logic (introspect.ts)

**hashHeaderFingerprint(headers)**
- Sort headers, lowercase, trim, join with `|`, SHA-256 hash
- Use `crypto.createHash('sha256')` (server-side only)

**profileCsvColumns(headers, rows)**
- For each column: count distinct values, detect dominant type (string/number/date/currency), compute null rate, collect sample values (up to 10)
- Type detection: try `normalizeDate()` → date, try `normalizeAmount()` → number/currency, else string

**profileCollection(docs)**
- Same as CSV profiling but on Firestore field values
- Takes pre-fetched doc snapshots (sampled server-side in the introspect endpoint)

**matchProfiles(csvProfiles, collectionProfiles, carrierFormats)**
- Scoring per CSV column:
  - Exact field name match: 100
  - In any carrier-format column_map: 95
  - Fuzzy name match (Levenshtein < 3): 80
  - Type overlap (both dates, both numbers): 60 bonus
  - Value intersection (>30% shared distinct values): 40 bonus
- Normalize to 0-100, rank alternatives
- Auto-map >= 90, suggest 50-89, skip < 50

**matchFingerprint(fingerprint, formats)**
- Exact match: return format + 100% confidence
- Partial (>80% header overlap): return format + overlap% confidence
- No match: return null

### POST /api/atlas/introspect Endpoint Flow
1. Hash headers → check `atlas/formats/` for fingerprint match
2. If exact match → return saved mapping at 100% confidence
3. If partial match → return saved mapping + flag partial confidence
4. Run `detectCarrierFormat()` from carrier-formats.ts
5. If carrier detected → use carrier column_map
6. Else → sample 50 docs from target collection, run full introspection
7. Store `IntrospectRun` in `atlas/introspect_runs/`
8. Return column_mappings with scores

---

## Builder B: ATLAS Frontend

### Architecture Decision: Three-Section Layout

ATLAS stays as an App (already in sidebar APP_ITEMS). The existing 5 flat tabs are reorganized into 3 sections with Import added as the first section:

```
ATLAS
├── 1. IMPORT (new — the action layer)
│   ├── Drop Zone (upload CSV)
│   ├── Review Queue (confirm mappings)
│   └── Import Report (ledger)
│
├── 2. REGISTRY (existing Sources + Tools — what ATLAS knows)
│   ├── Sources (carriers, data feeds, gap status)
│   └── Tools (functions, scripts, MCPs)
│
└── 3. OPERATIONS (existing Pipeline + Health + Audit — monitoring)
    ├── Pipeline (stage flow visualization)
    ├── Health (wire status, automation %)
    └── Audit (change history)
```

**Implementation:** Replace flat `Tab` type with `Section` type. Top-level nav shows 3 section pills. Each section has sub-tabs within it. Import section uses a 4-step wizard flow instead of sub-tabs.

### Files to MODIFY
| File | Changes |
|------|---------|
| `packages/ui/src/modules/AtlasRegistry.tsx` | Replace flat 5-tab layout with 3-section layout. Section 1 (Import) is entirely new. Sections 2-3 reorganize existing tabs under new groupings. ~500-700 lines of new code. |

### Section 1: Import (4-Step Wizard)

**Step 1 — Drop Zone** (TRK-178, 179)
- Full-width dashed border drop area (Forge drag-drop pattern)
- Accepts `.csv` files, parses client-side (split on comma, respect quotes)
- Category dropdown: medicare / annuity / life / bdria
- "Analyze" button → `POST /api/atlas/introspect` with headers + first 20 rows
- Loading state with "Analyzing..." indicator

**Step 2 — Mapping Review** (TRK-181)
- Card/table for each CSV column from introspection response
- Per column: header name, mapped field (editable dropdown of collection fields), confidence badge, 3 sample values
- Color coding from DeDup: green (auto >= 90), yellow (suggested 50-89), red (unmapped < 50)
- "Confirm Mapping" → `POST /api/atlas/introspect/confirm`
- Checkbox: "Save to format library" (default checked)

**Step 3 — Record Preview** (TRK-182)
- Table showing first 5 normalized records after mapping
- Each row: "New" badge or "Matched: [name] (score%)" badge
- Uses `POST /api/import/validate-full` for dry-run validation
- Shows validation warnings/errors inline

**Step 4 — Import + Report** (TRK-180, 183, 184)
- "Import [N] Records" button → `POST /api/import/batch` or `/accounts`
- Progress indicator during import
- On completion: three-column ledger table
  - Rows: Received, Auto-Matched, New Created, Updated, Duplicates Removed, Flagged, Skipped, Errors
  - Columns: Category | Count | Status (icon)
  - Footer: Input = Output total (balanced check)
- Expandable rows for drill-down (click "23 Flagged" → see the 23 records)
- Report stored via existing `startImportRun()`/`completeImportRun()` in `import_runs` collection

### Section 2: Registry (Existing — Reorganized)
- Sources tab (unchanged — existing `SourcesTab` component)
- Tools tab (unchanged — existing `ToolsTab` component)

### Section 3: Operations (Existing — Reorganized)
- Pipeline tab (unchanged — existing `PipelineTab` component)
- Health tab (unchanged — existing `HealthTab` component)
- Audit tab (unchanged — existing `AuditTab` component)

### Key Patterns to Follow
- `fetchWithAuth` for all API calls (from `./fetchWithAuth`)
- CSS variables: `var(--portal)`, `var(--bg-card)`, `var(--border)`, `var(--text-primary)`, `var(--text-muted)`
- Reuse existing AtlasRegistry primitives: `Pill`, `Badge`, `Stat`, `Empty`, `Icon`
- No `alert()`/`confirm()` — custom modal pattern from DeDup
- Material Icons via className `material-icons-outlined`

---

## Builder C: FORGE Polish

### Files to MODIFY
| File | Changes |
|------|---------|
| `packages/ui/src/modules/Forge.tsx` | Add Discovery Import section to Create Sprint modal (~150 lines) |

### TRK-185 + TRK-186: Verification Only
- `discovery_url` field: already on interfaces + forms + API. Verify type-check passes.
- Discovery Import API: `POST /api/sprints/import-discovery` already exists. Verify with dry_run test.

### TRK-187: Discovery Import UI
In the Create Sprint modal (around line 1668), below existing fields:

- Collapsible section: "Or Import from Discovery Document"
- Textarea (paste markdown) + file drop zone (.md/.txt)
- "Preview" button → `POST /api/sprints/import-discovery` with `dry_run: true`
- Preview shows: extracted sprint name, item count, item titles list
- "Import" button → commits without dry_run
- On success: refresh sprints, close modal, clear form
- Follow existing inline style pattern (Forge uses `style={{}}` not Tailwind)

---

## Execution Sequence

1. **Set plan_link on sprint** — PATCH sprint `131mgk5pOoNx3AvRL0Z4` with `plan_link: '.claude/plans/mellow-snacking-pie.md'` so FORGE links Discovery + Plan docs on the sprint
2. Write builder prompt files: `.claude/sprint10/BUILDER_A.md`, `BUILDER_B.md`, `BUILDER_C.md`
3. Spawn all 3 builders in parallel (worktree isolation)
4. Audit each builder's output against this plan
5. Merge: C → A → B (B depends on A's types being present)
6. Run `npm run type-check` (must pass 13/13)
7. Test on `npm run dev` — navigate to `/modules/atlas` Import tab
8. Update FORGE: all 18 items → `planned` status

---

## Verification Checklist

- [ ] `npm run type-check` passes 13/13
- [ ] `GET /api/atlas/wires` returns 17 wires (was 16)
- [ ] `GET /api/atlas/formats` returns empty array (collection ready)
- [ ] `POST /api/atlas/introspect` with test CSV headers returns column mappings
- [ ] AtlasRegistry shows 3 sections: Import, Registry, Operations
- [ ] Import is the default/first section
- [ ] Drop Zone accepts CSV, shows introspection results with confidence badges
- [ ] Mapping review uses DeDup color system (green/yellow/red)
- [ ] Import report shows balanced ledger (input = output)
- [ ] FORGE Create Sprint shows "Import from Discovery Document" section
- [ ] FORGE Discovery Import preview + commit works
- [ ] No `alert()`, `confirm()`, `prompt()` anywhere
- [ ] All API responses use `{ success, data, error }` pattern
