> ARCHIVED: Consolidated into prodashx-platform-roadmap.md (Stream 4: Client Output Engine) on 2026-03-08

# Plan: Case Central Package Module (PRODASHX)

## Context

JDM asked for a "Gradient handoff document format" for the Sprenger household. The Gradient transition is actively in progress (4-6 week timeline). Every client going through the pipeline will need a Case Central package for KonnexME submission. PRODASHX already has the full architecture waiting for this piece — Report #15 (`case_central_package`) is defined in the inventory with status "ready," the Yellow Stage dashboard has a Case Central tab with routing sheet UI, and the Medicare Rec module establishes the exact generation pattern to follow.

**Recommendation: Build the reusable module (not a one-off).** The architecture is literally waiting for this piece. One-off = throwaway work. Module = every client, one button, done.

---

## What Gets Built

A new `PRODASH_CASE_CENTRAL.gs` file (~500 lines) that generates a professional Case Central Package PDF from a Google Doc template. Follows the identical pattern as `PRODASH_MEDICARE_REC.gs`: copy template → populate merge fields → insert tables → clean sections → export PDF → save to ACF.

---

## Implementation

### 1. Create `PRODASH_CASE_CENTRAL.gs` (new file, ~500 lines)

**Constants:**
- `CASE_CENTRAL_SECTIONS_` — 11 sections: cover, demographics, account_summary, holdings, risk_profile, medicare, life_insurance, strategy_notes, discovery_status, report_manifest, disclosure
- `CASE_CENTRAL_PRESETS_` — 3 presets:
  - `full` (all 11 sections)
  - `gradient_handoff` (cover + demographics + accounts + holdings + risk + medicare + life + strategy + disclosure — 9 sections, skips discovery_status and report_manifest)
  - `quick_summary` (cover + demographics + accounts + risk + strategy + disclosure — 6 sections)

**Main function: `generateCaseCentralPackage_(clientId, options)`**
- Mirrors `uiGenerateMedicareRecForUI()` pattern (PRODASH_MEDICARE_REC.gs:53-153)
- Reads client from `_CLIENT_MASTER`
- Reads ALL account types via `scanSalesCenterData_()` + `getClientAccountsFromScan_()`
- Reads opportunity `type_fields` for discovery kit data, COMRA score, report order
- Copies template → populates → exports PDF → saves to ACF "B4 Cases" folder
- Updates `type_fields.report_order.reports.case_central_package.status = 'complete'`

**Section populators (one function per section):**
- `populateCoverPage_()` — Client/household name, date, agent name, RPI branding
- `populateDemographics_()` — Client + spouse: name, DOB, age, address, phone, email, Medicare #
- `populateAccountSummary_()` — Table: Carrier | Product | Account # | Type | Value | Status (all account types merged)
- `populateHoldings_()` — Table: Owner | Account | Ticker | Description | Shares | Value (from BD/RIA data)
- `populateRiskProfile_()` — COMRA score, color, allocation %. Falls back to "Not assessed"
- `populateMedicare_()` — Current Medicare plans table
- `populateLifeInsurance_()` — Life policies table: Carrier | Product | Face | Premium | Beneficiary
- `populateStrategyNotes_()` — Free-text case notes from casework
- `populateDiscoveryStatus_()` — 8-row table showing Discovery Kit form completion
- `populateReportManifest_()` — Ordered reports table with status
- Standard disclosure (static text)

**Household support:** Accepts optional `householdClientIds` array. When provided:
- Cover says "Sprenger Household" not individual name
- Demographics shows both clients
- Account summary merges all household accounts
- Holdings includes Owner column

**ACF folder resolution:** `resolveCasesFolder_()` — mirrors `resolveRecFolder_()` from PRODASH_MEDICARE_REC.gs:469-502, targets "B4 Cases" subfolder

**UI wrappers:**
- `uiGenerateCaseCentralPackageForUI(clientId, options)` — JSON.parse(JSON.stringify()) wrapped
- `uiGenerateHouseholdCaseCentralForUI(clientIds, options)` — Household variant

**SETUP + DEBUG:**
- `SETUP_CreateCaseCentralTemplate()` — Creates Google Doc template with section markers + merge fields
- `DEBUG_GenerateCaseCentralPackage()` — Smoke test with Sprenger client_id

### 2. Modify `Scripts.html` (~40 lines)

Add to the Case Central tab loader (`loadCaseCentralRouting()`, ~line 12397):
- "Generate Case Package" button (full preset)
- "Gradient Handoff" button (gradient_handoff preset)
- `generateCaseCentralPackage()` async JS function — calls server, shows loading, opens PDF on success

### 3. Modify `PRODASH_REPORT_ORDER.gs` (1 line)

Change `case_central_package` build_status from `'ready'` to `'shipped'` (line 38)

---

## Google Doc Template Structure

```
RETIREMENT PROTECTORS, INC.
"We're Your People"

CASE CENTRAL PACKAGE
========================
Prepared for: {{household_name}}
Prepared by: {{agent_name}} | {{generated_date}}

<<SEC:demographics>>
CLIENT INFORMATION
{{client_demo_fields}}
<<END:demographics>>

<<SEC:account_summary>>
ACCOUNT INVENTORY ({{account_count}} accounts, {{account_total_value}})
{{account_summary_table}}
<<END:account_summary>>

<<SEC:holdings>>
HOLDINGS DETAIL ({{holdings_count}} positions)
{{holdings_table}}
<<END:holdings>>

<<SEC:risk_profile>>
RISK ASSESSMENT
COMRA Score: {{comra_score}} / 100 ({{risk_label}})
Allocation: Fixed {{alloc_fixed}}% | Indexed {{alloc_index}}% | Variable {{alloc_variable}}%
<<END:risk_profile>>

<<SEC:medicare>>
MEDICARE COVERAGE
{{medicare_table}}
<<END:medicare>>

<<SEC:life_insurance>>
LIFE INSURANCE
{{life_table}}
<<END:life_insurance>>

<<SEC:strategy_notes>>
CASE NOTES & STRATEGY
{{strategy_notes_content}}
<<END:strategy_notes>>

<<SEC:discovery_status>>
DISCOVERY KIT STATUS
{{discovery_status_table}}
<<END:discovery_status>>

<<SEC:report_manifest>>
REPORT ORDER
{{report_manifest_table}}
<<END:report_manifest>>

<<SEC:disclosure>>
IMPORTANT DISCLOSURES
[Standard RPI disclosure]
<<END:disclosure>>
```

---

## Data Flow

```
_CLIENT_MASTER → demographics, address, spouse, agent
_ACCOUNT_* (all 5 types) → account summary + holdings tables
opportunity.type_fields.discovery_kit → COMRA score, form status
opportunity.type_fields.report_order → report manifest
opportunity.type_fields.casework → strategy notes
          ↓
PRODASH_CASE_CENTRAL.gs :: generateCaseCentralPackage_()
          ↓
Google Doc template (copy → merge → clean sections → PDF)
          ↓
ACF "B4 Cases" folder + report_order status updated
```

---

## Critical Files

| File | Action | Purpose |
|------|--------|---------|
| `PRODASH_CASE_CENTRAL.gs` | CREATE | Core module (~500 lines) |
| `PRODASH_MEDICARE_REC.gs` | READ (pattern) | Template copy + merge + section removal + PDF export + ACF resolution |
| `PRODASH_YELLOW_STAGE.gs` | READ (integration) | Case Central routing already wired up |
| `PRODASH_REPORT_ORDER.gs` | MODIFY (1 line) | Mark case_central_package as shipped |
| `PRODASH_SALES_CENTERS.gs` | READ (data) | scanSalesCenterData_() + getClientAccountsFromScan_() |
| `Scripts.html` | MODIFY (~40 lines) | Add generate buttons + async handler |

---

## Testing Plan

1. Run `SETUP_CreateCaseCentralTemplate` via execute_script → verify template created
2. Run `DEBUG_GenerateCaseCentralPackage` with Randy Sprenger (`9bf18dc7-f7a9-4f66-8038-588f5b439938`) → verify PDF generated in ACF
3. Run household variant with both Sprenger IDs → verify merged document
4. Test `gradient_handoff` preset → verify discovery_status and report_manifest sections excluded
5. Deploy → verify UI buttons work in Yellow Stage
6. Missing data test: generate for client with minimal data → verify graceful fallbacks

---

## Verification

- [ ] `clasp push --force` succeeds
- [ ] `SETUP_CreateCaseCentralTemplate` creates template, stores ID in Script Properties
- [ ] Sprenger Case Central PDF generates with all account data populated
- [ ] PDF saves to ACF B4 Cases folder
- [ ] Yellow Stage UI shows Generate buttons
- [ ] Report order status updates to 'complete' after generation
- [ ] Deploy (version + deploy + git commit + push + verify @version)
