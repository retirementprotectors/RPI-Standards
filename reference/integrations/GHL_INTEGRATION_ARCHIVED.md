# GHL Integration Best Practices

> **Created**: February 1, 2026  
> **Source**: PRODASHX GHL sync debugging session (12+ hours)
> **Status**: ARCHIVED — GHL push code removed Sprint 5. Import/sync code retained for M&A acquisitions only. - Follow these patterns for all GHL integrations

---

## 🎯 Key Principle: Account-Based Client Qualification

**NEVER** filter contacts by arbitrary criteria like "3+ custom fields populated."

**ALWAYS** use account-based qualification:
- A contact with an account **IS** a client
- Extract contact IDs from Custom Objects (accounts) first
- Then fetch and sync those specific contacts

### Why This Matters
- GHL has 4,637 contacts but only 3,552 are real clients
- The difference: junk leads, phone-only entries, test data
- The PROOF of a real client: they have accounts (Annuities, Life, Medicare, BD/RIA)

---

## 📡 GHL Custom Objects API

### CRITICAL: Use POST for Records Search

**WRONG** (returns 0 records):
```javascript
// GET endpoint doesn't work for Custom Objects records
GET /objects/:schemaKey?locationId=xxx
```

**CORRECT**:
```javascript
// POST to records/search endpoint
POST /objects/:schemaKey/records/search
{
  "locationId": "xxx",
  "page": 1,
  "pageLimit": 100,
  "searchAfter": ["lastRecordId"]  // for pagination
}
```

### Schema Keys for RPI
```javascript
const GHL_OBJECT_TYPES = {
  annuities: 'custom_objects.annuities',
  life: 'custom_objects.life',
  medicare: 'custom_objects.medicare',
  bd_ria: 'custom_objects.bd_ria'
};
```

### Contact ID Extraction
Custom Object records link to contacts via `relations` array:
```javascript
function extractContactId(record) {
  if (record.relations && record.relations.length > 0) {
    return record.relations[0].recordId;  // This is the contact ID
  }
  return null;
}
```

### Custom Objects Field Structure

**Raw API Response Structure:**
```javascript
{
  id: "696eb0326c35cb451abb6ead",
  createdAt: "2026-01-19T22:29:06.435Z",
  relations: [{ objectKey: "contact", recordId: "D8Kn8bQx4IKfSEgTpbRz" }],
  properties: {
    account_: 28254970,           // Simple values
    status: "active",              // LOWERCASE - normalize for UI
    carriers: "nassau",
    account_value: { currency: "default", value: 46401.1 },  // Currency fields
    benefit_factors: { income_rider_name: "..." }            // Nested objects
  }
}
```

**After `transformCustomObjectRecord_()`:**
```javascript
{
  id: "696eb0326c35cb451abb6ead",
  contactId: "D8Kn8bQx4IKfSEgTpbRz",
  "custom_objects.annuities.account_": 28254970,
  "custom_objects.annuities.status": "active",
  "custom_objects.annuities.carriers": "nassau",
  "custom_objects.annuities.account_value": 46401.1,  // Currency extracted
  "custom_objects.annuities.benefit_factors.income_rider_name": "..."
}
```

**Key Patterns:**
1. **Currency fields** - GHL returns `{ currency: "default", value: X }`, extract `.value`
2. **Status normalization** - GHL returns lowercase (`active`), UI expects Title Case (`Active`)
3. **Field prefixing** - After transform, keys become `custom_objects.{type}.{field}`
4. **Contact ID** - Extract from `relations` array, not a direct field

---

## 🔗 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GHL (GoHighLevel)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  CONTACTS (~4,600)              CUSTOM OBJECTS (~7,000)                      │
│  ├── Many are junk leads        ├── ANNUITIES (linked to contacts)          │
│  ├── Phone-only entries         ├── LIFE (linked to contacts)               │
│  └── Test data                  ├── MEDICARE (linked to contacts)           │
│                                 └── BD_RIA (linked to contacts)             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    STEP 1: Get unique contact IDs from accounts
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAPID_IMPORT (IMPORT_GHL.gs)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. fetchGHLCustomObjects() → Get ALL accounts                               │
│  2. Extract unique contact IDs → ~3,500 real clients                         │
│  3. fetchGHLContactById() → Get each contact's details                       │
│  4. mapGHLContactToClient() → Transform to MATRIX format                     │
│  5. Write to _CLIENT_MASTER                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRODASHX_MATRIX (Google Sheet)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  _CLIENT_MASTER (102 columns)    _ACCOUNT_ANNUITY (47 columns)              │
│  _ACCOUNT_LIFE (44 columns)      _ACCOUNT_MEDICARE (32 columns)             │
│  _ACCOUNT_BDRIA (33 columns)                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ GAS Library Best Practices

> **var vs let:** See CLAUDE.md GAS Gotcha #7 (var vs let for module-level caching).

### Always Create Explicit Versions
```bash
clasp push --force
clasp version "v18 - Description of changes"
```

### Use developmentMode for Rapid Iteration
```json
{
  "userSymbol": "IMPORT_GHL",
  "libraryId": "xxx",
  "version": "18",
  "developmentMode": true
}
```

---

## 🐛 Debugging Strategy

### 1. Never Trust Arbitrary Filters
If sync says "80 contacts imported" but you have 3,500+ clients, **investigate**.

### 2. Count Actual Data
```javascript
// Create diagnostic endpoints
GET /config/ghl/unique-clients → Count contacts with accounts
GET /config/ghl/debug-sync → Show filter breakdown
```

### 3. Validate Assumptions
- "How many contacts?" → Fetch and count
- "How many have accounts?" → Extract contact IDs from Custom Objects
- "Why are contacts filtered?" → Log filter reasons

### 4. Don't Guess - Get Evidence
- Add console.log statements
- Create diagnostic endpoints
- Trace data through the entire pipeline

---

## 📋 Sync Endpoints (RAPID_API)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/config/ghl/unique-clients` | GET | Count unique clients from accounts (~60s) |
| `/config/ghl/sync-by-accounts` | POST | Sync contacts by account-linked IDs |
| `/config/ghl/debug-sync` | GET | Show filter analysis |
| `/config/ghl/debug-objects` | GET | Test Custom Objects API |
| `/sync/ghl/contacts` | POST | Legacy sync (uses filters) |
| `/sync/ghl/accounts` | POST | Sync account records |

### Recommended Sync Flow
1. Call `/config/ghl/unique-clients` to get contact IDs (~3,500)
2. Call `/config/ghl/sync-by-accounts` with batches of 100 IDs
3. Repeat until all contacts synced

---

## ⚠️ Common Pitfalls

1. **Wrong API endpoint for Custom Objects** - Use POST /records/search
2. **Arbitrary qualification filters** - Use account-based qualification
3. **`let` at module level in libraries** - Use `var`
4. **Not following POST redirects** - GAS web apps return 302
5. **Trusting "X contacts imported"** - Validate against actual client count
6. **Caching stale data** - Invalidate cache after writes

---

## Related Documents

- `RAPID_IMPORT/IMPORT_GHL.gs` - Implementation
- `RAPID_API/API_GHL_Sync.gs` - API endpoints
