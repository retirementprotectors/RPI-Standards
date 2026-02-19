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
| Add a new GAS project | MONITORING.md (project list + scan loop), POSTURE.md (verification table), `clone-all-repos.sh` + `setup-hookify-symlinks.sh`, CLAUDE.md Project Locations tree |
| Add a new GAS web app (webapp) | POSTURE.md (add to verification table) |
| Complete a security audit | POSTURE.md (audit trail + dates) |
| Change deploy process | CLAUDE.md ONLY — never reference docs |
| Add a new MCP tool | MCP-Hub/CLAUDE.md (directory listing) |
| Change compliance rules | CLAUDE.md = the rule. Reference doc = the procedure. |

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
- [ ] Document completion date and who performed offboarding

**Responsible party:** COO (John Behn) or CEO (JDM).

**Super Admin access is locked to Josh + John Behn only.** OU `/RPI- Archived Users` is used for FINRA archiving.

---

## Part 3: Incident Response Procedure

### Response Steps

**Step 1: Contain**
Disable affected accounts/tokens immediately. Revoke any compromised API keys or OAuth grants. If a device is lost/stolen, initiate remote wipe via Google Workspace Admin.

**Step 2: Assess**
Determine scope: what data may have been accessed, how many records, what type (PHI, PII, financial). Identify the root cause — credential leak, phishing, misconfiguration, etc.

**Step 3: Notify**
Inform CEO (JDM) and COO (John Behn) immediately. For PHI breaches, HHS notification is required within 60 days. See notification requirements table below.

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
| Security incident (internal) | Leadership (JDM + John Behn) | Immediate |
| Breaches affecting 500+ individuals | HHS + media | 60 days |

### Contact Information

- **Google Workspace Support:** admin.google.com > Support
- **GitHub Security:** github.com/security
- **CEO (JDM):** Direct Slack DM or phone
- **COO (John Behn):** Direct Slack DM or phone

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
| Susan Kaelin, Bob Lacy, Vinnie Vazquez, Josh Archer, Aprille Trupiano, Lucas Dexter, Nikki Gray, Christa Irwin, Angelique Bonilla, John Behn | Shane Parmenter (CFO), Matt McCormick (B2B) |

---

## Part 5: PHI Incident Reporting

All workforce members must **immediately** report any of the following:

- Unauthorized access to PHI
- PHI sent to wrong recipient
- Lost or stolen devices with PHI access
- Suspected phishing or social engineering attempts
- Any other potential PHI breach

**Report to:** CEO (JDM) or COO (John Behn).

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

## Cross-References

- For the **rules** these processes enforce, see [STANDARDS.md](STANDARDS.md)
- For **current security state**, see [POSTURE.md](POSTURE.md)
- For **automated monitoring**, see [MONITORING.md](MONITORING.md)
- For the **full OS architecture**, see [OS.md](OS.md)

---

*Version: v1.0 | Feb 19, 2026*
*Consolidated from COMPLIANCE_STANDARDS.md, SECURITY_COMPLIANCE.md, PHI_POLICY.md, and CLAUDE.md*
