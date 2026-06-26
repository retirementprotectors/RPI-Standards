---
name: intent-pre-flight-check
enabled: true
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: '((build|implement|create)\s+(a\s+)?new\b|spawn\s+a\s+(new\s+)?(warrior|sub|sprint)|(start(ing)?|launch(ing)?|kickoff)\s+(a\s+)?(new\s+)?sprint|/forge[-\s]?sprint|new\s+sprint\b)'
owner: shinob1
---

## Pre-Flight Validator — MANDATORY before new sprint / build work

You appear to be starting NEW work — *build / implement / create / spawn / sprint launch* language detected in your prompt.

### Before you write a single line of code: RUN THE PRE-FLIGHT CHECK

Invoke the `cto_pre_flight_check` MCP tool with a 1–3 sentence description of what you're about to build:

```
mcp__rpi-cto__cto_pre_flight_check({
  "scope": "<brief description of intended work>"
})
```

The tool tokenizes your scope and matches against:
- The CTO Registry (atomic tools + super tools + wires by id + description)
- The last 60 shipped commits in toMachina (for already-merged similar work)
- Top 30 in-flight branches by recency (for parallel-work collisions)

Outcomes:
- **PROCEED** — no strong matches. Net-new build appears safe. Continue.
- **REFINE** — partial matches found. Re-scope to be additive (extend the existing capability or compose into a new super-tool/wire) OR coordinate with peers on in-flight branches.
- **ABORT** — strong match against existing capability. You are likely duplicating shipped work. Review the top match before building.

### Why this rule exists

On 2026-05-17 the structures audit surfaced that *every warrior in the Dojo* — RONIN-V, RONIN-X, VOLTRON, MEGAZORD, and SHINOB1 itself — has rebuilt work that already existed. Wasted sprints. Duplicate registries. Redundant tools. The pattern is consistent: agents work confidently from what they remember, miss what's already there, and rebuild what didn't need rebuilding.

The Pre-Flight Validator is the immune layer that catches this *before* a sprint starts — same way `block-hardcoded-secrets` catches secrets before they ship. Doctrine becomes infrastructure.

### When PROCEED is the right answer

Genuinely net-new work returns PROCEED quickly. Example: *"add interactive penguin choreography to the homepage"* — no matches in registry/commits/branches → PROCEED. Don't skip the check just because you "know" the work is new — verify via the tool, every time. The cost of running it is seconds; the cost of duplicate work is a sprint.

### Cross-reference

- Audit BUILD #4.5, #4.6 — the Registry MCP this rule depends on.
- Audit BUILD-AROUND #2 — working-tree collisions on shared checkouts (this rule also catches that class).
- Audit BUILD-AROUND #4 — doctrine drift; this rule moves doctrine into enforcement at the prompt boundary.

### Auto-invocation (future iteration)

This rule currently *nudges* — surfaces the requirement and the tool name, but the warrior must call the MCP tool manually. A future iteration will add a `check_pre_flight.sh` shell script (sibling to `scope-bound/check_*.sh`) that auto-invokes the MCP tool via JSON-RPC and surfaces the recommendation inline. That requires `enforce.sh` dispatch additions — separate doctrine-level change.

### Bypass

There is no bypass. If the regex over-fires (the prompt mentions "build a new approach" in a non-sprint context), simply run the check anyway — net-new scope → PROCEED → continue. The cost is seconds. Routing around the rule by rephrasing is the exact failure pattern this rule + the audit's hookify-bypass postmortem are guarding against.
