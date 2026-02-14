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
  # PRODASHX_TOOLS (B2C)
  "ProDash:PRODASHX_TOOLS/PRODASHX"
  "QUE-Medicare:PRODASHX_TOOLS/QUE/QUE-Medicare"

  # RAPID_TOOLS (Shared Services / B2E)
  "RPI-Content-Manager:RAPID_TOOLS/C3"
  "CAM:RAPID_TOOLS/CAM"
  "CEO-Dashboard:RAPID_TOOLS/CEO-Dashboard"
  "DEX:RAPID_TOOLS/DEX"
  "MCP-Hub:RAPID_TOOLS/MCP-Hub"
  "PDF_SERVICE:RAPID_TOOLS/PDF_SERVICE"
  "RAPID_API:RAPID_TOOLS/RAPID_API"
  "RAPID_CORE:RAPID_TOOLS/RAPID_CORE"
  "RAPID_IMPORT:RAPID_TOOLS/RAPID_IMPORT"
  "RIIMO:RAPID_TOOLS/RIIMO"
  "RPI-Command-Center:RAPID_TOOLS/RPI-Command-Center"
  "SPARK_WEBHOOK_PROXY:RAPID_TOOLS/SPARK_WEBHOOK_PROXY"

  # SENTINEL_TOOLS (B2B / DAVID)
  "DAVID-HUB:SENTINEL_TOOLS/DAVID-HUB"
  "sentinel:SENTINEL_TOOLS/sentinel"
  "sentinel-v2:SENTINEL_TOOLS/sentinel-v2"
)

# Name mismatches (for reference):
#   GitHub "RPI-Content-Manager" → local "C3" (renamed locally)
#   GitHub "ProDash"             → local "PRODASHX" (casing normalized + renamed)
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

# Create SuperProject folders
echo "Creating SuperProject folders..."
mkdir -p "${PROJECTS_DIR}/PRODASHX_TOOLS/QUE"
mkdir -p "${PROJECTS_DIR}/RAPID_TOOLS"
mkdir -p "${PROJECTS_DIR}/SENTINEL_TOOLS"
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
