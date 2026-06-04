---
name: block-client-roadmap-in-portal
enabled: true
event: file
action: block
# 2026-06-02 (SHINOB1): Authored after I built a Client Roadmap as a ProDashX
# React route (apps/prodash/.../roadmap/[clientSlug]/page.tsx + RoadmapShell) —
# the EXACT failure that triggered the entire toMachina2 rebuild. It recurred at
# the finish line because I built to my interpretation of an abstraction instead
# of the real artifact sitting in the repo. This gate makes that structurally
# impossible AND routes the writer to the real template.
conditions:
  - field: file_path
    operator: regex_match
    pattern: apps/[^/]+/.*[Rr]oadmap
  # Exempt a DEPRECATED pointer placed in the old trap dir.
  - field: file_path
    operator: not_contains
    pattern: DEPRECATED
owner: shinob1
---

**BLOCKED: building a Client Roadmap inside a portal app.**

You are writing a roadmap surface under `apps/<portal>/...`. The Client Roadmap
is NOT a portal route or a React component. It is a **standalone HTML surface**
that REPLACES the portal (the deprecated CRM concept) — the Center-of-the-Universe
surface you ACT FROM.

**The real artifact — start here, always (do not build, FILL):**
- Canonical template: `docs/cases/_client-roadmap-template.html`
- Driven by ONE `casework-import` JSON blob (client_id, household, contracts,
  `mounted_components`) — the page renders itself from the blob.
- Governed by `docs/templates/REGISTRY.md` — 3 Stages (PROSPER / PRESERVE /
  PROTECT), 8 VIEWs, 3 Story 1-Pagers, The RPI Way™.
- Existing examples: `docs/cases/griffin-roadmap.html`, `matt-mitchell-roadmap.html`,
  `leiting-roadmap.html`, `vandevort-roadmap.html`.

**The engine's only job:** assemble the `casework-import` JSON from the index →
inject into the canonical template → write a standalone roadmap HTML, identical in
kind to the ones already in `docs/cases/`. No React, no portal, no route.

**The root rule this enforces:** ground in the real artifact before building
anything that may already exist. The template was in the repo the whole time.
(JDM directive 2026-06-01.)
