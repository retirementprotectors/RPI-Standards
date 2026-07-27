#!/usr/bin/env python3
"""hookify-pretooluse-dispatch.py — OB1-HOOKIFY-NO-ENGINE-001

THE BUG THIS FIXES
------------------
Measured 2026-07-26 against violation-log.jsonl (45,191 rows since April):
  - ZERO of the 103 declared hookify rules had EVER produced a block.
  - All 247 real blocks came from 6 scope-bound rules + 5 hardcoded checks in
    enforce.sh.
  - enforce.sh — the only PreToolUse engine — walks ONLY hookify/scope-bound/.
    The 103 top-level hookify/*.local.md rules are read by:
        event: stop    -> hookify-stop-dispatch.py    (text injection only)
        event: prompt  -> hookify-prompt-dispatch.py  (text injection only)
        event: file    -> NOBODY   (50 enabled rules)
        event: bash    -> NOBODY   (18 enabled rules)

So 68 of 82 enabled rules had no engine at all. `action: block` could not block
because nothing was reading the rule. The reference page meanwhile advertised
"~73 Live-firing" — a count of rules LOADED, not rules that ever fired.

This dispatcher is the missing engine for event: file and event: bash.

SHADOW MODE BY DEFAULT — READ THIS BEFORE ARMING
------------------------------------------------
68 rules have never once been evaluated against live traffic. Arming them all at
the same instant would be reckless: any single over-broad regex would wall the
entire fleet out of Write/Edit/Bash, and the recovery move under pressure is to
disable everything — which is exactly how 21 rules went dark in
SHIN-FRICTION-LAND-001 and why the ones that worked hardest got switched off.

So: HOOKIFY_PRETOOL_MODE=shadow (default) evaluates every rule and LOGS what it
WOULD have done, changing nothing. Run it for a real workday, read the false
positives out of the log, fix them, and only then set MODE=enforce.

Shipping this armed would be the same confident-but-unverified move that caused
every incident in this log.

  HOOKIFY_PRETOOL_MODE=shadow   (default) log only, never block
  HOOKIFY_PRETOOL_MODE=warn     emit warnings on stderr, never block
  HOOKIFY_PRETOOL_MODE=enforce  action: block => exit 2 (real block)
  HOOKIFY_PRETOOL_OFF=1         kill switch, full bypass

Exit 0 = allow. Exit 2 = block (Claude Code convention, matches enforce.sh).
Never throws: a dispatcher crash must not wall the fleet, so every failure path
falls through to allow.
"""
import os
import re
import sys
import json
import glob
import datetime

RULES_DIR = os.path.expanduser("~/Projects/_RPI_STANDARDS/hookify")
LOG = os.path.expanduser("~/.claude/hooks/violation-log.jsonl")
MODE = os.environ.get("HOOKIFY_PRETOOL_MODE", "shadow").lower()

FILE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
BASH_TOOLS = {"Bash"}


def log(rule, tool, detail):
    try:
        rec = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "rule": rule, "tool": tool, "detail": detail,
            "hook": "hookify-pretooluse-dispatch",
        }
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        pass


def parse_rule(path):
    """Frontmatter parser matching hookify-stop-dispatch.py's shape."""
    try:
        txt = open(path, errors="replace").read()
    except Exception:
        return None
    if not txt.startswith("---"):
        return None
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None
    fm, body = parts[1], parts[2].strip()
    r = {"conditions": [], "body": body, "path": path}
    cur = None
    for raw in fm.splitlines():
        s = raw.strip()
        if s.startswith("#") or not s:
            continue
        if s.startswith("- field:"):
            cur = {"field": s.split(":", 1)[1].strip()}
            r["conditions"].append(cur)
        elif cur is not None and s.startswith("operator:"):
            cur["operator"] = s.split(":", 1)[1].strip()
        elif cur is not None and s.startswith("pattern:"):
            p = s.split(":", 1)[1].strip()
            if len(p) >= 2 and p[0] == p[-1] and p[0] in "\"'":
                p = p[1:-1]
            cur["pattern"] = p
        elif ":" in s and not s.startswith("-"):
            k, v = s.split(":", 1)
            if k.strip() in ("name", "event", "enabled", "action", "owner"):
                r[k.strip()] = v.strip()
    return r


def check(cond, values):
    """values: dict of field -> string. Unknown field/operator => NOT satisfied
    (fails safe: a rule we cannot evaluate never fires)."""
    f = cond.get("field")
    op = cond.get("operator")
    pat = cond.get("pattern")
    if f not in values or pat is None:
        return False
    v = values[f] or ""
    try:
        if op == "regex_match":
            return bool(re.search(pat, v, re.IGNORECASE))
        if op in ("regex_not_match", "not_regex_match"):
            return not re.search(pat, v, re.IGNORECASE)
        if op == "contains":
            return pat.lower() in v.lower()
        if op == "not_contains":
            return pat.lower() not in v.lower()
        if op == "equals":
            return v.strip() == pat.strip()
    except re.error:
        return False
    return False


def main():
    if os.environ.get("HOOKIFY_PRETOOL_OFF") == "1":
        return 0
    try:
        raw = sys.stdin.read()
        inp = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    tool = inp.get("tool_name") or ""
    ti = inp.get("tool_input") or {}
    if not tool:
        return 0

    if tool in FILE_TOOLS:
        event = "file"
        values = {
            "content": str(ti.get("content") or ti.get("new_string")
                           or ti.get("new_text") or ""),
            "new_text": str(ti.get("new_string") or ti.get("new_text") or ""),
            "file_path": str(ti.get("file_path") or ti.get("notebook_path") or ""),
            "path": str(ti.get("file_path") or ""),
            "tool": tool,
        }
    elif tool in BASH_TOOLS:
        event = "bash"
        values = {"command": str(ti.get("command") or ""), "tool": tool}
    else:
        return 0

    # never police the rule files themselves, or this log
    fp = values.get("file_path", "")
    if "hookify" in fp or "violation-log" in fp:
        return 0

    blocked, warned = [], []
    for path in sorted(glob.glob(os.path.join(RULES_DIR, "hookify.*.local.md"))):
        r = parse_rule(path)
        if not r or r.get("enabled") != "true" or r.get("event") != event:
            continue
        conds = r.get("conditions") or []
        if not conds:
            continue
        try:
            if not all(check(c, values) for c in conds):
                continue
        except Exception:
            continue
        name = r.get("name", os.path.basename(path))
        target = fp or values.get("command", "")[:120]
        if r.get("action") == "block":
            blocked.append((name, r["body"]))
            log(f"{name}::{'block' if MODE == 'enforce' else 'shadow-block'}",
                tool, f"{'blocked-on-' if MODE == 'enforce' else 'wouldblock-'}{event}:{target}")
        else:
            warned.append((name, r["body"]))
            log(f"{name}::{'warn' if MODE in ('warn', 'enforce') else 'shadow-warn'}",
                tool, target)

    if MODE == "shadow":
        return 0  # measure only — change nothing

    out = []
    for n, b in warned:
        out.append(f"⚠ [{n}]\n{b}")
    for n, b in blocked:
        out.append(f"⛔ [{n}]\n{b}")
    if out:
        sys.stderr.write("\n\n".join(out) + "\n")
    if blocked and MODE == "enforce":
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)   # a broken dispatcher must never wall the fleet
