# Existing Project Standards Audit

> **When to Use**: Verifying an EXISTING project follows RPI-Standards
> **Counterpart**: See CLAUDE.md "New Project Setup" section (for NEW projects)
> **How to Run**: Tell Claude Code "audit [PROJECT_NAME]"
> **Version**: v4.0 (February 14, 2026)

---

## Purpose

This audit verifies an **existing project** is fully compliant with RPI-Standards. It checks everything the Kickoff Template establishes, but retroactively.

| Kickoff Template | This Audit |
|------------------|------------|
| "Build it right" | "Is it right?" |
| Day 0 | Any day after |
| Creates docs | Verifies docs |

---

## What Gets Checked

| Category | Items |
|----------|-------|
| **Git & Deployment** | Git initialized, remote set, on main branch, synced |
| **Document Structure** | CLAUDE.md, Docs/ with handoff + briefing |
| **Standards Reference** | References `_RPI_STANDARDS/`, doesn't copy |
| **Code Quality** | No `alert()`/`confirm()`/`prompt()`, structured responses, no hardcoded colors |
| **Security** | Org-only access, no hardcoded credentials, Script Properties for secrets |
| **PHI Compliance** | No PHI in logs/errors, SSN masking, PHI only in Workspace |

---

## Audit Phases

### Phase 1: Git & Infrastructure

```bash
cd ~/Projects/[SUPERPROJECT]/[PROJECT_NAME]
git status
git remote -v
git log --oneline -5
```

**Expected**:
- On branch `main`
- Remote origin: `https://github.com/retirementprotectors/[REPO_NAME].git`
- Recent commits, clean working tree

**Note**: GitHub repo names may differ from local folder names.

---

### Phase 2: Document Structure

**Required documents:**

| Document | Required | Purpose |
|----------|----------|---------|
| `CLAUDE.md` | All projects | Project context for Claude Code |
| `Docs/0-SESSION_HANDOFF*.md` | GAS projects | Current state, continuity |
| `Docs/1-AGENT_BRIEFING.md` | GAS projects | Project context |
| `.clasp.json` | GAS projects | Script ID configuration |
| `appsscript.json` | GAS projects | GAS manifest |

---

### Phase 3: Standards Compliance

**CLAUDE.md must include or reference:**
- Project-specific context (what this project does, key modules)
- Required References section pointing to `_RPI_STANDARDS/reference/`
- Deployment ID for `clasp deploy -i`

**Must NOT contain:**
- Copies of global standards (reference `_RPI_STANDARDS/` instead)
- Outdated paths (`0-Setup/`, `1-Manage/`, `2-Production/`)

---

### Phase 4: Code Quality Scan

```bash
# Forbidden function calls
grep -rn '\balert(\|confirm(\|prompt(' *.html *.gs 2>/dev/null \
  | grep -v 'showConfirm\|showToast\|showAlert\|//\|CLAUDE\|\.md'

# Hardcoded colors
grep -rn 'style=.*#[0-9a-fA-F]\{3,6\}' *.html 2>/dev/null

# Plaintext credentials (tokens, webhook URLs, API keys)
grep -rn 'xoxb-\|xoxp-\|hooks\.slack\.com/services\|sk-[a-zA-Z0-9]\{20,\}' *.gs *.js *.json 2>/dev/null | grep -v node_modules

# Generic secret patterns (review manually — may include false positives)
grep -rn 'api_key\|apiKey\|password\|secret' *.gs 2>/dev/null \
  | grep -v 'PropertiesService\|getProperty\|CLAUDE\|\.md\|//\|function\|param'
```

---

### Phase 5: Security Check

- [ ] `appsscript.json` contains `"access": "DOMAIN"` (source file, not just GAS editor UI)
- [ ] `appsscript.json` contains `"executionApi": { "access": "DOMAIN" }` (if project needs MCP execute_script)
- [ ] No hardcoded credentials in code (all in Script Properties)
- [ ] No plaintext secrets in `.gs`, `.json`, `.js` files (check for `xoxb-`, `xoxp-`, webhook URLs, API keys)
- [ ] `.gitignore` includes `credentials.json`, `.env`, `tokens.json`
- [ ] GCP project linked to `90741179392` (manual GAS editor verification: Settings > GCP Project)
- [ ] No PHI in console.log/Logger.log statements
- [ ] Error messages don't expose sensitive data

---

## Audit Report Format

```markdown
## Standards Audit Report: [PROJECT_NAME]
**Date**: YYYY-MM-DD
**Path**: ~/Projects/[SUPERPROJECT]/[PROJECT_NAME]

### Git
| Check | Status |
|-------|--------|
| Git initialized | ✅/❌ |
| Remote set correctly | ✅/❌ |
| On main branch | ✅/❌ |
| Clean working tree | ✅/❌ |

### Documentation
| Document | Status |
|----------|--------|
| CLAUDE.md | ✅/❌ |
| Docs/0-SESSION_HANDOFF.md | ✅/❌/N/A |
| .clasp.json | ✅/❌/N/A |

### Code Quality
| Check | Status |
|-------|--------|
| No alert()/confirm()/prompt() | ✅/❌ |
| No hardcoded colors | ✅/❌ |
| No hardcoded credentials | ✅/❌ |
| Structured responses ({success, data/error}) | ✅/❌ |

### Security
| Check | Status |
|-------|--------|
| Org-only access | ✅/❌/⏳ |
| Script Properties for secrets | ✅/❌ |
| No PHI in logs | ✅/❌ |

### Final Status: ✅ COMPLIANT / ⚠️ PARTIAL / ❌ NEEDS WORK
```

---

## Project Tracker

| Project | Path | Last Audit | Status |
|---------|------|------------|--------|
| _RPI_STANDARDS | `_RPI_STANDARDS` | 2026-02-13 | ✅ |
| PRODASHX | `PRODASHX_TOOLS/PRODASHX` | 2026-02-04 | ✅ |
| QUE-Medicare | `PRODASHX_TOOLS/QUE/QUE-Medicare` | — | ⏳ |
| C3 | `RAPID_TOOLS/C3` | 2026-02-04 | ✅ |
| CAM | `RAPID_TOOLS/CAM` | 2026-02-04 | ✅ |
| CEO-Dashboard | `RAPID_TOOLS/CEO-Dashboard` | — | ⏳ |
| DEX | `RAPID_TOOLS/DEX` | — | ⏳ |
| MCP-Hub | `RAPID_TOOLS/MCP-Hub` | — | ⏳ |
| PDF_SERVICE | `RAPID_TOOLS/PDF_SERVICE` | — | ⏳ |
| RAPID_API | `RAPID_TOOLS/RAPID_API` | 2026-02-04 | ✅ |
| RAPID_CORE | `RAPID_TOOLS/RAPID_CORE` | 2026-02-04 | ✅ |
| RAPID_IMPORT | `RAPID_TOOLS/RAPID_IMPORT` | — | ⏳ |
| RIIMO | `RAPID_TOOLS/RIIMO` | — | ⏳ |
| RPI-Command-Center | `RAPID_TOOLS/RPI-Command-Center` | — | ⏳ |
| DAVID-HUB | `SENTINEL_TOOLS/DAVID-HUB` | 2026-02-04 | ✅ |
| sentinel | `SENTINEL_TOOLS/sentinel` | 2026-02-04 | ✅ |
| sentinel-v2 | `SENTINEL_TOOLS/sentinel-v2` | — | ⏳ |
| SPARK_WEBHOOK_PROXY | `RAPID_TOOLS/SPARK_WEBHOOK_PROXY` | — | ⏳ |

---

## Batch Audit Tips

1. **Parallel Execution**: Claude Code spawns sub-agents per project — independent audits run simultaneously
2. **Fix as you go**: Don't just report — fix issues when found
3. **Commit per project**: Each project gets its own commit with message `docs: RPI-Standards audit - [summary]`
4. **Update tracker**: Mark projects as compliant after successful audit

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v4.0 | Feb 14, 2026 | Added source file verification, expanded security checks, added SPARK_WEBHOOK_PROXY |
| v3.0 | Feb 13, 2026 | Rewritten for SuperProject paths, Claude Code, simplified phases, updated tracker |
| v2.0 | Jan 11, 2026 | Added deployment prompt format |
| v1.0 | Jan 2026 | Initial audit checklist |

---

*One standard. Every project. No exceptions.*
