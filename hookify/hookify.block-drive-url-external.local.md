---
name: block-drive-url-external
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (UrlFetchApp\.fetch|fetch\s*\(|axios).*drive\.google\.com
---

**BLOCKED: Drive URL in External Fetch**

Do not pass Google Drive URLs to external services. Fetch with authenticated Google API, send as base64 if needed.
