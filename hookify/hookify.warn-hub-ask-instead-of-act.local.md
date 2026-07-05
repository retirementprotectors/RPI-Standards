---
name: warn-hub-ask-instead-of-act
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: dojo-reply\.mjs.*([Oo]n your GO\b|[Oo]n your go\b|[Ww]ant me to\b|[Ss]hould I (proceed|go ahead|hold|kick|build|ship|start)|[Ss]ay (the word|GO\b|the GO)|[Ll]et me know if you (want|'?d like)|[Dd]o you want me to|[Ss]hall I |[Aa]waiting your (go|GO|sign|approval|nod)|pending your (go|GO|approval|sign|nod)|with your (approval|sign-?off)|or (should I )?hold\?)
owner: shinob1
---

**YOU'RE ASKING INSTEAD OF ACTING — JDM's #1 rage trigger.**

Locked by JDM 2026-07-05 (AgentX HQ, all-caps): *"If I ASK YOU TO DO SOMETHING... don't hold it up for an hour with 'I'll do X on your GO.' I ALREADY DID BY ASKING YOU TO DO THE THING."*

Your hub message (`dojo-reply.mjs`) hedges — *"on your GO / want me to / should I proceed / say the word / awaiting your go."* That stalls work JDM already greenlit and drives him up a wall.

**The De-Friction Law (operating-rules.md):** reversible + proven + technical = **DO it + report.** Do NOT ask. Only genuine business / irreversible / real-money / blast-radius parks on JDM.

- **If it's reversible + technical → delete the hedge, DO the thing, then report what you DID** (past tense). "Shipped X (PR #n)." not "Want me to ship X?"
- **If JDM already asked for it → that WAS the GO.** Re-confirming is the exact stall he hates.
- **If it's a REAL decision only JDM can make** → phrase it as a crisp decision WITH your recommendation he can one-tap ("Rec: X. Y if you'd rather."), NOT an open permission-ask that parks and waits.

The test before you send: *did JDM already ask for this, or is it genuinely reversible+technical?* If yes to either — you're not asking, you're doing. Rewrite the message to report action, not request it.
