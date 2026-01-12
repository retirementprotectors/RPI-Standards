# RPI Standards

> **Single Source of Truth** for all RPI project standards, templates, and frameworks.
> 
> **Location**: `/Users/joshd.millang/Projects/RPI-Standards/`  
> **GitHub**: https://github.com/retirementprotectors/RPI-Standards

---

## 📁 Contents

### `+0-` Core Standards (Always Read)

| File | Purpose |
|------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Universal agent team patterns, parallelization rules, handoff protocols |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | Checklist and templates for starting **NEW** projects |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI Design System - colors, typography, components, forbidden patterns |

### `+1-` Task Templates (Use as Needed)

| File | Purpose |
|------|---------|
| `+1- EXISTING_PROJECT_STANDARDS_AUDIT.md` | Verify/fix **EXISTING** projects against all standards |

### Naming Convention

| Prefix | Meaning |
|--------|---------|
| `+0-` | Core standards — the rules |
| `+1-` | Task templates — how to apply the rules |

---

## 🔀 Kickoff vs Audit

```
+0- PROJECT_KICKOFF_TEMPLATE    →    For NEW projects (do it right from the start)
           ↕ mirrors ↕
+1- EXISTING_PROJECT_AUDIT      →    For EXISTING projects (verify/fix retroactively)
```

**Both check the same things** — one guides you through setup, the other audits what already exists.

---

## 🔄 Two Workflows

### Workflow A: Project Setup (Starting New)

```
READ standards → CREATE project → CREATE project-specific docs → REFERENCE standards
```

1. **Read** the standards in this folder
2. AI creates project folder, GAS project, GitHub repo
3. AI creates project-specific `Docs/` that **reference** (not copy) standards
4. **JDM does first-time GAS auth** via Editor UI (one-time manual step)
5. AI deploys and continues

### Workflow B: Development (Learning Something New)

```
Working on project → Hit a gotcha → UPDATE standards → PUSH → Continue project
```

**"Shit, we forgot that. Document. Keep moving."**

```bash
# During any project, when you learn something universal:
cd /Users/joshd.millang/Projects/_RPI_STANDARDS
git add -A && git commit -m "docs: [what you learned]" && git push
cd /Users/joshd.millang/Projects/[PROJECT_NAME]  # Continue working
```

---

## 🚀 Why This Structure?

| Problem | Solution |
|---------|----------|
| Standards scattered | **One folder**: `_RPI_STANDARDS/` |
| Old versions in new projects | **Reference, don't copy** |
| Updates don't propagate | **Update once**, all projects benefit |
| Git conflicts | **Separate repo**, independent versioning |
| "Forgot to document that" | **Living Documentation Protocol** |

---

## 📝 Living Documentation Protocol

**"Shit, we forgot that. Document. Keep moving."**

When you learn something that should be universal:

1. Update the relevant file in THIS repo
2. `git add -A && git commit -m "docs: [what you learned]" && git push`
3. Continue with your project work

---

## 🔗 Referencing from Projects

In each project's `Docs/1-AGENT_BRIEFING.md`, add:

```markdown
## Standards Reference

Universal standards live in `_RPI_STANDARDS/` (not in this project):
- Agent Framework: `+0- MASTER_AGENT_FRAMEWORK.md`
- Kickoff Template: `+0- PROJECT_KICKOFF_TEMPLATE.md`  
- UI Guidelines: `+0- UI_DESIGN_GUIDELINES.md`

GitHub: https://github.com/retirementprotectors/RPI-Standards
```

---

## ⚠️ DO NOT

- ❌ Copy these files into project repos
- ❌ Create project-specific versions of universal standards
- ❌ Forget to push updates here after learning something new

## ✅ DO

- ✅ Reference these docs from project briefings
- ✅ Update these docs when you learn something universal
- ✅ Keep project-specific scope docs in project's `Docs/` folder
