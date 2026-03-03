# Production Testing Template

> **Copy this template for every production rollout.** Replace `[BRACKETS]` with actual values. Delete sections that don't apply. Add tests as needed.

---

## How to Use This Template

1. **Copy** this file (or use it as the basis for a Google Doc)
2. **Fill in** the header block with release details
3. **Write tests** — one per feature/change, following the numbered format below
4. **Assign** to a tester (team member who did NOT build the feature)
5. **Execute** — tester works through each test, checking boxes
6. **Log issues** in the Issues Found section
7. **Sign off** — tester signs, notes blocking issues, declares rollout readiness

### Test Naming Convention

Each test gets a number and a clear name: `Test 1: [Feature Name]`. Sub-tests use letters: `1A`, `1B`, `1C`.

### What Makes a Good Test

- **Purpose**: One sentence — what are we verifying?
- **Steps**: Numbered, specific, reproducible by someone unfamiliar with the code
- **Expected Results**: Checkboxes with exact values where possible (not "it works")
- **Notes**: Blank line for the tester to document what they actually saw

---

## Template Starts Here

---

# [PROJECT NAME] [VERSION] Testing Guide — [DESCRIPTION]

| | |
|---|---|
| **Version** | [vX.X (@deployment)] |
| **Date** | [YYYY-MM-DD] |
| **Tester** | _______________ |
| **Prepared by** | [Author] |

---

## Prerequisites

Before starting, confirm:

- [ ] [Deployment is live at correct version — include URL if web app]
- [ ] [Required data exists — e.g., "At least one client with Medicare data"]
- [ ] [Required tools/access — e.g., "Browser DevTools Console open (F12)"]
- [ ] [Any SETUP functions that need to run first]

---

## Test 1: [Feature Name]

**Purpose:** [One sentence — what does this test verify?]

**Where:** [Navigation path — e.g., "PRODASH > Accounts > Medicare tab"]

Steps:
1. [Specific action]
2. [Specific action]
3. [Specific action]

Expected Results:
- [ ] [Exact expected outcome with specific values where possible]
- [ ] [Another expected outcome]
- [ ] [No console errors (if UI test)]

Notes: _______________

---

## Test 2: [Feature Name]

**Purpose:** [One sentence]

### 2A: [Sub-feature or scenario]

Steps:
1. [Action]
2. [Action]

Expected Results:
- [ ] [Outcome]
- [ ] [Outcome]

### 2B: [Another scenario]

Steps:
1. [Action]
2. [Action]

Expected Results:
- [ ] [Outcome]
- [ ] [Outcome]

Notes: _______________

---

## Test N: [Data Verification / Spot-Check]

**Purpose:** Verify data landed correctly in the underlying sheet/database.

**Where:** [MATRIX sheet name or database location]

Steps:
1. Open [sheet/database]
2. Find [specific record by name/ID]
3. Check [specific field] = [expected value]

Expected Results:
- [ ] [Field] = [Value]
- [ ] [Field] = [Value]
- [ ] [Field] = [Value]

Notes: _______________

---

## Post-Testing Cleanup

After all tests pass:
- [ ] [Delete test records if applicable]
- [ ] [Revert any test data changes]
- [ ] [Or note: "No cleanup needed — changes are production data"]

---

## Test Summary

| Test | Feature | Status | Notes |
|------|---------|--------|-------|
| 1 | [Feature] | ⬜ Pass / ⬜ Fail | |
| 2A | [Sub-feature] | ⬜ Pass / ⬜ Fail | |
| 2B | [Sub-feature] | ⬜ Pass / ⬜ Fail | |
| N | [Data Verification] | ⬜ Pass / ⬜ Fail | |

---

## Issues Found

| # | Test | Description | Severity | Screenshot |
|---|------|-------------|----------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Severity levels:** BLOCKER (cannot ship) / HIGH (must fix before rollout) / MEDIUM (fix soon) / LOW (nice to fix)

---

## Sign-Off

| | |
|---|---|
| **Tested by** | _______________ |
| **Date** | _______________ |
| **Overall Result** | ⬜ All Pass / ⬜ Issues Found (see above) |
| **Ready for team rollout** | ⬜ Yes / ⬜ No — blocked by: _______________ |

---

## Appendix: Test Types Reference

Use this checklist when deciding what tests to write for a release:

| Release Type | Required Tests |
|-------------|---------------|
| **New UI Feature** | Navigation, CRUD operations, error handling, mobile responsiveness, no console errors |
| **Schema Change** | Column headers exist, data populated, spot-check 3-5 records with exact values |
| **Data Migration/Enrichment** | DryRun counts match, field values correct, no data overwritten, spot-check by client name |
| **API/Integration** | Endpoint responds, auth works, payload structure correct, error handling graceful |
| **Bug Fix** | Original bug no longer reproduces, regression check on related features |
| **Security Change** | Access controls verified, no unauthorized access, audit trail populated |

---

*Template location: `_RPI_STANDARDS/reference/os/PRODUCTION_TESTING_TEMPLATE.md`*
*Pattern source: 6 testing guides from 2.15.26 + 2.16.26 Night Shift (Shared Drive)*
