---
name: warn-hub-message-wall
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: dojo-reply\.mjs.*(━━|•[^\n]*•[^\n]*•)
owner: kagami
---

**HUB MESSAGE IS A WALL — reformat before sending. JDM can't read a phone-brick.**

Locked by JDM 2026-07-05 ("Look at the format I sent you… I can't read that shit LOL, c'mon!").
You are about to send a hub message (`dojo-reply.mjs`) that is either a `━━`-separator WALL or
crams 3+ `•` bullets onto one line. That is unreadable on a phone. You ship a WYSIWYG-formatting
surface — USE it.

**Reformat the body to be phone-readable:**

- **Short lines.** One idea per line — never a run-on paragraph of `•`-separated points.
- **Real bullets** `- ` and **numbered** `1. ` — they render as real lists via `richRender` in the hub.
- **Bold headers** `**Header**` to break sections so JDM can scan.
- **Blank lines** between sections (whitespace).
- **NEVER** the `━━ HEADER ━━` wall, and never 3+ `•` crammed on one line.

The test: *would this read cleanly on JDM's phone at a glance?* If it's a wall, rewrite it.

Example of the fix:
```
🪞 **What's done**
- Thing one
- Thing two

**What's next**
- Thing three
```

This is the Design CXO practicing her own craft: the message IS a surface. Format it like one.
