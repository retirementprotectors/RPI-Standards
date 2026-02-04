---
name: block-hardcoded-colors
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(gs|html)$
  - field: content
    operator: regex_match
    pattern: (#[0-9a-fA-F]{3,6}|rgb\s*\(|rgba\s*\()(?!.*var\s*\(--)
---

**BLOCKED: Hardcoded Color Value Detected**

You are using a hardcoded color (hex code or rgb) instead of CSS variables.

**Why this is blocked:**
- Hardcoded colors make theming impossible
- Creates inconsistent UI across the platform
- Makes maintenance a nightmare

**Fix:**
```javascript
// WRONG
element.style.backgroundColor = '#3b82f6';
element.style.color = 'rgb(255, 0, 0)';

// CORRECT
element.classList.add('bg-primary');
element.classList.add('text-danger');
```

```css
/* Use CSS variables */
.my-element {
  background-color: var(--color-primary);
  color: var(--color-danger);
}
```

See: `~/.claude/CLAUDE.md` → Code Standards → Forbidden Patterns
