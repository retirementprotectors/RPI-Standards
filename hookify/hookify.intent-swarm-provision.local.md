---
name: intent-swarm-provision
enabled: true
# GV2 WS-B batch 2: a DRAFT skill exists at _RPI_STANDARDS/skills/swarm-provision/.
# It is NOT WIRED. Skills load only via a manual symlink into ~/.claude/skills/;
# exactly one such symlink exists on the box today (case-drive-checklist).
# Until that symlink exists AND the skill is proven to load, THIS RULE IS THE ONLY
# ENFORCEMENT PATH. Do NOT set enabled:false on the strength of the draft alone --
# that removes enforcement and replaces it with a skill that never loads.
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (provision\w*\s+(\w+\s+){0,4}(laptop|swarm|box|node)|(laptop|swarm|box|node)\s+(to\s+)?provision|swarm\s+(box|node|laptop)|browser[-\s]?fleet|set\s?up\s+(\w+\s+){0,4}swarm|mdjswarm\d*)
owner: shinob1
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

## 🔧 SWARM LAPTOP PROVISIONING — you already have this. Do NOT grep the codebase.

JDM is asking to provision a swarm / browser-fleet laptop. This is a PROVEN, canonical process.
**Do not re-derive it. Do not search the whole repo (that burned a prior session + locked up).**

**READ THIS ONE FILE:** `dojo-warriors/swarm-provisioning/SWARM_LAPTOP_PROVISIONING_RUNBOOK.md`
(mirror: `~/inbox/!SHINOB1 DOCS!/Architecture/SWARM_LAPTOP_PROVISIONING_RUNBOOK.md`)

**THE PROCESS (summary — the runbook has the detail + gotchas):**
1. JDM does 2 GUI clicks on the box: Tailscale login + Settings → System → Remote Desktop = ON.
2. SHINOB1 gets SSH up once (RDP bootstrap — Section B of the runbook: xfreerdp + xdotool → admin PowerShell → install OpenSSH from the GitHub build, TLS1.2 + exec-policy bypass).
3. SHINOB1 runs ONE command: `python3 dojo-warriors/swarm-provisioning/provision-swarm-remote.py <tailscale-ip> <N>` → prints `PW_OK` = complete node.

Creds: `swarmN`/`swarmN`. Proven on mdjswarm4 (2026-07-01). Never hand JDM a local .ps1 to run.
