# RPI PHI Training Acknowledgment System

> **Purpose:** Create a defensible, auditable record of PHI training compliance
> **Owner:** CEO / COO
> **Review Frequency:** Annual

---

## System Components

### 1. Google Form (Acknowledgment Collection)

**Form Name:** `RPI PHI Training Acknowledgment`

**Form Fields:**
1. Full Legal Name (Short answer, required)
2. Email Address (Email validation, required)
3. Date (Auto-captured by Google Forms)
4. Acknowledgment Statement (Checkbox, required):
   - "I have read and understand the RPI PHI Training document"
   - "I agree to follow the PHI handling policies described"
   - "I understand that violations may result in disciplinary action"
   - "I will immediately report any PHI incidents to leadership"
5. Policy Version Acknowledged (Hidden/Auto: "v1.0 - February 2026")

**Form Settings:**
- Collect email addresses: ON
- Limit to 1 response: ON (per email)
- Edit after submit: OFF
- Response destination: Google Sheet (for audit trail)

### 2. Response Sheet (Audit Trail)

**Sheet Name:** `PHI Training Acknowledgments - [Year]`

**Columns:**
| Column | Source |
|--------|--------|
| Timestamp | Auto |
| Email Address | Form |
| Full Legal Name | Form |
| Acknowledgment 1 | Form checkbox |
| Acknowledgment 2 | Form checkbox |
| Acknowledgment 3 | Form checkbox |
| Acknowledgment 4 | Form checkbox |
| Policy Version | Form (hidden) |
| Employment Status | Manual (Active/Terminated/Contractor) |
| Notes | Manual |

**Sheet Location:** `RPI Compliance > PHI Training > Acknowledgments`

---

## Process Workflows

### New Hire Onboarding

1. **Day 1:** HR/Manager sends PHI Training link
2. **Within 3 days:** New hire must complete training + acknowledgment
3. **Day 4:** COO verifies acknowledgment in sheet
4. **If not complete:** Access to PHI systems blocked until complete

**Onboarding Checklist Item:**
```
[ ] PHI Training completed and acknowledgment submitted
    - Training doc: [Link to PHI_TRAINING.md in Drive]
    - Acknowledgment form: [Link to Google Form]
```

### Annual Re-Acknowledgment

**Timeline:** January each year (align with annual security review)

1. **Jan 1-7:** CEO/COO sends annual re-acknowledgment email to all staff
2. **Jan 7-21:** Staff complete acknowledgment (2-week window)
3. **Jan 22:** COO reviews completion, follows up with non-compliant
4. **Jan 31:** Final deadline - escalate to CEO if not complete

**Annual Email Template:**
```
Subject: [ACTION REQUIRED] Annual PHI Training Re-Acknowledgment Due by Jan 21

Team,

As part of our annual security compliance, all team members must
re-acknowledge our PHI (Protected Health Information) handling policies.

1. Review the PHI Training document: [LINK]
2. Complete the acknowledgment form: [LINK]

Deadline: January 21, [YEAR]

This is required for continued access to client systems.

Questions? Contact John Behn or Josh Millang.

- RPI Leadership
```

### Policy Update Re-Acknowledgment

When PHI policies are materially updated:

1. Update PHI_TRAINING.md and PHI_POLICY.md
2. Increment version number (e.g., v1.0 → v1.1)
3. Update Google Form hidden field with new version
4. Send re-acknowledgment request to all staff
5. Document update in revision history

---

## Audit & Compliance

### Quarterly Check

During quarterly security reviews:
- [ ] Export acknowledgment sheet
- [ ] Verify all active employees have current acknowledgment
- [ ] Flag any gaps or expired acknowledgments
- [ ] Document review date and reviewer

### Documentation Retention

| Document | Retention Period |
|----------|-----------------|
| Acknowledgment responses | 7 years after termination |
| Training documents (versioned) | Permanent |
| Annual re-acknowledgment emails | 3 years |

### Defensibility Elements

**What makes this legally defensible:**

1. **Written policy** - PHI_POLICY.md is the formal policy
2. **Training** - PHI_TRAINING.md proves training was provided
3. **Acknowledgment** - Google Form captures explicit agreement
4. **Timestamp** - Google Forms auto-timestamps all submissions
5. **Version tracking** - Policy version is captured with each acknowledgment
6. **Audit trail** - All responses stored in uneditable Google Sheet
7. **Regular renewal** - Annual re-acknowledgment shows ongoing compliance
8. **Email records** - Distribution emails prove notification

---

## Emergency Procedures

### If an Employee Refuses to Acknowledge

1. Document refusal in writing
2. Restrict access to PHI systems
3. Escalate to CEO
4. If refusal continues: employment action per HR policy

### If Acknowledgment is Discovered Missing

1. Immediately send training + acknowledgment form
2. Document gap discovery date
3. Restrict PHI access until complete (if practical)
4. Note incident in compliance log

---

## Quick Reference

| Event | Action | Owner | Deadline |
|-------|--------|-------|----------|
| New hire | Send training + form | HR/Manager | Day 1 |
| New hire completion | Verify acknowledgment | COO | Day 4 |
| Annual renewal | Send re-acknowledgment | CEO/COO | Jan 1 |
| Annual completion | Verify all complete | COO | Jan 31 |
| Policy update | Send re-acknowledgment | CEO | Within 7 days |
| Quarterly review | Audit acknowledgment sheet | COO | Quarterly |

---

## Google Form Setup Instructions

### Create the Form

1. Go to [forms.google.com](https://forms.google.com)
2. Create new form: "RPI PHI Training Acknowledgment"
3. Add questions per the fields above
4. Settings:
   - Collect email addresses: ON
   - Limit to 1 response: ON
   - Respondents can edit: OFF
5. Link responses to new Google Sheet
6. Share form link (anyone with link can respond)

### Create the Response Sheet

1. In form settings, click "Responses" tab
2. Click Google Sheets icon to create linked sheet
3. Move sheet to: `RPI Compliance > PHI Training > Acknowledgments`
4. Add manual columns: Employment Status, Notes
5. Protect sheet (restrict editing to admins only)

---

*This system creates a defensible record that RPI provided training, employees acknowledged understanding, and compliance is maintained on an ongoing basis.*
