---
name: block-alert-confirm-prompt
enabled: true
event: file
action: block
conditions:
  # TRK-HOOK-207 (2026-07-30, ronin). The pattern was `(alert|confirm|prompt)\s*\(` with NO file_path
  # condition. Three independent defects in one line:
  #
  #   1. `\s` MATCHES NEWLINES in Python. A plain-text line ending in one of the three trigger
  #      words, followed by any line beginning with an open paren, was a hard block.
  #   2. `\s*` matches ZERO characters, so the ordinary English plural of the third trigger
  #      word — the word followed immediately by a parenthesised "s" — is a direct hit.
  #   3. NO file_path condition. `field: content` alone means it inspected EVERY file write on
  #      the box, so the population most exposed was whoever writes prose: status reports,
  #      discovery docs, and rule files describing this very rule.
  #
  # It blocked three seats' status reports on 2026-07-30, and it blocked an edit belonging to a
  # DIFFERENT ticket in this same phase whose only offence was prose naming a dispatcher field
  # ahead of a line reference. Documentation of a hazard contains the hazard verbatim, which
  # makes the report ABOUT a rule the likeliest false-fire shape — and the one nobody puts in a
  # fixture. This very file could not be edited through the Write/Edit tools while the old
  # pattern stood; the repair had to be applied by a route the tool-argument matcher cannot see,
  # which is TRK-HOOK-208's L2 ceiling, hit from inside 207.
  #
  # THE ENGINE COMPILES WITH re.IGNORECASE (rule_engine.py:24), so every pattern here is
  # case-insensitive whether or not it looks it. Camel-cased identifiers ending in the second
  # trigger word do not match, because the character before the keyword must be a non-word,
  # non-dot character.
  #
  # Scoped to the file types where a browser dialog API can actually exist. This is the same
  # scoping enforce.sh's OWN copy of this rule has always had (`\.(gs|js|ts|html)$`) — the shell
  # twin was the safer implementation all along, and only the hookify copy inspected every file.
  - field: file_path
    operator: regex_match
    pattern: \.(gs|js|jsx|mjs|cjs|ts|tsx|html|htm)$
  # `(?m)^` anchors every attempt to a line start, so no match can span a newline. The negative
  # lookahead drops lines whose first non-space character marks a comment or prose — a real
  # instance already exists in apps/prodash, a JSX comment that names the second trigger word to
  # say it is NOT used. `[^\w.]` before the keyword keeps method calls and camelCase out, while
  # the window-qualified form stays in via its own alternative.
  - field: content
    operator: regex_match
    pattern: (?m)^(?![ \t]*(?://|\*|/\*|\{/\*|<!--|#|>|\||-|`|'|"))(?:[^\n]*[^\w.])?(?:window\.)?(?:alert|confirm|prompt)[ \t]*\(
owner: shinob1
---

**BLOCKED: Browser Dialog API Detected**

Do not use browser dialog APIs. They block the UI thread and provide no branding control.

**Instead use:**
- `showToast('Message', 'success')` for notifications
- `await showConfirmation({...})` for confirmations
- Custom modal components for complex inputs
