# Plan: _RPI_STANDARDS Reference Pruning + Enforcement Integration

## Context

The `_RPI_STANDARDS/reference/` directory has 57 files. 47 are dead, stale, or actively contradict `CLAUDE.md`. Yesterday's security audit on the other machine found systemic gaps (appsscript.json vs GAS editor UI disconnect, 5 unchecked web apps, plaintext secrets in git). Two brief files document what to incorporate. This plan prunes reference/ from 57 files to 6, fixes those 6, updates CLAUDE.md, creates 2 hookify rules, and adds documentation maintenance triggers so drift can't recur silently.

**End state:** 6 accurate reference docs. Zero contradictions with CLAUDE.md. 14 hookify rules (12 existing + 2 new). Agent-triggered doc maintenance on project/security changes.

---

## Phase 1: Delete (57 → 6 files)

`git rm` everything in `reference/` EXCEPT the 6 keepers. Also delete the two brief files.

**Keep:**
- `reference/compliance/PHI_POLICY.md`
- `reference/compliance/COMPLIANCE_STANDARDS.md`
- `reference/compliance/SECURITY_COMPLIANCE.md`
- `reference/integrations/GHL_INTEGRATION.md`
- `reference/maintenance/WEEKLY_HEALTH_CHECK.md`
- `reference/maintenance/PROJECT_AUDIT.md`

**Delete (entire directories):**
- `reference/archive/` (23 files — legacy plans, old setup docs)
- `reference/strategic/` (7 files — vision docs, roadmaps)
- `reference/playbooks/` (4 files — team ops docs, includes 2.7MB Sales playbook)
- `reference/new-project/` (1 file — PROJECT_KICKOFF_TEMPLATE, all paths wrong)
- `reference/production/` (3 files — PRE_LAUNCH_CHECKLIST etc., contradicts CLAUDE.md)

**Delete (individual files in kept directories):**
- `reference/compliance/PHI_ACKNOWLEDGMENT_SYSTEM.md`
- `reference/compliance/PHI_TRAINING.md`
- `reference/compliance/AUDIT_LOG_GUIDE.md`
- `reference/compliance/WEBSITE_DISCLOSURES.md`
- `reference/compliance/Millang-Disclosures.docx`
- `reference/compliance/ENFORCEMENT_GAP_ANALYSIS.md`
- `reference/integrations/MATRIX_CONFIG.md`
- `reference/print-velocity-to-pdf.mjs`
- All `.DS_Store` files in reference/

**Delete (root level):**
- `ENFORCEMENT_FIXES_FOR_PRUNING_AGENT.md`

**Total removed:** ~51 files. All preserved in git history.

---

## Phase 2: Fix the 6 Keepers

### 2a. SECURITY_COMPLIANCE.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/compliance/SECURITY_COMPLIANCE.md`

Changes:
- **Line 64**: Change "all 7 apps verified DOMAIN" → "13 GAS web apps identified; 8 verified DOMAIN on 2026-02-13"
- **Line 192 (RIIMO)**: Change "Already compliant (v7)" → "VIOLATION — appsscript.json has ANYONE_ANONYMOUS since initial commit. GAS editor UI showed DOMAIN but source file was wrong."
- **Add 5 apps to verification table** (Part 7): RAPID_API (ANYONE_ANONYMOUS — evaluate if intentional for SPARK webhook), RAPID_IMPORT (not verified), RPI-Command-Center (ANYONE — source file), QUE-Medicare (not verified), DAVID-HUB (ANYONE — source file)
- **Add new section** after Part 2: "Source Code vs. Deployment Access" — explaining appsscript.json is the source of truth, GAS editor UI can diverge, clasp push uses source file
- **Line 63**: Add caveat that CORE_Config.gs has plaintext secrets (syncAllProperties pattern) — flag as known gap with remediation plan
- **Lines 151-154**: Update references to PHI_TRAINING.md and AUDIT_LOG_GUIDE.md (being deleted) — fold critical info inline or remove
- **Line 261**: Fix "All 7 GAS apps" in revision history note
- **Add revision history entry**: 2026-02-14

### 2b. COMPLIANCE_STANDARDS.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/compliance/COMPLIANCE_STANDARDS.md`

Changes:
- **Lines 379-383 (Appendix C)**: Replace stale paths (`0-Setup/`, `1-Manage/`, `2-Production/`) with current `reference/` paths or remove references to killed docs entirely
- **Lines 58, 73-74, 76**: Update internal references — PHI_TRAINING.md reference stays as historical record but note "training materials archived, see PHI_POLICY.md for current requirements"
- **Line 75**: Breach reporting already says "John Behn" — consistent with CLAUDE.md update target

### 2c. PHI_POLICY.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/compliance/PHI_POLICY.md`

Changes:
- **Lines 130-133 (Related Documents)**: Remove reference to PHI_TRAINING.md (being deleted). Keep SECURITY_COMPLIANCE.md and COMPLIANCE_STANDARDS.md references.
- Line 104: Already says "CEO (JDM) or COO (John Behn)" — this is the canonical version. No change needed.

### 2d. GHL_INTEGRATION.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/integrations/GHL_INTEGRATION.md`

Changes:
- **Lines 147-154**: Remove `var` vs `let` section — replace with one line: "See CLAUDE.md GAS Gotcha #7 (var vs let for module-level caching)."
- **Lines 229-233 (Related Documents)**: Remove references to killed docs (GHL_INTEGRATION_GA_TASK_BREAKDOWN, MATRIX_CONFIGURATION_STANDARDS). Keep IMPORT_GHL.gs and API_GHL_Sync.gs references.

### 2e. WEEKLY_HEALTH_CHECK.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/maintenance/WEEKLY_HEALTH_CHECK.md`

Changes:
- **Lines 39-56 (git health loop)**: Add `~/Projects/RAPID_TOOLS/SPARK_WEBHOOK_PROXY` to project list
- **Lines 84-85 (code quality scan)**: Expand from 5 projects to ALL GAS web app projects (add CEO-Dashboard, RIIMO, C3, RAPID_API, RAPID_CORE, RAPID_IMPORT, sentinel-v2, DAVID-HUB, RPI-Command-Center)
- **Add new section "Source Code Security Scan"** after code quality scan:
  - Check all appsscript.json for wrong access settings (grep -v DOMAIN)
  - Check for hardcoded MATRIX IDs outside RAPID_CORE
  - Check for plaintext tokens/secrets in source
  - Check GitHub repo privacy (`gh repo list --visibility public`)
- **Lines 119-128 (MCP table)**: Remove tool count "59 tools" from rpi-workspace. List MCPs by capability only.
- **Lines 215-218 (Integration section)**: Remove references to killed docs (PROJECT_STRUCTURE, PRE_LAUNCH_CHECKLIST). Update remaining references.
- **Add version history entry**: v3.0 Feb 14, 2026

### 2f. PROJECT_AUDIT.md
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/reference/maintenance/PROJECT_AUDIT.md`

Changes:
- **Line 5**: Remove reference to killed PROJECT_KICKOFF_TEMPLATE.md
- **Line 51**: Remove reference to PROJECT_STRUCTURE.md
- **Lines 152-170 (Project Tracker)**: Add SPARK_WEBHOOK_PROXY row
- **Phase 5 (Security Check, lines 100-104)**: Add these checks:
  - `appsscript.json` contains `"access": "DOMAIN"` (source file, not just GAS editor)
  - `appsscript.json` contains `"executionApi": { "access": "DOMAIN" }` (if project needs MCP execute_script)
  - No plaintext secrets in `.gs`, `.json`, `.js` files
  - `.gitignore` includes `credentials.json`, `.env`, `tokens.json`
  - GCP project linked to `90741179392` (manual GAS editor verification)
- **Lines 93-94 (credential grep)**: Fix overly aggressive exclusions — rewrite to not hide secrets mentioned alongside PropertiesService in comments
- **Add version history entry**: v4.0 Feb 14, 2026

---

## Phase 3: Update CLAUDE.md

File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/CLAUDE.md`

### 3a. Add GAS Gotcha #11: appsscript.json is Source of Truth
After existing Gotcha #10 (MATRIX Writes), add:
```
### 11. appsscript.json Controls Web App Access, Not the GAS Editor
`clasp push --force` deploys whatever's in appsscript.json. If someone sets
DOMAIN in the GAS editor but the source file says ANYONE_ANONYMOUS, the next
clasp push silently reverts to ANYONE_ANONYMOUS.
Always fix the source file. Always verify after deploy.
```

### 3b. Remove References to 4 Killed Docs
- **Lines 628-631 (Reference Docs table)**: Remove MATRIX_CONFIG.md, THREE_PLATFORM_ARCHITECTURE.md rows. Keep GHL_INTEGRATION.md and COMPLIANCE_STANDARDS.md.
- **Lines 657-662 (Reference Detection Protocol auto-detect table)**: Remove MATRIX_CONFIG.md trigger → replace with "Read RAPID_CORE/CORE_Database.gs TABLE_ROUTING directly". Remove PROJECT_KICKOFF_TEMPLATE.md trigger. Remove PRE_LAUNCH_CHECKLIST.md trigger.
- **Line 623**: Remove "For detailed checklist: Read reference/new-project/PROJECT_KICKOFF_TEMPLATE.md"
- **Line 781**: Update MATRIX section — change reference from MATRIX_CONFIG.md to "Read `RAPID_CORE/CORE_Database.gs` TABLE_ROUTING directly"

### 3c. Fix Breach Contact
- **Line 266**: Change "Report suspected breaches to John Behn immediately" → "Report suspected breaches to JDM or John Behn immediately" (matches PHI_POLICY.md canonical version)

### 3d. Add Documentation Maintenance Triggers
New section after Reference Detection Protocol (~line 695), before Maintenance Behaviors:

```markdown
## Documentation Maintenance Triggers

When you change the codebase, update the corresponding docs:

| When You...                    | Update These                                          |
|-------------------------------|-------------------------------------------------------|
| Add a new GAS project          | WEEKLY_HEALTH_CHECK.md (project list + scan loop)     |
|                                | PROJECT_AUDIT.md (tracker table)                       |
|                                | SECURITY_COMPLIANCE.md (verification table)            |
|                                | clone-all-repos.sh + setup-hookify-symlinks.sh         |
|                                | CLAUDE.md Project Locations tree                       |
| Add a new GAS web app (webapp) | SECURITY_COMPLIANCE.md (add to verification table)     |
| Complete a security audit      | SECURITY_COMPLIANCE.md (audit trail + dates)           |
| Change deploy process          | CLAUDE.md ONLY — never reference docs                  |
| Add a new MCP tool             | MCP-Hub/CLAUDE.md (directory listing)                  |
| Change compliance rules        | CLAUDE.md = the rule. Reference doc = the procedure.   |

**Rules live in CLAUDE.md. Procedures live in reference docs. Never duplicate rules into reference docs.**
```

### 3e. Add MCP-Hub CLAUDE.md Reference
In the MCP Consolidation Rule section (~line 546), after "Pattern: Export { TOOLS, HANDLERS }...", add:
```
For MCP development standards, directory structure, and OAuth setup: read `MCP-Hub/CLAUDE.md`
```

---

## Phase 4: Create 2 Hookify Rules

### 4a. `hookify.block-anyone-anonymous-access.local.md`
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/hookify/hookify.block-anyone-anonymous-access.local.md`

```yaml
---
name: block-anyone-anonymous-access
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: appsscript\.json$
  - field: content
    operator: regex_match
    pattern: "access":\s*"(ANYONE_ANONYMOUS|ANYONE)"
---
```
Message: Block explaining appsscript.json must have `"access": "DOMAIN"` and why.

### 4b. `hookify.block-credentials-in-config.local.md`
File: `/Users/joshd.millang/Projects/_RPI_STANDARDS/hookify/hookify.block-credentials-in-config.local.md`

```yaml
---
name: block-credentials-in-config
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(gs|json|js)$
  - field: content
    operator: regex_match
    pattern: (xoxb-|xoxp-|hooks\.slack\.com/services|sk-[a-zA-Z0-9]{20,})
---
```
Message: Block explaining plaintext credentials must use Script Properties or env vars.

### 4c. Run setup-hookify-symlinks.sh
Distribute all 14 rules (12 existing + 2 new) to all projects.

---

## Phase 5: Commit & Push

Single commit in _RPI_STANDARDS:
```
v5.2 — Prune reference/ from 57 to 6 docs, integrate enforcement fixes, add doc maintenance triggers

- Delete 51 stale/redundant/dangerous reference docs (preserved in git history)
- Fix 6 surviving docs: correct app counts, add source-file verification, expand scans
- CLAUDE.md: add appsscript.json gotcha, doc maintenance triggers, MCP-Hub reference
- 2 new hookify rules: block-anyone-anonymous-access, block-credentials-in-config
```

---

## Verification

After all changes:
1. `ls reference/` — should show exactly: `compliance/` (3 files), `integrations/` (1 file), `maintenance/` (2 files)
2. `grep -r '0-Setup\|1-Manage\|2-Production\|RPI-Standards/' reference/` — should return 0 results
3. `grep -r 'MATRIX_CONFIG\|PROJECT_KICKOFF\|PRE_LAUNCH_CHECKLIST\|THREE_PLATFORM_ARCHITECTURE' CLAUDE.md` — should return 0 results
4. `ls hookify/*.local.md | wc -l` — should return 14
5. `grep 'appsscript.json' CLAUDE.md` — should find the new gotcha
6. `grep 'Documentation Maintenance' CLAUDE.md` — should find the new triggers section
7. Run `./scripts/setup-hookify-symlinks.sh` — should distribute 14 rules to 16 projects
