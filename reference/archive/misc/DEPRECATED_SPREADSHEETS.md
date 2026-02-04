# Deprecated Spreadsheets - Archive Notice

> **Created**: February 2026  
> **Status**: ARCHIVED - DO NOT USE

---

## Deprecated MATRIXes

The following spreadsheets have been replaced by the Three-Platform MATRIX Architecture and should be moved to a "Legacy/Archived" folder in Google Drive.

### 1. OLD_MASTER_INDEX (SENTINEL_MASTER_INDEX)

| Property | Value |
|----------|-------|
| **Spreadsheet ID** | `1eyuZt-pjfBads0Y5mrXh1OXiNLe9NoTRMqM5nqJUxuo` |
| **URL** | https://docs.google.com/spreadsheets/d/1eyuZt-pjfBads0Y5mrXh1OXiNLe9NoTRMqM5nqJUxuo/edit |
| **Status** | DEPRECATED |
| **Data Migrated To** | RAPID_MATRIX, SENTINEL_MATRIX, PRODASH_MATRIX |

**Original Contents:**
- Reference data → Migrated to RAPID_MATRIX
- Producer/deal data → Migrated to SENTINEL_MATRIX
- Client/policy data → Migrated to PRODASH_MATRIX

---

### 2. OLD_MATRIX (MATRIX)

| Property | Value |
|----------|-------|
| **Spreadsheet ID** | `1XSQOIW6v-ntyGZKeDYOq8rssveViGiIrRiow5g3jSpQ` |
| **URL** | https://docs.google.com/spreadsheets/d/1XSQOIW6v-ntyGZKeDYOq8rssveViGiIrRiow5g3jSpQ/edit |
| **Status** | DEPRECATED |
| **Data Migrated To** | RAPID_MATRIX, SENTINEL_MATRIX, PRODASH_MATRIX |

**Original Contents:**
- Comp grids, carriers, IMOs → Migrated to RAPID_MATRIX
- Opportunities, producers → Migrated to SENTINEL_MATRIX
- Clients, accounts → Migrated to PRODASH_MATRIX

---

## Migration Reference

Data was migrated using `RIIMO_MATRIX_Setup.gs` functions:
- `MIGRATE_TO_RAPID_MATRIX()` - Reference data
- `MIGRATE_TO_SENTINEL_MATRIX()` - B2B data
- `MIGRATE_TO_PRODASH_MATRIX()` - B2C data

---

## Action Required

1. **Verify** the three new MATRIXes contain all required data
2. **Move** the above spreadsheets to a "Legacy/Archived" folder in Google Drive
3. **Do NOT delete** - keep for historical reference

---

## Current Active MATRIXes

| MATRIX | ID | Purpose |
|--------|----|---------| 
| RAPID_MATRIX | `1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU` | Shared reference data |
| SENTINEL_MATRIX | `1K_DLb-txoI4F1dLrUyoFOuFc0xwsH1iW5eff3pQ_o6E` | B2B producer/deal data |
| PRODASH_MATRIX | `1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w` | B2C client/account data |

See [MATRIX_CONFIGURATION_STANDARDS.md](MATRIX_CONFIGURATION_STANDARDS.md) for configuration details.
