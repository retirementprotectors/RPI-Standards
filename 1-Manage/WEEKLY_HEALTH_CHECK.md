# Weekly Health Check

> **When to Use**: Weekly audit of all active projects  
> **Frequency**: Every Monday or first day of work week  
> **Time Required**: 15-30 minutes  
> **Version**: v1.0 (January 25, 2026)

---

## Purpose

Quick verification that all projects maintain baseline health:
- Git status clean and synced
- No forbidden code patterns introduced
- MCP tools functioning
- Documentation current

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
| `EXISTING_PROJECT_STANDARDS_AUDIT.md` | Full compliance audit (monthly or new projects) |
| `DOCUMENTATION_CLEANUP_GUIDE.md` | Major doc reorganization needed |
| `ECOSYSTEM_DOCUMENTATION_INVENTORY.md` | Tracking all docs across projects |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 25, 2026 | Initial weekly health check |

---

*A healthy codebase is a productive codebase. 15 minutes weekly prevents hours of firefighting.*
