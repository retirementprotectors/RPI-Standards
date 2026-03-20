---
name: warn-missing-structured-response
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: function\s+\w+\s*\([^)]*\)\s*\{[\s\S]*?return\s+(?!.*success)
  - field: file_path
    operator: regex_match
    pattern: \.(gs|ts|js)$
---

**WARNING: Missing Structured Response**

Functions should return `{ success: true/false, data/error }` pattern for consistent error handling.
