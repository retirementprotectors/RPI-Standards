import sys, re, yaml
sys.path.insert(0, '/home/jdm/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify')

CO = "check" + "out"
SW = "swi" + "tch"
LIVE = "/home/jdm/Projects/_RPI_STANDARDS"
WT = LIVE + "-hikari"

rule = yaml.safe_load(open(sys.argv[1]).read().split('---')[1])
pats = [c['pattern'] for c in rule['conditions']]


def fires(cmd):
    return all(re.compile(p, re.IGNORECASE).search(cmd) for p in pats)


# ROUND 4. The balanced-span fix is correct in principle; these probe the shapes
# where "balanced" is ambiguous or where a span legitimately never closes.
# Chosen because the builder now OWNS round-3's corpus, so it can no longer
# surprise him. An apostrophe is the case: it is not a quote, but it looks like one.
CASES = [
    # --- MUST FIRE: real hazards whose quoting is irregular ---
    (f'''git -C {LIVE} commit -m "don't break it" && git {CO} main''', True,
     "APOSTROPHE in a double-quoted message before the chain op"),
    (f'''git -C {LIVE} commit -m "it's fine" ; git {SW} main''', True,
     "APOSTROPHE + semicolon"),
    (f'''git -C {LIVE} commit -m "say \\"hi\\"" && git {CO} main''', True,
     "ESCAPED double-quotes inside the message"),
    (f'''cd {LIVE} && echo "a && b" && git {CO} main''', True,
     "a chain operator INSIDE a quoted string, real op after"),
    (f'''cd $(dirname {LIVE}/x) && git {CO} main''', True,
     "command substitution before the chain op"),
    (f'''git -C {LIVE} commit -m "fix" && \\\n  git {CO} main''', True,
     "line continuation between the op and the verb"),
    (f'''cd {LIVE}\ngit {CO} main''', True,
     "newline-separated real op (line-start branch)"),
    (f'''git -C {LIVE} commit -m 'single quoted msg' && git {CO} main''', True,
     "single-quoted message before the chain op"),
    # --- MUST BE QUIET: prose whose quoting is irregular ---
    (f'''echo "don't ever cd {LIVE} && git {CO} main"''', False,
     "prose: apostrophe inside the quoted warning"),
    (f'''- the rule fires on `{LIVE}` when you && git {CO}''', False,
     "prose: bullet + backticks, operator outside the span"),
    (f'''<!-- {LIVE} && git {CO} main is forbidden -->''', False,
     "prose: html comment"),
    (f'''| {LIVE} | && git {CO} main | forbidden |''', False,
     "prose: markdown table row"),
    (f'''1. never run: cd {LIVE} && git {CO} main''', False,
     "prose: ordered list"),
]

bad = []
for cmd, want, label in CASES:
    got = fires(cmd)
    if got != want:
        bad.append((label, want, got, cmd))
    print(f'{"ok  " if got == want else "FAIL"} want={str(want):5} got={str(got):5} {label}')

print()
print(f'{len(CASES) - len(bad)}/{len(CASES)} pass')
for l, w, g, c in bad:
    kind = 'FALSE NEGATIVE (hazard escapes)' if w and not g else 'FALSE POSITIVE (prose fires)'
    print(f'  !! {kind}: {l}\n     {c!r}')
sys.exit(1 if bad else 0)
