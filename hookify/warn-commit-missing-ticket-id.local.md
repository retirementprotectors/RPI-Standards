---
name: warn-commit-missing-ticket-id
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: git\s+commit\b(?!.*--amend)
exclude:
  - pattern: git\s+commit\s+.*--allow-empty
  - pattern: git\s+commit\s+.*\[no-ticket\]
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
