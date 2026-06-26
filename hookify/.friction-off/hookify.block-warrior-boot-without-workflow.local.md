---
name: block-warrior-boot-without-workflow
enabled: true
event: bash
action: block
# 2026-05-19 (SHINOB1): hookify upstream removed `exclude:` semantics, which
# silently bricked this rule — ALL warrior spawns were blocked instead of
# only non-allowlisted ones. Rewrote to express the same intent using only
# operators the current runtime supports: a single negative-lookahead
# regex_match (allowlist baked in) ANDed with one not_contains opt-out.
# Same allowlist as the frozen 2026-05-03 set — no scope change.
#
# 2026-05-30 (RONIN, CUT-006): Removed opt-out #2 (not_contains --legacy-boot).
# --legacy-boot was the gate-bypass backdoor killed in CUT-005 (Symphony Cutover).
# Single positive condition only: WORKFLOW.md must be present. No escape hatch.
conditions:
  # Block when launch-warrior.sh fires for a warrior NOT in the frozen allowlist.
  # Allowlist (frozen 2026-05-03, one-way ratchet, SHINOB1 sign-off required to expand):
  #   Mains (7): megazord, musashi, raiden, ronin, shinob1, taiko, voltron
  #   Ronin variants: ronin-<lowercase>
  #   Shinob1 variants (14): auditor / auditor-hermes / auditor-raiden / coach /
  #     discovery-cxonode / discovery-launchguide / discovery-masterplan /
  #     mwm-spyglass / plan-p1 / plan-p2 / plan-p3 / plan-pwauth /
  #     dex (added 2026-06-09 — JDM "clear the hook for SHINOB1-DEX"; SHINOB1 sign-off)
  - field: command
    operator: regex_match
    # 2026-06-09: + megazord-usps-county, ronin-usps-label (JDM "USPS 100%, parallelize
    #   via sub-CXO launches"; SHINOB1 sign-off). Multi-segment names the single-segment
    #   ronin(-[a-z]+)? pattern + megazord-no-variant didn't cover.
    # BROADENED 2026-06-09 (JDM "one yes and sub-CXO launches stop hitting this" = explicit
    #   authorization for the open fix). Any of the 7 mains + any -<lowercase/digit/hyphen>
    #   variant launches. The WORKFLOW.md requirement (this rule's ACTUAL purpose) is still
    #   enforced by the not_contains condition below — who-gating is removed, version-gating
    #   stays. Replaces the frozen explicit allowlist that generated 3 friction-edits in one night.
    # 2026-06-15 (SHINOB1 sign-off): + kagami — the 8th MAIN warrior (Surface CXO),
    #   born this session, WORKFLOW.md authored at toMachina/docs/warriors/kagami/.
    #   New permanent main = allowlist add (the one-way ratchet, CTO sign-off).
    pattern: launch-warrior\.sh\s+(?!(megazord|musashi|raiden|taiko|voltron|ronin|shinob1|kagami)(-[a-z0-9-]+)?(\s|$))[a-z]
  # Opt-out: workflow-aware boot — operator referenced WORKFLOW.md in the
  # same bash invocation (e.g. `cat warriors/foo/WORKFLOW.md && launch-warrior.sh foo`).
  - field: command
    operator: not_contains
    pattern: WORKFLOW.md
owner: shinob1
---

**BLOCKED: Warrior boot without WORKFLOW.md**

Per JDM directive 2026-05-03 (FORGE 2.0 Phase 2, SYM-003), all warrior boots
must have a versioned `WORKFLOW.md`. The Symphony Launcher Cutover (CUT-006,
2026-05-30) removed the `--legacy-boot` escape. There is no bypass.

**Why this is blocked:**
- Soul/spirit/boot scatter is unversioned, drifts across machines, and forks
  warrior identity silently. Three Ronins running today already differ.
- WORKFLOW.md is the single source of truth: identity, registry, doctrines,
  comms protocol, and runtime config in one versioned file.
- Without WORKFLOW.md, parallel warrior variants accumulate undocumented
  divergence — the exact failure mode FORGE 2.0 P2 exists to fix.

**To proceed:**

1. **Author WORKFLOW.md for the warrior** (the only path):
   - Create `~/Projects/dojo-warriors/warriors/<name>/WORKFLOW.md` per the
     FORGE 2.0 P2 spec (see `forge2-symphony-discovery-doc-v1.0.html` SYM-002).
   - For sub-CXOs / case nodes: they inherit the parent's WORKFLOW.md via the
     parent-fallback chain in `launch-warrior.sh` — no separate WORKFLOW.md needed
     if the parent already has one.
   - Re-run the launch — the rule will pass once WORKFLOW.md is present.

2. **Add to legacy allowlist** (only for pre-2026-05-03 warriors with SHINOB1 sign-off):
   - Edit this rule's allowlist regex. This is a one-way ratchet — SHINOB1 review required.

**Reference:**
- FORGE 2.0 Discovery Doc — SYM-003 in Tab 6 (Tickets)
- Symphony Cutover — launcher-symphony-cutover-v1.html (CUT-006)
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
