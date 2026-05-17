# Hookify Rule: block-parent-cxo-disco-without-spawn
# Category: scope-bound
# TRK-14757 · ZRD-SCOPE-005-001 ENF-007 | _RPI_STANDARDS/hookify/scope-bound/
event: pre-slack-post
check: check_pre_slack_post.sh

## Rule Identity
- **Rule ID**: block-parent-cxo-disco-without-spawn
- **Category**: scope-bound
- **Severity**: BLOCK (pre-Slack-post hook)
- **Author**: SHINOB1
- **Ticket**: TRK-14757 / ENF-007 (activation)
- **Event**: `pre-slack-post` — fires on `mcp__slack__slack_post_message` invocations

## Trigger
Fires on **pre-Slack-post** in parent CXO bilateral channels:
- `#shinob1` (SHINOB1 bilateral)
- `#musashi` (MUSASHI bilateral)
- `#megazord` (MEGAZORD bilateral)
- `#voltron` (VOLTRON bilateral)
- `#taiko` (TAIKO bilateral)

## Condition
A Slack message is BLOCKED when ALL of the following are true:

1. The message is posted to one of the channels above
2. The message body contains any of these scope/disco claim patterns:
   - "disco" or "discovery" (case-insensitive)
   - "scope" + ("writing" | "drafting" | "authoring" | "completing")
   - "ZRD-" followed by a scope identifier
   - "8-tab" or "8 tab"
   - "discovery doc" or "disco doc"
3. No `<parent>-disco-sub-*` session exists in `ForgeRunState` for that parent
   within the last **1 hour** (`spawn_ts >= now - 3600s`)

## Block Message
When triggered, the hook blocks with this message:
```
BLOCKED: scope/disco claim without active sub-warrior spawn.

Parent CXOs cannot write discovery docs in-session.
Exclusive path: spawn a sub-CXO first.

  scripts/spawn-subcxo-disco.sh \
    --parent <PARENT> \
    --scope-id <scope-id> \
    --brief <path/to/brief.md>

Sub-warrior writes the disco. Parent reviews + ACKs. Death-gate closes.
No exceptions. ZRD-SCOPE-SCOPE-001.
```

## Allow Conditions
The post is ALLOWED when:
- An active `disco-sub` entry exists in `ForgeRunState` with `parent_cxo == <this_parent>` and `spawn_ts >= now - 3600s`
- OR the message is the death-gate ACK itself (contains "ACK" + "disco-sub-" + PR URL pattern)
- OR the message is from the sub-warrior session reporting completion (automated)

## Implementation Notes
This rule enforces the exclusive-path constraint from ZRD-SCOPE-SCOPE-001 Decision Q3:
pre-Slack-post hookify block makes bypass impossible (vs. social contract which can be ignored).

ForgeRunState query:
```typescript
// Check for active disco-sub session
const oneHourAgo = Date.now() - 3600_000
const hasActiveSub = forgeRunState.some(entry =>
  entry.task_type === 'disco-sub' &&
  entry.parent_cxo === parentCxo &&
  entry.spawn_ts != null &&
  new Date(entry.spawn_ts).getTime() >= oneHourAgo
)
```

Rollback: rename `_RPI_STANDARDS/hookify/scope-bound/` to `_RPI_STANDARDS/hookify/scope-bound.disabled/`.
FORGE Runner extensions survive rollback; only enforcement wall is disabled.

## Related
- ZRD-SCOPE-SCOPE-001 v1.0 (discovery doc — signed by JDM)
- TRK-14754: ForgeRunState.task_type + spawn_ts fields
- TRK-14758: death-gate enforcement (tmux kill-session block)
- `scripts/spawn-subcxo-disco.sh` (TRK-14756)
