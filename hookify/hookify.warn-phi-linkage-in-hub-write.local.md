---
name: warn-phi-linkage-in-hub-write
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: '(dojo-reply\.mjs|dojo-send\b)'
  - field: command
    operator: regex_match
    pattern: '\b(medicare|medicaid|ma[- ]?pd|mapd|\bpdp\b|medigap|moop|deductible|formulary|premium|carrier|diagnos|enrollment|part\s+[abcd]\b|\brx\b|medication|health\s+intake|-roadmap|client-summary)\b'
  - field: command
    operator: regex_match
    pattern: '(\b[a-z0-9]{2,}(-[a-z0-9]{2,})+-(roadmap|client-summary|budget-runway|intake)\b|(?-i:\b(?!(?:Medicare|Medicaid|Medigap|Supplement|Supplemental|Advantage|Part|Plan|Plans|Drug|Prescription|Enrollment|Election|Period|Window|Premium|Premiums|Carrier|Carriers|Deductible|Formulary|Diagnosis|Diagnoses|Medication|Intake|Roadmap|Claim|Claims|Coverage|Benefit|Benefits|Annuity|Social|Security|Open|Special|Annual|Initial|AEP|OEP|SEP|MAPD|MOOP|PDP|Josh|Millang|Retirement|Protectors|Cloud|Run|Approval|Hub|Live|Verify|Firestore|BigQuery|Officer|Dojo|Scroll|Corpus|Both|This|That|These|Those|Team|Here)\b)[A-Z][a-z]{2,}\s+(?!(?:Medicare|Medicaid|Medigap|Supplement|Supplemental|Advantage|Part|Plan|Plans|Drug|Prescription|Enrollment|Election|Period|Window|Premium|Premiums|Carrier|Carriers|Deductible|Formulary|Diagnosis|Diagnoses|Medication|Intake|Roadmap|Claim|Claims|Coverage|Benefit|Benefits|Annuity|Social|Security|Open|Special|Annual|Initial|AEP|OEP|SEP|MAPD|MOOP|PDP|Josh|Millang|Retirement|Protectors|Cloud|Run|Approval|Hub|Live|Verify|Firestore|BigQuery|Officer|Dojo|Scroll|Corpus|Both|This|That|These|Those|Team|Here)\b)[A-Z][a-z]{2,}\b))'
owner: shinob1
---

⚠️ **POSSIBLE PHI LINKAGE in a hub write — go POINTER-ONLY before you send.**

This hub message pairs a **client-name signal** (a person-name or a `*-roadmap` / `client-summary`
case-file slug) with a **health term** (Medicare / MAPD / plan / carrier / premium / enrollment /
diagnosis / intake …). A named person tied to health/Medicare detail **is PHI**.

Why this is a hard rule (learned the hard way, 2026-07-11): every hub message body **auto-mirrors
to BigQuery** (`toMachina.conversations`) AND lands in Firestore `dojo_messages`. So PHI typed into
a thread instantly exists in **two stores** — and a redaction/status message that *re-types the names*
re-leaks the very PHI it reports on. Whack-a-mole forever.

**The fix — POINTER-ONLY. Reference, never re-type:**

- ✅ "the 6 households in the `cases/` set" · "the flagged client" · "the roadmap files"
- ❌ a client's name next to a plan / carrier / Medicare status / dollar figure / health field

This is WARN-first (heuristic — it fires on **linkage**, not a name alone; a teammate mention with no
health context does NOT trip it). If this is a genuine false positive, send as-is. But if there's a
real name-to-health pairing here, **rewrite it as a pointer first.**

Rule: `OB1-PHI-HYGIENE-001` · pointer-only doctrine · owner SHINOB1 (A6 immune-system lane).
