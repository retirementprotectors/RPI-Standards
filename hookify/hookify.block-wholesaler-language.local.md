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
