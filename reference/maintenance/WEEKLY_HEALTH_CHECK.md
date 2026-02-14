# Weekly Health Check

> **When to Use**: Weekly audit of all active projects
> **Frequency**: Every Monday or first day of work week
> **Time Required**: 15-30 minutes (automated via Claude Code)
> **Version**: v3.0 (February 14, 2026)

---

## Purpose

Quick verification that all projects maintain baseline health:
- Git status clean and synced
- No forbidden code patterns introduced
- MCP tools functioning
- Documentation current

This is a **quick check**, not a full audit. For comprehensive project audits, use `PROJECT_AUDIT.md`.

---

## How to Run

Tell Claude Code: **"weekly check"** or **"health check"**

Claude Code will automatically:
1. Check git status across all 16 projects (using SuperProject paths)
2. Scan for forbidden code patterns
3. Verify documentation status
4. Report results

---

## Weekly Checklist

### 1. Git Health (All 16 Projects)

```bash
for repo in \
  ~/Projects/_RPI_STANDARDS \
  ~/Projects/PRODASH_TOOLS/PRODASH \
  ~/Projects/PRODASH_TOOLS/QUE/QUE-Medicare \
  ~/Projects/RAPID_TOOLS/C3 \
  ~/Projects/RAPID_TOOLS/CAM \
  ~/Projects/RAPID_TOOLS/CEO-Dashboard \
  ~/Projects/RAPID_TOOLS/DEX \
  ~/Projects/RAPID_TOOLS/MCP-Hub \
  ~/Projects/RAPID_TOOLS/PDF_SERVICE \
  ~/Projects/RAPID_TOOLS/RAPID_API \
  ~/Projects/RAPID_TOOLS/RAPID_CORE \
  ~/Projects/RAPID_TOOLS/RAPID_IMPORT \
  ~/Projects/RAPID_TOOLS/SPARK_WEBHOOK_PROXY \
  ~/Projects/RAPID_TOOLS/RIIMO \
  ~/Projects/RAPID_TOOLS/RPI-Command-Center \
  ~/Projects/SENTINEL_TOOLS/DAVID-HUB \
  ~/Projects/SENTINEL_TOOLS/sentinel \
  ~/Projects/SENTINEL_TOOLS/sentinel-v2; do
  name=$(echo "$repo" | sed "s|$HOME/Projects/||")
  git_short=$(git -C "$repo" status --short 2>/dev/null)
  branch=$(git -C "$repo" branch --show-current 2>/dev/null)
  last=$(git -C "$repo" log -1 --format="%ar" 2>/dev/null)
  if [ -z "$git_short" ]; then
    echo "$name | CLEAN | $branch | $last"
  else
    count=$(echo "$git_short" | wc -l | tr -d ' ')
    echo "$name | DIRTY ($count) | $branch | $last"
  fi
done
```

**Red Flags**:
- `DIRTY` → Commit and push
- `fatal: not a git repository` → Git not initialized (CRITICAL)
- Last commit > 2 weeks ago on active project → Check if stale

---

### 2. Code Quality Scan

Scan for forbidden patterns across all GAS web apps:

```bash
# alert()/confirm()/prompt() — actual function calls only
# Exclude: variable names, CSS classes, comments, parameter names
for repo in ~/Projects/PRODASH_TOOLS/PRODASH ~/Projects/PRODASH_TOOLS/QUE/QUE-Medicare \
  ~/Projects/RAPID_TOOLS/C3 ~/Projects/RAPID_TOOLS/CAM ~/Projects/RAPID_TOOLS/CEO-Dashboard \
  ~/Projects/RAPID_TOOLS/DEX ~/Projects/RAPID_TOOLS/RIIMO ~/Projects/RAPID_TOOLS/RPI-Command-Center \
  ~/Projects/RAPID_TOOLS/RAPID_API ~/Projects/RAPID_TOOLS/RAPID_CORE ~/Projects/RAPID_TOOLS/RAPID_IMPORT \
  ~/Projects/SENTINEL_TOOLS/sentinel ~/Projects/SENTINEL_TOOLS/sentinel-v2 ~/Projects/SENTINEL_TOOLS/DAVID-HUB; do
  name=$(basename "$repo")
  grep -rn '\balert(\|confirm(\|prompt(' "$repo"/*.html "$repo"/*.gs 2>/dev/null \
    | grep -v 'showConfirm\|showToast\|showAlert\|//\|CLAUDE\|\.md' | head -3
done

# Hardcoded inline colors
for repo in ~/Projects/PRODASH_TOOLS/PRODASH ~/Projects/PRODASH_TOOLS/QUE/QUE-Medicare \
  ~/Projects/RAPID_TOOLS/C3 ~/Projects/RAPID_TOOLS/CAM ~/Projects/RAPID_TOOLS/CEO-Dashboard \
  ~/Projects/RAPID_TOOLS/DEX ~/Projects/RAPID_TOOLS/RIIMO ~/Projects/RAPID_TOOLS/RPI-Command-Center \
  ~/Projects/RAPID_TOOLS/RAPID_API ~/Projects/RAPID_TOOLS/RAPID_CORE ~/Projects/RAPID_TOOLS/RAPID_IMPORT \
  ~/Projects/SENTINEL_TOOLS/sentinel ~/Projects/SENTINEL_TOOLS/sentinel-v2 ~/Projects/SENTINEL_TOOLS/DAVID-HUB; do
  name=$(basename "$repo")
  grep -rn 'style=.*#[0-9a-fA-F]\{3,6\}' "$repo"/*.html 2>/dev/null | head -3
done
```

**Known violations to track:**

| Project | Issue | Severity |
|---------|-------|----------|
| QUE-Medicare | 3x `alert()` + 1x `confirm()` in Scripts.html | HIGH — real forbidden calls |
| PRODASH | Hardcoded hex colors in Index.html + C3-Evolution.html | MEDIUM |
| QUE-Medicare | Hardcoded hex colors in Index.html + Scripts.html | MEDIUM |
| DEX | Hardcoded hex colors in Index.html (input modal) | LOW |
| sentinel | Hardcoded hex colors in Index.html (modals) | LOW |

### Source Code Security Scan

```bash
# Check all appsscript.json for wrong access settings
grep -rn '"access"' ~/Projects/*/appsscript.json ~/Projects/*/*/appsscript.json 2>/dev/null | grep -v DOMAIN

# Check for hardcoded MATRIX IDs outside RAPID_CORE
grep -rn '1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU\|1K_DLb-txoI4F1dLrUyoFOuFc0xwsH1iW5eff3pQ_o6E' ~/Projects/ --include='*.gs' --include='*.html' --include='*.json' 2>/dev/null | grep -v RAPID_CORE | grep -v node_modules

# Check for plaintext tokens/secrets in source
grep -rn 'xoxb-\|xoxp-\|hooks\.slack\.com/services' ~/Projects/ --include='*.gs' --include='*.js' --include='*.json' 2>/dev/null | grep -v node_modules

# Check GitHub repo privacy
gh repo list retirementprotectors --visibility public 2>/dev/null
```

**Red Flags**:
- Any `appsscript.json` NOT showing DOMAIN (except RAPID_API -- approved exception for SPARK webhook)
- Any MATRIX IDs outside RAPID_CORE
- Any plaintext tokens in source files
- Any public repos

---

### 3. MCP Tools Verification

```bash
claude mcp list
```

**Check these are running:**

| MCP | Type | What It Does |
|-----|------|--------------|
| rpi-workspace | Consolidated | GAS execution, Chat, People, WordPress, Canva, Video |
| rpi-business | Consolidated | Commission intelligence, Meeting processor |
| rpi-healthcare | Consolidated | NPI, ICD-10, CMS coverage |
| gdrive | Third-party | Google Drive access |
| google-calendar | Third-party | Calendar events |
| gmail | Third-party | Read/send email |
| slack | Third-party | Slack messages/channels |
| playwright | Plugin | Browser automation |

---

### 4. Documentation Spot Check

Pick one project each week and verify:

- [ ] `CLAUDE.md` exists and is current
- [ ] `Docs/0-SESSION_HANDOFF.md` reflects current state
- [ ] Version number in handoff matches deployed version

**Projects missing session handoffs (as of 2026-02-13):**
- QUE-Medicare, C3, MCP-Hub, PDF_SERVICE, RIIMO, RPI-Command-Center, sentinel-v2

**Projects missing Docs/ directory entirely:**
- PDF_SERVICE, RIIMO

---

## Weekly Report Template

```markdown
## Weekly Health Check Report
**Date**: YYYY-MM-DD
**Checked by**: Claude Code GA

### Git Status
| Project | Status | Last Commit | Notes |
|---------|--------|-------------|-------|
| _RPI_STANDARDS | ✅/⚠️ | X ago | |
| PRODASH_TOOLS/PRODASH | ✅/⚠️ | X ago | |
| PRODASH_TOOLS/QUE/QUE-Medicare | ✅/⚠️ | X ago | |
| RAPID_TOOLS/C3 | ✅/⚠️ | X ago | |
| RAPID_TOOLS/CAM | ✅/⚠️ | X ago | |
| RAPID_TOOLS/CEO-Dashboard | ✅/⚠️ | X ago | |
| RAPID_TOOLS/DEX | ✅/⚠️ | X ago | |
| RAPID_TOOLS/MCP-Hub | ✅/⚠️ | X ago | |
| RAPID_TOOLS/PDF_SERVICE | ✅/⚠️ | X ago | |
| RAPID_TOOLS/RAPID_API | ✅/⚠️ | X ago | |
| RAPID_TOOLS/RAPID_CORE | ✅/⚠️ | X ago | |
| RAPID_TOOLS/RAPID_IMPORT | ✅/⚠️ | X ago | |
| RAPID_TOOLS/RIIMO | ✅/⚠️ | X ago | |
| RAPID_TOOLS/RPI-Command-Center | ✅/⚠️ | X ago | |
| SENTINEL_TOOLS/DAVID-HUB | ✅/⚠️ | X ago | |
| SENTINEL_TOOLS/sentinel | ✅/⚠️ | X ago | |
| SENTINEL_TOOLS/sentinel-v2 | ✅/⚠️ | X ago | |

### Code Quality
- [ ] No new forbidden pattern violations

### MCP Tools
- [ ] All MCPs connected

### Documentation
- **Spot-checked**: [PROJECT_NAME]

### Issues Found
[List any issues and remediation taken]

### Status: ✅ HEALTHY / ⚠️ NEEDS ATTENTION
```

---

## Escalation Triggers

**Immediate Action Required**:
- Git not initialized on any project
- MCP tools all failing (auth issue)
- New `alert()`/`confirm()`/`prompt()` calls in production code

**Schedule Fix This Week**:
- Uncommitted changes older than 3 days
- Out-of-date session handoffs
- New hardcoded colors introduced

**Note for Next Week**:
- Minor documentation gaps
- Non-critical MCP failures

---

## Integration with Other Standards

| Related Standard | When to Use Instead |
|-----------------|---------------------|
| `reference/compliance/COMPLIANCE_STANDARDS.md` | Security/PHI concerns discovered |
| `reference/maintenance/PROJECT_AUDIT.md` | Full compliance audit (monthly or new projects) |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3.0 | Feb 14, 2026 | Expanded scans to all projects, added source code security scan, removed stale doc references |
| v2.0 | Feb 13, 2026 | Rewritten for SuperProject paths, Claude Code (not Cursor), consolidated MCPs, all 16 projects |
| v1.2 | Feb 1, 2026 | Added GAS DevTools Pattern Check |
| v1.1 | Jan 25, 2026 | Added Project Alignment Audit |
| v1.0 | Jan 25, 2026 | Initial weekly health check |

---

*A healthy codebase is a productive codebase. 15 minutes weekly prevents hours of firefighting.*
