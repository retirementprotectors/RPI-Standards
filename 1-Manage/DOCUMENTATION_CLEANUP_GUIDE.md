# Documentation Cleanup Guide

> **When to Use**: During project audits or when a project has accumulated scattered docs  
> **Counterpart**: `+0- PROJECT_KICKOFF_TEMPLATE.md` (prevents this from happening)  
> **Version**: v1.1 (January 25, 2026)

---

## The Problem

Projects accumulate documentation debt:
- Task-specific docs created during debugging (`FIX_*.md`, `CHECK_*.md`, `TEST_*.md`)
- Agent scope docs in root instead of `Docs/`
- Plan files scattered across Desktop, project roots, or trash
- **Hidden Cursor plans** in `~/.cursor/plans/` (invisible, not in git)
- Duplicate standards copied into projects instead of referenced

**Root Cause**: The Project Kickoff Template creates `Docs/` but doesn't enforce ongoing organization. Agents create docs where convenient, not where correct. Cursor's default plan location is not configurable.

---

## Standard Project Structure

### What Goes Where

| Location | Content | Examples |
|----------|---------|----------|
| **Project Root** | Code, config, README only | `Code.gs`, `appsscript.json`, `.clasp.json`, `README.md` |
| **`Docs/`** | Agent scope docs, session handoff | `1-AGENT_BRIEFING.md`, `2.x-AGENT_SCOPE_*.md` |
| **`Docs/User/`** | Human-facing guides | `Admin_Guide.html`, `Overview.html` |
| **`Docs/Reference/`** | Strategic/architecture docs | `PROJECT_MASTER.md`, `ARCHITECTURE_VISION.md` |
| **`Docs/Archive/`** | Backup files, old versions | `xCode_v11_BACKUP.gs` |
| **`RPI-Standards/0-Setup/`** | Setup standards (new agents/projects) | `MASTER_AGENT_FRAMEWORK.md`, `PROJECT_KICKOFF_TEMPLATE.md` |
| **`RPI-Standards/1-Manage/`** | Management standards (weekly audits) | `WEEKLY_HEALTH_CHECK.md`, `DOCUMENTATION_CLEANUP_GUIDE.md` |
| **`RPI-Standards/2-Production/`** | Production standards | `PRE_LAUNCH_CHECKLIST.md`, `PRODUCTION_LAUNCH_ROLLOUT_KIT.md` |
| **`RPI-Standards/Plans/`** | All project plans | `*.plan.md` files |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Agent Docs | Numbered prefix | `0-SESSION_HANDOFF.md`, `1-AGENT_BRIEFING.md` |
| Universal Standards | `+0-` or `+1-` prefix | `+0- MASTER_AGENT_FRAMEWORK.md` |
| Task/Debug Docs | `FIX_`, `CHECK_`, `TEST_` prefix | `FIX_VERSION_UNDEFINED.md` |
| Plan Files | `.plan.md` extension | `cam_comp_grid_build.plan.md` |

---

## Full Cleanup Audit Process

### Phase 1: Discovery (Find Everything)

#### Step 1.1: Inventory Project Root Docs

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
ls *.md 2>/dev/null
```

**Goal**: Only `README.md` should be in root.

#### Step 1.2: Find Scattered Plan Files

```bash
# In all Projects
find /Users/joshd.millang/Projects -name "*.plan.md" -not -path "*RPI-Standards*"

# On Desktop
ls ~/Desktop/*.plan.md 2>/dev/null

# In Trash
ls ~/.Trash/*.plan.md 2>/dev/null
```

#### Step 1.3: Check Cursor's Hidden Plans (CRITICAL)

**⚠️ Cursor stores plan files in a hidden location that's NOT in any project!**

```bash
ls ~/.cursor/plans/
```

**Why this matters:**
- Plans created during Cursor sessions go to `~/.cursor/plans/` by default
- These files are **NOT in any git repo** - lost on machine rebuild
- They don't sync between machines
- Valuable work happens here without you realizing it

**Can you change this default?** No. Cursor's plan storage location is hardcoded. There's no setting in:
- `~/Library/Application Support/Cursor/User/settings.json`
- `~/.cursor/` config files

**Workaround Options:**

| Option | Command | Risk |
|--------|---------|------|
| Move after each session | `mv ~/.cursor/plans/*.plan.md RPI-Standards/Plans/` | Easy to forget |
| Symlink the folder | `ln -sf /path/to/RPI-Standards/Plans ~/.cursor/plans` | Might break Cursor |
| Monthly audit | Check as part of cleanup | Reactive, not preventive |

---

### Phase 2: Relocation (Move to Correct Locations)

#### Step 2.1: Move Agent Docs to Docs/

```bash
mkdir -p Docs/

mv 0-SESSION_HANDOFF.md Docs/ 2>/dev/null
mv 1-AGENT_BRIEFING.md Docs/ 2>/dev/null
mv 2.*-AGENT_SCOPE_*.md Docs/ 2>/dev/null
mv 3.*-AGENT_SCOPE_*.md Docs/ 2>/dev/null
```

#### Step 2.2: Move Plan Files to RPI-Standards/Plans/

```bash
# From project roots
mv *.plan.md /Users/joshd.millang/Projects/RPI-Standards/Plans/

# From hidden Cursor location
mv ~/.cursor/plans/*.plan.md /Users/joshd.millang/Projects/RPI-Standards/Plans/

# From Desktop/Trash
mv ~/Desktop/*.plan.md /Users/joshd.millang/Projects/RPI-Standards/Plans/ 2>/dev/null
mv ~/.Trash/*.plan.md /Users/joshd.millang/Projects/RPI-Standards/Plans/ 2>/dev/null
```

#### Step 2.3: Organize Docs/ Subfolders (if needed)

```bash
mkdir -p Docs/Reference Docs/Archive Docs/Revenue

# Move strategic docs
mv Docs/*ARCHITECTURE*.md Docs/Reference/
mv Docs/*MASTER*.md Docs/Reference/

# Move backups
mv Docs/*BACKUP* Docs/Archive/
mv Docs/x*.md Docs/Archive/  # 'x' prefixed files are often backups

# Move revenue docs (if project has them)
mv Docs/REVENUE_*.md Docs/Revenue/
```

---

### Phase 3: Consolidation Review (BEFORE Committing)

**⚠️ STOP HERE. Review what you've collected before finalizing.**

#### Step 3.1: Review Relocated Plan Files

```bash
ls -la /Users/joshd.millang/Projects/RPI-Standards/Plans/*.plan.md
```

**For each plan file, determine:**

| Question | If Yes | If No |
|----------|--------|-------|
| Is this a duplicate of an existing plan? | Delete the older/less complete one | Keep |
| Is this superseded by a more complete plan? | Merge unique content, then delete | Keep |
| Is this a completed/archived plan? | Mark as "Completed" in PLAN_INDEX | Keep |
| Is this actually a task, not a plan? | Delete (it was one-time action) | Keep |

#### Step 3.2: Review Task-Specific Docs

For files like `FIX_*.md`, `CHECK_*.md`, `TEST_*.md`:

| Question | Action |
|----------|--------|
| One-time fix already applied? | **Delete** |
| Recurring process? | **Keep in Docs/** |
| Universal value for all projects? | **Move to RPI-Standards/** |
| Historical reference only? | **Move to Docs/Archive/** |

#### Step 3.3: Check for Duplicate Standards

If project has `PROJECT_STANDARDS.md`:
- Does it duplicate `RPI-Standards/` content? → **Delete**
- Does it have project-specific additions? → **Merge into `1-AGENT_BRIEFING.md`**, then delete

#### Step 3.4: Identify Content for RPI-Standards

Look for docs that should be centralized:

| Content Type | Move To |
|--------------|---------|
| Team playbooks | `RPI-Standards/Playbooks/` |
| Strategic docs | `RPI-Standards/Strategic/` |
| Setup guides | `RPI-Standards/Onboarding/` |
| Project plans | `RPI-Standards/Plans/` |

---

### Phase 4: Update Index Files

#### Step 4.1: Update PLAN_INDEX.md

After adding new plans, update `RPI-Standards/Plans/PLAN_INDEX.md`:

1. Add to **Quick Reference** table
2. Add to appropriate **Category** section
3. Update **Files in This Folder** list
4. Add entry to **Consolidation Log**

**Categories in PLAN_INDEX:**
- Commission Intelligence
- CAM
- DAVID-HUB
- Infrastructure
- Data Analysis

#### Step 4.2: Update Project Agent Briefing (if needed)

If you moved significant docs, update the project's `Docs/1-AGENT_BRIEFING.md` to reflect:
- New Docs/ subfolder structure
- Any docs moved to RPI-Standards (add reference link)

---

### Phase 5: Commit and Push

#### Step 5.1: Commit Project Changes

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git add -A
git commit -m "docs: cleanup - reorganized Docs/ folder structure"
git push origin main
```

#### Step 5.2: Commit RPI-Standards Changes

```bash
cd /Users/joshd.millang/Projects/RPI-Standards
git add -A
git commit -m "docs: add [N] rescued plans, update PLAN_INDEX"
git push origin main
```

---

## Prevention Checklist

### During Development
- [ ] Creating a doc? Put it in `Docs/`, not root
- [ ] Creating a plan? Move it from `~/.cursor/plans/` to `RPI-Standards/Plans/` immediately
- [ ] Need a standard? Reference `RPI-Standards/`, don't copy

### Monthly Audit (Full Process Above)
- [ ] Run Steps 1.1-1.3 (Discovery)
- [ ] Run Steps 2.1-2.3 (Relocation)
- [ ] **Run Step 3 (Consolidation Review)** ← Most important!
- [ ] Run Step 4 (Update Indexes)
- [ ] Run Step 5 (Commit)

### After Major Milestones
- [ ] Delete completed `FIX_*.md` and `TEST_*.md` files
- [ ] Archive or delete obsolete plan files
- [ ] Update `0-SESSION_HANDOFF.md` with current state

---

## Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| Agent docs in root | `mv *AGENT*.md Docs/` |
| PROJECT_STANDARDS.md in project | Delete (reference central) |
| Plan files on Desktop | Move to `RPI-Standards/Plans/` |
| Plans in `~/.cursor/plans/` | Move to `RPI-Standards/Plans/` |
| `x` prefixed files mixed with code | Move to `Docs/Archive/` |
| Task docs from old sprints | Delete if completed, archive if historical |
| Playbooks in project | Move to `RPI-Standards/Playbooks/` |

---

## Integration with Existing Standards

| Standard | Purpose | When to Use |
|----------|---------|-------------|
| `0-Setup/PROJECT_KICKOFF_TEMPLATE.md` | Prevent mess from day 0 | New projects |
| `1-Manage/EXISTING_PROJECT_STANDARDS_AUDIT.md` | Verify project compliance | Any project |
| `1-Manage/WEEKLY_HEALTH_CHECK.md` | Quick weekly verification | Every Monday |
| `2-Production/PRE_LAUNCH_CHECKLIST.md` | Technical pre-launch verification | Before production |
| `2-Production/PRODUCTION_LAUNCH_ROLLOUT_KIT.md` | Add user-facing docs | After production deployment |
| **This Guide** | Clean up accumulated docs + consolidation review | Monthly/as needed |

---

*Documentation is only useful if you can find it. Keep it organized.*
