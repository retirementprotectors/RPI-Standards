# RPI Compliance & Security Standards

> **Part of The Operating System** -- the governance layer of The Machine.
> See [OS.md](OS.md) for the full architecture.
> This document defines the standards -- what the rules ARE.

> **Version**: v2.0
> **Created**: January 25, 2026
> **Updated**: February 19, 2026
> **Policy Number**: SEC-001
> **Scope**: Universal - Applies to ALL RPI Projects, Employees, Contractors, and Agents
> **Status**: Active - Enforced
> **Owner**: CEO (Josh D. Millang)
> **Security Officer**: COO (John Behn)

---

## Purpose

This document establishes compliance and security standards for RPI's AI-powered platform. RPI handles:
- **Protected Health Information (PHI)** - Medicare, health conditions, providers, claims
- **Personally Identifiable Information (PII)** - Client demographics, SSNs, DOBs
- **Financial Data** - Account balances, transactions, commissions

Clear standards are required to protect clients, meet regulatory requirements (including HIPAA), and maintain trust. This policy applies to all systems and devices that access, store, or transmit PHI, PII, or financial data.

---

## Part 1: Data Classification

### Classification Levels

| Level | Description | Examples | Handling Requirements |
|-------|-------------|----------|----------------------|
| **PUBLIC** | Non-sensitive, can be shared freely | Company name, public marketing | None |
| **INTERNAL** | Business operations, not client data | Agent performance metrics, internal plans | Internal access only |
| **CONFIDENTIAL** | Client business data | Account balances, policy numbers, premium amounts | Need-to-know basis |
| **RESTRICTED** | PHI/PII requiring regulatory protection | SSN, DOB, health conditions, claims history | HIPAA/regulatory controls |

### Classification by Data Type

| Data Type | Classification | Storage Location | Encryption Required |
|-----------|---------------|------------------|---------------------|
| Client Name | CONFIDENTIAL | MATRIX | At rest |
| SSN | RESTRICTED | MATRIX (masked) | At rest + in transit |
| DOB | RESTRICTED | MATRIX | At rest |
| Health Conditions | RESTRICTED | Health DB (future) | At rest + in transit |
| Medicare Claims | RESTRICTED | Blue Button (future) | At rest + in transit |
| Policy Numbers | CONFIDENTIAL | MATRIX | At rest |
| Account Balances | CONFIDENTIAL | MATRIX | At rest |
| Agent Commissions | INTERNAL | MATRIX | At rest |

---

## Part 2: HIPAA Compliance

> **Status**: HIPAA applies to RPI. BAA signed with Google (February 4, 2026). PHI training deployed and enforced.

RPI is both a **Covered Entity** (handles PHI as part of client service -- Medicare data, health conditions, claims) and a **Business Associate** (processes PHI on behalf of clients). This policy establishes requirements for handling PHI to ensure compliance with HIPAA regulations and protect client privacy.

### Determination

- [x] Is RPI a "Covered Entity" under HIPAA? -- **Yes.**
- [x] Is RPI a "Business Associate" of any Covered Entity? -- **Yes.**
- [x] What Business Associate Agreements (BAAs) are required? -- **Google Workspace BAA signed Feb 4, 2026.**
- [x] Does Google Workspace meet HIPAA requirements? -- **Yes.** HIPAA-compliant with BAA in place.
- [x] What training is required? -- **PHI Training deployed.** See Part 10.

### HIPAA Triggers (Active)

| Activity | HIPAA Status | Controls |
|----------|-------------|----------|
| Storing client health conditions | **Active** -- PHI in MATRIX (Google Sheets) | BAA + encryption at rest |
| Blue Button API integration | **Future** -- Requires client consent + security | Design pending |
| AI processing health data | **Active** -- MCP tools access health data | Scoped access, no PHI in logs |
| Sharing health info with carriers | **Active** -- Carrier data exchanges | BAA per carrier (TBD) |

### Controls (Implemented)

1. **Administrative Safeguards**
   - Designated Security Officer: John Behn (COO)
   - PHI Training deployed Feb 4, 2026 (see Part 10 for status)
   - Incident response: Report breaches to John Behn immediately

2. **Physical Safeguards**
   - Google Workspace handles physical security (SOC 2, ISO 27001)
   - Device policy: No PHI on personal devices outside Google Workspace

3. **Technical Safeguards**
   - Access controls: MATRIX role-based permissions
   - Audit controls: Google Sheets edit history + GAS execution logs
   - Integrity controls: RAPID_API single-source-of-truth for writes
   - Transmission security: Google Workspace TLS encryption in transit
   - PHI masking: SSN shows last 4 only, DOB masked unless task-required
   - No PHI in: logs, error messages, Slack, personal email

---

## Part 3: Data Handling Rules

### Collection

| Rule | Implementation |
|------|----------------|
| **Minimum necessary** | Only collect/access data required for the task. Do not access client records without a business need. |
| **Consent** | Document client consent for data usage |
| **Source verification** | Validate data comes from authorized sources |
| **Minimum disclosure** | Share only the PHI necessary for the recipient's legitimate purpose. Do not disclose to coworkers who do not require it. |

### Storage

| Rule | Implementation |
|------|----------------|
| **Encryption at rest** | Google Workspace provides encryption |
| **Access controls** | MATRIX permissions by role |
| **Retention limits** | Define how long data is kept (TBD) |
| **Backup** | Google Workspace automatic backup |

**Approved PHI Storage Locations:**

| System | Purpose | Security |
|--------|---------|----------|
| Google Workspace (Sheets/Drive/Docs) | Client records, MATRIX | Google BAA, encryption, access controls |
| Gmail (@retireprotected.com) | Business communication | Google BAA, TLS encryption |
| Google Apps Script applications | Internal tools (PRODASHX, etc.) | Organization-only access, Google infrastructure |

**PHI is PROHIBITED in:**
- Personal email accounts
- Personal cloud storage (Dropbox, iCloud, OneDrive, personal Google accounts)
- Messaging platforms (Slack, text messages, WhatsApp)
- Unapproved third-party applications
- Personal devices not managed by RPI
- Physical documents removed from RPI premises

### Processing

| Rule | Implementation |
|------|----------------|
| **Purpose limitation** | Only use data for stated purpose |
| **Audit logging** | Log who accessed what, when |
| **AI processing** | Document what AI sees and does |

### Sharing & Transmission

| Rule | Implementation |
|------|----------------|
| **Need-to-know** | Only share with those who require access |
| **Third-party agreements** | Contracts with vendors handling data |
| **Client authorization** | Get consent before sharing externally |

**Internal transmission:**
- PHI transmitted via Gmail between @retireprotected.com addresses is encrypted in transit (TLS)
- Use Google Confidential Mode for sensitive PHI when additional protection is needed

**External transmission:**
- PHI may only be transmitted to external parties with proper authorization
- Use encrypted methods (secure portal, encrypted email) for external PHI transmission
- Never send PHI to personal email addresses of external parties

**Prohibited transmission methods:**
- Unencrypted email to non-Google recipients
- Text/SMS messages
- Fax (unless encrypted/secure fax service)
- Social media or messaging apps

### Disposal

| Rule | Implementation |
|------|----------------|
| **Secure deletion** | Purge data that's no longer needed |
| **Retention schedule** | Define retention periods by data type |

---

## Part 4: Access Control

### Role-Based Access (MATRIX)

| Role | Access Level | Data Visible |
|------|--------------|--------------|
| **Executive** | Full | All data |
| **Service Team** | Client-focused | Assigned clients, accounts, health |
| **Sales Team** | Pipeline-focused | Prospects, assigned clients |
| **BD Team** | Agent-focused | Agent data, production |
| **AI Agents** | Task-scoped | Only data needed for task |

**Access Control Rules:**
- Access to PHI/PII is granted on a need-to-know basis aligned with job responsibilities
- All users must authenticate via Google Workspace with mandatory 2FA
- Access permissions are reviewed quarterly
- Terminated employees have access revoked same-day

> For current role tables, MDJ instance access assignments, and detailed access matrices, see [POSTURE.md](POSTURE.md).

---

## Part 5: Audit & Logging

### What Must Be Logged

| Event | Log Contains | Retention |
|-------|--------------|-----------|
| **Data access** | Who, what record, when | 90 days (TBD) |
| **Data modification** | Who, what changed, old/new values | 1 year (TBD) |
| **AI queries** | What was asked, what data returned | 90 days (TBD) |
| **Export/download** | Who, what data, when | 1 year (TBD) |
| **Access failures** | Who, what denied, when | 90 days (TBD) |

**Logging Rules:**
- All access to PHI systems is logged via Google Workspace audit logs
- Logs include: who accessed what, when, and what actions were taken
- Logs are retained per Google Workspace retention settings
- Logs are reviewed as part of quarterly security reviews

> For current logging implementation status by system, see [MONITORING.md](MONITORING.md).

---

## Part 6: Incident Response

### Incident Categories

| Category | Definition | Response Time |
|----------|------------|---------------|
| **CRITICAL** | Data breach, unauthorized access to PHI | Immediate |
| **HIGH** | System outage affecting client service | 4 hours |
| **MEDIUM** | Security vulnerability discovered | 24 hours |
| **LOW** | Policy violation, minor issue | 1 week |

### Notification Timeframes

| Scenario | Who to Notify | Timeline |
|----------|---------------|----------|
| PHI breach | HHS + affected individuals | 60 days |
| PII breach (state laws apply) | State AG + affected individuals | Varies by state (Iowa: 60 days) |
| Security incident (internal) | Leadership | Immediate |

> For the incident response procedure (7-step process), notification details, and reporting instructions, see [OPERATIONS.md](OPERATIONS.md).

---

## Part 7: AI-Specific Considerations

### AI Data Processing Rules

| Rule | Rationale |
|------|-----------|
| **No PHI in prompts by default** | Minimize exposure |
| **Scoped MCP access** | Each AI instance only sees what it needs |
| **No training on client data** | RPI data doesn't train external models |
| **Audit trail for AI decisions** | Know what AI recommended and why |

### MDJ Guardrails (Future)

| Guardrail | Implementation |
|-----------|----------------|
| **Can't share data cross-instance** | MDJ-Sales can't access MDJ-Service data |
| **Can't take actions without approval** | AI recommends, humans decide |
| **Can't access raw PHI** | Only aggregated/anonymized health data |
| **Can't export bulk data** | Rate limits on data access |

### AI Disclosure

When AI interacts with clients (if ever):
- [ ] Disclose that AI is being used
- [ ] Provide human escalation path
- [ ] Don't make AI pretend to be human

---

## Part 8: Vendor & Third-Party Standards

### Current Platforms

| Platform | Data Stored | Security Status |
|----------|-------------|-----------------|
| **Google Workspace** | MATRIX, Drive, Gmail | SOC 2, ISO 27001, HIPAA BAA available |
| **GitHub** | Code only (no client data) | SOC 2 |
| **Slack** | Internal comms (no PHI) | SOC 2, HIPAA (Enterprise) |
| **GAS Web Apps** | Processed data | Google security |

### Third-Party Requirements

Before using new vendors that handle client data:
- [ ] Security assessment completed
- [ ] Data handling agreement signed
- [ ] HIPAA BAA (if applicable)
- [ ] Encryption verified
- [ ] Access controls confirmed

---

## Part 9: Disaster Recovery

### Backup Strategy

| Data | Backup Method | Frequency | Retention |
|------|---------------|-----------|-----------|
| **MATRIX** | Google Sheets version history | Automatic | 30 days |
| **Code** | GitHub | Every commit | Unlimited |
| **Documents** | Google Drive | Automatic | Unlimited |
| **GAS Apps** | `clasp push` to GAS | Manual | Versions |

### Recovery Procedures

| Scenario | Recovery Method | RTO Target |
|----------|-----------------|------------|
| Accidental data deletion | Sheets version history | 1 hour |
| Code rollback | Git revert | 15 minutes |
| GAS app rollback | `clasp deploy` to previous version | 30 minutes |
| Account compromise | Google account recovery | 4 hours |
| Full system outage | Contact Google support | 24 hours |

### What's NOT Covered (Gaps)

- [ ] Point-in-time recovery for MATRIX beyond 30 days
- [ ] Cross-region redundancy
- [ ] Offline backups
- [ ] Formal DR testing schedule

---

## Part 10: Training & Awareness

### Required Training

| Role | Training Required | Frequency |
|------|-------------------|-----------|
| All team members | PHI handling | Annual |
| Service/Sales | PHI/PII handling | Annual |
| Technical | Security best practices | Annual |
| Leadership | Incident response | Annual |

**Training Rules:**
- All workforce members must complete PHI handling training before accessing PHI
- Annual refresher training is required
- Training completion is documented via signed acknowledgment

> For training schedule, completion status, and roster tracking, see [OPERATIONS.md](OPERATIONS.md).

---

## Part 11: Compliance Checklists

### Before Launching New Features

- [ ] Data classification reviewed
- [ ] Access controls defined
- [ ] Logging implemented
- [ ] PHI/PII handling documented
- [ ] No hardcoded credentials
- [ ] Error messages don't expose sensitive data

### Before Using New Vendor

- [ ] Security assessment
- [ ] Data handling agreement
- [ ] BAA (if handling PHI)
- [ ] Documented in vendor inventory

> For periodic review schedule (quarterly access audits, annual vendor reviews, etc.), see [MONITORING.md](MONITORING.md).

---

## Part 12: Enforcement

Violations of these standards may result in:
- Additional training requirements
- Restricted system access
- Disciplinary action up to and including termination
- Potential legal liability for willful violations

**There is no penalty for good-faith reporting of incidents.** Report to CEO (JDM) or COO (John Behn).

---

## Appendix A: Definitions

| Term | Definition |
|------|------------|
| **PHI** | Protected Health Information - individually identifiable health information transmitted or maintained in any form |
| **ePHI** | Electronic PHI - PHI in electronic form |
| **PII** | Personally Identifiable Information - data that can identify a person |
| **BAA** | Business Associate Agreement - HIPAA contract with vendors |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **SOC 2** | Service Organization Control 2 - security audit standard |
| **Encryption at rest** | Data encrypted when stored |
| **Encryption in transit** | Data encrypted when transmitted |
| **Minimum Necessary** | Limiting PHI access and disclosure to the minimum needed for the intended purpose |
| **Covered Entity** | Healthcare providers, health plans, and healthcare clearinghouses subject to HIPAA |
| **Business Associate** | Entity that handles PHI on behalf of a Covered Entity |

---

## Appendix B: Open Questions

1. ~~**HIPAA Status**: Is RPI a Covered Entity or Business Associate?~~ -- **RESOLVED.** Yes to both. BAA signed with Google Feb 4, 2026.
2. **State Laws**: What state privacy laws apply (Iowa, others)? -- Iowa Consumer Data Protection Act (effective Jan 1, 2025)
3. **Retention**: What are legal retention requirements for different data types?
4. **Consent**: What consent language is needed for AI processing of client data?
5. **Breach Notification**: What are our exact notification obligations? -- Iowa: 60 days, HHS: 60 days for PHI
6. ~~**Training**: What formal training is legally required?~~ -- **RESOLVED.** PHI Training deployed, acknowledgment form live.

---

## Appendix C: Related Documents

| Document | Purpose |
|----------|---------|
| [OS.md](OS.md) | The Operating System architecture |
| [POSTURE.md](POSTURE.md) | Current security posture, role tables, access assignments |
| [MONITORING.md](MONITORING.md) | Logging status, periodic review schedules |
| [OPERATIONS.md](OPERATIONS.md) | Incident response procedures, training tracking, policy acknowledgment |
| `reference/compliance/SECURITY_COMPLIANCE.md` | Security framework and audit trail |
| `reference/maintenance/WEEKLY_HEALTH_CHECK.md` | Operational verification |
| `reference/maintenance/PROJECT_AUDIT.md` | Full compliance audit |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jan 25, 2026 | Initial skeleton |
| v1.0 | Feb 13, 2026 | HIPAA status resolved (BAA signed), PHI training status updated (10/13 complete), version upgraded from draft to active |
| v2.0 | Feb 19, 2026 | Merged from COMPLIANCE_STANDARDS.md + PHI_POLICY.md into OS kernel. Operational content moved to OPERATIONS.md, monitoring content to MONITORING.md, posture details to POSTURE.md. Added enforcement section, transmission security rules, approved storage locations, expanded definitions. |
