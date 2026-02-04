# RPI Claude Code Configuration

> **One command. Any computer. Fully configured.**

---

## Quick Setup (Do This)

**Open Terminal. Paste this. Done.**

```bash
mkdir -p ~/.claude && curl -sSL https://raw.githubusercontent.com/retirementprotectors/RPI-Standards/main/claude-config/CLAUDE.md > ~/.claude/CLAUDE.md
```

That's it. Claude Code now has all RPI standards, GAS gotchas, and rules auto-injected every session.

---

## What You Just Installed

| What | Effect |
|------|--------|
| JDM/RPI context | Every agent knows who you are and how you work |
| Golden rules | Complete solutions, act don't ask |
| Code standards | No alert/confirm/prompt, structured responses |
| **ALL GAS gotchas** | Date serialization, JSON roundtrip, base64, etc. |
| Deployment rules | 5-step deploy, commit+deploy together |
| New project setup | Points to kickoff template |

---

## Full Setup (Optional)

If you want pre-approved permissions + MCP servers (Slack, Gmail, etc.):

```bash
# Clone the repo
cd ~/Projects
git clone https://github.com/retirementprotectors/RPI-Standards.git _RPI_STANDARDS

# Run full setup
cd _RPI_STANDARDS/claude-config
./setup.sh

# Add your Slack tokens
nano ~/.claude/settings.json
```

---

## What's In This Folder

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Global context (the important one) |
| `settings.template.json` | Permissions + MCP config template |
| `setup.sh` | Full installation script |

---

*Quick setup = 1 command. Full setup = 3 commands + tokens.*

---

## What Gets Installed

### CLAUDE.md (Auto-Injected Every Session)
- JDM/RPI context
- Golden rules (complete solutions, act don't ask)
- Code standards (no alert/confirm/prompt)
- **ALL GAS gotchas** (Date serialization, JSON roundtrip, etc.)
- Deployment rules (5-step deploy)
- New project setup reference

### settings.json
- Pre-approved permissions (Read, Edit, Write, Bash, etc.)
- MCP server configurations (Slack, Gmail, Drive, etc.)
- Ctrl+Enter for newlines enabled

---

## Keeping In Sync

When CLAUDE.md or settings.json are updated:

```bash
# Pull latest standards
cd ~/Projects/_RPI_STANDARDS
git pull

# Re-run setup (backs up existing, installs new)
cd claude-config
./setup.sh
```

---

## Files Location

After setup, files live at:
```
~/.claude/
├── CLAUDE.md      # Global context
└── settings.json  # Permissions + config
```

---

*This is the source of truth for Claude Code configuration across all RPI machines.*
