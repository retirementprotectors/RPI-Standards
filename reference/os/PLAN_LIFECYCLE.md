# Plan Lifecycle — Governance & Rules

> Part of The Operating System. Governs how plans are created, evolve, consolidated, and archived.
> Last updated: 2026-03-08

---

## Plan Categories

| Category | What It Is | Naming Convention | Example |
|----------|-----------|-------------------|---------|
| **Platform Roadmap** | Consolidated master plan per major project/platform. Absorbs feature plans as "streams." One per project. | `{project}-platform-roadmap.md` | `prodashx-platform-roadmap.md` |
| **Working Plan** | Active implementation plan for a specific body of work. Has phases, checkpoints, acceptance criteria. | Descriptive slug or auto-generated name | `portal-overhaul.md` |
| **Feature Plan** | Individual feature build. Gets created via `#LetsPlanIt`, executed, then either folded into a Platform Roadmap as a stream or archived standalone. | Auto-generated name | `humming-exploring-mochi.md` |
| **App Plan** | Standalone project plan for an App (ATLAS, Command Center, etc.) that doesn't have a Platform Roadmap yet. Becomes the seed for one if the app grows. | Auto-generated or descriptive | `polymorphic-twirling-hopper.md` |

---

## Plan Locations

| Location | What Lives Here | Who Reads It |
|----------|----------------|-------------|
| `~/.claude/plans/` | ALL active plans (Platform Roadmaps, Working Plans, Feature Plans, App Plans) | Claude Code (every session) |
| `~/.claude/plans/_ARCHIVED/` | Completed, superseded, or consolidated plans | Claude Code (on-demand, for historical context) |
| `_RPI_STANDARDS/plans/` | **Canonical copy** of Platform Roadmaps only (git-tracked, survives machine changes) | Claude Code + anyone reading the repo |
| Shared Drive / Roadmaps | Exported snapshots of roadmaps (Google Docs format, shareable with team) | JDM, team, investors |
| Shared Drive / Session Handoffs | End-of-session context exports | Next Claude Code session |
| Shared Drive / Build Plans | Detailed build specs (shareable format) | JDM, team |
| Shared Drive / Testing Guides | Production testing docs | Testers (Vince, Nikki, Matt) |
| Shared Drive / Reference Docs | Compliance, checklists, delegation guides | Team reference |

---

## Lifecycle Stages

```
#LetsPlanIt
    |
    v
[1. CREATED] -- Feature Plan or Working Plan in ~/.claude/plans/
    |
    v
[2. ACTIVE] -- Being worked. Phases executing. Status updates in-plan.
    |
    |-- Work completes on a feature plan
    |       |
    |       v
    |   [3a. CONSOLIDATE] -- Content folded into Platform Roadmap as a stream.
    |       |                  Original moved to _ARCHIVED/ with header:
    |       |                  "Consolidated into {roadmap} on {date}"
    |       v
    |   [4. ARCHIVED]
    |
    |-- Work completes on a standalone plan (no roadmap to absorb it)
    |       |
    |       v
    |   [3b. COMPLETED] -- All phases done. Header updated with completion date.
    |       |                Moved to _ARCHIVED/.
    |       v
    |   [4. ARCHIVED]
    |
    |-- Plan is replaced by a newer version
    |       |
    |       v
    |   [3c. SUPERSEDED] -- Newer plan exists. Header:
    |       |                "Superseded by {new-plan} on {date}"
    |       |                Moved to _ARCHIVED/.
    |       v
    |   [4. ARCHIVED]
    |
    +-- Plan becomes seed for a Platform Roadmap
            |
            v
        [3d. PROMOTED] -- App Plan becomes the first Platform Roadmap
                           for that project. Renamed to {project}-platform-roadmap.md.
                           Copied to _RPI_STANDARDS/plans/.
```

---

## Archive Rules

**Move to `_ARCHIVED/` when ANY of these are true:**

1. All phases/tasks are complete
2. Content has been consolidated into a Platform Roadmap
3. A newer plan supersedes it
4. Plan hasn't been touched in 30+ days AND isn't referenced by an active roadmap

**Before archiving, ALWAYS:**

1. Add a status header to line 1: `> ARCHIVED: {reason} -- {date}` with one of:
   - `Consolidated into {roadmap-name} on {date}`
   - `Superseded by {plan-name} on {date}`
   - `Completed on {date}`
   - `Stale -- no activity since {last-modified-date}`
2. Verify the plan's content is captured elsewhere (roadmap stream, session handoff, or standalone completion)

**Never archive without a trace.** The plan's knowledge must survive in at least one active location.

---

## Platform Roadmap Rules

1. **One per major project.** Currently: PRODASHX, RIIMO, RAPID_IMPORT, _RPI_STANDARDS. Future: SENTINEL, ATLAS, Command Center (when they accumulate enough streams).
2. **Dual-homed.** Active copy in `~/.claude/plans/` + canonical copy in `_RPI_STANDARDS/plans/`. Sync on major updates.
3. **Streams, not monoliths.** Each roadmap is organized into numbered streams. Feature plans become streams when consolidated.
4. **Version history at the top.** Every shipped milestone gets a row in the version table.
5. **Source plan attribution.** Each stream notes which original plan it came from (e.g., "Source plan: `humming-exploring-mochi.md`").

---

## Shared Drive Export Rules

| When | What Gets Exported | Where |
|------|--------------------|-------|
| End of major session | Session handoff doc (context + next steps) | Session Handoffs |
| Feature ships to production | Testing guide (Google Form + guide doc) | Testing Guides |
| Roadmap milestone | Roadmap snapshot (current state) | Roadmaps |
| New build starts | Build plan (architecture + phases) | Build Plans |
| Never | Raw working plans from ~/.claude/plans/ | N/A -- those stay local |

---

## Maintenance Triggers

These are mirrored in CLAUDE.md under Documentation Maintenance Triggers:

| When You... | Update These |
|-------------|-------------|
| Complete a feature plan | Consolidate stream into Platform Roadmap, archive original |
| Create a new plan | Verify a Platform Roadmap exists for that project; if not, this plan may become the seed |
| Ship a production release | Update Platform Roadmap version history |
| Start a new session on a project | Check for stale plans (30+ days untouched) |
