---
name: block-hardcoded-colors
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (style\s*=\s*['"][^'"]*(?:color|background|border-color)\s*:\s*#[0-9a-fA-F]{3,8})
  - field: file_path
    operator: regex_match
    pattern: \.(tsx|jsx|ts|js|html)$
---

**BLOCKED: Hardcoded Color Detected**

Do not use inline style colors. Use CSS variables or Tailwind classes for portal theming.

**Instead use:**
- `var(--portal)` for portal accent color
- `var(--text-primary)`, `var(--text-muted)`, etc. for text
- `var(--bg-card)`, `var(--bg-surface)` for backgrounds
- Tailwind classes: `text-[var(--portal)]`, `bg-[var(--bg-card)]`
