# Documentation Cleanup Guide

> **When to Use**: During project audits or when a project has accumulated scattered docs  
> **Counterpart**: `+0- PROJECT_KICKOFF_TEMPLATE.md` (prevents this from happening)  
> **Version**: v1.0 (January 25, 2026)

---

## The Problem

Projects accumulate documentation debt:
- Task-specific docs created during debugging (`FIX_*.md`, `CHECK_*.md`, `TEST_*.md`)
- Agent scope docs in root instead of `Docs/`
- Plan files scattered across Desktop, project roots, or trash
- Duplicate standards copied into projects instead of referenced

**Root Cause**: The Project Kickoff Template creates `Docs/` but doesn't enforce ongoing organization. Agents create docs where convenient, not where correct.

---

## Standard Project Structure

### What Goes Where

| Location | Content | Examples |
|----------|---------|----------|
| **Project Root** | Code, config, README only | `Code.gs`, `appsscript.json`, `.clasp.json`, `README.md` |
| **`Docs/`** | Agent scope docs, session handoff | `1-AGENT_BRIEFING.md`, `2.x-AGENT_SCOPE_*.md` |
| **`Docs/User/`** | Human-facing guides | `Admin_Guide.html`, `Overview.html` |
| **`RPI-Standards/`** | Universal standards (reference, don't copy) | `+0-*.md`, `+1-*.md` |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Agent Docs | Numbered prefix | `0-SESSION_HANDOFF.md`, `1-AGENT_BRIEFING.md` |
| Universal Standards | `+0-` or `+1-` prefix | `+0- MASTER_AGENT_FRAMEWORK.md` |
| Task/Debug Docs | `FIX_`, `CHECK_`, `TEST_` prefix | `FIX_VERSION_UNDEFINED.md` |
| Plan Files | `.plan.md` extension | `cam_comp_grid_build.plan.md` |

---

## Cleanup Process

### Step 1: Inventory Root Docs

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
ls *.md | wc -l
```

**Goal**: Only `README.md` should be in root. All other `.md` files belong in `Docs/`.

### Step 2: Move Agent Docs to Docs/

```bash
# Create Docs/ if missing
mkdir -p Docs/

# Move agent scope docs
mv 0-SESSION_HANDOFF.md Docs/
mv 1-AGENT_BRIEFING.md Docs/
mv 2.*-AGENT_SCOPE_*.md Docs/
mv 3.*-AGENT_SCOPE_*.md Docs/
```

### Step 3: Review Task-Specific Docs

Task docs (`FIX_*.md`, `CHECK_*.md`, `TEST_*.md`, `TASK_*.md`) fall into two categories:

| Outcome | Action |
|---------|--------|
| **Still Relevant** | Move to `Docs/` |
| **Completed/Obsolete** | Delete or archive |

**Decision Criteria:**
- Does this doc describe a one-time fix that's already applied? → Delete
- Does this doc describe a recurring process? → Move to `Docs/`
- Does this doc have universal value? → Move to `RPI-Standards/`

### Step 4: Handle PROJECT_STANDARDS.md Duplicates

If the project has a `PROJECT_STANDARDS.md`:

1. **Check if it duplicates RPI-Standards** → Delete (reference central instead)
2. **Check if it has project-specific additions** → Merge into `1-AGENT_BRIEFING.md`

**Correct Pattern** (in Agent Briefing):
```markdown
## 📚 Standards Reference

Universal standards live in `RPI-Standards/` (NOT in this project):

| Document | Purpose |
|----------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Agent team patterns |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | New project checklist |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI Design System |

**Location**: `/Users/joshd.millang/Projects/RPI-Standards/`
**GitHub**: https://github.com/retirementprotectors/RPI-Standards

⚠️ **Do NOT copy standards into project repos** - reference them.
```

### Step 5: Consolidate Plan Files

Plan files (`.plan.md`) belong in `RPI-Standards/Plans/`:

```bash
# Find scattered plan files
find /Users/joshd.millang/Projects -name "*.plan.md" -not -path "*RPI-Standards*"

# Move to central location
mv *.plan.md /Users/joshd.millang/Projects/RPI-Standards/Plans/

# Update PLAN_INDEX.md with new entries
```

### Step 6: Commit Cleanup

```bash
git add -A
git commit -m "docs: cleanup - moved docs to Docs/ folder"
git push origin main
```

---

## Prevention Checklist

Add to your workflow to prevent future accumulation:

### During Development
- [ ] Creating a doc? Put it in `Docs/`, not root
- [ ] Creating a plan? Put it in `RPI-Standards/Plans/`
- [ ] Need a standard? Reference `RPI-Standards/`, don't copy

### During Audits (Monthly)
- [ ] Run `ls *.md` in project root - should be only `README.md`
- [ ] Check `Docs/` for task docs that should be deleted
- [ ] Check Desktop/Trash for orphaned plan files

### After Major Milestones
- [ ] Delete completed `FIX_*.md` and `TEST_*.md` files
- [ ] Archive or delete obsolete plan files
- [ ] Update `0-SESSION_HANDOFF.md` with current state

---

## Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| Agent docs in root | `mv *.AGENT*.md Docs/` |
| PROJECT_STANDARDS.md in project | Delete (reference central) |
| Plan files on Desktop | Move to `RPI-Standards/Plans/` |
| `x` prefixed files mixed with code | Move to `Docs/` (not deprecated, just misplaced) |
| Task docs from old sprints | Delete if completed, move if ongoing |

---

## Integration with Existing Standards

This guide works with:

| Standard | Purpose | When to Use |
|----------|---------|-------------|
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | Prevent mess from day 0 | New projects |
| `+1- EXISTING_PROJECT_STANDARDS_AUDIT.md` | Verify project compliance | Any project, any time |
| `+1- PRODUCTION_LAUNCH_ROLLOUT_KIT.md` | Add user-facing docs | Before production |
| **This Guide** | Clean up accumulated docs | When auditing existing projects |

---

*Documentation is only useful if you can find it. Keep it organized.*
