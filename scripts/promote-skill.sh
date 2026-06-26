#!/bin/bash
# promote-skill.sh — Skills Registry promotion gate
#
# A field-authored skill draft → canonical Skills Registry.
# HALTS for SHINOB1 (or lane-owner CXO) sign-off before propagating.
# Auto-propagation of an unvetted field-draft is BLOCKED.
#
# Usage: ./scripts/promote-skill.sh <draft-path>
#
#   <draft-path>  Path to the draft skill directory (must contain all 4 files)
#
# What this does:
#   1. Validates the 4-file structure: SKILL.md, gates.md, surface.html, skill.json
#   2. Validates skill.json schema (required fields)
#   3. HALTS — outputs the review checklist for SHINOB1 / lane-owner CXO
#   4. After sign-off (operator types "APPROVED"), copies to canonical dir + propagates
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

# ---- Step 1: Validate 4-file structure ----
echo "Step 1 — Validating 4-file structure..."
ERRORS=0

for required_file in "SKILL.md" "gates.md" "surface.html" "skill.json"; do
  if [ -f "$DRAFT_PATH/$required_file" ]; then
    echo "  ✅ $required_file"
  else
    echo "  ❌ $required_file — MISSING"
    ((ERRORS++))
  fi
done

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "❌ BLOCKED: $ERRORS required file(s) missing. Fix the draft and retry."
  exit 1
fi
echo ""

# ---- Step 2: Validate skill.json schema ----
echo "Step 2 — Validating skill.json schema..."

SKILL_JSON="$DRAFT_PATH/skill.json"

if ! node -e "JSON.parse(require('fs').readFileSync('$SKILL_JSON','utf8'))" 2>/dev/null; then
  echo "❌ BLOCKED: skill.json is not valid JSON."
  exit 1
fi

# Check required fields via node
node << 'EOF'
const fs = require('fs')
const meta = JSON.parse(fs.readFileSync(process.env.SKILL_JSON_PATH, 'utf8'))
const required = ['id', 'owner_warrior', 'lane', 'version', 'hooks_enforcing', 'mcps_called']
const missing = required.filter(f => !(f in meta))
if (missing.length) {
  console.error('❌ BLOCKED: skill.json missing required fields:', missing.join(', '))
  process.exit(1)
}
if (typeof meta.hooks_enforcing !== 'object' || !Array.isArray(meta.hooks_enforcing)) {
  console.error('❌ BLOCKED: hooks_enforcing must be an array')
  process.exit(1)
}
if (typeof meta.mcps_called !== 'object' || !Array.isArray(meta.mcps_called)) {
  console.error('❌ BLOCKED: mcps_called must be an array')
  process.exit(1)
}
console.log('  ✅ id:', meta.id)
console.log('  ✅ owner_warrior:', meta.owner_warrior)
console.log('  ✅ lane:', meta.lane)
console.log('  ✅ version:', meta.version)
console.log('  ✅ hooks_enforcing:', JSON.stringify(meta.hooks_enforcing))
console.log('  ✅ mcps_called:', JSON.stringify(meta.mcps_called))
EOF
SKILL_JSON_PATH="$SKILL_JSON" node << 'JSEOF'
const fs = require('fs')
const meta = JSON.parse(fs.readFileSync(process.env.SKILL_JSON_PATH, 'utf8'))
const required = ['id', 'owner_warrior', 'lane', 'version', 'hooks_enforcing', 'mcps_called']
const missing = required.filter(f => !(f in meta))
if (missing.length) { console.error('❌ BLOCKED: skill.json missing required fields:', missing.join(', ')); process.exit(1) }
if (!Array.isArray(meta.hooks_enforcing)) { console.error('❌ BLOCKED: hooks_enforcing must be an array'); process.exit(1) }
if (!Array.isArray(meta.mcps_called)) { console.error('❌ BLOCKED: mcps_called must be an array'); process.exit(1) }
console.log('  ✅ Schema valid — id:', meta.id, '| owner:', meta.owner_warrior, '| v' + meta.version)
JSEOF

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
echo "  □ gates.md: references hookify rules BY NAME only (no duplicated patterns)"
echo "  □ gates.md: referenced rules exist in _RPI_STANDARDS/hookify/"
echo "  □ skill.json: id matches directory name ($SKILL_NAME)"
echo "  □ skill.json: owner_warrior is correct"
echo "  □ skill.json: hooks_enforcing cites real, existing hookify rules"
echo "  □ surface.html: renders correctly; no PHI; no hard-coded data"
echo "  □ No hookify rule PATTERNS duplicated anywhere in this skill's files"
echo "  □ Any NEW hookify rules needed by this skill have gone through the"
echo "    hookify authoring process (SHINOB1 review) separately — NOT authored here"
echo ""
echo "Files to review:"
echo "  $DRAFT_PATH/SKILL.md"
echo "  $DRAFT_PATH/gates.md"
echo "  $DRAFT_PATH/surface.html"
echo "  $DRAFT_PATH/skill.json"
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

cp "$DRAFT_PATH/SKILL.md"     "$CANONICAL_DIR/SKILL.md"
cp "$DRAFT_PATH/gates.md"     "$CANONICAL_DIR/gates.md"
cp "$DRAFT_PATH/surface.html" "$CANONICAL_DIR/surface.html"
cp "$DRAFT_PATH/skill.json"   "$CANONICAL_DIR/skill.json"
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
