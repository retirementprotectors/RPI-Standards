---
name: block-opus-subagent
enabled: true
event: file
action: block
conditions:
  # Scope to CODE files only — Agent() is a tool call in .ts/.js/.py, never in prose.
  # Without this, the content pattern matched the substring "agent (" case-insensitively,
  # so a doc/brief mentioning the "mdj-agent (the ...)" SERVICE NAME got falsely blocked,
  # and the rule even blocked edits to its own .md (which contains Agent() examples).
  # A6 precision fix (false-positive minimization). SHINOB1 2026-06-26.
  - field: file_path
    operator: regex_match
    pattern: \.(ts|tsx|js|jsx|mjs|cjs|py)$
  - field: content
    operator: regex_match
    pattern: Agent\s*\([^)]*(?:model\s*[:=]\s*['"]opus['"]|(?!model\s*[:=]))
owner: shinob1
---

🛑 **BLOCKED: Sub-Agent using Opus or missing `model=` parameter**

All `Agent()` calls MUST specify `model=` and should use the cheapest model that fits the task. JDM's org burns ~$250/day, 98% on Opus — most sub-agent work runs fine on Sonnet.

**Model Routing Table:**

| Task | Model | Cost/1M tokens (in/out) |
|---|---|---|
| Planning / architecture | `opus` | $15 / $75 |
| Code execution / research / builds | `sonnet` | $3 / $15 |
| Simple lookups / validation | `haiku` | $0.80 / $4 |

**Canonical:**
```python
❌ Agent(prompt="write the feature")              # blocked — no model=
❌ Agent(model="opus", prompt="find this file")   # blocked — Opus on lookup work

✅ Agent(model="sonnet", prompt="write the feature")
✅ Agent(model="haiku",  prompt="find this file")
✅ Agent(model="opus",   prompt="architect the migration plan")
```

**Override (when Opus IS justified — multi-project architectural reasoning):**
- The only legitimate Opus use for a sub-agent is genuine planning / architecture / multi-project reasoning. If that's what's happening, the Opus call IS correct — just include `model="opus"` explicitly so the rule's pattern matches AND a comment justifying it: `# opus-justified: <reason>` on the same line or immediately above.

**Why BLOCK, not WARN:** the WARN was invisible. Smart model routing saves ~$4,000/month. BLOCK forces explicit model choice every time.
