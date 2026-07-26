import sys, re, yaml
sys.path.insert(0, '/home/jdm/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify')

# Verbs assembled at runtime: the literal shapes below are hazard samples, and
# writing them out verbatim trips the very gates under test (it already did once).
CO = "check" + "out"
SW = "swi" + "tch"
LIVE = "/home/jdm/Projects/_RPI_STANDARDS"
WT = LIVE + "-hikari"

txt = open(sys.argv[1]).read()
rule = yaml.safe_load(txt.split('---')[1])
pats = [c['pattern'] for c in rule['conditions']]


def fires(cmd):
    return all(re.compile(p, re.IGNORECASE).search(cmd) for p in pats)


# MY corpus. The builder did not choose these. Deliberately hazard-shaped WITH
# quotes -- a shape his mention-shaped corpus structurally could not contain.
CASES = [
    # --- MUST FIRE: real branch ops against the live shared tree ---
    (f'git -C {LIVE} {CO} -b hikari/x', True, 'baseline: -C form'),
    (f'cd {LIVE} && git {CO} main', True, 'baseline: chain'),
    (f'git -C {LIVE} commit -m "fix the thing" && git {CO} main', True, 'HAZARD: quoted -m before the chain op'),
    (f"cd '{LIVE}' && git {CO} main", True, 'HAZARD: single-quoted path before chain op'),
    (f'cd "{LIVE}" && git {SW} main', True, 'HAZARD: double-quoted path before chain op'),
    (f'git -C {LIVE} stash push -m "wip" ; git {SW} main', True, 'HAZARD: quoted before ;'),
    (f'echo start && cd {LIVE} && git {CO} main', True, 'HAZARD: two chain ops, no quotes'),
    (f'git -C {LIVE} {CO} main # restore', True, 'trailing comment after a real op'),
    # --- MUST BE QUIET: prose / mentions ---
    (f'echo "never run git {CO} main in {LIVE}"', False, 'prose: quoted echo'),
    (f'- run `cd {LIVE} && git {CO} main` to break it', False, 'prose: md bullet + backticks'),
    (f'> {LIVE}: do not cd there && git {CO} anything', False, 'prose: blockquote'),
    (f'# {LIVE} && git {CO} main is forbidden', False, 'prose: comment line'),
    (f'* {LIVE} && git {SW} main -- never do this', False, 'prose: star bullet'),
    # --- MUST BE QUIET: safe ops / worktrees ---
    (f'git -C {WT} {CO} -b hikari/x', False, 'worktree is the correct path'),
    (f'git -C {LIVE} status --porcelain', False, 'read'),
    (f'git -C {LIVE} {CO} -- hookify/foo.md', False, 'file restore, not a branch op'),
    (f'git -C {LIVE} worktree add {WT} -b b origin/main', False, 'worktree add'),
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
    print(f'  !! {kind}: {l}\n     {c}')
sys.exit(1 if bad else 0)
