---
name: block-github-io-dead-link
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^.*/toMachina.*\.(html|md|txt|json|tsx|ts)$
  - field: content
    operator: regex_match
    pattern: retirementprotectors\.github\.io/toMachina(?!.*github-io-justified)
owner: shinob1
---

🛑 **BLOCKED: dead `retirementprotectors.github.io/toMachina/...` link — GitHub Pages is OFF.**

You're embedding a `retirementprotectors.github.io/toMachina/...` URL. **That URL 404s. Always. Right now.** GitHub Pages is **not enabled** on the `toMachina` repo (`GET /repos/.../pages` → 404; site root, `/docs/`, every path → 404). It was taken down as part of the PHI funnel-privacy lockdown (2026-06-27) — warrior/case docs can't sit on a public web surface.

This is **the #1 brick wall** JDM keeps hitting: a session links a doc via `github.io`, JDM clicks it, dead end. The doc is **alive in the repo** — only the URL convention is dead. There is no permission/authorization problem; the link is born 404.

**Do NOT cite `github.io` for any toMachina doc. Use a surface that actually resolves:**

| You want JDM/the fleet to... | Use |
|---|---|
| Open a doc that lives in `/home/jdm/inbox/**` | `https://mdjserver.tail7845ea.ts.net:8443/inbox/<file>` (tailnet-only, private) |
| Reference a repo doc (`docs/warriors/**`, `docs/discoveries/**`) | the **repo-relative path** (`docs/warriors/shinob1/FOO.html`) — read live; do NOT wrap it in a github.io URL |
| Hand JDM a clickable repo doc | copy it into the inbox first, then cite the `:8443/inbox/<file>` link |

**Why BLOCK, not WARN:** every `github.io` link is a guaranteed dead end for JDM. The cost of a false-positive (one override marker) is trivial; the cost of shipping another brick wall is JDM clicking a 404 — again.

**Genuine exception** (e.g. documenting this very rule, or a one-off where Pages is confirmed re-enabled): append the marker `github-io-justified` on the same line / in the same file.

Why this exists: JDM directive 2026-06-28 ("I have a HUNDRED of these... sessions build a brick wall in front of me despite these protections — The Rules/Hooks + Doctrine are what they are"). Doctrine alone didn't hold because nothing *enforced* it. This is the enforcement. Owner: SHINOB1 (immune system). Companion sweep: repoint existing `github.io/toMachina` links → repo-relative / `:8443/inbox`.
