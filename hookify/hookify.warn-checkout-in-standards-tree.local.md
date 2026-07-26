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
    pattern: (?:(?:^|\n)[ \t]*|(?:^|\n)(?![ \t]*[>\-*#])[^\n"'`#]*?(?:&&|\|\||;|\|)[ \t]*)git\s+(?:-C\s+\S+\s+)*(?:checkout|switch)\b(?!\s+--\s)
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
# ── MZ-ANCHOR-CHAIN-FIX-001 — A FALSE CLAIM, CORRECTED (2026-07-26) ──────────────────────
# The v1 comment here asserted this rule "will NOT fire on a quoted mention inside an echo."
# THAT WAS FALSE AND MEASURABLY SO. SHINOB1 read the shipped rule against an 8-shape mention
# corpus and 5 of 8 fired, the echo case among them.
#
# MECHANISM: v1 anchored on (?:^|\n|&&|\|\||;|\||\() and NONE of the chain-operator
# alternatives cares what PRECEDES it on the line. Any text containing "... && git <verb>"
# matched regardless of sitting inside quotes, a comment, a bullet or a blockquote.
# Line-start anchoring worked; the chain-operator anchors did not — and those are exactly the
# forms documentation naturally uses.
#
# WHY MY OWN TEST MISSED IT: my corpus had two prose shapes and NEITHER contained a chain
# operator, so both went quiet for the wrong reason and I read that as the anchor working.
# A sample that cannot reproduce the phenomenon is not evidence about it. The test was the
# artifact, not the rule — the same shape as the defect this whole arc is about.
#
#   MEASURED, through core.rule_engine, both conditions ANDed:
#            mention shapes firing      hazards      safe ops
#     v1            7 / 10               6 / 6        0 / 6
#     v2 (this)     1 / 10               6 / 6        0 / 6
#
# v2 keeps the line-start branch and guards the chain-operator branch two ways: the line must
# not OPEN with a markdown/comment marker (> - * #), and no quote or backtick may appear
# before the operator. Quoted, single-quoted, bulleted, blockquoted and commented mentions all
# go quiet; every real hazard still fires, including the leading-whitespace form.
#
# ⚠️ WHAT IT STILL CANNOT SEE — the one surviving shape, DECLARED rather than denied:
# an INDENTED chained command ("    cd <tree> && git <verb> main") still fires. That is not
# fixable here and arguably should not be — it is byte-identical to a real indented line in a
# shell script, which SHOULD fire. Inside a fenced code block it is a mention; in a script it
# is a command; regex cannot tell them apart. Heredoc bodies are the same class.
# Both are why this rule is warn and not block: a guard that cannot distinguish a command from
# a quotation of one will fire on the postmortem and miss the incident, and warn posture makes
# that cost a nudge instead of a wedge.
#
# ALSO NOT MATCHED: a FILE-RESTORE checkout (the double-dash pathspec form). Restoring a
# file is not a branch op and must not warn — found while writing this fix, by needing to
# restore a file in the live tree and watching my own rule warn about it. The modern
# restore subcommand never matched; the legacy double-dash form did, and now does not.
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
