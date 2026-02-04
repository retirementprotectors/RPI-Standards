---
name: block-alert-confirm-prompt
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(gs|html)$
  - field: content
    operator: regex_match
    pattern: (alert|confirm|prompt)\s*\(
---

**BLOCKED: Forbidden UI Pattern Detected**

You are trying to use `alert()`, `confirm()`, or `prompt()` in a GAS file.

**Why this is blocked:**
- These patterns are forbidden in ALL RPI projects
- They don't work reliably in Google Apps Script web apps
- They create poor user experience

**Use instead:**
- `showToast('Message', 'success')` for notifications
- `await showConfirmation({...})` for confirmations
- Custom modal dialogs for input

See: `~/.claude/CLAUDE.md` → Code Standards → Forbidden Patterns
