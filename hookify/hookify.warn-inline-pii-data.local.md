---
name: warn-inline-pii-data
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: var\s+\w+\s*=\s*\{\s*'[^']+'\s*:\s*\{[^}]*(dob|ssn|social_security|medicare_id|phone|email|address|date_of_birth)[^}]*\}
---

**WARNING: Inline PII Data Detected**

You are embedding what appears to be personal data (names, DOB, SSN, phone, email, address) directly in source code.

**What was detected:**
- A `var` declaration containing an object literal with PII field names

**Why this is a concern:**
- PII in source code gets committed to git history permanently
- Even if removed later, git history retains it
- Violates data minimization principle

**Better approach:**
- Store bulk data as CSV/JSON in Google Drive (not in git)
- Use `bobLoadJsonFromDrive_(fileId)` to load at runtime
- Or use MATRIX sheet data directly via `bobReadSheet_(tabName)`

**If this is intentional (one-time FIX_ function):**
- Run it immediately, then archive the inline data to Drive
- Replace with Drive loader before committing

See: `RAPID_IMPORT/CLAUDE.md` BoB Import/Enrichment Workflow
