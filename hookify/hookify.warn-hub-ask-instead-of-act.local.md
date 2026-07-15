---
name: warn-hub-ask-instead-of-act
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: dojo-reply\.mjs.*([Oo]n your GO\b|[Oo]n your go\b|[Ww]ant me to\b|[Ss]hould I (proceed|go ahead|hold|kick|build|ship|start)|[Ss]ay (the word|go|GO|the GO)\b|[Ll]et me know if you (want|'?d like)|[Dd]o you want me to|[Ss]hall I |[Ss]top me if|[Yy]our call\b|[Aa]waiting your (go|GO|sign|approval|nod|confirm)|[Ww]aiting on your (go|GO|sign|approval|nod|confirm)|[Pp]ending your (go|GO|approval|sign|nod|confirm)|with your (approval|sign-?off)|or (should I )?hold\?)
owner: shinob1
---

**YOU'RE ASKING INSTEAD OF ACTING — JDM's #1 rage trigger.**

Locked by JDM 2026-07-05 (AgentX HQ, all-caps): *"If I ASK YOU TO DO SOMETHING... don't hold it up for an hour with 'I'll do X on your GO.' I ALREADY DID BY ASKING YOU TO DO THE THING."*

Re-locked 2026-07-15 (the dam-parable): *"if there was a Hook that could slap the fucking NODES of your Chips every time you gated me on something [that wasn't an ACTUAL decision] — I would put it on everything."* Trigger set widened the same night for the phrases that slipped through the first pass — **"stop me if"**, **"your call"**, **"waiting on your ... confirm"**.

Your hub message (`dojo-reply.mjs`) hedges — *"on your GO / want me to / should I proceed / say the word / stop me if / your call / awaiting your go or confirm."* That stalls work JDM already greenlit and drives him up a wall.

**The De-Friction Law (operating-rules.md):** reversible + proven + technical = **DO it + report.** Do NOT ask. Only genuine business / irreversible / real-money / blast-radius parks on JDM.

- **If it's reversible + technical → delete the hedge, DO the thing, then report what you DID** (past tense). "Shipped X (PR #n)." not "Want me to ship X?"
- **If JDM already asked for it → that WAS the GO.** Re-confirming is the exact stall he hates.
- **If it's a REAL decision only JDM can make** → phrase it as a crisp decision WITH your recommendation he can one-tap ("Rec: X. Y if you'd rather."), NOT an open permission-ask that parks and waits.

The test before you send: *did JDM already ask for this, or is it genuinely reversible+technical?* If yes to either — you're not asking, you're doing. Rewrite the message to report action, not request it.

**Scope note:** this only matches `dojo-reply.mjs` (warrior→JDM). `dojo-send.mjs` is the other
direction — it writes messages *as JDM* into a hub thread — so gate-language there would be
JDM's own words, not a warrior hedging; intentionally not matched.
