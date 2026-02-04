#!/bin/bash
# RPI Claude Code Setup Script
# Run this on any new machine to configure Claude Code with RPI standards

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== RPI Claude Code Setup ==="
echo ""

# Create ~/.claude if it doesn't exist
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Creating $CLAUDE_DIR..."
    mkdir -p "$CLAUDE_DIR"
fi

# Backup existing files if they exist
if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
    echo "Backing up existing CLAUDE.md..."
    mv "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d)"
fi

if [ -f "$CLAUDE_DIR/settings.json" ]; then
    echo "Backing up existing settings.json..."
    mv "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.backup.$(date +%Y%m%d)"
fi

# Copy CLAUDE.md
echo "Installing CLAUDE.md..."
cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/"

# Copy settings template
echo "Installing settings.json from template..."
cp "$SCRIPT_DIR/settings.template.json" "$CLAUDE_DIR/settings.json"

# Update username in paths
CURRENT_USER=$(whoami)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/YOUR_USERNAME/$CURRENT_USER/g" "$CLAUDE_DIR/settings.json"
else
    sed -i "s/YOUR_USERNAME/$CURRENT_USER/g" "$CLAUDE_DIR/settings.json"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Installed to: $CLAUDE_DIR"
echo "  - CLAUDE.md (global context + GAS gotchas)"
echo "  - settings.json (permissions + MCP config template)"
echo ""
echo "⚠️  NEXT STEPS:"
echo "  1. Edit ~/.claude/settings.json"
echo "  2. Add your Slack tokens (SLACK_BOT_TOKEN, SLACK_USER_TOKEN, SLACK_TEAM_ID)"
echo "  3. Verify MCP credential paths are correct"
echo ""
echo "Claude Code is now configured with RPI standards."
echo ""
