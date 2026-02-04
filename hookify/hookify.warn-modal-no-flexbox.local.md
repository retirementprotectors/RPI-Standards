---
name: warn-modal-no-flexbox
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.html$
  - field: content
    operator: contains
    pattern: modal-content
  - field: content
    operator: not_contains
    pattern: display: flex
---

**WARNING: Modal Content Without Flexbox Pattern**

You are editing `.modal-content` but it doesn't include `display: flex`.

**Why this matters:**
- Modal buttons may scroll out of view on long content
- Users won't be able to see/click action buttons
- This has caused many UX complaints

**Recommended pattern:**
```css
.modal-content {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
}
.modal-header, .modal-footer { flex-shrink: 0; }
.modal-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;  /* Required for flex scroll */
}
```

See: `~/.claude/CLAUDE.md` → GAS Gotchas → #6
