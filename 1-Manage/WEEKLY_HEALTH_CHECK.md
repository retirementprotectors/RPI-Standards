# Weekly Health Check

> **When to Use**: Weekly audit of all active projects  
> **Frequency**: Every Monday or first day of work week  
> **Time Required**: 15-30 minutes  
> **Version**: v1.1 (January 25, 2026)

---

## Purpose

Quick verification that all projects maintain baseline health:
- Git status clean and synced
- No forbidden code patterns introduced
- MCP tools functioning
- Documentation current
- **Project alignment with vision** (monthly or on-demand)

This is a **quick check**, not a full audit. For comprehensive project audits, use `EXISTING_PROJECT_STANDARDS_AUDIT.md`.

---

## Weekly Checklist

### 1. Git Health (All Projects)

Run this script to check all projects at once:

```bash
cd /Users/joshd.millang/Projects

for dir in RPI-Standards CAM DAVID-HUB PRODASH sentinel RAPID_CORE RAPID_IMPORT RAPID_API; do
  echo "=== $dir ==="
  if [ -d "$dir" ]; then
    cd "$dir"
    git status --short
    git remote -v | head -1
    cd ..
  else
    echo "  [NOT FOUND]"
  fi
  echo ""
done
```

**Expected**: Each project shows clean status and correct origin URL.

**Red Flags**:
- `fatal: not a git repository` → Git not initialized (CRITICAL)
- Uncommitted changes → Commit and push
- Ahead/behind origin → Sync with remote

---

### 2. Code Quality Scan

Quick check for forbidden patterns across all projects:

```bash
cd /Users/joshd.millang/Projects

# Check for alert/confirm/prompt
echo "=== Checking for alert/confirm/prompt ==="
for dir in CAM DAVID-HUB PRODASH sentinel; do
  if [ -d "$dir" ]; then
    results=$(grep -rn "alert\|confirm\|prompt" "$dir"/*.html "$dir"/*.gs 2>/dev/null | grep -v "showConfirm\|showToast" | head -5)
    if [ -n "$results" ]; then
      echo "⚠️ $dir:"
      echo "$results"
    fi
  fi
done

# Check for hardcoded colors
echo ""
echo "=== Checking for hardcoded colors ==="
for dir in CAM DAVID-HUB PRODASH sentinel; do
  if [ -d "$dir" ]; then
    results=$(grep -rn 'style=.*#[0-9a-fA-F]' "$dir"/*.html 2>/dev/null | head -3)
    if [ -n "$results" ]; then
      echo "⚠️ $dir:"
      echo "$results"
    fi
  fi
done
```

**Expected**: No output (clean).

**If violations found**: Create task to fix, assign to appropriate SPC.

---

### 3. MCP Tools Verification

Open Cursor → Settings → Tools & MCP

**Check these are Connected**:
| MCP Server | Status |
|------------|--------|
| gdrive | ✅ Connected |
| gmail | ✅ Connected |
| google-calendar | ✅ Connected |
| slack | ✅ Connected |
| npi-registry | ✅ Connected |
| medicare-plans | ✅ Connected |
| commission-intelligence | ✅ Connected |

**If any show Error**: See `0-Setup/NEW_MACHINE_SETUP.md` for troubleshooting.

---

### 4. Standards Repo Sync

```bash
cd /Users/joshd.millang/Projects/RPI-Standards
git fetch origin
git status
```

**Expected**: `Your branch is up to date with 'origin/main'`

**If behind**: `git pull` to get latest standards.

---

### 5. Documentation Spot Check

Pick one project each week and verify:

- [ ] `Docs/0-SESSION_HANDOFF.md` reflects current state
- [ ] Version number in handoff matches deployed version
- [ ] No stale `FIX_*.md` or `TEST_*.md` files in root

---

### 6. Project Alignment Audit (Monthly or On-Demand)

Run a deeper check across all projects for vision alignment, drift, redundancies, and blind spots.

**When to run**: Monthly, or when prompted with "run project alignment audit"

#### Vision Alignment Check

For each project's `Docs/1-AGENT_BRIEFING.md`:
- [ ] Purpose still aligns with overall vision (see `0-Setup/AI_PLATFORM_STRATEGIC_ROADMAP.md`)
- [ ] No project has drifted into scope of another
- [ ] Module status reflects actual code state (no stale "Not Started" on completed modules)

#### Stale Reference Scan

```bash
cd /Users/joshd.millang/Projects
for dir in CAM DAVID-HUB PRODASH sentinel RAPID_CORE RAPID_IMPORT RAPID_API; do
  echo "=== $dir ==="
  grep -rn "_RPI_STANDARDS\|+0-\|+1-\|+2-" "$dir/Docs/" 2>/dev/null | head -5 || echo "  Clean"
done
```

**Expected**: No output (all references updated to `0-Setup/`, `1-Manage/`, `2-Production/`).

#### Redundancy Check

- [ ] No two projects duplicating the same functionality
- [ ] Shared code lives in RAPID_CORE, not copied into individual projects
- [ ] No duplicate documentation across projects (reference RPI-Standards instead)

#### Blind Spot Scan

- [ ] All projects have session handoffs (`Docs/0-SESSION_HANDOFF.md`)
- [ ] Security concerns documented (auth gaps, PHI handling)
- [ ] Dependencies between projects documented in briefings
- [ ] Compliance considerations noted where applicable (see `0-Setup/COMPLIANCE_STANDARDS.md`)

#### Project Status Summary

| Project | Vision Aligned | Stale Refs | Session Handoff | Notes |
|---------|---------------|------------|-----------------|-------|
| CAM | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| DAVID-HUB | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| PRODASH | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| sentinel | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| RAPID_CORE | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| RAPID_IMPORT | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |
| RAPID_API | ✅ / ⚠️ | ✅ / ⚠️ | ✅ / ⚠️ | |

---

## Weekly Report Template

```markdown
## Weekly Health Check Report
**Date**: YYYY-MM-DD
**Checked by**: [Agent/Person]

### Git Status
| Project | Status | Notes |
|---------|--------|-------|
| RPI-Standards | ✅ | Clean |
| CAM | ✅ | Clean |
| DAVID-HUB | ✅ | Clean |
| PRODASH | ✅ | Clean |
| sentinel | ✅ | Clean |

### Code Quality
- [ ] No forbidden patterns found

### MCP Tools
- [ ] All MCPs connected

### Documentation
- **Spot-checked**: [PROJECT_NAME]
- [ ] Handoff current
- [ ] No stale temp files

### Project Alignment (if run this week)
- [ ] All projects aligned with vision
- [ ] No stale references found
- [ ] No redundancies identified
- [ ] Blind spots: [List any found]

### Issues Found
[List any issues and remediation taken]

### Status: ✅ HEALTHY / ⚠️ NEEDS ATTENTION
```

---

## Escalation Triggers

**Immediate Action Required**:
- Git not initialized on any project
- MCP tools all failing (auth issue)
- Forbidden patterns in production code

**Schedule Fix This Week**:
- Uncommitted changes older than 3 days
- Out-of-date session handoffs
- Temp files accumulating

**Note for Next Week**:
- Minor documentation gaps
- Non-critical MCP failures

---

## Integration with Other Standards

| Related Standard | When to Use Instead |
|-----------------|---------------------|
| `0-Setup/AI_PLATFORM_STRATEGIC_ROADMAP.md` | Vision reference for alignment checks |
| `0-Setup/COMPLIANCE_STANDARDS.md` | Security/PHI concerns discovered |
| `EXISTING_PROJECT_STANDARDS_AUDIT.md` | Full compliance audit (monthly or new projects) |
| `DOCUMENTATION_CLEANUP_GUIDE.md` | Major doc reorganization needed |
| `ECOSYSTEM_DOCUMENTATION_INVENTORY.md` | Tracking all docs across projects |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.1 | Jan 25, 2026 | Added Project Alignment Audit (Section 6) |
| v1.0 | Jan 25, 2026 | Initial weekly health check |

---

*A healthy codebase is a productive codebase. 15 minutes weekly prevents hours of firefighting.*
