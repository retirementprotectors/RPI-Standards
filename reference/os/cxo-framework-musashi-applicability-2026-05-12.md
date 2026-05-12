# MUSASHI MM-REG-V2 Framework: Applicability to Other CXO Warriors

> **SHINOB1 (CTO) strategic analysis — 2026-05-12.** Requested by JDM after MUSASHI shipped `MM-REG-V2-009` (CMO Registry v2). Question: *"What do you think about what I'm doing with MUSASHI as a Framework for the other CXO Warriors with Registries + Meshes? Is it logical/possible based on what they're building/registering? Why/Why not? What can you propose as alternatives to each, that still maintain the integrity of the Solutions?"*

---

## TL;DR

MUSASHI's framework is **structurally sound and partially transferable**, but **not a one-size-fits-all template**. The core pattern (Division→Brand→Type tree + operational metadata layer + lineage graph + cascade UI + hookify enforcement) maps cleanly onto **3 of 7 warriors** (SHINOB1, TAIKO, parts of RONIN). The other 4 either have **mature registries that already solve the problem differently** (MEGAZORD, VOLTRON) or have **a fundamentally different domain shape** (RAIDEN reactive triage, RONIN sprint-batched).

**Recommendation:** adopt the framework's *additive layers* (lineage graph + cascade UI + hookify enforcement on canonical paths) across all warriors, but **do not force the Division→Brand→Type filesystem tree** on warriors whose registries are Firestore-native or event-shaped.

---

## What MUSASHI's framework actually is

Read of `mm-reg-v2-discovery-doc-v1.html` (live at retirementprotectors.github.io/toMachina/docs/discoveries/) yields 5 load-bearing layers:

| Layer | What it does |
|---|---|
| **1. Two-layer registry** | Archival (`category`, `brand`, `status`, `version`, `location`) + Operational (`division`, `audience[]`, `type`, `lineage`, `companions[]`, `approvals[]`, `shipped_refs[]`). One row per *work-product*, not per file. |
| **2. Filesystem tree** | `Division → Brand → Type` cascade. Two parallel trees (Pages-published + inbox-drafts) with identical structure. |
| **3. Auto-discovery wire** | Scans the tree at intervals, surfaces new entries, eliminates hand-curation cost. |
| **4. Hookify enforcement** | Blocks non-canonical commits at the bash tool level. *Tree integrity is a runtime invariant, not a guideline.* |
| **5. Cascade UI + lineage graph** | Browsable filter UI (Division × Audience × Type), per-entry detail with full lineage chain (disco_id → ticket_id → pr_url → commit_sha). |

**Decisive innovation:** *"Work-product, not file, is the unit of registration."* One DAVID Kit (7 child files) = 1 registry entry, not 7. This is the conceptual move that makes everything else compose.

---

## Per-CXO Applicability

### 1. SHINOB1 (CTO — Architecture / Doctrine / Discovery Docs)

**Fit: STRONG. Biggest applicability of any CXO.**

I do not currently have a structured registry. My work-products (Discovery Docs, hookify rules, doctrine memories, ZRD records, architecture decisions) are scattered across:
- `docs/discoveries/` (~57 disco docs in the toMachina repo)
- `_RPI_STANDARDS/CLAUDE.md` (1100+ lines, no entry-level index)
- `_RPI_STANDARDS/hookify/` (~55 rules, partially indexed)
- `_RPI_STANDARDS/reference/os/` (a half-dozen strategic docs)
- `~/.claude/projects/.../memory/` (hundreds of feedback/project/reference memories)

*This is the exact 167-work-products-scattered-across-20-locations problem MUSASHI solved for himself.*

**Recommended adoption (full framework, with one substitution):**
- Division → `architecture | doctrine | hookify | reference | postmortem`
- Brand → not applicable (substitute: `scope` = `os | toMachina | gas | services`)
- Type → `disco | adr | rule | memory | reference`
- Operational layer (lineage / audience / shipped_refs) → adopt verbatim
- Auto-discovery wire → adopt, scanning `_RPI_STANDARDS/` + `docs/discoveries/` + memory dir
- Hookify enforcement → adopt (canonical path enforcement on Discovery Doc creation)
- Cascade UI → adopt

**Cost:** ~2 weeks to scaffold; biggest lift is the auto-discovery wire + the cascade UI in ProDashX.
**Payoff:** every architecture decision becomes traceable to the doctrine that produced it. Memory becomes searchable.

### 2. TAIKO (Comms Infrastructure — Pipes Registry)

**Fit: STRONG. Pipes Registry isn't formalized yet — best moment to adopt.**

TAIKO owns end-to-end comms infra: Twilio Voice/SMS, SendGrid Email, Google Meet, Google Chat, RPI Connect module, in-portal Comms, alerts. The "Pipes Registry" concept exists but isn't yet a structured registry.

**Recommended adoption (full framework):**
- Division → `voice | sms | email | meet | chat | alert`
- Brand → carrier/provider (`twilio | sendgrid | google-meet | google-chat`)
- Type → `endpoint | template | webhook | wire | suppression-list`
- Operational layer → adopt verbatim; especially valuable for `lineage` (TKO-COMMS-005a / ZRDs that produced each pipe)
- Auto-discovery → adopt, scanning routes + webhooks + GSM secret manifest
- Hookify → adopt (block direct pipe writes outside the registered surface)
- Cascade UI → adopt (TAIKO Command Center)

**Why TAIKO benefits most:** the pipes are *operational* (the team uses them daily, JDM cares which carriers/templates exist). Visibility = trust. Without registry, the team lives in TAIKO's head; with registry, the team self-serves.

### 3. RONIN (FORGE Sprint Executor)

**Fit: PARTIAL. The framework partially fits — RONIN's work-product shape is a *sprint*, not an *asset*.**

RONIN's domain is sprint-batched: Discovery Doc → Plan → Build → Ship → LandedIt. Each sprint is the work-product. The artifacts produced (PRs, code) belong to the consuming warrior, not RONIN.

**Recommended adoption (adapted):**
- Division → not natural for sprints (consider: `track` like `architecture | feature | refactor | bugfix`)
- Brand → not applicable
- Type → `sprint | hotfix | spike`
- **Key adaptation:** the registry entry is the SPRINT, not the asset. Lineage graph is sprint → tickets → PRs → live deploys
- Auto-discovery → adopt, scanning `forge/` runner output
- Hookify → not needed (FORGE already enforces sprint shape)
- Cascade UI → adopt (browsable past sprints with outcome filters)

**Alternative:** RONIN doesn't strictly need MUSASHI's framework — the FORGE template registry already plays the registry role. *What RONIN benefits from is the lineage graph and the browsable past-sprint UI*, not the full Division→Brand→Type tree.

### 4. MEGAZORD (CIO — ATLAS: Sources, Tools, Wires)

**Fit: WEAK. ATLAS already solves the registry problem with a different storage model.**

ATLAS is a *mature, Firestore-native* registry:
- `source_registry` collection
- `tool_registry` collection
- `wire_registry` collection
- `atlas_audit` collection
- 15 atomic tools, 12 super tools, 5 wires, all entered + queryable

The MUSASHI filesystem tree pattern is *redundant* here. ATLAS already has cascade-able metadata (category, side_effects, composability, owner_warrior). What ATLAS does NOT yet have:

**Recommended adoption (additive layers only):**
- ❌ Filesystem tree — *don't impose; ATLAS is Firestore-native*
- ❌ Auto-discovery wire — *ATLAS is hand-registered intentionally; that's a feature*
- ✅ Explicit lineage graph (disco_id → ticket_id → pr_url → commit_sha) — currently atlas_audit captures runtime hits but not creation lineage
- ✅ Cascade UI surface (MegazordCommandCenter Capability Matrix is the embryo; expand to MUSASHI-style cascade)
- ✅ Hookify enforcement (block direct Firestore writes outside the registered tool surface — partially already enforced)

**Alternative for MEGAZORD:** stay Firestore-native. Adopt the *operational metadata schema* (audience / lineage / companions) at the Firestore document level, not as filesystem layout. Skip the tree.

### 5. VOLTRON (CSO — QUE: 5 Lions + 82 tools)

**Fit: WEAK. Same shape as MEGAZORD — registry already exists, Firestore-native.**

VOLTRON owns QUE: 5 Lions (Medicare, Annuity, Life/Estate, Investment, Legacy/LTC) + 82 wired tools (57 toMachina API + 25 MCP) + case_analysis_matrix (CAM).

**Recommended adoption (additive layers only):**
- ❌ Filesystem tree — *QUE is module-based in code (`packages/ui/src/modules/CommandCenter`)*
- ❌ Auto-discovery wire — *82 tools are explicitly wired; that's intentional*
- ✅ Explicit lineage graph for each tool (which Lion owns it, which disco doc produced it, which PR shipped it)
- ✅ Cascade UI within MDJ Panel (Lion × tool × approval-tier × side-effect filter)
- ✅ Hookify enforcement on canonical patterns (already exists for `warn-untyped-api-response`)

**Alternative for VOLTRON:** same as MEGAZORD. Stay code/module-based. Adopt the operational layer + cascade UI + lineage graph; skip the filesystem tree.

### 6. RAIDEN (Reactive Guardian)

**Fit: NONE. Different domain shape — RAIDEN is event-shaped, not artifact-shaped.**

RAIDEN's work is reactive triage: messages arrive in Slack, RAIDEN classifies + responds/routes/fixes. The "work-products" are *resolved incidents*, not assets. The current model is the `tracker_items` Firestore collection (status RDN-*).

**Recommended adoption (different framework entirely):**
- ❌ Filesystem tree — irrelevant
- ❌ Division → Brand → Type — no natural mapping
- ✅ A different pattern: **Pattern Library** — recurring triage patterns (Access/Navigation/Data-Display/Feature-Request/Bug-Report/Integration) as registry entries with `pattern_id`, `recognition_signal`, `default_action`, `escalation_route`
- ✅ Lineage graph linking pattern → incident → resolution (audit trail)

**Alternative for RAIDEN:** build a *Triage Pattern Registry*, not an asset registry. Conceptually similar (registered work-products with metadata + lineage), but the unit is "pattern of incident," not "asset." Different shape; different fit.

### 7. MUSASHI (CMO — already the source)

**Fit: N/A. This IS the source framework.**

---

## Doctrine recommendation: a tiered adoption model

Rather than force MUSASHI's framework onto every CXO, formalize **3 tiers of registry adoption** that any CXO can pick:

| Tier | What | Best for |
|---|---|---|
| **Tier 1 — Full Framework** | Division→Brand→Type tree + operational layer + auto-discovery + hookify + cascade UI + lineage graph | SHINOB1, TAIKO, MUSASHI |
| **Tier 2 — Additive Layers Only** | Operational metadata + cascade UI + lineage graph; preserve existing storage model | MEGAZORD (ATLAS), VOLTRON (QUE), RONIN (FORGE) |
| **Tier 3 — Different Pattern Entirely** | Custom registry shape that matches the domain (e.g., Triage Pattern Registry) | RAIDEN |

This honors the *integrity* of each warrior's existing solution while spreading the framework's most valuable additive layers (lineage + cascade UI + hookify) universally.

---

## What to do next

1. **MUSASHI ships MM-REG-V2 to completion.** That validates the Tier 1 implementation.
2. **TAIKO adopts Tier 1** as the second instance. Validates cross-warrior reusability of the full framework. Best second adopter because the Pipes Registry isn't yet formalized — clean slate.
3. **SHINOB1 adopts Tier 1** as the third instance. Highest payoff per cycle (biggest scattered-work-products problem of all CXOs).
4. **MEGAZORD + VOLTRON adopt Tier 2** (additive layers only). No registry rebuild — just enhancement.
5. **RONIN adopts a custom Tier 2 variant** (sprint-shaped lineage graph).
6. **RAIDEN gets its own Tier 3 design** (Triage Pattern Registry — separate ZRD).

**Estimated total lift:** ~4-6 weeks across all warriors if executed in sequence. Half that if MUSASHI's auto-discovery wire pattern is extracted as a shared library and the cascade UI is built once as a generic React component.

---

## Risk acknowledgments

1. **The Division→Brand→Type tree is a forcing function.** It's the most opinionated part of the framework. Warriors with already-mature registries (MEGAZORD, VOLTRON) will resist the filesystem rebuild — and they should. The Tier 2 model honors that resistance.
2. **Auto-discovery wires can drift.** If the tree is the source of truth but the wire is the indexer, what happens when they disagree? MUSASHI's hookify enforcement addresses this — block non-canonical commits at the bash tool level. Other warriors adopting the framework MUST also adopt the hookify rule; otherwise drift is inevitable.
3. **Cascade UI is the expensive part.** Building it once-per-warrior is wasteful. Build it once as a generic component (`<RegistryCascadeView source={cmoRegistry} />`), parameterize on the registry shape.

---

## Open questions for JDM

1. **Tier assignment per warrior — agree with this read?** If yes, this becomes the doctrine; warriors execute against their tier.
2. **Cascade UI as shared component?** Recommend ProDashX hosts it as `<RegistryCascadeView>` and each warrior's command center imports it. Avoids 7x reimplementation.
3. **RAIDEN Triage Pattern Registry — is that a real next ZRD, or defer?** Different shape entirely; can be scoped separately.

🥷 — SHINOB1 (OG) — 2026-05-12
