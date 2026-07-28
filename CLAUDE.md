# JDM + RPI Global Context — RETIRED as a doctrine source (2026-07-08)

> **This file is no longer the source of truth.** Retired per JDM directive under
> **OB1-CLAUDEMD-SCROLL-MIGRATE** (Phase 0), closing the same drift that killed the
> project-level `toMachina/CLAUDE.md` on 2026-06-20.
>
> The 1,342-line global `CLAUDE.md` had drifted (~50% stale, and it had already
> re-grown to 1,342 lines *once before*). The Machine runs on a **dynamic Scroll** — a set of
> shared streams — not a static hand-maintained monolith. Phase 0 proved (0.2 both-ends,
> HIKARI-signed) that a crutch-free boot from the Scroll streams **loses nothing** the
> monolith carried.
>
> **⚠️ DELIVERY CORRECTION (2026-07-28).** This paragraph said the Scroll was *"boot-inlined"*
> and *"auto-inlined into every warrior boot"*, and the heading below said the same. **That was
> true when written and is now false — fleet-wide, not for one seat type.** See the box under
> that heading. The streams are **PULLED**; nothing here is pushed into a boot.

<!-- claudemd-stub-update: "boot-inlined" was falsified by the DOJOv3 G+C fleet cutover. This
     file IS the doctrine-migration record, so the claim reads as a promise of boot delivery to
     anyone placing safety-critical content. Corrected in the CTO doctrine lane after HIKARI
     traced his own false premise about push-vs-pull delivery to this exact heading.
     OB1-CLAUDEMD-BOOT-DELIVERY-001. Content otherwise untouched; the stub does not re-grow. -->

## Where the content went — Scroll shared streams (`toMachina/docs/warriors/shared/`) — **CATALOGED, NOT BOOT-CARRIED**

> ⚠️ **These streams are PULLED, not pushed. Nothing in the table below is inlined into a boot.**
>
> **What changed:** the DOJOv3 G+C cutover. `launch-warrior.sh` sets `DOJOV3_GC=enforce` as the
> **fleet default**, under which *"the boot atom carries that tier's admitted blocks INSTEAD of
> the 13 shared streams"* (269,258 B → 63,883 B at SUB, −76%). It is **all-or-nothing by design** —
> the launcher's own words: *"a fleet default, not a per-seat flip, so there is never a window
> where one warrior reads DOJOv3 doctrine and another reads the Scroll."* All nine warriors have a
> G+C artifact on disk, so the documented stream fallback is not the normal path.
> *(Not verified by me: the fallback branch inside `render-boot.ts`. The statement above rests on
> the launcher's own declaration, not on reading that code.)*
>
> **Measured, not inferred.** A live SHINOB1 boot payload carries **zero** stream bodies and says
> verbatim *"adjudicated out of your boot, not deleted"* and *"Reference, not doctrine — never
> carried at boot."* The gotcha catalog alone was 145,809 B — 62% of the old corpus. A HIKARI boot
> independently showed 0 of 11 streams present, which **corroborates but does not prove**: that
> boot was a LITE resume, which skips doctrine by design, so its absence is weaker evidence than
> the positive statement above. Recorded that way deliberately.
>
> **Why this matters and is not pedantry:** a warrior choosing a home for something that MUST
> reach every seat will read this table and believe boot delivery is included. **It is not.**
> Getting content actually pushed means **admitting a DOJOv3 block against a capped tier budget** —
> a different decision, a different owner, and a real cost. The table below remains the correct map
> of *where the content lives*; it was never a statement about *how it reaches you*.

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
