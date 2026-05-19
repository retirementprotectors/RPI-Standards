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

**Per JDM directive 2026-05-15** — team-facing means clean public URLs (GitHub Pages or auth-gated portal route), never Funnel.

**Detected pattern:** `mdjserver\.tail7845ea\.ts\.net`

**What to use instead:**

Use `scripts/inbox-to-pages.sh` to copy the inbox artifact into the toMachina docs tree:

```bash
scripts/inbox-to-pages.sh \
  "/home/jdm/inbox/!VOLTRON DOCS!/!Cases/Riesberg Case/Statement.pdf" \
  riesberg \
  "statement.pdf"

# stdout: https://retirementprotectors.github.io/toMachina/docs/cases/assets/riesberg/statement.pdf
```

Embed THAT URL in the team-facing doc, not the Funnel URL.

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
