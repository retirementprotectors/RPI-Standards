# CSG Actuarial API Integration — Session Handoff

> **Created**: 2026-03-09
> **Context**: JDM + Claude Code research session discovered CSG Actuarial's full API documentation. This is NET NEW information — zero CSG references exist anywhere in QUE-Medicare or healthcare-mcps today.
> **Action**: Read this, then start building.

---

## TL;DR

CSG Actuarial has a fully documented REST API that provides **all-carrier** Medicare Supplement, Final Expense, Hospital Indemnity, and Dental/Vision quoting. RPI already has a CSG account with portal access. The API docs are on Apiary. This replaces the current approach of chasing individual carrier API approvals one by one (Humana has been pending since Jan 29).

**CSG = the source of truth for Med Supp + ancillary quoting data.** Carrier-direct APIs (Humana, Aetna, etc.) remain for MA/PDP and patient-level data (FHIR).

---

## CSG API — Full Technical Reference

### Authentication

```
POST https://api.csgactuarial.com/v1/auth.json
Content-Type: application/json

{
  "api_key": "<YOUR_API_KEY>",
  "portal_name": "csg_individual"
}

// OR authenticate with email/password:
{
  "email": "josh@retireprotected.com",
  "password": "csg1234!",
  "portal_name": "csg_individual"
}
```

**Response (200):**
```json
{
  "token": "cffc66a5...",
  "expires_date": "2026-03-09T22:42:39.861010",
  "user": {
    "products": [{ "plan_code": "admin", "state": "active" }],
    "api_key": "<YOUR_API_KEY>",
    "email": "email@example.com"
  },
  "key": "session_key_here",
  "created_date": "2026-03-09T14:42:39.860960"
}
```

**Token rules:**
- Valid for **8 hours**
- Use in header: `x-api-token: <token>`
- Expired token returns **403** with message "Session Expired Error"
- Handle expiry: re-auth on 403, or CRON refresh every 7 hours
- Token can be shared across multiple simultaneous requests

### Sub-APIs (All Documented on Apiary)

| API | Docs URL | Base Path | Description |
|-----|----------|-----------|-------------|
| **Auth/Getting Started** | https://csgapi.docs.apiary.io/ | `/v1/auth.json` | Token management |
| **Medicare Supplement** | https://medigapapi.docs.apiary.io/ | `/v1/med_supp/` | Med Supp rates, all carriers |
| **Medicare Advantage** | https://medicareadvantageapi.docs.apiary.io/ | TBD | MA plan data |
| **Final Expense Life** | https://finalexpenselifeapi.docs.apiary.io/ | TBD | FE rates |
| **Hospital Indemnity** | https://hospitalindemnityapi.docs.apiary.io/ | TBD | HI rates |
| **Dental/Vision/Hearing** | https://dentalvisionandhearingapi.docs.apiary.io/ | TBD | DVH rates |

**API base URL for all:** `https://api.csgactuarial.com`

### Medicare Supplement API — Endpoint Detail

#### Quotes (GET)
```
GET https://api.csgactuarial.com/v1/med_supp/quotes.json
Headers: x-api-token: <token>

Query params:
  age=65          (required)
  gender=M|F      (required)
  zip5=50309      (required)
  tobacco=0|1     (required)
  plan=A|B|C|D|F|G|N|...  (optional, filter by plan)
  naic=79413      (optional, filter by carrier NAIC)
  fips_code=19153 (optional, county-level filter)
  county=Polk     (optional, mutually exclusive with fips_code)
  apply_discounts=0|1  (optional, apply HHD discounts)
```

**Rate notes:**
- Rates in **pennies** (divide by 100 for dollars)
- EFT discount included by default
- Rates bounded by effective/expiration date of today
- Response includes `annual`, `month`, `quarter`, `semi_annual` periods

#### Quotes (POST)
Same parameters, POST body instead of query string.

#### Single Quote
```
GET https://api.csgactuarial.com/v1/med_supp/quote/{key}.json
Headers: x-api-token: <token>
```

#### Plan Rates (Cached)
```
GET https://api.csgactuarial.com/v1/med_supp/plan_rates.json
Headers: x-api-token: <token>
```

#### Plan Names
```
GET https://api.csgactuarial.com/v1/med_supp/plan_names.json
Headers: x-api-token: <token>
```

#### Underwriting Criteria
```
GET https://api.csgactuarial.com/v1/med_supp/underwriting.json
Headers: x-api-token: <token>
```

#### Companies (NO TOKEN REQUIRED)
```
GET https://api.csgactuarial.com/v1/med_supp/companies.json
```
Use `name_full` property to filter by company name.

#### Plan Details
```
GET https://api.csgactuarial.com/v1/med_supp/plan_details.json
Headers: x-api-token: <token>
```

### Riders (WI + MN State Specials)

Wisconsin and Minnesota have state-special plans with optional riders:

| Plan | Riders Available |
|------|-----------------|
| WI_PLAN_1 (≈Plan N) | WIR_UHR1, WIR_UHR3, WIR_PTA, WIR_TVL |
| WI_PLAN_2 (≈Plan G) | WIR_UHR1, WIR_UHR3, WIR_PTA, WIR_TVL, WIR_EXCS |
| WI_PLAN_3 (≈Plan F) | WIR_UHR1, WIR_UHR3, WIR_PTA, WIR_TVL, WIR_EXCS, WIR_PTB |
| MN_PLAN_1 (≈Plan N) | MNR_PTA |
| MN_PLAN_2 (≈Plan G) | MNR_PTA, MNR_EXCS |
| MN_PLAN_3 (≈Plan F) | MNR_PTA, MNR_EXCS, MNR_PTB |

Rider rates are in dollars (not pennies). Add rider rate to base plan rate.

### Household Discount (HHD) Logic

The `view_type` array on each quote controls display:

| `view_type` | HHD Off | HHD On | Discount Calc |
|-------------|---------|--------|---------------|
| `["sans_hhd"]` | SHOW | HIDE | None — display as-is |
| `["with_hhd"]` | HIDE | SHOW | None — pre-calculated |
| `[]` (empty) | SHOW | SHOW | DYNAMIC — apply from `discounts` array |

For dynamic discounts: `final_rate = base_rate - sum(discount_amounts)`. Percentage discounts: `base_rate × (value ÷ 100)`. Fixed discounts: use value directly.

---

## What Exists in QUE-Medicare Today

### Current Med Supp Approach (Humana Only — STALLED)

**QUE-Medicare `api/server.js` lines 706-746:**
```javascript
// GET /api/humana/plans/medsup — Humana Med Supp plans
app.get('/api/humana/plans/medsup', async (req, res) => { ... });

// GET /api/humana/plans/medsup/quotes — Humana Med Supp quotes
app.get('/api/humana/plans/medsup/quotes', async (req, res) => {
    const url = new URL(`${HUMANA_BASE()}/v2/plan-info/medicare-supplement/quotes`);
    // ... requires Humana OAuth token
});
```

**MCP tools in `rpi-healthcare-mcp/src/humana-fhir-tools.js`:**
- `humana_get_medsup_plans` (line 247)
- `humana_get_medsup_quotes` (line 258)

**Status:** Humana developer portal approval PENDING since January 29, 2026. These endpoints cannot be used until Humana approves.

### Current Data Source Map

| Product | Source | Status |
|---------|--------|--------|
| **MA/PDP Plans** | CMS PBP public data | LIVE |
| **Drug Coverage** | CMS Formulary files | LIVE |
| **Pharmacy Networks** | CMS Pharmacy files | LIVE |
| **Provider Directories** | Carrier FHIR APIs | LIVE (Humana, Cigna, Centene, Devoted, Aetna) |
| **Med Supp Rates** | Humana-only | BLOCKED (pending approval) |
| **Final Expense** | None | Not started |
| **Hospital Indemnity** | None | Not started |
| **Dental/Vision** | None | Not started |

---

## Integration Plan

### Architecture: Where CSG Fits

```
┌──────────────────────────────────────────────────────┐
│                QUE GAS WEB APP                        │
│    UI: Plan Search + Quote + Compare + Enroll         │
└──────────────────┬───────────────────────────────────┘
                   │ UrlFetchApp
┌──────────────────▼───────────────────────────────────┐
│          healthcare-mcps API (Cloud Run)               │
│                                                        │
│  MAPD/PDP (existing):                                  │
│    /api/plans, /api/quote, /api/formulary/*            │
│    Source: CMS public data                             │
│                                                        │
│  Med Supp + Ancillary (NEW — CSG):                     │
│    /api/csg/auth        → CSG token management         │
│    /api/csg/medsup      → Med Supp quotes (all carrier)│
│    /api/csg/fex         → Final Expense quotes         │
│    /api/csg/hi          → Hospital Indemnity quotes    │
│    /api/csg/dental      → Dental/Vision quotes         │
│    /api/csg/companies   → Carrier list (no auth)       │
│    /api/csg/plans       → Plan names + details         │
│    /api/csg/underwriting→ UW criteria                  │
│                                                        │
│  Provider Networks (existing — keep):                   │
│    /api/provider/*                                     │
│    Source: Carrier FHIR APIs                           │
└──────────────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   CMS Data    CSG API    Carrier FHIR
   (MA/PDP)   (Med Supp   (Provider
              + Ancillary)  Networks)
```

### Implementation Steps

#### Phase 1: CSG Auth + Med Supp Quoting (Priority)
1. **Add CSG client module** to `healthcare-mcps/` — handles auth, token caching (7hr refresh), request wrapper
2. **Add `/api/csg/medsup` endpoint** to `server.js` — proxies to CSG Med Supp API with zip, age, gender, tobacco, plan filters
3. **Add `/api/csg/companies` endpoint** — carrier list (no auth needed, good for testing connectivity first)
4. **Add `/api/csg/plans` endpoint** — plan names + details for UI dropdowns
5. **Wire QUE GAS frontend** — add Med Supp tab/section to UI, call new endpoints
6. **Handle riders** — WI/MN state special logic in frontend
7. **Handle HHD** — Household discount display logic per `view_type`

#### Phase 2: Ancillary Products
8. **Final Expense** — `/api/csg/fex` endpoint
9. **Hospital Indemnity** — `/api/csg/hi` endpoint
10. **Dental/Vision** — `/api/csg/dental` endpoint
11. **UI for each** — Tabs or sections in QUE

#### Phase 3: Replace Humana-Only Code
12. **Deprecate** `/api/humana/plans/medsup` and `/api/humana/plans/medsup/quotes` endpoints
13. **Deprecate** `humana_get_medsup_plans` and `humana_get_medsup_quotes` MCP tools
14. Keep Humana FHIR for Provider Directory + Patient Access (not quoting)

### CSG Credentials

| Item | Value |
|------|-------|
| **Portal** | https://tools.csgactuarial.com |
| **Email** | josh@retireprotected.com |
| **Password** | csg1234! |
| **Portal Name** | `csg_individual` |
| **API Key** | PENDING — Brien Welch checking with devs (as of 2026-03-06) |
| **Contact** | Brien Welch, bwelch@csgactuarial.com |

**Store credentials in Script Properties / env vars. NEVER hardcode.**

### Subscription Gaps

These features on the CSG portal show "not included in your current subscription":
- **Data Feeds** — may be needed for SERFF bulk data
- **Agent Lists** — recruiting data
- **Rate Change Report** — rate change tracking

The quoting API access may require an API key (separate from portal login). Brien is getting this from his dev team.

---

## SERFF Raw Data Pipeline (Separate Workstream)

Brien Welch shared normalized closed block data via Google Drive on 2026-03-06:
- **File**: https://drive.google.com/file/d/17ehH7nmGC3_7lzhlXQjWG9qTZNbm5DOz/view?usp=sharing
- **Format**: Normalized data in CSG standard feed format
- **API access**: Brien confirmed data is loaded to their cloud and will be available via API. Waiting on endpoint details + API key.

**Planned pipeline (once API endpoints are confirmed):**
```
CSG SERFF Data API → BigQuery → Campaign targeting (C3/PRODASHX)
                            → PRODASHX MATRIX enrichment
                            → Rate change tracking
                            → Competitive intelligence
```

**Email sent 2026-03-09** asking Brien to confirm: are the SERFF data feed API endpoints built, or still in development? The published Apiary docs only show quoting endpoints, not bulk data feeds.

---

## Files to Modify

| File | What to Do |
|------|-----------|
| `healthcare-mcps/` — new `src/csg-client.js` | CSG auth + token caching + request wrapper |
| `healthcare-mcps/api/server.js` | Add `/api/csg/*` endpoints |
| `rpi-healthcare-mcp/src/` — new `csg-tools.js` | MCP tools for CSG API |
| `QUE-Medicare/Code.gs` | Add proxy functions for CSG endpoints |
| `QUE-Medicare/Scripts.html` | Med Supp quoting UI |
| `QUE-Medicare/Index.html` | Med Supp tab/section |
| `QUE-Medicare/CLAUDE.md` | Update data sources, add CSG references |
| `QUE-Medicare/docs/CARRIER_API_ACCESS.md` | Add CSG section |

---

## Key Decisions Already Made

1. **CSG is the source of truth for Med Supp + ancillary quoting** — not individual carrier APIs
2. **Carrier FHIR APIs remain for MA/PDP and patient-level data** — CSG doesn't replace those
3. **Humana Med Supp code will be deprecated** — replaced by CSG (all carriers)
4. **CSG credentials go in Script Properties / env vars** — never hardcoded
5. **SERFF bulk data is a separate workstream** — waiting on Brien for API endpoint details

---

## Quick Start for New Session

```bash
cd /Users/joshd.millang/Projects/PRODASHX_TOOLS/QUE/QUE-Medicare
```

1. Read this handoff document ✓ (you just did)
2. Read `CLAUDE.md` for project context
3. Start with Phase 1, Step 3 — hit the companies endpoint first (no auth needed) to verify connectivity:
   ```
   GET https://api.csgactuarial.com/v1/med_supp/companies.json
   ```
4. Then authenticate and pull Med Supp quotes
5. Build the `csg-client.js` module
6. Wire up the endpoints
7. Build the UI

**The Apiary docs have example curl commands and response schemas for every endpoint. Use them.**

---

*"Not estimates. Not projections. Math." — And now we have the data source to prove it.*
