# The Operating System — Consolidation Plan

## Context

RPI's governance infrastructure grew organically across 5 policy docs, 21 hookify rules, 4 launchd agents, and scattered CLAUDE.md sections. JDM identified this needs to be unified under **"The Operating System"** — the governance layer that runs The Machine.

**The architecture:**
```
The Machine (the business)
  └── The OS (governance layer)
        ├── Standards         ← the kernel
        ├── Posture           ← access control
        ├── The Immune System ← enforcement + learning
        ├── Monitoring        ← watchdogs + health checks
        └── Operations        ← human processes
```

The Immune System keeps its brand as a named subsystem of The OS.

---

## Phase 1: Create OS Directory + 6 Documents

**New directory:** `~/Projects/_RPI_STANDARDS/reference/os/`

### 1a. OS.md (~100 lines, NET NEW)
The master architecture document. Entry point for understanding The OS.
- The 5-subsystem tree diagram
- How systems connect (Standards → Immune System → Monitoring → Operations → Standards)
- Quick reference: "I need to..." → which doc to read
- The compliance grid (9 layers mapped to OS subsystems)

### 1b. STANDARDS.md (~350 lines, MERGE)
**Source:** `compliance/COMPLIANCE_STANDARDS.md` (396 lines) + `compliance/PHI_POLICY.md` (152 lines)

Merge PHI_POLICY into COMPLIANCE_STANDARDS. PHI is a subset of compliance — currently ~70% overlap.
- Parts 1-3 (Data Classification, HIPAA, Data Handling): keep + merge PHI storage/transmission rules in
- Part 4 (Access Control): **move role tables to POSTURE.md**, keep standards-level rules
- Part 5 (Audit & Logging): keep rules, **move "Current Logging Status" table to MONITORING.md**
- Part 6 (Incident Response): keep categories/timeframes, **move process steps to OPERATIONS.md**
- Parts 7-9 (AI, Vendor, DR): keep as-is
- Part 10 (Training): keep requirements, **move schedule to OPERATIONS.md**
- Part 11 (Compliance Checklist): **move periodic review schedule to MONITORING.md**

### 1c. POSTURE.md (~250 lines, EVOLVE)
**Source:** `compliance/SECURITY_COMPLIANCE.md` (295 lines)

Rename + extract procedures out.
- Part 1 (Client/Partner Statement): keep
- Part 2 (Compliance Checklist): keep (this IS posture)
- Part 3 (Scheduled Tasks): **move to MONITORING.md**
- Part 4 (Offboarding): **move to OPERATIONS.md**
- Part 5 (Incident Response): **move to OPERATIONS.md**
- Part 6 (HIPAA): keep BAA status, **move PHI policies to STANDARDS.md**
- Parts 7-8 (Completed Actions, Remaining Items): keep (posture state)
- **Import** access control tables from STANDARDS.md Part 4

### 1d. IMMUNE_SYSTEM.md (~520 lines, RENAME)
**Source:** `reference/HOOKIFY_SYSTEM.md` (23.6KB)

Rename + add 3-line OS context header. Content is already correct and comprehensive.
- Add: "The Immune System is one of 5 subsystems in The Operating System. See OS.md."
- Update rule count to 21
- Add cross-references to sibling OS docs

### 1e. MONITORING.md (~400 lines, MERGE)
**Source:** `maintenance/PROJECT_AUDIT.md` (203 lines) + `maintenance/WEEKLY_HEALTH_CHECK.md` (265 lines) + extracted content

Structure:
1. Cadences Overview table (daily/weekly/monthly/quarterly)
2. Automated Monitoring (GAS triggers + launchd agents)
3. Weekly Health Check (from WEEKLY_HEALTH_CHECK.md)
4. Project Audit (from PROJECT_AUDIT.md)
5. Periodic Review Schedule (from COMPLIANCE_STANDARDS Part 11)
6. Logging Status (from COMPLIANCE_STANDARDS Part 5)

### 1f. OPERATIONS.md (~200 lines, NEW from extractions)
All human processes consolidated from scattered sources:
1. Documentation Maintenance Triggers (from `~/.claude/CLAUDE.md`)
2. Offboarding Checklist (from SECURITY_COMPLIANCE Part 4)
3. Incident Response Procedure (from COMPLIANCE_STANDARDS Part 6 + SECURITY_COMPLIANCE Part 5, deduplicated)
4. Training Program (from COMPLIANCE_STANDARDS Part 10)
5. New Project Setup (reference to CLAUDE.md steps)
6. PHI Policy Acknowledgment (from PHI_POLICY Section 7)

**Execution:** Spawn 6 parallel agents — one per document.

---

## Phase 2: Backward-Compatible Symlinks

Replace old files with symlinks so existing references don't break:

```
compliance/COMPLIANCE_STANDARDS.md  → ../os/STANDARDS.md
compliance/PHI_POLICY.md            → ../os/STANDARDS.md
compliance/SECURITY_COMPLIANCE.md   → ../os/POSTURE.md
maintenance/PROJECT_AUDIT.md        → ../os/MONITORING.md
maintenance/WEEKLY_HEALTH_CHECK.md  → ../os/MONITORING.md
reference/HOOKIFY_SYSTEM.md         → os/IMMUNE_SYSTEM.md
```

---

## Phase 3: Update ~/.claude/CLAUDE.md (1163 lines, recently cleaned by JDM)

JDM already consolidated dangling footnotes into proper sections (GAS Gotcha #14, OAuth reauth in MCP section). Remaining governance edits:

**A. Lines 1095-1143: Replace "The Machine's Immune System" section** with new "The Operating System" section:
- 5-subsystem tree with doc paths
- Keep enforcement hierarchy + hookify rule type lists + emergency escape hatch
- Keep "Closed Loop (LIVE)" description
- The Immune System becomes a named subsystem, not the whole section

**B. Lines 827-844: Update "Documentation Maintenance Triggers"** — replace old doc names (WEEKLY_HEALTH_CHECK, PROJECT_AUDIT, SECURITY_COMPLIANCE) with OS doc names (MONITORING, POSTURE). Move detailed table to OPERATIONS.md.

**C. Lines 848-866: Slim "Maintenance Behaviors"** — replace procedure descriptions with pointers to OS docs. Keep trigger phrases + launchd list. Update paths:
- Line 853: `reference/maintenance/WEEKLY_HEALTH_CHECK.md` → `reference/os/MONITORING.md`
- Line 865: `reference/compliance/SECURITY_COMPLIANCE.md` → `reference/os/POSTURE.md`
- Line 866: `reference/maintenance/PROJECT_AUDIT.md` → `reference/os/MONITORING.md`

**D. Line 345:** `reference/compliance/PHI_POLICY.md` → `reference/os/STANDARDS.md`

**E. Line 767:** `reference/compliance/COMPLIANCE_STANDARDS.md` → `reference/os/STANDARDS.md`

**F. Line 791:** `reference/compliance/COMPLIANCE_STANDARDS.md` → `reference/os/STANDARDS.md`

**G. Line 762:** Update "New Project Setup" step 11 doc names (MONITORING.md, POSTURE.md instead of old names)

---

## Phase 4: Update Project CLAUDE.md Files (7 files)

Parallel agents update old path references in:

| File | Change |
|------|--------|
| `PRODASHX/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `CEO-Dashboard/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `RPI-Command-Center/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `DEX/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `PDF_SERVICE/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `MCP-Hub/CLAUDE.md` | COMPLIANCE_STANDARDS → STANDARDS |
| `_RPI_STANDARDS/CLAUDE.md` | Multiple path updates |

---

## Phase 5: Update Hookify Rule References (4 rules)

| Rule | Change |
|------|--------|
| `block-anyone-anonymous-access` | SECURITY_COMPLIANCE → POSTURE |
| `block-hardcoded-secrets` | SECURITY_COMPLIANCE → POSTURE |
| `block-credentials-in-config` | SECURITY_COMPLIANCE → POSTURE |
| `warn-phi-in-error-message` | COMPLIANCE_STANDARDS → STANDARDS |

**Do NOT merge** `block-hardcoded-secrets` + `block-credentials-in-config` — they serve complementary purposes (generic safety net vs. specific credential format detection).

---

## Phase 6: Update Desktop Grid + MEMORY.md

- Update `/Users/joshd.millang/Desktop/RPI-Compliance-Security-Audit-Grid.md` with OS subsystem mapping
- Clean up MEMORY.md — remove items now covered by OS docs

---

## Phase 7: Git Commit + Push

Commit _RPI_STANDARDS + all updated project repos. One commit per repo.

---

## Phase 8: GAS Watchdog Activation (Requires JDM for 2 triggers)

Verify which of the 5 GAS triggers are live via `execute_script`. For any pending triggers that require editor auth (likely `SETUP_NewUserDetection` and `SETUP_AutoOffboard`), JDM runs them manually.

---

## Execution Strategy

| Phase | Parallel? | Depends On |
|-------|-----------|------------|
| 1 (6 OS docs) | 6 parallel agents | Nothing |
| 2 (Symlinks) | Sequential | Phase 1 |
| 3 (Global CLAUDE.md) | Sequential | Phase 1 |
| 4 (7 project CLAUDE.md) | 7 parallel agents | Phase 1 |
| 5 (4 hookify rules) | Sequential | Phase 1 |
| 6 (Grid + MEMORY) | Parallel with 3-5 | Phase 1 |
| 7 (Git) | Sequential | Phases 2-6 |
| 8 (GAS Watchdog) | JDM action | Independent |

Phases 1, 3-6 can overlap. Phase 2 must follow 1. Phase 7 is last.

---

## Verification

1. **Symlink check** — all 6 old paths resolve to new OS docs
2. **Content completeness** — every section from every old doc appears in exactly one OS doc
3. **Path scan** — grep all project CLAUDE.md files for old paths (should find 0)
4. **CLAUDE.md rule integrity** — all RULES still in CLAUDE.md (only PROCEDURES moved out)
5. **Hookify rule scan** — all 4 updated rules reference new paths
6. **Read test** — read each OS doc to verify formatting and cross-references

---

## Growth Path

- **Q2 2026:** `knowledge-promote.js` routes findings to specific OS subsystem docs. New `intent-os-check` hookify rule for "check the OS" structured briefing.
- **Q2-Q3 2026:** MDJ instance governance adds per-instance rules to IMMUNE_SYSTEM.md, MDJ health checks to MONITORING.md
- **H2 2026:** M&A partner onboarding uses STANDARDS.md as compliance baseline, OPERATIONS.md for partner checklists
- **Ongoing:** Detection → enforcement → learning loop becomes self-correcting for known patterns

---

## Critical Files

| File | Role |
|------|------|
| `~/.claude/CLAUDE.md` | Global rules — surgical edits to governance sections |
| `_RPI_STANDARDS/reference/compliance/COMPLIANCE_STANDARDS.md` | Largest source (396 lines), becomes STANDARDS.md |
| `_RPI_STANDARDS/reference/compliance/PHI_POLICY.md` | Merges INTO STANDARDS.md |
| `_RPI_STANDARDS/reference/compliance/SECURITY_COMPLIANCE.md` | Becomes POSTURE.md |
| `_RPI_STANDARDS/reference/HOOKIFY_SYSTEM.md` | Becomes IMMUNE_SYSTEM.md |
| `_RPI_STANDARDS/reference/maintenance/PROJECT_AUDIT.md` | Merges into MONITORING.md |
| `_RPI_STANDARDS/reference/maintenance/WEEKLY_HEALTH_CHECK.md` | Merges into MONITORING.md |
