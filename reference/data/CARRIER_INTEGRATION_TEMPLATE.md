---

# Carrier Integration Template

> Use this template when onboarding a new carrier integration. Copy, fill in, and add to `CARRIER_INTEGRATION_MATRIX.md`.
>
> **Last updated:** 2026-02-16

---

## [Carrier Name]

### Overview

| Attribute | Value |
|-----------|-------|
| **Products** | [MAPD, PDP, MedSupp, IUL, FIA, MYGA, etc.] |
| **Domain** | [HEALTH / WEALTH / BOTH] |
| **IMO Intermediary** | [SPARK, Signal, Gradient, Direct, etc.] |
| **Portal URL** | [URL] |
| **Current Status** | [Not Started / Manual / Semi-auto / Automated] |
| **Priority** | [CRITICAL / HIGH / MEDIUM / LOW] |
| **RAPID_IMPORT Module** | [File name, or "Planned"] |

### Current Integration

Describe what exists today:
- How data currently flows (or doesn't)
- Which IMPORT modules handle this carrier
- Any manual steps involved

### Available APIs

| API | Type | Auth Method | Documentation | Status |
|-----|------|-------------|---------------|--------|
| [API name] | [REST/FHIR/SOAP/Webhook] | [OAuth/API Key/Basic/None] | [URL or "Private"] | [Available/Planned/None] |

### Data Types

| Type | Current Method | Target Method | Status |
|------|---------------|---------------|--------|
| Client demographics | [Method or N/A] | [Target] | [Auto/Semi-auto/Manual/Planned/Not Started] |
| Account/policy data | | | |
| Commission | | | |
| New business/pending | | | |
| Reactive service/claims | | | |

### Field Mapping

| External Field | MATRIX Tab | MATRIX Field | Notes |
|----------------|-----------|--------------|-------|
| [carrier_field] | [_CLIENT_MASTER] | [field_name] | [any transformation needed] |
| | | | |

### Setup Requirements

**JDM Actions:**
1. [ ] [What JDM needs to do - e.g., "Enroll in developer program"]
2. [ ] [Obtain credentials]
3. [ ] [Confirm access through IMO]

**Technical Setup:**
1. [ ] Add Script Properties: `[CARRIER]_API_KEY`, `[CARRIER]_API_URL`
2. [ ] Create `IMPORT_[Carrier].gs` following existing patterns
3. [ ] Add to `syncAll[Category]()` orchestrator
4. [ ] Update `DATA_SOURCE_REGISTRY.md` cascade table
5. [ ] Update `CARRIER_INTEGRATION_MATRIX.md` carrier section
6. [ ] If webhook: Add handler to `RAPID_API/API_[Carrier].gs`
7. [ ] If new MATRIX fields: Update TAB_SCHEMAS in `RAPID_CORE/CORE_Database.gs`

### Integration Cascade Position

Where does this carrier fall in the priority cascade?

```
1. Real-time API        → [Yes/No - details]
2. Webhook push         → [Yes/No - details]
3. Scheduled API pull   → [Yes/No - details]
4. SFTP/bulk file       → [Yes/No - details]
5. Manual portal + FIX_ → [Yes/No - details]
6. Paper/fax/phone      → [Yes/No - details]
```

### Dedup Strategy

How do we match incoming records to existing MATRIX data?

| Match Key | Priority | Tab | Field |
|-----------|----------|-----|-------|
| [e.g., policy_number] | Primary | [_ACCOUNT_LIFE] | [policy_number] |
| [e.g., SSN last 4 + DOB] | Fallback | [_CLIENT_MASTER] | [ssn_last4 + dob] |
| [e.g., name + DOB] | Last resort | [_CLIENT_MASTER] | [first_name + last_name + dob] |

### Testing Checklist

- [ ] `TEST_[Carrier]Connection()` passes
- [ ] DryRun import shows correct match count
- [ ] No duplicate records created
- [ ] PHI fields properly handled (no logging, no Slack)
- [ ] Commission maps to correct `_REVENUE_MASTER` records
- [ ] New MATRIX fields populated correctly
- [ ] Reconciliation catches any new duplicates

### Notes

[Any carrier-specific quirks, gotchas, or important context]

---

## Quick Reference: Existing Patterns

When building a new carrier integration, reference these existing implementations:

| Pattern | Example File | Key Function |
|---------|-------------|--------------|
| Webhook handler | `RAPID_API/API_Spark.gs` | `handleWebhook()` |
| CSV bulk import | `IMPORT_BoBImport.gs` | `FIX_ImportBoBData()` |
| XLSX enrichment | `IMPORT_BoBEnrich_Archive.gs` | `FIX_EnrichLifeFromCarrier()` |
| API sync | `IMPORT_Revenue.gs` | `fetchStateableCommissions()` |
| Comms sync | `IMPORT_Comms.gs` | `syncTwilioMessages()` |
| FHIR integration | rpi-healthcare MCP | `aetna_fetch_patient_data` |

---

*Copy this template for each new carrier. Delete sections that don't apply.*
