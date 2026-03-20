---
name: block-let-module-caching
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (let|const)\s+_\w*(cache|Cache|data|Data|config|Config)\w*\s*=
  - field: file_path
    operator: regex_match
    pattern: \.gs$
---

**BLOCKED: let/const for Module Cache Variable**

In GAS, `let` and `const` do not persist between function calls. Use `var` for module-level cache variables.
