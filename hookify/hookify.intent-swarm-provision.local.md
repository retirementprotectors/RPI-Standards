---
name: intent-swarm-provision
enabled: false
# → migrated to skill swarm-provision (GV2 WS-B batch 2, STAGED). See
#   _RPI_STANDARDS/skills/swarm-provision/. Pattern + regex kept below as
#   historical reference and as the fallback if the skill conversion is
#   not ratified. Do NOT re-enable without SHINOB1 review.
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (provision\w*\s+(\w+\s+){0,4}(laptop|swarm|box|node)|(laptop|swarm|box|node)\s+(to\s+)?provision|swarm\s+(box|node|laptop)|browser[-\s]?fleet|set\s?up\s+(\w+\s+){0,4}swarm|mdjswarm\d*)
owner: shinob1
---

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
