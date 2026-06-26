---
name: block-done-without-live-verify
enabled: true
event: file
action: block
owner: shinob1
introduced: 2026-06-26
reviewed: 2026-06-26 SHINOB1 A6 — FP-fixed + activated. Dropped the 'shipped_refs:' trigger (a PR-convention LABEL present in 21 files + 7 briefs = the FP). Now fires only on a genuine status FLIP to a live-state, excluding doc/brief/changelog contexts where 'status: shipped' is history, not a fresh claim. NOTE: this file-write gate is the LIGHT tripwire; the real build!=live wall is the death-gate live_verify requirement (Phase 1).
conditions:
  - field: content
    operator: regex_match
    pattern: status:\s*(shipped|live)\b
  - field: content
    operator: not_contains
    pattern: live_verify
  - field: file_path
    operator: not_contains
    pattern: hookify
  - field: file_path
    operator: not_contains
    pattern: /docs/
  - field: file_path
    operator: not_contains
    pattern: /briefs/
  - field: file_path
    operator: not_contains
    pattern: changelog
---

NOPE — that's build-verified, not live-verified. Run /qa-verify and paste the live_verify block first. → docs/strategy/disco-verification-layer-and-doctrine-consolidation.md
