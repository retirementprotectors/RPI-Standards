# JDM + RPI Global Context — RETIRED as a doctrine source (2026-07-08)

> **This file is no longer the source of truth.** Retired per JDM directive under
> **OB1-CLAUDEMD-SCROLL-MIGRATE** (Phase 0), closing the same drift that killed the
> project-level `toMachina/CLAUDE.md` on 2026-06-20.
>
> The 1,342-line global `CLAUDE.md` had drifted (~50% stale, and it had already
> re-grown to 1,342 lines *once before*). The Machine runs on a **dynamic, boot-inlined
> Scroll** — a set of shared streams auto-inlined into every warrior boot — not a
> static hand-maintained monolith. Phase 0 proved (0.2 both-ends, HIKARI-signed) that a
> crutch-free boot from the Scroll streams **loses nothing** the monolith carried.

## Where the content went — Scroll shared streams (`toMachina/docs/warriors/shared/`, boot-inlined)

| Content | Canonical stream |
|---|---|
| PHI / workspace governance | `phi-governance.md` |
| JDM identity · RPI business · **team roster** · channels · offboarded users | `rpi-business.md` |
| Warrior roster · Dojo · Hall of Fame | `dojo-roster.md` |
| MCP inventory · consolidation rule · CLI config | `mcp-inventory.md` (volatile list → read-live `claude mcp list`) |
| Platform vocabulary (Platform/Portals/Sections/Modules/Apps/Tools/MATRIX) | `platform-taxonomy.md` |
| Session protocol · thinking levels · role · Reference Detection | `warrior-ops.md` |
| A.P.P.A. · Golden Rules · operating rules · #1 respond-where-you-receive | `operating-rules.md` |
| Engineering standards · deploy/#SendIt · trunk-based · MATRIX · API | `toMachina-engineering-doctrine.md` |
| Signals · verbosity · hub/Slack format | `comms-glossary.md` |
| Industry + standard terminology | `terminology.md` |
| ATLAS / Operating System narrative | `os-narrative.md` |
| Cross-warrior gotchas | `cross-warrior-gotchas.md` |

Boot atom: `dojo-warriors/doctrine/SHARED_BOOT_DOCTRINE.md`.

## Read-live (deliberately NOT migrated — never in a static file)

- **Repo STRUCTURE** (apps, packages, services, route counts, collections) → read the live repo.
- **MDJ_SERVER infra / soul** → read live.
- **Project Locations tree + Session URLs** → read live.
- **MCP inventory volatile list** → `claude mcp list`.

## Enforcement

Rules are enforced by the **hookify gates** (the SSOT for literal forbidden strings),
independent of this file. This stub itself is guarded by `block-global-claudemd-write` —
re-growing this file is blocked. Legit stub edits carry the token
`# claudemd-stub-update: <reason>`.

Pre-retirement content is in git history (`git log -p -- CLAUDE.md`).

🥷 — SHINOB1, CTO — doctrine moved to the Scroll; structure read live from the repo
