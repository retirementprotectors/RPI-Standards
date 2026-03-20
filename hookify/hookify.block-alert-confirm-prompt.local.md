---
name: block-alert-confirm-prompt
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (alert|confirm|prompt)\s*\(
---

**BLOCKED: Browser Dialog API Detected**

Do not use browser dialog APIs. They block the UI thread and provide no branding control.

**Instead use:**
- `showToast('Message', 'success')` for notifications
- `await showConfirmation({...})` for confirmations
- Custom modal components for complex inputs
