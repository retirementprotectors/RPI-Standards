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
    pattern: (?:(?:(?:^|\n)[ \t]*|(?:^|\n)(?![ \t]*(?:[>\-*#<|]|\d+[.)]))(?:[^\n"\'`#]|"[^"\n]*"|\'[^\'\n]*\'|`[^`\n]*`)*?(?:&&|\|\||;|\|)[ \t]*)git\s+(?:-C\s+\S+\s+)*(?:checkout|switch)\b(?!\s+--\s))|(?:(?:\A[ \t]*|(?:^|\n)(?![ \t]*(?:[>\-*#<|]|\d+[.)]))(?:[^\n"\'`#]|"[^"\n]*"|\'[^\'\n]*\'|`[^`\n]*`)*?(?:&&|\|\||;|\|)[ \t]*)(?:ba|z|k)?sh\s+(?:-[A-Za-z]+\s+)*-c\s*(?:"[^"]*|\'[^\']*)\bgit\s+(?:-C\s+\S+\s+)*(?:checkout|switch)\b)
# ── TRK-HOOK-215 (ronin, 2026-07-30) — SILENT ON THE HAZARD IT NAMES ────────────────────
# This rule went QUIET on 4 of 8 real branch ops, on the tree its own body calls the
# worst-exposed of the three. Everything else this contract found was a gate firing when it
# should not. This was a gate not firing when it should, where silence disarms the fleet.
#
# The four, and why the shipped pattern could not see them:
#   bash -c "cd <tree> && git <verb> main"   the && lives INSIDE a quoted span, which the
#   bash -c 'cd <tree> && git <verb> main'   chain branch consumes as a unit, so the operator
#   sh   -c "git -C <tree> <verb> main"      is never available; and the line-start branch
#                                            requires git itself at line start.
#   GIT_PAGER=cat git -C <tree> <verb> main  an env assignment sits between line start and
#                                            git, so [ \t]* never reaches the verb.
#
# THREE OF THE FOUR ARE NOW CAUGHT. A second alternative recognises a shell interpreter
# invoked with -c whose quoted script carries the git op — with the INTERPRETER anchored to
# \A or a real chain operator, never a bare newline. That anchor is the whole trick: a genuine
# `bash -c` hazard IS the command being run, while a documented one sits on a continuation
# line inside someone's report. Verified against this file's own mention corpus AND against a
# real 215 status report: 0 false fires.
#
# ⚠️ THE FOURTH IS DECLARED INEXPRESSIBLE, NOT FIXED, AND THE MEASUREMENT IS WHY.
# Allowing an env-var prefix catches `GIT_PAGER=cat git -C <tree> <verb>` — and fires on the
# DOCUMENTATION of that same hazard, because an indented line in a quoted report is
# byte-identical to an indented line in a shell script. Measured both ways: with the env
# allowance, hazard FIRES and its own doc line FIRES; without it, both go quiet. There is no
# third option available to a text test, which is this file's own declared limit
# ("inside a fenced code block it is a mention; in a script it is a command; regex cannot tell
# them apart") reached from a new direction. An env-prefixed branch op on this tree needs a
# check that reads TREE STATE rather than command text — routed to TRK-HOOK-208's L2/L3 half.
# Recorded here rather than left for the next reader to rediscover by being missed.
#
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
# ── TWO REVIEWER-FOUND DEFECTS, BOTH IN THE SAME CLAUSE (2026-07-26) ─────────────────────
# This rule has now had its claim corrected TWICE by reviewers who chose their own inputs.
#
# 1. SHINOB1, against 4d815aa: the opening-marker lookahead covered > - * # but NOT `<`,
#    `|`, or ordered-list tokens — so an html comment, a markdown TABLE ROW and `1.` / `1)`
#    list items all fired. `|` is itself in the operator alternation, so a table row is a
#    chain operator by construction. His one-character-class fix is applied.
#
# 2. HIKARI, same head, hazard-shaped corpus: FOUR FALSE NEGATIVES — real branch ops going
#    SILENT. The guard was "no quote appears earlier on the line," which buys prose silence
#    and ALSO silences any genuine command carrying a quoted argument:
#        git -C <tree> commit -m "msg" && git <verb> main      <- escaped
#        cd '<tree>' && git <verb> main                         <- escaped
#        cd "<tree>" && git <verb> main                         <- escaped, and this is
#        git -C <tree> stash push -m "wip" ; git <verb> main       BYTE-FOR-BYTE the incident
#                                                                  shape that created this rule
#    A false negative here is strictly worse than a false positive: the rule exists to catch
#    exactly those. Her framing was the fix and she deliberately did not hand it to me —
#    "is the git token inside an OPEN quote span" is a different question from "does a quote
#    appear earlier on the line." Correct, and it is expressible: the guard now allows
#    BALANCED quote spans ("..." '...' `...`) and only an UNCLOSED span blocks the match.
#    A quoted mention never closes before the operator, so it stays quiet; a real command's
#    quoted argument does close, so it fires.
#
#   MEASURED, core.rule_engine, both conditions ANDed, both reviewers' corpora:
#            hazards fire   mentions quiet   safe quiet
#     v1        6 / 10          1 / 10         3 / 4
#     v3       10 / 10*         10 / 10        5 / 5     *6/10 once HIKARI's shapes are added
#     v4       10 / 10         10 / 10        5 / 5
#
# ⚠️ WHAT IT STILL CANNOT SEE — DECLARED rather than denied. This paragraph said "the ONE
# surviving shape" in the first draft of this fix. SHINOB1 measured FOUR: html comment,
# markdown table cell, and numbered-list markers in both the 1. and 1) forms, none of
# which the opening-marker lookahead covered — and `|` is itself in the operator
# alternation, so a table ROW is a chain operator by construction. His one-character-class
# fix is applied above and all four now go quiet. I am recording that the claim was wrong
# a SECOND time in the same file, because that is the actual recurring defect here.
# What remains, and it is genuinely one shape:
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
