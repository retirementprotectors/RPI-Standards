import sys, re, yaml
CO="check"+"out"; LIVE="/home/jdm/Projects/_RPI_STANDARDS"
rule=yaml.safe_load(open(sys.argv[1]).read().split('---')[1])
pats=[c['pattern'] for c in rule['conditions']]
f=lambda c: all(re.compile(p,re.IGNORECASE).search(c) for p in pats)
CASES=[
 (f'''git -C {LIVE} commit -m 'he said "go" now' && git {CO} main''', True, 'MIRROR: double-quote inside a SINGLE-quoted span'),
 (f'''git -C {LIVE} commit -m 'a "b" c' ; git {CO} main''', True, 'MIRROR: same, semicolon'),
 (f'''echo 'never run git {CO} main in {LIVE}' ''', False, 'MIRROR prose: single-quoted warning'),
 (f'''git -C {LIVE} commit -m "path is `pwd`" && git {CO} main''', True, 'backtick span inside double quotes'),
]
bad=[]
for c,w,l in CASES:
    g=f(c); bad += [] if g==w else [(l,w,g,c)]
    print(f'{"ok  " if g==w else "FAIL"} want={str(w):5} got={str(g):5} {l}')
print()
for l,w,g,c in bad:
    print(f'  !! {"FALSE NEGATIVE" if w else "FALSE POSITIVE"}: {l}\n     {c!r}')
print(f'{len(CASES)-len(bad)}/{len(CASES)} pass')
