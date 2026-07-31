#!/usr/bin/env bash
# atomic-symlink.sh — replace a symlink WITHOUT ever leaving the path absent.
#
# TRK-HOOK-309 (ronin, 2026-07-31) · scope OB1-HOOKIFY-OVERHAUL-001
#
# ── WHY THIS EXISTS ───────────────────────────────────────────────────────────────────
#
# `ln -sf <target> <link>` is NOT atomic. It is unlink(2) followed by symlink(2), and
# BETWEEN THOSE TWO CALLS THE PATH DOES NOT EXIST.
#
# For a hookify rule link that window is not academic. The rule loaders glob a directory and
# an absent entry is not an error — it is simply a rule that was not found. So a hook firing
# inside the window loads a SHORT rule set and reports an ordinary pass. Silent partial
# enforcement, indistinguishable from a clean run, produced by the very script whose job is to
# install the enforcement.
#
# MEASURED SCALE, 2026-07-30: 17 warrior seats firing PreToolUse hooks continuously while
# setup-hookify-symlinks.sh rewrites 106 links across 4 repos — 424 links per run — on a
# 10-minute timer via standards-mirror-sync. The migration's own repoint was rewritten to use
# the construction below precisely to avoid this; restarting that timer without this fix would
# have reinstalled the same race as a PERMANENT, RECURRING condition, which is worse than the
# one-time window the migration opened, because a window closes and a cron does not.
#
# WORST OF THE FOUR CALL SITES: setup-skills-symlinks.sh did
#     rm -f "$target_dir/SKILL.md"
#     ln -sf "$skill_md" "$target_dir/SKILL.md"
# an EXPLICIT unlink before a non-atomic replace — a strictly wider window than plain `ln -sf`,
# and the comment above it called the pair "idempotent", which it is, while saying nothing
# about the gap it opens. Idempotent and atomic are different properties; that comment
# conflated them.
#
# ── THE CONSTRUCTION ──────────────────────────────────────────────────────────────────
#
# Write the new link under a temporary name, then rename(2) it over the old one. rename(2) is
# atomic: any observer sees either the OLD target or the NEW target, never nothing. `mv -T`
# forces rename semantics on the link itself rather than "move into the directory it points
# at", which is what `mv` would do for a symlink-to-directory.
#
# On failure the temp is removed and the ORIGINAL LINK IS LEFT UNTOUCHED — a failed install
# must never be a disarmed one.
#
# ── USAGE ─────────────────────────────────────────────────────────────────────────────
#   source "$(dirname "${BASH_SOURCE[0]}")/atomic-symlink.sh"
#   atomic_ln <target> <link-path>        # link-path is the LINK, never its parent directory
# Returns 0 on success, 1 on failure. Callers must handle 1 — a populator that fails quietly
# is the defect class this whole scope exists to remove.

atomic_ln() {
  local target="$1" link="$2"
  [ -n "$target" ] && [ -n "$link" ] || return 1
  local tmp="${link}.__atomic.$$"
  if ! ln -sfn "$target" "$tmp" 2>/dev/null; then rm -f "$tmp" 2>/dev/null; return 1; fi
  if ! mv -T "$tmp" "$link" 2>/dev/null; then rm -f "$tmp" 2>/dev/null; return 1; fi
  return 0
}
