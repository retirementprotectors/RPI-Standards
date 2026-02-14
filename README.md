# RPI Standards

> **One file. Every session. All the knowledge.**

---

## New Machine Setup (4 commands)

```bash
mkdir -p ~/Projects && cd ~/Projects
gh repo clone retirementprotectors/RPI-Standards _RPI_STANDARDS
./_RPI_STANDARDS/scripts/clone-all-repos.sh
./_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh
```

This clones all 16 repos into the correct folder structure, symlinks `~/.claude/CLAUDE.md` to this repo, and installs hookify enforcement rules across all projects.

**Then:** Add credentials (OAuth tokens, Slack tokens, API keys) — see `MCP-Hub/docs/credentials.md`.

---

## What Gets Installed

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` → `_RPI_STANDARDS/CLAUDE.md` | **Symlinked.** Auto-injected every session. All RPI standards, GAS gotchas, code rules. |
| `<project>/.claude/hookify.*.local.md` | **Symlinked.** 12 enforcement rules per project (block alert(), block PHI in logs, etc.) |

---

## Structure

```
_RPI_STANDARDS/
├── CLAUDE.md              ← THE master file (symlinked to ~/.claude/CLAUDE.md)
├── hookify/               ← 12 enforcement rules (symlinked into every project)
├── scripts/
│   ├── clone-all-repos.sh          ← Clones all 16 repos with correct folder structure
│   ├── setup-hookify-symlinks.sh   ← Creates all symlinks (CLAUDE.md + hookify rules)
│   └── setup.sh                    ← Legacy installer (use setup-hookify-symlinks.sh instead)
├── settings.json          ← MCP config template (reference only — actual config is ~/.mcp.json)
├── README.md              ← You are here
│
└── reference/             ← Deep-dive docs (read only when needed)
    ├── new-project/       ← Starting new projects
    ├── integrations/      ← GHL, MATRIX config
    ├── compliance/        ← PHI/PII handling, security, HIPAA
    ├── maintenance/       ← Weekly checks, audits
    ├── production/        ← Launch checklists
    ├── strategic/         ← Vision, roadmaps, architecture
    ├── playbooks/         ← Team operations
    └── archive/           ← Legacy docs, historical plans
```

---

## Injected vs Referenced

| Type | What | When |
|------|------|------|
| **Injected** | `CLAUDE.md` content | Every session, automatically |
| **Referenced** | `reference/` docs | Only when task requires, via Read tool |

**Injected** = Claude Code knows it without being told
**Referenced** = Claude Code reads it when needed

---

## Keeping In Sync

```bash
cd ~/Projects/_RPI_STANDARDS
git pull
# Symlinks auto-update — no reinstall needed
```

Only re-run `setup-hookify-symlinks.sh` if new projects are added.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v5.0 | Feb 14, 2026 | Symlink-based setup, hookify enforcement rules, 6-step deploy with VERIFY, bootstrap scripts |
| v4.0 | Feb 4, 2026 | Single CLAUDE.md consolidation. Restructured to reference/ folder. |
| v3.0 | Jan 26, 2026 | Added THREE_PLATFORM_ARCHITECTURE.md |
| v2.0 | Jan 25, 2026 | Reorganized into 0-Setup, 1-Manage, 2-Production folders |

---

*This is the source of truth for Claude Code configuration across all RPI machines.*
