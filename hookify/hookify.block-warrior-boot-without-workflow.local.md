---
name: block-warrior-boot-without-workflow
enabled: true
event: bash
action: block
# 2026-05-19 (SHINOB1): hookify upstream removed `exclude:` semantics, which
# silently bricked this rule — ALL warrior spawns were blocked instead of
# only non-allowlisted ones. Rewrote to express the same intent using only
# operators the current runtime supports: a single negative-lookahead
# regex_match (allowlist baked in) ANDed with two not_contains opt-outs.
# Same allowlist as the frozen 2026-05-03 set — no scope change.
conditions:
  # Block when launch-warrior.sh fires for a warrior NOT in the frozen allowlist.
  # Allowlist (frozen 2026-05-03, one-way ratchet, SHINOB1 sign-off required to expand):
  #   Mains (7): megazord, musashi, raiden, ronin, shinob1, taiko, voltron
  #   Ronin variants: ronin-<lowercase>
  #   Shinob1 variants (13): auditor / auditor-hermes / auditor-raiden / coach /
  #     discovery-cxonode / discovery-launchguide / discovery-masterplan /
  #     mwm-spyglass / plan-p1 / plan-p2 / plan-p3 / plan-pwauth
  - field: command
    operator: regex_match
    pattern: launch-warrior\.sh\s+(?!(megazord|musashi|raiden|taiko|voltron|ronin(-[a-z]+)?|shinob1(-(auditor(-hermes|-raiden)?|coach|discovery-(cxonode|launchguide|masterplan)|mwm-spyglass|plan-(p1|p2|p3|pwauth)))?)(\s|$))[a-z]
  # Opt-out 1: workflow-aware boot — operator referenced WORKFLOW.md in the
  # same bash invocation (e.g. `cat warriors/foo/WORKFLOW.md && launch-warrior.sh foo`).
  - field: command
    operator: not_contains
    pattern: WORKFLOW.md
  # Opt-out 2: explicit legacy-path opt-out — operator confirms intentional pre-FORGE-2.0 boot.
  - field: command
    operator: not_contains
    pattern: --legacy-boot
---

**BLOCKED: Warrior boot without WORKFLOW.md**

Per JDM directive 2026-05-03 (FORGE 2.0 Phase 2, SYM-003), all NEW warrior boots
must consume their runtime config from a versioned `WORKFLOW.md`, not the legacy
`soul.md` / `spirit.md` / `/tmp/<warrior>-boot.txt` scatter.

**Why this is blocked:**
- Soul/spirit/boot scatter is unversioned, drifts across machines, and forks
  warrior identity silently. Three Ronins running today already differ.
- WORKFLOW.md is the single source of truth: identity, registry, doctrines,
  comms protocol, and runtime config in one versioned file.
- Without WORKFLOW.md, parallel warrior variants accumulate undocumented
  divergence — the exact failure mode FORGE 2.0 P2 exists to fix.

**To proceed, do ONE of these:**

1. **Migrate the warrior** (preferred):
   - Author `~/Projects/dojo-warriors/warriors/<name>/WORKFLOW.md` per the
     FORGE 2.0 P2 spec (consolidates soul + spirit + boot into one file).
   - Re-run the launch — the rule will pass once WORKFLOW.md is referenced.

2. **Add to legacy allowlist** (only for pre-2026-05-03 warriors):
   - Edit this rule's `exclude:` block to add the warrior to the legacy
     allowlist regex. Get SHINOB1 sign-off — the allowlist is a one-way ratchet.

3. **Explicit one-shot legacy opt-out**:
   - Append `--legacy-boot` to your bash invocation, e.g.
     `bash launch-warrior.sh <name> --legacy-boot`. Use sparingly; this is
     for emergency reboots of legacy warriors only, not new variants.

**Reference:**
- FORGE 2.0 Discovery Doc — SYM-003 in Tab 6 (Tickets)
- Phase 2 Plan — per-line spec for WORKFLOW.md format
- `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` — propagates this rule
  to active project `.claude/` dirs after merge

**Legacy allowlist (frozen 2026-05-03 — explicit, NOT prefix-wildcard):**
- Mains (7): `megazord`, `musashi`, `raiden`, `ronin`, `shinob1`, `taiko`, `voltron`
- Ronin variants (3): `ronin-a`, `ronin-b`, `ronin-c`
- Shinob1 variants (13): `shinob1-auditor`, `shinob1-auditor-hermes`,
  `shinob1-auditor-raiden`, `shinob1-coach`, `shinob1-discovery-cxonode`,
  `shinob1-discovery-launchguide`, `shinob1-discovery-masterplan`,
  `shinob1-mwm-spyglass`, `shinob1-plan-p1`, `shinob1-plan-p2`,
  `shinob1-plan-p3`, `shinob1-plan-pwauth`

New warriors created after 2026-05-03 must ship WORKFLOW.md or be explicitly
added to this list with SHINOB1 review.
