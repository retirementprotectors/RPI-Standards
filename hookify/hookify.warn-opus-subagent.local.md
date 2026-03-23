---
name: warn-opus-subagent
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: Agent\s*\([^)]*(?:model\s*[:=]\s*['"]opus['"]|(?!model\s*[:=]))
---

**WARNING: Sub-Agent Using Opus or Missing Model Parameter**

All `Agent()` calls MUST specify `model=` and should use the cheapest model that fits the task.

**Model Routing Table:**
| Task | Model | Cost/1M tokens (in/out) |
|------|-------|------------------------|
| Planning / architecture | `opus` | $15 / $75 |
| Code execution / research / builds | `sonnet` | $3 / $15 |
| Simple lookups / validation | `haiku` | $0.80 / $4 |

**Why this matters:**
- JDM's org burns ~$250/day, 98% on Opus
- Most sub-agent work (code, research, builds) runs fine on Sonnet
- Smart routing saves ~$4,000/month

**Fix:**
```
❌ Agent(prompt="write the feature")
❌ Agent(model="opus", prompt="search for this file")

✅ Agent(model="sonnet", prompt="write the feature")
✅ Agent(model="haiku", prompt="search for this file")
✅ Agent(model="opus", prompt="architect the migration plan")
```

Only use `model="opus"` for planning, architecture, and complex multi-project reasoning.
