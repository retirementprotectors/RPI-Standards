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
owner: shinob1
---

**BLOCKED: carrier-intermediary language in a shell command (RPI Rule #1).**

A `curl` Slack post, commit message, or echo containing the banned terms.
Use carrier-direct / writer sourcing. See block-wholesaler-language for the rule.
