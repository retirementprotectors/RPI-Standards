---
name: CAM Platform Build
overview: Commit CAM's current shell state (HYPO removed since it lives in DAVID-HUB), then build CAM as RPI's internal commission accounting platform starting with the Comp Grid module.
todos:
  - id: commit-shell
    content: Commit CAM shell state (HYPO removal) and cleanup misplaced files
    status: completed
  - id: align-css
    content: Update Styles.html to use RPI Design System colors instead of DAVID green
    status: completed
  - id: comp-grid-backend
    content: Create CAM_CompGrid.gs with MATRIX integration for commission structures
    status: completed
  - id: comp-grid-ui
    content: Build Comp Grid UI section in Index.html with admin controls
    status: completed
  - id: routing-update
    content: Update Code.gs routing for comp grid actions
    status: completed
---

# CAM Internal Commission Platform - Build Plan

## Current State

- DAVID-HUB owns the Partnership Revenue Projector (PRP/HYPO) - deployed v6.1
- CAM has uncommitted changes removing HYPO (correct - it migrated to DAVID-HUB)
- CAM shell is ready to become the internal commission accounting platform

## Phase 0: Cleanup (Immediate)

1. **Commit CAM's current state** - finalize the HYPO removal
2. **Remove misplaced file** - `Docs/SENTINEL_PartnerProjector.gs` (code file in docs folder)
3. **Update CSS colors** - align with RPI Design System (currently uses DAVID green)

## Phase 1: Comp Grid Module

The foundation for all commission calculations.

**What it does:**
- Display carrier commission structures (MAPD, Life, etc.)
- Admin interface to update commission rates
- Tier-based structures (Bronze → Diamond)

**Files:**
- `CAM_CompGrid.gs` - Backend CRUD operations
- Update `Index.html` - Comp Grid UI section
- Update `Code.gs` - Add routing for comp grid actions

## Phase 2: Internal Calculators

**Commission Calculator** - Calculate agent commissions based on:
- Production volume
- Commission tier
- Override structures

## Phase 3+: Future Modules

Per the existing documentation:
- Submitted Business tracking
- NewBiz pipeline management
- Reconciliation (submitted vs paid)
- Commission payments
- Analytics dashboard

## Key Decisions

| Question | Answer |
|----------|--------|
| Where does HYPO/PRP live? | DAVID-HUB (already deployed) |
| What is CAM for? | Internal commission accounting |
| Should we commit the shell? | Yes - it correctly removes migrated code |