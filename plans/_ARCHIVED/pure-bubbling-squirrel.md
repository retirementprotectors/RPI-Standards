> ARCHIVED: Superseded by glimmering-baking-clarke.md on 2026-03-08

# SENTINEL v2 MI — Overhaul Plan

## Context

JDM tested the MI build and gave 6 categories of feedback. This plan addresses ALL of them in priority order. The biggest item is making BigQuery read-WRITE (edit, merge, archive, relationships). The quickest wins are License Types in the grid, DOI link fixes, and Securities parser fix.

---

## Session 1: Quick Wins (This Session)

### 1A. License Types in Grid (replaces "Licensed States")

**Problem:** "Licensed States" count is bad UX — doesn't tell Matt WHAT the agent sells. JDM has asked for License Types 10x.

**Fix:** Replace "Licensed States" column with product-type badge pills.

- **Grid column header:** "Products" (not "License Types" — per the relabel in v3.7.1)
- **Display:** Up to 4 short badge pills (MA, MS, Life, Ann, FE, LTC, etc.) + "+N" overflow
- **Abbreviation map:** Medicare_Advantage→MA, Medicare_Supplement→MS, Life→Life, Annuity→Ann, Final_Expense_Life→FE, Long_Term_Coverage→LTC, Cancer→Can, Critical_Illness→CI, Dental→Den, Disability→Dis, Hospital_Indemnity→HI, Major_Medical→MM, Short_Term_Coverage→STC
- **Data source:** 14 binary product columns already in AgentListCSG — add them to SELECT in search query
- **Files:** `SENTINEL_MarketIntelligence.gs` (search SQL), `Index.html` (grid render)

### 1B. Securities Parser — NPN → "First Last"

**Problem:** BrokerCheck/IAPD links use NPN, but NPN (National Producer Number for insurance) is NOT the same as CRD (securities). FINRA doesn't look up by NPN.

**Fix:**
- BrokerCheck URL: `https://brokercheck.finra.org/search/genericsearch/grid?query={FirstName}+{LastName}`
- SEC IAPD URL: `https://www.adviserinfo.sec.gov/IAPD/IAPDSearch.aspx` (name search, no direct URL param)
- Keep the text parser for pasted data — just fix the lookup links
- **File:** `Index.html` (Securities tab link generation)

### 1C. DOI Link Verification + Fixes

**Problem:** State DOI links aren't working. NIPR + NAIC are fine.

**Fix:** Verify all 51 URLs using Playwright. Fix broken ones. Many NAIC LION URLs (`sbs-{state}.naic.org/lion-web/...`) may have moved — NAIC migrated their system. Replace broken NAIC LION URLs with the state's actual DOI site or NAIC's centralized lookup.

**File:** `Index.html` (STATE_DOI_URLS_CLIENT object, lines 3703-3755)

### 1D. Enrichment Tab Cleanup

**Problem:**
- NPI Registry is for PHYSICIANS, not insurance agents — wrong tool entirely
- Commission Intel in enrichment sidebar is redundant (already in RPI Data tab)
- Whitepages UI is bad (data may be fine)

**Fix:**
- **Remove NPI Registry** from enrichment tool sidebar
- **Remove Commission Intel** from enrichment tool sidebar
- **Keep:** Whitepages (redesign UI), Humana, Google Contacts (wire), Workspace Dir (wire)
- **Redesign Whitepages results:** Card-based layout per result — name, phones (with type labels if available from API), emails, current address, employer. Actionable buttons: "Use this phone" / "Use this email" → saves to agent overlay (once edit system exists, Phase 2)
- **Wire Google Contacts:** `search_contacts` via `rpi-workspace` MCP — search by agent name, show if we have them in our contacts
- **Wire Workspace Directory:** `search_directory` — check if agent is in RPI domain (are they already one of us?)
- **Files:** `Index.html` (enrichment tab), `SENTINEL_MarketIntelligence.gs` (server functions)

---

## Session 2: BigQuery Write Architecture

### 2A. Create Overlay Dataset + Tables

**New BigQuery dataset:** `claude-mcp-484718.sentinel_rpi`

**6 new tables:**

| Table | Purpose |
|-------|---------|
| `agent_edits` | Field-level overrides (csg_id, field_name, field_value, edited_by, edited_at, is_active) |
| `agent_archives` | Soft-delete (csg_id, reason, archived_by, archived_at, is_active) |
| `agent_merges` | Duplicate resolution (source_csg_id → target_csg_id, merged_by, is_active) |
| `agent_notes` | Free-text notes per agent |
| `agent_relationships` | Agent → Entity → Distributor → Carrier hierarchy (flat, denormalized) |
| `audit_log` | Cross-cutting audit trail for all write operations |

**Key design decisions:**
- Field-level edits (not row copies) — surgical, reversible, composable
- All operations use `is_active` boolean — nothing physically deleted, everything undoable
- Overlays JOIN onto CSG source data via COALESCE — vendor data stays pristine
- DML via `BigQuery.Jobs.query()` (immediate consistency, same code path as reads)
- Existing `bigquery` scope in appsscript.json already covers DML — no re-auth needed

**New file:** `SENTINEL_MarketIntelligenceWrite.gs` — all write operations

**Setup:** `SETUP_CreateOverlayTables()` function creates dataset + all 6 tables

### 2B. Edit Agent Records

- Inline-editable fields in agent detail modal (phone, email, address, name corrections)
- Save → INSERT into `agent_edits` with audit logging
- Revert → set `is_active = FALSE` on the edit
- Edit history visible per agent
- Search query COALESCEs edited email/phone on top of source data
- Visual indicator (badge) on agents with active edits

### 2C. Archive Agents

- Archive button in agent detail modal with reason field
- Search query excludes archived agents by default
- "Show Archived" toggle reveals archived agents
- Unarchive action available from archived view
- Bulk archive from search results (select multiple → archive)

### 2D. Merge Agents

- Merge flow: select source (duplicate) → confirm target (keep) → preview both → confirm
- Creates `agent_merges` row
- Source agent disappears from search
- Detail view redirect: opening source shows target with "merged from" indicator
- Unmerge available
- Notes and edits stay on original CSGIDs for audit trail

### 2E. Relationship Model (Agent → Entity → Distribution → Carrier)

**Table structure** (flat, denormalized — one row per chain):
- `csg_id` → Agent
- `entity_name` + `entity_type` → Retail entity (agency, sole prop, cluster)
- `distributor_name` + `distributor_type` → Wholesale (IMO, FMO, MGA, BG)
- `carrier_name` + `carrier_naic` → Carrier
- `relationship_type` → appointed, contracted, LOA, etc.
- `effective_date` / `termination_date`

**UI:** New "Relationships" section in agent detail — table showing full chain with add/edit/remove. Bulk import for batch relationship entry.

### 2F. Notes

- Free-text notes per agent (timestamped, attributed)
- Chronological list in agent detail
- Soft-delete with is_active flag

### 2G. Bulk Operations

- Batch INSERT with 500-row chunks (not individual INSERTs)
- Bulk edit: select agents → pick field → set value
- Bulk archive: select agents → archive with shared reason
- Bulk relationship import: paste/upload CSV → INSERT into relationships table

---

## Files to Modify

| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Search SQL (add product columns, overlay JOINs, archive/merge exclusions), detail query (merge redirect, edit overlay), MI_CONFIG (overlay table refs) |
| `Index.html` | Grid columns (products badges), Securities links (First Last), DOI URLs (fix broken), Enrichment tab (remove NPI/CommIntel, redesign Whitepages, wire Contacts/Dir), Edit UI, Archive/Merge actions, Relationships tab, Notes |
| **NEW:** `SENTINEL_MarketIntelligenceWrite.gs` | All write operations: edit, revert, archive, unarchive, merge, unmerge, relationships CRUD, notes CRUD, bulk ops, audit logging, setup |

---

## Verification

### Session 1 Testing
1. Search → grid shows product badge pills (MA, MS, Life, etc.) not state count
2. Securities tab → BrokerCheck link searches by "First Last" not NPN
3. DOI links → click each major state (IA, TX, CA, FL, OH, IL, PA, GA) → correct site opens
4. Enrichment tab → only 4 tools in sidebar (Whitepages, Humana, Google Contacts, Workspace Dir)
5. Whitepages results → card layout with actionable data

### Session 2 Testing
6. Run `SETUP_CreateOverlayTables` → 6 tables created in `sentinel_rpi` dataset
7. Open agent → edit phone → save → refresh → edited phone shows
8. Archive agent → disappears from search → toggle "Show Archived" → appears → unarchive → back in search
9. Merge two agents → source disappears → opening source redirects to target → unmerge → both visible
10. Add relationship (Agent → Entity → Distributor → Carrier) → shows in detail → edit → delete
11. Bulk archive 3 agents → all disappear from search
