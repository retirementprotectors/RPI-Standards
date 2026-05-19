---
name: block-modal-no-flexbox
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: \.modal-content
  - field: file_path
    operator: regex_match
    pattern: \.(html|css)$
---

🛑 **BLOCKED: `.modal-content` rule without flexbox layout**

Modal content MUST use `display: flex; flex-direction: column` with a scrollable body and fixed header/footer. Non-flex modals scroll buttons off-screen on tall content — confirmed bug class, multiple incidents.

**Canonical:**
```css
.modal-content {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}
.modal-content .modal-body   { flex: 1 1 auto; overflow-y: auto; }
.modal-content .modal-footer { flex-shrink: 0; }
```

**Override (rare — legacy modal pending migration):**
- Add comment immediately before the `.modal-content` rule: `/* legacy-modal-exempt: <ticket-or-reason> */`
- The block matches the literal substring `.modal-content` — if you genuinely need a different class name (e.g. `.dialog-content` for a non-modal popover), that won't match.

**Why BLOCK, not WARN:** the WARN was invisible in tool output. Non-flex modals have shipped to production at least twice this year. BLOCK forces flex layout or explicit migration acknowledgement.
