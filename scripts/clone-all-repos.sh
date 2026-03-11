#!/bin/bash
# RPI Repository Clone Script
# Clones ALL RPI repos into the correct SuperProject folder structure.
#
# USAGE (new machine):
#   1. mkdir -p ~/Projects && cd ~/Projects
#   2. gh repo clone retirementprotectors/RPI-Standards _RPI_STANDARDS
#   3. ./_RPI_STANDARDS/scripts/clone-all-repos.sh
#   4. ./_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh
#
# WHY THIS EXISTS:
#   GitHub repos are flat — "retirementprotectors/CAM" has no concept of
#   living inside "RAPID_TOOLS/". Without this script, `gh repo clone` puts
#   everything at the top level, creating duplicates outside the SuperProject
#   folders. This script is the canonical mapping from GitHub repo → local path.

set -e

PROJECTS_DIR="${HOME}/Projects"
ORG="retirementprotectors"

# Format: "GITHUB_REPO_NAME:LOCAL_PATH_RELATIVE_TO_PROJECTS"
# The local path includes the SuperProject folder.
REPO_MAP=(
  # toMachina (THE PLATFORM — monorepo)
  "toMachina:toMachina"

  # GAS engines (maintenance mode)
  "RAPID_CORE:gas/RAPID_CORE"
  "RAPID_IMPORT:gas/RAPID_IMPORT"
  "RAPID_COMMS:gas/RAPID_COMMS"
  "RAPID_API:gas/RAPID_API"
  "RPI-Content-Manager:gas/C3"
  "CAM:gas/CAM"
  "DEX:gas/DEX"
  "ATLAS:gas/ATLAS"

  # Standalone services
  "MCP-Hub:services/MCP-Hub"
  "PDF_SERVICE:services/PDF_SERVICE"
  "Marketing-Hub:services/Marketing-Hub"

  # Archive (read-only, tagged pre-migration-archive)
  "ProDashX:archive/PRODASHX"
  "RIIMO:archive/RIIMO"
  "sentinel-v2:archive/sentinel-v2"
  "sentinel:archive/sentinel-v1"
  "DAVID-HUB:archive/DAVID-HUB"
  "CEO-Dashboard:archive/CEO-Dashboard"
  "RPI-Command-Center:archive/RPI-Command-Center"
)

# Name mismatches (for reference):
#   GitHub "RPI-Content-Manager" → local "C3" (renamed locally)
#   GitHub "ProDashX"            → local "PRODASHX" (casing normalized)
#   GitHub "RPI-Standards"       → local "_RPI_STANDARDS" (prefixed for sort)

echo "=== RPI Repository Clone Script ==="
echo "Projects directory: ${PROJECTS_DIR}"
echo ""

# Check prerequisites
if ! command -v gh &> /dev/null; then
  echo "ERROR: GitHub CLI (gh) is required. Install: brew install gh"
  exit 1
fi

if ! gh auth status &> /dev/null 2>&1; then
  echo "ERROR: GitHub CLI not authenticated. Run: gh auth login"
  exit 1
fi

# Create directory structure
echo "Creating directory structure..."
mkdir -p "${PROJECTS_DIR}/gas"
mkdir -p "${PROJECTS_DIR}/services"
mkdir -p "${PROJECTS_DIR}/archive"
echo ""

# Clone each repo
CLONED=0
SKIPPED=0
FAILED=0

for entry in "${REPO_MAP[@]}"; do
  REPO_NAME="${entry%%:*}"
  LOCAL_PATH="${entry##*:}"
  FULL_PATH="${PROJECTS_DIR}/${LOCAL_PATH}"

  if [ -d "${FULL_PATH}" ]; then
    echo "SKIP: ${LOCAL_PATH} (already exists)"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  echo "CLONE: ${ORG}/${REPO_NAME} → ${LOCAL_PATH}"
  if gh repo clone "${ORG}/${REPO_NAME}" "${FULL_PATH}" 2>/dev/null; then
    CLONED=$((CLONED + 1))
  else
    echo "  FAILED: Could not clone ${ORG}/${REPO_NAME}"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "=== Done ==="
echo "Cloned: ${CLONED}"
echo "Skipped: ${SKIPPED} (already existed)"
echo "Failed: ${FAILED}"
echo ""

if [ ${FAILED} -gt 0 ]; then
  echo "WARNING: ${FAILED} repo(s) failed to clone. Check GitHub access."
  exit 1
fi

echo "Next step: ./_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh"
