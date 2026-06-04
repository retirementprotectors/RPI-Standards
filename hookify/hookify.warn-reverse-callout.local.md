---
name: warn-reverse-callout
enabled: true
event: file
action: warn
# JDM directive 2026-06-02: "strike dead the ridiculous concept of reverse-call-outs."
# The anti-pattern: ANNOUNCING what you are excluding / omitting / declining to mention —
# which re-surfaces the exact thing you were told to remove. SILENT EXCLUSION is the rule.
# WARN (not block): semantic pattern with false-positive risk on legit "excluded from total"
# data/code usage; surfaces every time so the behavior corrects. Exempts hookify + doctrine
# files that necessarily quote the anti-pattern as examples.
conditions:
  - field: content
    operator: regex_match
    pattern: excluded\s+(here|from\s+(view|this))|(\bis|\bare|\band)\s+excluded\b[^.]{0,25}\bhere\b|\bnot\s+(going\s+to\s+)?(mention|name|us|includ|referenc)\w*[^.]{0,30}\b(here|in\s+this)|per\s+[^.]{0,30}\b(rule|instruction|directive)\b[^.]{0,30}\b(not|never|exclud|omit)|(omitted|redacted|left\s+out)\b[^.]{0,20}\b(here|as\s+(instructed|directed|requested|noted))
  - field: file_path
    operator: not_contains
    pattern: hookify
  - field: file_path
    operator: not_contains
    pattern: CLAUDE.md
  - field: file_path
    operator: not_contains
    pattern: memory
owner: shinob1
---

**SILENT EXCLUSION — no reverse call-outs.**

You are *announcing* something you are excluding, omitting, or declining to mention.
That re-surfaces the exact thing you were told to remove — the failure JDM battles
daily ("I told you not to talk about it, so here I am pointing out that I'm not").

**The rule:** when you exclude / redact / omit / decline, the output SIMPLY DOES NOT
CONTAIN IT — and does not reference the removal. No "X ... excluded." No "I'm not
mentioning Y." No "per the rule, not Z." No footnote about what was left out.

If a reader genuinely needs a correction noted, state the neutral corrected fact once.
Never a self-referential pointer at what you are not saying.
