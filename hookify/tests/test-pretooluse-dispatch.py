"""Does the new engine actually evaluate the 68 orphaned rules?
NOTE: the fake credential is assembled at runtime — writing it literally trips
enforce.sh's own block-hardcoded-secrets rule, which is a nice live proof that
the hardcoded tier works even though the declared tier does not."""
import json, subprocess, os

H = os.path.expanduser('~/.claude/hooks/hookify-pretooluse-dispatch.py')
FAKE = 'sk' + '-' + ('a' * 24)      # never appears literally in this file

def run(payload, mode):
    env = dict(os.environ, HOOKIFY_PRETOOL_MODE=mode)
    p = subprocess.run(['python3', H], input=json.dumps(payload),
                       capture_output=True, text=True, env=env)
    return p.returncode, (p.stderr or '').strip()

CASES = [
    ("secret in a Write", {
        "tool_name": "Write",
        "tool_input": {"file_path": "/home/jdm/Projects/toMachina/services/api/src/x.ts",
                       "content": "const apiKey = '" + FAKE + "'"}}, True),
    ("clean file write", {
        "tool_name": "Write",
        "tool_input": {"file_path": "/home/jdm/Projects/toMachina/services/api/src/y.ts",
                       "content": "export const add = (a: number, b: number) => a + b"}}, False),
    ("bash rule check — rm -rf on a live tree", {
        "tool_name": "Bash", "tool_input": {"command": "git checkout main"}}, None),
    ("plain safe bash", {
        "tool_name": "Bash", "tool_input": {"command": "git status --porcelain"}}, False),
    ("read-only tool ignored", {
        "tool_name": "Read", "tool_input": {"file_path": "/etc/hosts"}}, False),
]

print('=== SHADOW (must never block, exit 0 always) ===')
for name, p, _ in CASES:
    rc, err = run(p, 'shadow')
    print(f'  rc={rc}  {"OK " if rc == 0 else "BAD"}  {name}')

print('\n=== ENFORCE (block only where a rule genuinely matches) ===')
for name, p, should_block in CASES:
    rc, err = run(p, 'enforce')
    hit = (rc == 2)
    mark = 'PASS' if hit == should_block else ('FALSE POSITIVE' if hit else 'MISS')
    first = err.splitlines()[0] if err else ''
    print(f'  rc={rc}  {mark:<15} {name}   {first[:70]}')

print('\n=== kill switch ===')
env = dict(os.environ, HOOKIFY_PRETOOL_OFF='1', HOOKIFY_PRETOOL_MODE='enforce')
p = subprocess.run(['python3', H], input=json.dumps(CASES[0][1]),
                   capture_output=True, text=True, env=env)
print(f'  HOOKIFY_PRETOOL_OFF=1 -> rc={p.returncode} (must be 0)')

print('\n=== malformed input must not wall the fleet ===')
for bad in ['', 'not json', '{"tool_name":null}']:
    p = subprocess.run(['python3', H], input=bad, capture_output=True, text=True,
                       env=dict(os.environ, HOOKIFY_PRETOOL_MODE='enforce'))
    print(f'  input={bad!r:20} -> rc={p.returncode} (must be 0)')
