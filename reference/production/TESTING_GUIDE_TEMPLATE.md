# [PROJECT] Testing Guide — [MODULE NAME] (v[VERSION])

**Print this and check off each item as you test.**
**Date:** _______________
**Tester:** _______________
**Version:** v[VERSION] ([brief description])

---

## PREREQUISITES

Before testing, confirm:

- [ ] [PROJECT] deployed at v[VERSION] or later
- [ ] [Required service 1 running / configured — e.g., "Healthcare MCPs running"]
- [ ] [Required service 2 — e.g., "Webhook proxy live at [URL]"]
- [ ] [Required data — e.g., "At least one client exists in _CLIENT_MASTER with [relevant data]"]
- [ ] Browser DevTools Console open (for error checking)

---

## OVERVIEW

[MODULE NAME] has [N] tabs/views. Each test below covers one feature area.

| Tab / View | Purpose | Data Source |
|------------|---------|-------------|
| [Tab 1] | [What it does] | [Where data comes from] |
| [Tab 2] | [What it does] | [Where data comes from] |
| [Tab 3] | [What it does] | [Where data comes from] |
| ... | ... | ... |

---

## TEST 1: [Feature/Tab Name]

**Where:** [Navigation path — e.g., "Module > Tab Name (default tab)"]

- [ ] [First thing to verify — e.g., "Open [module] from the sidebar"]
- [ ] [UI element renders correctly]
- [ ] [Data displays — or empty state if no data]
- [ ] [Key data points are accurate]:

| Field / Element | Expected |
|-----------------|----------|
| [Field 1] | [What it should show] |
| [Field 2] | [What it should show] |

- [ ] [Interactive element works — e.g., "Clicking a card opens detail"]
- [ ] No console errors

---

## TEST 2: [Feature/Tab Name]

**Where:** [Navigation path]

- [ ] [Navigate to this feature — tab switches correctly]
- [ ] [Input fields / controls are visible and functional]
- [ ] [Perform the primary action — e.g., "Select filters, click Search"]
- [ ] [Loading indicator appears during async operation]
- [ ] [Results display with correct columns/fields]:

| Column / Field | Expected |
|----------------|----------|
| [Column 1] | [Expected content] |
| [Column 2] | [Expected content] |

- [ ] [Results are scrollable / paginated if large dataset]
- [ ] [Selection / interaction works — e.g., "Clicking a row selects it"]
- [ ] [Offline / error state — e.g., "If API offline: graceful error message, NOT a crash"]
- [ ] No console errors

---

## TEST 3: [Feature/Tab Name]

**Where:** [Navigation path]

- [ ] [Navigate to feature]
- [ ] [Empty state shown when no prior selections]
- [ ] [Go perform prerequisite action in another tab, then return]
- [ ] [Feature now populated with data from prior action]
- [ ] [Key comparisons / calculations are correct]:

| Row / Metric | What to Verify |
|--------------|----------------|
| [Metric 1] | [Expected behavior] |
| [Metric 2] | [Expected behavior] |

- [ ] [Removal / modification works]
- [ ] No console errors

---

<!-- ═══ COPY/PASTE THIS BLOCK FOR ADDITIONAL FEATURES ═══ -->
<!--
## TEST N: [Feature/Tab Name]

**Where:** [Navigation path]

- [ ] [Test items...]
- [ ] No console errors
-->
<!-- ═══ END COPY BLOCK ═══ -->

---

## TEST [N]: [Complex Feature — Sub-section Pattern]

**Where:** [Navigation path]

> Use sub-sections (A, B, C...) when a single feature has multiple distinct workflows.
> Example: an Enrollment tab with Search, Payload Generation, Validation, and Submission.

### [N]A: [Sub-feature Name]

- [ ] [Test items for this sub-feature]
- [ ] [Test items...]

### [N]B: [Sub-feature Name]

- [ ] [Test items...]
- [ ] [Nested/dependent items]:
  - [ ] [Sub-item that depends on parent]
  - [ ] [Sub-item that depends on parent]

### [N]C: [Sub-feature Name]

- [ ] [Test items...]
- [ ] [Verify against data table]:

| Field | Source | Expected |
|-------|--------|----------|
| [field_name] | [source system] | [expected value] |
| [field_name] | [source system] | [expected value] |

### [N]D: [Validation / Warnings]

- [ ] [Validation scenario 1 — e.g., "Missing required field: warning toast"]
- [ ] [Validation scenario 2]
- [ ] [Multiple validations can fire simultaneously]

### [N]E: [Submission / Write Operation]

> If this feature writes data, call it out explicitly.

- [ ] [Button enabled after prerequisites met]
- [ ] [Click triggers loading state — button disabled]
- [ ] [On success: confirmation UI + toast message]
- [ ] [On failure: button re-enabled + error toast]
- [ ] **Verify in [SHEET/SYSTEM]**:

| Field | Expected Value |
|-------|----------------|
| [field] | [value] |
| [field] | [value] |

- [ ] [Double-submit prevention — button stays disabled after success]
- [ ] No console errors

---

## TEST [N+1]: Cross-Feature Workflow (End-to-End)

**This tests the full workflow across all features/tabs.**

[Describe the test scenario — e.g., "Pick a real client from _CLIENT_MASTER who has [relevant data]."]

- [ ] **Step 1 — [Feature]**: [What to do]
- [ ] **Step 2 — [Feature]**: [What to do]
- [ ] **Step 3 — [Feature]**: [What to do]
- [ ] **Step 4 — [Feature]**: [What to do]
- [ ] **Step 5 — [Feature]**: [What to do — include sub-steps if complex]:
  - [ ] [Sub-step]
  - [ ] [Sub-step]
- [ ] **Step 6 — [Verify]**: [Return to starting point, verify end state]
- [ ] Data persists correctly when switching between tabs/views
- [ ] No console errors throughout the workflow

---

## TEST [N+2]: External Integration

**[Name the integration — e.g., "SPARK Webhook Integration"]**

**Prerequisites:** [Access requirements — e.g., "Access to Spark Back Office"]

- [ ] [Integration endpoint configured — e.g., "Webhook URL set in external system"]
- [ ] [Test the connection — e.g., "External system confirms successful response"]
- [ ] [Trigger inbound event — e.g., "Create record in external system"]:
  - [ ] [Verify data synced to internal system — specific fields]
  - [ ] [Verify tracking fields populated — e.g., "sync ID", "last_sync timestamp"]
- [ ] [Trigger another event type if applicable]

> Delete this section if the module has no external integrations.

---

## TEST [N+3]: Error Handling & Edge Cases

- [ ] **[Primary API/service] offline**: All features show user-friendly offline message
- [ ] **Empty results**: Shows "No [items] found" message (not blank/broken)
- [ ] **Invalid inputs**: Validation errors shown before sending request
- [ ] **Network timeout**: Shows timeout message, not infinite spinner
- [ ] **Tab/view switching during load**: Previous request doesn't break current view
- [ ] **Multiple rapid clicks**: Buttons are debounced (no duplicate requests)
- [ ] **Mobile/responsive**: Layout adapts at narrow screen widths

---

## TEST [N+4]: Data Accuracy Spot-Check

Pick one real record from [SOURCE SYSTEM] and verify data matches across systems.

| Field | [Source System] Value | [Project] Value | Match? |
|-------|----------------------|-----------------|--------|
| [Field 1] | | | [ ] |
| [Field 2] | | | [ ] |
| [Field 3] | | | [ ] |
| [Field 4] | | | [ ] |
| [Field 5] | | | [ ] |
| [Field 6] | | | [ ] |
| [Field 7] | | | [ ] |
| [Field 8] | | | [ ] |
| [Field 9] | | | [ ] |

---

## Post-Test Summary

| Test | Pass | Fail | Notes |
|------|------|------|-------|
| 1. [Feature Name] | | | |
| 2. [Feature Name] | | | |
| 3. [Feature Name] | | | |
| ... | | | |
| [N]. Cross-Feature Workflow | | | |
| [N+1]. External Integration | | | |
| [N+2]. Error Handling | | | |
| [N+3]. Data Accuracy | | | |

**Overall Status:** PASS / FAIL

**Blocking Issues:**
1. ___
2. ___
3. ___

**Tester Signature:** _______________ **Date:** _______________

---

## Generating the HTML Version

After completing this markdown guide, generate an interactive HTML version for `~/Desktop/`:

**Requirements (from PRE_LAUNCH_CHECKLIST.md Phase 7.3):**
- Interactive checkboxes with sticky progress bar
- Per-section progress counters
- RPI branding (Navy `#0A2240`, Light Blue `#CAE7F9`, Poppins font)
- Print-friendly (clean page breaks, visible checkbox squares)
- Pass/Fail toggle buttons in summary section
- Self-contained single HTML file (no external dependencies beyond Google Fonts)

**Reference implementation:** `~/Desktop/TESTING_GUIDE_MEDICARE_CENTER.html`

**Prompt for Claude:**
> "Generate an interactive HTML testing checklist from this markdown guide. Follow the pattern in `~/Desktop/TESTING_GUIDE_MEDICARE_CENTER.html` — sticky progress bar, RPI branding, print-friendly, clickable checkboxes."

---

*Template version: v1.0 (February 13, 2026)*
*Based on: PRODASH Medicare Sales Center Testing Guide v165*
*Standard: PRE_LAUNCH_CHECKLIST.md Phase 7.3*
