---
name: block-alert-confirm-prompt
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (alert|confirm|prompt)\s*\(
  # Doctrine-file exemption (SHINOB1-CLAUDEMD-MIGRATE-001 follow-on): canonical doctrine
  # files necessarily QUOTE forbidden patterns as examples — exempt them, like reverse-callout.
  - field: file_path
    operator: not_contains
    pattern: warriors/shared
  - field: file_path
    operator: not_contains
    pattern: hookify
  - field: file_path
    operator: not_contains
    pattern: CLAUDE.md
owner: shinob1
---

**BLOCKED: Browser Dialog API Detected**

Do not use browser dialog APIs. They block the UI thread and provide no branding control.

**Instead use:**
- `showToast('Message', 'success')` for notifications
- `await showConfirmation({...})` for confirmations
- Custom modal components for complex inputs
