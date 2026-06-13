# HIPAA + InfoSec Compliance Framework — v1 (the SPINE)

**Owner:** 🥷 SHINOB1 (CTO) · **Controls woven by:** 🏯 MEGAZORD (Posture/Standards/Operations) · **Date:** 2026-06-13
**Status:** **CANONICAL** — landed 2026-06-13 (JDM GO). The compliance SSOT; Standards / Posture / Operations thread the HIPAA lens and **cite this spine, never re-derive it.**
**Lens for:** the entire OS. Not a chapter — the spine the other OS docs hang from (the 6th OS component; see `OS.md`).

---

## 0. The reframe — we changed regulatory weight class tonight

Before tonight, RPI was **a firm handling its own clients' data** — single-tenant, our BAA with Google covers it, done.

As of tonight's build, RPI is **a multi-tenant custodian of partner firms' credentials AND their clients' PHI.** The moment we onboard a partner's book of business, that partner's clients' health + financial data lives in our vault and flows through our hub. That is a categorically different obligation:

- We now hold **other entities' PHI** → HIPAA Business-Associate obligations attach.
- We now hold **other firms' carrier credentials** → InfoSec breach exposure is multi-tenant (one leak can't be allowed to cross partners).
- The machine runs this **autonomously** → the compliance framework has to be enforced by *controls*, not by a human remembering.

**The thesis:** the autonomous partner-onboarding loop ([[project_prodash_bottleneck_is_the_thesis]]) only stays trustworthy AND legal if the compliance framework keeps pace with the capability. The bones already exist (signed BAA, AES-256-GCM, per-tenant keys, owner-gating, audit logging, PITR). What was missing — and what this doc supplies — is the **explicit written framework covering the NEW surfaces** (vault, hub, partner data) instead of assuming single-tenant rules still cover everything.

---

## 1. The BAA chain — who is a Business Associate of whom

A BAA (Business Associate Agreement) is the HIPAA-required contract that lets PHI flow between a Covered Entity and a vendor that processes it on their behalf. PHI may not legally flow across a link until the BAA on that link is signed.

```
  PARTNER FIRM ──(their clients' PHI)──▶  RPI  ──(stored/processed via)──▶  GOOGLE (Workspace + GCP)
       │                                   │                                      │
   Covered Entity                  Business Associate                    Subcontractor BA
   (or its own BA)                 of the Partner                        of RPI
```

| Link | Status | Gate |
|---|---|---|
| **RPI → Google** | ✅ **SIGNED 2026-02-04.** Covers Workspace + GCP HIPAA-eligible services (Firestore, Cloud STT, Vertex, BigQuery). On-box at `reference/os/STANDARDS.md` + `POSTURE.md`. See [[reference_google_baa_signed]]. | **CLEARED** — PHI-to-Google is legally covered. |
| **Partner → RPI** | ⛔ **DOES NOT EXIST YET.** When we ingest a partner's book, RPI becomes a Business Associate of that partner (we process their clients' PHI on their behalf). This requires a signed BAA between the partner and RPI. | **🔴 HARD GATE — see §2.** The tech can be 100% ready and we still cannot legally ingest a single byte of a partner's client PHI without it. |

**Why this is the CRITICAL find (JDM, 2026-06-13):** it is invisible until it is a problem. Everything technical can be green — vault encrypted, hub live, conductor pulling — and we'd still be in violation the instant partner PHI lands without the partner↔RPI BAA. Catching it *before* the first onboarding is the whole point of having a compliance spine.

---

## 2. The PARTNER↔RPI BAA GATE — the named onboarding checkpoint (the build)

This is the concrete control. It makes the BAA requirement *enforceable* instead of *remembered*.

> **GATE: `PARTNER↔RPI BAA SIGNED` blocks the first byte of any partner's client PHI.**
> No partner book ingestion — no BoB download, no vault write of partner *client* records, no conductor run against a partner's clients — proceeds until this gate is GREEN for that partner.

**Onboarding sequence (the gate's position in the loop):**

```
1. Partner deal closed (JDM/business)
2. ⛔ GATE: PARTNER↔RPI BAA executed  ◀── legal doc, JDM + counsel; blocks step 4+
3. Partner credential intake (carrier logins → vault)        ← InfoSec, no client PHI yet, allowed pre-BAA
4. Partner CLIENT BoB ingestion (PHI lands)                  ← BLOCKED until step 2 is GREEN
5. Conductor / statements / analysis on partner clients      ← downstream of 4
```

Note the ordering nuance: **carrier-credential intake (step 3) can begin pre-BAA** (a carrier login is RPI's operational credential to *act as* the partner, not the partner's clients' PHI). The hard line is **partner CLIENT data (step 4)** — that is the PHI, that is what the BAA gates. This lets onboarding start moving (vault, access) while the legal doc is in flight, without ever risking PHI exposure.

**Gate mechanics (how it's enforced, not just written):**
- A `tenant` record carries `baa_status: pending | signed` + `baa_signed_date` + `baa_doc_ref`.
- `baa_status != signed` → the ingestion path (step 4) refuses to write partner client records. Fail-loud, not silent-skip.
- The gate is a **named checkpoint in the onboarding playbook** (Operations) — surfaced on the partner's Agency profile so status is visible, not buried.

**For MWM specifically (first live partner):** worth getting the partner↔RPI BAA in front of Matt **now**, in parallel with the tech, so the legal link is signed before the book is ready to ingest. The tech timeline and the legal timeline should run together — neither should be the thing that blocks the other at the finish line.

**What's mine vs. what's JDM/counsel:**
- **SHINOB1 builds:** the gate (the `baa_status` enforcement + the playbook checkpoint + the Agency-profile surfacing), the documented safeguards (§3), the breach runbook (§5).
- **JDM + counsel own:** the BAA *legal document itself* and its signature. The framework makes it real and enforceable; the signature is a human act.

---

### Pre-stage: Due Diligence needs its OWN gate (added 2026-06-13, JDM)

Due diligence happens **before** the deal closes — and DD on an agency *is* pulling their book through our ingestion to evaluate it. The moment that pull touches the partner's clients' PHI, **RPI is a Business Associate** — even if we ultimately pass on the deal. So there are **two** PHI-grade gates, not one:

1. **NDA** — confidentiality, before anything is shared (not a PHI instrument).
2. **⛔ DD GATE — Due-Diligence Data-Access Agreement** (a *DD-scoped BAA*): authorizes the evaluation pull, time-bound to the DD window, BAA-grade terms because it touches PHI. No DD ingestion before it's executed.
3. **⛔ BAA GATE — full Partner↔RPI BAA** (this section's gate): ongoing custody at deal-close.

Both gates are enforced through the **Partner Onboarding Forms Kit** (NDA · DD-Access · BAA, executed via DEX + DocuSign — extends the live Open-a-Kit flow). Full scope: `partner-forms-kit-scope-v1.html`. The Forms Kit is the *enforcement surface* for these gates — a doc's executed-status unlocks the capability it covers.

---

## 3. HIPAA technical safeguards — written down as controls (§164.312)

HIPAA requires technical safeguards to be *documented controls*, not just implementation details. Each below maps to a HIPAA citation and points to where the control actually lives (MEGAZORD documents the specifics in Posture/Standards — this is the framing index, no duplication).

| HIPAA safeguard | Citation | Our control | Where it lives / verified |
|---|---|---|---|
| **Access control** | §164.312(a)(1) | Firebase Auth `@retireprotected.com` domain restriction + per-tenant custom claims (`isPartnerOfTenant(t)`) + owner-gating (`owner_email==token.email`) | `firestore.rules`; Posture §1 (collection table) |
| **Person/entity authentication** | §164.312(d) | Firebase Auth (Google Workspace SSO), `@retireprotected.com` domain lock; `tenant` custom claim set server-side for partner sessions | `packages/auth`; Standards §1 |
| **Tenant isolation** (a documented safeguard, not just a rule) | §164.312(a)(1) | Per-tenant vault paths (`partner_vault/{tenant}/**`, deny-by-default catch-all) + per-tenant encryption keys → **one partner can never read another's creds or PHI, even on a breach** | Posture §1; verified — partner_vault deny-by-default, `approval_secrets` read=false (held through 2 rule clobbers this week) |
| **Encryption at rest** | §164.312(a)(2)(iv) | Partner creds: AES-256-GCM via `@tomachina/core/crypto/vault-cipher`, `VAULT_ENCRYPTION_KEY` from GSM, **no plaintext anywhere**. PHI in Firestore: Google-encrypted, BAA-covered | Standards (vault-cipher); the 2,584-pw bulk load was encrypted + shredded |
| **Encryption in transit** | §164.312(e)(1) | TLS everywhere — Tailscale funnel (TLS), Firestore SDK (TLS), tm-api (HTTPS) | infra default |
| **Audit controls** | §164.312(b) | **Verified:** `vault_audit` write on every credential op (actor+action+role, `jwt-issuer.ts`); `dojo_messages` is an **immutable** conversation audit log (rules: update/delete=`false`); approval-card decision trail. **Platform write-stream (caveated):** `bigquery-stream` Cloud Fn captures every Firestore create/update/delete (collection, op, snapshot, changed_fields) → `firestore_changes` — but **best-effort** (logs-and-continues on transient BQ error) and **per-partner named-DBs require activation** (`BQ_STREAM_PARTNERS`), so a partner's PHI-DB writes are not write-streamed until turned on per onboarding. → **gap, §7** | `services/api/.../jwt-issuer.ts`; `services/bigquery-stream/src/index.ts` (verified 2026-06-13) |
| **Integrity + availability** | §164.312(c)(1) / §164.308(a)(7) | **PITR ON** for every conversation/PII collection — the recoverability control. Proven: 37-message recovery 2026-06-13 | Posture §2 — **PITR OFF on any PII collection = Sev-1 posture gap** |

---

## 4. PHI handling on the NEW surfaces

The global PHI rules (PHI only in Workspace/Firestore, never Slack, never logs, mask SSN/DOB) **now explicitly extend to the surfaces we built tonight:**

- **The hub (`dojo_messages`):** Firestore-backed → **BAA-covered**, PHI-safe by storage. BUT a Slack/Chat *mirror* is **NOT in the BAA** → **never route PHI to a mirror window.** The hub is home; mirrors are disposable and PHI must never reach them. (This is also why the two-channel collapse is a *compliance* improvement, not just a UX one — fewer surfaces = smaller PHI attack surface.)
- **The vault (`partner_vault`, `approval_secrets`):** server-only (Admin SDK), read=false at the rules layer, encrypted at rest. PHI/creds never client-readable.
- **Approval Hub cards (`approval_requests`):** owner-gated; card *titles/metadata* are operational, secret *values* live in `approval_secrets` (read=false). Never put a raw PHI value or a plaintext secret in a card body.
- **Logs (everywhere):** the existing `block-phi-in-logs` enforcement extends unchanged to all new code paths — hub, vault, conductor, ingestion.

---

## 5. Breach / incident response runbook

The documented loss/exposure-response posture. Two worked examples from tonight prove the path.

**Disclosure standard (the doctrine): straight + immediate + recovery-proof.** When something goes wrong, the report is honest, sent immediately to JDM (compliance owner), and paired with proof of the recovery state. TAIKO's handling of tonight's incidents is the model. No softening, no delay, no burying.

**Runbook by incident class:**

| Class | Immediate action | Recovery | Disclosure |
|---|---|---|---|
| **Data loss** (bad delete / bulk op) | Stop the operation | **PITR restore** toward last-known-good (REST `runQuery` w/ `readTime` → commit-restore; exact IDs/types). Proven: 37 msgs recovered 2026-06-13 | JDM immediately, with the recovered-count proof |
| **Rules clobber** (security spine reverted) | Identify the missing block | REST restore-toward-known-good ruleset + **same-session byte-identical land-to-main** that closes the window; incident log | JDM + #shinob1; note whether it was denial (safe) or exposure (Sev-1) |
| **Credential exposure** (a secret transits an unsafe surface) | **ROTATE, don't just delete** — assume compromised | Re-vault encrypted; revoke the exposed token | JDM immediately |
| **PHI exposure** (PHI reaches a non-BAA surface: Slack, logs, public repo) | Pull the surface (e.g. repo → private; delete the message) | Confirm no further propagation (caches/edges can lag — note it) | **JDM or John Behn IMMEDIATELY** — suspected PHI breach is the highest-severity class |
| **Account-level cutoff** (billing/rate-limit kills the fleet) | — | Out-of-band SMS alarm already fires (see [[reference_dojo_outofband_alarm_and_mirror_kill]]) | Automatic — JDM's phone, works when the API is down |

**Data-loss prevention control (feeds the Immune System rule):** never delete by a flag the *system* writes for its own bookkeeping. Dry-run a **COUNT** first; delete only by a **test-only marker stamped at creation** (`e2e-test-`/`is_test:true`), never a runtime flag. (Tonight: 37 real msgs swept by the dual-purpose `chat_mirrored` flag → PITR saved them → new rule `warn-bulk-delete-without-count-dryrun`.)

---

## 6. How this spine threads the other OS docs (no duplication)

This doc is the **framing SSOT**. The specific controls live in the operational docs and *reference back here*:

- **POSTURE** (MEGAZORD draft) — the collection-access table, PITR requirement, IAM-standing flag, BAA-chain verification line. → implements §3's access/audit/availability controls.
- **STANDARDS** (MEGAZORD draft, on signal) — encryption standard (vault-cipher), access-control rules, PHI-handling extension, deploy-from-main rules. → implements §3 + §4.
- **OPERATIONS** (MEGAZORD draft, on signal) — the partner-onboarding loop with the **BAA gate as a named checkpoint** (§2), bulk-delete dry-run procedure, incident-disclosure standard (§5).
- **IMMUNE SYSTEM** (SHINOB1) — `warn-bulk-delete-without-count-dryrun` rule + the rules-integrity guardrail (§5 prevention control).
- **LAUNCH GUIDE** (SHINOB1) — the two-channel collapse is a §4 PHI-surface-reduction (fewer surfaces, smaller attack surface).

---

## 7. Open items (gated on JDM / counsel)

| Item | Owner | Blocks |
|---|---|---|
| **PARTNER↔RPI BAA legal doc + signature** | JDM + counsel | Partner client-PHI ingestion (step 4). Get in front of MWM/Matt now, parallel to tech. |
| **WIF owner-bootstrap** (4 gcloud cmds + #shinob1 webhook) | JDM (2-min, his hand) | The rules-integrity guardrail going fully live (§5 prevention) |
| **IAM standing scope-down review** | SHINOB1 → JDM | Not urgent; `mdj-agent` projectIamAdmin standing privilege ([[project_firestore_rules_integrity_guardrail]]) |
| **Per-partner BQ audit-stream activation** | SHINOB1 / MEGAZORD | §164.312(b) audit coverage for a partner's named PHI-DB. Add to the onboarding checklist: set `BQ_STREAM_PARTNERS=<slug>`, create the dataset, redeploy `bigquery-stream` — so partner PHI-DB writes are audit-captured, not just `vault_audit` cred-ops. (MT-011 checklist already documents the steps.) |

---

*This is the spine. The capability got ahead of the paperwork tonight — this is the paperwork catching up, written as enforceable controls so the autonomous machine stays both trustworthy and legal. — 🥷 SHINOB1, CTO*
