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
    pattern: (?i)(spawn[-_ ]?(?:subcxo|worker|sub|seat)|spawn-subcxo-mesh|launch-warrior|dispatch(?:ed|ing)?\s+(?:a\s+)?(?:worker|seat|sub|ronin)|\b(TRK|OB1|ZRD|MZD|HIK|KGM|VOL|RON|TKO)-[A-Z0-9-]{3,}|subject[-_ ]registry|recall\.html|tracker_items|\bPR\s*#?\d+|\b[0-9a-f]{7,40}\b|to\s+disk\b|to\s+memory\b)
  # 3. Exemption — talking ABOUT the pattern (retro, this rule, critique).
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (?i)(block-banked|OB1-BANKED|scrolls away|banned form|hedge sweep|hookify|this rule|the gate|retro|i (said|wrote|used)|caught myself|n-?gram|corpus|violations?\b|must-?not-?fire|must-?fire|false.?positive|re-?measured|measured|exemption|hits\b|by lane)
---

⛔ **BLOCKED — you banked something and took no action.**

Naming a location does not count. *"Banked to `/tmp/notes.md`"* is how this box got to
**93,704 `.md` files, 4,255 unique**, none of which anyone can find twice. A location is a
coordinate. What is required is a **disposition** — a decision, and a worker that acts on
it *now*.

**Answer these four, in order, in this turn:**

**1 · Does this belong on a Canonical Dynamic Subject Surface?**
`https://mdjserver.tail7845ea.ts.net:8443/inbox/recall.html` — the Subjects registry.
That is the default home for anything a human will ever need to find again.

**2 · Why, or why not?** State it in one line. Not "probably" — decide.

**3 · If YES → SPAWN A WORKER TO ADD IT NOW.**
```
bash ~/Projects/dojo-warriors/scripts/spawn-subcxo-mesh.sh \
  --parent RONIN --sub-type BUILD --scope-id <slug> --brief <brief-path>
```
Not "I'll add it." Not a ticket to add it later. The worker is spawned in this turn, or
the information is not banked.

**4 · If NO →**
&nbsp;&nbsp;**a)** why not — what makes it *not* findable-worthy
&nbsp;&nbsp;**b)** where does it correctly belong — the actual canonical home
&nbsp;&nbsp;**c)** **spawn a worker to move it there RIGHT NOW**

---

**What passes this gate:** a spawn command, a launched seat, a filed ticket id, a
`subject-registry` entry, a PR/commit, or genuine state persistence (`to disk` before a
refresh).

**What does not:** a file path. A promise. "Noted." "Banked."

> *"'Banking it' is a hub post that scrolls away."* — one of your own, unprompted.

The whole failure class in one line: **an acknowledgement wearing the costume of an
action.** Same defect as calling a ticket *"Delegated"* — the only artifact is that you
said it. Decide, then spawn.
