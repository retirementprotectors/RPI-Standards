---
name: intent-sendit
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    # OB1-INTENT-TRIGGER-INTENT-001 (2026-07-25): bare `send\s+it` and `ship\s+it` REMOVED.
    # They are not deploy syntax — they are ordinary operational English, and this is an
    # event:prompt rule whose body is INJECTED INTO A WARRIOR'S CONTEXT AS DIRECTIVES. So a
    # bare-verb-phrase match here is a fabricated-deploy-order generator.
    # MEASURED on 2026-07-25: every single fire that night came from ordinary prose — a
    # comms-ROUTING broadcast containing "send it to me" fired the deploy protocol on four
    # seats at once; a "SHIP IT AND REPORT" broadcast hit the rest. Eight-plus fires across
    # six seats, ZERO of them a deploy request. Nothing bad happened only because six seats
    # each independently refused a false order.
    # A deploy trigger must require an EXPLICIT, UNAMBIGUOUS invocation. `#SendIt` is that.
    # Do NOT re-add a bare verb phrase here. If one is ever genuinely needed, require
    # co-occurrence with a deploy noun (prod|release|merge to main) and exclude quoted or
    # routed blocks — a matcher with no concept of intent cannot be trusted with a protocol.
    # (Found by HIKARI-DOJOV3 by reading the regex instead of theorising from a fire;
    #  independently probed by HIKARI, which ran strings THROUGH the pattern. Two
    #  differently-constructed checks, same answer.)
    #
    # OB1-INTENT-SENDIT-ANCHOR-001 (2026-07-26): ANCHORED. The previous pattern was
    # correct about WHAT counts as an invocation and had no concept of WHERE. It matched
    # the token anywhere, so it fired on every QUOTATION of itself -- and this rule's own
    # documentation, its verification tables, and every routed message about it all
    # contain the literal token. A matcher over a corpus that documents itself matches
    # its own documentation.
    # MEASURED before the fix, all three FIRED and all three are prose:
    #     '"#SendIt narrowing noted." - MEGAZORD'          (a peer's quotation)
    #     'the trigger now needs an explicit #SendIt'        (a mid-sentence mention)
    #     '`#SendIt` fires on explicit invocation ONLY'      (a routed verification row)
    # Same class HIKARI enumerated across every event:prompt rule: a numbered imperative
    # body injected on a phrase match, with no anchor to separate a declaration from a
    # discussion of one. This body is the DEPLOY PROTOCOL, so a false fire fabricates a
    # deploy order -- the failure that hit six seats on 2026-07-25.
    #
    # Now: the token must OPEN A LINE (after optional whitespace) and must NOT be opened
    # by a quote, backtick, blockquote or list marker.
    # DELIBERATE FALSE-NEGATIVE, stated so nobody 'fixes' it: 'do X then #SendIt'
    # mid-sentence will NOT fire. That tightens the contract to what the doctrine already
    # says -- #SendIt is an EXPLICIT invocation -- and it falls in the safe direction: a
    # missed fire injects no protocol, while a false fire manufactures a deploy order.
    # For a rule whose body is a deploy procedure that asymmetry is the whole design.
    #
    # VERIFIED 15/15 before commit: 9 quotation/mention/routed forms QUIET (including the
    # three above that previously fired), 6 real invocations FIRE ('#SendIt', indented,
    # with trailing text, 'deploy to prod', indented, and after a newline).
    # Falsifier, kept live: any line in this repo's own docs that fires this pattern.
    pattern: (?i)(?:^|\n)[ \t]*(?![>"'`*_-])(?:#SendIt|deploy[ \t]+to[ \t]+prod)\b
owner: shinob1
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

**DEPLOY PROTOCOL TRIGGERED (#SendIt)**

toMachina Deploy Sequence:

1. **PRE-FLIGHT:** `git status` — working tree clean?
2. **BUILD VERIFY:** `npm run build` — all workspaces pass?
3. **COMMIT:** `git add -A && git commit`
4. **BRANCH + PR:** `git push origin [branch]` then `gh pr create --title "description"`
5. **CI GATE:** Wait for CI / check to pass (required by branch protection — cannot merge without green)
6. **MERGE — PIN THE SHA:** `gh pr merge <#> --squash --match-head-commit <full-40-char-sha>`
   (merges to main → triggers deploy-api + Firebase App Hosting)
   - **`--match-head-commit` takes the FULL 40-character sha.** An abbreviated one fails with
     `Could not coerce value to GitObjectID`.
   - **Never `--auto` on a death-gated or PHI PR.** `--auto` is not sha-pinned: it lands whatever
     the head *becomes*, so it can merge content nobody signed off on (cross-warrior gotcha #41).
   - Before arming `--auto` on an ordinary `services/api` PR, confirm the `analyze` (CodeQL) check
     is green — it runs and reports but is **not** in the required set, so `--auto` does not wait
     on it (gotcha #8).
7. **DEPLOY REPORT:**

| Step | Result |
|------|--------|
| npm run build | pass/fail |
| git commit | [hash] |
| PR created | [URL] |
| CI / check | pass/fail (must pass to merge) |
| PR merged | [merge hash] |
| CI / deploy-api | pass/fail |
| Firebase App Hosting | auto-deploys on merge |

**Branch protection is ON.** Direct push to main is blocked. Must go through PR with CI green.
