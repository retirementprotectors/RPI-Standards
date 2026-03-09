# Plan: Build 3 Master Roadmaps (RIIMO, RAPID_IMPORT, _RPI_STANDARDS)

## Context

We just completed a full plan inventory (39 plans, Feb 15 – Mar 3), consolidated them by project, archived 16 completed plans, and created a consolidation notes file. PRODASHX already has a master roadmap. Three projects still need theirs built to take us from 24 active plan files down to ~11 clean docs.

**Pattern:** Follow the exact structure from `prodashx-platform-roadmap.md`:
- Header + consolidation note + last updated date
- Version History table (deployed versions only)
- Streams (numbered, each with Status + Source plan + item table + files + dependencies)
- Recommended Execution Order (phased)
- Source Plans reference table at bottom

---

## Deliverable 1: RIIMO Platform Roadmap

**File:** `~/.claude/plans/riimo-platform-roadmap.md`

**Absorbs 5 active plans:**
- noble-skipping-plum (PARTIAL — multi-phase build)
- warm-humming-riddle (OPEN — unit auto-assignment)
- rustling-wibbling-babbage (OPEN — EP onboarding, moved from EP-Business)
- parsed-hugging-lerdorf (BLOCKED — playbook doc extraction, moved from Google-Drive)
- FROM wondrous-snuggling-phoenix: Team availability dashboard

**Version History (from archived plans):**
- v1.9-2.1: Deprecated code removal, real MATRIX health, Cloud Run (twinkling-tinkering-shell)
- v3.0: Entitlements v2, Onboarding/Tasks, Job Descriptions, Dashboard (wise-gliding-stonebraker)
- v3.6.0: First name fix, Drive folder, profile photos, Google Picker (linked-spinning-meerkat)
- v3.6.x: Dashboard vs Intelligence restructure (zany-snacking-petal)

**Streams:**
1. Production Build Phases 0-4 (from noble-skipping-plum) — Security cleanup, Foundation, Visibility, Control, Intelligence
2. Unit-Based Auto-Assignment (from warm-humming-riddle) — Unit dropdown fix, LEADER_DEFAULT_RAPID_TOOLS, auto-compute permissions
3. EP Onboarding Package (from rustling-wibbling-babbage) — Carrier inventory, commission structure, Signal transactions for Zane/EP
4. Playbook & Job Description Extraction (from parsed-hugging-lerdorf) — Read 8 Drive docs, extract job descriptions for RIIMO module
5. Team Availability Dashboard (from wondrous-snuggling-phoenix) — Calendar free/busy + Chat presence card
6. Strategic Context (from riimo-strategic-context.md) — TDM Levels, MDJ Instances, AI Platform Control Plane, Data Quality Pipeline

**Plans archived after build:** noble-skipping-plum, warm-humming-riddle, rustling-wibbling-babbage, parsed-hugging-lerdorf

---

## Deliverable 2: RAPID_IMPORT Platform Roadmap

**File:** `~/.claude/plans/rapid-import-platform-roadmap.md`

**Absorbs 6 active plans:**
- sparkling-nibbling-bird (OPEN — data integration overhaul, moved from Cross-Platform)
- stateless-marinating-hopper (PARTIAL — data quality 7-phase, Ph 6 blocked)
- shiny-whistling-lecun (PARTIAL — comprehensive upgrade)
- shiny-whistling-lecun-agent (RESEARCH — API vendor analysis)
- dapper-rolling-glade (OPEN — mail approval workflow fix)
- lucky-tumbling-beacon (OPEN — SPARK schema expansion)
- FROM wondrous-snuggling-phoenix: Comms intake sync

**Version History:** Extract from MEMORY.md completed phases (data quality phases 1-5+7, FK normalization, etc.)

**Streams:**
1. Compliance & Security (from shiny-whistling-lecun Phase 1) — SSN masking, confirmation dialogs, secret exposure fix
2. Code Quality & UX (from shiny-whistling-lecun Phases 2-3) — ZIP fix, DryRun, home page, batch search, orphan UX
3. Mail Approval Workflow (from dapper-rolling-glade) — Slack links, channel routing, home page batch list
4. SPARK Enrichment Pass 3 (from lucky-tumbling-beacon) — 6 new schema fields, enrichment function
5. Data Quality Completion (from stateless-marinating-hopper) — Phase 6 CoF policy import (BLOCKED)
6. Data Integration Overhaul (from sparkling-nibbling-bird) — DTCC, Schwab, Gradient, Blue Button, Chat/Jira/GHL archives
7. API Validation Architecture (from shiny-whistling-lecun Phase 4 + agent research) — WhitePages, Google Places, NeverBounce
8. Comms Intake Sync (from wondrous-snuggling-phoenix) — Twilio/SendGrid/Meet recording import

**Plans archived after build:** All 6 source plans

---

## Deliverable 3: _RPI_STANDARDS Governance Roadmap

**File:** `~/.claude/plans/rpi-standards-governance-roadmap.md`

**Absorbs 3 active plans:**
- radiant-scribbling-goose (OPEN — Data Operating System)
- peaceful-forging-kurzweil (PARTIAL — Hooks as Layer 0)
- quizzical-pondering-chipmunk (PARTIAL — Immune System comprehensive)

**Note:** Plans 2 and 3 overlap heavily (both are Immune System / hooks architecture). Merge into single stream reflecting what was BUILT (hookify) vs what remains (shell hooks, PHI firewall, etc.)

**Version History (from archived plans):**
- Hookify activation: 4 rules, 18 projects (mighty-fluttering-ripple)
- OS directory: 6 docs, symlinks (wondrous-wiggling-music)
- Knowledge pipeline: Slack digest, compliance history (peppy-discovering-naur)
- Reference pruning: 51 docs deleted, 2 new rules (crystalline-toasting-gadget)
- Knowledge Machine v2: AI fix, compliance sweep (bright-jumping-rabbit)

**Streams:**
1. Data Operating System (from radiant-scribbling-goose) — 5 pillars, normalizers, quality gate, contact validation, health check
2. Immune System Evolution (MERGED from peaceful-forging-kurzweil + quizzical-pondering-chipmunk) — What's built (hookify 21 rules, knowledge pipeline, launchd agents) vs what's next (shell hooks for PHI firewall, deploy verifier, destructive action gate, session-end capture)

**Plans archived after build:** All 3 source plans

---

## Execution Plan

### Step 1: Build RIIMO roadmap
- Read all 5 source plans + 4 archived plans + strategic context + consolidation notes
- Write riimo-platform-roadmap.md following PRODASHX pattern
- Archive 4 absorbed plans

### Step 2: Build RAPID_IMPORT roadmap
- Read all 6 source plans + consolidation notes
- Write rapid-import-platform-roadmap.md following PRODASHX pattern
- Archive 6 absorbed plans

### Step 3: Build _RPI_STANDARDS roadmap
- Read all 3 source plans + consolidation notes
- Write rpi-standards-governance-roadmap.md following PRODASHX pattern
- Archive 3 absorbed plans

### Step 4: Cleanup
- Verify _CONSOLIDATION_NOTES.md items are all captured in roadmaps
- Delete _CONSOLIDATION_NOTES.md (served its purpose)
- Update count: should be ~11 active plan files remaining

**All 3 roadmaps can be built in parallel via sub-agents.**

---

## Verification

After all 3 roadmaps are built:
1. `ls ~/.claude/plans/*.md | wc -l` → should be ~11 files (3 new roadmaps + 8 remaining standalone plans)
2. `ls ~/.claude/plans/_ARCHIVED/ | wc -l` → should be ~29 files (16 previous + 13 newly archived)
3. Each roadmap has: Version History, Streams with status, Recommended Execution Order, Source Plans reference
4. Every item from _CONSOLIDATION_NOTES.md is captured in a roadmap
5. Cross-project items from wondrous-snuggling-phoenix are distributed (RIIMO: availability dashboard, RAPID_IMPORT: comms intake sync)
