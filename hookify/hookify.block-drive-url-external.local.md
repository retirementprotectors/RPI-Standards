---
name: block-drive-url-external
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (UrlFetchApp\.fetch|fetch\s*\(|axios|request).*drive\.google\.com
---

**BLOCKED: Google Drive URL Being Sent to External Service**

You are passing a Google Drive URL to an external service or fetch call.

**Why this is blocked:**
- External services CANNOT access Google Drive URLs
- Drive URLs require Google authentication that external services don't have
- This always fails silently or with auth errors

**Fix:**
Fetch the file with Apps Script and send as base64:
```javascript
// WRONG
const pdfUrl = 'https://drive.google.com/file/d/xxx/view';
UrlFetchApp.fetch(externalService, { body: { url: pdfUrl }});

// CORRECT
function getPdfAsBase64(driveUrl) {
  const fileId = extractFileId(driveUrl);
  const file = DriveApp.getFileById(fileId);
  const blob = file.getBlob();
  return Utilities.base64Encode(blob.getBytes());
}
// Then send the base64 to the external service
```

See: `~/.claude/CLAUDE.md` → GAS Gotchas → #3
