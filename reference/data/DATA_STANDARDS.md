# DATA_STANDARDS -- Field Registry, Canonical Values & Correction Log

> Pillar 1 of the Data Operating System. Defines what the rules ARE for data quality across all MATRIX tabs.

---

## Field Registry

Fields are mapped to normalizer types via `FIELD_NORMALIZERS` in `RAPID_CORE/CORE_Database.gs`. When `insertRow()` or `updateRow()` is called, each field is checked against this map and the corresponding normalizer fires automatically. 90+ fields are mapped. Unmapped fields pass through unchanged.

### Normalizer Types

| Type | Function | What It Does |
|------|----------|--------------|
| `name` | `normalizeSingleName()` | Title case, McName/O'Name awareness (McDonald, O'Brien) |
| `phone` | `normalizePhone()` | Format to (XXX) XXX-XXXX |
| `email` | `normalizeEmail()` | Lowercase, trim whitespace |
| `date` | `normalizeDate()` then `toSheetDate_()` | ISO YYYY-MM-DD then Date object for Sheets |
| `state` | `normalizeState()` | 2-letter uppercase code |
| `zip` | `normalizeZip()` | 5-digit with zero-padding (e.g., "7102" becomes "07102") |
| `amount` | `normalizeAmount()` | Numeric, strips `$` and commas, guards epoch dates |
| `carrier` | `normalizeCarrierName()` | Alias map (238+ entries) + CARRIER_MASTER lookup |
| `product` | `normalizeProductType()` | Maps to canonical product types (MAPD, PDP, FIA, etc.) |
| `product_name` | `normalizeProductName()` | Alias map (50+ entries), strips registered trademark symbols |
| `plan_name` | `normalizePlanName()` | Alias map (30+ entries), regex fixes (Heathcare to Healthcare, PLATNIUM to PLATINUM), clears CMS plan IDs |
| `imo` | `normalizeIMOName()` | Alias map + IMO_MASTER lookup |
| `status` | `normalizeStatus()` | Maps typos/shorthand to canonical values |
| `bob` | `normalizeBoB()` | Maps book_of_business variations to canonical names |
| `address` | `normalizeAddress()` | Title case with directional/suffix awareness (NW, Ave, Blvd) |
| `city` | `normalizeCity()` | Title case (only if ALL-CAPS input) |
| `skip` | No normalization | Timestamps, system fields, IDs -- pass through unchanged |

### How Fields Are Mapped

In `FIELD_NORMALIZERS`, each field name points to a normalizer type:

```
first_name        -> name
last_name         -> name
phone             -> phone
email             -> email
date_of_birth     -> date
effective_date    -> date
state             -> state
zip               -> zip
premium           -> amount
carrier_name      -> carrier
product_type      -> product
product_name      -> product_name
plan_name         -> plan_name
imo_name          -> imo
status            -> status
book_of_business  -> bob
address_line_1    -> address
city              -> city
created_at        -> skip
updated_at        -> skip
...and 70+ more
```

---

## Canonical Value Lists

### Carrier Names (Top 50)

These are the canonical forms. All aliases, typos, and abbreviations map to these exact strings.

| # | Canonical Name | Common Aliases |
|---|---------------|----------------|
| 1 | Aetna | aetna, AETNA, Aetna CVS Health |
| 2 | UnitedHealthcare | United Healthcare, UHC, United Health Care, AARP/UHC |
| 3 | Humana | humana, HUMANA |
| 4 | Cigna | CIGNA, Cigna Healthcare |
| 5 | WellCare | Wellcare, Well Care, WELLCARE |
| 6 | BCBS | Blue Cross Blue Shield, Blue Cross, BlueCross BlueShield |
| 7 | Anthem | Anthem BCBS, Anthem Blue Cross |
| 8 | Centene | centene |
| 9 | Molina Healthcare | Molina, MOLINA |
| 10 | Mutual of Omaha | MoO, Mutual, mutual of omaha |
| 11 | Catholic Order of Foresters | CoF, COF, Catholic Order, Cath Order of Foresters |
| 12 | Kansas City Life | KCL, KC Life, Kansas City Life Insurance |
| 13 | North American Company | NAC, North American, NA Company |
| 14 | National Western Life | NWL, Nat Western, National Western |
| 15 | American Equity | AEL, American Equity Investment, Amer Equity |
| 16 | Athene | athene, ATHENE, Athene Annuity |
| 17 | Global Atlantic | GA, Global Atlantic Financial |
| 18 | F&G Life | FGL, Fidelity & Guaranty, F and G |
| 19 | Prudential | Pru, PRUDENTIAL, Prudential Financial |
| 20 | Transamerica | transamerica, TRANSAMERICA, TA |
| 21 | Allianz | allianz, ALLIANZ, Allianz Life |
| 22 | Nationwide | nationwide, NATIONWIDE, Nationwide Life |
| 23 | Lincoln Financial | Lincoln, LFG, Lincoln National |
| 24 | Pacific Life | PacLife, Pacific, PACIFIC LIFE |
| 25 | Sammons Financial | Sammons, North American (Sammons) |
| 26 | Midland National | Midland, MNL, Midland Natl |
| 27 | Protective Life | Protective, PROTECTIVE |
| 28 | Security Benefit | SBL, Security Benefit Life |
| 29 | Great American | GAIG, Great American Insurance |
| 30 | Corebridge Financial | Corebridge, COREBRIDGE, AIG (legacy) |
| 31 | MassMutual | Mass Mutual, MASSMUTUAL |
| 32 | New York Life | NYL, NY Life, NEW YORK LIFE |
| 33 | Brighthouse Financial | Brighthouse, BRIGHTHOUSE |
| 34 | Jackson National | Jackson, JNL, JACKSON |
| 35 | Ameritas | ameritas, AMERITAS |
| 36 | Bankers Life | Bankers, BANKERS LIFE |
| 37 | Foresters Financial | Foresters, FORESTERS |
| 38 | Gerber Life | Gerber, GERBER LIFE |
| 39 | Guarantee Trust Life | GTL, Guarantee Trust |
| 40 | Liberty Bankers | Liberty Bankers Life, LBL |
| 41 | Manhattan Life | MANHATTAN LIFE |
| 42 | Medico | MEDICO, Medico Corp |
| 43 | Physicians Mutual | Physicians, PHYSICIANS MUTUAL |
| 44 | Royal Neighbors | RNA, Royal Neighbors of America |
| 45 | SILAC | silac, SILAC Insurance |
| 46 | State Farm | STATE FARM |
| 47 | Devoted Health | Devoted, DEVOTED |
| 48 | Zing Health | Zing, ZING |
| 49 | Wellpoint | WELLPOINT |
| 50 | CVS Aetna | CVS/Aetna |

### Product Types

Canonical product types, grouped by line of business:

**Medicare:**
| Product Type | Description |
|-------------|-------------|
| MAPD | Medicare Advantage Prescription Drug |
| PDP | Prescription Drug Plan (standalone) |
| DSNP | Dual Special Needs Plan |
| CSNP | Chronic Special Needs Plan |
| SNP | Special Needs Plan (generic) |
| MedSupp | Medicare Supplement (Medigap) |

**Life Insurance:**
| Product Type | Description |
|-------------|-------------|
| Term Life | Term life insurance |
| Whole Life | Whole life insurance |
| Final Expense | Final expense / burial insurance |
| IUL | Indexed Universal Life |

**Annuities:**
| Product Type | Description |
|-------------|-------------|
| FIA | Fixed Index Annuity |
| MYGA | Multi-Year Guaranteed Annuity |
| SPIA | Single Premium Immediate Annuity |
| Variable Annuity | Variable annuity |

**Advisory / Brokerage:**
| Product Type | Description |
|-------------|-------------|
| Advisory (Fee-Based) | RIA fee-based advisory |
| Brokerage (Commission-Based) | BD commission-based brokerage |

**Ancillary:**
| Product Type | Description |
|-------------|-------------|
| Dental | Dental plan |
| Vision | Vision plan |
| DVH | Dental/Vision/Hearing combo |
| Hospital Indemnity | Hospital indemnity plan |
| Cancer | Cancer insurance |
| Critical Illness | Critical illness insurance |

### Status Values

| Status | Used For | Notes |
|--------|----------|-------|
| Active | All tabs | Currently in force |
| Inactive | All tabs | No longer in force (lapsed, cancelled, disenrolled) |
| Active - Internal | Agents | Internal RPI team member |
| Active - External | Agents | External agent/producer |
| Pending | All tabs | In process, not yet finalized |
| Complete | Workflows | Task/process completed |
| Cancelled | Policies | Cancelled by client or carrier |
| Terminated | Agents, Policies | Terminated relationship or policy |
| Lapsed | Policies | Premium not paid, coverage lapsed |
| Deceased | Clients | Client is deceased |
| Deleted | All tabs | Soft delete (row retained for audit) |
| Surrendered | Annuities | Annuity surrendered by owner |
| Claim | Life | Life claim filed |
| Matured | Annuities | Annuity reached maturity |
| Annuity (reclassified) | Life tab | Was in life tab, reclassified as annuity product |

### Book of Business Names

| Canonical Name | Common Aliases |
|---------------|----------------|
| Millang Financial Group | MFG, Millang, millang financial |
| Retirement Protectors | RPI, retirement protectors, Retire Protectors |
| Senior Products Insurance | SPI, Senior Products, senior products insurance |
| RetireWise | Retirewise, RETIREWISE, Retire Wise |
| Dexter | dexter, DEXTER |
| Archer | archer, ARCHER |
| Greene Point Partners | Greene Point, GPP, Greene Pt |
| Janet Woods - CoF | Janet Woods, Woods CoF, Janet Woods CoF |

---

## Garbage Patterns

Known garbage patterns that normalizers catch and correct automatically:

### 1. Epoch Dates in Amount Fields

Date objects with year <=1901 or strings containing "1899 GMT" appear when Sheets auto-converts a date-formatted cell that was intended to hold a dollar amount.

- **Detection**: `value instanceof Date && value.getFullYear() <= 1901` OR `String(value).includes('1899 GMT')`
- **Correction**: Cleared to `0`
- **Normalizer**: `normalizeAmount()`

### 2. CMS Plan IDs as Plan Names

CMS contract IDs like H1234-567, S5921-363 sometimes populate the plan_name field instead of the actual plan name.

- **Detection**: Regex pattern `/^[HSR]\d{4}-\d{3}/`
- **Correction**: Cleared to empty string
- **Normalizer**: `normalizePlanName()`

### 3. Trademark Symbols

Registered trademark symbols appear in product and plan names from carrier data feeds.

- **Detection**: Contains `\u00AE` character
- **Correction**: Stripped (replaced with empty string)
- **Normalizer**: `normalizeProductName()`, `normalizePlanName()`

### 4. Double Spaces

Multiple consecutive spaces from copy-paste or bad data sources.

- **Detection**: `/\s{2,}/`
- **Correction**: Collapsed to single space
- **Normalizer**: All name-based normalizers

### 5. Trailing Underscores (GHL Snake Case)

GoHighLevel exports use snake_case field values that sometimes leak through as underscored display values.

- **Detection**: Contains underscores in display fields
- **Correction**: Underscores converted to spaces, then title-cased
- **Normalizer**: `normalizeSingleName()`, `normalizeAddress()`

### 6. Systematic Typos

Known misspellings that recur in carrier data feeds and manual entry.

| Garbage | Canonical |
|---------|-----------|
| Heathcare | Healthcare |
| PLATNIUM | PLATINUM |
| Perscription | Prescription |
| Advatange | Advantage |
| Prefered | Preferred |

- **Normalizer**: `normalizePlanName()` (regex-based corrections)

### 7. Truncated Names

Product/plan names cut off at character limits from source systems.

| Garbage | Canonical |
|---------|-----------|
| Personal Income Annuit | Personal Income Annuity |
| Aetna Medicare Advantag | Aetna Medicare Advantage |

- **Normalizer**: `normalizeProductName()`, `normalizePlanName()` (alias map)

### 8. Missing Parentheses

Plan type suffixes that should be parenthesized arrive without parens from some carrier feeds.

| Garbage | Canonical |
|---------|-----------|
| Aetna Signature HMO-POS | Aetna Signature (HMO-POS) |
| Humana Gold Plus H5619-086 HMO | Humana Gold Plus (HMO) |

- **Normalizer**: `normalizePlanName()` (regex + alias map)

---

## Correction Log

### 2026-02-20: Normalizer Promotion (Data OS Phase A)

All 73 product/plan corrections promoted from one-time FIX_ functions into permanent RAPID_CORE normalizers.

| Change | Detail |
|--------|--------|
| `normalizeProductName()` | 50+ alias entries added |
| `normalizePlanName()` | 30+ alias entries + 2 regex patterns |
| `FIELD_NORMALIZERS` | product_name, plan_name, imo_name wired in |
| `normalizeAmount()` | Epoch date guard added |
| RAPID_CORE version | v1.12.0 |
| Impact | All future `insertRow()`/`updateRow()` calls auto-normalize these fields |

### 2026-02-19: Product Name Cleanup (Phase 7)

Executed via `FIX_FixProductNames_` in `IMPORT_BoBEnrich.gs` with DryRun preview pattern.

| Category | Corrections | Examples |
|----------|-------------|---------|
| Annuity products | 23 | VersaChoice casing, Synergy typos, ApexAdvantage, Income Pay Pro |
| Life products | 19 | SuperNOVA casing, EquiFlex, Compass Elite, V4L expansion |
| Medicare plans | 31 exact + 2 regex | Aetna/Wellcare paren fixes, Humana standardization, CMS ID clearing |
| **Total records affected** | **~700** | Across 5 PRODASH_MATRIX tabs |

### 2026-02-18: Status + Carrier Cleanup (Phases 1-4)

Executed via multiple FIX_ functions in `IMPORT_BoBEnrich.gs`.

| Phase | Function | Records | Detail |
|-------|----------|---------|--------|
| Phase 1 | `FIX_NormalizeClients` | 4,649 | Names, phones, dates, emails, states, zips |
| Phase 2 | `FIX_CleanStatuses` | 4,617 | Active typos, pipeline stages to Pending, disenrolled to Inactive |
| Phase 3 | `FIX_MergeClientDupes` | 270 | Merged via reconciliation (kept newest, updated FKs) |
| Phase 4 | `FIX_ResolveAnnuityDupes` | 39 | Resolved via FK updates to canonical client records |
| Also | `FIX_NormalizeMedicare`, `FIX_NormalizeLife`, `FIX_NormalizeAnnuity`, `FIX_NormalizeBDRIA` | -- | Product-line-specific normalization |

---

## How Corrections Become Permanent Rules

```
1. Identify garbage pattern via DEBUG_ diagnostic
   - Run DEBUG_ function to scan a MATRIX tab
   - Output: list of non-canonical values + frequency counts

2. Build FIX_ correction with DryRun preview
   - FIX_ function takes a dryRun parameter (default true)
   - DryRun logs what WOULD change without writing
   - Review DryRun output before executing

3. Execute correction on existing data
   - Run FIX_ with dryRun = false
   - Log: records changed, old value -> new value

4. Add alias entry to RAPID_CORE normalizer map
   - PRODUCT_NAME_ALIASES, PLAN_NAME_ALIASES, CARRIER_ALIASES, etc.
   - Key = lowercase garbage value, Value = canonical form

5. Wire field into FIELD_NORMALIZERS if not already mapped
   - In CORE_Database.gs, add field_name: 'normalizer_type'

6. Deploy RAPID_CORE
   - Pattern is now auto-caught on all future imports
   - Every insertRow() and updateRow() runs through FIELD_NORMALIZERS

7. Document in this Correction Log
   - Date, what changed, records affected, method used
```

### Pattern Lifecycle

```
Garbage data discovered
        |
        v
DEBUG_ diagnostic (read-only scan)
        |
        v
FIX_ one-time correction (DryRun first, then execute)
        |
        v
Promote to RAPID_CORE normalizer (alias map or regex)
        |
        v
Wire into FIELD_NORMALIZERS
        |
        v
Deploy RAPID_CORE (permanent, automatic)
        |
        v
Log in DATA_STANDARDS.md Correction Log
```

This ensures:
- **Existing data** is cleaned by the FIX_ function
- **Future data** is auto-cleaned by the normalizer on ingest
- **The pattern never recurs** -- it is caught at the gate permanently

---

*Part of the Data Operating System. See also: DATA_POSTURE.md, DATA_MONITORING.md, DATA_OPERATIONS.md*
