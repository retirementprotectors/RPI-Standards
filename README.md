# RPI Standards

> **One file. Every session. All the knowledge.**

---

## Quick Install (Any Machine)

```bash
mkdir -p ~/.claude && curl -sSL https://raw.githubusercontent.com/retirementprotectors/RPI-Standards/main/CLAUDE.md > ~/.claude/CLAUDE.md
```

---

## Full Install (With Permissions + MCP)

```bash
cd ~/Projects
git clone https://github.com/retirementprotectors/RPI-Standards.git _RPI_STANDARDS
cd _RPI_STANDARDS
./setup.sh

# Then add your tokens
nano ~/.claude/settings.json
```

---

## What Gets Installed

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | **Auto-injected every session** - All RPI standards, GAS gotchas, code rules |
| `~/.claude/settings.json` | Permissions + MCP server configs (Slack, Gmail, Drive, etc.) |

---

## Structure

```
_RPI_STANDARDS/
├── CLAUDE.md           ← THE master file (source for ~/.claude/CLAUDE.md)
├── settings.json       ← Permissions + MCP config template
├── setup.sh            ← Installer script
├── README.md           ← You are here
│
└── reference/          ← Deep-dive docs (read only when needed)
    ├── new-project/    ← Starting new projects
    ├── integrations/   ← GHL, MATRIX config
    ├── compliance/     ← PHI/PII handling
    ├── maintenance/    ← Weekly checks, audits
    ├── production/     ← Launch checklists
    ├── strategic/      ← Vision, roadmaps
    ├── playbooks/      ← Team operations
    └── archive/        ← Legacy docs, historical plans
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
./setup.sh
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v4.0 | Feb 4, 2026 | **MAJOR CONSOLIDATION**: Single CLAUDE.md with all standards baked in. Restructured to reference/ folder. Eliminated 0-Setup, 1-Manage, 2-Production folders. |
| v3.0 | Jan 26, 2026 | Added THREE_PLATFORM_ARCHITECTURE.md |
| v2.0 | Jan 25, 2026 | Reorganized into 0-Setup, 1-Manage, 2-Production folders |

---

*This is the source of truth for Claude Code configuration across all RPI machines.*
