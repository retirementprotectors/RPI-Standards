> ARCHIVED: Completed on 2026-03-08

# Plan Lifecycle — Governance & Cleanup Plan

## Context

RPI has accumulated 17 active local plans, 36 archived plans, and ~65 docs on the Claude Code Shared Drive — but no documented lifecycle governing when plans are created, how they evolve, when they get consolidated, and when they get archived. JDM identified this gap and asked for the definitive governance doc.

**The problem:** Without lifecycle rules, individual plans pile up, superseded plans linger alongside their replacements, feature plans that should be streams in a consolidated roadmap sit orphaned, and the Shared Drive becomes a flat dumping ground (which we just fixed).

**The outcome:** A reference doc (`_RPI_STANDARDS/reference/os/PLAN_LIFECYCLE.md`) that defines the rules, plus immediate cleanup of the 17 remaining local plans per those rules.

---

## Part 1: The Lifecycle Document

Create `_RPI_STANDARDS/reference/os/PLAN_LIFECYCLE.md` with the following structure:

### Plan Categories

| Category | What It Is | Naming Convention | Example |
|----------|-----------|-------------------|---------|
| **Platform Roadmap** | Consolidated master plan per major project/platform. Absorbs feature plans as "streams." One per project. | `{project}-platform-roadmap.md` | `prodashx-platform-roadmap.md` |
| **Working Plan** | Active implementation plan for a specific body of work. Has phases, checkpoints, acceptance criteria. | Descriptive slug or auto-generated name | `portal-overhaul.md` |
| **Feature Plan** | Individual feature build. Gets created via `#LetsPlanIt`, executed, then either folded into a Platform Roadmap as a stream or archived standalone. | Auto-generated name | `humming-exploring-mochi.md` |
| **App Plan** | Standalone project plan for an App (ATLAS, Command Center, etc.) that doesn't have a Platform Roadmap yet. Becomes the seed for one if the app grows. | Auto-generated or descriptive | `polymorphic-twirling-hopper.md` |

### Plan Locations

| Location | What Lives Here | Who Reads It |
|----------|----------------|-------------|
| `~/.claude/plans/` | ALL active plans (Platform Roadmaps, Working Plans, Feature Plans, App Plans) | Claude Code (every session) |
| `~/.claude/plans/_ARCHIVED/` | Completed, superseded, or consolidated plans | Claude Code (on-demand, for historical context) |
| `_RPI_STANDARDS/plans/` | **Canonical copy** of Platform Roadmaps only (git-tracked, survives machine changes) | Claude Code + anyone reading the repo |
| Shared Drive / Roadmaps | Exported snapshots of roadmaps (Google Docs format, shareable with team) | JDM, team, investors |
| Shared Drive / Session Handoffs | End-of-session context exports | Next Claude Code session |
| Shared Drive / Build Plans | Detailed build specs (shareable format) | JDM, team |
| Shared Drive / Testing Guides | Production testing docs | Testers (Vinnie, Nikki, Matt) |
| Shared Drive / Reference Docs | Compliance, checklists, delegation guides | Team reference |

### Lifecycle Stages

```
#LetsPlanIt
    |
    v
[1. CREATED] ── Feature Plan or Working Plan in ~/.claude/plans/
    |
    v
[2. ACTIVE] ── Being worked. Phases executing. Status updates in-plan.
    |
    ├── Work completes on a feature plan
    |       |
    |       v
    |   [3a. CONSOLIDATE] ── Content folded into Platform Roadmap as a stream.
    |       |                  Original moved to _ARCHIVED/ with header:
    |       |                  "Consolidated into {roadmap} on {date}"
    |       v
    |   [4. ARCHIVED]
    |
    ├── Work completes on a standalone plan (no roadmap to absorb it)
    |       |
    |       v
    |   [3b. COMPLETED] ── All phases done. Header updated with completion date.
    |       |                Moved to _ARCHIVED/.
    |       v
    |   [4. ARCHIVED]
    |
    ├── Plan is replaced by a newer version
    |       |
    |       v
    |   [3c. SUPERSEDED] ── Newer plan exists. Header:
    |       |                "Superseded by {new-plan} on {date}"
    |       |                Moved to _ARCHIVED/.
    |       v
    |   [4. ARCHIVED]
    |
    └── Plan becomes seed for a Platform Roadmap
            |
            v
        [3d. PROMOTED] ── App Plan becomes the first Platform Roadmap
                           for that project. Renamed to {project}-platform-roadmap.md.
                           Copied to _RPI_STANDARDS/plans/.
```

### Archive Rules

**Move to `_ARCHIVED/` when ANY of these are true:**
1. All phases/tasks are complete
2. Content has been consolidated into a Platform Roadmap
3. A newer plan supersedes it
4. Plan hasn't been touched in 30+ days AND isn't referenced by an active roadmap

**Before archiving, ALWAYS:**
1. Add a status header to line 1: `> ARCHIVED: {reason} — {date}` with one of:
   - `Consolidated into {roadmap-name} on {date}`
   - `Superseded by {plan-name} on {date}`
   - `Completed on {date}`
   - `Stale — no activity since {last-modified-date}`
2. Verify the plan's content is captured elsewhere (roadmap stream, session handoff, or standalone completion)

**Never archive without a trace.** The plan's knowledge must survive in at least one active location.

### Platform Roadmap Rules

1. **One per major project.** Currently: PRODASHX, RIIMO, RAPID_IMPORT, _RPI_STANDARDS. Future: SENTINEL, ATLAS, Command Center (when they accumulate enough streams).
2. **Dual-homed.** Active copy in `~/.claude/plans/` + canonical copy in `_RPI_STANDARDS/plans/`. Sync on major updates.
3. **Streams, not monoliths.** Each roadmap is organized into numbered streams. Feature plans become streams when consolidated.
4. **Version history at the top.** Every shipped milestone gets a row in the version table.
5. **Source plan attribution.** Each stream notes which original plan it came from (e.g., "Source plan: `humming-exploring-mochi.md`").

### Shared Drive Export Rules

| When | What Gets Exported | Where |
|------|--------------------|-------|
| End of major session | Session handoff doc (context + next steps) | Session Handoffs |
| Feature ships to production | Testing guide (Google Form + guide doc) | Testing Guides |
| Roadmap milestone | Roadmap snapshot (current state) | Roadmaps |
| New build starts | Build plan (architecture + phases) | Build Plans |
| Never | Raw working plans from ~/.claude/plans/ | N/A — those stay local |

### Maintenance Triggers

Add to CLAUDE.md Documentation Maintenance Triggers:

| When You... | Update These |
|-------------|-------------|
| Complete a feature plan | Consolidate into Platform Roadmap, archive original |
| Create a new plan | Verify a Platform Roadmap exists for that project; if not, this plan may become the seed |
| Ship a production release | Update Platform Roadmap version history |
| Start a new session on a project | Check for stale plans (30+ days untouched) |

---

## Part 2: Immediate Cleanup Actions

Based on the lifecycle rules above, here's what happens to each of the 17 remaining plans:

### Archive Now (3 superseded)

| File | Reason | Superseded By |
|------|--------|---------------|
| `zazzy-meandering-flamingo.md` | Phase 6 Booking | `memoized-stirring-nova.md` (Phase 7 includes Phase 6 cleanup) |
| `pure-bubbling-squirrel.md` | SENTINEL MI Overhaul | `glimmering-baking-clarke.md` (corrected MI Master Plan) |
| `lexical-honking-breeze.md` | ATLAS initial plan | `polymorphic-twirling-hopper.md` (ATLAS v1.3) |

### Consolidate into Platform Roadmaps, Then Archive (4)

| File | Title | Consolidate Into | As Stream |
|------|-------|-----------------|-----------|
| `humming-exploring-mochi.md` | Case Central Package | `prodashx-platform-roadmap.md` | New stream: Case Central / Client Output |
| `declarative-crunching-rainbow.md` | Comms Wiring | `prodashx-platform-roadmap.md` | New stream: Communications Wiring |
| `hidden-juggling-dahl.md` | Performance Refactor | `prodashx-platform-roadmap.md` | New stream: Performance (Unified Matrix Cache) |
| `memoized-stirring-nova.md` | Calendly-Killer (Phase 7) | `riimo-platform-roadmap.md` | New stream: Booking Engine (Phase 6+7) |

### Keep Active — Platform Roadmaps (4)

| File | Stays Because |
|------|---------------|
| `prodashx-platform-roadmap.md` | Active consolidated roadmap |
| `riimo-platform-roadmap.md` | Active consolidated roadmap |
| `rapid-import-platform-roadmap.md` | Active consolidated roadmap |
| `rpi-standards-governance-roadmap.md` | Active consolidated roadmap |

### Keep Active — Working Plans (2)

| File | Stays Because |
|------|---------------|
| `portal-overhaul.md` | Active, phases in progress |
| `deep-nibbling-quiche.md` | Sessions E+F, extends portal-overhaul |

### Keep Active — Standalone App/Project Plans (4)

| File | Title | Why It Stays |
|------|-------|-------------|
| `glimmering-baking-clarke.md` | SENTINEL v2 MI Master Plan | No SENTINEL roadmap yet — this IS the roadmap seed |
| `adaptive-sauteeing-bird.md` | Command Center Roadmap v2.0 | No CC roadmap yet — this IS the roadmap seed |
| `polymorphic-twirling-hopper.md` | ATLAS v1.3 | No ATLAS roadmap yet — this IS the roadmap seed |
| `snoopy-wobbling-sifakis.md` | RPI Connect Enhancement | Cross-portal, standalone until a "Shared Features" roadmap makes sense |

### Post-Cleanup Result: 10 Active Plans

```
~/.claude/plans/
├── _ARCHIVED/                          (43 files — was 36)
├── prodashx-platform-roadmap.md        # Platform Roadmap
├── riimo-platform-roadmap.md           # Platform Roadmap
├── rapid-import-platform-roadmap.md    # Platform Roadmap
├── rpi-standards-governance-roadmap.md # Platform Roadmap
├── portal-overhaul.md                  # Working Plan (active)
├── deep-nibbling-quiche.md             # Working Plan (active)
├── glimmering-baking-clarke.md         # App Plan seed (SENTINEL)
├── adaptive-sauteeing-bird.md          # App Plan seed (Command Center)
├── polymorphic-twirling-hopper.md      # App Plan seed (ATLAS)
└── snoopy-wobbling-sifakis.md          # App Plan seed (RPI Connect)
```

### Sync Platform Roadmaps to _RPI_STANDARDS/plans/

Copy all 4 platform roadmaps to `_RPI_STANDARDS/plans/` (canonical git-tracked copies):
- `prodashx-platform-roadmap.md`
- `riimo-platform-roadmap.md`
- `rapid-import-platform-roadmap.md`
- `rpi-standards-governance-roadmap.md`

(`portal-overhaul.md` is already there.)

---

## Part 3: CLAUDE.md Updates

Add to global CLAUDE.md under Documentation Maintenance Triggers:

```
| Complete a feature plan    | Consolidate stream into Platform Roadmap, archive original |
| Create a new plan          | Check if Platform Roadmap exists for project              |
| Ship a production release  | Update Platform Roadmap version history                   |
```

Add to Session Protocol > Starting:
```
8. Check for stale plans (30+ days untouched in ~/.claude/plans/)
```

---

## Verification

1. `ls ~/.claude/plans/*.md | wc -l` → 10
2. `ls ~/.claude/plans/_ARCHIVED/ | wc -l` → 43
3. `ls ~/Projects/_RPI_STANDARDS/plans/ | wc -l` → 5 (4 roadmaps + portal-overhaul)
4. `cat _RPI_STANDARDS/reference/os/PLAN_LIFECYCLE.md` → exists, complete
5. Each archived file has `> ARCHIVED:` header on line 1
6. Each consolidated stream in the Platform Roadmap has `Source plan:` attribution
7. CLAUDE.md has updated maintenance triggers
