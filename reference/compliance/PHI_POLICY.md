# RPI Protected Health Information (PHI) Policy

> **Policy Number:** SEC-001
> **Effective Date:** February 4, 2026
> **Owner:** CEO (Josh D. Millang)
> **Review Frequency:** Annual

---

## 1. Purpose

This policy establishes requirements for handling Protected Health Information (PHI) at Retirement Protectors, Inc. (RPI) to ensure compliance with HIPAA regulations and protect client privacy.

---

## 2. Scope

This policy applies to:
- All RPI employees, contractors, and agents
- All systems and devices that access, store, or transmit PHI
- All business operations involving client health information

---

## 3. Definitions

| Term | Definition |
|------|------------|
| **PHI** | Protected Health Information - individually identifiable health information transmitted or maintained in any form |
| **ePHI** | Electronic PHI - PHI in electronic form |
| **Minimum Necessary** | Limiting PHI access and disclosure to the minimum needed for the intended purpose |
| **Covered Entity** | Healthcare providers, health plans, and healthcare clearinghouses subject to HIPAA |
| **Business Associate** | Entity that handles PHI on behalf of a Covered Entity |

---

## 4. Policy Statements

### 4.1 Approved Storage Locations

**PHI may ONLY be stored in the following approved systems:**

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

### 4.2 Access Controls

- Access to PHI is granted on a need-to-know basis aligned with job responsibilities
- All users must authenticate via Google Workspace with mandatory 2FA
- Access permissions are reviewed quarterly
- Terminated employees have access revoked same-day

### 4.3 Transmission Security

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

### 4.4 Minimum Necessary Standard

- Access only the PHI required to perform your job function
- Share only the PHI necessary for the recipient's legitimate purpose
- Do not access client records without a business need
- Do not disclose PHI to coworkers who do not require it for their duties

### 4.5 Audit Logging

- All access to PHI systems is logged via Google Workspace audit logs
- Logs include: who accessed what, when, and what actions were taken
- Logs are retained per Google Workspace retention settings
- Logs are reviewed as part of quarterly security reviews

### 4.6 Incident Reporting

**All workforce members must immediately report:**
- Unauthorized access to PHI
- PHI sent to wrong recipient
- Lost or stolen devices with PHI access
- Suspected phishing or social engineering attempts
- Any other potential PHI breach

**Report to:** CEO (JDM) or COO (John Behn)

**There is no penalty for good-faith reporting of incidents.**

### 4.7 Training Requirements

- All workforce members must complete PHI handling training before accessing PHI
- Annual refresher training is required
- Training completion is documented via signed acknowledgment

---

## 5. Enforcement

Violations of this policy may result in:
- Additional training requirements
- Restricted system access
- Disciplinary action up to and including termination
- Potential legal liability for willful violations

---

## 6. Related Documents

| Document | Location |
|----------|----------|
| Security Compliance Framework | `reference/compliance/SECURITY_COMPLIANCE.md` |
| Compliance Standards | `reference/compliance/COMPLIANCE_STANDARDS.md` |

---

## 7. Policy Acknowledgment

All workforce members must acknowledge this policy by completing:
- Initial PHI training acknowledgment form
- Annual policy re-acknowledgment

---

## 8. Revision History

| Version | Date | Description | Author |
|---------|------|-------------|--------|
| 1.0 | 2026-02-04 | Initial policy | JDM / Claude Code |

---

*This policy is effective immediately upon publication. Questions should be directed to the CEO or COO.*
