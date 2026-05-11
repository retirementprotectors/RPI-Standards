---
name: warn-launch-guide-edit
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/warrior-launch-guide\.html$
---

**WARNING: Direct edit of `warrior-launch-guide.html`**

The Warrior Launch Guide is a high-traffic operational doc — every team
member uses it to onboard, recover sessions, and understand sub-warrior
patterns. Silent edits create risk:

- Stub sections (Section 5 "Infinite Ronin" was stale 8+ days when audited 2026-05-11)
- Channel routing drift between body content and JS `CHANNEL_BLOCK`
- Variant table conflations (recurring roles vs one-shot specialty spawns)

**Preferred path:** Open a Discovery Doc OR drop a TRK ticket in RONIN's
queue. RONIN ships HTML edits as PRs with browser-render verification.

The disco for current launch-guide gaps is already merged:
`docs/discoveries/zrd-launchguide-gaps-2026-05-11.html` → RONIN sprint
`LGG-2026-05-11`.

**If your edit is the right move (urgent fix, typo, broken link):** ignore
this warning and proceed. Hookify warns, doesn't block.

Why this exists: ZRD-SHINOB1-AUDIT-POSTURE-001 + 2026-05-11 launch-guide-gaps audit.
