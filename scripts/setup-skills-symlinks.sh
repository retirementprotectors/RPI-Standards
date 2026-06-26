#!/bin/bash
# setup-skills-symlinks.sh — Skills Registry propagation
#
# Mirrors setup-hookify-symlinks.sh exactly, but for Skills:
#   - Symlinks ONLY SKILL.md into each project's .claude/skills/<name>/SKILL.md
#   - Does NOT symlink surface.html, gates.md, or skill.json — those are
#     registry metadata that live in _RPI_STANDARDS/skills/ only.
#
# Claude Code resolves a skill by finding .claude/skills/<name>/SKILL.md
# in the project or in ~/.claude/. That's all it needs to make /name invocable.
#
# Usage: ./scripts/setup-skills-symlinks.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$STANDARDS_ROOT/skills"
PROJECTS_ROOT="$(dirname "$STANDARDS_ROOT")"

echo "================================================"
echo "RPI Skills Registry — Symlink Propagation"
echo "================================================"
echo "Standards root: $STANDARDS_ROOT"
echo "Skills dir:     $SKILLS_DIR"
echo "Projects root:  $PROJECTS_ROOT"
echo ""

# Verify skills dir exists and has at least one skill
if [ ! -d "$SKILLS_DIR" ] || [ -z "$(ls -A "$SKILLS_DIR" 2>/dev/null)" ]; then
  echo "❌ ERROR: No skills found in $SKILLS_DIR"
  exit 1
fi

SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
echo "Found $SKILL_COUNT skill(s):"
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  if [ -f "$skill_dir/SKILL.md" ]; then
    echo "  /$skill_name"
  fi
done
echo ""

# Active projects — mirrors setup-hookify-symlinks.sh project list exactly
PROJECTS=(
  "toMachina"
  "gas/RAPID_CORE"
  "gas/RAPID_IMPORT"
  "gas/DEX"
  "services/MCP-Hub"
  "services/PDF_SERVICE"
  "services/Marketing-Hub"
  "_RPI_STANDARDS"
)

SUCCESS=0
SKIPPED=0

# Step 1: Global ~/.claude/ (always-active regardless of CWD)
echo "Setting up global skills in ~/.claude/..."
GLOBAL_CLAUDE_DIR="$HOME/.claude"
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  skill_md="$skill_dir/SKILL.md"
  if [ -f "$skill_md" ]; then
    target_dir="$GLOBAL_CLAUDE_DIR/skills/$skill_name"
    mkdir -p "$target_dir"
    ln -sf "$skill_md" "$target_dir/SKILL.md"
  fi
done
GLOBAL_SKILL_COUNT=$(find "$GLOBAL_CLAUDE_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
echo "✅ ~/.claude/skills/ ($GLOBAL_SKILL_COUNT skill(s))"
echo ""

# Step 2: Per-project .claude/skills/
echo "Setting up per-project skills..."
for project in "${PROJECTS[@]}"; do
  PROJECT_PATH="$PROJECTS_ROOT/$project"
  PROJECT_NAME=$(basename "$project")

  if [ -d "$PROJECT_PATH" ]; then
    for skill_dir in "$SKILLS_DIR"/*/; do
      skill_name="$(basename "$skill_dir")"
      skill_md="$skill_dir/SKILL.md"
      if [ -f "$skill_md" ]; then
        target_dir="$PROJECT_PATH/.claude/skills/$skill_name"
        mkdir -p "$target_dir"
        # Remove and re-create symlink (idempotent)
        rm -f "$target_dir/SKILL.md"
        ln -sf "$skill_md" "$target_dir/SKILL.md"
      fi
    done
    echo "✅ $PROJECT_NAME"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "⚠️  $PROJECT_NAME (not found - skipped)"
    SKIPPED=$((SKIPPED + 1))
  fi
done

echo ""
echo "================================================"
echo "Propagation Complete"
echo "================================================"
echo "  ✅ Configured: $SUCCESS projects"
echo "  ⚠️  Skipped:    $SKIPPED projects (not found)"
echo ""
echo "Skills are now invocable as /case-drive-checklist etc. in all configured projects."
echo "Run scripts/generate-skills-registry.mjs to regenerate the machine inventory."
echo ""
