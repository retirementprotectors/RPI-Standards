---
name: block-unregistered-surface
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: \b(?:const|let|var)\s+(?:APP_REGISTRY_FIXTURE|partner_always_hidden)\b|\b(?:APP_REGISTRY_FIXTURE|partner_always_hidden)\s*[:=]\s*[\[{]|key\s*:\s*['"][a-z0-9_]{3,}['"]\s*,\s*kind\s*:\s*['"](?:hub_surface|app|module|feature)['"]|kind\s*:\s*['"](?:hub_surface|app|module|feature)['"]\s*,\s*key\s*:\s*['"][a-z0-9_]{3,}['"]|\b(?:permitted_bands|permitted_tenancy|tray_eligible|home_default)\s*:
  - field: file_path
    operator: regex_match
    pattern: \.(?:tsx|jsx|ts|mts|cts|js|mjs|cjs)$
  - field: file_path
    operator: not_contains
    pattern: registry/app-registry-def.ts
  - field: file_path
    operator: not_contains
    pattern: check-registry-conformance
  - field: file_path
    operator: not_contains
    pattern: death-gate-matcher
  - field: file_path
    operator: not_contains
    pattern: modules/AdminPanel.tsx
owner: shinob1
---

**WARNING: A surface may be entering the platform WITHOUT an App Registry row — surfaces derive from the App Registry SSOT, never a hardcoded side-list.**

This write carries one of three registry-forking shapes, in a code file that is **not** the registry definition:

1. **A retired surface fixture is being re-declared** — `APP_REGISTRY_FIXTURE` or `partner_always_hidden`, the hardcoded catalog / hide-lists the aXe hub used *before* the App Registry became the single source of truth (removed by KGM-SR-103, #2357).
2. **A registry ROW is being declared outside the registry** — a `key` + `kind` pair (`hub_surface` / `app` / `module` / `feature`). That is the literal shape of an App Registry entry. Outside `app-registry-def.ts` it is a second catalog.
3. **Registry-only gating vocabulary is being hand-written** — `permitted_bands`, `permitted_tenancy`, `tray_eligible`, `home_default`. These fields exist to be *read from* the registry, never re-authored beside it.

This is the **L2** layer of the **Registry-Registration** doctrine (fast, write-time feedback):
- **L1 (source):** the disco standing question — every new surface / module / app / hub-primitive declares its `app_registry` entry (`docs/warriors/shared/toMachina-engineering-doctrine.md` → "REGISTRY REGISTRATION"; emitter KGM-SR-106).
- **L2 (this rule):** catches a registry-forking SHAPE at the moment it's written, repo-wide, before commit.
- **L3 (merge backstop):** the CI `registry-conformance` gate (KGM-SR-105, a REQUIRED check; extended for DIPSET by OB1-DIPSET-10) — bidirectional nav-gating ⇄ hub_surface conformance, zero fixture residual, zero orphan surface keys.

**Why this matters:**
The App Registry (`packages/core/src/registry/app-registry-def.ts` → the typed SEED that projects the Firestore `app_registry/{key}` rows) is the ONE catalog. Nav, tray, HOME, and TEP surfaces are all **runtime VIEWS** over it. A second catalog forks that truth: a surface can render (or hide) out of step with what the registry says, and — worse — a partner-eligible surface added to a hand-written list with no gating can **fail open** to ineligible tenants (the exact P0 class KGM-SR-105 exists to seal). It is also how a surface gets reported "done" while the registry cannot see it — the BUILT-BUT-DARK failure this rule's DIPSET extension exists to make impossible (9 of 11 "done" DIPSET tickets rendered nothing; 3 of 4 board tabs were never registered).

**Fix — adding a row is a PR-gated CODE change, not a console edit:**
- **Registering a new surface?** Add its row to `packages/core/src/registry/app-registry-def.ts` — key, `kind`, `permitted_bands`, `permitted_tenancy`, `is_phi`, and `parent_key` if it is a `feature` under a shell. That file is the ONLY sanctioned home for a registry row, and edits to it are deliberately not matched by this rule. Adding the row is a **PR-gated code change**; toggling an already-registered key's runtime visibility for a tenant is a **data edit** on `app_registry/{key}` with no deploy (THE DATA/POLICY LINE).
- **Rendering a surface list?** Filter `APP_REGISTRY_DEF` / `HUB_SURFACE_DEF` (or the live `app_registry/{key}` rows) by `kind`, `permitted_bands`, and `permitted_tenancy` — don't hand-maintain a parallel array.
- **PHI-bearing surface?** `is_phi: true` plus an ENTITY tenancy segment (e.g. `partner_midwest_medigap`), never blanket `['rpi']`. Isolation belongs on the registry row, above the surface that renders it.
- **Need a DOM-only binding** (e.g. a nav-key → selector map, which genuinely can't live in Firestore)? That's fine — it's not a catalog, and it carries none of the three shapes above. It must still stay conformant: `registry-conformance` (L3) asserts every selector key maps to a real `hub_surface`.

**Scope of this rule (v2 — 2026-07-25, OB1-DIPSET-09):**
- **Three arms, each measured against the live tree before shipping** (2,455 JS/TS files scanned):
  - *fixture re-declaration* — 2 files, both excluded below. Unchanged from v1.
  - *registry-row shape* (`key` + `kind`) — **1 file: `app-registry-def.ts` itself**, excluded. Zero false alarms.
  - *registry gating vocabulary* — **2 files**, both excluded. Zero false alarms.
- **A fourth arm was measured and REJECTED.** A generic "hardcoded nav catalog" matcher (`const SOME_ARRAY = [ … key: '…' … ]`) hit **58 files** on day one — column defs, tab defs, and menu arrays across 58 unrelated modules. Shipping it would have made this rule a crier, and a rule that cries wolf gets muted, which leaves the gap open AND everyone believing it is covered. Generic hardcoded nav is therefore **explicitly out of L2 scope** and is left to L3 `registry-conformance`, which can do the cross-file set-difference L2 structurally cannot.
- **Excluded via `not_contains` conditions — NOT the `exclude:` key.** The hookify engine has **no `exclude:` support**: `core/config_loader.py` reads only `name` / `enabled` / `event` / `pattern` / `conditions` / `action` / `tool_matcher`, and no file under the plugin references `exclude` at all. v1 of this rule declared 8 `exclude:` patterns that were **inert** — verified by live probe (a Write to the "excluded" `AdminPanel.tsx` carrying the fixture FIRED). Exclusions in this rule family must be `not_contains` / negative-lookahead **conditions**, which the engine does evaluate.
- **Legitimately excluded (measured, zero-FP):** `app-registry-def.ts` (the registry itself — where rows BELONG; excluding it is also what keeps this gate from blocking the DIPSET registration tickets), `scripts/check-registry-conformance.mjs` + `.github/scripts/death-gate-matcher.js` (the L3 enforcement tooling names these shapes on purpose — it is what *detects* them), `modules/AdminPanel.tsx` (still carries the fixture; **tracked-OUT** to the Portal Registry Adoption wave). Non-code paths (`.md`, `.html`, `.yml`, discos, templates, `/inbox/`) are excluded structurally by the file-extension condition.
- **POSTURE: WARN, unchanged from v1 — this v2 does NOT flip to BLOCK.** v1's own ratchet condition ("BLOCK once the tracked-OUT AdminPanel / sidebars are converted and no legitimate fixture remains") is **not yet met** — `AdminPanel.tsx` still carries 2 fixture references today, verified. Flipping now would hard-stop a tracked-OUT file for every warrior on the fleet. The ratchet stays SHINOB1's lever, to be pulled when the conversion lands. *(Note the observer's blind spot: an `action: warn` never enters the model's context — it lands in `~/.claude/hooks/violation-log.jsonl` and on the human's pane. Grep the log to see this rule fire; "I didn't see it" is not evidence it didn't.)*

**Extending:** when a new registry-forking shape is identified (or a tracked-OUT file is converted), add its arm to the pattern alternation / drop the now-clean `not_contains` condition — and **measure the new arm against the live tree first**. Coordinate with SHINOB1 (registry immune-system stewardship).

Doctrine: `docs/warriors/shared/toMachina-engineering-doctrine.md` → "REGISTRY REGISTRATION" + "3-LAYER ENFORCEMENT" + "THE DATA/POLICY LINE". L3 backstop: the CI `registry-conformance` required check (KGM-SR-105, DIPSET extension OB1-DIPSET-10).
