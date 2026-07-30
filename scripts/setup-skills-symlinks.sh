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

# ── TRK-HOOK-305a — REFUSE TO RUN FROM A NON-CANONICAL CHECKOUT ──────────────────────
#
# THE HEADER OF THIS FILE SAYS IT "Mirrors setup-hookify-symlinks.sh exactly." IT DID NOT.
# That installer refuses a non-canonical checkout at its lines 44-59. This one had no such
# guard anywhere — no CANONICAL, no REFUSING, no override token. The comment asserted a
# mechanism that was never implemented, and the missing half is the safety half.
#
# WHY IT MATTERS, AND WHY IT IS NOT A MIGRATION ISSUE: STANDARDS_ROOT above is derived from
# wherever this script happens to SIT. Run it out of a worktree and every skill symlink —
# global, and per-project — silently re-points at that worktree. The fleet's entire skill
# set then hangs off a feature branch that is one `git worktree remove` away from vanishing.
#
# THIS EXACT CLASS FIRED ON THIS BOX ON 2026-07-30. The hookify installer was run from
# `_RPI_STANDARDS-ob1-claudemd` and re-pointed 318 rule symlinks at a temporary worktree
# while every instrument reported healthy — the COUNT was identical, so nothing looked
# wrong. `readlink -f` was the only measurement that would have caught it, and nothing was
# looking at it. The hookify side has been guarded since. This side has not been, and it
# can fire tonight, with or without the migration.
#
# THE BLAST RADIUS IS NOT SMALLER HERE, IT IS DIFFERENT. The 10 skills include
# session-start, pre-flight-check, registry-check and atlas-consult — the ones that gate
# OTHER work. A silently-repointed skill does not error; it resolves to a file that may be
# stale or may disappear, and the seat reads the result as doctrine.
#
# Deliberately identical in shape and in override token to setup-hookify-symlinks.sh, so
# the two installers can be read side by side and any future divergence is visible.
CANONICAL_STANDARDS_ROOT="${CANONICAL_STANDARDS_ROOT:-$HOME/Projects/_RPI_STANDARDS}"
if [ "$STANDARDS_ROOT" != "$CANONICAL_STANDARDS_ROOT" ] && [ "${ALLOW_NONCANONICAL_STANDARDS_ROOT:-}" != "yes-i-mean-it" ]; then
  echo "❌ REFUSING: this script is running from a NON-CANONICAL checkout." >&2
  echo "     running from : $STANDARDS_ROOT" >&2
  echo "     canonical    : $CANONICAL_STANDARDS_ROOT" >&2
  echo "" >&2
  echo "   Every skill symlink it creates would point HERE. The fleet's skills would then" >&2
  echo "   live in this checkout, and deleting it would take them down silently — a missing" >&2
  echo "   SKILL.md is simply an uninvocable skill, never an error." >&2
  echo "" >&2
  echo "   Run it from the canonical tree instead:" >&2
  echo "     bash $CANONICAL_STANDARDS_ROOT/scripts/setup-skills-symlinks.sh" >&2
  echo "" >&2
  echo "   Genuinely relocating? ALLOW_NONCANONICAL_STANDARDS_ROOT=yes-i-mean-it" >&2
  exit 1
fi

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
