#!/usr/bin/env python3
"""Evaluate hookify.warn-unretired-writeback-loop.local.md's conditions against a
file's content, replicating the engine's AND-of-conditions / field=content semantics
(https://.../hookify writing-rules skill: regex_match = re.search, not_contains = substring
absent). Standalone verification harness — no live tool-call side effects.
"""
import re
import sys

CONDITIONS = [
    ("regex_match", r"\bload\b[\s\S]{0,80}--replace\b|--replace\b[\s\S]{0,80}\bload\b"),
    ("regex_match", r"setInterval\s*\(|while\s*\(\s*true\s*\)|while\s+true\b|while:\s*true|cron\.schedule\("),
    ("not_contains", "RETIREMENT_CHECK"),
    ("not_contains", "LIVENESS_CHECK"),
]


def evaluate(content):
    for op, pattern in CONDITIONS:
        if op == "regex_match":
            if not re.search(pattern, content):
                return False, f"regex_match FAILED: {pattern!r}"
        elif op == "not_contains":
            if pattern in content:
                return False, f"not_contains FAILED (found {pattern!r} — clears the warn)"
    return True, "all 4 conditions matched"


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, "r") as f:
            content = f.read()
        fires, detail = evaluate(content)
        verdict = "WARN FIRES" if fires else "clean (no warn)"
        print(f"{path}: {verdict}  ({detail})")
