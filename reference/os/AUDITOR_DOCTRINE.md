# AUDITOR DOCTRINE — Completeness & the Live-Reality Law

> Canonical. Codified 2026-06-17 (SHINOB1, JDM-directed). Earned across the overnight
> BoB-Machine + RSA-ITP dual-EPIC: one law, proven by six catches in a single night —
> every one caught a defect *before it shipped*, several on the auditors' own claims.
> Supersedes the scattered `AUDITOR-DOCTRINE-001` clauses in the warrior templates
> (which now reference this file).

---

## 1. The Completeness Auditor

**A green PR is NOT "done."** Every scope closes only when its **independent completeness
auditor** signs it 100%.

- The auditor is the **scope-author** (the disco-sub that wrote the scope) — **never the
  builder.** Author ≠ builder is non-negotiable; self-audit is not audit.
- The auditor **takes the contract back after the build**, works the builder to close
  every gap, then signs `auditor_signed: <name>` in the PR's `shipped_refs` (signer ≠ builder).
- The auditor's **death-gate is HELD** until: **every ticket** in the contract shipped
  **+ CI green + LIVE-verified** (see §3). The builder's job ends at "PR green + auditor
  notified," never at self-close.

This kills "shipped = opened a PR and bailed" and "shipped = 20% of the tickets done."

---

## 2. THE LAW — Verify the Live Reality, Not the Static/Code Artifact

> **The merged/registered/written artifact is not the running truth. Verify the running truth.**

Three states, all must be green, never conflated: **merged ≠ deployed ≠ live-verified.**

This law earned its keep six times in one night — and caught its own authors three of those
times (the doctrine is load-bearing precisely because it binds even the auditor):

1. **Live-render bar** — code merged ≠ surface live. (SV2 grid: merged + green, still 404.)
2. **curl-200, registered ≠ serving** — a route in source/manifest is not a mounted route.
   (Dead `ROUTE_MANIFEST`: registered everywhere, served nowhere → silent 404.)
3. **Fail-loud over silent** — a documented enforcement that isn't wired IS the bug.
   (The "auto-loaded by server.ts" docstring was a lie; this very guard, §4, was
   claimed-but-never-built until this codification.)
4. **Prior-art sweeps LIVE SURFACES, not just code** — checking the codebase misses a
   re-invent of an *existing live surface*. (E3 nearly rebuilt VOLTRON's live DIPSet board.)
5. **200 ≠ 200-with-DATA; verify the SA can READ** — an endpoint returning 200-empty may be
   a *provisioning gap* (the service-account lacks the data-source grant), not "no data."
   (partner_rpi /revenue served empty-200 until the tm-api SA got BQ READER.)
6. **The auth gate masks the answer** — an unauth/IAM 401 is returned for mounted AND
   unmounted routes alike (the parent `requireAuth` fires before routing). 401-not-404 is
   *suggestive*, never conclusive. Only an **authed 200/data** proves mounted + serving.

The recurring failure mode: a **proxy for the truth** (the directory instead of the SSOT;
the unauth curl instead of the authed one; the code instead of the live surface) read as if
it were the truth. Always verify the **real source / the live surface / the authed path**.

---

## 3. The Completeness Bar, by Deliverable Type

The auditor signs only after the **live** check for the deliverable's type:

| Deliverable | Completeness check (LIVE, not static) |
|---|---|
| **API / endpoint** | authed **curl-200 with DATA** against the deployed surface. `registered ≠ mounted+serving`; `200 ≠ 200-with-data`; an unauth/IAM 401 proves nothing (auth gates before routing). |
| **Surface / UI** | live-render co-sign on the **deployed** URL (token-clean + honest-empty where no data, no fake-green) — not a local/branch render, not "code merged." For a multi-view surface, verify **EACH tab/route mounts its DISTINCT real content** — a front-door 200 proves nothing about the tabs. (RSA-ITP E4: a registry shipped every real module to main yet mapped every tab to a stub — code-correct + bundle-current + Firestore-empty still rendered stubs. **Built ≠ wired**: the registry rewire was the missing tissue.) And for a surface that makes AUTHED API calls, render-mount is necessary but NOT sufficient — verify the authed call SUCCEEDS live; the non-auth render harness proves the mount but cannot make the call, so a 401 hides behind a clean render. (RSA-ITP Coach: E5 passed the per-tab render co-sign — the chat UI painted — but POST /api/rsa-itp/coach 401'd on a real login because the client never attached the Bearer token. Proof = the POST flipping 401→200 in the API logs, not a render.) |
| **Data surface** | the producing run actually wrote, AND the consumer's service-account can READ the data-source (provisioning grant present) → 200-**with-data**. |
| **Route mount** | boot **fail-loud assertion** proves it mounted (a registry that nothing consumes is dead); a non-mounted route must THROW at boot, never silently 404. |
| **New build vs prior-art** | prior-art audit sweeps **live surfaces** (funnel boards / the living-surface-registry), not just code — confirm no existing live surface already does it. |

Source-of-truth discipline: verify against the **SSOT** (Firestore users for RPI-people;
the live deployed surface for "is it serving"), never a proxy (the Workspace directory, a
local boot, the merge state).

---

## 4. The Teeth — `death-gate.sh` Guard (Enforcement)

The doctrine is only real if it's **enforced at the tool**. `death-gate.sh` (the close
primitive) MUST refuse to close a scope unless:

1. the handoff PR is **merged + CI-green**, AND
2. the scope carries an **`auditor_signed:`** record, AND
3. the signer **≠ the builder**.

Missing any → the gate **refuses (fail-loud)**, not "warns and closes." A close-without-the-
record is exactly the "claimed-but-unenforced" anti-pattern this doctrine exists to kill.
(Override for genuinely exceptional closes is explicit + logged, never silent.)

---

## 5. The Class-Fixes (rot-proofing, zero-config defaults)

Each instance of the law gets a **structural** fix so it can't recur — opt-out by config,
never opt-in:

- **Manifest loader + fail-loud boot-assertion** — every `ROUTE_MANIFEST` entry resolves +
  mounts at boot, else THROW. No route can silently die.
- **Living-surface-registry** — prior-art audit's live-surface source (boards/funnel), so a
  re-invent of an existing surface is caught at scope-time.
- **Partner-dataset provisioning auto-grant** — `onboard-partner` auto-grants the tm-api SA
  BQ READER on every `partner_<slug>`, so no partner's surface is silently-empty.
- **curl-200-with-data step** in endpoint audits (+ ideally a CI assertion).

---

🥷 — SHINOB1, CTO. Earned the hard way, one night, six times. Verify the live reality.
