#!/usr/bin/env python3
# Detector for check_respond_where_received.sh (RULE #1 enforcement).
# Reads the Claude Code transcript JSONL on stdin. Prints "VIOLATION\t<snippet>"
# iff the MOST RECENT genuine JDM directive (a user-role message whose TEXT
# starts with the dispatcher tag) was NOT followed by an
# mcp__slack__slack_post_message in the response. Otherwise prints nothing.
#
# Cross-warrior tmux traffic is invisible here — only JDM directives are judged.
# SHINOB1-RULE1-ENFORCE-001 · owner: shinob1 · 2026-06-12
import sys, json

MARK = "Incoming from U09BBHTN8F2"

def role(o):
    return o.get("type")

def text_only(o):
    m = o.get("message", o)
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""

def has_slack_post(o):
    m = o.get("message", o)
    c = m.get("content")
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "tool_use" \
               and b.get("name") == "mcp__slack__slack_post_message":
                return True
    return False

def is_directive(o):
    if role(o) != "user":
        return False
    for ln in text_only(o).splitlines():
        if ln.lstrip("# ").startswith(MARK):
            return True
    return False

def main():
    msgs = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except Exception:
            continue
    dir_idxs = [i for i, o in enumerate(msgs) if is_directive(o)]
    if not dir_idxs:
        return
    i = dir_idxs[-1]  # judge only the most-recent (just-closed) directive turn
    posted = any(role(msgs[j]) == "assistant" and has_slack_post(msgs[j])
                 for j in range(i + 1, len(msgs)))
    if not posted:
        snip = text_only(msgs[i]).strip().replace("\n", " ")[:80]
        sys.stdout.write("VIOLATION\t" + snip)

if __name__ == "__main__":
    main()
