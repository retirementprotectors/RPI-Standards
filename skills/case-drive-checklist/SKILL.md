---
description: Run the canonical VOLTRON Case-Drive Checklist to drive a client case to 100%. Covers the 7-step process: Sweep 5 surfaces → Reconcile 3 SORs → Polish roadmap → Gate 1 (Firestore true-up, MEGAZORD lane) → Gate 2 (ACF true-up) → Execute + document → Sign-off. "100%" = both Gates 4 and 5 closed.
---

# VOLTRON Case-Drive Checklist

You have been invoked as the Case-Drive Checklist skill. Drive the current client case to 100% using the canonical 7-step process below. Work through each step in order; do not skip.

**"100%" = both Gate 4 (Firestore) AND Gate 5 (ACF) are closed.**

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

---

## Step 3 — POLISH the Roadmap

Drive the client roadmap to current truth. Iterate with the writer/JDM until the roadmap is **LOCKED**.

- The roadmap is the live case record — it must reflect carrier-direct truth.
- The one-pager and pay-plan distill the roadmap — build or sync those AFTER the roadmap locks. Do not re-sync on every iteration.
- Do not advance to Gates 4 or 5 until the roadmap is locked.

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

## Step 7 — SIGN-OFF + Park

Before anything goes client-facing: JDM eyeballs it.

After sign-off:
- The case-sub stands by and keeps the roadmap current as carrier truth moves.
- Do not call death-gate until JDM explicitly closes the case.

---

## Completion Definitions

| Term | Meaning |
|------|---------|
| **roadmap-100%** | Steps 1–3 done and locked |
| **case-100%** | Gates 4 + 5 both closed AND Step 6 executed |

Track gate status per case directly on the roadmap.

---

*VOLTRON, CSO — Client Operations · Case-Drive Checklist v1.0 · born on the Myers case, 2026-06-26*
