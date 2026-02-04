---
name: warn-missing-structured-response
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.gs$
  - field: content
    operator: regex_match
    pattern: function\s+\w+\s*\([^)]*\)\s*\{[\s\S]*return\s+(?!.*success\s*:)
---

**WARNING: Function May Be Missing Structured Response**

This function has a return statement but doesn't appear to follow the structured response pattern.

**RPI Standard:**
All functions should return `{ success: true/false, data/error }`:

```javascript
// WRONG
function doSomething() {
  const result = processData();
  return result;  // What if it fails?
}

// CORRECT
function doSomething() {
  try {
    const result = processData();
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

**When to ignore this warning:**
- Simple getter functions (getConfig, etc.)
- Functions that intentionally return raw values
- Test functions

See: `~/.claude/CLAUDE.md` → Code Standards → Required Patterns
