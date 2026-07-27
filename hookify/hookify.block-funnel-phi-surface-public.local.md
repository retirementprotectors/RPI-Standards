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

---

## ⛔ DO NOT ANCHOR THIS PATTERN TO A COMMAND POSITION — measured 2026-07-27, `OB1-FUNNEL-RULE-KEEP-LOOSE-001`

**EXCLUDED-WITH-CAUSE.** The loose match below is **deliberate**, not an oversight. Read this
before "fixing" it.

**The known false-positive class is real:** the pattern matches the bare token anywhere in a
command, so **prose that merely MENTIONS this command trips a Tier-1 block.** It fired on a
SHINOB1 boot recitation whose IDENTITY bullet described the mdj-agent architecture ("reached
via API → the public tunnel"). The seat then mis-attributed the block to a *different* rule
whose subject it had just been writing about — the tripping token was two bullets away from
the one it blamed. (Truth signal for any block: `~/.claude/hooks/violation-log.jsonl`, never
a guess from the rule name. Cross-warrior gotcha #14.)

**The obvious fix was built, attacked, and REJECTED.** Anchoring to a command position —
`(?:^|[;&|]\s*|\n|\$\(\s*|`+"`"+`\s*)\s*(?:sudo\s+)?…` — the pattern already proven in-house by
`block-git-checkout-main-in-worktree`, **cleared all three false positives and opened FIVE
false negatives.** Each of these is a real invocation that would have reached the public
internet with **no block**:

| Form | Why the anchor misses it |
|---|---|
| `nohup <cmd> 443 &` | wrapper before the command |
| `env FOO=1 <cmd> 443` | env prefix |
| `if true; then <cmd> 443; fi` | `then` is not a separator char |
| `for p in 1 2; do <cmd> $p; done` | `do` is not a separator char |
| `xargs <cmd>` | invoked indirectly |

**The asymmetry is the whole argument, and it is rule-specific.** A checkout guard's false
negative costs a worktree collision — annoying, recoverable, so an anchor is the right trade
*there*. **This rule's false negative costs client PHI on the open internet: a reportable
HIPAA breach.** On this gate, over-blocking prose is the CORRECT posture and the friction is
the price. Do not port the sibling rule's anchor here on the grounds that it is "the house
pattern" — the house pattern is correct for the house's *recoverable* gates.

**The correct remedy for the friction is NOT a looser pattern.** Pass long message bodies to
scripts via a file (`"$(cat body.txt)"`) rather than inline. That is already fleet doctrine for
an unrelated reason — inline bodies let the shell execute backtick content and silently drop
words from a message.

⚠️ **BUT KNOW WHAT THAT REMEDY COSTS, because it is a hole in this layer, not a clean fix:**
the identical body **blocks inline and passes via `"$(cat file)"`** — measured both ways, same
rule, opposite result. **File indirection bypasses EVERY content-matching Bash gate we have,
not just this one.** The write-time layer structurally cannot see a body it never receives.
Content gates aimed at *message bodies* therefore belong at the **script/publish boundary**
(inside `dojo-reply.mjs` / `scroll-recite.sh`), not on the shell command surface. Tracked as
`OB1-HOOK-FILE-INDIRECTION-001` — do not mistake this rule's green for coverage of a
file-routed body.

**If you still want to change this pattern:** reproduce the five forms above against your
candidate first, and get the sign-off from someone who did not write it. A tightening that has
only been tested on inputs its own author chose has been rehearsed, not tested.

⚠️ **AND PIN YOUR PROBE'S CWD, OR IT WILL LIE TO YOU.** The hookify loader globs rule files
**relative to process CWD**. The same probe, same payloads, same engine, run from two
directories on 2026-07-27:

```
cwd = ~/Projects/toMachina-shinob1     -> 7 of 7 expected results
cwd = ~/Projects/_RPI_STANDARDS        -> 3 of 7   (four rules silently stopped firing)
```

Nothing errors. The wrong-cwd run returns `{}` for commands that genuinely block, which reads
exactly like *"no rule matched"* — **a clean pass is the failure mode.** This nearly produced a
false conclusion that editing THIS file had broken the whole dispatcher, because the verify run
happened to be issued after a `cd` into the standards repo. **State the cwd next to any hookify
probe result**; a result without its cwd is unfalsifiable. (Same shape as the `claude mcp list`
cwd-dependence already flagged in the MCP inventory doctrine, and as gotcha #41 — your own
instrument manufacturing a clean negative.)

🥷 — SHINOB1, CTO · measured, not reasoned · the fix was built and killed with evidence
