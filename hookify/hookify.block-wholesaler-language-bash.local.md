---
name: block-wholesaler-language-bash
enabled: true
event: bash
action: block
# 2026-06-02 (SHINOB1): bash companion to block-wholesaler-language — catches the
# banned terms in curl Slack posts, commit messages, echo/printf, etc. The MCP
# slack_post_message tool is a separate vector not covered by either (noted gap).
conditions:
  - field: command
    operator: regex_match
    pattern: ([Ww]holesaler|[Jj]ustin\s*[Bb]rock)
# ── TRK-HOOK-214 (ronin, 2026-07-30) — THE META-CITATION TOKEN IS REMOVED ────────────────
# It was added 2026-06-15 (ZRD-SCOPE-HOOK-001) so a dispatch legitimately CITING this rule could
# pass. The intent was right and the mechanism was a universal bypass. Measured against the
# wired engine before removal:
#
#   real violation, no token ....................... BLOCK  ✓
#   legitimate meta-citation carrying the token .... allow  ✓
#   REAL VIOLATION carrying the token .............. allow  ✗
#   real violation, token in a trailing comment .... allow  ✗
#
# `not_contains` asks whether a STRING APPEARS ANYWHERE in the command. It cannot ask whether
# that string is a citation. So the token stood the whole rule down on genuine content, and the
# token was PUBLISHED in this file — anyone reading the rule to understand it had learned how
# to defeat it. RPI Rule #1 is JDM's #1 directive; a documented password on it is worse than
# the inconvenience it removed.
#
# THE SAME DEFECT, SAME REPO, ALREADY PAID FOR ONCE: block-checkout-in-live-deploy-tree carried
# a `not_contains` exemption naming its repair script, HIKARI broke it with a trailing comment
# in one command, and it was REMOVED rather than re-keyed with the reasoning recorded in that
# file: "you cannot express 'this executable was invoked, and nothing else dangerous was' as a
# text test over a raw command line." That conclusion generalises to every content token.
#
# WHAT REPLACES IT: nothing, and that is measured, not assumed. Before removing, every file on
# this box carrying the banned term was classified — 0 relied on the token, 8 are covered by
# LOCATION exemptions on the file-tier twin. No legitimate flow loses its only path. The
# working alternatives are (a) name the rule DESCRIPTIVELY rather than quoting the term, which
# is how the fleet ruling on this very topic was authored without tripping anything, and
# (b) for reports, pass the body as a FILE rather than as command text
# (tmux-dispatch.sh <TARGET> -f <path>, git commit -F, gh pr create --body-file).
#
# LOCATION-SCOPED EXEMPTIONS ARE THE SAFE FORM AND THEY STAY on the file-tier twin (hookify,
# CLAUDE.md, docs/discoveries). To claim one you must ACTUALLY BE WRITING IN THAT LOCATION,
# which the engine can check and which cannot be asserted by typing a word. A content token
# can always be typed. That is the whole distinction, and it is now fleet doctrine.
owner: shinob1
---

**BLOCKED: carrier-intermediary language in a shell command (RPI Rule #1).**

A `curl` Slack post, commit message, or echo containing the banned terms.
Use carrier-direct / writer sourcing. See block-wholesaler-language for the rule.
