# RPI Security Compliance Framework

> **Owner:** CEO (JDM) with operational support from Fractional CTO
> **Last Updated:** 2026-02-04
> **Review Frequency:** Quarterly

---

## Executive Summary

RPI applications run on Google Cloud infrastructure (via Google Apps Script and Google Workspace). This architecture delegates infrastructure security to Google while RPI maintains responsibility for application-level security, access controls, and compliance policies.

---

## Part 1: What We Can Say to Clients/Partners

### Standard Security Statement

> "RPI's applications are built on Google Cloud infrastructure, which maintains SOC 2 Type II, ISO 27001, and HIPAA certifications. Access to our systems is restricted to authenticated personnel within our organization. We follow security best practices including mandatory two-factor authentication, credential management protocols, and regular access reviews."

### If Asked About Specific Certifications

| Question | Response |
|----------|----------|
| "Are you SOC 2 certified?" | "Our infrastructure runs on Google Cloud, which is SOC 2 Type II certified. RPI has not pursued independent SOC 2 certification as our architecture delegates infrastructure security to Google." |
| "Are you HIPAA compliant?" | **If BAA confirmed:** "Yes, we maintain a Business Associate Agreement with Google and operate on HIPAA-eligible infrastructure." **If not:** "We operate on HIPAA-eligible Google infrastructure. Please contact us to discuss specific PHI handling requirements." |
| "What security measures do you have?" | See Security Controls section below |
| "Can you sign a BAA with us?" | "We can execute a Business Associate Agreement. Our infrastructure is HIPAA-eligible through Google Cloud." |

### Security Controls Summary (For Client Conversations)

1. **Authentication:** Google Workspace SSO with mandatory 2FA
2. **Authorization:** Application access restricted to RPI organization members
3. **Encryption:** TLS 1.3 in transit, AES-256 at rest (Google-managed)
4. **Infrastructure:** Google Cloud Platform (SOC 2, ISO 27001, HIPAA certified)
5. **Access Reviews:** Quarterly review of user access
6. **Credential Management:** API keys and secrets stored in secure Script Properties, not in code
7. **Audit Logging:** Google Workspace audit logs retained per Google policy

---

## Part 2: Compliance Checklist

### Google Workspace Security Settings

| Item | Required State | Status | Verified Date |
|------|---------------|--------|---------------|
| 2FA enforced for all users | ON | [x] | 2026-02-04 |
| Less secure app access | OFF | [ ] | |
| Third-party app access | Restricted to approved apps | [ ] | |
| External sharing (Drive) | Restricted or warn | [ ] | |
| Email authentication (SPF/DKIM/DMARC) | Configured | [ ] | |
| Mobile device management | Basic or higher | [ ] | |
| Admin roles | Principle of least privilege | [ ] | |
| BAA with Google | Signed (if handling PHI) | [x] | 2026-02-04 |

### Application Security

| Item | Required State | Status | Verified Date |
|------|---------------|--------|---------------|
| No hardcoded credentials in code | All secrets in Script Properties | [x] | 2026-02-04 |
| Apps deployed as "Organization only" | All internal apps restricted | [~] | 2026-02-04 (PRODASH verified, others pending) |
| No alert()/confirm()/prompt() | Using custom modals | [x] | 2026-02-04 |
| API endpoints authenticated | API key validation where needed | [x] | 2026-02-04 |
| Git repos private | All RPI repos private on GitHub | [x] | 2026-02-04 |

### Access Management

| Item | Required State | Status | Verified Date |
|------|---------------|--------|---------------|
| User access list current | No former employees have access | [ ] | |
| Admin access limited | Only necessary personnel | [ ] | |
| Offboarding checklist exists | Documented process | [ ] | |
| Contractor access reviewed | Time-limited, minimal access | [ ] | |

---

## Part 3: Scheduled Security Tasks

### Weekly (Automated/Passive)
- Google Workspace automatically logs authentication events
- No manual action required

### Monthly
| Task | Owner | Week |
|------|-------|------|
| Review Google Workspace login alerts | Admin | 1st week |
| Check for any new third-party app authorizations | Admin | 1st week |

### Quarterly
| Task | Owner | Month |
|------|-------|-------|
| Full access review (who has Workspace access) | Admin/COO | Jan, Apr, Jul, Oct |
| Verify 2FA still enforced | Admin | Jan, Apr, Jul, Oct |
| Review and rotate any API keys/tokens | Dev | Jan, Apr, Jul, Oct |
| Update this compliance document | CEO/CTO | Jan, Apr, Jul, Oct |
| Test offboarding procedure | COO | Jan, Apr, Jul, Oct |

### Annually
| Task | Owner | Month |
|------|-------|-------|
| Full security review (external or internal) | CEO/CTO | January |
| Review BAA status with Google | CEO | January |
| Security awareness reminder to team | CEO/COO | January |
| Review and update Security Statement | CEO | January |

---

## Part 4: Offboarding Security Checklist

When an employee/contractor leaves RPI:

- [ ] Disable Google Workspace account (same day as departure)
- [ ] Remove from any shared drives with sensitive data
- [ ] Remove from GitHub organization (if applicable)
- [ ] Remove from Slack workspace
- [ ] Remove from any third-party tools (DocuSign, etc.)
- [ ] Review any API keys/tokens they had access to
- [ ] Transfer ownership of any Docs/Sheets they owned
- [ ] Document completion date and who performed offboarding

---

## Part 5: Incident Response

### If You Suspect a Security Issue

1. **Contain:** Disable affected accounts/tokens immediately
2. **Assess:** Determine what data may have been accessed
3. **Notify:** Inform CEO and affected parties as required
4. **Remediate:** Fix the vulnerability, rotate credentials
5. **Document:** Record what happened and how it was resolved

### Contact Information
- **Google Workspace Support:** admin.google.com → Support
- **GitHub Security:** github.com/security
- **Slack Security:** slack.com/help/requests/new

---

## Part 6: HIPAA-Specific Requirements

*Complete this section if RPI handles Protected Health Information (PHI)*

### BAA Status
- [x] BAA signed with Google Workspace
- [x] Date signed: February 4, 2026
- [x] Location of signed BAA: Google Admin Console → Account → Legal and Compliance

### PHI Handling Policies
- [x] Staff trained on PHI handling → `reference/compliance/PHI_TRAINING.md` + acknowledgment form
- [x] PHI only stored in approved systems (Workspace) → `reference/compliance/PHI_POLICY.md`
- [x] PHI not sent via unencrypted email → DLP rules configured in Google Admin
- [x] PHI access logged and reviewable → `reference/compliance/AUDIT_LOG_GUIDE.md`

### Breach Notification
- HIPAA requires notification within 60 days of discovering a breach
- Breaches affecting 500+ individuals must be reported to HHS and media
- Document any potential breaches immediately

---

## Part 7: Completed Security Actions (2026-02-04)

This section documents security improvements completed during the initial security audit.

### Infrastructure Security
- [x] Enabled 2FA enforcement for Google Workspace (1-week grace period for existing users)
- [x] Accepted HIPAA Business Associate Amendment with Google
- [x] Verified GitHub repos are private

### Application Security
- [x] Removed hardcoded credentials from code (CEO-Dashboard, RAPID_API)
- [x] Rotated exposed Slack tokens
- [x] Updated all MCP config files with new tokens
- [x] Added API key authentication to RAPID_API
- [x] Replaced forbidden UI patterns (alert/confirm/prompt)
- [x] Verified PRODASH has organization-only access

### Documentation
- [x] Created security compliance documentation
- [x] Added org-only access enforcement to CLAUDE.md
- [x] Added deploy-time security hook for access verification

### Pending Verification
| App | Organization-Only Access |
|-----|-------------------------|
| PRODASH | ✅ Verified 2026-02-04 |
| SENTINEL | ⏳ Pending |
| DEX | ⏳ Pending |
| RIIMO | ⏳ Pending |
| CAM | ⏳ Pending |
| CEO-Dashboard | ⏳ Pending |
| C3 | ⏳ Pending |

---

## Part 8: Remaining Action Items

### This Week (Priority 2)
- [ ] Review current Workspace users for former employees/contractors
- [ ] Confirm offboarding process with COO (John Behn)

### This Month (Priority 3)
- [ ] Set quarterly calendar reminders for access reviews
- [ ] Brief team on 2FA requirements and security reporting

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-02-04 | Initial document created | Claude Code |
| 2026-02-04 | 2FA enforcement enabled, HIPAA BAA accepted | JDM + Claude Code |
| 2026-02-04 | Merged IMMEDIATE_ACTIONS.md into this document | Claude Code |

---

*This document should be reviewed quarterly and updated as RPI's security posture evolves.*
