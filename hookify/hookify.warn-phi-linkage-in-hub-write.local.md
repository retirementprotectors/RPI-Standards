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
    pattern: '\b(diagnos|comorbid|medication|prescri|\brx\b|treatment|therapy|chemo|radiation|biopsy|surgery|surgical|hospice|dialysis|infusion|oncolog|cardiolog|neurolog|psychiatr|nephrolog|endocrinolog|rheumatolog|pulmonolog|gastroenterolog|dermatolog|urolog|orthoped|cancer|tumor|diabet|dementia|alzheimer|copd|hypertens|health\s+intake|medical\s+history|lab\s+(result|work)|med\s+list|drug\s+list|-roadmap|client-summary)[a-z]*\b'
  - field: command
    operator: regex_match
    pattern: '(\b[a-z0-9]{2,}(-[a-z0-9]{2,})+-(roadmap|client-summary|budget-runway|intake)\b|(?-i:\b(?!(?:Medicare|Medicaid|Medigap|Supplement|Supplemental|Advantage|Part|Plan|Plans|Drug|Prescription|Enrollment|Election|Period|Window|Premium|Premiums|Carrier|Carriers|Deductible|Formulary|Diagnosis|Diagnoses|Medication|Intake|Roadmap|Claim|Claims|Coverage|Benefit|Benefits|Annuity|Social|Security|Open|Special|Annual|Initial|AEP|OEP|SEP|MAPD|MOOP|PDP|Josh|Millang|Retirement|Protectors|Cloud|Run|Approval|Hub|Live|Verify|Firestore|BigQuery|Officer|Dojo|Scroll|Corpus|Both|This|That|These|Those|Team|Here|Breast|Lung|Colon|Prostate|Heart|Kidney|Liver|Blood|Bone|Skin|Cancer|Tumor|Stage|Type|Chronic|Acute|Doctor|Provider|Specialist|Oncologist|Oncology|Cardiologist|Neurologist|Physician|Primary|Care|Treatment|Therapy|Chemo|Radiation|Surgery|Surgical|Biopsy|Hospice|Dialysis|Infusion|Lab|Labs|Result|Results|History|Medical|Health|Diabetes|Dementia|Alzheimer|Hypertension|Condition|Conditions)\b)[A-Z][a-z]{2,}\s+(?!(?:Medicare|Medicaid|Medigap|Supplement|Supplemental|Advantage|Part|Plan|Plans|Drug|Prescription|Enrollment|Election|Period|Window|Premium|Premiums|Carrier|Carriers|Deductible|Formulary|Diagnosis|Diagnoses|Medication|Intake|Roadmap|Claim|Claims|Coverage|Benefit|Benefits|Annuity|Social|Security|Open|Special|Annual|Initial|AEP|OEP|SEP|MAPD|MOOP|PDP|Josh|Millang|Retirement|Protectors|Cloud|Run|Approval|Hub|Live|Verify|Firestore|BigQuery|Officer|Dojo|Scroll|Corpus|Both|This|That|These|Those|Team|Here|Breast|Lung|Colon|Prostate|Heart|Kidney|Liver|Blood|Bone|Skin|Cancer|Tumor|Stage|Type|Chronic|Acute|Doctor|Provider|Specialist|Oncologist|Oncology|Cardiologist|Neurologist|Physician|Primary|Care|Treatment|Therapy|Chemo|Radiation|Surgery|Surgical|Biopsy|Hospice|Dialysis|Infusion|Lab|Labs|Result|Results|History|Medical|Health|Diabetes|Dementia|Alzheimer|Hypertension|Condition|Conditions)\b)[A-Z][a-z]{2,}\b))'
owner: shinob1
---

⚠️ **POSSIBLE CLINICAL PHI LINKAGE in a hub write — go POINTER-ONLY before you send.**

This hub message pairs a **client-name signal** (a person-name or a `*-roadmap` / `client-summary`
case-file slug) with a **CLINICAL term** (diagnosis / medication / treatment / provider specialty /
lab / condition). A named person tied to clinical detail is the **highest-harm** form of PHI.

**Inference counts.** "Jane Doe, Tamoxifen" and "Jane Doe — Dr. Smith, Oncologist" are PHI even
though no condition is ever named: the drug and the specialty reveal it.

Why this is a hard rule (learned the hard way, 2026-07-11): every hub message body **auto-mirrors
to BigQuery** (`toMachina.conversations`) AND lands in Firestore `dojo_messages`. So PHI typed into
a thread instantly exists in **two stores** — and a redaction/status message that *re-types the names*
re-leaks the very PHI it reports on. Whack-a-mole forever.

**The fix — POINTER-ONLY. Reference, never re-type:**

- ✅ "the 6 households in the `cases/` set" · "the flagged client" · "the roadmap files"
- ❌ a client's name next to a diagnosis / medication / specialist / treatment

---

### Scope change 2026-07-26 — coverage + payment terms REMOVED from the trigger

This rule previously also fired on `medicare · medicaid · mapd · pdp · medigap · moop · deductible ·
formulary · premium · carrier · enrollment · part a-d`. **Those no longer trip it.**

Coverage and payment data **is still PHI** — 45 CFR 160.103 prong (c), "payment for the provision of
health care," squarely covers it, and "health plan beneficiary number" is an enumerated Safe Harbor
identifier. Nothing here reclassifies it.

But it is also the **substrate of the entire book of business**. Warning on it meant warning on
ordinary daily traffic, which trained everyone to click through — and a warning that always fires
protects nothing. **Classification is not escalation.** This gate now guards the high-harm tier,
where a false negative actually costs something.

Coverage/payment data stays governed by the standing rules: Workspace-only storage, need-to-know,
pointer-only in persisted streams. It is simply no longer an interrupt.

**Known limit:** brand-name drugs cannot be enumerated in a regex. "Jane Doe, Tamoxifen" will NOT
trip this gate — the doctrine block teaches the inference rule; this gate is the suspenders, not
the belt.

Rule: `OB1-PHI-HYGIENE-001` · pointer-only doctrine · owner SHINOB1 (A6 immune-system lane)
Narrowed to Tier-1 clinical per JDM ruling 2026-07-26; see STANDARDS.md Part 2.
