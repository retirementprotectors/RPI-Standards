# RPI Claude Code Configuration

> **One-command setup for any new machine.**

---

## What's Here

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Global context injected into every Claude Code session |
| `settings.template.json` | Permissions, MCP servers (with placeholder tokens) |
| `setup.sh` | Installation script |

---

## New Machine Setup

```bash
# 1. Clone _RPI_STANDARDS (if not already)
cd ~/Projects
git clone https://github.com/retirementprotectors/RPI-Standards.git _RPI_STANDARDS

# 2. Run setup
cd _RPI_STANDARDS/claude-config
chmod +x setup.sh
./setup.sh
```

That's it. Claude Code is now configured with all RPI standards.

### After Setup: Add Your Secrets

The setup script installs a template. You need to add your actual tokens:

```bash
# Edit settings.json
nano ~/.claude/settings.json

# Add your Slack tokens:
# - SLACK_BOT_TOKEN: xoxb-...
# - SLACK_USER_TOKEN: xoxp-...
# - SLACK_TEAM_ID: T...
```

Get tokens from: https://api.slack.com/apps (or ask JDM for RPI workspace tokens)

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
