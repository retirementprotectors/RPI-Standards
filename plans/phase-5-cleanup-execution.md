# Phase 5: Cleanup — Execution Plan

> Depends on: Phase 4 complete (GAS engines thinned, portals archived, bridge adapted)
> Master plan: `~/.claude/plans/valiant-napping-waterfall.md` (lines 425-488)

---

## Overview

Phase 5 is housekeeping. The platform is built (Phases 0-3), the old systems are thinned (Phase 4). Now we clean up the development environment, documentation, governance rules, and local infrastructure to reflect the new reality.

**This phase has NO production code changes.** It's docs, configs, scripts, and folder reorganization.

---

## Sub-Phase 5a: Local Folder Reorganization

### Target Structure
```
~/Projects/
├── _RPI_STANDARDS/              # Standards + governance (updated)
├── toMachina/                   # THE monorepo
│   ├── apps/prodash/
│   ├── apps/riimo/
│   ├── apps/sentinel/
│   ├── packages/ui/core/auth/db/
│   ├── services/api/bridge/
│   └── CLAUDE.md
├── gas/                         # GAS engines (Sheets automation only)
│   ├── RAPID_CORE/
│   ├── RAPID_FLOW/
│   ├── RAPID_IMPORT/
│   ├── RAPID_COMMS/
│   ├── ATLAS/
│   ├── CAM/
│   ├── DEX/
│   └── C3/
├── services/                    # Standalone backend services
│   ├── MCP-Hub/
│   ├── PDF_SERVICE/
│   ├── QUE-API/                 # healthcare-mcps (Cloud Run)
│   └── Marketing-Hub/
└── archive/                     # Pre-toMachina projects (read-only)
    ├── PRODASHX/
    ├── RIIMO/
    ├── sentinel-v2/
    ├── sentinel-v1/
    ├── DAVID-HUB/
    ├── CEO-Dashboard/
    └── RPI-Command-Center/
```

### Steps
1. Create new directory structure:
   ```bash
   mkdir -p ~/Projects/gas
   mkdir -p ~/Projects/services
   mkdir -p ~/Projects/archive
   ```

2. Move GAS engine projects to `gas/`:
   ```bash
   mv ~/Projects/RAPID_TOOLS/RAPID_CORE ~/Projects/gas/RAPID_CORE
   mv ~/Projects/RAPID_TOOLS/RAPID_FLOW ~/Projects/gas/RAPID_FLOW
   mv ~/Projects/RAPID_TOOLS/RAPID_IMPORT ~/Projects/gas/RAPID_IMPORT
   mv ~/Projects/RAPID_TOOLS/RAPID_COMMS ~/Projects/gas/RAPID_COMMS
   mv ~/Projects/RAPID_TOOLS/ATLAS ~/Projects/gas/ATLAS
   mv ~/Projects/RAPID_TOOLS/CAM ~/Projects/gas/CAM
   mv ~/Projects/RAPID_TOOLS/DEX ~/Projects/gas/DEX
   mv ~/Projects/RAPID_TOOLS/C3 ~/Projects/gas/C3
   ```

3. Move standalone services:
   ```bash
   mv ~/Projects/RAPID_TOOLS/MCP-Hub ~/Projects/services/MCP-Hub
   mv ~/Projects/RAPID_TOOLS/PDF_SERVICE ~/Projects/services/PDF_SERVICE
   mv ~/Projects/RAPID_TOOLS/Marketing-Hub ~/Projects/services/Marketing-Hub
   # QUE-API is inside MCP-Hub/healthcare-mcps — stays there
   ```

4. Move archived projects (Phase 4a already moved portals):
   ```bash
   # Verify archive/ has: PRODASHX, RIIMO, sentinel-v2
   mv ~/Projects/SENTINEL_TOOLS/sentinel ~/Projects/archive/sentinel-v1
   mv ~/Projects/SENTINEL_TOOLS/DAVID-HUB ~/Projects/archive/DAVID-HUB
   mv ~/Projects/RAPID_TOOLS/CEO-Dashboard ~/Projects/archive/CEO-Dashboard
   mv ~/Projects/RAPID_TOOLS/RPI-Command-Center ~/Projects/archive/RPI-Command-Center
   ```

5. Clean up empty parent directories:
   ```bash
   # Only after verifying everything moved successfully
   rmdir ~/Projects/RAPID_TOOLS 2>/dev/null || echo "RAPID_TOOLS not empty — check remaining contents"
   rmdir ~/Projects/SENTINEL_TOOLS 2>/dev/null || echo "SENTINEL_TOOLS not empty — check remaining contents"
   rmdir ~/Projects/PRODASHX_TOOLS 2>/dev/null || echo "PRODASHX_TOOLS not empty — check remaining contents"
   ```

### Verification
- [ ] `ls ~/Projects/` shows: _RPI_STANDARDS, toMachina, gas, services, archive
- [ ] `ls ~/Projects/gas/` shows 8 GAS projects
- [ ] `ls ~/Projects/services/` shows MCP-Hub, PDF_SERVICE, Marketing-Hub
- [ ] `ls ~/Projects/archive/` shows 7 archived projects
- [ ] All git repos still have their remotes (`git remote -v` in each)
- [ ] All .clasp.json files still have correct script IDs
- [ ] clasp push still works from new paths (test with one project)

### Builder Assignment: **Builder 1** (owns main, knows the repo structure)
**Effort: ~30 minutes**

---

## Sub-Phase 5b: CLAUDE.md Reduction

### What Gets Removed (~260 lines from global CLAUDE.md)

| Section | Lines | Why Remove |
|---------|-------|-----------|
| GAS Gotchas (all 14 items) | ~120 | No longer building GAS frontends. GAS engines use frozen patterns. |
| 6-Step Deploy process | ~20 | toMachina uses auto-deploy (push → CI → Cloud Run). GAS deploys are rare maintenance-only. |
| clasp-specific rules | ~15 | Reduced to a note: "GAS projects in ~/Projects/gas/ use clasp for rare maintenance deploys" |
| `appsscript.json` access control rules | ~10 | Archived projects disabled. Active GAS projects already configured. |
| GAS Self-Check checklists (commit + deploy) | ~30 | Replaced by CI/CD pipeline + TypeScript compiler |
| GAS Function Execution via execute_script (detailed section) | ~15 | Reduced to a note referencing MCP-Hub docs |
| GAS Editor Instructions (MANDATORY) | ~10 | JDM rarely touches GAS editor now |
| GAS Project Session Start protocol | ~15 | Replaced by toMachina session start |
| Deploy Report format | ~10 | Auto-deploy, no manual report needed |
| GAS Gotchas (additions in MEMORY.md) | ~10 | Move to archive reference doc |

### What Gets Added

| Section | Content |
|---------|---------|
| toMachina Platform | Architecture overview, monorepo structure, dev commands |
| toMachina Deploy | "Push to main → auto-deploy. That's it." |
| Builder/Auditor Protocol | Reference to `toMachina/.claude/AUDITOR_PROTOCOL.md` |
| GAS Maintenance Mode | "GAS projects in ~/Projects/gas/ are in maintenance mode. Use clasp for rare deploys. Business logic lives in toMachina packages/core." |
| Updated Project Locations | New folder structure tree |
| Updated Session URLs | toMachina portal URLs, Firebase Console, GitHub |

### What Gets Updated

| Section | Change |
|---------|--------|
| Three-Platform Architecture | Add toMachina URLs, update portal descriptions |
| Project Locations tree | Replace 27-repo tree with new 4-directory structure |
| Available MCP Tools | Add callCloudRunAPI pattern, update routing notes |
| Code Standards | Merge GAS standards (frozen) with TypeScript standards (active) |
| Session Protocol | Update to toMachina-first workflow |

### Steps
1. Read current global CLAUDE.md
2. Create a backup: `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.pre-phase5`
3. Remove the ~260 lines identified above
4. Add the new sections
5. Update the modified sections
6. Verify no broken references

### Verification
- [ ] Global CLAUDE.md is shorter (target: ~400-500 lines, down from ~700+)
- [ ] No references to deleted sections from other docs
- [ ] toMachina project CLAUDE.md has all necessary project-specific context
- [ ] Session start protocol references toMachina first, GAS second

### Builder Assignment: **Builder 1** (owns CLAUDE.md, understands the full context)
**Effort: ~1.5 hours** (careful editing, not coding)

---

## Sub-Phase 5c: Hookify Rule Pruning

### Rules to Remove (15)

| Rule | Why Remove |
|------|-----------|
| `block-forui-no-json-serialize` | GAS serialization bug. Not relevant in TypeScript/React. |
| `block-let-module-caching` | GAS `var` vs `let` caching. Not relevant in ES modules. |
| `block-hardcoded-colors` | Tailwind + CSS variables handle this in toMachina. |
| `warn-date-return-no-serialize` | GAS Date serialization. Firestore Timestamps don't have this bug. |
| `warn-modal-no-flexbox` | React Modal component already implements flexbox scroll. |
| `block-alert-confirm-prompt` | React components use Toast/ConfirmDialog. No alert() possible. |
| `warn-plain-person-select` | SmartLookup is a React component in @tomachina/ui. |
| `warn-missing-structured-response` | TypeScript interfaces enforce return types. |
| `block-direct-matrix-write` | Bridge handles all writes. Direct Sheets writes are GAS-only (frozen). |
| `block-hardcoded-matrix-ids` | Firestore collection names, not Sheets IDs. |
| `block-anyone-anonymous-access` | Firebase Auth + Firestore rules handle access. No GAS web app deploy. |
| `block-drive-url-external` | toMachina uses Firestore, not Drive URLs. |
| `quality-gate-deploy-verify` | Auto-deploy pipeline. No manual deploy verification needed. |
| `quality-gate-commit-remind` | CI/CD handles build verification. |
| `intent-sendit` | Simplified deploy — just push to main. |

### Rules to Keep (13)

| Rule | Why Keep |
|------|---------|
| `block-hardcoded-secrets` | Universal — applies to ALL code |
| `block-credentials-in-config` | Universal |
| `block-phi-in-logs` | Universal — PHI rules never change |
| `warn-phi-in-error-message` | Universal |
| `warn-inline-pii-data` | Universal |
| `intent-session-start` | Still needed — triggers session protocol |
| `intent-immune-system-check` | Still needed — compliance briefing |
| `intent-plan-mode` | Still needed — #LetsPlanIt trigger |
| `intent-execute-plan` | Still needed — #LetsRockIt trigger |
| `intent-atlas-consult` | Still needed — data import/migration |
| `quality-gate-phase-complete` | Useful for toMachina phase tracking |
| `quality-gate-audit-verify` | Useful for builder/auditor workflow |
| `quality-gate-plan-format` | Useful for plan quality |

### New Rules to Consider

| Rule | Purpose |
|------|---------|
| `block-any-type` | Block `any` in TypeScript files (enforce strict typing) |
| `warn-no-auth-middleware` | Warn if new API routes don't apply requireAuth |
| `quality-gate-builder-report` | Remind builders to write reports per auditor protocol |

### Steps
1. Remove 15 hookify rule files from `_RPI_STANDARDS/hookify/`
2. Remove corresponding symlinks from all active projects
3. Update `setup-hookify-symlinks.sh` to reflect new rule list + new project paths
4. Optionally create 1-3 new toMachina-specific rules
5. Run `setup-hookify-symlinks.sh` to verify clean state

### Verification
- [ ] 13 rules remain in `_RPI_STANDARDS/hookify/`
- [ ] All active projects have correct symlinks (toMachina + 8 GAS projects)
- [ ] No orphan symlinks in archived projects
- [ ] `setup-hookify-symlinks.sh` runs clean

### Builder Assignment: **Builder 3** (understands the rule system from porting entitlements)
**Effort: ~1 hour**

---

## Sub-Phase 5d: Maintenance Script Updates

### Scripts to Update

| Script | Change |
|--------|--------|
| `clone-all-repos.sh` | Update paths: 27 repos → ~14 active repos in new directory structure |
| `setup-hookify-symlinks.sh` | Update project list: remove archived, add toMachina, update paths to `gas/` |
| `machine-check.sh` | Update project paths, add toMachina health checks (build status, deploy status) |
| `machine-check-hook.sh` | Same path updates |

### Docs to Update

| Document | Change |
|----------|--------|
| `MONITORING.md` | Update project list, add toMachina monitoring (Cloud Run health, Firebase status) |
| `POSTURE.md` | Update verification table: remove GAS web apps, add Cloud Run services |
| `IMMUNE_SYSTEM.md` | Update rule count (28 → 13-16), add toMachina-specific enforcement |
| `OPERATIONS.md` | Update deploy procedures, add toMachina deploy section |

### Steps
1. Update each script with new paths
2. Update each doc with new project lists
3. Test `clone-all-repos.sh` on a clean machine (or dry-run)
4. Test `setup-hookify-symlinks.sh`
5. Verify `machine-check.sh` reports green

### Verification
- [ ] `clone-all-repos.sh` clones all active repos to correct paths
- [ ] `setup-hookify-symlinks.sh` links rules to all active projects
- [ ] `machine-check.sh` reports ALL GREEN
- [ ] MONITORING.md lists all active projects with correct paths
- [ ] POSTURE.md verification table matches current deployment state

### Builder Assignment: **Builder 1** (owns _RPI_STANDARDS, knows the maintenance scripts)
**Effort: ~1 hour**

---

## Sub-Phase 5e: Launchd Agent Migration

### Agent Disposition

| Agent | Current | After | Action |
|-------|---------|-------|--------|
| `com.rpi.document-watcher` | Local polling (always-on) | Cloud Run + Pub/Sub trigger | Create Cloud Function triggered by Drive changes. Disable launchd agent. |
| `com.rpi.analytics-push` | Daily 3:30am cron | Firestore → BigQuery change stream | Already automatic if BigQuery export extension is enabled. Disable launchd agent. |
| `com.rpi.mcp-analytics` | Monday 8am cron | KEEP | MCP analytics are local. No change. |
| `com.rpi.claude-cleanup` | Sunday 3am cron | KEEP | Local session cleanup. No change. |
| `com.rpi.knowledge-promote` | Daily 4am cron | KEEP | Local MEMORY → CLAUDE.md promotion. No change. |

### Steps
1. Verify BigQuery export extension is active (Phase 4 / Builder 2 set this up)
2. If active: disable `com.rpi.analytics-push` launchd agent
3. Document-watcher migration is a larger task — create a Cloud Function:
   - Trigger: Google Drive webhook (or Pub/Sub from Drive changes)
   - Logic: same as current watcher.js but runs on Cloud Run
   - This can be a future task if the current local watcher still works
4. Keep the 3 local-only agents running

### Verification
- [ ] `com.rpi.analytics-push` disabled (if BigQuery export handles it)
- [ ] `com.rpi.mcp-analytics` still runs Monday 8am
- [ ] `com.rpi.claude-cleanup` still runs Sunday 3am
- [ ] `com.rpi.knowledge-promote` still runs daily 4am

### Builder Assignment: **Builder 2** (owns infrastructure, set up BigQuery export)
**Effort: ~30 minutes** (document-watcher Cloud Function is deferred)

---

## Sub-Phase 5f: MEMORY.md Cleanup

### What Changes
- Remove GAS-specific gotchas that are now in archive reference
- Update project references to new paths
- Add toMachina session notes (builder/auditor workflow, etc.)
- Remove stale entries that reference archived projects

### Builder Assignment: **Auditor** (has full context across all sessions)
**Effort: ~30 minutes**

---

## Builder Lane Assignments (Summary)

| Builder | Sub-Phases | Est. Time |
|---------|-----------|-----------|
| **Builder 1** | 5a (folder reorg) + 5b (CLAUDE.md reduction) + 5d (maintenance scripts) | 3 hours |
| **Builder 2** | 5e (launchd agents) | 30 minutes |
| **Builder 3** | 5c (hookify pruning) | 1 hour |
| **Auditor** | 5f (MEMORY.md cleanup) + verify all sub-phases | 1 hour |

**Note:** Phase 5 is lighter than Phase 4. Builder 1 has the most work (docs + scripts). Builders 2 and 3 could take on Phase 4 work in parallel if Phase 5 is combined with Phase 4 in a single session.

---

## JDM Manual Steps

| Step | When | Duration |
|------|------|----------|
| Review CLAUDE.md changes before they go live | After 5b | 10 minutes — this is YOUR operating manual |
| Verify toMachina portals after folder reorg | After 5a | 2 minutes |
| Approve hookify rule removal list | Before 5c | Business decision |

---

## Combined Phase 4+5 Builder Lanes (If Running Together)

Since Phase 5 is light, it can be combined with Phase 4 in a single session:

| Builder | Phase 4 | Phase 5 | Total Est. |
|---------|---------|---------|-----------|
| **Builder 1** | 4a (archive portals) + 4e (archive app UIs) | 5a (folder reorg) + 5b (CLAUDE.md) + 5d (scripts) | 4-5 hours |
| **Builder 2** | 4b (complete API port) + 4f (RAPID_IMPORT bridge) + MCP | 5e (launchd agents) | 4-5 hours |
| **Builder 3** | 4d (thin RAPID_CORE) | 5c (hookify pruning) | 3-4 hours |
