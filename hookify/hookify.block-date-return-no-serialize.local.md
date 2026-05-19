---
name: block-date-return-no-serialize
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: return\s+.*new\s+Date\s*\(
  - field: file_path
    operator: regex_match
    pattern: \.gs$
owner: shinob1
---

🛑 **BLOCKED: Returning a raw Date object from GAS**

Date objects become NULL when passed from GAS server → client. The serialization barrier strips Date prototypes silently — the consumer gets `null` and sees no error. Confirmed bug class with at least three historical incidents (CXO Roadmap launches lost dates, Sprint planning dates dropped silently).

**Canonical pattern — ForUI / `forUI*` / API handler returning a Date:**
```javascript
❌ return new Date(rawDob)                               // blocked

✅ return JSON.parse(JSON.stringify({ dob: new Date(rawDob) }))
✅ return new Date(rawDob).toISOString()                 // string form
✅ return new Date(rawDob).getTime()                     // ms epoch
```

**Override (rare — pure server-side helper, never crosses the boundary):**
- If the function is genuinely internal (called only from other server-side .gs functions, never from `google.script.run`), the raw Date IS safe.
- Add comment on the return line: `// server-only: not cross-boundary`
- Or rename the function so it doesn't pattern-match (avoid `forUI*` / `api*` naming) — pattern fires on the literal `return ...new Date(`.

**Why BLOCK, not WARN:** the WARN was invisible. Silent date drops have shipped to production multiple times. BLOCK forces explicit serialization.
