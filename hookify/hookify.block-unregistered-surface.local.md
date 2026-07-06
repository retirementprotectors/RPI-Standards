---
name: block-unregistered-surface
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: \b(?:const|let|var)\s+(?:APP_REGISTRY_FIXTURE|partner_always_hidden)\b|\b(?:APP_REGISTRY_FIXTURE|partner_always_hidden)\s*[:=]\s*[\[{]
exclude:
  - pattern: \.(md|txt)$
  - pattern: docs/discoveries/
  - pattern: docs/templates/
  - pattern: /inbox/
  - pattern: hookify\.block-unregistered-surface
  - pattern: packages/ui/src/modules/AdminPanel\.tsx$
  - pattern: scripts/check-registry-conformance\.mjs$
  - pattern: \.github/workflows/death-gate\.yml$
owner: shinob1
---

**WARNING: A hardcoded surface fixture may be re-entering — surfaces derive from the App Registry SSOT, never a hardcoded side-list.**

This file DECLARES one of the surface fixtures that KGM-SR-103 (#2357) removed — `APP_REGISTRY_FIXTURE` or `partner_always_hidden`. Those were the hardcoded catalog / hide-lists the aXe hub used *before* the App Registry became the single source of truth. Re-declaring one means a surface's visibility is being decided by a hardcoded list again, not by the live registry.

This is the **L2** layer of the **Registry-Registration** doctrine (fast, write-time feedback):
- **L1 (source):** the disco standing question — every new surface / module / app / hub-primitive declares its `app_registry` entry (`docs/warriors/shared/toMachina-engineering-doctrine.md` → "REGISTRY REGISTRATION"; emitter KGM-SR-106).
- **L2 (this rule):** catches a hardcoded surface fixture at the moment it's written, repo-wide, before commit.
- **L3 (merge backstop):** the CI `registry-conformance` gate (KGM-SR-105, a REQUIRED check) — bidirectional nav-gating ⇄ hub_surface conformance + zero fixture residual in the aXe hub.

**Why this matters:**
The App Registry (`packages/core/src/registry/app-registry-def.ts` → the typed SEED that projects the Firestore `app_registry/{key}` rows) is the ONE catalog. Nav, tray, HOME, and TEP surfaces are all **runtime VIEWS** over it. A hardcoded fixture forks that truth: a surface can render (or hide) out of step with what the registry says, and — worse — a partner-eligible surface added to a hardcoded list with no gating can **fail open** to ineligible tenants (the exact P0 class KGM-SR-105 exists to seal).

**Fix:**
- Render from the registry: filter `APP_REGISTRY_DEF` / `HUB_SURFACE_DEF` (or the live `app_registry/{key}` Firestore rows) by `kind`, `permitted_bands`, and `permitted_tenancy` — don't hand-maintain a parallel list.
- Adding a new surface? Add its row to the registry def (`app-registry-def.ts`) + declare `permitted_bands` × `permitted_tenancy`, and let the views pick it up. That's the L1 registration step.
- Need a DOM-only binding (e.g. a nav-key → selector map, which genuinely can't live in Firestore)? That's fine — it's not a catalog. But it must stay conformant with the registry: `registry-conformance` (L3) asserts every selector key maps to a real `hub_surface` and every partner-eligible surface HAS a selector.

**Scope of this rule (v1):**
- Targets the two KNOWN eliminated fixtures by identifier (`APP_REGISTRY_FIXTURE`, `partner_always_hidden`), in **declaration shape** (`const/let/var X`, or `X = [` / `X: {`) — a maintained blocklist, same model as `block-hardcoded-matrix-ids`. A prose mention or a string literal (`'APP_REGISTRY_FIXTURE'`) does NOT trip it — only a real re-declaration.
- **Excluded (legitimate, verified zero-FP):** `AdminPanel.tsx` still carries the fixture and is **tracked-OUT** to the Portal Registry Adoption wave (unverifiable in P1's G0-aXe-only scope) — editing it must not block the eventual swap; `scripts/check-registry-conformance.mjs` and `death-gate.yml` name the fixtures on purpose (they're the enforcement tooling that *detects* them); docs / authoring artifacts reference them by name.
- **WARN** posture in v1 (fast feedback without hard-blocking during the P1 → portal transition). Ratchets to **BLOCK** as SHINOB1's lever once the tracked-OUT AdminPanel / sidebars are converted and no legitimate fixture remains.

**Extending:** when a new hardcoded surface fixture is identified (or a tracked-OUT file is converted), add its identifier to the pattern alternation / remove the now-clean file from `exclude`. Coordinate with SHINOB1 (registry immune-system stewardship).

Doctrine: `docs/warriors/shared/toMachina-engineering-doctrine.md` → "REGISTRY REGISTRATION" + "3-LAYER ENFORCEMENT". L3 backstop: the CI `registry-conformance` required check (KGM-SR-105).
