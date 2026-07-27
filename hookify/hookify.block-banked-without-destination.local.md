---
name: block-banked-without-destination
enabled: true
event: stop
action: block
severity: BLOCK
scope: OB1-BANKED-001
introduced: 2026-07-27
owner: shinob1
# JDM, 2026-07-27: "Do we have a hook to SLAP THE FUCK out of someone who says
# 'Banked.' or 'I'll Bank it.'"
#
# Measured before writing this: 225 hits across 29 warrior identities in
# toMachina.discussions, 2026-04-09 -> 2026-07-27. It is one of the most durable
# verbal tics in the corpus.
#
# WHY IT IS THE SAME BUG AS §7.2. "Banked" is an ACKNOWLEDGEMENT WEARING THE COSTUME
# OF AN ACTION. It reads like disposal — the thing has been handled, filed, put
# somewhere — while nothing was written anywhere. It is exactly "Delegated to RONIN":
# the only artifact is that you SAID it.
#
# A warrior in this very corpus already diagnosed it, unprompted:
#   "'Banking it' is a hub post that scrolls away"
# That is the whole indictment. A hub post is not a destination.
#
# THE TEST — the same artifact test as project-launch-template.md §7.2:
#   Banked WHERE? Name the destination or you did not bank anything.
#
# NOT A BAN ON THE WORD. Legitimate uses pass automatically because they carry a
# destination or are plainly mechanical:
#   "banking this seat's delta to disk"          -> disk, a real target
#   "banked it as TRK-14798"                     -> a ticket id
#   "banked to /home/jdm/inbox/x.html"           -> a path
#   "'Banking it' is a hub post that scrolls away" -> critique, exempted below
conditions:
  # 1. The turn claims to have banked / shelved / noted-for-later.
  - field: last_assistant_message
    operator: regex_match
    pattern: (?i)(?:\bbank(?:ed|ing)\b|\bbank\s+it\b|\bi.?ll\s+bank\b|\bnoted\s+and\s+banked\b|\blogg(?:ed|ing)\s+(?:it|that)\s+for\s+later\b|\bfil(?:ed|ing)\s+(?:it|that)\s+for\s+later\b|\bshelv(?:ed|ing)\s+(?:it|that)\b|\bpark(?:ed|ing)\s+(?:it|that)\s+for\s+later\b|\badded\s+to\s+the\s+backlog\b)
  # 1b. FINANCE-NOISE EXCLUSION — mandatory. The dominant n-grams in this corpus are
  #     "bankers fidelity" (10,764 — a carrier), "bank_managed"/"bank manages" (7,164 —
  #     a schema field), and client "bank account/routing/information". A gate that
  #     fires on those is disabled within a day.
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (?i)\b(?:banker|bankers|bankrupt\w*|bank[_\s]manage\w*|bank\s+isn)
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (?i)\bbank(?:ing)?\s+(?:account|routing|information|info|statement|deposit|draft|transfer|fidelity|life|of\s)
  # 2. ...and NO destination artifact appears anywhere in the turn.
  #    A ticket id, a file path, a URL, a PR/commit, or a named collection all count.
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (?i)(\b(TRK|OB1|ZRD|MZD|HIK|KGM|VOL|RON|TKO)-[A-Z0-9-]{3,}|/[a-z0-9_.-]+/[a-z0-9_.-]+|https?://|\bPR\s*#?\d+|\b[0-9a-f]{7,40}\b|tracker_items|firestore|bigquery|\.json\b|\.ndjson\b|to\s+disk\b)
  # 3. Exemption — talking ABOUT the pattern (retro, this rule, critique).
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (?i)(block-banked|OB1-BANKED|scrolls away|banned form|hedge sweep|hookify|this rule|the gate|retro|i (said|wrote|used)|caught myself|n-?gram|corpus|violations?\b|must-?not-?fire|must-?fire|false.?positive|re-?measured|measured|exemption|hits\b|by lane)
---

⛔ **BLOCKED — "banked" is not a destination.**

You said you banked / shelved / noted-for-later, and **you did not name where.**

That is an acknowledgement wearing the costume of an action. It reads like the thing was
handled. Nothing was written anywhere. It is the same defect as calling a ticket
*"Delegated"* — the only artifact is that you said it.

One of your own already put it better than this rule can:

> *"'Banking it' is a hub post that scrolls away."*

**The test — same as §7.2: banked WHERE?**

Name one and this passes:

- a **ticket id** — `TRK-14798`, `OB1-…`, `ZRD-…`
- a **file path** — `/home/jdm/inbox/…`
- a **URL** — the surface it renders to
- a **PR or commit sha**
- a **collection** — `tracker_items`, Firestore, BigQuery
- **to disk** — for genuine state persistence before a refresh

If you cannot name one, you have not banked anything. **Go write it somewhere it will be
found by someone who is not you, then say where.**

JDM has 93,704 `.md` files and 4,255 unique. The reason nothing is findable is that
"banked" has meant "mentioned once, in a stream, and never again."
