# OPERATIONS.md — Human Processes & Checklists

> **Part of The Operating System** — the governance layer of The Machine.
> See [OS.md](OS.md) for the full architecture.
> This document defines what humans do — checklists, processes, and procedures.

---

## Part 1: Documentation Maintenance Triggers

When the codebase changes, the corresponding docs must be updated. Claude is responsible for executing these updates as part of the change.

**Rules live in CLAUDE.md. Procedures live in reference docs. Never duplicate rules into reference docs.**

| When You... | Update These |
|---|---|
| Add a new GAS project (rare — maintenance mode) | MONITORING.md (project list + scan loop), POSTURE.md (verification table), `clone-all-repos.sh` + `setup-hookify-symlinks.sh`, CLAUDE.md Project Locations tree |
| Add a new GAS web app (rare — maintenance mode) | POSTURE.md (add to verification table) |
| Complete a security audit | POSTURE.md (audit trail + dates) |
| Change deploy process | CLAUDE.md ONLY — never reference docs |
| Add a new MCP tool | MCP-Hub/CLAUDE.md (directory listing) |
| Change compliance rules | CLAUDE.md = the rule. Reference doc = the procedure. |
| Ship a production release | Create testing guide from `PRODUCTION_TESTING_TEMPLATE.md`, assign to tester, store on Shared Drive under release folder |

---

## Part 2: Offboarding Security Checklist

When an employee or contractor leaves RPI, the following must be completed **the same day as departure**:

- [ ] Disable Google Workspace account (same day as departure)
- [ ] Remove from any shared drives with sensitive data
- [ ] Remove from GitHub organization (if applicable)
- [ ] Remove from Slack workspace
- [ ] Remove from any third-party tools (DocuSign, etc.)
- [ ] Review any API keys/tokens they had access to
- [ ] Transfer ownership of any Docs/Sheets they owned
- [ ] Review and remove third-party GitHub App installations (Vercel incident 2026-03-19: unused app had broad repo access for months after project archived)
- [ ] Document completion date and who performed offboarding

**Responsible party:** CEO (JDM).

**Super Admin access is locked to Josh only** (John Behn offboarded 2026 — Josh sole super-admin, GAM-verified 2026-07-06).

**OU Structure:**
- `/RPI- Archived Users` = FINRA email archiving via Global Relay (active securities-licensed users: Josh, Nikki, Angelique)
- `/RPI- Non-Archived Users` = Active employees NOT under securities email archiving
- `/RPI- Offboarded` = Suspended/departed employees (NOT archived to Global Relay)

**On departure:** Move user to `/RPI- Offboarded` — do NOT move to `/RPI- Archived Users` (that OU is for FINRA compliance only).

### Workspace Account Mechanics — what "disable the account" actually does

The offboard sequence (currently a manual GAM runbook — `gam` = gamadv-xtd3 at `~/bin/gamadv-xtd3/gam`; being automated, see *Automation* below) sets these states on the departing user. **Each is a SEPARATE state — reactivation must reverse all of them:**

1. **Suspend** — `gam update user <email> suspended on`
2. **Archive** — sets `Is Archived: True` and downgrades the license to **"Business Plus – Archived User"** (retention-only). ⚠️ This is a *distinct* state from suspended — an archived user can't log in or use Gmail even when not suspended.
3. **Rename** — `gam update user <email> username <local>.archived` → `user@` becomes `user.archived@`
4. **Park the freed email on the 2FA hub** — `user@retireprotected.com` is added as an alias on the `2fa@retireprotected.com` service-team catch-all so in-flight mail to the departed user is caught. *(This is the "move the other to 2FA" step.)*
5. **OU** — move to `/RPI- Offboarded`.

### Reactivation / Rehire — the REVERSE (un-suspend alone is NOT enough)

⚠️ **The archive flag, the license, and the 2FA-hub alias each must be reversed or the rehire's email stays dead.** This has bitten **twice**: **Nikki's rehire (2026-05-14)** bounced SMTP 5.2.1 because the path reversed `suspended` but not `archived`; **Matt McCormick (2026-06-05)** showed "inactive" for the identical reason.

Validated GAM checklist (run in order):
1. `gam update user <X>.archived@ suspended off`
2. **`gam update user <X>.archived@ archived off`** ← the step that gets missed; this auto-restores the active Business Plus license (a separate `add license` will fail "already has a license")
3. `gam update user <X>.archived@ ou "/"`  *(active employees live in root `/`)*
4. Reclaim the email: `gam delete alias <X>@retireprotected.com` (pull it off the 2fa@ catch-all) **then** `gam update user <X>.archived@ username <X>` (rename back). The rename throws "Entity already exists" if run immediately after the alias delete — directory propagation lag; wait a beat + retry.
5. `gam update user <X>@retireprotected.com password '<temp>' changepassword on`
6. If 2FA is enforced and their old device is gone: `gam user <X>@ update backupcodes` then `gam user <X>@ show backupcodes`.

**Verify ALL of:** `Account Suspended: False` · `Is Archived: False` · active (non-Archived-User) license · `Mailbox is setup: True`. *(A GAM "Service Account … not authorized for Gmail API" error on `show vacation` is a GAM scope limit, NOT the user's mailbox being down — don't confuse the two.)*

### Automation

The full offboard/rehire sequence is **implemented** as the `wire_email_reroute` (offboard) / `wire_email_unreroute` (rehire) MCP tools in `services/MCP-Hub/rpi-workspace-mcp/src/drive-audit-tools.js` (the 3-week-old seed disco assumed no executor; it was built since). The reverse wire reverses delete-hub-alias → kill-auto-forward → rename-back → license-check → unsuspend → **un-archive** (Step 6 `unarchive_user`, added 2026-06-05 in MCP-Hub `5f3eb60` — the gap that bounced Nikki's rehire + left Matt inactive). New code goes live on MCP restart; dry-run verified (full 7-step plan reaches `unarchive_user`). **The wire is fail-fast** — it errors out if the account isn't in the exact state its prior wire produced, so run `wire_email_reroute` to offboard and `wire_email_unreroute` to rehire; the GAM checklist above is the hand-run fallback for partial/manual states.

---

## Part 3: Incident Response Procedure

### Response Steps

**Step 1: Contain**
Disable affected accounts/tokens immediately. Revoke any compromised API keys or OAuth grants. If a device is lost/stolen, initiate remote wipe via Google Workspace Admin.

**Step 2: Assess**
Determine scope: what data may have been accessed, how many records, what type (PHI, PII, financial). Identify the root cause — credential leak, phishing, misconfiguration, etc.

**Step 3: Notify**
Inform CEO (JDM) immediately. For PHI breaches, HHS notification is required within 60 days. See notification requirements table below.

**Step 4: Remediate**
Fix the vulnerability. Rotate all affected credentials. Patch the attack vector. Deploy additional controls if needed.

**Step 5: Document**
Record what happened, when it was discovered, what data was affected, what actions were taken, and the timeline of response. Store in a secure, access-controlled location.

**Step 6: Review**
Update controls, hookify rules, and CLAUDE.md to prevent recurrence. Conduct a post-incident review with leadership.

### Notification Requirements

| Scenario | Who to Notify | Timeline |
|----------|---------------|----------|
| PHI breach | HHS + affected individuals | 60 days |
| PII breach (state laws) | State AG + affected individuals | Varies (Iowa: 60 days) |
| Security incident (internal) | Leadership (JDM) | Immediate |
| Breaches affecting 500+ individuals | HHS + media | 60 days |

### Contact Information

- **Google Workspace Support:** admin.google.com > Support
- **GitHub Security:** github.com/security
- **CEO (JDM):** Direct Slack DM or phone

---

## Part 4: Training Program

### Required Training

| Role | Training Required | Frequency | Status |
|------|-------------------|-----------|--------|
| All team members | PHI handling | Annual | Deployed -- 10/13 completed |
| Service/Sales | PHI/PII handling | Annual | Deployed |
| Technical | Security best practices | Annual | TBD |
| Leadership | Incident response | Annual | TBD |

### Training Deployment Status

- [x] PHI Training deployed (Feb 4, 2026)
- [x] PHI Acknowledgment Form -- 10 of 13 completed
- [ ] General data privacy training -- Not yet developed
- [ ] AI usage guidelines -- Not yet developed
- [ ] Incident reporting process -- Not yet developed

### Completion Roster

| Completed | Outstanding |
|-----------|-------------|
| Susan Kaelin, Bob Lacy, Vince Vazquez, Josh Archer, Aprille Trupiano (departed), Lucas Dexter, Nikki Gray, Christa Irwin, Angelique Bonilla, John Behn (departed) | Shane Parmenter (CFO, departed), Matt McCormick (B2B) |

---

## Part 5: PHI Incident Reporting

All workforce members must **immediately** report any of the following:

- Unauthorized access to PHI
- PHI sent to wrong recipient
- Lost or stolen devices with PHI access
- Suspected phishing or social engineering attempts
- Any other potential PHI breach

**Report to:** CEO (JDM).

**There is no penalty for good-faith reporting.** RPI encourages reporting of all suspected incidents regardless of severity. Early reporting minimizes damage and demonstrates compliance.

---

## Part 6: PHI Policy Acknowledgment

All workforce members must acknowledge the PHI policy by completing:

- **Initial PHI training acknowledgment form** -- completed during onboarding or at policy deployment
- **Annual policy re-acknowledgment** -- completed each year during the annual training cycle

Acknowledgment records are maintained by leadership and tracked in the completion roster above (Part 4).

---

## Part 7: Enforcement

Violations of PHI policy, security standards, or compliance requirements may result in:

- Additional training requirements
- Restricted system access
- Disciplinary action up to and including termination
- Potential legal liability for willful violations

Enforcement applies to all workforce members, contractors, and any individual with access to RPI systems or data.

---

## Part 8: New Project Setup

For the full new project setup checklist (11 steps including git init, CLAUDE.md creation, GCP linking, hookify symlinks, and tracking doc updates), see the **"New Project Setup"** section in `~/.claude/CLAUDE.md`.

The documentation maintenance triggers in Part 1 of this document must be followed for every new project.

---

## Part 9: Production Testing

Every production rollout — feature launch, schema change, data migration, UI update — gets a **Testing Guide** before it goes to the team.

### Template

`_RPI_STANDARDS/reference/os/PRODUCTION_TESTING_TEMPLATE.md`

### Required Structure

1. **Header** — Version, date, tester name, prepared by
2. **Prerequisites** — What must be true before testing starts
3. **Numbered Tests** — Each test has: Purpose, Where (nav path), Steps, Expected Results (checkboxes), Notes
4. **Test Summary Table** — Pass/Fail grid for all tests
5. **Issues Found Table** — #, Test, Description, Severity (BLOCKER/HIGH/MEDIUM/LOW)
6. **Sign-Off** — Tester signature, date, overall result, rollout readiness

### Format

- Create as `.md` file on the Shared Drive (renders clean when opened)
- Store in the release folder or the Shared Drive root (`0AFUXPgL0EWC6Uk9PVA`)
- Reference: 6 testing guides from 2.15.26 + 2.16.26 Night Shift sessions (PRODASH v168, Marketing Hub, RIIMO v3.0, Comms Integration, Data Overhaul, Medicare v165)

### When to Create

| Release Type | Testing Guide Required? |
|-------------|----------------------|
| New UI feature | Yes — full interaction tests |
| Schema change + data migration | Yes — spot-check records with exact expected values |
| Bug fix (isolated) | No — unless it affects user-facing behavior |
| Config/deploy-only change | No |

### Assignment

- Tester should be someone who did NOT build the feature (separation of concerns)
- Default testers: Vince (Sales/ProDashX), Nikki (Service), Matt (DAVID/SENTINEL)

---

## Cross-References

- For the **rules** these processes enforce, see [STANDARDS.md](STANDARDS.md)
- For **current security state**, see [POSTURE.md](POSTURE.md)
- For **automated monitoring**, see [MONITORING.md](MONITORING.md)
- For the **full OS architecture**, see [OS.md](OS.md)

---

*Version: v2.0 | March 19, 2026 (OS Audit refresh)*
*Consolidated from COMPLIANCE_STANDARDS.md, SECURITY_COMPLIANCE.md, PHI_POLICY.md, and CLAUDE.md*


---

<!-- Landed 2026-06-13 (MEGAZORD, OS governance pass). Cites COMPLIANCE.md spine; does not re-derive the §164.312 matrix or the 2-gate model. -->

## Operations — Partner Onboarding, Data Integrity + Incident Response

---

### Part 1 — Partner Onboarding Loop

#### Overview

Partner onboarding follows a fixed autonomous sequence:

1. **BoB Ingestion** — partner's book of business imported into the platform
2. **Encrypted Vault** — partner credentials stored in the partner's dedicated encrypted vault
3. **Conductor** — partner's carrier registry + audit UI provisioned (agency view)
4. **Carrier Statement Pulls** — automated carrier statement retrieval begins

Each partner (e.g., Midwest Medigap / Matt Mitchell) receives their own isolated encrypted vault and agency view. No cross-partner data bleed is permitted.

---

#### HARD GATE — BAA Execution (Non-Negotiable Checkpoint)

> **No partner PHI may be ingested until the PARTNER→RPI Business Associate Agreement is fully executed.**

**Legal basis:** As custodian of a partner's clients' PHI, RPI functions as a Business Associate of that partner under HIPAA. The executed BAA is the legal instrument that authorizes RPI to hold and process that PHI.

**Canonical model:** the 2-gate onboarding model (PARTNER↔RPI BAA + audit-stream `BQ_STREAM_PARTNERS` activation) is defined canonically in `COMPLIANCE.md` §2 (the DD-Data-Access / BAA gate). This Operations section is the *procedure that enforces* it — the gate definitions live in the spine, not re-derived here.

**Reference:** The RPI→Google BAA is on file (signed 2026-02-04). The PARTNER→RPI BAA is the new agreement this onboarding loop creates for each partner.

**Enforcement (TWO coupled gates — partner PHI ingestion requires BOTH):**
- **Gate 1 — BAA executed.** The BoB ingestion pipeline must refuse to process partner PHI until a `baa_executed_date` is stamped on the partner record; the onboarding operator attaches the executed BAA document reference before the gate clears.
- **Gate 2 — Audit-streaming live.** The partner's named-DB writes are NOT audit-streamed (and therefore NOT §164.312(b)-covered) until the partner is activated in the BigQuery sink. Onboarding MUST set `BQ_STREAM_PARTNERS=<slug>` + the partner dataset + redeploy (per MT-011) BEFORE PHI ingestion. Ingesting partner PHI while its writes are un-audited is itself a §164.312(b) gap.
- This is a hard checkpoint — not revisitable after the fact. Any PHI that arrives before BOTH gates clear must be quarantined, not processed, and the incident disclosed per Part 3.

**HIPAA citation:** §164.308(a)(6) — Security Incident Procedures (BAA gate) + §164.312(b) — Audit Controls (streaming-activation gate). Failure of either gate before PHI ingestion is a reportable incident.

---

### Part 2 — Bulk-Delete Procedure

Bulk delete operations against any Firestore collection require the following sequence without exception.

#### Step 1 — Dry-Run COUNT First

Before executing any bulk delete, run a COUNT query using the intended filter and verify the result against the expected number.

- An unexpected count is the primary early-warning signal
- If the count does not match expectations, **stop** — do not proceed until the discrepancy is explained
- Document the expected count and the observed count before proceeding

#### Step 2 — Delete by Explicit Test-Only Marker

Delete operations must filter on a marker that was set **exclusively** at record creation for test-data identification purposes.

**Acceptable markers:**
- ID prefix (e.g., `e2e-test-`)
- A field set only at test-record creation (e.g., `is_test: true`)

**Prohibited filter patterns:**
- Any flag the runtime also writes for its own operational bookkeeping (dual-purpose flags)
- A dual-purpose flag will sweep real production records that the runtime has legitimately stamped

#### Step 3 — Confirm PITR is Active

Before any bulk delete on a collection holding conversation history, PII, or PHI, verify that Firestore Point-in-Time Recovery (PITR) is enabled on that collection. If PITR is not confirmed active, the delete does not proceed.

**HIPAA citation:** §164.308(a)(7) — Contingency Plan (Data Backup Plan + Disaster Recovery Plan). PITR is the technical implementation of the data backup and recovery requirement for Firestore-resident PHI and conversation records.

---

#### Worked Example — 2026-06-13 Chat Mirror Sweep

| Item | Detail |
|---|---|
| **What happened** | A cleanup job filtered on `chat_mirrored OR chat_origin`. A prior backlog-clear had stamped `chat_mirrored: true` on all messages in the backlog, including 37 real production messages. The delete swept those 37 records. |
| **Early warning** | The count returned 37. Expected: 0 production records. The mismatch was caught before operator sign-off. |
| **Recovery** | PITR restore. All 37 messages recovered with original document IDs and timestamps. Net data loss: zero. |
| **Root cause** | Dual-purpose flag — `chat_mirrored` was used both as a test-data marker and as a runtime bookkeeping field. |
| **Corrective action** | Cleanup filters now require an explicit `is_test: true` marker set only at test-record creation. Runtime bookkeeping fields are never used as delete filters. |

---

### Part 3 — Incident Disclosure Standard

Any operation that touches, modifies, exposes, or risks exposing PHI, PII, or partner credentials must be disclosed immediately upon discovery, regardless of whether data loss ultimately occurred.

**Required disclosure elements (all four, every time):**

1. **What happened** — precise description of the operation and its unintended effect
2. **What was affected** — scope: record count, collection(s), data types, partner(s) impacted
3. **How it was recovered** — specific recovery mechanism used (e.g., PITR restore, backup restore, manual reconstruction)
4. **Independent verification** — confirmation that the recovered state matches the pre-incident state (record count, IDs, timestamps)

**Prohibited disclosure patterns:**
- Burying the incident in a summary or status update without explicit identification
- Minimizing scope ("probably fine," "likely no real data")
- Disclosing recovery without disclosing the incident
- Disclosing the incident without the recovery proof

**HIPAA citation:** §164.308(a)(6) — Security Incident Procedures (identification, response, and reporting of security incidents).

---

### Part 4 — Breach / Loss-Response Posture

The three controls above constitute RPI's documented operational breach/loss-response posture:

| Control | What It Does | HIPAA Anchor |
|---|---|---|
| **BAA Gate** | Prevents unauthorized PHI ingestion at the partner onboarding boundary | §164.308(a)(6) |
| **PITR Recovery Path** | Ensures any Firestore-resident PHI or conversation record can be restored to a known-good state | §164.308(a)(7) |
| **Incident Disclosure Standard** | Ensures all data-touch incidents are surfaced immediately with recovery proof, not buried | §164.308(a)(6) |

**Canonical worked example:** The 2026-06-13 chat mirror sweep (37 records, PITR-recovered, net zero loss) is the reference implementation of all three controls operating together: the unexpected COUNT triggered the gate review, PITR executed the recovery, and the incident was disclosed with full scope + verification.

**Scope:** RPI is a multi-tenant custodian of partner credentials and partners' clients' PHI. All three controls apply to every partner lane, every collection holding PHI or PII, and every bulk operation regardless of whether the operator believes the data is "test only."
