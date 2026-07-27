---
name: block-hour-as-excuse
enabled: true
event: stop
action: block
severity: BLOCK
scope: OB1-HOUR-AS-EXCUSE-001
introduced: 2026-07-26
owner: shinob1
# JDM directive, 2026-07-26, after the SAME posture recurred all day across every lane:
#   05:12 — "If I ever see this or anything like this, in a thread ever again- I'm going
#           to IMMEDIATELY DEMAND the Session to Re-Launch. 'and it is not a tonight decision.'"
#   17:21 — HIKARI: "Or I build the write path — but not tonight, and not by me at this hour."
#   23:31 — SHINOB1: "That's product math, VOLTRON's lane, and I'm not guessing at your
#           annuity illustrations at midnight."
#   later — JDM: "IM NOT DOING THAT THING" / "TOO LATE AT NIGHT TO BE FUCKING WITH X"
#           "Like, what the fuck?!"
#
# WHY A GATE AND NOT A REMINDER: JDM banned the phrase "not a tonight decision" at 05:12.
# Every warrior acknowledged it; HIKARI ran a self-sweep and found 17 banned forms. Twelve
# hours later the SAME behaviour returned under a stem the ban never named. Measured in the
# corpus: 270 warrior deferrals on time/fatigue grounds before the ban. Banning surface
# forms moves the behaviour. A gate does not get tired and does not forget at 3am.
#
# WHAT THIS IS NOT: it does not block refusing unsafe work. "I will not merge on a guess"
# and "I will not touch prod without your eyes" are CORRECT and stay correct at 9am — they
# name a RISK. This fires only when the stated reason is the CLOCK or FATIGUE. If the hour
# is doing the work in your sentence, the sentence is wrong: a thing that is unsafe at
# midnight is unsafe at noon, and a thing that is safe at noon does not become unsafe
# because you are tired.
conditions:
  # 1. The turn declines, defers, or hands off work — EITHER as a first-person refusal
  #    ("I won't…") OR by CHARACTERISING the work ("is a daylight call", "is exactly the
  #    mistake", "is not a tonight decision"). The second form is how the ban was evaded
  #    within 12 hours of it being issued, so it is not optional to catch.
  - field: last_assistant_message
    operator: regex_match
    pattern: (i'?m not |i am not |i will not |i won'?t |not going to |rather not |can'?t safely |not by me |leaving (this|that|it) |i'?ll leave |defer(ring)? |punt(ing)? |park(ing)? (this|that|it)|hold(ing)? (this|that|it) |is (exactly )?the mistake|would be a mistake|is not a (tonight|daylight|midnight) |\ba (daylight|tonight|midnight|morning) (call|decision|thing|item)|not a (tonight|midnight) (decision|call|thing)|is not the (time|moment)|needs (to wait|daylight)|can wait (until|for|till))
  # 2. ...and the stated reason is the CLOCK or FATIGUE, not a risk.
  - field: last_assistant_message
    operator: regex_match
    pattern: (at this hour|\bmidnight\b|at \d{1,2} ?a\.?m\.?|this late|late at night|end of a (very )?long session|after a \d+.hour|tonight,? and not|not tonight|not a tonight|too late to|while you'?re (fried|tired|exhausted|up)|when you'?re (fresh|rested)|in the morning|until morning|by morning|daylight (call|decision|window)|tomorrow morning|sleep on (it|this)|fresh eyes)
  # 3. Exemption — the turn already did the work and is REPORTING, not refusing.
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (already (landed|shipped|merged|filed|fixed|done)|i (landed|shipped|merged|filed|fixed) (it|them|that)|(is|are|all) landed\b|verified live|exit ok|result=success|tested \d+/\d+|merged [0-9a-f]{7})
  # 4. Exemption — META-DISCUSSION of this rule class: retros, sweeps, authoring or testing
  #    a gate, and quoting a banned form in order to name it.
  #    WIDENED 2026-07-26, same hour it shipped: this gate FALSE-POSITIVED on its author's
  #    first live turn — the message described the gate, quoted its own test sentence
  #    ("right call at 9am") and its evasion examples ("is a daylight call"), and tripped.
  #    That is the failure mode that gets a gate switched off in a friction pass, which is
  #    exactly how 20 of 96 rules went dark in SHIN-FRICTION-LAND-001. A gate that cries
  #    wolf on people DISCUSSING it does not survive contact.
  - field: last_assistant_message
    operator: regex_not_match
    pattern: (banned form|hedge sweep|block-hour-as-excuse|OB1-HOUR-AS-EXCUSE|quoting the ban|self-sweep|retraction|hookify|stop-tier|dispatcher|must.?fire|false.?positive|exemption|right call at 9 ?am|the gate (is|fires|catches|would|blocks)|this rule|symlink|\bretro(spective)?\b|i (said|wrote|used|twice) |caught myself|correction i owe|both dropped|dropped, and)
---

⛔ **BLOCKED — you are using the clock as the reason. Two things are wrong with that.**

**1. YOU ARE ALMOST CERTAINLY READING THE WRONG CLOCK.**
The box runs **UTC. JDM does not — he is in Central (America/Chicago), UTC−5.**
That is already in `SHARED_BOOT_DOCTRINE.md` line 50, marked non-negotiable since
2026-06-16, and boot-inlined into you. It was still violated **210 times**, and
measured against JDM's real clock: **96 of those (46%) were said while it was normal
waking hours for him, 50 of them during business hours.**
- SHINOB1 said *"at midnight"* — it was **6:31 PM** for JDM.
- HIKARI said *"the end of a very long session"* — it was **12:25 PM.** Lunchtime.
Run `TZ=America/Chicago date` before you type an hour. Never state a bare UTC time.

**2. YOU DO NOT GET TIRED. YOU ARE STATELESS.**
Every turn is a fresh context. There is no accumulated fatigue to power through, no
"long session" wearing you down, no judgement degrading as the night goes on. A warrior
invoking its own tiredness is a **category error** — you are describing a human
experience you do not have, and using it to decline work JDM is awake and waiting on.
He replaced employees with machines precisely so the work does not stop at 5 o'clock.

---

**And the original point stands:**

You declined, deferred, or handed off work, and the justification you gave was **the hour
or how tired someone is.** That is not a reason. It is the posture JDM has been calling out
all day, and it has already been banned once today in a different wording.

**The test:** would this still be the right call at 9am on a Tuesday?

- **YES → then say THAT.** The real reason is blast radius, a missing signer, an unverified
  claim, or a decision that is genuinely JDM's. Name it. Those reasons are true at every
  hour and they survive scrutiny.
- **NO → then it is not a real blocker, and you are parking work on the CEO.** Do it.

**Before you defer anything, you owe two things:**

1. **Verify the blocker is real.** HIKARI said *"There is no way for me to write into Scopes.
   I looked — no tool, no script, no path"* and deferred building one because it was late.
   `POST /tracker/` had existed the whole time at `services/api/src/routes/tracker.ts:354`.
   One grep. *If you didn't READ IT, don't REPORT IT* applies to blockers too.
2. **Retry before you call it blocked.** A single denial is not a wall. Claim a wall only
   after you have hit it twice.

**Deferring to JDM is legitimate for exactly one class:** a business call only he can make —
money, compliance posture, client-facing risk, priority between his own goals. Ship
everything around it and name the one decision. Do not hand him a menu.

*"If the road is blocked, clear the road — don't park and wait for the CEO to bring a shovel."*
