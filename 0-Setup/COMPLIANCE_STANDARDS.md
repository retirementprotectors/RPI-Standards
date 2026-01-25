# RPI Compliance & Security Standards

> **Version**: v0.1 (Skeleton - Awaiting Review)  
> **Created**: January 25, 2026  
> **Scope**: Universal - Applies to ALL RPI Projects  
> **Status**: Draft - Requires legal/compliance review before enforcement

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

## Part 2: HIPAA Considerations

> **Note**: This section is a placeholder. RPI should consult with healthcare compliance counsel to determine HIPAA applicability and requirements.

### Questions to Answer

- [ ] Is RPI a "Covered Entity" under HIPAA?
- [ ] Is RPI a "Business Associate" of any Covered Entity?
- [ ] What Business Associate Agreements (BAAs) are required?
- [ ] Does Google Workspace meet HIPAA requirements for our use case?
- [ ] What training is required for team members?

### Potential HIPAA Triggers

| Activity | Potential HIPAA Implication |
|----------|---------------------------|
| Storing client health conditions | May require PHI protections |
| Blue Button API integration | Requires client consent + security |
| AI processing health data | Requires safeguards + audit trail |
| Sharing health info with carriers | May require BAA |

### Placeholder Controls (Pending Legal Review)

If HIPAA applies, RPI will need:

1. **Administrative Safeguards**
   - Designated Security Officer
   - Risk assessment process
   - Workforce training
   - Incident response procedures

2. **Physical Safeguards**
   - Workstation security policies
   - Device controls

3. **Technical Safeguards**
   - Access controls (role-based)
   - Audit controls (logging)
   - Integrity controls (change tracking)
   - Transmission security (encryption)

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
| PHI breach (if HIPAA applies) | HHS + affected individuals | 60 days |
| PII breach (if state laws apply) | State AG + affected individuals | Varies by state |
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

### Required Training (Placeholder)

| Role | Training Required | Frequency |
|------|-------------------|-----------|
| All team members | Data handling basics | Annual |
| Service/Sales | PHI/PII handling (if HIPAA applies) | Annual |
| Technical | Security best practices | Annual |
| Leadership | Incident response | Annual |

### Training Not Yet Developed

- [ ] General data privacy training
- [ ] HIPAA training (if applicable)
- [ ] AI usage guidelines
- [ ] Incident reporting process

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

## Appendix B: Open Questions for Legal/Compliance Review

1. **HIPAA Status**: Is RPI a Covered Entity or Business Associate?
2. **State Laws**: What state privacy laws apply (Iowa, others)?
3. **Retention**: What are legal retention requirements for different data types?
4. **Consent**: What consent language is needed for AI processing of client data?
5. **Breach Notification**: What are our exact notification obligations?
6. **Training**: What formal training is legally required?

---

## Appendix C: Related Documents

| Document | Purpose |
|----------|---------|
| `0-Setup/MASTER_AGENT_FRAMEWORK.md` | Agent roles and access patterns |
| `0-Setup/MDJ_STRATEGIC_VISION.md` | MDJ instance scoping |
| `0-Setup/RPI_PLATFORM_BLUEPRINT.md` | Data architecture |
| `1-Manage/WEEKLY_HEALTH_CHECK.md` | Operational verification |
| `2-Production/PRE_LAUNCH_CHECKLIST.md` | Launch security checks |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jan 25, 2026 | Initial skeleton - awaiting legal review |

---

*This document is a starting point. It requires review by legal counsel and compliance professionals before enforcement. RPI's specific regulatory obligations depend on factors that should be assessed by qualified advisors.*
