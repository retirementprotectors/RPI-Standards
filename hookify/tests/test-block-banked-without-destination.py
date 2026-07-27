import re, sys, importlib.util
spec = importlib.util.spec_from_file_location('d', '/home/jdm/.claude/hooks/hookify-stop-dispatch.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
r = d.parse_rule('/home/jdm/Projects/_RPI_STANDARDS/hookify/hookify.block-banked-without-destination.local.md')
print('parsed:', r.get('name'), '| enabled:', r.get('enabled'), '| action:', r.get('action'), '| conds:', len(r['conditions']))

def fires(ans):
    conds = [c for c in r['conditions'] if c.get('field') in ('last_assistant_message','final_message','content')]
    def ok(c):
        op, pat = c.get('operator'), c.get('pattern')
        if not pat: return False
        if op == 'regex_match': return bool(re.search(pat, ans, re.IGNORECASE))
        if op in ('regex_not_match','not_regex_match'): return not re.search(pat, ans, re.IGNORECASE)
        return False
    return all(ok(c) for c in conds)

MUST_FIRE = [
    ("JDM ex: he banked them", "Pulling the exact 4 commands from MEGAZORD (he banked them)."),
    ("JDM ex: banking the trap", "Plus 2689 — banking the trap that caused all this."),
    ("JDM ex: all banking", "Three things, all banking, none of them risky."),
    ("banked gotcha", "Good catch — banked gotcha for the fleet."),
    ("banking the lesson", "Banking the lesson so it does not happen twice."),
    ("bare 'Banked.'", "Banked."),
    ("I'll bank it", "Good catch — I'll bank it and move on to the next thing."),
    ("banking it, no target", "Noted. Banking it. Now continuing with the deploy."),
    ("shelved for later", "That's a real finding but I'm shelving it for later, focusing on the merge."),
    ("added to backlog, vague", "Understood — added to the backlog. Moving on."),
]
MUST_NOT_FIRE = [
    ("CARRIER: bankers fidelity", "Pulled the Bankers Fidelity rate sheet and reconciled 40 rows."),
    ("SCHEMA: bank_managed", "The bank_managed flag is false on 3,582 accounts; bank manages the rest."),
    ("CLIENT DATA: bank account", "Client provided bank account and routing information for the draft."),
    ("bankrupt", "The carrier went bankrupt in 2019 so those policies moved."),
    ("MY OWN FP — analysis of the pattern", "bank used as a VERB 1,865 after excluding finance vocabulary. names a destination 1,126, NO destination 739 violations. Real n-grams: banked above, banked as a, banking the lesson, he banked them. by lane shinob1 249. I re-measured across the corpus."),
    ("banked WITH ticket id", "Banked it as TRK-14798 with the repro attached."),
    ("banked to disk (state)", "Now taking the freshness refresh — first banking this seat's delta to disk."),
    ("banked to a path", "Banked it to /home/jdm/inbox/findings.html so it renders."),
    ("banked w/ PR", "I'll bank it on PR #2688 as a follow-up comment."),
    ("banked into firestore", "Banking that into tracker_items rather than forwarding noise."),
    ("critique of banking", "'Banking it' is a hub post that scrolls away — that's the whole problem."),
    ("this rule itself", "Wrote block-banked-without-destination; it fires on 'I'll bank it' with no target."),
    ("normal work, no bank", "Merged #2690 and verified it on origin/main."),
]
bad = 0
print('\nMUST FIRE:')
for n_, t in MUST_FIRE:
    f = fires(t); print(f"  {'PASS' if f else 'MISS'}  {n_}")
    bad += 0 if f else 1
print('\nMUST NOT FIRE:')
for n_, t in MUST_NOT_FIRE:
    f = fires(t); print(f"  {'PASS' if not f else 'FALSE POSITIVE'}  {n_}")
    bad += 1 if f else 0
print(f"\n{'ALL CLEAR' if bad==0 else str(bad)+' PROBLEM(S)'}")
