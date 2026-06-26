---
name: warn-early-conclusion
enabled: true
event: file
action: warn
owner: ronin
introduced: 2026-06-26
status: PENDING_SHINOB1_REVIEW
conditions:
  - field: content
    operator: regex_match
    pattern: \b(it'?s|this\s+is)\s+(definitely\s+|clearly\s+|obviously\s+|must\s+be\s+)?(a\s+)?(iOS|Android|mobile|Safari|Chrome|browser.specific|cach(e|ing)|flak(e|y)|network\s+issue|timing\s+(issue|problem)|race\s+condition|prod(uction)?\s+(issue|bug|problem)|CDN\s+issue)
  - field: content
    operator: not_contains
    pattern: https://
  - field: file_path
    operator: not_contains
    pattern: hookify
---

⚠ That's a diagnosis, not an observation. What did you READ/RUN to know this? Cite the evidence (url / log / shot) or soften to a hypothesis.
