---
name: warn-tailscale-serve-funnel-nuke
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: tailscale\s+serve\b
owner: taiko
---

**⚠️ `tailscale serve` BLACKS OUT THE ENTIRE PUBLIC FUNNEL on MDJ_SERVER**

The `mdjserver.tail7845ea.ts.net` endpoint serves the platform's whole public
face via Tailscale **Funnel** (public): `/` (portals → :4200), `/inbox`
(→ :80 — case roadmaps + funnel-served HTML JDM links to), `/submit`, `/code`,
`/chat/events`, `/system-synergy-local`.

`tailscale serve` = **TAILNET-ONLY** mode, mutually exclusive with funnel on :443.
Running it flips the WHOLE funnel to "tailnet only" — dropping EVERY public path
at once, not just the one you're adding. (Verified ~5s full public outage
2026-06-13 while adding a single path with `serve`.)

**Use `tailscale funnel` for PUBLIC routes — it's additive + stays public:**

    sudo tailscale funnel --bg --set-path=/your/path http://127.0.0.1:<port>

**VERIFY:** `sudo tailscale funnel status` MUST show "**Funnel on**" + every
expected path. If you see "(tailnet only)" you just blacked out the platform's
public face for everyone — re-run with `funnel`, not `serve`.

(2nd gotcha: tailscale STRIPS the mount-path prefix → the backend receives `/`,
so register the handler at BOTH `/` and the mount path or it 404s through the funnel.)

If you genuinely intend a private tailnet-only serve and are certain it won't
disturb the public funnel on :443: ignore this warning and proceed.
