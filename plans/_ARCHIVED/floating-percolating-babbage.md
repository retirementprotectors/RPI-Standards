# PRODASH Session Plan — Feb 15, 2026

## Context

QUE- Medicare rename is staged (68 refs, 13 files). AI3 template is missing the Medicare merge field. Banking product type is 40% wired. Planning docs are stale and overlapping. Tonight's goal: deploy rename, formalize banking, consolidate docs, and design the Medicare Recommendation output — completing Medicare's full A-to-Z output pipeline.

---

## Execution Order

```
STEP 1: Deploy v166 (QUE-Medicare rename)          ~5 min
STEP 2: JDM runs SETUP function (template patch)   ~2 min (JDM)
   >>> JDM starts testing QUE-Medicare in parallel <<<
STEP 3: Banking formalization (2 files)             ~15 min
STEP 4: Deploy v167 (banking)                       ~5 min
STEP 5: Consolidate docs → PRODASH_ROADMAP.md       ~20 min
STEP 6: Medicare Recommendation output design       ~30 min
STEP 7: Deploy v168 (recommendation foundation)     ~5 min
```

---

## Step 1-2: Deploy Rename + SETUP

**Deploy v166** with standard 6-step:
```bash
cd ~/Projects/PRODASH_TOOLS/PRODASH
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "v166 - QUE-Medicare rename + AI3 template SETUP"
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i AKfycbwy2bEebHA2n9gABzZp34VcDq-8dsHaiUF0FGRZGo_lKEpXT55qOYEh0enF3f7F8vUlWA -V [VERSION] -d "v166"
# VERIFY @version matches
git add -A && git commit -m "v166 - QUE-Medicare rename + AI3 template SETUP" && git push
```

**JDM runs SETUP:**
- Project: **PRODASH**
- File: **PRODASH_CLIENT360.gs**
- Function: **SETUP_AddQueMedicareToAi3Template**

Idempotent — safe to run multiple times. Adds "QUE- Medicare" H3 + `{{que_medicare_content}}` to Section 6 of the AI3 template.

---

## Step 3-4: Banking Formalization

**40% already done**: schema, TABLE_ROUTING, AI3 merge fields all exist.

**What needs adding** (mechanical, follows exact pattern of annuity/life/medicare/bdria):

### PRODASH_Accounts.gs (6 edits)
| Location | Change |
|----------|--------|
| `sheetMap` (~line 33) | Add `'banking': '_ACCOUNT_BANKING'` |
| `typeMap` (~line 321) | Add `'Banking': 'banking'` |
| Display mapping (~line 376) | Add `a.accountType === 'banking' ? 'Banking' :` |
| `getProductTypeOptions()` (~line 737) | Add `{ value: 'Banking', label: 'Banking' }` |
| Stats object (~line 773) | Add `banking: { count: 0, active: 0, totalBalance: 0 }` |
| `uiGetAccountForEdit` sheetMap (~line 596) | Add `'banking': '_ACCOUNT_BANKING'` |

Also: add `'banking'` to `types` array (~line 781), banking stats calculation block, banking stats return block.

### PRODASH_SALES_CENTERS.gs (1 edit)
| Location | Change |
|----------|--------|
| `allAccountSheets` (line 47) | Add `banking: '_ACCOUNT_BANKING'` |

**Deploy as v167.**

---

## Step 5: Doc Consolidation → PRODASH_ROADMAP.md

### Problem
Two overlapping docs, both stale:
- `CLIENT_OUTPUT_ENGINE_MASTER_PLAN.md` (Feb 12) — vision + architecture
- `CLIENT_OUTPUT_ENGINE_PHASE_PLANS.md` (Feb 13) — implementation details
- ~60% overlap, both say Phase 1-2 are "planned" when they're COMPLETE

### Solution
Create **one** `Docs/PRODASH_ROADMAP.md` with these sections:

1. **Strategic Position** — condensed Five-Layer Blueprint + "why this matters" (5 lines)
2. **The Full Pipeline** — keep the ASCII pipeline diagram from Master Plan (gold)
3. **Implementation Status** — 3 tables: COMPLETE, IN PROGRESS, NEXT UP (current as of tonight)
4. **The 5 Yellow Stage Deliverables** — updated descriptions with status per deliverable
5. **Output Type Architecture** — the reusable template pattern (NEW — established by Medicare Rec)
6. **The 7 Strategy Output Types** — table + Three-Level Package System
7. **Architecture Reference** — Sales Center 3-layer pattern, output doc pattern
8. **Key Files** — condensed reference (not phase-by-phase lists)

### Disposition of old docs
- Rename to `_ARCHIVE_*` prefix (keep for git history, don't clutter active docs)

---

## Step 6-7: Medicare Recommendation Output

### What It Is
Client-facing **recommendation document** — the "strategy output" for Medicare. Tells the client: "Here's your situation, here's what we compared, here's what we recommend and why."

This is output #3 in the Medicare pipeline:
1. AI3 PDF (inventory) — **DONE**
2. QUE- Medicare (analysis tools) — **DONE**
3. **Medicare Recommendation** (strategy doc) — BUILD THIS
4. Enrollment Package (SPARK + implementation) — partial

### Architecture (same as AI3)
```
CLIENT360 / QUE- Medicare UI
  → uiGenerateMedicareRecForUI(clientId, options)
    → Copy Google Doc template
    → Populate merge fields from MATRIX + cached QUE data
    → Clean disabled sections
    → Export PDF to ACF "Recommendations" folder
    → Return { docUrl, pdfUrl }
```

### New File: `PRODASH_MEDICARE_REC.gs` (~300 lines)
Mirrors `PRODASH_CLIENT360.gs` AI3 generation pattern.

### Template Sections (7, toggleable)

| # | Section | Data Source | Key Merge Fields |
|---|---------|-------------|------------------|
| 1 | **Current Situation** | _CLIENT_MASTER + _ACCOUNT_MEDICARE | `{{client_name}}`, `{{current_plan_*}}` |
| 2 | **Plan Comparison** | QUE plan search results (passed in) | `{{comparison_table}}`, `{{comparison_count}}` |
| 3 | **Drug Coverage** | QUE formulary results (passed in) | `{{drug_coverage_table}}`, `{{drug_cost_savings}}` |
| 4 | **Provider Network** | QUE provider results (passed in) | `{{provider_network_table}}`, `{{provider_summary}}` |
| 5 | **Our Recommendation** | Computed from comparison data | `{{recommended_plan_*}}`, `{{recommendation_reasons}}` |
| 6 | **Next Steps** | _CLIENT_MASTER (SOA, specialist) | `{{soa_status}}`, `{{enrollment_window}}` |
| 7 | **Disclosure** | Static (same CMS disclaimer as AI3) | None (template text) |

### Data Flow — No Re-fetching
The recommendation uses data **already gathered** during QUE- Medicare workflow. User runs plan search, formulary, provider checks in the QUE tabs, then clicks "Generate Recommendation" which passes cached results to the server. No duplicate API calls.

### UI Trigger
Button in QUE- Medicare Enrollment tab OR CLIENT360:
```
[Generate Medicare Recommendation]
```
Opens config modal (same pattern as AI3): section toggles, presets ("Full Recommendation", "Quick Compare", "Drug Focus"), generate button.

### Storage
- Google Doc + PDF in ACF > "Recommendations" subfolder
- Tracked in `_CASE_TASKS`: `medicare_rec_url`, `medicare_rec_date`

### Replication Pattern for Annuity
Every recommendation output follows the same 7-section shell:
1. Current Situation (what you have)
2. Comparison Analysis (what we compared)
3. Domain Detail A (drugs → income projection)
4. Domain Detail B (providers → surrender analysis)
5. Our Recommendation (what we suggest and why)
6. Next Steps (what happens now)
7. Disclosure

Sections 3-4 are domain-specific; 1, 2, 5, 6, 7 are nearly identical across all product lines. `PRODASH_ANNUITY_REC.gs` follows the same pattern with annuity-specific sections.

---

## Verification

| Check | Method |
|-------|--------|
| v166 deploy | `clasp deployments | grep @166` |
| SETUP ran | Open AI3 template → Section 6 has "QUE- Medicare" header |
| Banking in Accounts tab | Load Accounts page → filter by Banking → shows any banking records |
| Banking in stats | Dashboard stats card includes banking total |
| QUE-Medicare nav works | Click "QUE- Medicare" in sidebar → loads 6-tab view |
| Medicare Rec generates | Select client → Generate Medicare Recommendation → PDF in ACF |
| Roadmap doc is current | `Docs/PRODASH_ROADMAP.md` exists, old docs archived |

---

## Files Modified/Created

| File | Action |
|------|--------|
| `PRODASH_Accounts.gs` | Edit (6 banking additions) |
| `PRODASH_SALES_CENTERS.gs` | Edit (1 banking addition) |
| `PRODASH_MEDICARE_REC.gs` | **CREATE** (~300 lines) |
| `Docs/PRODASH_ROADMAP.md` | **CREATE** (consolidated roadmap) |
| `Docs/CLIENT_OUTPUT_ENGINE_MASTER_PLAN.md` | Rename → `_ARCHIVE_*` |
| `Docs/CLIENT_OUTPUT_ENGINE_PHASE_PLANS.md` | Rename → `_ARCHIVE_*` |
| AI3 Google Doc Template | Updated via SETUP function (QUE-Medicare merge field) |
| Medicare Rec Google Doc Template | **CREATE** (via DocumentApp in SETUP) |
