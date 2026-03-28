---
name: quality-gate-agent-launch
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (invoke|client|agent).*\.ts$
  - field: content
    operator: regex_match
    pattern: (maxTurns\s*:\s*\d+|maxBudgetUsd\s*:\s*\d|permissionMode\s*:\s*['"]acceptEdits['"])
---

**BLOCKED: CCSDK Agent Lobotomy Detected**

You are writing a CCSDK agent config that artificially limits the agent's capability.

**What's blocked and why:**

- `maxTurns: <number>` — Hard caps the agent's reasoning depth. Agents that hit the limit mid-task silently stop. Remove it; the SDK default is appropriate.
- `maxBudgetUsd: <number>` — Budget caps cause abrupt agent termination with no recovery path. Use cost controls at the API key / org level instead.
- `permissionMode: 'acceptEdits'` — Wrong mode for autonomous agents. Use `'bypassPermissions'` for RONIN/MDJ agents that need to act without interruption.

**The rule:** CCSDK agents must be able to run to completion. Artificial limits produce half-finished work and silent failures — the worst possible outcome.

**Fix:** Remove the offending field, or see `CCSDK_AGENT_PREFLIGHT.md` for the correct agent launch config.
