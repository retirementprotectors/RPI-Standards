ARCHIVED: Completed/Superseded on 2026-03-13. Content consolidated into platform roadmaps.
# SENTINEL v2: Market Intelligence — Master Plan (Corrected Baseline)

## Context

Phase 1 (Agent Search overhaul) shipped as v3.6.0 (@22). During review, JDM identified critical corrections:
- **License Types** in the UI are CSG's binary product flags — NOT real state license types (Life, A&H, Variable, etc.)
- **NIPR IS the Licensing tab** — it's the source of truth for licensing/appointments/contact data, not a separate tab
- **Entity Types** (Agent vs Business Entity vs Carrier) are missing entirely from CSG data
- **Provider Network (FHIR) tools** are for healthcare providers (doctors), NOT insurance agents — zero relevance here
- **Aetna Provider tools** = provider directory, NOT agent data
- **Enrichment arsenal is massive** — 85+ relevant MCP tools weren't reflected in the original plan
- **State DOI websites** exist for free agent lookup by NPN per state

This plan is the corrected baseline for all remaining MI work.

---

## Current State

| Item | Value |
|------|-------|
| **Deployed** | v3.6.0 (@22) |
| **Phase 1** | COMPLETE — Agent Search overhaul shipped |
| **CSG Data** | 3.4M agents — good for structure/volume, data quality is garbage |
| **BigQuery** | `claude-mcp-484718.StateRepCSG_1772503365711` |
| **Tables** | AgentListCSG (3.4M), ApptListCSGbyCSGID (4.7M), ApptListCSGbyNAIC (4.7M), StateRepData (8.7M) |

### What CSG Data Actually Provides (and Doesn't)

| Has | Doesn't Have |
|-----|-------------|
| 14 binary product flags (0/1) | Real license types (Life, A&H, Variable, Surplus Lines) |
| Carrier appointment names + NAIC | Entity type (Individual vs Business vs Carrier) |
| State license numbers + dates | License class (Resident vs Non-Resident — only derivable) |
| Multiple addresses/phones/emails | License status (Active, Inactive, Cancelled, Revoked) |
| EarliestLicIssueDate | Lines of Authority (LOA) per state |
| | Appointment dates, termination reasons |
| | Regulatory actions |

**CSG = scaffolding for structure + volume. Real data comes from enrichment APIs.**

---

## Detail Modal Tab Architecture (Current → Target)

| # | Tab | Current (v3.6.0) | Target | Data Source |
|---|-----|-------------------|--------|-------------|
| 1 | **Contact** | CSG addresses, 6 emails, 8 phones | + Whitepages verified data, comms history | CSG → Whitepages, RAPID_COMMS |
| 2 | **Appointments** | CSG carrier list + NAIC, searchable | + Humana Agent API (SAN, certs, plans, production) | CSG → Humana API, future carrier APIs |
| 3 | **Licensing** | CSG product flags + StateRepData (placeholder) | **NIPR replaces this** — real license types, entity types, LOAs, state licenses, status | CSG (temp) → NIPR (authoritative) + State DOI |
| 4 | **RPI Data** | Cross-ref _PRODUCER_MASTER + NPI Registry | Done (functional) | SENTINEL_MATRIX + CMS NPPES |
| 5 | **Securities** | Stub — "Coming Soon" + manual links | FINRA BrokerCheck + SEC IAPD data | FINRA API + SEC API |
| 6 | **Enrichment** | Stub — "Coming Soon" | Whitepages person search, contact verification | Whitepages (rpi-business MCP) |

---

## Phase Roadmap

| Phase | Scope | Status | Blocker |
|-------|-------|--------|---------|
| **Phase 1** | Agent Search overhaul | **COMPLETE** (v3.6.0 @22) | — |
| **Phase 2** | Carrier Intelligence overhaul | Requirements captured | None |
| **Phase 3** | Contact + Agent Enrichment | Ready to build | None — tools exist |
| **Phase 4** | NIPR Integration (Licensing tab becomes real) | Research needed | NIPR subscription required |
| **Phase 5** | State DOI Lookups | Research needed | URL mapping per state |
| **Phase 6** | Securities (FINRA + SEC) | Research needed | API investigation |
| **Phase 7** | RAPID_COMMS Integration | Not yet scoped | None |
| **Phase 8** | DEX Integration | Not yet scoped | None |
| **Phase 9** | C3 Integration | Not yet scoped | None |
| **Dashboard** | Deferred | Revisit after enrichment proves data quality | — |
| **Cross-Reference** | Deferred | Revisit after enrichment proves data quality | — |

---

## PHASE 1: Agent Search Overhaul — COMPLETE

**Shipped v3.6.0 (@22) on 2026-03-02.**

What was built:
- 2-row filter bar (First Name, Last Name, NPN, Phone, ZIP, State, Carrier multi-select, License Type, First Licensed range, Resident checkbox)
- Results grid (Name, NPN, State, City, License Type badges, Carrier count, Email, Phone)
- 6-tab detail modal (Contact, Appointments, Licensing, RPI Data, Securities stub, Enrichment stub)
- Carrier multi-select with 1hr cached BigQuery list
- NPI Registry lookup via CMS NPPES API (free, wired in RPI Data tab)
- Add to Pipeline with duplicate detection
- Market Dashboard, Carrier Intelligence, Cross-Reference views (pre-existing, unchanged)

**Known debt (carried forward):**
- "License Type" filter + badges use CSG product flags — relabel or replace when NIPR flows in (Phase 4)
- No entity type distinction — requires NIPR data (Phase 4)
- Results grid "License Types" column shows CSG product abbreviations, not real license types

---

## PHASE 2: Carrier Intelligence Overhaul

### Scope
Overhaul the Carrier Intelligence view to provide carrier-level detail with distribution management.

### Filter Bar
| Filter | Type | Source |
|--------|------|--------|
| Carrier Name | Searchable dropdown | Cached carrier list (already built — `getCarrierListForUI()`) |
| Product Lines | Multi-select | CSG product flags for now, NIPR LOAs later |
| Distribution Type | Multi-select | TBD — define distribution types (Direct, IMO, MGA, etc.) |

### Carrier Detail Section
- Agent count for this carrier (from BigQuery)
- Distribution field + CREATE NEW feature / assignment
- Cross-reference RAPID_MATRIX `_CARRIER_MASTER` for internal carrier data
- Product types the carrier offers (from MATRIX)
- Top states by agent count for this carrier
- SERFF (System for Electronic Rates & Forms Filing) — research API for state regulatory filings

### Backend
- `getCarrierDetailForUI(carrierName)` — agent count, state breakdown, internal cross-ref
- Distribution type management (SENTINEL_MATRIX schema addition if needed)

### Files to Modify
| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Add `getCarrierDetailForUI()`, distribution management |
| `Index.html` | Carrier Intel filter bar, carrier detail panel, distribution UI |

---

## PHASE 3: Contact + Agent Enrichment

### Scope
Wire existing MCP tools into the detail modal. No new APIs needed — we already have the tools.

### 3A: Enrichment Tab (Whitepages)

**Currently stubbed.** Wire in Whitepages person search.

| Tool | MCP | What It Does |
|------|-----|-------------|
| `search_person` | rpi-business | Find verified phone, email, address, DOB, employer, relatives, properties by name/phone/address |
| `get_person` | rpi-business | Full person record by Whitepages ID (free — no query consumed) |
| `search_property` | rpi-business | Property ownership lookup by address |
| `check_whitepages_usage` | rpi-business | Monitor trial query consumption (free) |

**UI**: Search button in Enrichment tab → calls `search_person` with agent's name + known address/phone → displays verified contact data, employment, relatives, property ownership.

**Backend**: New `enrichAgentWhitepagesForUI(csgId)` — fetches agent from BigQuery, calls Whitepages `search_person` via GAS `UrlFetchApp` (Whitepages API key in Script Properties), returns enriched data.

**Note**: Whitepages is on 14-day trial (50 queries). Usage tracking built in via `check_whitepages_usage`.

### 3B: Carrier Agent Data (Appointments Tab Enhancement)

Wire Humana Agent API tools into Appointments tab. Only Humana has agent-level APIs currently.

| Tool | MCP | What It Does |
|------|-----|-------------|
| `humana_get_agent` | rpi-healthcare | Agent profile by SAN — status, approval, contracts |
| `humana_get_agent_plans` | rpi-healthcare | Plans agent is contracted to sell |
| `humana_get_agent_certifications` | rpi-healthcare | Product certifications (Medicare, Life, Annuity) |
| `humana_get_agent_licenses` | rpi-healthcare | State licenses + status from Humana's perspective |
| `humana_get_bam_report` | rpi-healthcare | Book of business — premium/policy counts |
| `humana_get_aped_report` | rpi-healthcare | Production metrics — enrollments, changes |

**UI**: "Carrier API Lookups" section in Appointments tab (placeholder already exists). If agent has Humana appointment, show "Look up Humana data" button → fetches SAN-based data → displays certs, plans, licenses, production.

**Challenge**: Need to map CSG agent to Humana SAN. Options:
1. NPN-based lookup (if Humana API supports NPN → SAN mapping)
2. Manual SAN entry field
3. Cross-ref with `_PRODUCER_MASTER` which may have SAN

**Backend**: New `enrichAgentHumanaForUI(csgId)` — route through healthcare-mcps Cloud Run or direct MCP call.

### 3C: Commission Cross-Reference (RPI Data Tab Enhancement)

| Tool | MCP | What It Does |
|------|-----|-------------|
| `get_agent_rates` | rpi-business | RPI commission levels for agent by carrier |
| `identify_level` | rpi-business | Reverse-lookup agent's tier from a rate |
| `list_supported_carriers` | rpi-business | All carriers with rate data |

**UI**: If agent is found in RPI system (RPI Data tab), show commission tier info alongside existing cross-ref data.

### Files to Modify
| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Add `enrichAgentWhitepagesForUI()`, `enrichAgentHumanaForUI()` |
| `Index.html` | Enrichment tab content, Appointments tab Humana section, RPI Data tab commission info |

---

## PHASE 4: NIPR Integration — Licensing Tab Becomes Real

### Scope
NIPR (National Insurance Producer Registry) **IS** the Licensing tab. Replace CSG product flags with authoritative licensing data.

### What NIPR Provides (That CSG Doesn't)

| Data | Description |
|------|-------------|
| **License Type** | Life, Accident & Health, Variable, Surplus Lines, Personal Lines, Property & Casualty, etc. |
| **Entity Type** | Individual, Business Entity, Carrier |
| **License Class** | Resident, Non-Resident |
| **License Status** | Active, Inactive, Cancelled, Expired, Revoked |
| **Lines of Authority (LOA)** | Detailed LOA per state per license |
| **Appointment Details** | Carrier appointments with effective/termination dates and reasons |
| **Regulatory Actions** | Disciplinary actions, if any |
| **Contact Data** | NIPR-maintained (authoritative vs CSG compiled/stale) |

### NIPR Access Model
- **Subscription**: Per-transaction fees, no minimums, no setup/cancellation fees
- **Free**: NPN lookup (basic validation only)
- **Paid**: Detailed PDB (Producer Database) queries for license types, LOAs, appointments
- **Blocker**: Need to complete NIPR Producer Database Access form + license agreement
- **Action Required**: Research exact pricing, complete application

### Licensing Tab Redesign

**Current (CSG placeholder):**
- 14 binary product badges
- Stats: EarliestLicIssueDate, NumberOfLicensedStates, NumberofProducts
- State license table: State, License#, Issued, Expires, Resident flag

**Target (NIPR-powered):**
- **Entity Type badge**: Individual / Business Entity / Carrier
- **Active License Types**: Life, A&H, Variable, etc. (real types, not product flags)
- **Lines of Authority**: Detailed LOA breakdown per state
- **State License Table**: State, License#, Type, Class (Resident/Non-Resident), Status (Active/Inactive/etc.), Issued, Expires, LOAs
- **Appointment History**: Carrier appointments with effective dates, termination dates, termination reasons
- **Regulatory Actions**: If any exist

### Backend
- `getAgentNiprDataForUI(npn)` — call NIPR PDB API with NPN, return full licensing profile
- Cache results (NIPR charges per transaction — cache aggressively)
- Graceful fallback to CSG data if NIPR unavailable

### Filter Bar Updates
- Replace "License Type" dropdown (CSG product flags) with real license type options from NIPR
- Add "Entity Type" filter (Individual, Business Entity, Carrier)
- Add "License Status" filter (Active, Inactive, etc.)

### Results Grid Updates
- Replace "License Types" badge column with real license type abbreviations from NIPR
- Add entity type indicator

### Files to Modify
| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Add `getAgentNiprDataForUI()`, update `searchAgentsForUI()` filters |
| `Index.html` | Rebuild Licensing tab, update filter bar, update results grid |

---

## PHASE 5: State DOI Lookups

### Scope
Free, authoritative state-level license verification via state Department of Insurance websites. Complement to NIPR (or alternative if NIPR subscription is deferred).

### Approach Options

| Approach | Complexity | Value | Cost |
|----------|-----------|-------|------|
| **Manual links** — generate clickable URL per state DOI site with NPN pre-filled | Low | Quick reference, user verifies manually | Free |
| **Playwright scraping** — automated lookup per state | Medium-High | Auto-pull license data from state sites | Free but fragile |
| **NIPR API** — single API for all 50 states | Low (API call) | Authoritative, all states, structured data | Subscription |

### State DOI URL Reference (No Standardized Pattern)
Each state has its own system. Examples:
- California: `https://cdicloud.insurance.ca.gov/cal/LicenseNumberSearch`
- New York: `https://myportal.dfs.ny.gov/nylinxext/elsearch.alis`
- Ohio: `https://gateway.insurance.ohio.gov/UI/ODI.Agent.Public.UI/`
- NAIC master directory: `http://www.naic.org/state_web_map.htm`

### Recommended Approach
**Start with manual links (Phase 5A)**, build toward automated lookup (Phase 5B) if NIPR subscription is deferred.

**Phase 5A**: Map state DOI URLs for all 50 states + DC. In Licensing tab, show "Verify on [State] DOI" link per state license row. Low effort, high value.

**Phase 5B** (optional): Playwright-based automated lookup for high-priority states (Iowa, surrounding states, states with most agents in pipeline).

### Files to Modify
| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Add `STATE_DOI_URLS` mapping, `getStateDOILink(state)` |
| `Index.html` | Add DOI link column to state license table in Licensing tab |

---

## PHASE 6: Securities (FINRA + SEC)

### Scope
Securities tab — FINRA BrokerCheck + SEC IAPD. This is for agents who also hold securities licenses (Series 6/7/63/65/66).

### FINRA BrokerCheck
- Public lookup: `https://brokercheck.finra.org/`
- Research: Does a public API exist? Or Playwright scraping?
- Data: Broker registration, disclosures, employment history, exam results

### SEC IAPD (Investment Adviser Public Disclosure)
- Public lookup: `https://adviserinfo.sec.gov/`
- Research: Does a public API exist?
- Data: Investment Adviser registration, firm details, regulatory actions

### Securities Tab Content (Target)
- FINRA registration status
- Series licenses held (6, 7, 63, 65, 66)
- Employment history
- Disclosures / regulatory actions
- SEC/RIA registration status
- Manual lookup links (immediate) + API data (when available)

### Files to Modify
| File | Changes |
|------|---------|
| `SENTINEL_MarketIntelligence.gs` | Add `getAgentSecuritiesForUI()` if APIs available |
| `Index.html` | Build Securities tab content |

---

## PHASE 7: RAPID_COMMS Integration

### Scope
Full communication workflow within SENTINEL deals and agent outreach.

### Available Tools (rpi-comms MCP)
| Category | Tools | Purpose |
|----------|-------|---------|
| **SMS** | `comms_send_sms`, `comms_get_sms_status`, `comms_list_sms` | Send/track SMS |
| **Email** | `comms_send_email`, `comms_send_bulk_email`, `comms_get_email_activity`, `comms_get_delivery_stats` | Send/track email |
| **Voice** | `comms_initiate_call`, `comms_get_call_status`, `comms_list_recordings` | Outbound calls |
| **Templates** | `comms_list_templates`, `comms_create_template` | Email template management |
| **Campaigns** | `campaign_execute_send`, `campaign_execute_batch`, `campaign_schedule_sequence` | Multi-step sequences |

### Integration Points
- Contact tab: "Send SMS" / "Send Email" buttons per agent
- Deal detail: Communication history (SMS + email + call log)
- Pipeline: Outreach campaigns for prospecting stage
- Activity log: All comms logged to SENTINEL_MATRIX

---

## PHASE 8: DEX Integration — NOT YET SCOPED

Document management within SENTINEL deals — NDA, LOI, Purchase Agreement generation + tracking via DEX + PDF_SERVICE.

---

## PHASE 9: C3 Integration — NOT YET SCOPED

Campaign engine for B2B prospecting outreach via C3 content/campaign manager.

---

## Dashboard — DEFERRED

Data is trash (CSG product flags). Revisit after NIPR (Phase 4) proves real data quality. No point building dashboards on incomplete flags.

## Cross-Reference — DEFERRED

Pending enrichment. CSG-to-RPI cross-ref exists (Phase 1), but deeper cross-referencing needs real data.

---

## Enrichment Arsenal (Full Tool Inventory)

### Contact Enrichment
| Tool | MCP | Data Returned |
|------|-----|---------------|
| `search_person` | rpi-business (Whitepages) | Verified phone, email, address, DOB, employer, relatives, properties |
| `get_person` | rpi-business (Whitepages) | Full person detail (free, cached) |
| `search_property` | rpi-business (Whitepages) | Property ownership, residents, APN |
| `search_contacts` | rpi-workspace (Google People) | RPI Google Contacts cross-ref |
| `search_directory` | rpi-workspace (Google People) | RPI Workspace directory cross-ref |

### Carrier Agent Data (Humana Only — Other Carriers Don't Expose Agent APIs)
| Tool | MCP | Data Returned |
|------|-----|---------------|
| `humana_get_agent` | rpi-healthcare | Agent profile by SAN |
| `humana_get_agent_plans` | rpi-healthcare | Contracted plans |
| `humana_get_agent_certifications` | rpi-healthcare | Product certifications |
| `humana_get_agent_licenses` | rpi-healthcare | State licenses from Humana |
| `humana_get_bam_report` | rpi-healthcare | Book of business production |
| `humana_get_aped_report` | rpi-healthcare | Agent production metrics |

### Commission Intelligence
| Tool | MCP | Data Returned |
|------|-----|---------------|
| `get_agent_rates` | rpi-business | Commission rates by carrier/state/plan |
| `identify_level` | rpi-business | Agent's commission tier from a rate |
| `list_supported_carriers` | rpi-business | All carriers with rate data (15+) |

### NPI Registry (Already Wired — Phase 1)
| Tool | MCP | Data Returned |
|------|-----|---------------|
| `lookup_npi` | rpi-healthcare / direct UrlFetchApp | Provider type, specialty, addresses, taxonomy |
| `validate_npi` | rpi-healthcare | NPI format validation |

### Communications (Phase 7)
| Tool | MCP | Data Returned |
|------|-----|---------------|
| `comms_send_sms` | rpi-comms | Send SMS, get message SID |
| `comms_send_email` | rpi-comms | Send email (template or raw) |
| `comms_initiate_call` | rpi-comms | Outbound call with recording |
| `comms_list_sms` | rpi-comms | SMS history by contact |
| `comms_get_email_activity` | rpi-comms | Email history by contact |
| `campaign_execute_send` | rpi-comms | Campaign send with audit logging |

### NOT Relevant to Agent Data (Do Not Conflate)
| Tool Category | MCP | Why NOT Relevant |
|---------------|-----|-----------------|
| Provider Network (FHIR) | rpi-healthcare | Checks if DOCTORS are in-network for Medicare plans — NOT insurance agents |
| Aetna Provider tools | rpi-healthcare | Provider directory for healthcare providers — NOT agent/producer data |
| Medicare Plan tools | rpi-healthcare | Plan comparison for client quoting — NOT agent intelligence |
| Blue Button / Claims | rpi-healthcare | Patient health data — NOT agent data |
| ICD-10 / CMS Coverage | rpi-healthcare | Clinical codes — NOT agent data |

---

## Implementation Priority (For JDM Decision)

| Option | What Ships | Dependencies |
|--------|-----------|-------------|
| **Phase 2 next** | Carrier Intelligence overhaul | None — builds on existing carrier data |
| **Phase 3 next** | Enrichment wiring (Whitepages + Humana) | None — tools already exist, just need to wire them |
| **Phase 4 next** | NIPR (real license types replace CSG garbage) | NIPR subscription application + approval |
| **Phase 5A next** | State DOI manual links | None — just URL mapping |
| **Relabel now** | Quick fix — rename CSG "License Types" to "Products" honestly | None — 30 min change |

**Recommended order**: Phase 3 → Phase 5A → Phase 2 → Phase 4 (while NIPR subscription processes) → Phase 6 → Phase 7-9

Rationale: Phase 3 uses tools we already have (zero blockers). Phase 5A is free and fast. Phase 2 builds carrier view. Phase 4 (NIPR) has a subscription blocker that should be started early but implemented when approved.
