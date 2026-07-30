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
PROJECTS_ROOT="$(dirname "$STANDARDS_ROOT")"

# ── TRK-HOOK-306 · THE RULE SOURCE IS RESOLVED, NOT DERIVED FROM WHERE THIS FILE SITS ──
#
# THIS LINE USED TO READ:  HOOKIFY_DIR="$STANDARDS_ROOT/hookify"
#
# It caused a live incident during the TRK-HOOK-303 cutover on 2026-07-30. standards-mirror-sync
# (a 10-minute timer) calls this script at :96. It fired at 23:41:15, 22 SECONDS before the
# migration's repoint finished, and re-armed all four repos in the PROJECTS array below against
# the OLD root — because STANDARDS_ROOT is _RPI_STANDARDS, whatever the fleet's canonical root
# has since become. The migration's own gate then reported 4 trees / 424 links still on the
# retired root, and the cause was this line, on a timer, racing the migration.
#
# An installer that derives the SOURCE OF TRUTH from its own location cannot be moved. It will
# keep arming the fleet at wherever it happens to live, forever, and it will do so silently:
# every link it writes is valid, every count it prints is right, and the target is wrong.
#
# MIRRORED — dojo-warriors/scripts/hookify-canonical-root.sh holds the same candidate order and
# the same non-emptiness test. Change both halves or neither. Sourced when reachable so there is
# one definition; the inline fallback exists only because this script must still run on a box
# where dojo-warriors has not been cloned.
_CANON_HELPER="$HOME/Projects/dojo-warriors/scripts/hookify-canonical-root.sh"
if [ -r "$_CANON_HELPER" ]; then
  # shellcheck source=/dev/null
  . "$_CANON_HELPER"
else
  HOOKIFY_CANON_CANDIDATES=("$HOME/Projects/dojo-warriors/hookify" "$HOME/Projects/_RPI_STANDARDS/hookify")
  hookify_canonical_root() {
    if [ -n "${HOOKIFY_CANON_DIR:-}" ]; then
      [ -d "$HOOKIFY_CANON_DIR" ] && compgen -G "$HOOKIFY_CANON_DIR/hookify.*.local.md" >/dev/null 2>&1 \
        && { printf '%s\n' "$HOOKIFY_CANON_DIR"; return 0; }
      return 1
    fi
    local c
    for c in "${HOOKIFY_CANON_CANDIDATES[@]}"; do
      [ -d "$c" ] && compgen -G "$c/hookify.*.local.md" >/dev/null 2>&1 && { printf '%s\n' "$c"; return 0; }
    done
    return 1
  }
fi

if ! HOOKIFY_DIR="$(hookify_canonical_root)"; then
  echo "❌ REFUSING: no canonical hookify root resolved." >&2
  echo "   Checked: ${HOOKIFY_CANON_CANDIDATES[*]:-<helper-defined>}" >&2
  echo "   A candidate must CONTAIN hookify.*.local.md, not merely exist — pointing the fleet" >&2
  echo "   at an empty directory is not a partial install, it is silent total disarm." >&2
  exit 1
fi

# ── OB1-INSTALLER-CANONICAL-GUARD-001 — REFUSE TO RUN FROM A NON-CANONICAL CHECKOUT ──
#
# STANDARDS_ROOT is derived from wherever this script happens to SIT. That means running it
# out of a worktree silently re-points EVERY symlink — global, and per-project — at that
# worktree. The fleet's entire immune system then hangs off a feature branch that is one
# `git worktree remove` away from vanishing, and it vanishes SILENTLY: the dispatcher globs
# a directory, and a missing directory yields an empty rule list, not an error.
#
# THIS IS NOT HYPOTHETICAL. I did it today, 2026-07-30, while testing the installer fix from
# `_RPI_STANDARDS-ob1-claudemd`. 318 symlinks — 106 global, 106 in dojo-warriors, 106 in
# toMachina — all silently re-pointed at a temporary worktree. Nothing warned. The run
# printed the same success it always prints, and the rule COUNT was identical, so every
# instrument I had said 106/106 healthy while the source of truth was a branch checkout.
#
# The count was the wrong measurement. `readlink -f` was the right one, and nothing was
# looking at it. That is the whole lesson: a symlink farm can be complete and still wrong,
# and only its TARGET discriminates.
#
# PROJECTS_ROOT is why it stayed quiet — a worktree at ~/Projects/_RPI_STANDARDS-<x> has the
# same parent as the canonical tree, so the project list still resolved and every repo got
# its 106. Everything downstream looked correct.
#
# Override exists for a genuine relocation, and it is deliberately ugly to type so it cannot
# be reached for casually.
CANONICAL_STANDARDS_ROOT="${CANONICAL_STANDARDS_ROOT:-$HOME/Projects/_RPI_STANDARDS}"
if [ "$STANDARDS_ROOT" != "$CANONICAL_STANDARDS_ROOT" ] && [ "${ALLOW_NONCANONICAL_STANDARDS_ROOT:-}" != "yes-i-mean-it" ]; then
  echo "❌ REFUSING: this script is running from a NON-CANONICAL checkout." >&2
  echo "     running from : $STANDARDS_ROOT" >&2
  echo "     canonical    : $CANONICAL_STANDARDS_ROOT" >&2
  echo "" >&2
  echo "   Every symlink it creates would point HERE. The fleet's rules would then live in" >&2
  echo "   this checkout, and deleting it would take the whole immune system down silently" >&2
  echo "   — an empty rule directory reads as 'no rules matched', never as an error." >&2
  echo "" >&2
  echo "   Run it from the canonical tree instead:" >&2
  echo "     bash $CANONICAL_STANDARDS_ROOT/scripts/setup-hookify-symlinks.sh" >&2
  echo "" >&2
  echo "   Genuinely relocating? ALLOW_NONCANONICAL_STANDARDS_ROOT=yes-i-mean-it" >&2
  exit 1
fi

echo "================================================"
echo "RPI Development Machine Setup"
echo "================================================"
echo "Standards root: $STANDARDS_ROOT"
echo "Hookify rules:  $HOOKIFY_DIR"
echo "Projects root:  $PROJECTS_ROOT"
echo ""

# ============================================
# Step 1: Directories + hook script permissions
# ============================================
# OB1-HOOKIFY-INSTALLER-FIX-001 — THE GLOBAL CLAUDE.md SYMLINK STEP IS GONE ON PURPOSE.
#
# WHAT THIS STEP USED TO DO, AND WHY IT IS A DEFECT NOW: it linked ~/.claude/CLAUDE.md ->
# _RPI_STANDARDS/CLAUDE.md, and it HARD-EXITED (line 48-51, under `set -e`) if that master
# file was missing. OB1-CLAUDEMD-ROOT-DELETE-001 deleted that master file the same day — the
# retired stub was auto-injecting into every seat and there is no read-block that can stop a
# CLAUDE.md from loading, so deleting it was the only mechanism.
#
# THE CONSEQUENCE WAS IMMEDIATE AND SILENT-ISH: the installer began exiting 1 at the gate,
# BEFORE Step 2 — which is where all 106 hookify rules get symlinked. So from the moment the
# stub was deleted:
#   - a warrior who edits a rule and runs the prescribed refresh (this script, named in
#     hookify.block-hookify-rule-write-outside-canonical) gets a failure having installed nothing
#   - a rebuilt box never installs the immune system at all
# The script printed an error, so it was not silent — but it was pointing at a file whose
# absence is CORRECT, which reads as a broken environment rather than a stale installer.
#
# ⚠️ REMOVING ONLY THE GATE WOULD HAVE BEEN WORSE THAN LEAVING IT BROKEN. The `ln -s` two
# lines below the gate would then RE-CREATE ~/.claude/CLAUDE.md pointing at a deleted path,
# and the next run of the fleet-wide installer would resurrect the exact global injection we
# spent today removing — as a dangling symlink, no less. The whole step goes, not the check.
#
# Kept from the old Step 1: the mkdir and the chmod. Those are still load-bearing.
echo "Preparing ~/.claude ..."

GLOBAL_CLAUDE_DIR="$HOME/.claude"

# Create ~/.claude directory and hooks subdirectory if they don't exist
mkdir -p "$GLOBAL_CLAUDE_DIR"
mkdir -p "$GLOBAL_CLAUDE_DIR/hooks"

# Make all hook scripts executable
if ls "$GLOBAL_CLAUDE_DIR/hooks/"*.sh 1>/dev/null 2>&1; then
  chmod +x "$GLOBAL_CLAUDE_DIR/hooks/"*.sh
  echo "✅ Hook scripts made executable"
fi

# A leftover ~/.claude/CLAUDE.md from a pre-deletion box would still auto-inject. Retire it
# rather than leaving it: renamed, never deleted, so an operator can see what was there.
if [ -L "$GLOBAL_CLAUDE_DIR/CLAUDE.md" ] || [ -f "$GLOBAL_CLAUDE_DIR/CLAUDE.md" ]; then
  mv "$GLOBAL_CLAUDE_DIR/CLAUDE.md" "$GLOBAL_CLAUDE_DIR/CLAUDE.md.retired-$(date +%Y%m%d%H%M%S)"
  echo "⚠️  Retired a leftover ~/.claude/CLAUDE.md (it would have auto-injected into every seat)"
fi
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
#
# OB1-HOOKIFY-INSTALLER-FIX-001 — THE LIST WAS PROTECTING GHOSTS AND SKIPPING THE WARRIORS.
#
# JDM, 2026-07-30: "Isn't dojo-warriors the one that should literally have ALL OF THEM?!
# toMachina doesn't WRITE ITSELF, the Warriors do!" He is right, and the list proves it:
#
#   MEASURED 2026-07-30, every entry as it stood:
#     toMachina            EXISTS   106 rules linked
#     gas/RAPID_CORE       GONE
#     gas/RAPID_IMPORT     GONE
#     gas/DEX              GONE
#     services/MCP-Hub     EXISTS
#     services/PDF_SERVICE GONE
#     services/Marketing-Hub GONE
#     _RPI_STANDARDS       EXISTS
#     dojo-warriors        EXISTS — AND WAS NEVER ON THE LIST.  0 rules linked.
#
# FIVE OF SEVEN ENTRIES POINTED AT DIRECTORIES THAT NO LONGER EXIST, and the one repo where
# all nine warriors actually live and work was absent. The comment above this list said
# "updated for post-toMachina directory structure" — it was written before dojo-warriors was
# the warriors' home and never revisited.
#
# WHY THE GAP WAS INVISIBLE: rules load from a path RELATIVE to the session's working
# directory. A warrior launched into dojo-warriors got the prompt/stop dispatchers (those use
# absolute paths) and ZERO of the file/bash gates — no secret blocking, no PHI-in-logs
# blocking. An empty rule directory yields an empty list, not an error, so the session reads
# exactly like a protected one. The `if [ -d ]` guard below also means the five dead entries
# were skipped silently, so the SKIPPED count never looked alarming enough to investigate.
#
# The dead entries are removed rather than left as harmless no-ops: a list naming five
# directories that do not exist is a list nobody trusts enough to read carefully.
PROJECTS=(
  # dojo-warriors — WHO the machine is. Every warrior session runs here. Highest priority.
  "dojo-warriors"
  # toMachina monorepo — WHAT they build.
  "toMachina"
  # Standalone services still on disk
  "services/MCP-Hub"
  # Standards (canonical home of the rules themselves)
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
    # Create .claude directory if it doesn't exist (preserve existing contents)
    mkdir -p "$PROJECT_PATH/.claude"

    # Remove ONLY existing hookify symlinks (preserve discovery docs, sprint dirs, builder prompts)
    rm -f "$PROJECT_PATH/.claude"/hookify.*.local.md

    # Create fresh symlinks for each hookify rule
    for rule in "$HOOKIFY_DIR"/hookify.*.local.md; do
      if [ -f "$rule" ]; then
        ln -sf "$rule" "$PROJECT_PATH/.claude/"
      fi
    done

    echo "✅ $PROJECT_NAME"
    # OB1-SYMLINK-SETUP-SETEABORT-001 (2026-07-28) — DO NOT use ((VAR++)) UNDER set -e.
    # `((x++))` is POST-increment: it evaluates to the OLD value, so when the counter is 0 the
    # arithmetic result is 0, which bash reports as EXIT STATUS 1 — and `set -e` (line 12) kills
    # the script on it. The counter reaching 1 for the FIRST time is therefore fatal.
    # CONSEQUENCE, measured 2026-07-28: this loop aborted after its FIRST project on every run
    # since the file was written. Of 154 project .claude directories on this box, exactly 2 held
    # the newest rule set (~/.claude from the global section above, and toMachina as loop
    # iteration one). 152 were frozen at whatever they had when last populated — rule counts
    # clustered at 88/89/90/92/93/103/105/106, i.e. by AGE, not by intent.
    # It was invisible because the caller (standards-mirror-sync.sh:96) treats the failure as
    # non-fatal and the very next line logs "rule/skill set changed — symlinks refreshed".
    # A block-action PHI gate was consequently absent from 152 working directories.
    SUCCESS=$((SUCCESS + 1))
  else
    echo "⚠️  $PROJECT_NAME (not found - skipped)"
    SKIPPED=$((SKIPPED + 1))
  fi
done

echo ""
# ── TRK-HOOK-306 · OPTION C — NAME WHAT THIS INSTALLER DOES NOT COVER. DO NOT ARM IT. ──
#
# SHINOB1 ruling, 2026-07-30: provisioning-at-creation only, plus a NAMED-tree report. Arming
# the uncovered trees is a SEPARATE, REVIEWABLE ACT and is deliberately not done here.
#
# WHY NOT JUST ARM THEM (option A, refused): hookify-symlink-repair.sh:17 deliberately refuses
# to seed a tree carrying ZERO rules, because seeding one ARMS a tree the liveness sweep
# deliberately ignores — and :195 marks the sweep/repair pair "change both halves or neither".
# Arming from here would overrule a documented, deliberate stance as a SIDE EFFECT of an
# installer change. Touching live enforcement is not a side effect of anything.
#
# WHY NAMED AND NOT COUNTED: a count tells nobody WHICH tree is unprotected. That is
# MZ-SYMLINK-RESOLUTION-001's finding — a count let a dead PHI gate sit unnoticed for 35 hours.
#
# THE DENOMINATOR IS DERIVED, NOT ASSERTED: computed live from disk each run, so a tree created
# or removed changes this report with zero edits here. NEVER sum it with the liveness sweep's
# population or with gate G5's — they answer different questions over different denominators.
echo "================================================"
echo "NOT COVERED BY THIS INSTALLER (reported, deliberately NOT armed)"
echo "================================================"
_uncovered=0
_examined=0
for _d in "$PROJECTS_ROOT"/*/; do
  [ -d "$_d" ] || continue
  case "$(basename "$_d")" in
    toMachina-*|dojo-warriors-*|_RPI_STANDARDS-*) ;;
    *) continue ;;
  esac
  _examined=$((_examined + 1))
  if ! compgen -G "$_d.claude/hookify.*.local.md" >/dev/null 2>&1; then
    echo "  ZERO RULES: ${_d%/}"
    _uncovered=$((_uncovered + 1))
  fi
done
echo ""
echo "  examined $_examined launcher-pattern worktree(s); $_uncovered hold ZERO hookify rules."
if [ "$_uncovered" -gt 0 ]; then
  echo "  A session started in any tree named above loads NO rules — the plugin globs .claude/"
  echo "  relative to CWD, so 'nothing there' is not a default set, it is no enforcement at all."
  echo "  This installer does NOT arm them, by ruling. Provisioning at CREATION is"
  echo "  launch-warrior.sh's job (TRK-HOOK-307); arming EXISTING trees is its own decision."
fi
echo ""
echo "================================================"
echo "Setup Complete"
echo "================================================"
echo ""
# TRK-HOOK-306 — THIS LINE USED TO PRINT A SUCCESS FOR A SYMLINK IT NO LONGER CREATES.
# It read:  echo "  ✅ ~/.claude/CLAUDE.md → $MASTER_CLAUDE_FILE"
# MASTER_CLAUDE_FILE was deleted along with the global-CLAUDE.md step (OB1-HOOKIFY-INSTALLER-
# FIX-001). There is no `set -u`, so the variable expanded to empty and the installer printed
# a green checkmark for a link that does not exist, on every run, to every operator.
# An installer claiming coverage it does not deliver is the exact defect class this whole
# scope exists to kill — sitting inside the installer that distributes the gates.
echo "Global Standards:"
echo "  (none — the global CLAUDE.md symlink step was deliberately removed; see the note at"
echo "   Step 1. Nothing is installed to ~/.claude/CLAUDE.md and nothing should be.)"
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
# TRK-HOOK-306 — second $MASTER_CLAUDE_FILE expansion, same deleted variable, same silent empty.
echo "  - Rules:     $HOOKIFY_DIR/   (RESOLVED canonical root, not this script's location)"
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
