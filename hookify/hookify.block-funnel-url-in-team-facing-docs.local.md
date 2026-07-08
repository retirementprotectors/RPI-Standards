---
name: block-funnel-url-in-team-facing-docs
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^.*toMachina/docs/(cases|brochures|client-deliverables|public)/.*\.(html|md)$
  - field: content
    operator: regex_match
    pattern: mdjserver\.tail7845ea\.ts\.net
owner: shinob1
---

**BLOCKED: Tailscale Funnel URL detected in team-facing document.**

You are embedding a `mdjserver.tail7845ea.ts.net/...` URL inside a document that the IRL team will see. The team doesn't have Tailscale clients on their machines, and even though Funnel URLs are technically reachable as public anycast, the optics are wrong (the URL looks internal/private).

**Per JDM directive 2026-05-15** — team-facing means an **auth-gated portal route** or delivery **through the AgentX app**, never Funnel. (A `retirementprotectors.github.io/...` URL is NOT an option: GitHub Pages 404s since the 2026-06-27 PHI funnel-privacy lockdown, and `block-github-io-dead-link` blocks it. This remedy was reconciled 2026-07-08 — GV2 WS-A conflict #1 — so it no longer points at the exact dead URL the sibling rule blocks.)

**Detected pattern:** `mdjserver\.tail7845ea\.ts\.net`

**What to use instead:**

The public-`github.io`-Pages flow (`inbox-to-pages.sh` → a `github.io` URL) is **retired** — Pages
was taken down in the 2026-06-27 PHI funnel-privacy lockdown, so that URL is born-404 AND blocked by
`block-github-io-dead-link`. For a team-facing artifact, deliver through an **auth-gated surface**:

- **Auth-gated portal route** (ProDash / RIIMO / SENTINEL) — the team signs in; the artifact is served behind entitlement, not a public URL.
- **The AgentX app** — the sanctioned team + partner delivery surface (2-way Dojo / dashboards).
- For a doc that lives in the repo, reference the **repo-relative path** (`toMachina/docs/...`), not a public URL — the doc is alive in the repo even though the public URL convention is dead.

Never embed the Funnel URL (`mdjserver.tail7845ea.ts.net`) in a team-facing doc.

> **STAGED / GV2 WS-A #1 — for JDM/HIKARI review:** the exact concrete team-facing delivery mechanism
> (which portal route / app surface for case PDFs) should be confirmed at bless; this reconcile removes
> the dead+blocked `github.io` recommendation regardless of that choice.

**Scope of this rule:**

Fires on writes to any of:
- `toMachina/docs/cases/*.html` / `.md`
- `toMachina/docs/brochures/*.html` / `.md`
- `toMachina/docs/client-deliverables/*.html` / `.md`
- `toMachina/docs/public/*.html` / `.md`

These are the team-facing surfaces. Warrior-only artifacts (e.g. `docs/discoveries/*.html`, `docs/warriors/<name>/*`) are NOT subject to this rule — funnel URLs are fine in warrior-internal artifacts.

**Rationale:**

Two case roadmaps shipped with funnel URLs that the team can't reach (`riesberg-roadmap.html` + `welter-roadmap.html`). PR #1197 added the doctrine + helper. This rule turns the doctrine into enforcement so the next warrior who tries to embed a funnel URL into a team-facing doc gets blocked at write time, not at PR review.

**Doctrine reference:** `toMachina/docs/warriors/shinob1/handoff-schema.md` → "Audience Rule — TEAM-FACING ARTIFACTS"

**Rollback:** Set `enabled: false` in this frontmatter, or delete this rule file.
