#!/bin/bash
# RPI Development Machine Setup Script
# Run this on a new development machine after cloning _RPI_STANDARDS
#
# Usage: ./scripts/setup-hookify-symlinks.sh
#
# This script:
# 1. Symlinks ~/.claude/CLAUDE.md to _RPI_STANDARDS/CLAUDE.md (global standards)
# 2. Creates symlinks from each RPI project's .claude/ directory
#    to the master hookify rules in _RPI_STANDARDS/hookify/

set -e

# Determine the script's directory and _RPI_STANDARDS root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKIFY_DIR="$STANDARDS_ROOT/hookify"
PROJECTS_ROOT="$(dirname "$STANDARDS_ROOT")"

echo "================================================"
echo "RPI Development Machine Setup"
echo "================================================"
echo "Standards root: $STANDARDS_ROOT"
echo "Hookify rules:  $HOOKIFY_DIR"
echo "Projects root:  $PROJECTS_ROOT"
echo ""

# ============================================
# Step 1: Global CLAUDE.md Symlink
# ============================================
echo "Setting up global CLAUDE.md..."

GLOBAL_CLAUDE_DIR="$HOME/.claude"
GLOBAL_CLAUDE_FILE="$GLOBAL_CLAUDE_DIR/CLAUDE.md"
MASTER_CLAUDE_FILE="$STANDARDS_ROOT/CLAUDE.md"

# Create ~/.claude directory and hooks subdirectory if they don't exist
mkdir -p "$GLOBAL_CLAUDE_DIR"
mkdir -p "$GLOBAL_CLAUDE_DIR/hooks"

# Make all hook scripts executable
if ls "$GLOBAL_CLAUDE_DIR/hooks/"*.sh 1>/dev/null 2>&1; then
  chmod +x "$GLOBAL_CLAUDE_DIR/hooks/"*.sh
  echo "✅ Hook scripts made executable"
fi

# Check if master CLAUDE.md exists
if [ ! -f "$MASTER_CLAUDE_FILE" ]; then
  echo "❌ ERROR: Master CLAUDE.md not found at $MASTER_CLAUDE_FILE"
  exit 1
fi

# Remove existing CLAUDE.md (file or symlink) and create symlink
if [ -L "$GLOBAL_CLAUDE_FILE" ]; then
  rm "$GLOBAL_CLAUDE_FILE"
elif [ -f "$GLOBAL_CLAUDE_FILE" ]; then
  echo "   Backing up existing CLAUDE.md to CLAUDE.md.backup"
  mv "$GLOBAL_CLAUDE_FILE" "$GLOBAL_CLAUDE_FILE.backup"
fi

ln -s "$MASTER_CLAUDE_FILE" "$GLOBAL_CLAUDE_FILE"
echo "✅ Global CLAUDE.md linked to $MASTER_CLAUDE_FILE"
echo ""

# ============================================
# Step 2: Hookify Rules Symlinks
# ============================================
echo "Setting up hookify rules..."

# Verify hookify rules exist
if [ ! -d "$HOOKIFY_DIR" ] || [ -z "$(ls -A $HOOKIFY_DIR/*.local.md 2>/dev/null)" ]; then
  echo "❌ ERROR: No hookify rules found in $HOOKIFY_DIR"
  exit 1
fi

RULE_COUNT=$(ls -1 "$HOOKIFY_DIR"/*.local.md 2>/dev/null | wc -l | tr -d ' ')
echo "Found $RULE_COUNT hookify rules"
echo ""
echo "Block Rules (action: block):"
echo "  block-hardcoded-secrets, block-credentials-in-config, block-phi-in-logs"
echo "Warn Rules (action: warn):"
echo "  warn-phi-in-error-message, warn-inline-pii-data"
echo "Intent Rules (event: prompt):"
echo "  intent-session-start, intent-immune-system-check,"
echo "  intent-plan-mode, intent-execute-plan, intent-atlas-consult"
echo "Quality Gates (event: bash/prompt):"
echo "  quality-gate-plan-format, quality-gate-phase-complete, quality-gate-audit-verify"
echo ""

# All RPI project directories (relative to PROJECTS_ROOT)
# Updated for post-toMachina directory structure
PROJECTS=(
  # toMachina monorepo (THE platform)
  "toMachina"
  # GAS engines (maintenance mode — only 3 remain)
  "gas/RAPID_CORE"
  "gas/RAPID_IMPORT"
  "gas/DEX"
  # Standalone services
  "services/MCP-Hub"
  "services/PDF_SERVICE"
  "services/Marketing-Hub"
  # Standards
  "_RPI_STANDARDS"
)

SUCCESS=0
SKIPPED=0

# Step 2a: Global ~/.claude/ hookify rules (always active regardless of CWD)
echo "Setting up global hookify rules in ~/.claude/..."
for rule in "$HOOKIFY_DIR"/hookify.*.local.md; do
  if [ -f "$rule" ]; then
    ln -sf "$rule" "$GLOBAL_CLAUDE_DIR/"
  fi
done
GLOBAL_RULE_COUNT=$(ls -1 "$GLOBAL_CLAUDE_DIR"/hookify.*.local.md 2>/dev/null | wc -l | tr -d ' ')
echo "✅ ~/.claude/ ($GLOBAL_RULE_COUNT global rules)"
echo ""

# Step 2b: Per-project .claude/ hookify rules
echo "Setting up per-project hookify rules..."
for project in "${PROJECTS[@]}"; do
  PROJECT_PATH="$PROJECTS_ROOT/$project"
  PROJECT_NAME=$(basename "$project")

  if [ -d "$PROJECT_PATH" ]; then
    # Remove existing .claude directory if it exists
    rm -rf "$PROJECT_PATH/.claude"

    # Create fresh .claude directory
    mkdir -p "$PROJECT_PATH/.claude"

    # Create symlinks for each hookify rule
    for rule in "$HOOKIFY_DIR"/hookify.*.local.md; do
      if [ -f "$rule" ]; then
        ln -sf "$rule" "$PROJECT_PATH/.claude/"
      fi
    done

    echo "✅ $PROJECT_NAME"
    ((SUCCESS++))
  else
    echo "⚠️  $PROJECT_NAME (not found - skipped)"
    ((SKIPPED++))
  fi
done

echo ""
echo "================================================"
echo "Setup Complete"
echo "================================================"
echo ""
echo "Global Standards:"
echo "  ✅ ~/.claude/CLAUDE.md → $MASTER_CLAUDE_FILE"
echo ""
echo "Hookify Rules:"
echo "  ✅ Configured: $SUCCESS projects"
echo "  ⚠️  Skipped:    $SKIPPED projects (not found)"
echo ""
echo "All RPI standards and enforcement rules are now active."
echo ""

# ============================================
# Step 3: Shell Extensions (tab titles, etc.)
# ============================================
echo "Setting up shell extensions..."
SHELL_SCRIPT="$STANDARDS_ROOT/scripts/shell-tab-title.sh"
SOURCE_LINE='[ -f "$HOME/Projects/_RPI_STANDARDS/scripts/shell-tab-title.sh" ] && source "$HOME/Projects/_RPI_STANDARDS/scripts/shell-tab-title.sh"'

if [ -f "$SHELL_SCRIPT" ]; then
  if grep -qF "shell-tab-title.sh" "$HOME/.zshrc" 2>/dev/null; then
    echo "✅ Shell tab titles already in ~/.zshrc"
  else
    echo "" >> "$HOME/.zshrc"
    echo "# RPI shell extensions (tab titles, etc.) — managed in _RPI_STANDARDS repo" >> "$HOME/.zshrc"
    echo "$SOURCE_LINE" >> "$HOME/.zshrc"
    echo "✅ Shell tab titles added to ~/.zshrc"
  fi
else
  echo "⚠️  shell-tab-title.sh not found — skipped"
fi
echo ""

echo "To edit:"
echo "  - Standards: $MASTER_CLAUDE_FILE"
echo "  - Rules:     $HOOKIFY_DIR/"
echo ""
echo "================================================"
echo "⚠️  Manual Step Required: API Keys"
echo "================================================"
echo ""
echo "For MCP-Hub and other Node.js tools, add to ~/.zshrc:"
echo ""
echo "  export ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "Get key from: https://console.anthropic.com/settings/keys"
echo "Or from GAS Script Properties (CEO-Dashboard)"
echo ""
