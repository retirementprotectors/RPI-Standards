---
name: block-wholesaler-language
enabled: true
event: file
action: block
# 2026-06-02 (SHINOB1): RE-AUTHORED + COMMITTED after a durability audit found the
# original was NEVER committed to git and had silently died — deleted canonical +
# dangling symlinks — leaving JDM's #1 directive with ZERO live enforcement.
# Committed this time so it cannot die unversioned again.
conditions:
  - field: content
    operator: regex_match
    pattern: ([Ww]holesaler|[Jj]ustin\s*[Bb]rock)
  # Exempt the rule definition itself + the CLAUDE.md doctrine that legitimately
  # names what is banned (otherwise the definition self-blocks).
  - field: file_path
    operator: not_contains
    pattern: hookify
  - field: file_path
    operator: not_contains
    pattern: CLAUDE.md
  # 2026-06-15 (SHINOB1, ZRD-SCOPE-HOOK-001): the disco/audit surface that legitimately names +
  # grades this rule (docs/discoveries/) was NOT exempt and tripped the gate 3x while authoring
  # the hook-scope audit. LOCATION-scoped, and it stays.
  - field: file_path
    operator: not_contains
    pattern: docs/discoveries
# ── TRK-HOOK-214 (ronin, 2026-07-30) — THE CONTENT TOKEN IS REMOVED; THE THREE LOCATION
#    EXEMPTIONS ABOVE STAY. That asymmetry IS the ruling, and it is now fleet doctrine.
#
# A LOCATION exemption is safe: to claim `hookify`, `CLAUDE.md` or `docs/discoveries` you must
# ACTUALLY BE WRITING THERE, which the engine checks against the real file_path. A CONTENT
# token is not: it asks whether a string appears anywhere in the payload, and a string can
# always be typed. Measured on the bash twin against the wired engine before removal — a REAL
# violation carrying the token PASSED, and so did one with the token in a trailing comment.
# Published in the rule file, so it was a known key on JDM's #1 directive.
#
# MEASURED BEFORE STRIPPING, not assumed: every file on this box carrying the banned term was
# classified. 0 relied on the token; 8 are covered by the location exemptions above. No
# legitimate flow loses its only path. Where prose must discuss this rule outside the three
# locations, name it DESCRIPTIVELY instead of quoting the term — that is how the fleet ruling
# on this very topic was authored without tripping anything.
#
# DO NOT RE-ADD A CONTENT TOKEN. This is asserted in hookify/term-gate.test.py, not merely
# written here: a real violation carrying any such token must BLOCK. A recorded decision that
# is only prose gets re-litigated — the sibling deploy-tree rule wrote "recorded so you do not
# fix it" in a comment and two seats tried to fix it anyway, four hours apart, on one night.
# A comment cannot fail a build. The test can.
owner: shinob1
---

**BLOCKED: carrier-intermediary language (RPI Rule #1 — non-negotiable).**

RPI does not engage intermediaries in its flow. The banned terms (and any
specific intermediary's name) were killed ~6 months ago and kept creeping back
into agent output. Per JDM 2026-05-27 + reaffirmed 2026-05-31: this is Rule #1.

**Use the real source of truth instead:**
- The CARRIER (Nassau direct, NAC direct, NIA direct, etc.) — "carrier-direct"
- The WRITER (Vince, JDM) for any negotiated number
- Never an intermediary, never "approval/illustration-pending" framings tied to one.

**Why this is a hard block, not just doctrine:** the documentation layer alone
failed twice. The only durable layer is the tool-level gate.

See `toMachina/CLAUDE.md` Rule #1 for the full directive + provenance.
