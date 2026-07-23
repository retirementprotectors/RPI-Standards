---
name: warn-disco-missing-compliance-blocks
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/discoveries/.*\.html$
  - field: content
    operator: not_contains
    pattern: scope_class
owner: shinob1
---

⚠️ **DISCO COMPLIANCE — this discovery doc is missing required blocks. Fix before sign-off.**

You're writing a discovery doc to `docs/discoveries/` with **no `scope_class`** on its tickets — the exact incompleteness that shipped a non-compliant disco tonight (2026-07-13) and cost a 2-hour manual dig. Per `docs/templates/DISCOVERY_DOC_FORMAT.md`, every disco MUST carry all three of these, or it is INCOMPLETE:

**1. `scope_class` per Tab-6 ticket** (Ticket Taxonomy Doctrine, JDM 2026-07-05 — REQUIRED).
Every ticket declares one of `BUILD · DATA · WORKFLOW · CREATIVE · COMMS · ARCH` — that's what auto-routes it to the right warrior (BUILD→RONIN · DATA/WORKFLOW→MEGAZORD · CREATIVE→MUSASHI · COMMS→TAIKO · ARCH→SHINOB1). No `scope_class` = an orphan no sweeper routes.

**2. Tab-8 Registry Registration** (Registry Registration Doctrine, SHINOB1+JDM 2026-07-06 — REQUIRED).
Any scope introducing a surface/module/app/hub-primitive/entitlement MUST declare its App Registry entry in Tab 8 (`{ key, kind, permitted_bands, permitted_tenancy, tray_eligible, home_default }`, reconciled from live gating code). If it introduces NO surface, state `N/A` explicitly — never omit the question.

**3. L1/L2/L3 per invariant** (3-Layer Enforcement Doctrine — REQUIRED).
Every invariant the disco introduces names its enforcement at all three layers: **L1 SOURCE** (doctrine/disco question) · **L2 WRITE** (hookify at code-write time) · **L3 MERGE** (CI required-check). An invariant enforced at only one layer has an open bypass.

**This is WARN-first** (the doctrine's own posture is soft-self-check, not block). If this disco genuinely has all three (and just didn't spell `scope_class` in a ticket table this heuristic reads), proceed. Otherwise: add the missing block(s) before you hand it for co-sign — the whole point is you get smacked HERE, at author time, not by JDM two hours deep.

Rule: `OB1-DISCO-COMPLIANCE-GATE-001` · closes the author-time (L2) gap under the Ticket-Taxonomy + Registry-Registration doctrines · owner SHINOB1 (A6 immune-system lane).
