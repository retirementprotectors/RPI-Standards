#!/bin/bash
# RPI Hookify Setup Script
# Run this on a new development machine after cloning _RPI_STANDARDS
#
# Usage: ./scripts/setup-hookify-symlinks.sh
#
# This creates symlinks from each RPI project's .claude/ directory
# to the master hookify rules in _RPI_STANDARDS/hookify/

set -e

# Determine the script's directory and _RPI_STANDARDS root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKIFY_DIR="$STANDARDS_ROOT/hookify"
PROJECTS_ROOT="$(dirname "$STANDARDS_ROOT")"

echo "================================================"
echo "RPI Hookify Symlink Setup"
echo "================================================"
echo "Standards root: $STANDARDS_ROOT"
echo "Hookify rules:  $HOOKIFY_DIR"
echo "Projects root:  $PROJECTS_ROOT"
echo ""

# Verify hookify rules exist
if [ ! -d "$HOOKIFY_DIR" ] || [ -z "$(ls -A $HOOKIFY_DIR/*.local.md 2>/dev/null)" ]; then
  echo "❌ ERROR: No hookify rules found in $HOOKIFY_DIR"
  exit 1
fi

RULE_COUNT=$(ls -1 "$HOOKIFY_DIR"/*.local.md 2>/dev/null | wc -l | tr -d ' ')
echo "Found $RULE_COUNT hookify rules"
echo ""

# All RPI project directories (relative to PROJECTS_ROOT)
PROJECTS=(
  "PRODASH_TOOLS/PRODASH"
  "PRODASH_TOOLS/QUE/QUE-Medicare"
  "RAPID_TOOLS/C3"
  "RAPID_TOOLS/CAM"
  "RAPID_TOOLS/CEO-Dashboard"
  "RAPID_TOOLS/DEX"
  "RAPID_TOOLS/MCP-Hub"
  "RAPID_TOOLS/RAPID_API"
  "RAPID_TOOLS/RAPID_CORE"
  "RAPID_TOOLS/RAPID_IMPORT"
  "RAPID_TOOLS/RIIMO"
  "RAPID_TOOLS/RPI-Command-Center"
  "RAPID_TOOLS/TOMIS"
  "SENTINEL_TOOLS/DAVID-HUB"
  "SENTINEL_TOOLS/sentinel"
  "SENTINEL_TOOLS/sentinel-v2"
  "_RPI_STANDARDS"
)

SUCCESS=0
SKIPPED=0

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
echo "✅ Configured: $SUCCESS projects"
echo "⚠️  Skipped:    $SKIPPED projects (not found)"
echo ""
echo "Hookify rules are now active in all configured projects."
echo "Edit rules in: $HOOKIFY_DIR"
echo ""
