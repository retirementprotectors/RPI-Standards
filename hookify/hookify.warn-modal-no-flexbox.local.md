---
name: warn-modal-no-flexbox
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: \.modal-content
  - field: file_path
    operator: regex_match
    pattern: \.(html|css)$
---

**WARNING: Modal Without Flexbox**

Modal content should use `display: flex; flex-direction: column` with scrollable body and fixed header/footer. Without this, buttons may scroll out of view.
