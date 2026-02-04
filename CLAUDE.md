# _RPI_STANDARDS

> **Central Standards Repository for All RPI Projects**

---

## What This Is

This repository contains universal standards, templates, and documentation that apply across ALL RPI projects. It is the single source of truth for how things should be built.

**This is NOT a code project.** It contains documentation only.

---

## Structure

| Folder | Purpose |
|--------|---------|
| `0-Setup/` | Standards for new projects and agents |
| `1-Manage/` | Standards for ongoing maintenance |
| `2-Production/` | Standards for production launches |
| `3-Reference/` | Plans, playbooks, strategic docs |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| `0-Setup/MASTER_AGENT_FRAMEWORK.md` | Agent team patterns and roles |
| `0-Setup/CLAUDE_CODE_EXECUTION.md` | How Claude Code operates |
| `0-Setup/UI_DESIGN_GUIDELINES.md` | UI patterns and colors |
| `0-Setup/PROJECT_KICKOFF_TEMPLATE.md` | New project setup |
| `1-Manage/WEEKLY_HEALTH_CHECK.md` | Weekly maintenance |

---

## Rules for This Repo

1. **Standards go here, not in project repos** - Projects reference this repo
2. **Update when you learn something** - Living documentation
3. **No code files** - Documentation only

---

## Git

```bash
git status && git remote -v
git add -A && git commit -m "docs: [description]"
git push
```

---

*This repo defines the rules. Project CLAUDE.md files enforce them locally.*
