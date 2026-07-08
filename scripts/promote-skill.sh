#!/bin/bash
# promote-skill.sh — Skills Registry promotion gate
#
# A field-authored skill draft → canonical Skills Registry.
# HALTS for SHINOB1 (or lane-owner CXO) sign-off before propagating.
# Auto-propagation of an unvetted field-draft is BLOCKED.
#
# Usage: ./scripts/promote-skill.sh <draft-path>
#
#   <draft-path>  Path to the draft skill directory (must contain SKILL.md)
#
# What this does:
#   1. Requires SKILL.md (the invocable unit). gates.md / surface.html / skill.json
#      are OPTIONAL governance wrappers — present only if the skill wants a surface.
#   2. Validates required metadata from SKILL.md FRONTMATTER (via lib/skill-frontmatter.mjs)
#   3. HALTS — outputs the review checklist for SHINOB1 / lane-owner CXO
#   4. After sign-off (operator types "APPROVED"), copies to canonical dir + propagates
#
# SKILL-FORMAT (OB1-GV2 lock, 2026-07-08): a skill IS a single SKILL.md with rich
# frontmatter (id / owner_warrior / lane / version / hooks_enforcing / mcps_called).
# The runtime only loads SKILL.md; the registry/surface read its frontmatter.
#
# RATIONALE: A skill symlinked into every warrior + every MDJ specialist is
# high-blast-radius — same as a hookify rule. Field-draft → fleet law requires
# owner/CTO precision review. This script IS the gate.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$STANDARDS_ROOT/skills"

DRAFT_PATH="${1:-}"

if [ -z "$DRAFT_PATH" ]; then
  echo "❌ Usage: $0 <draft-path>"
  echo "   Example: $0 /tmp/my-new-skill/"
  exit 1
fi

# Normalize path (remove trailing slash)
DRAFT_PATH="${DRAFT_PATH%/}"

if [ ! -d "$DRAFT_PATH" ]; then
  echo "❌ Draft directory not found: $DRAFT_PATH"
  exit 1
fi

SKILL_NAME="$(basename "$DRAFT_PATH")"

echo "================================================"
echo "Skills Registry — Promotion Gate"
echo "================================================"
echo "Draft:     $DRAFT_PATH"
echo "Skill ID:  $SKILL_NAME"
echo ""

# ---- Step 1: Require SKILL.md (invocable unit); wrappers optional ----
echo "Step 1 — Validating structure (SKILL.md required; wrappers optional)..."

if [ -f "$DRAFT_PATH/SKILL.md" ]; then
  echo "  ✅ SKILL.md"
else
  echo "  ❌ SKILL.md — MISSING (required)"
  echo ""
  echo "❌ BLOCKED: SKILL.md is the invocable unit and must be present."
  exit 1
fi
for optional_file in "gates.md" "surface.html" "skill.json"; do
  if [ -f "$DRAFT_PATH/$optional_file" ]; then
    echo "  ✅ $optional_file (optional wrapper — present)"
  else
    echo "  ·  $optional_file (optional — absent)"
  fi
done
echo ""

# ---- Step 2: Validate required metadata from SKILL.md frontmatter ----
echo "Step 2 — Validating metadata (SKILL.md frontmatter; skill.json fallback)..."

if ! node "$SCRIPT_DIR/lib/skill-frontmatter.mjs" --validate "$DRAFT_PATH"; then
  exit 1
fi

echo ""

# ---- Check if skill already exists ----
CANONICAL_DIR="$SKILLS_DIR/$SKILL_NAME"
if [ -d "$CANONICAL_DIR" ]; then
  echo "⚠️  Skill '$SKILL_NAME' already exists in canonical dir — this is an UPDATE, not a first-promote."
fi

# ---- Step 3: HALT — Output review checklist ----
echo "================================================"
echo "HALT — OWNER / CTO REVIEW REQUIRED"
echo "================================================"
echo ""
echo "A skill symlinked fleet-wide is high-blast-radius — same as a hookify rule."
echo "SHINOB1 (CTO) or the skill's lane-owner CXO must review before propagation."
echo ""
echo "Review checklist:"
echo ""
echo "  □ SKILL.md: steps are accurate, correct, and safe to run fleet-wide"
echo "  □ SKILL.md: no hallucinated tooling, no fabricated process steps"
echo "  □ SKILL.md frontmatter: id matches directory name ($SKILL_NAME)"
echo "  □ SKILL.md frontmatter: owner_warrior is correct"
echo "  □ SKILL.md frontmatter: hooks_enforcing cites real, existing hookify rules"
echo "  □ gates.md (if present): references hookify rules BY NAME only (no duplicated patterns)"
echo "  □ gates.md (if present): referenced rules exist in _RPI_STANDARDS/hookify/"
echo "  □ surface.html (if present): renders correctly; no PHI; no hard-coded data"
echo "  □ No hookify rule PATTERNS duplicated anywhere in this skill's files"
echo "  □ Any NEW hookify rules needed by this skill have gone through the"
echo "    hookify authoring process (SHINOB1 review) separately — NOT authored here"
echo ""
echo "Files to review:"
for f in SKILL.md gates.md surface.html skill.json; do
  [ -f "$DRAFT_PATH/$f" ] && echo "  $DRAFT_PATH/$f"
done
echo ""
echo "If APPROVED, type exactly: APPROVED"
echo "If REJECTED, type anything else (or Ctrl+C to abort)."
echo ""
read -r -p "Decision: " DECISION

if [ "$DECISION" != "APPROVED" ]; then
  echo ""
  echo "❌ Promotion rejected. Skill stays in draft. Fix and re-run."
  exit 1
fi

# ---- Step 4: Copy to canonical dir + propagate ----
echo ""
echo "✅ APPROVED — promoting $SKILL_NAME to canonical Skills Registry..."

if [ -d "$CANONICAL_DIR" ]; then
  echo "  Updating existing canonical entry..."
else
  echo "  Creating new canonical entry..."
  mkdir -p "$CANONICAL_DIR"
fi

cp "$DRAFT_PATH/SKILL.md" "$CANONICAL_DIR/SKILL.md"
for optional_file in "gates.md" "surface.html" "skill.json"; do
  if [ -f "$DRAFT_PATH/$optional_file" ]; then
    cp "$DRAFT_PATH/$optional_file" "$CANONICAL_DIR/$optional_file"
  fi
done
echo "  ✅ Copied to $CANONICAL_DIR"

# Regenerate registry
echo "  Regenerating skills-registry.json..."
node "$SCRIPT_DIR/generate-skills-registry.mjs"

# Propagate symlinks
echo "  Propagating SKILL.md symlinks..."
bash "$SCRIPT_DIR/setup-skills-symlinks.sh"

echo ""
echo "================================================"
echo "Promotion Complete"
echo "================================================"
echo "  Skill:    /$SKILL_NAME"
echo "  Canonical: $CANONICAL_DIR"
echo ""
echo "Next steps:"
echo "  1. git add _RPI_STANDARDS/skills/$SKILL_NAME/"
echo "  2. git add _RPI_STANDARDS/skills-registry.json _RPI_STANDARDS/skills-registry.html"
echo "  3. git commit -m 'ronin(SKILLS-REG-001): promote $SKILL_NAME as Skill #<N>'"
echo "  4. gh pr create + gh pr merge --auto --squash # code-verified: skill structure valid"
echo ""
