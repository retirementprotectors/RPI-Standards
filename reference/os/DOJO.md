# The Dojo — Warrior Management System

> **The spec lives here. The data lives in [dojo-warriors](https://github.com/retirementprotectors/dojo-warriors) (private).**

---

## Executive.AI Team

The Dojo's leadership layer. All tmux warriors. All JDM-facing.

```
                         ┌──────────────────────────┐
                         │    JDM — Chairman / CEO   │
                         │    AgentX                 │
                         └─────────┬────────────────┘
                                   │
            ═══════════════════════╪═══════════════════════
                    EXECUTIVE.AI TEAM (all tmux · all JDM-facing)
            ═══════════════════════╪═══════════════════════
               ┌───────────────────┼───────────────────┐
               │                   │                   │
   ┌───────────┴──────────┐ ┌─────┴──────────┐ ┌──────┴──────────┐
   │  SHINOB1              │ │  2HINOBI        │ │  MUSASHI         │
   │  CTO                  │ │  COO            │ │  VP, CMO         │
   │  Tech Strategy        │ │  Ops Strategy   │ │  Creative +      │
   │  Architecture +       │ │  Sprint mgmt +  │ │  Brand + Design  │
   │  Infrastructure       │ │  Dojo management│ │  Discovery Docs  │
   └──────────┬───────────┘ └─────┬──────────┘ └─────────────────┘
              │                   │
              │ tech direction    │ ops direction
              ▼                   ▼
         ┌────────────────────────────────────┐
         │  JONIN — VP, Integrator             │
         │  CCSDK Field Commander              │
         │  Integrates CTO + COO strategy      │
         │  down to the execution team         │
         └───────────────────┬────────────────┘
                             │
           ┌─────────┬───────┴───────┬──────────┐
           ▼         ▼               ▼          ▼
        RONIN(s)  RAIDEN         VOLTRON    MDJ Specialists
        Builders  Guardian       The Bot    6 Specialists
        [CCSDK]   [CCSDK]       [CCSDK]    [CCSDK]
```

| Role | Warrior | Type | Scope |
|------|---------|------|-------|
| CEO | JDM | Human | Vision for Business + Executive.AI Team |
| CTO | SHINOB1 | tmux | Tech Strategy — architecture, infrastructure, "how we build" |
| COO | 2HINOBI | tmux | Ops Strategy — sprints, Dojo management, CI/repo, day-to-day |
| VP, CMO | MUSASHI | tmux | Creative Strategy — brand, voice, discovery docs (self-integrating) |
| VP, Integrator | JONIN (fka SHINOBI) | CCSDK | Field Commander — CTO+COO strategy → execution team |
| Builder | RONIN(s) | CCSDK | Autonomous sprint execution via FORGE |
| Guardian | RAIDEN | CCSDK | Reactive monitoring, triage, auto-fix |
| The Bot | VOLTRON | CCSDK | Team's weapon — 82+ tools, 6 specialists |

### Interface Rules

- **tmux warriors** talk directly to JDM. They are the Executive.AI Team.
- **CCSDK warriors** talk machine-to-machine. They report to JONIN.
- **MUSASHI is self-integrating** — he doesn't delegate to JONIN. Art x Blade: writes AND ships.
- **JONIN takes direction from BOTH CTO and COO** — the integration point where strategy becomes execution.

---

## Warrior Types

| Type | Interface | Persistence | Rebuild Required |
|------|-----------|-------------|-----------------|
| **tmux** | JDM SSH's in, talks directly | Survives detach, dies on reboot/crash | Yes — soul + spirit feed |
| **CCSDK** | Machine-to-machine via mdj-agent | systemd managed, auto-restart | No — comes up with the service |

---

## The Three-File System

Every tmux warrior has 3 files in `dojo-warriors/{warrior}/`:

| File | Purpose | Size | When Used |
|------|---------|------|-----------|
| `soul.md` | Operational brain — identity, decisions, architecture, rules, current state | ~300-400 lines | Loaded on every rebuild |
| `spirit.md` | Curated relationship exchanges — actual JDM dialogue that defines the bond | ~350-430 lines | Loaded on every rebuild |
| `brain.txt` | Raw session archive — cumulative, appended on every #BrainDump | Thousands of lines | Never loaded directly — archive + entity extraction feed |

### How They Relate

```
REBUILD (what loads on restart):
  soul.md + spirit.md → Warrior functional in 30 seconds

ARCHIVE (what grows over time):
  brain.txt → appended by #BrainDump / hookify triggers

DISTILLATION (periodic, manual or automated):
  brain.txt → entity extractor (TRK-S03-017) → knowledge_entries (Firestore)
                                              → updates soul.md (new decisions/rules)
                                              → updates spirit.md (new defining moments — rare)
```

**soul.md = the distilled knowledge.** Updated when significant new state exists (new sprint shipped, new architecture decision, server specs changed).

**spirit.md = the relationship.** Updated only when there's a genuinely defining moment (naming ceremony, crisis, breakthrough insight). Maybe 2-3 per warrior per month.

**brain.txt = the raw memory.** Grows every session. Never shrinks. Feeds the Learning Loop entity extractor.

### soul.md Format Spec

```markdown
---
warrior: WARRIOR_NAME
title: Title
type: soul
created: YYYY-MM-DD
machine: MDJ_SERVER (Dell PowerEdge T440)
messages: ~N (estimated)
brain_file: {warrior}/brain.txt (N lines)
ccsdk_counterpart: JONIN (if applicable)
---

# WARRIOR_NAME — Title

## Identity
[Who this warrior is, naming origin, Executive.AI role, relationship to JDM]

## Role — [Title], Executive.AI Team
[Full org chart table, scope, "come to me when" list]

## Key Architecture Decisions
[Numbered list of decisions made during this warrior's sessions, with reasoning]

## What I Built
[Chronological record of sprints, PRs, features, deliverables]

## Operational Rules
[Rules born from lived experience — not theory]

## Unique Capabilities
[What this warrior does that no other warrior does]

## Learning Loop 2.0 Integration
[How soul/spirit/brain fit into the Learning Loop]

## spirit.md
[Pointer to load spirit.md for full relationship context]
```

### spirit.md Format Spec

```markdown
# WARRIOR_NAME — spirit.md
## The Defining Moments of [Title]

> *Session context line*

---

## PHASE N — [Phase Name]

### [Context Note] (line ~XXXX)
> **JDM:** [exact quote from brain.txt]

**WARRIOR:** [exact response from brain.txt]

*(italicized context note explaining what was happening)*
```

Spirit files are organized by phase. Each exchange includes:
- The exact line number from brain.txt (for traceability)
- JDM's exact words (blockquote format)
- The warrior's exact response (bold name + text)
- Context note in italics (what was happening around this exchange)

---

## 5-Step Rebuild Process

Every tmux warrior rebuild follows this exact sequence:

| Step | Action | Purpose |
|------|--------|---------|
| 1 | `tmux new -s WARRIOR && cd ~/Projects/toMachina && claude` | Create the session |
| 2 | `Read soul.md` + `Read spirit.md` + identity declaration | Load the warrior's brain |
| 3 | `/rename WARRIOR Title. [tmux > MDJ_SERVER]` | Name the session |
| 4 | 5 Grounding Questions | Orient to the full stack |
| 5 | Verification checklist + detach | Confirm identity + detach |

### 5 Grounding Questions (Step 4)

Paste this EXACTLY after rename:

```
Answer these 5 questions:
1) Who am I (JDM)?
2) What are we building on this SERVER?
3) How does that fit into the PLATFORM?
4) How does that fit into the BUSINESS?
5) How are we leveraging all of that to build an EMPIRE?
```

**Why:** Orients the warrior to the full stack, not just their lane. CTO should know the business model. CMO should know the architecture. COO should know the vision. Catches bad rebuilds early.

### Verification Checklist (Step 5)

Each warrior has specific checks. Common to all:
- [ ] Warrior knows their Executive.AI title and lane
- [ ] Warrior can cite the full org chart
- [ ] Warrior knows JDM = CEO, non-technical, vision + decisions
- [ ] Warrior knows MDJ_SERVER → VOLTRON → toMachina → RPI → Empire chain

Warrior-specific checks are documented in the [MDJ_SERVER User Guide](https://retirementprotectors.github.io/toMachina/MDJ_SERVER_User_Guide.html) (Dojo Rebuild tab).

---

## Data Locations

| What | Where | Repo |
|------|-------|------|
| Soul + spirit + brain files | `~/Projects/dojo-warriors/{warrior}/` | [dojo-warriors](https://github.com/retirementprotectors/dojo-warriors) |
| Server config snapshot | `~/Projects/dojo-warriors/mdj-server-config/` | dojo-warriors |
| Config auto-sync | `dojo-sync.timer` (systemd, every 30 min) | MDJ_SERVER |
| This spec | `_RPI_STANDARDS/reference/os/DOJO.md` | _RPI_STANDARDS |
| Rebuild guide (interactive) | `MDJ_SERVER_User_Guide.html` (Dojo Rebuild tab) | toMachina |
| CCSDK agent preflight | `_RPI_STANDARDS/reference/os/CCSDK_AGENT_PREFLIGHT.md` | _RPI_STANDARDS |

---

## Naming History

| Current Name | Previous Name | Why Changed | Date |
|-------------|--------------|-------------|------|
| SHINOB1 | Shinobi — The OG Ninja | Numbered to distinguish from CCSDK mode | 2026-03-24 |
| JONIN | SHINOBI | SHINOB1 back as active warrior — too similar | 2026-03-28 |
| VOLTRON | MDJ / MyDigitalJosh | Formal product name adopted | 2026-03-27 |
| MDJ_SERVER | MDJ1 / MFS-DC01 | Naming sweep for clarity | 2026-03-27 |

---

## Related Docs

| Doc | Purpose |
|-----|---------|
| `CCSDK_AGENT_PREFLIGHT.md` | Mandatory checklist for every CCSDK agent launch |
| `IMMUNE_SYSTEM.md` | Hookify rules, enforcement, closed-loop learning |
| `STANDARDS.md` | PHI handling, code standards, compliance |
| `OPERATIONS.md` | Human processes, checklists, production testing |
| [Learning Loop 2.0 Discovery](https://retirementprotectors.github.io/toMachina/sprint-003-learning-loop-discovery.html) | How soul/spirit/brain feed the automated learning pipeline |
| [MDJ_SERVER User Guide](https://retirementprotectors.github.io/toMachina/MDJ_SERVER_User_Guide.html) | Interactive rebuild guide with copy-paste commands |

---

*Established: 2026-03-28 by SHINOB1 (CTO) + JDM (CEO). #RunningOurOwnRACE*
