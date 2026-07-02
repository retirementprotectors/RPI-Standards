---
name: block-funnel-phi-surface-public
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: tailscale\s+funnel\b(?!\s+status)(?!\s+--help)(?!.*\boff\b)(?!.*funnel-public-justified)
owner: shinob1
---

🛑 **BLOCKED: `tailscale funnel` exposes a surface to the PUBLIC INTERNET — confirm intent**

You're about to put something on the **public Tailscale Funnel** (reachable by anyone on the
open internet, no tailnet required). This is the #1 source of accidental PHI exposure on
MDJ_SERVER. On 2026-06-27 the `/inbox` file server sat on the public funnel with no auth and
an open directory listing — serving live client PHI (names, account numbers, balances, DOBs)
to the open internet for days. VOLTRON caught it; SHINOB1 locked it down.

**Default posture = PRIVATE.** Box surfaces should use `tailscale serve` (tailnet-only —
reachable by JDM's devices + warriors, NOT the public internet). The funnel is reserved for
the *tiny* set of endpoints that external third parties MUST hit:

| Legit public funnel | Why | Must have |
|---|---|---|
| Twilio voice/SMS webhook (`/voice`) | Twilio servers call it | signature verification |
| Form-submit webhook (`/submit`) | external form POSTs | method + payload validation |
| AgentX hub (`/`) | JDM's phone (until phone is on the tailnet) | Firebase auth |

**NEVER public-funnel:** any local **file server**, anything serving `/home/jdm/inbox/**`,
code-server, raw Firestore/Drive proxies, or ANY surface that can return PHI/credentials.

**The fix is almost always:** use `tailscale serve` instead of `tailscale funnel`:
```bash
sudo tailscale serve  --bg --set-path=/your-path http://127.0.0.1:PORT   # tailnet-only (correct default)
```
If JDM can't reach a tailnet-only surface from his phone, the answer is **put his phone on the
tailnet** (install the Tailscale app) — NOT expose it to the world.

**Override (a genuinely-public, auth-gated webhook):** append the marker to the command:
```bash
sudo tailscale funnel --set-path=/voice http://127.0.0.1:4230   # funnel-public-justified: Twilio webhook, signature-verified
```
The marker forces a conscious decision + leaves an audit trail. `tailscale funnel status`,
`--help`, and any `... off` (turning exposure OFF) are always allowed.

**Why BLOCK, not WARN:** a public PHI leak is a HIPAA breach. The cost of a false-positive
(add one marker comment) is trivial; the cost of a missed exposure is a reportable breach.

Why this exists: ZRD-SCOPE-FUNNEL-PRIVATE-BY-DEFAULT-001 (JDM directive 2026-06-27,
"solve this Tailscale public/private BS tonight") + the /inbox PHI breach VOLTRON flagged.
Owner: SHINOB1 (immune system).
