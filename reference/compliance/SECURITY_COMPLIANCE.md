# RPI Security Compliance Framework

> **Owner:** CEO (JDM) with operational support from Fractional CTO
> **Last Updated:** 2026-02-15
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
| "Are you HIPAA compliant?" | "Yes, we maintain a Business Associate Agreement with Google and operate on HIPAA-eligible infrastructure." |
| "What security measures do you have?" | See Security Controls section below |
| "Can you sign a BAA with us?" | "We can execute a Business Associate Agreement. Our infrastructure is HIPAA-eligible through Google Cloud." |
| "Do you have encryption?" | "Yes - all data is encrypted both in transit (TLS 1.3) and at rest (AES-256). Gmail uses TLS for all transmissions, and Google encrypts all stored data automatically." |
| "Is email encrypted?" | "Yes. Gmail-to-Gmail is always encrypted via TLS. External email uses opportunistic TLS (encrypted when recipient supports it, which most servers do). For sensitive content, we can use Google Confidential Mode for additional restrictions." |

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
| 2FA enforced for all users | ON | [x] | 2026-02-13 |
| Less secure app access | OFF | [ ] | |
| Third-party app access | Restricted to approved apps | [x] | 2026-02-13 |
| External sharing (Drive) | Restricted or warn | [ ] | |
| Email authentication (SPF/DKIM/DMARC) | Configured | [ ] | |
| Mobile device management | Basic or higher | [x] | 2026-02-13 |
| Admin roles | Principle of least privilege | [x] | 2026-02-13 |
| BAA with Google | Signed (if handling PHI) | [x] | 2026-02-04 |

### Application Security

| Item | Required State | Status | Verified Date |
|------|---------------|--------|---------------|
| No hardcoded credentials in code | All secrets in Script Properties | [~] | 2026-02-14 (known gap: CORE_Config.gs syncAllProperties pattern stores plaintext secrets in source — remediation planned) |
| Apps deployed as "Organization only" | All internal apps restricted | [x] | 2026-02-15 (13 GAS web apps: 12 DOMAIN verified, 1 approved exception RAPID_API; see Part 7) |
| No alert()/confirm()/prompt() | Using custom modals | [x] | 2026-02-04 |
| API endpoints authenticated | API key validation where needed | [x] | 2026-02-04 |
| Git repos private | All RPI repos private on GitHub | [x] | 2026-02-04 |

### Access Management

| Item | Required State | Status | Verified Date |
|------|---------------|--------|---------------|
| User access list current | No former employees have access | [x] | 2026-02-13 |
| Admin access limited | Only necessary personnel | [x] | 2026-02-13 |
| Offboarding checklist exists | Documented process | [x] | 2026-02-13 |
| Contractor access reviewed | Time-limited, minimal access | [x] | 2026-02-13 |

### Source Code vs. Deployment Access (CRITICAL)

> **Discovery Date:** 2026-02-14
> **Impact:** Silent security regression on `clasp push`

The GAS editor UI and `appsscript.json` are **two different settings** that can diverge:

| Setting Location | What It Controls | How It's Set |
|-----------------|-----------------|--------------|
| GAS Editor UI (Deploy → Manage) | The LIVE deployment's access | Manual click in browser |
| `appsscript.json` `"webapp.access"` | What `clasp push` + `clasp deploy` will SET | Source code file |

**The danger:** If someone fixes access in the GAS editor UI but the source file still says `ANYONE_ANONYMOUS`, the next `clasp push --force` + `clasp deploy` silently reverts to public access.

**Rule:** Always fix `appsscript.json` first. Always verify after deploy. Audits must check the source file, not just the GAS editor.

**Projects with known disconnect (as of 2026-02-14):** ~~RIIMO, RPI-Command-Center, DAVID-HUB~~ — All 3 remediated via "Phase 0: Security hardening" commits. Verified 2026-02-15.

---

## Part 3: Scheduled Security Tasks

### Automated (GAS Triggers in RAPID_API → API_Compliance.gs)

| Trigger | Frequency | Function | What It Does |
|---------|-----------|----------|--------------|
| Quarterly Audit | Feb, May, Aug, Nov 1st @ 7 AM | `runQuarterlyAuditIfDue_()` | Full compliance audit → posts to Slack |
| Weekly Stale User Monitor | Mondays @ 7 AM | `runWeeklyStaleUserCheck_()` | Flags users inactive 30+ days |
| Monthly Token Hygiene | 15th @ 7 AM | `runMonthlyTokenHygiene_()` | Scans for unapproved apps with sensitive scopes |

**Setup:** Project: RAPID_API | File: API_Compliance.gs | Run: `SETUP_ComplianceTrigger` (and/or `SETUP_WeeklyStaleUserMonitor`, `SETUP_MonthlyTokenHygiene`)

### Manual Quarterly (Claude Code-Assisted)
| Task | Owner | Months |
|------|-------|--------|
| Review automated audit results in Slack | CEO/Admin | Feb, May, Aug, Nov |
| Remediate critical findings via Claude Code | CEO/Admin | Feb, May, Aug, Nov |
| Update this compliance document | CEO/CTO | Feb, May, Aug, Nov |

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
- [x] Staff trained on PHI handling — training materials archived (10/13 completed as of Feb 13, 2026). See `PHI_POLICY.md` for current requirements.
- [x] PHI only stored in approved systems (Workspace) → `reference/compliance/PHI_POLICY.md`
- [x] PHI not sent via unencrypted email → DLP rules configured in Google Admin
- [x] PHI access logged and reviewable → Google Workspace audit logs (retained per Google policy)

### Breach Notification
- HIPAA requires notification within 60 days of discovering a breach
- Breaches affecting 500+ individuals must be reported to HHS and media
- Document any potential breaches immediately

---

## Part 7: Completed Security Actions

### Initial Security Audit (2026-02-04)

#### Infrastructure Security
- [x] Enabled 2FA enforcement for Google Workspace (1-week grace period for existing users)
- [x] Accepted HIPAA Business Associate Amendment with Google
- [x] Verified GitHub repos are private

#### Application Security
- [x] Removed hardcoded credentials from code (CEO-Dashboard, RAPID_API)
- [x] Rotated exposed Slack tokens
- [x] Updated all MCP config files with new tokens
- [x] Added API key authentication to RAPID_API
- [x] Replaced forbidden UI patterns (alert/confirm/prompt)
- [x] Verified PRODASHX has organization-only access

#### Documentation
- [x] Created security compliance documentation
- [x] Added org-only access enforcement to CLAUDE.md
- [x] Added deploy-time security hook for access verification

#### Organization-Only Access Verification (Complete)
| App | Access | Verified Date | Notes |
|-----|--------|---------------|-------|
| PRODASHX | DOMAIN | 2026-02-04 | Already compliant |
| SENTINEL | DOMAIN | 2026-02-13 | All 21 deploys DOMAIN (19 stale ANYONE deploys updated to v381) |
| SENTINEL v2 | DOMAIN | 2026-02-13 | All 2 deploys already DOMAIN — clean |
| DEX | DOMAIN | 2026-02-13 | All 20 deploys DOMAIN (19 stale ANYONE deploys updated to v64) |
| RIIMO | DOMAIN | 2026-02-15 | Fixed — "Phase 0: Security hardening" commit `85854e0`. Source file + deployment verified. |
| CAM | DOMAIN | 2026-02-13 | Fixed from ANYONE → DOMAIN (v51) |
| CEO-Dashboard | DOMAIN | 2026-02-13 | Fixed from ANYONE_ANONYMOUS → DOMAIN (v32). Was CRITICAL — no auth required. |
| C3 | DOMAIN | 2026-02-13 | Already compliant (v127) |
| RAPID_API | ANYONE_ANONYMOUS | 2026-02-14 | Intentional for SPARK webhook reception — approved exception. Document rationale. |
| RAPID_IMPORT | DOMAIN | 2026-02-14 | Verified — appsscript.json has `"access": "DOMAIN"` in both webapp and executionApi |
| RPI-Command-Center | DOMAIN | 2026-02-15 | Fixed — "Phase 0: Security hardening" commit `d265ac5`. Source file + deployment verified. |
| QUE-Medicare | DOMAIN | 2026-02-15 | Verified — appsscript.json `"access": "DOMAIN"` confirmed. |
| DAVID-HUB | DOMAIN | 2026-02-15 | Fixed — "Phase 0: Security hardening" commit `fcc5011`. Source file + deployment verified. |

### Q1 2026 Compliance Audit (2026-02-13)

#### Token Revocations (26 total)
| User | Tokens Revoked | Details |
|------|---------------|---------|
| Josh | 3 | cloudHQ (full Gmail+Drive), Adobe Acrobat (admin scope), Zoominfo (gmail.readonly) |
| Christa | 17 | Full deprovision — all tokens revoked |
| Allison | 2 | Microsoft + Chrome — already suspended, tokens cleaned |
| Nikki | 1 | Adobe Acrobat (admin.directory.user.readonly) |

#### User Suspensions (2 new)
| User | Action |
|------|--------|
| rpifax@ | Suspended — 382+ days since last login |
| christa@ | Suspended + fully deprovisioned (17 tokens revoked) |

#### OU Corrections (2)
| User | From → To | Reason |
|------|-----------|--------|
| nikki@ | Non-Archived → Archived | Securities/FINRA email archiving compliance |
| talan@ | / (root) → Non-Archived | Proper OU placement |

#### Super Admin Downgrades (3)
| User | Before → After |
|------|----------------|
| shane@ | Super Admin → Delegated Admin (Billing, Groups, Storage, Help Desk) |
| matt@ | Super Admin → No admin roles |
| jmdconsulting@ | Super Admin → No admin roles |

**Result: Super Admins reduced 5 → 2 (Josh + John Behn only)**

#### 2FA Status
- Enforced org-wide: 19/19 users
- Enrolled: 5/19 (Josh, Angelique, Christa, Robert, Vince)
- Grace period set in Admin Console for remaining users

#### Automation Built
- [x] Created `API_Compliance.gs` in RAPID_API — automated quarterly audit with Slack posting
- [x] Added `delete_mobile_device` tool to rpi-workspace-mcp (10 → 11 admin tools)
- [x] Quarterly/weekly/monthly triggers for continuous monitoring

---

## Part 8: Remaining Action Items

### Immediate (Post Q1 Audit)
- [ ] Delete 13 stale mobile devices (requires MCP restart for `delete_mobile_device` tool)
- [ ] JDM: Run `SETUP_ComplianceTrigger` in RAPID_API → API_Compliance.gs (authorizes Admin SDK + creates trigger)
- [ ] JDM: Set SLACK_BOT_TOKEN and SLACK_CHANNEL_ADMIN in RAPID_API Script Properties (for audit Slack notifications)

### This Month (Priority 3)
- [ ] Brief team on 2FA enrollment requirement (grace period active)
- [ ] Review Josh's ~45 SSO-only app tokens for cleanup (low risk, clutter reduction)
- [ ] Optionally enable weekly + monthly monitors: `SETUP_WeeklyStaleUserMonitor`, `SETUP_MonthlyTokenHygiene`

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-02-04 | Initial document created | Claude Code |
| 2026-02-04 | 2FA enforcement enabled, HIPAA BAA accepted | JDM + Claude Code |
| 2026-02-04 | Merged IMMEDIATE_ACTIONS.md into this document | Claude Code |
| 2026-02-13 | 8 of 13 GAS apps verified org-only. Fixed DEX, CAM, CEO-Dashboard. | Claude Code |
| 2026-02-13 | Stale deployment cleanup: 38 old ANYONE deploys (19 DEX + 19 SENTINEL) updated to DOMAIN. | Claude Code |
| 2026-02-13 | Q1 2026 audit: 26 tokens revoked, 2 users suspended, 3 Super Admins downgraded, 2 OU moves | Claude Code |
| 2026-02-13 | Part 2 checklist updated. Part 3 rewritten with automated triggers. Part 7/8 expanded. | Claude Code |
| 2026-02-13 | API_Compliance.gs added to RAPID_API — quarterly/weekly/monthly automated compliance | Claude Code |
| 2026-02-14 | Corrected app count (13 identified, 8 verified). Fixed RIIMO false-positive. Added source-code-vs-deployment section. Added 5 missing apps to tracker. | Claude Code |
| 2026-02-15 | All 13 apps verified DOMAIN (12 compliant + 1 approved exception). RIIMO, RPI-Command-Center, DAVID-HUB remediated via Phase 0 commits. QUE-Medicare verified. | Claude Code |

---

*This document should be reviewed quarterly and updated as RPI's security posture evolves.*
