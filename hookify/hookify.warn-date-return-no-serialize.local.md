---
name: warn-date-return-no-serialize
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: return\s+.*new\s+Date\s*\(
  - field: file_path
    operator: regex_match
    pattern: \.gs$
---

**WARNING: Returning Date Object**

Date objects may become NULL when passed from GAS server to client. Wrap with `JSON.parse(JSON.stringify())` in ForUI functions.
