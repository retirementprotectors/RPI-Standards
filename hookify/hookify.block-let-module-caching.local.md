---
name: block-let-module-caching
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.gs$
  - field: content
    operator: regex_match
    pattern: (let|const)\s+_\w*(cache|Cache|data|Data|config|Config)\w*\s*=
---

**BLOCKED: Invalid Caching Variable Declaration**

You are using `let` or `const` for a module-level caching variable in a GAS file.

**Why this is blocked:**
- `let` and `const` at module level don't persist between function calls in GAS
- Cache variables will reset unexpectedly, causing bugs
- This has caused hours of debugging in RPI projects

**Fix:**
```javascript
// WRONG
let _cachedData = null;
const _configCache = {};

// CORRECT
var _cachedData = null;
var _configCache = {};
```

See: `~/.claude/CLAUDE.md` → GAS Gotchas → #7 Caching Variables Reset
