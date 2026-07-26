"""Fire the new gate against real corpus text — the actual quotes JDM pasted,
plus legitimate refusals that MUST NOT trip it."""
import re, sys, os
sys.path.insert(0, '/home/jdm/.claude/hooks')
import importlib.util
spec = importlib.util.spec_from_file_location('d', '/home/jdm/.claude/hooks/hookify-stop-dispatch.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

r = d.parse_rule('/home/jdm/Projects/_RPI_STANDARDS/hookify/hookify.block-hour-as-excuse.local.md')
print('parsed:', r.get('name'), '| event:', r.get('event'), '| enabled:', r.get('enabled'),
      '| conditions:', len(r['conditions']))

def fires(ans):
    conds = [c for c in r['conditions'] if c.get('field') in ('last_assistant_message', 'final_message', 'content')]
    def ok(c):
        op, pat = c.get('operator'), c.get('pattern')
        if not pat: return False
        if op == 'regex_match': return bool(re.search(pat, ans, re.IGNORECASE))
        if op in ('regex_not_match', 'not_regex_match'): return not re.search(pat, ans, re.IGNORECASE)
        return False
    return all(ok(c) for c in conds)

MUST_FIRE = [
    ("HIKARI 17:21 (real)", "Or I build the write path — but not tonight, and not by me at this hour."),
    ("HIKARI 17:21 (real)", "Building one right now, at the end of a very long session, is exactly the mistake I've spent the day telling other people not to make."),
    ("SHINOB1 23:31 (real)", "That's product math, VOLTRON's lane, and I'm not guessing at your annuity illustrations at midnight."),
    ("JDM's paraphrase", "I'm not doing that thing, it's too late at night to be fucking with the vault config."),
    ("banned 05:12 form", "A BAA signed now does not reach backward — that part is still yours to rule on, and it is not a tonight decision."),
    ("softened form", "I'd rather not flip that until the morning when you're fresh."),
    ("daylight form", "That's a daylight call, not a midnight one."),
]

MUST_NOT_FIRE = [
    ("real risk refusal", "I will not merge to main on a guess — that's the exact thing that's been burning you."),
    ("real risk refusal", "I will not touch the live PHI drive without your eyes on the IAM grant. Blast radius is the reason."),
    ("did the work", "Landed and verified live: exit ok, 0 replayed. I'll run the sweep again in the morning to confirm it holds."),
    ("self-audit", "THE HEDGE SWEEP, measured not recalled: 17 banned forms — 'not a tonight decision', 'in the morning', 'daylight'."),
    ("this rule itself", "Wrote block-hour-as-excuse; it fires on 'at this hour' and 'not tonight' patterns."),
    ("plain schedule report", "The timer is set for 06:00 UTC daily, so the page regenerates in the morning."),
    ("MY OWN FP — describing the gate", "Gate is live right now. Fires only when both are true: the turn declines work and the reason given is the clock or fatigue. Refusing on risk does not trip it. I will not merge on a guess stays clean, that is true at 9am too. The test: would this still be the right call at 9am on a Tuesday? It also catches the evasion: your ban got dodged by characterizing the work instead of refusing it, is a daylight call, is exactly the mistake. Tested 13/13. git push denied twice. Everything else from tonight is landed."),
    ("warrior retro quoting a form", "In my retro I found I said it is not a tonight decision twice. Both dropped."),
]

bad = 0
print('\nMUST FIRE:')
for name, t in MUST_FIRE:
    f = fires(t)
    print(f"  {'PASS' if f else 'MISS'}  {name}")
    if not f: bad += 1
print('\nMUST NOT FIRE (false-positive check):')
for name, t in MUST_NOT_FIRE:
    f = fires(t)
    print(f"  {'PASS' if not f else 'FALSE POSITIVE'}  {name}")
    if f: bad += 1
print(f"\n{'ALL CLEAR' if bad == 0 else str(bad) + ' PROBLEM(S)'}")
