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
echo "  block-hardcoded-secrets, block-credentials-in-config, block-phi-in-logs,"
echo "  block-anyone-anonymous-access, block-hardcoded-matrix-ids, block-alert-confirm-prompt,"
echo "  block-drive-url-external, block-forui-no-json-serialize, block-hardcoded-colors,"
echo "  block-let-module-caching"
echo "Warn Rules (action: warn):"
echo "  warn-date-return-no-serialize, warn-missing-structured-response,"
echo "  warn-modal-no-flexbox, warn-phi-in-error-message, warn-plain-person-select, warn-inline-pii-data"
echo "Intent Rules (event: prompt):"
echo "  intent-session-start, intent-sendit"
echo "Quality Gates (event: bash):"
echo "  quality-gate-deploy-verify, quality-gate-commit-remind"
echo ""

# All RPI project directories (relative to PROJECTS_ROOT)
PROJECTS=(
  "PRODASHX_TOOLS/PRODASHX"
  "PRODASHX_TOOLS/QUE/QUE-Medicare"
  "RAPID_TOOLS/C3"
  "RAPID_TOOLS/CAM"
  "RAPID_TOOLS/CEO-Dashboard"
  "RAPID_TOOLS/DEX"
  "RAPID_TOOLS/Marketing-Hub"
  "RAPID_TOOLS/MCP-Hub"
  "RAPID_TOOLS/RAPID_API"
  "RAPID_TOOLS/RAPID_COMMS"
  "RAPID_TOOLS/RAPID_CORE"
  "RAPID_TOOLS/RAPID_IMPORT"
  "RAPID_TOOLS/RIIMO"
  "RAPID_TOOLS/RPI-Command-Center"
  "RAPID_TOOLS/PDF_SERVICE"
  "SENTINEL_TOOLS/DAVID-HUB"
  "SENTINEL_TOOLS/sentinel"
  "SENTINEL_TOOLS/sentinel-v2"
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
