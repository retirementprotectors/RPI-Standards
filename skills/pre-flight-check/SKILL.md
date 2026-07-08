---
name: pre-flight-check
description: Mandatory before new sprint/build work — run the cto_pre_flight_check MCP tool against the CTO Registry + last 60 shipped commits + top 30 in-flight branches before writing a line of code, to catch duplicate/colliding build work before it starts.
version: 0.1.0-draft
---

# Pre-Flight Check

You have been invoked as the Pre-Flight Check skill — you appear to be starting NEW work (*build / implement / create / spawn / sprint launch*).

## Before you write a single line of code: RUN THE PRE-FLIGHT CHECK

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

## Outcomes

- **PROCEED** — no strong matches. Net-new build appears safe. Continue.
- **REFINE** — partial matches found. Re-scope to be additive (extend the existing capability or compose into a new super-tool/wire) OR coordinate with peers on in-flight branches.
- **ABORT** — strong match against existing capability. You are likely duplicating shipped work. Review the top match before building.

## Why This Skill Exists

On 2026-05-17 the structures audit surfaced that every warrior in the Dojo had rebuilt work that already existed — wasted sprints, duplicate registries, redundant tools. Agents work confidently from what they remember, miss what's already there, and rebuild what didn't need rebuilding. The Pre-Flight Check is the immune layer that catches this *before* a sprint starts — same way `block-hardcoded-secrets` catches secrets before they ship.

## When PROCEED is the right answer

Genuinely net-new work returns PROCEED quickly. Example: *"add interactive penguin choreography to the homepage"* — no matches in registry/commits/branches → PROCEED. Don't skip the check just because you "know" the work is new — verify via the tool, every time. The cost of running it is seconds; the cost of duplicate work is a sprint.

## Bypass

There is no bypass. If the check over-fires on a non-sprint context, run it anyway — net-new scope → PROCEED → continue. The cost is seconds.

---

*SHINOB1, CTO · pre-flight-check · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-pre-flight-check` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
