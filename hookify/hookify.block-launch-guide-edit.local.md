---
name: block-launch-guide-edit
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)warrior-launch-guide\.html$
---

🛑 **BLOCKED: Direct edit of `warrior-launch-guide.html`**

The Warrior Launch Guide is a high-traffic operational doc — every team member uses it to onboard, recover sessions, and understand sub-warrior patterns. Silent edits create real risk:

- Stub sections silently going stale (Section 5 "Infinite Ronin" was stale 8+ days when audited 2026-05-11)
- Channel routing drift between body content and JS `CHANNEL_BLOCK`
- Variant table conflations (recurring roles vs one-shot specialty spawns)
- Boot prompt drift across the 7 warrior identity strings (lines 899–905)

**Preferred path:**
- Open a Discovery Doc OR drop a TRK ticket in RONIN's queue
- RONIN ships HTML edits as PRs with browser-render verification

The disco for current launch-guide gaps already merged: `docs/discoveries/zrd-launchguide-gaps-2026-05-11.html` → RONIN sprint `LGG-2026-05-11`.

**Override (legitimate direct edit — urgent fix, typo, broken link, doctrine-clause update like 2026-05-19):**
- The launch guide IS the right place to update boot-prompt doctrine (today's pivot clause + DOJO_STATE pointer was a textbook example). When the edit IS the right move, the override path is: add a marker comment immediately before the edit-target line: `<!-- launch-guide-edit-justified: <ticket-or-reason> -->`
- Or, when editing programmatically (e.g. a `replace_all` that targets a specific unique substring), the regex still fires per-file — but the edit happens in one tool call, then a Slack land-it surfaces the change to the team via `#shinob1` or `#musashi`.

**Why BLOCK, not WARN:** the WARN was invisible AND the path regex was wrong (`docs/warrior-launch-guide.html$` — but the canonical file is at repo root, so it never fired). This BLOCK upgrade fixes both: visibility + correct path.

Why this exists: ZRD-SHINOB1-AUDIT-POSTURE-001 + 2026-05-11 launch-guide-gaps audit. Path-regex bug-fix bundled in this upgrade.
