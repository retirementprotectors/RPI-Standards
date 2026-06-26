---
name: block-done-without-live-verify
enabled: false
event: file
action: block
owner: ronin
introduced: 2026-06-26
status: PENDING_SHINOB1_REVIEW
conditions:
  - field: content
    operator: regex_match
    pattern: shipped_refs:|status:\s*shipped
  - field: content
    operator: not_contains
    pattern: live_verify
  - field: file_path
    operator: not_contains
    pattern: hookify
---

NOPE — that's build-verified, not live-verified. Run /qa-verify and paste the live_verify block first. → docs/strategy/disco-verification-layer-and-doctrine-consolidation.md
