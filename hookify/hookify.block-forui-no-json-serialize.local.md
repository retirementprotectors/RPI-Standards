---
name: block-forui-no-json-serialize
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.gs$
  - field: content
    operator: regex_match
    pattern: function\s+\w+ForUI\s*\([^)]*\)\s*\{(?![\s\S]*JSON\.parse\s*\(\s*JSON\.stringify)
---

**BLOCKED: ForUI Function Missing JSON Serialization**

You are creating/editing a `*ForUI()` function without `JSON.parse(JSON.stringify())`.

**Why this is blocked:**
- GAS doesn't properly serialize complex objects to the client
- Date objects become NULL
- Nested objects may disappear entirely
- This has caused countless "data is null" bugs

**Fix:**
```javascript
// WRONG
function getDataForUI() {
  const result = MyModule.getData();
  return result;  // Data may be null/incomplete on client!
}

// CORRECT
function getDataForUI() {
  const result = MyModule.getData();
  return JSON.parse(JSON.stringify(result));  // Clean serialization
}
```

See: `~/.claude/CLAUDE.md` → GAS Gotchas → #1 and #2
