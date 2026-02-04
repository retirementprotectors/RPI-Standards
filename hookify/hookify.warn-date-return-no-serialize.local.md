---
name: warn-date-return-no-serialize
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.gs$
  - field: content
    operator: regex_match
    pattern: return\s+.*new\s+Date\s*\(
---

**WARNING: Returning Date Object Without Serialization**

You are returning a `new Date()` object which may become NULL on the client.

**Why this matters:**
- GAS doesn't serialize Date objects properly when passed to client
- Date fields silently become null
- This has caused many "where's my date?" bugs

**If this is a ForUI function, fix it:**
```javascript
// WRONG
function getDataForUI() {
  return { created: new Date(), name: 'Test' };
}

// CORRECT
function getDataForUI() {
  const data = { created: new Date(), name: 'Test' };
  return JSON.parse(JSON.stringify(data));  // Dates become ISO strings
}
```

**If this is server-side only, you can ignore this warning.**

See: `~/.claude/CLAUDE.md` → GAS Gotchas → #1
