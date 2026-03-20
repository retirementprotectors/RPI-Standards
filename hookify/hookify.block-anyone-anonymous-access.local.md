---
name: block-anyone-anonymous-access
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: "access"\s*:\s*"(ANYONE_ANONYMOUS|ANYONE)"
  - field: file_path
    operator: regex_match
    pattern: appsscript\.json$
---

**BLOCKED: Public Access Detected**

GAS web apps MUST use organization-only access.
Fix: Set `"access": "DOMAIN"` in appsscript.json.
