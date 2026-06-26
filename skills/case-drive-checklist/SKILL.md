---
description: Run the canonical VOLTRON Case-Drive Checklist to drive a client case to 100%. Covers the 8-step process: Sweep 5 surfaces → Reconcile 3 SORs (+ capture AOR) → Polish roadmap → Gate 1 (Firestore true-up, MEGAZORD lane) → Gate 2 (ACF true-up) → Execute + document → Polish deliverables → Gate 3 (AOR / Held-Away Recapture) → Sign-off. "100%" = all three Gates closed (Firestore, ACF, AOR) and execution logged.
---

# VOLTRON Case-Drive Checklist

You have been invoked as the Case-Drive Checklist skill. Drive the current client case to 100% using the canonical 8-step process below. Work through each step in order; do not skip.

**"100%" = Gate 1 (Firestore, Step 4) AND Gate 2 (ACF, Step 5) AND Gate 3 (AOR, Step 8) are ALL closed, and the execution in Step 6 is logged.**

---

## Step 1 — SWEEP the 5 Surfaces

Before touching anything, pull context from all five case surfaces:

1. **Registry** — look up the client in the VOLTRON client registry (QUE / Firestore).
2. **Data** — pull carrier-direct account values, policy details, and rider status. Carrier-direct wins over any on-file number.
3. **State** — read the client Firestore document. Note every stale or mismatched field.
4. **Comms** — BigQuery recall of prior advisor–client touchpoints and prior case notes.
5. **Auth** — verify carrier-direct auth is available for every carrier/product on the case.

Do not start analysis cold — the case history is one recall away.

---

## Step 2 — RECONCILE the 3 Systems of Record

Line up **every number** across: **Carrier ↔ Firestore ↔ ACF**.

- Flag every drift. Write the drift list before proposing any action.
- The carrier-direct value is truth. On-file and Firestore values are the floor, not today's reality.
- Document which fields need correcting and in which system.
- **Capture the Advisor of Record (AOR) for every account as you enumerate it** — record who holds advisory/servicing standing alongside the value. This is data capture only (no evaluation); Step 8 evaluates and gates it. One source for the AOR datum, captured here, enforced there — no dual-gather.

---

## Step 3 — POLISH the Roadmap

Drive the client roadmap to current truth. Iterate with the writer/JDM until the roadmap is **LOCKED**.

- The roadmap is the live case record — it must reflect carrier-direct truth.
- Where income-rider timing is in play, model the **optimal-flip-year / Year-N activation pattern** (let the rider roll up, turn it on the year it covers the bulk of the withdrawal need) — generically, per the client's own RMD and income picture.
- The one-pager and pay-plan distill the roadmap — build or sync those AFTER the roadmap locks. Do not re-sync on every iteration.
- Do not advance to the Gates until the roadmap is locked.

---

## Step 4 — FIRESTORE TRUE-UP ⟨Gate #1 — MEGAZORD lane⟩

> **VOLTRON role: flag and coordinate only. MEGAZORD executes the writes.**

Flag every Firestore field that needs correction based on carrier-direct truth:
- DOB, account values, rider status, beneficiaries, duplicate records, stale fields.

Hand the corrected-field list to MEGAZORD. Gate is closed when:
- Firestore matches carrier-direct on every flagged field.
- No stale fields remain.
- No duplicate records exist.

**Gate 1 is MEGAZORD's to sign, not VOLTRON's.** Relay "Gate 1 handed to MEGAZORD — pending sign" until MEGAZORD confirms.

---

## Step 5 — ACF TRUE-UP ⟨Gate #2 — Document file⟩

Verify every document that should be on file IS on file:
- Carrier statements (most recent)
- Illustrations (carrier-direct)
- RMD letters (if applicable)
- Signed forms: distribution election, ACH authorization, activation forms
- Beneficiary designation forms

Pull or file anything missing. Gate is closed when nothing referenced in the roadmap is un-filed.

**Gate 2 is yours to close.** Confirm each document category before declaring it closed.

---

## Step 6 — EXECUTE + Document

Run the open work identified in the reconciliation (Steps 2–5):
- Submit forms, trigger activations, initiate distributions.
- Log the **standing instruction in ProDash** so the action recurs automatically. Do not leave it as a one-time manual pull.

---

## Step 7 — POLISH the Deliverables

Distill the locked roadmap into the client-facing artifacts:
- Build/sync the **gold-standard 2-page Income Pay Plan** and the one-pager from the locked roadmap (not before — they distill it).
- Keep them in sync with carrier-direct truth; no figure appears that isn't reconciled.

---

## Step 8 — AOR / HELD-AWAY RECAPTURE CHECK ⟨Gate #3 — BLOCKING ship-gate⟩

> **No case ships until this check returns a clean result.** It consumes the AOR field captured in Step 2 and adds zero new financial figures — it adds only the ownership/AOR axis.

Every case must surface accounts the household **owns** where the **Advisor of Record is not us** — assets we serve the client on but do not yet manage. Each is a **pending-RIA AOR recapture candidate** (e.g., an account custodied/advised at Signal, Ameritas, or another firm where we are not the AOR). A candidate is a **FLAG, not an action** — it authorizes no transaction and moves no money.

**Procedure** — for every account across **all** household members:
- **AOR is ours** → no flag.
- **AOR is not ours** (another firm/advisor, or none) → flag as a **pending-RIA recapture candidate**.
- **AOR unknown / not captured** → flag as **AOR-unconfirmed**, treated as a candidate until confirmed. Never silently cleared.
- **AOR genuinely not applicable** (direct-held coverage with no advisory layer, plans ineligible for advisory) → record the **exclusion with a reason code** — do not drop the account silently.

**Decision rule (the gate):**
- **PASS** — every account is one of: (a) ours, (b) an explicit reason-coded non-applicable exclusion, or (c) flagged `pending-RIA`. The case may ship.
- **BLOCK** — any not-ours-or-unconfirmed account is **not** flagged. The case does not ship until it is flagged or resolved.

A clean result is **not** "zero held-away accounts" — it is **"every held-away account is accounted for and flagged."** Zero candidates is valid only when genuinely none exist.

**Output artifact:** a short **AOR block** on the case record listing each recapture candidate — or an explicit `none — all accounts ours / N/A` attestation. This block is the evidence the gate passed and the feed into the recapture pipeline downstream.

**Golden Rule:** if you didn't **READ** the account's AOR, don't **REPORT** it as ours. Unconfirmed AOR is a candidate, never an assumed clear.

---

## Step 9 — SIGN-OFF + Park

Before anything goes client-facing: JDM eyeballs it. Sign-off attests all three gates passed (Firestore, ACF, AOR).

After sign-off:
- The case-sub stands by and keeps the roadmap current as carrier truth moves.
- Do not call death-gate until JDM explicitly closes the case.

---

## Completion Definitions

| Term | Meaning |
|------|---------|
| **roadmap-100%** | Steps 1–3 done and locked |
| **case-100%** | Gates 1 + 2 + 3 (Firestore, ACF, AOR) all closed AND Step 6 executed |

Track gate status per case directly on the roadmap.

---

*VOLTRON, CSO — Client Operations · Case-Drive Checklist v1.1 · born on a live client case, 2026-06-26*
