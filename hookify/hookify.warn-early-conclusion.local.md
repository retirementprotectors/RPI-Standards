---
name: warn-early-conclusion
enabled: true
event: file
action: warn
owner: ronin
introduced: 2026-06-26
reviewed: 2026-07-07 SHINOB1 — closed out. Flipped enabled:true 2026-06-26 (GV2-WALL-FLIP-001, #42) under JDM's go, alongside the A6 FP-fix pass on block-done-without-live-verify + block-checkout-in-live-deploy-tree, but this rule's own frontmatter never got its closing review note. No matcher change needed: conditions already exclude hookify/*.local.md self-writes and any content citing a https:// evidence link, matching the P0 intent (catch confident diagnosis without evidence). Reviewed against live firing behavior per OB1-GV2-REBASELINE-001 (WS-B gap ledger) — ratifying as active, no further FP tuning required at this time.
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
