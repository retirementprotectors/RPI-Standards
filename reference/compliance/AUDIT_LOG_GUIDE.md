# RPI Audit Log Access Guide

> **Purpose:** How to view and review PHI access logs in Google Workspace
> **Audience:** Administrators (JDM, designated reviewers)
> **Last Updated:** February 2026

---

## Why Audit Logs Matter

HIPAA requires that PHI access be "logged and reviewable." Google Workspace provides comprehensive audit logging automatically - we just need to know how to access and review it.

---

## Accessing Audit Logs

### Step 1: Open Google Admin Console

1. Go to [admin.google.com](https://admin.google.com)
2. Sign in with your admin account (@retireprotected.com)

### Step 2: Navigate to Audit Logs

```
Admin Console → Reporting → Audit and investigation → [Select log type]
```

Or use the direct path:
```
Admin Console → Reporting (left sidebar) → Audit log
```

---

## Key Log Types for PHI Monitoring

### 1. Drive Audit Log (Most Important for PHI)

**What it shows:** Who viewed, edited, downloaded, or shared files in Google Drive/Sheets

**Path:** `Reporting → Audit and investigation → Drive log events`

**Key events to monitor:**
| Event | What It Means |
|-------|---------------|
| `view` | Someone opened/viewed a file |
| `edit` | Someone modified a file |
| `download` | Someone downloaded a file |
| `share` | Someone shared a file with others |
| `print` | Someone printed a file |

**How to filter:**
- By user: See what a specific person accessed
- By file: See who accessed a specific file
- By date range: Focus on specific time period
- By event type: Filter to downloads only, shares only, etc.

### 2. Login Audit Log

**What it shows:** Who logged in, when, from where, success/failure

**Path:** `Reporting → Audit and investigation → Login audit log`

**Key events:**
| Event | What It Means |
|-------|---------------|
| `login_success` | Successful authentication |
| `login_failure` | Failed login attempt |
| `login_challenge` | 2FA challenge issued |
| `suspicious_login` | Google flagged as unusual |

### 3. Admin Audit Log

**What it shows:** Administrative changes (user creation, permission changes, etc.)

**Path:** `Reporting → Audit and investigation → Admin log events`

**Key events:**
| Event | What It Means |
|-------|---------------|
| `CREATE_USER` | New user account created |
| `DELETE_USER` | User account deleted |
| `GRANT_ADMIN_PRIVILEGE` | Someone given admin access |
| `CHANGE_PASSWORD` | Password was changed |

### 4. Token Audit Log

**What it shows:** Third-party app authorizations

**Path:** `Reporting → Audit and investigation → Token audit log`

**Why it matters:** Shows if users authorized any third-party apps to access their Google data

---

## Quarterly Review Checklist

Use this checklist for quarterly PHI access reviews:

### Drive Access Review
- [ ] Filter Drive logs for MATRIX file access
- [ ] Verify only authorized users accessed sensitive files
- [ ] Check for unusual download activity
- [ ] Review any external sharing events
- [ ] Document review date and findings

### User Access Review
- [ ] List all active users
- [ ] Verify each user still requires access
- [ ] Check for any terminated employees with active accounts
- [ ] Review admin privilege assignments
- [ ] Document review date and findings

### Login Activity Review
- [ ] Check for failed login patterns
- [ ] Review any suspicious login alerts
- [ ] Verify 2FA is enforced for all users
- [ ] Document review date and findings

---

## How to Export Logs

For documentation or deeper analysis:

1. Navigate to the desired audit log
2. Set your filters (date range, user, event type)
3. Click the **Download** icon (top right)
4. Choose format: CSV or Google Sheets
5. Save to a secure location in Drive

---

## Setting Up Alerts

Proactive monitoring via email alerts:

### Create a Custom Alert

1. Go to `Reporting → Audit and investigation`
2. Set your filter criteria
3. Click **Create alert** (bell icon)
4. Configure:
   - Alert name
   - Email recipients
   - Frequency

### Recommended Alerts

| Alert | Trigger | Why |
|-------|---------|-----|
| External sharing | Any external share event | PHI leaving organization |
| Mass download | 10+ downloads in 1 hour by same user | Potential data exfiltration |
| Failed logins | 5+ failures for same account | Potential attack |
| New admin | Admin privilege granted | Security-critical change |

---

## Log Retention

Google Workspace retains audit logs for:
- **Basic/Starter:** 6 months
- **Business/Enterprise:** 6 months (some events longer)

For HIPAA compliance, consider:
- Exporting logs quarterly to Drive for long-term retention
- Setting calendar reminders for log exports

---

## Quick Reference

| I want to see... | Go to... |
|------------------|----------|
| Who accessed a specific Sheet | Drive log → Filter by file name |
| What files a user accessed | Drive log → Filter by user |
| Who logged in today | Login log → Filter by date |
| Who was added as admin | Admin log → Filter by "GRANT_ADMIN" |
| What apps users authorized | Token log |

---

## Documentation

After each review, document:
1. Date of review
2. Who performed the review
3. Date range covered
4. Any anomalies found
5. Actions taken (if any)

Store documentation in: `[Secure Drive folder for compliance records]`

---

*For questions about audit log interpretation, contact the Fractional CTO (Jason Moran) or JDM.*
