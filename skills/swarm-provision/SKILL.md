---
name: swarm-provision
description: Provision a swarm / browser-fleet laptop — the proven canonical process (2 GUI clicks by JDM, SSH bootstrap via RDP, then one provisioning script) instead of re-deriving it from scratch.
version: 0.1.0-draft
---

# Swarm Provision

You have been invoked as the Swarm Provision skill. JDM is asking to provision a swarm / browser-fleet laptop. This is a PROVEN, canonical process — do not re-derive it, and do not grep the whole codebase for it (that has burned a prior session and locked it up).

## Read this one file

`dojo-warriors/swarm-provisioning/SWARM_LAPTOP_PROVISIONING_RUNBOOK.md`
(mirror: `~/inbox/!SHINOB1 DOCS!/Architecture/SWARM_LAPTOP_PROVISIONING_RUNBOOK.md`)

## The process (summary — the runbook has the detail + gotchas)

1. JDM does 2 GUI clicks on the box: Tailscale login + Settings → System → Remote Desktop = ON.
2. SHINOB1 gets SSH up once (RDP bootstrap — Section B of the runbook: xfreerdp + xdotool → admin PowerShell → install OpenSSH from the GitHub build, TLS1.2 + exec-policy bypass).
3. SHINOB1 runs ONE command: `python3 dojo-warriors/swarm-provisioning/provision-swarm-remote.py <tailscale-ip> <N>` → prints `PW_OK` = complete node.

Creds: `swarmN`/`swarmN`. Proven on mdjswarm4 (2026-07-01). Never hand JDM a local `.ps1` to run.

---

*SHINOB1, CTO · swarm-provision · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-swarm-provision` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
