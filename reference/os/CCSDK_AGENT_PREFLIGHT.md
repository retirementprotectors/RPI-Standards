# CCSDK Agent Preflight Checklist

## Purpose

Every CCSDK agent (VOLTRON, RONIN, RAIDEN, 2HINOBI, MUSASHI, etc.) must pass this checklist before launch. RONIN Sprint 001 went live with `maxTurns: 10`, a `$3` budget cap, `acceptEdits` permission mode, no CLAUDE.md context, and no retry logic — and shipped 10 bugs directly attributable to those missing defaults. This checklist exists so that never happens again. An agent that launches wrong does more damage than no agent at all.

---

## Mandatory Defaults (Non-Negotiable)

| Setting | Required Value | What Happens If Wrong |
|---|---|---|
| `permissionMode` | `'bypassPermissions'` — hardcoded at agent definition, never per-call | Agent pauses mid-task waiting for human approval; FORGE phases stall or fail silently |
| `maxTurns` | Not set (no limit) | Agent cuts off mid-task; partial work shipped as complete; FORGE audit checkpoints never reached |
| `maxBudgetUsd` | Not set (no cap) | Agent abandons complex tasks at arbitrary cost threshold; incomplete features deployed |
| Timeout | Not set at agent level — individual phases set their own only if truly required | Legitimate long-running builds (npm install, type-check) killed; false failures reported |
| Auto-retry on transient errors | 3-attempt exponential backoff: 10s → 30s → 60s for 500 / overload / ECONNRESET | Single flaky API call terminates the entire sprint; agent reports failure on recoverable error |
| CLAUDE.md context | Global (`~/.claude/CLAUDE.md`) + project CLAUDE.md injected into system prompt or read at invoke time | Agent ignores RPI standards, generates alert(), hardcodes colors, skips structured responses |
| FORGE_STANDARDS.md | Loaded for any agent participating in FORGE lifecycle | Agent skips audit checkpoints, ships without evidence, misses phase transition format |
| Hookify rules present | `.claude/hookify.*.local.md` symlinks verified on MDJ_SERVER before launch | Tier 1 block rules inactive; PHI leaks, hardcoded secrets, and generated logos can ship |
| Full tool access | All configured MCP tools available — no artificial filtering | Agent cannot call Firestore, Slack, Drive, or workspace tools needed to complete tasks |
| Discovery doc spec | `intent-create-disco-doc.local.md` content injected into discovery prompts | Discovery docs generated without required sections; downstream FORGE phases fail intake |

---

## Verification Script

Run this against any agent's invoke file before launch:

```bash
INVOKE_FILE="$1"

echo "=== CCSDK Agent Preflight ==="

grep -q "bypassPermissions" "$INVOKE_FILE" \
  && echo "✓ permissionMode: bypassPermissions" \
  || echo "✗ FAIL: permissionMode not set to bypassPermissions"

grep -q "maxTurns" "$INVOKE_FILE" \
  && echo "✗ FAIL: maxTurns is set — remove it" \
  || echo "✓ maxTurns: not set (good)"

grep -q "maxBudgetUsd" "$INVOKE_FILE" \
  && echo "✗ FAIL: maxBudgetUsd is set — remove it" \
  || echo "✓ maxBudgetUsd: not set (good)"

grep -q "acceptEdits" "$INVOKE_FILE" \
  && echo "✗ FAIL: permissionMode is acceptEdits — must be bypassPermissions" \
  || echo "✓ permissionMode: not acceptEdits"

grep -q "CLAUDE.md" "$INVOKE_FILE" \
  && echo "✓ CLAUDE.md context referenced" \
  || echo "✗ WARN: CLAUDE.md context not explicitly referenced"

grep -q "retry" "$INVOKE_FILE" \
  && echo "✓ Retry logic present" \
  || echo "✗ WARN: No retry logic detected — add 3-attempt backoff"

echo "=== Preflight complete ==="
```

Usage: `bash ccsdk_preflight.sh path/to/agent-invoke.js`

---

## Hookify Enforcement

A hookify rule `quality-gate-agent-launch` should be added to `_RPI_STANDARDS/hookify/` to block any `claudeInvoke()` or `query()` call that sets `maxTurns`, `maxBudgetUsd`, or `permissionMode: 'acceptEdits'`. The rule does not exist yet — it needs to be created and symlinked across all active projects. Until it exists, this checklist is the enforcement mechanism.

---

## History

- **2026-03-27**: Created after RONIN Sprint 001 launched with 10 bugs due to missing defaults (`maxTurns: 10`, `maxBudgetUsd: 3`, `permissionMode: 'acceptEdits'`, no CLAUDE.md, no retry logic).
