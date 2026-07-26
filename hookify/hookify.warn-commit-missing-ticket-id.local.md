---
name: warn-commit-missing-ticket-id
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: '(?:^|[;&|]\s*|\n)\s*git\s+commit\b(?!.*(?:--amend|--allow-empty|\[no-ticket\]))'
# NOTE: the `exclude:` block this rule used to carry was DELETED, not moved — the engine has
# no `exclude` field (core/config_loader.py Rule model: name/enabled/event/pattern/conditions/
# action/tool_matcher/message). It was parsed into nothing and silently dropped, so both
# documented escape hatches (--allow-empty, [no-ticket]) fired anyway. Verified by test, not
# by reading. Exclusions are now negative lookaheads inside the pattern, where they execute.
# The leading `(?:^|[;&|]\s*|\n)` anchors the match to a COMMAND POSITION so the rule cannot
# fire on the words "git commit" quoted inside other text — the same prose-substring
# false-fire class as block-opus-subagent / block-alert-confirm-prompt.
owner: shinob1
# ACTIVATED 2026-07-26 (megazord · MZ-ACTIVATE-DEAD-RULES-001). Written 2026-06-25 and
# never once loaded: the filename lacked the `hookify.` prefix that every engine globs
# for, so `enabled: false` was moot — it could not have fired even flipped to true.
# Renamed AND enabled together; either alone leaves it dead.
# Posture stays WARN (per "Status" below): a false alarm on a docs-only commit costs a
# line of injected text, a miss costs a ticket its audit credit. Escape hatches
# ([no-ticket], --allow-empty) are already in `exclude`.
---

**COMMIT GATE: Missing ticket-ID in commit subject**

Every commit subject must follow the cross-warrior format:

```
<warrior>(<ticket-id>): <description>
```

**Valid examples:**
```
taiko(TAIKO-GSM-002): mount Voice API Key + TwiML App from GSM
megazord(VCV-002): mount VAULT_ENCRYPTION_KEY from GSM on tm-api
ronin(MFP-504): RPI Roles scenarios for comp-calc
musashi(MFP-801): Medicare Planning Guide PDF layout
shinob1(ZRD-EFP-208): visual QA gate sign-off
```

**Pattern:** `^[a-z]+\([A-Z0-9][A-Z0-9\-]+\):`

**Bundle-merge rule:** When one commit covers multiple tickets, add to the PR body:
```
Covers: MFP-504, MFP-505, MFP-506
```

**Why this matters:**
The WAVE 1 re-audit (2026-05-02) found 19 shipped tickets that got no audit credit because:
- Bundle-merge commits named the parent ticket only (e.g. `VAL-PROD-006`) but covered sub-IDs (-002/-004/-005/-006/-007)
- Some commits used scope labels ("Sprint 6 tokens", "taiko(zrd-comms)") instead of exact ticket IDs
- MUSASHI/TAIKO artifacts shipped outside git entirely — those need the shipped_refs artifact pointer in the ticket (separate concern, but same audit-blindness root cause)

**Status:** Currently WARN. Upgrades to BLOCK once all 7 warriors have adopted the format (target: after v1.2 scope audit closes).

**Escape hatches:**
- Docs-only commits, merge commits, and fixup commits may use free-form subject. Add `[no-ticket]` tag to suppress this:
  ```
  docs[no-ticket]: update ROADMAP.md version history
  ```
- Empty commits (--allow-empty) are excluded automatically.

**Companion rule (separate file):** `block-chained-firestore-collection-doc` -- TAIKO discovered 2026-05-02 on PR #818 that the existing `block-direct-firestore-write` rule's `exclude: services/api/src/` clause does NOT bypass content-regex matches; the `.collection().doc()` chained pattern still triggers on whitelisted paths. Workaround: split into two variables. Followup ticket: split-or-fix the existing rule.

See: CLAUDE.md -> Code Standards -> Commit + Ticket Close-Out Doctrine
