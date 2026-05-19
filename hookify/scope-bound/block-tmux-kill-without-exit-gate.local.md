---
name: block-tmux-kill-without-exit-gate
category: scope-bound
event: pre-tmux-kill
check: check_pre_tmux_kill.sh
owner: ronin
---
# Hookify Rule: block-tmux-kill-without-exit-gate
# Category: scope-bound
# TRK-14758 · ZRD-SCOPE-005-001 ENF-008 | _RPI_STANDARDS/hookify/scope-bound/
event: pre-tmux-kill
check: check_pre_tmux_kill.sh

## Rule Identity
- **Rule ID**: block-tmux-kill-without-exit-gate
- **Category**: scope-bound
- **Severity**: BLOCK (pre-tmux kill-session hook)
- **Author**: RONIN
- **Ticket**: TRK-14758 / ENF-008 (activation)
- **Event**: `pre-tmux-kill` — fires on Bash `tmux kill-session` invocations

## Trigger
Fires on **pre-`tmux kill-session`** when the session name matches:
```
<parent>-disco-sub-<scope-id>
```
Pattern: `^(musashi|megazord|voltron|taiko|shinob1)-disco-sub-.+$`

## Condition
The kill is BLOCKED when either condition is false:
- `ForgeRunState.exit_gate.disco_pr_merged === false` (PR not yet merged)
- `ForgeRunState.exit_gate.parent_ack === false` (parent has not ACKed)

Both MUST be `true` for the kill to proceed.

## Block Message
When triggered, the hook blocks with this message:
```
BLOCKED: tmux kill-session requires exit gate to be fully open.

Current gate state for <session-name>:
  disco_pr_merged: <true|false>
  parent_ack:      <true|false>

To open the gate:
  1. PR must be merged to main (GitHub webhook auto-flips disco_pr_merged)
  2. Parent CXO must ✅-react to your completion post in bilateral channel
     (Slack react listener auto-flips parent_ack)

Do NOT kill this session until both are true.
ZRD-SCOPE-SCOPE-001 Death-Gate Protocol.
```

## Exit Gate State Machine

### How disco_pr_merged flips to true
GitHub PR-merge webhook POSTs to `/api/forge/exit-gate`:
```typescript
// POST /api/forge/exit-gate
// Body: { session_name: string, event: 'pr_merged', pr_number: number }
// Handler sets ForgeRunState.exit_gate.disco_pr_merged = true
```

### How parent_ack flips to true
Slack bilateral ✅-react listener fires when parent CXO reacts to the
sub-warrior's completion post with ✅:
```typescript
// Slack event: reaction_added { reaction: 'white_check_mark', ... }
// Handler sets ForgeRunState.exit_gate.parent_ack = true
//              ForgeRunState.exit_gate.ack_ts = new Date().toISOString()
//              ForgeRunState.completion_ts = new Date().toISOString()
```

### isExitGateOpen() helper
Available in `services/api/src/forge/phases.ts` (TRK-14754):
```typescript
import { isExitGateOpen } from './phases.js'
// Returns true only when both flags are true
const canKill = isExitGateOpen(runState)
```

## Implementation Notes
The pre-tmux-kill hook implementation queries ForgeRunState by session name
(derived from `parent_cxo` + `scope_id` fields) before allowing the kill.

Pseudo-implementation:
```bash
# In pre-kill hook handler:
SESSION_NAME="$1"
# e.g. SESSION_NAME="musashi-disco-sub-cmo-001"

# Query ForgeRunState
STATE=$(curl -sf "${API_BASE}/api/forge/run-state?session=${SESSION_NAME}")
PR_MERGED=$(echo "${STATE}" | jq -r '.exit_gate.disco_pr_merged')
PARENT_ACK=$(echo "${STATE}" | jq -r '.exit_gate.parent_ack')

if [[ "${PR_MERGED}" != "true" || "${PARENT_ACK}" != "true" ]]; then
  echo "BLOCKED: Exit gate not open. pr_merged=${PR_MERGED}, parent_ack=${PARENT_ACK}"
  exit 1
fi
# else: allow kill
```

## Rollback
Same as TRK-14757: rename `_RPI_STANDARDS/hookify/scope-bound/` to disable.

## Related
- TRK-14754: ForgeRunState.exit_gate schema + isExitGateOpen() helper
- TRK-14757: block-parent-cxo-disco-without-spawn (paired enforcement rule)
- ZRD-SCOPE-SCOPE-001 Decision Q4: "Both PR-merge + parent ACK required"
