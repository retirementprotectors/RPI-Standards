---
name: block-case-roadmap-in-repo
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/cases/(?!_client-roadmap-template\.html$).+\.(html|pdf)$
owner: shinob1
---

🛑 **BLOCKED: Client case file written under `docs/cases/` — PHI/PII PUBLIC-EXPOSURE risk**

> Locked 2026-06-12 after a P0 breach: `retirementprotectors/toMachina` was a PUBLIC repo serving GitHub Pages from repo-root, and **28 client case files under `docs/cases/` were live on the open internet** (roadmaps with names/DOBs/acct#s/balances + carrier illustration PDFs). Found by VOLTRON-PARKS, tourniquet'd by SHINOB1 (repo→private). This gate is item 4 of the remediation — the enforcement layer.

**Client case roadmaps + illustrations are PHI. They live in the inbox/funnel ONLY — NEVER committed to the toMachina repo**, because anything in `docs/cases/` can hit GitHub Pages and become public.

- ❌ `docs/cases/<client>-roadmap.html`
- ❌ `docs/cases/<client>-client-summary.html`
- ❌ `docs/cases/illustrations/<client>-*.pdf`
- ❌ `docs/cases/assets/<client>/*.pdf`

**Where case roadmaps belong instead:**
- Per-case worktree (private) for working state, AND
- `/home/jdm/inbox/!VOLTRON DOCS!/!Cases/<Case>/` + served via the mdj-agent funnel (auth-gated), where the sister-pill nav already points.

**Allowed in `docs/cases/`:** `_client-roadmap-template.html` (the PII-free template) and brand assets (`assets/*.png|jpg`).

If you genuinely need to surface a case artifact, deliver a **funnel/Pages link to the inbox copy**, never the raw PHI and never a repo commit. See [[feedback_pages_publish_holds_commission_legal]] + the VOLTRON `case-roadmaps-never-to-docs-cases` memory.
