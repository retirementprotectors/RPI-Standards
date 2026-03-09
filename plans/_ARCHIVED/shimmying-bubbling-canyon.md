# Sprint: PRODASHX v3.12 — MyRPI Polish + Medicare Rec UI + Quick Intake UX

## Context

v3.11.x stabilized the platform (dead screen fix, search, button unification). This sprint finishes Phase 1 (MyRPI layout, Quick Intake UX) and starts Phase 2 (Medicare Rec UI wiring). All three items are frontend-focused with existing backends — high ROI, no new GAS files needed.

---

## Item 1: MyRPI Layout Alignment (P3 from v3.11.1)

**Problem:** PRODASHX MyRPI renders cards in a flat 2-column grid with no intentional layout hierarchy. RIIMO has a structured left/right column layout (profile + job desc left, modules + docs right). JDM said it's "kinda whack."

**Backend:** `PRODASH_Profile.gs:uiGetMyProfile()` already returns all data (user, division, unit, reportsTo, jobTemplate, entitlements, team, folderFiles, workspacePhotoUrl). No backend changes.

**What changes (CSS + JS only):**

### CSS (Styles.html ~3736)
- Change `.myrpi-layout` from flat `1fr 1fr` grid to explicit left/right column layout
- Profile card: full width (already spans with `grid-column: 1 / -1`)
- Left column: Job Description card (if exists), Communication Preferences, Quick Links
- Right column: Module Access, Documents, My Team
- Add `.myrpi-section-title` icon alignment improvements
- Add card hover shadow for polish

### JS (Scripts.html ~13465)
- Restructure `renderMyProfile()` to wrap cards in `<div class="myrpi-col-left">` and `<div class="myrpi-col-right">` containers
- Add Job Description section (data already comes from backend as `data.jobTemplate`)
  - Title, unit, description
  - Only renders if `data.jobTemplate` exists
- Current section order: Profile → Job Desc + Comm Prefs + Quick Links (left) → Modules + Docs + Team (right)

### Files Modified
| File | Change |
|------|--------|
| `Styles.html:3736-3810` | Restructure grid to explicit 2-column with named areas |
| `Scripts.html:13465-13612` | Reorder sections into left/right containers, add Job Description |

---

## Item 2: Medicare Rec UI Wiring (3.5 + 3.6)

**Problem:** The Recommendation tab HTML already exists in Index.html (lines 2849-2946) with preset buttons, client search, plan dropdown, generate button. But the JS wiring is missing — nothing happens when you click anything.

**Backend:** `PRODASH_MEDICARE_REC.gs:uiGenerateMedicareRecForUI(clientId, options)` is complete. Accepts `{ preset, comparisonData, drugData, providerData, recommendedPlan }`.

**What changes (JS only):**

### Scripts.html — Wire the Recommendation tab
1. **`setupRecClientSearch()`** — Initialize typeahead on `#mcRecClient` input, reuse enrollment pattern (`uiSearchClientsForEnrollment`)
2. **`updateRecPlanOptions()`** — Populate plan dropdown from `medicareState.searchResults`
3. **`updateRecDataSummary()`** — Update chip counts: `medicareState.comparisonPlans.length` plans compared, formulary results count, provider results count
4. **`buildRecOptions()`** — Assemble cached data into the format `uiGenerateMedicareRecForUI` expects
5. **`generateMedicareRec()`** — Validate inputs, call server, show loading, display Doc + PDF links on success
6. **Hook into `switchMedicareTab('recommendation')`** — Init client search + update plan options on first visit

### Scripts.html — Wire the Comparison tab (3.6)
1. **`runComparison()`** — When Comparison tab activates with 2+ plans queued, call `uiComparePlans(medicareState.comparisonPlans)` and cache result in `medicareState.comparisonResults`
2. **`renderComparisonResults(data)`** — Build comparison table in the comparison tab content area
3. Hook `runComparison()` into `switchMedicareTab('comparison')`

### Files Modified
| File | Change |
|------|--------|
| `Scripts.html` (after ~9625) | Add rec functions: setupRecClientSearch, updateRecPlanOptions, updateRecDataSummary, buildRecOptions, generateMedicareRec |
| `Scripts.html` (after ~9031) | Add comparison functions: runComparison, renderComparisonResults |
| `Scripts.html:9683-9714` | Hook new functions into switchMedicareTab() |

---

## Item 3: Quick Intake Custom Field UX (P4 from v3.11.1)

**Problem:** "Add Field" currently renders a dropdown + text value input in one step. JDM wants:
1. Step 1: Select field name from dropdown
2. Step 2: Render the appropriate input widget for that field type (text, dropdown with options, date picker, etc.)
3. Beneficiary fields should have structured sub-fields (Name, Relationship, Percentage, DOB, SSN)

**What changes (JS only):**

### Scripts.html (~13166-13261)
1. **Refactor `addCustomIntakeField()`** to be two-step:
   - Step 1: Show field name dropdown only. On selection → detect field type → render appropriate input
   - Field type mapping: dates → date picker, percentages → number input, beneficiary → structured sub-form, carrier → existing carriers dropdown, status → status dropdown, everything else → text
2. **Add `renderBeneficiarySubFields()`** — When user selects `primary_beneficiary` or `contingent_beneficiary`:
   - Name (text)
   - Relationship (dropdown: Spouse, Child, Trust, Estate, Other)
   - Percentage (number, 0-100)
   - DOB (date picker, masked display)
   - SSN (text, masked — last 4 only)
   - Combine into single value string for storage: `"Name | Relationship | Pct% | DOB | ***-**-XXXX"`
3. **Field type detection:** Map schema keys to input types based on key name patterns (contains `date` → date, contains `pct`/`percent` → number, contains `beneficiary` → structured, etc.)

### Files Modified
| File | Change |
|------|--------|
| `Scripts.html:13166-13261` | Refactor addCustomIntakeField to two-step flow |
| `Scripts.html` (new ~13262) | Add renderBeneficiarySubFields() + field type detection |

---

## Build Order

1. **MyRPI Layout** — CSS restructure + JS reorder (~30 min)
2. **Medicare Rec UI Wiring** — JS functions + tab hooks (~45 min)
3. **Quick Intake Custom Fields** — JS refactor + beneficiary sub-form (~30 min)
4. **Deploy as v3.12** — Single deploy covering all 3 items

---

## Verification

1. **MyRPI:** Navigate to My RPI → verify 2-column layout (profile full width, left/right columns below)
2. **MyRPI Job Desc:** If user has a job template → verify it renders in left column
3. **Medicare Rec:** QUE-Medicare → search plans → add to comparison → switch to Comparison tab → verify table renders
4. **Medicare Rec:** Switch to Recommendation tab → select client → select plan → choose preset → Generate → verify Doc + PDF links appear
5. **Quick Intake:** Quick Intake → extract account → click Add Field → verify dropdown appears FIRST → select field → verify appropriate input renders
6. **Quick Intake Beneficiary:** Select "primary_beneficiary" → verify structured sub-fields (Name, Relationship, %, DOB, SSN) appear
7. **Deploy:** 6-step deploy + VERIFY @version
