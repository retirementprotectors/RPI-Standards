---
name: block-direct-firestore-write
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: db\.collection\(|\.collection\(.*\)\.doc\(|getFirestore\(\)\.collection\(
exclude:
  - pattern: services/api/src/
  - pattern: services/bridge/src/
  - pattern: services/intake/
  - pattern: services/bigquery-stream/
  - pattern: \.(test|spec)\.(ts|js)
---

**BLOCKED: Direct Firestore Write Outside API**

You are writing directly to Firestore outside the authorized write paths.

**Why this is blocked:**
- All data modifications must go through the API write gate
- Direct writes bypass validation, audit logging, and the bridge dual-write layer
- This creates data integrity risks and breaks the single-source-of-truth pattern

**Authorized write paths:**
- `services/api/src/` — Cloud Run REST API (primary write gate)
- `services/bridge/src/` — Dual-write bridge (Firestore + Sheets)
- `services/intake/` — Intake Cloud Functions
- `services/bigquery-stream/` — BigQuery streaming Cloud Functions

**Fix:**
- Move your Firestore write logic into the appropriate service
- For new API endpoints: add a route in `services/api/src/routes/`
- For data ingestion: use the intake Cloud Functions
- For read-only access in portal code: use the API client (`/api/[...path]` proxy)

See: `~/Projects/toMachina/CLAUDE.md` -> API Proxy Architecture
