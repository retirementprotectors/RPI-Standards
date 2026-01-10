# RPI Standards

> **Single Source of Truth** for all RPI project standards, templates, and frameworks.
> 
> **Location**: `/Users/joshd.millang/Projects/_RPI_STANDARDS/`
> **GitHub**: https://github.com/retirementprotectors/RPI-Standards

---

## 📁 Contents

| File | Purpose |
|------|---------|
| `+0- MASTER_AGENT_FRAMEWORK.md` | Universal agent team patterns, parallelization rules, handoff protocols |
| `+0- PROJECT_KICKOFF_TEMPLATE.md` | Checklist and templates for starting any new project |
| `+0- UI_DESIGN_GUIDELINES.md` | RPI Design System - colors, typography, components, forbidden patterns |

---

## 🚀 How to Use

### Starting a New Project

1. **Read** the relevant standards docs here (don't copy them)
2. **Reference** them in your project's `Docs/1-AGENT_BRIEFING.md`:
   ```markdown
   > **Standards Reference**: See `_RPI_STANDARDS/` for universal frameworks
   ```
3. **Create project-specific** scope docs in your project's `Docs/` folder

### Why This Structure?

| Problem | Solution |
|---------|----------|
| Standards scattered across projects | **One folder**, one source of truth |
| Old versions copied to new projects | **Reference, don't copy** |
| Updates don't propagate | **Update here**, all projects benefit |
| Git conflicts with standards | **Separate repo**, independent versioning |

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
