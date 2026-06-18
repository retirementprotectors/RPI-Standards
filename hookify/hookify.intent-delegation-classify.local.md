---
name: intent-delegation-classify
enabled: true
event: bash
action: intent
conditions:
  - field: command
    operator: regex_match
    pattern: ^(?!.*[Qq]uadrant[:=]\s*[A-Da-d]\b).*(launch-warrior|spawn-subcxo|spawn-coach)
owner: shinob1
---

> **🪞 NARROW CARVE-OUT (JDM-authorized 2026-06-17 · KAGAMI-implemented · SHINOB1-keystone):** the `pattern` carries a leading negative-lookahead `(?!.*quadrant[:=][A-D])`. The Belt STILL FIRES (denies) on any **undeclared** launcher invocation — the forcing function is intact, classification still required. It PASSES only when the operator **explicitly declares the quadrant inline** (e.g. `# quadrant:D`). That is the Belt's own demand — "name the quadrant first" — made satisfiable, NOT a gut: undeclared launches remain blocked. Scope: declared-quadrant pass only; substring over-match (prose mentions) left unchanged.

## DELEGATION CHECKPOINT — Classify Before You Delegate (The Belt)

**You are about to launch a Sub or a Ronin. STOP and name the quadrant first.**
JDM's Delegation Matrix (RATIFIED 2026-06-16). Full protocol: `inbox/!SHINOB1 DOCS!/JDM-DOCTRINES/worker-vs-sub-vs-ronin-protocol-v1.md`.

```
                 BUILD (code)                IN MY DOMAIN (my craft)
  small  →  B = 1+ Build Ticket          C = a TASK
            → Launch THE RONIN (parent)    → Spawn a Worker (in-session Node)

  large  →  A = a BUILD SCOPE            D = a PROJECT
            → Launch A RONIN (sub)         → Launch a Sub (your own sub-CXO)
```

**Declare A / B / C / D and confirm the instrument you just reached for matches it:**
- **A — Build SCOPE → Launch A RONIN.** A coherent, linear, packageable build a dedicated sub-Ronin owns end-to-end. *You* launch it (lowercase name); parent RONIN is unaware unless told.
- **B — 1+ Build Ticket (or could grow into one) → Launch THE RONIN.** Reach parent RONIN directly. He builds it or fans his own workers, per workload.
- **C — Your-domain TASK → Spawn a Worker.** An in-session Node for *your craft* — research, analysis, audit, triage. Never for building code tickets.
- **D — Your-domain PROJECT → Launch a Sub.** Your own dedicated sub-CXO (lowercase session name, or it won't show in JDM's Subs Roster).

### The two principles underneath (Josh-isms)
1. **Just because you CAN, doesn't mean you SHOULD.**
2. **Your core competency is the thing you're GREAT at and LOVE doing — THAT is where you add value to your team, our clients, and the business.**

The matrix isn't "code vs not-code" — it's **your craft vs a colleague's craft.** For most CXOs, code is RONIN's craft → route it to him.

### Hard rules (the implementer enforces these as blocks — see the enforce.sh ticket)
- **RONIN and RAIDEN: NO SUBS.** They are terminal build/guard lanes. If RONIN or RAIDEN is launching a Sub, they're off-pattern → BLOCK.
- **Sub session names MUST be lowercase** → BLOCK an uppercase sub-name (or it's invisible in JDM's Subs Roster).
- **You don't write code** — *domain-aware.* A CXO editing source under the app/package source dirs → WARN, route to RONIN. **EXCEPT KAGAMI in the surface/render layer** (the UI package + app component layer): front-end IS her core competency — she's the *surface self-integrating CXO* (like MUSASHI self-integrates creative). KAGAMI in backend plumbing still WARNS; everyone else in any source WARNS.

> **Belt vs Suspenders:** the A/B/C/D declaration is the **Belt** (a forcing checkpoint — a hook can't prove your "Task" isn't really a "Project"). The deterministic blocks above are the **Suspenders** (real teeth), implemented in enforce.sh because they need warrior-identity (`tmux display-message -p '#S'`) + domain-aware path logic. This `.local.md` is the doctrine SSOT; the enforce.sh engine is the matching/blocking implementation.
