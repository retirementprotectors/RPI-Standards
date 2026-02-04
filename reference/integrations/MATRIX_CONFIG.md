# MATRIX Configuration Standards

> **Last Updated**: February 2026  
> **Owner**: RIIMO (B2E Operations Platform)  
> **Source of Truth**: `RAPID_TOOLS/RAPID_CORE/CORE_Database.gs`

---

## Overview

The RPI platform uses three Google Sheets spreadsheets as databases (MATRIXes) following the Three-Platform Architecture. This document defines the standards for configuring and accessing these MATRIXes across all projects.

---

## The Three MATRIXes

| MATRIX | ID | Platform | Purpose |
|--------|----|---------|---------| 
| **RAPID_MATRIX** | `1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU` | B2E (RIIMO) | Shared reference data: carriers, comp grids, CMS plans, import mappings |
| **SENTINEL_MATRIX** | `1K_DLb-txoI4F1dLrUyoFOuFc0xwsH1iW5eff3pQ_o6E` | B2B (DAVID) | Producer/deal data: `_PRODUCER_MASTER`, `Opportunities`, revenue, commissions |
| **PRODASH_MATRIX** | `1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w` | B2C (ProDash) | Client/account data: `_CLIENT_MASTER`, `_ACCOUNT_MASTER`, RMD tracking |

---

## Standard Configuration Approach

### 1. Single Source of Truth: RAPID_CORE

All MATRIX IDs are centralized in `RAPID_TOOLS/RAPID_CORE/CORE_Database.gs`. This file exports:

```javascript
// Get a MATRIX ID by platform name
RAPID_CORE.getMATRIX_ID('RAPID')     // Returns RAPID_MATRIX ID
RAPID_CORE.getMATRIX_ID('SENTINEL')  // Returns SENTINEL_MATRIX ID
RAPID_CORE.getMATRIX_ID('PRODASH')   // Returns PRODASH_MATRIX ID

// Get a MATRIX spreadsheet object
RAPID_CORE.getMATRIX_SS('PRODASH')   // Returns Spreadsheet object

// Get all MATRIX IDs
RAPID_CORE.getMATRIX_IDS()           // Returns { RAPID: '...', SENTINEL: '...', PRODASH: '...' }
```

### 2. Project Configuration Pattern

Every project should follow this pattern for MATRIX access:

```javascript
/**
 * Get MATRIX_ID from RAPID_CORE (preferred)
 * Falls back to Script Properties, then hardcoded
 */
function _getMATRIX_ID(platform) {
  // Try RAPID_CORE first (preferred method)
  if (typeof RAPID_CORE !== 'undefined' && RAPID_CORE.getMATRIX_ID) {
    return RAPID_CORE.getMATRIX_ID(platform);
  }
  
  // Fallback to Script Properties
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty(`${platform}_MATRIX_ID`);
  if (id) return id;
  
  // Final fallback to hardcoded (for testing/emergency only)
  Logger.log(`Warning: RAPID_CORE unavailable, using hardcoded ${platform}_MATRIX_ID`);
  const FALLBACK_IDS = {
    RAPID: '1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU',
    SENTINEL: '1K_DLb-txoI4F1dLrUyoFOuFc0xwsH1iW5eff3pQ_o6E',
    PRODASH: '1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w'
  };
  return FALLBACK_IDS[platform];
}
```

### 3. Script Properties as Fallback

Script Properties should store MATRIX IDs as a fallback for:
- Testing with alternate spreadsheets
- Emergency override scenarios
- Projects that can't import RAPID_CORE

Property names:
- `RAPID_MATRIX_ID`
- `SENTINEL_MATRIX_ID`  
- `PRODASH_MATRIX_ID`

---

## Which MATRIX to Use

| Data Type | MATRIX | Tab Examples |
|-----------|--------|--------------|
| Carriers, Products, IMOs | RAPID_MATRIX | `_CARRIER_MASTER`, `_PRODUCT_MASTER`, `_IMO_MASTER` |
| Comp Grids | RAPID_MATRIX | `_MAPD_COMP_GRID`, `_LIFE_COMP_GRID`, `_ANNUITY_COMP_GRID` |
| CMS Plan Data | RAPID_MATRIX | `_CMS_PLANS`, `_CMS_FMV_RATES` |
| Producers/Agents | SENTINEL_MATRIX | `_PRODUCER_MASTER` |
| B2B Opportunities | SENTINEL_MATRIX | `Opportunities` |
| Revenue/Commissions | SENTINEL_MATRIX | `_REVENUE_MASTER`, `_COMMISSION_CYCLES` |
| Clients | PRODASH_MATRIX | `_CLIENT_MASTER` |
| Accounts/Policies | PRODASH_MATRIX | `_ACCOUNT_MASTER` |
| RMD Tracking | PRODASH_MATRIX | `_RMD_TRACKING` |

---

## MATRIX Setup & Maintenance

### Ownership: RIIMO

Per the Three-Platform Architecture, **RIIMO** (B2E Operations) owns MATRIX setup and maintenance:

- **Setup File**: `RAPID_TOOLS/RIIMO/RIIMO_MATRIX_Setup.gs`
- **Responsibilities**:
  - Creating/modifying MATRIX tab schemas
  - Running data migrations between MATRIXes
  - Managing MATRIX backup and validation
  - Maintaining the `MATRIX_IDS` constant in RAPID_CORE

### Setup Functions

```javascript
// Run once to create all tabs in all three MATRIXes
RIIMO.SETUP_ALL_MATRICES()

// Run to migrate data from legacy spreadsheets
RIIMO.MIGRATE_ALL_DATA()

// Audit existing data
RIIMO.AUDIT_ALL_OLD_SOURCES()
```

---

## Do NOT

1. **Do NOT hardcode MATRIX IDs directly in project files** - Always use RAPID_CORE
2. **Do NOT create new tabs without updating schemas** - Coordinate with RIIMO
3. **Do NOT access MATRIX via different patterns in different files** - Use consistent helper functions
4. **Do NOT store MATRIX IDs in multiple places** - RAPID_CORE is the single source

---

## Migration Notes

### Tab Name Changes

| Old Name | New Name | MATRIX |
|----------|----------|--------|
| `_AGENT_MASTER` | `_PRODUCER_MASTER` | SENTINEL_MATRIX |

### File Location Changes

| File | Old Location | New Location |
|------|--------------|--------------|
| `MATRIX_Setup.gs` | `SENTINEL_TOOLS/sentinel/` | `RAPID_TOOLS/RIIMO/RIIMO_MATRIX_Setup.gs` |

---

## Related Documents

- [THREE_PLATFORM_ARCHITECTURE.md](THREE_PLATFORM_ARCHITECTURE.md) - Full architecture overview
- [RPI_PLATFORM_BLUEPRINT.md](RPI_PLATFORM_BLUEPRINT.md) - Five-layer system architecture
