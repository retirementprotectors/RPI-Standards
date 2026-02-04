---
name: block-phi-in-logs
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (console\.log|Logger\.log|console\.error|console\.warn).*(\bssn\b|\bSSN\b|social_security|socialSecurity|\bdob\b|\bDOB\b|date_of_birth|dateOfBirth|medicare_id|medicareId|beneficiary_id)
---

**BLOCKED: PHI Detected in Log Statement**

You are logging Protected Health Information (PHI) which is a compliance violation.

**What was detected:**
- SSN, DOB, Medicare ID, or similar PHI field in a log statement

**Why this is blocked:**
- HIPAA violation - PHI must never be logged
- Audit logs may expose client data
- This creates legal liability for RPI

**Fix:**
- Remove the PHI field from the log statement
- If debugging, use masked values: `SSN: ***-**-${ssn.slice(-4)}`
- Log record IDs instead of PHI

See: `~/.claude/CLAUDE.md` → PHI Handling Rules
