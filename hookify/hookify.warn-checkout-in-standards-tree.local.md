---
name: warn-checkout-in-standards-tree
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: Projects/_RPI_STANDARDS(?![\w-])
  - field: command
    operator: regex_match
    pattern: (?:^|\n|&&|\|\||;|\||\()\s*git\s+(?:-C\s+\S+\s+)*(?:checkout|switch)\b
# MZ-STANDARDS-TREE-GUARD-001 (megazord, 2026-07-26) — the THIRD live shared tree.
#
# block-checkout-in-live-deploy-tree covers dojo-warriors and toMachina. It does not cover
# _RPI_STANDARDS, which is the worst-exposed of the three: every hookify rule symlinked into
# every warrior's ~/.claude resolves INTO this tree. A bad checkout here does not break one
# service — it disarms the immune system fleet-wide, silently, for every seat at once.
#
# PROVEN, NOT THEORISED (2026-07-26): while landing MZ-POSIX-PATTERN-DEATH-001 I created a
# branch in this tree, and HEAD was moved back to main underneath me before I committed — two
# empty-message reflog entries either side of the checkout. My commits landed on local main,
# and a truncated pathspec swept a peer's staged work into one of them. Two warriors were
# branching in this tree inside the same hour. Nothing was pushed and everything was restored,
# but the tree offered no guard of any kind while the two lesser-exposed trees now do.
#
# WARN, NOT BLOCK — deliberate, and it is the whole first-pass posture (SHINOB1's condition):
# multiple warriors are actively branching here right now. A block that fires on legitimate
# live rule work wedges the immune system instead of protecting it. Warn first, measure the
# false-fire rate, and only then consider block. Upgrading is one word.
#
# WHAT THIS PATTERN CANNOT SEE — stated next to the result, per cross-warrior gotcha #42.
# Condition 2 anchors on COMMAND POSITION (line start, or after && || ; | and an opening
# paren) rather than matching the token anywhere. That is the declaration-vs-mention fix: it
# will NOT fire on a quoted mention inside an echo, or on a path named mid-sentence.
# It CAN still fire on a git command sitting at the start of a line INSIDE a heredoc or a
# quoted multi-line string — regex cannot tell a heredoc body from a script body. That is a
# known, accepted false-positive class, and it is precisely why this rule is warn and not
# block. A guard that cannot distinguish a command from a quotation of one will fire on the
# postmortem and miss the incident; warn posture makes that cost a nudge instead of a wedge.
#
# NOT MATCHED, ON PURPOSE: the worktree-add subcommand. Creating a worktree is the CORRECT
# action this rule steers toward, and its command contains neither checkout nor switch.
#
# NO POSIX CLASSES. Every dispatcher evaluates with a bare re.compile (rule_engine.py:24),
# which does not implement them; a bracket expression here would compile clean and never
# match. Verified through that same call, not through grep (MZ-POSIX-PATTERN-DEATH-001).
owner: megazord
---

**`_RPI_STANDARDS` is a live shared tree — branch ops there disarm the immune system.**

Your command references the live `_RPI_STANDARDS` checkout (not a worktree) together with a
branch-switching git op.

**Why this tree is different from the other two:** it is not a deploy target, it is the
**runtime**. Every `hookify.*.local.md` symlinked into `~/.claude` — and into every warrior's
project — resolves into this directory. Move HEAD here and every seat's rule set changes
underneath it, with no error, no log line, and nothing on any surface saying enforcement just
changed.

**What to do instead:**

| What you want | Correct path |
|---|---|
| Edit or add a rule | Add a worktree at `~/Projects/_RPI_STANDARDS-<warrior>` off `origin/main` |
| Work an existing branch | Use that worktree, never the live tree |
| Read a rule | Read from the live tree freely — reads are safe, only branch ops are not |
| Land a change | PR from your worktree. Never commit on the live tree's `main`. |

**Two failure modes this tree produces that the others do not:**

1. **Your commit lands on `main` instead of your branch** if HEAD moved while you worked.
   Verify the ref *at commit time*, not at branch-create time.
2. **A commit with a malformed pathspec commits the whole index** — including another
   warrior's staged work, under your ticket id. Stage by explicit path, never `-A`, and read
   the commit's actual output rather than assuming a shell error meant it never ran.

**Known interaction, worth naming:** `block-hookify-rule-write-outside-canonical` matches the
file_path *string*, so it refuses rule-file writes inside a worktree and pushes every rule edit
back into this live tree — the one place this rule is asking you not to move HEAD. The two
controls are individually correct and compose badly. Author at the canonical path, relocate
into your worktree, and commit from there.

**This is a warning, not a block.** If you are deliberately operating on the live tree and know
why, proceed. If you are about to do rule work, use a worktree.

See: MZ-LIVETREE-GUARD-001 (`block-checkout-in-live-deploy-tree`, the other two trees).
