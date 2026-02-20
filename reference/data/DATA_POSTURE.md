# DATA_POSTURE — Current State of Data Quality

> Pillar 2 of the Data Operating System. Documents the current state of data quality across all MATRIX tabs.

## PRODASH_MATRIX Health Summary

(Last updated: 2026-02-20)

### Tab-Level Metrics

| Tab | Est. Records | Status |
|-----|-------------|--------|
| `_CLIENT_MASTER` | ~4,650 | Normalized (Phase 1-4). Contact validation pending. |
| `_ACCOUNT_MEDICARE` | ~3,500 | Normalized. Plan names cleaned (Phase 7). |
| `_ACCOUNT_LIFE` | ~800 | Normalized. Product names cleaned (Phase 7). |
| `_ACCOUNT_ANNUITY` | ~600 | Normalized. Product names cleaned (Phase 7). |
| `_ACCOUNT_BDRIA` | ~200 | Normalized. Product names cleaned (Phase 7). |

### Normalization Status

| Normalizer | Wired Since | Covers |
|------------|-------------|--------|
| carrier_name | v1.0 | All account tabs |
| product_type | v1.0 | All account tabs |
| product_name | v1.12.0 | All account tabs (new — Feb 2026) |
| plan_name | v1.12.0 | _ACCOUNT_MEDICARE (new — Feb 2026) |
| imo_name | v1.12.0 | All account tabs (field wired, normalizer existed) |
| status | v1.0 | All tabs |
| name/phone/email/date/state/zip | v1.0 | _CLIENT_MASTER, _AGENT_MASTER |
| amount (with epoch guard) | v1.12.0 | All amount fields |
| bob | v1.5 | book_of_business field |
| address/city | v1.8 | Primary + mailing addresses |

### Known Issues

| Issue | Status | Blocker |
|-------|--------|---------|
| CoF policy import (Phase 6) | BLOCKED | Waiting on Catholic Order of Foresters data response |
| Orphan accounts | PENDING | ~100 accounts not linked to clients. DEBUG_OrphanDiagnostic ready. |
| GHL opportunities import | PENDING | FIX_ImportGHLOpportunities built, not yet executed |
| Contact validation | PENDING | APIs built + keyed, batch function not yet created |

## SENTINEL_MATRIX Health Summary

| Tab | Est. Records | Status |
|-----|-------------|--------|
| `_AGENT_MASTER` | ~50 | Normalized via Phase 3 reconciliation |
| `_REVENUE_MASTER` | ~2,000 | Revenue records from CAM commission imports |

## RAPID_MATRIX Health Summary

| Tab | Est. Records | Status |
|-----|-------------|--------|
| `_CARRIER_MASTER` | ~80 | Reference data — canonical carrier list |
| `_PRODUCT_MASTER` | ~30 | Reference data — product taxonomy |
| `_IMO_MASTER` | ~10 | Reference data — IMO list |

## Dedup Status

| Capability | Status |
|------------|--------|
| Phase 2: Pre-write dedup (insertRow) | ACTIVE — auto-fires on every insert |
| Phase 3: Batch reconciliation | AVAILABLE — run on demand |
| Client dedup | 270 merged (Feb 2026) |
| Annuity dedup | 39 resolved via FK updates (Feb 2026) |
| Agent dedup | Clean (no dupes found) |

## M&A Data Import Log

| Source | Date | Records | Quality | Issues | Status |
|--------|------|---------|---------|--------|--------|
| GHL (full export) | 2025-12 | ~5,000 | C | Missing DOBs, snake_case values, status garbage | Cleaned via Phases 1-7 |
| CoF (Janet Woods) | 2026-01 | ~200 | B | Missing client_ids, policy format differences | Phase 5 complete, Phase 6 blocked |
| *(template for future imports)* | | | | | |

## Contact Quality Distribution

*(Pending — will be populated after first FIX_ValidateContacts_ run)*

| Grade | Count | % | Description |
|-------|-------|---|-------------|
| A | - | - | All channels valid (phone + email + address) |
| B | - | - | 2 of 3 valid |
| C | - | - | 1 of 3 valid |
| D | - | - | Channels present but degraded |
| F | - | - | No valid contact channels |
| Never validated | ~4,650 | 100% | No validation run yet |

---

*Part of the Data Operating System. See also: DATA_STANDARDS.md, DATA_MONITORING.md, DATA_OPERATIONS.md*
