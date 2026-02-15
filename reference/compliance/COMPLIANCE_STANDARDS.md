# RPI Compliance & Security Standards

> **Version**: v1.0
> **Created**: January 25, 2026
> **Updated**: February 13, 2026
> **Scope**: Universal - Applies to ALL RPI Projects
> **Status**: Active - Enforced

---

## Purpose

This document establishes compliance and security standards for RPI's AI-powered platform. Given that RPI handles:
- **Protected Health Information (PHI)** - Medicare, health conditions, providers
- **Personally Identifiable Information (PII)** - Client demographics, SSNs, DOBs
- **Financial Data** - Account balances, transactions, commissions

...clear standards are required to protect clients, meet regulatory requirements, and maintain trust.

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

### Determination

- [x] Is RPI a "Covered Entity" under HIPAA? — **Yes.** RPI handles PHI (Medicare data, health conditions, claims) as part of client service.
- [x] Is RPI a "Business Associate" of any Covered Entity? — **Yes.** RPI processes PHI on behalf of clients.
- [x] What Business Associate Agreements (BAAs) are required? — **Google Workspace BAA signed Feb 4, 2026.**
- [x] Does Google Workspace meet HIPAA requirements for our use case? — **Yes.** Google Workspace is HIPAA-compliant with BAA in place. PHI stored only in Google Workspace (Drive, Sheets).
- [x] What training is required for team members? — **PHI Training deployed.** Training materials archived; see `reference/compliance/PHI_POLICY.md` for current requirements. 10 of 13 team members completed acknowledgment as of Feb 13, 2026.

### HIPAA Triggers (Active)

| Activity | HIPAA Status | Controls |
|----------|-------------|----------|
| Storing client health conditions | **Active** — PHI in MATRIX (Google Sheets) | BAA + encryption at rest |
| Blue Button API integration | **Future** — Requires client consent + security | Design pending |
| AI processing health data | **Active** — MCP tools access health data | Scoped access, no PHI in logs |
| Sharing health info with carriers | **Active** — Carrier data exchanges | BAA per carrier (TBD) |

### Controls (Implemented)

1. **Administrative Safeguards**
   - Designated Security Officer: John Behn (COO)
   - PHI Training: Training materials archived (deployed Feb 4, 2026). See `PHI_POLICY.md` for current requirements.
   - Acknowledgment form: 10/13 team members completed
   - Incident response: Report breaches to John Behn immediately
   - PHI Policy: `reference/compliance/PHI_POLICY.md`

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
| **Minimum necessary** | Only collect data required for service | 
| **Consent** | Document client consent for data usage |
| **Source verification** | Validate data comes from authorized sources |

### Storage

| Rule | Implementation |
|------|----------------|
| **Encryption at rest** | Google Workspace provides encryption |
| **Access controls** | MATRIX permissions by role |
| **Retention limits** | Define how long data is kept (TBD) |
| **Backup** | Google Workspace automatic backup |

### Processing

| Rule | Implementation |
|------|----------------|
| **Purpose limitation** | Only use data for stated purpose |
| **Audit logging** | Log who accessed what, when |
| **AI processing** | Document what AI sees and does |

### Sharing

| Rule | Implementation |
|------|----------------|
| **Need-to-know** | Only share with those who require access |
| **Third-party agreements** | Contracts with vendors handling data |
| **Client authorization** | Get consent before sharing externally |

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

### MDJ Instance Access (Future)

| MDJ Instance | Data Scope |
|--------------|------------|
| MDJ-Service-Medicare | Service clients + health data |
| MDJ-Service-Retirement | Service clients + account data |
| MDJ-Sales-Medicare | Prospects + plan data (no health) |
| MDJ-Sales-Retirement | Prospects + account data |
| MDJ-BD | Agents + production (no client PII) |
| MDJ-Executive | All (aggregated, not individual PHI) |

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

### Current Logging Status

| System | Logging Available | Implemented |
|--------|-------------------|-------------|
| MATRIX (Sheets) | Edit history | ✅ Native |
| GAS Web Apps | Execution logs | ✅ Native |
| MCP Tools | Query logging | 🔲 Not yet |
| MDJ Instances | Conversation logging | 🔲 Future |

---

## Part 6: Incident Response

### Incident Categories

| Category | Definition | Response Time |
|----------|------------|---------------|
| **CRITICAL** | Data breach, unauthorized access to PHI | Immediate |
| **HIGH** | System outage affecting client service | 4 hours |
| **MEDIUM** | Security vulnerability discovered | 24 hours |
| **LOW** | Policy violation, minor issue | 1 week |

### Response Process (Placeholder)

1. **Detect** - Identify the incident
2. **Contain** - Stop ongoing damage
3. **Assess** - Determine scope and impact
4. **Notify** - Inform affected parties (if required)
5. **Remediate** - Fix the root cause
6. **Document** - Record incident and response
7. **Review** - Update controls to prevent recurrence

### Notification Requirements

| Scenario | Who to Notify | Timeline |
|----------|---------------|----------|
| PHI breach | HHS + affected individuals | 60 days |
| PII breach (state laws apply) | State AG + affected individuals | Varies by state (Iowa: 60 days) |
| Security incident (internal) | Leadership | Immediate |

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

| Role | Training Required | Frequency | Status |
|------|-------------------|-----------|--------|
| All team members | PHI handling | Annual | **Deployed** — 10/13 completed |
| Service/Sales | PHI/PII handling | Annual | **Deployed** (same as above) |
| Technical | Security best practices | Annual | TBD |
| Leadership | Incident response | Annual | TBD |

### Training Status

- [x] PHI Training — Training materials archived (deployed Feb 4, 2026). See `PHI_POLICY.md`.
- [x] PHI Acknowledgment Form — Live, 10 of 13 team members completed
- [ ] General data privacy training — Not yet developed
- [ ] AI usage guidelines — Not yet developed
- [ ] Incident reporting process — Not yet developed

### PHI Training Completion (as of Feb 13, 2026)

| Completed | Outstanding |
|-----------|-------------|
| Susan Kaelin, Bob Lacy, Vinnie Vazquez, Josh Archer, Aprille Trupiano, Lucas Dexter, Nikki Gray, Christa Irwin, Angelique Bonilla, John Behn | Shane Parmenter (CFO), Matt McCormick (B2B) |

---

## Part 11: Compliance Checklist

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

### Periodic Reviews

- [ ] Access permissions audit (quarterly)
- [ ] Vendor security review (annual)
- [ ] Policy review and update (annual)
- [ ] Training completion verification (annual)

---

## Appendix A: Definitions

| Term | Definition |
|------|------------|
| **PHI** | Protected Health Information - individually identifiable health info |
| **PII** | Personally Identifiable Information - data that can identify a person |
| **BAA** | Business Associate Agreement - HIPAA contract with vendors |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **SOC 2** | Service Organization Control 2 - security audit standard |
| **Encryption at rest** | Data encrypted when stored |
| **Encryption in transit** | Data encrypted when transmitted |

---

## Appendix B: Open Questions

1. ~~**HIPAA Status**: Is RPI a Covered Entity or Business Associate?~~ — **RESOLVED.** Yes to both. BAA signed with Google Feb 4, 2026.
2. **State Laws**: What state privacy laws apply (Iowa, others)? — Iowa Consumer Data Protection Act (effective Jan 1, 2025)
3. **Retention**: What are legal retention requirements for different data types?
4. **Consent**: What consent language is needed for AI processing of client data?
5. **Breach Notification**: What are our exact notification obligations? — Iowa: 60 days, HHS: 60 days for PHI
6. ~~**Training**: What formal training is legally required?~~ — **RESOLVED.** PHI Training deployed, acknowledgment form live.

---

## Appendix C: Related Documents

| Document | Purpose |
|----------|---------|
| `reference/compliance/PHI_POLICY.md` | PHI handling requirements |
| `reference/compliance/SECURITY_COMPLIANCE.md` | Security framework and audit trail |
| `reference/maintenance/WEEKLY_HEALTH_CHECK.md` | Operational verification |
| `reference/maintenance/PROJECT_AUDIT.md` | Full compliance audit |
| `reference/integrations/GHL_INTEGRATION.md` | GHL/GoHighLevel integration patterns |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jan 25, 2026 | Initial skeleton |
| v1.0 | Feb 13, 2026 | HIPAA status resolved (BAA signed), PHI training status updated (10/13 complete), version upgraded from draft to active |

<!-- Promoted from MEMORY.md 2026-02-15 -->
- New fields flow: RAPID_CORE schemas → RAPID_API SETUP → RAPID_IMPORT maps → watcher.js
