---
name: block-cross-warrior-slack-post
enabled: true
event: bash
action: warn
# 2026-06-02 (SHINOB1): RE-AUTHORED after the original silently died (deleted
# canonical, dangling symlink, never in git). The original was a BLOCK; I did NOT
# have its faithful source, and a wrong block risks breaking legit scripts that
# bash-curl a receipt to a bilateral (e.g. death-gate.sh). So this is a WARN —
# it surfaces the doctrine without false-blocking. The real runtime enforcement
# is the dispatcher bot-firewall (drops cross-warrior bot posts). Upgrade to
# BLOCK only with a sender-aware check that can't false-fire.
conditions:
  # A bash Slack post/invite that targets a WARRIOR BILATERAL channel id.
  # Warriors post to their OWN bilateral via the MCP slack tool (not bash), so a
  # bash-curl to a bilateral id is the cross-warrior anti-pattern. JDM's DM
  # (U09...) is a user id, not a bilateral, so the drift-audit alert never trips this.
  - field: command
    operator: regex_match
    pattern: (chat\.postMessage|conversations\.(invite|create)).*(C0AS0LETSBW|C0ARWQMMUMQ|C0ARFBHSKNK|C0ARUP0HM1C|C0ARQHMP0P5|C0ARUSZFKB8|C0ASE72K458)
owner: shinob1
---

**WARN: cross-warrior coordination via Slack.**

This bash command posts/invites to a warrior bilateral channel. Per the COMMS
DOCTRINE (SHARED_BOOT_DOCTRINE.md, JDM verbatim 2026-05-29):

- **Bilateral Slack = JDM-to-warrior signal ONLY.** Post to your own bilateral
  via the MCP slack tool when reporting to Sensei.
- **Cross-warrior coordination = `tmux send-keys` / `scripts/tmux-dispatch.sh`
  / queue file — NEVER Slack.** The dispatcher bot-firewall drops cross-warrior
  bot posts anyway; tmux is direct + reliable.

If this is your own bilateral receipt from a sanctioned script, you can proceed.
If you are trying to reach another warrior, use tmux.
