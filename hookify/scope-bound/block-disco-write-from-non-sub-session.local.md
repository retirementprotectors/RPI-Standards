---
name: block-disco-write-from-non-sub-session
event: pre-write, pre-edit
check: check_disco_write.sh
severity: BLOCK
scope: SCOPE-005-1-L
introduced: 2026-05-13
owner: shinob1
---

# block-disco-write-from-non-sub-session

Blocks `Write` / `Edit` tool calls targeting `docs/discoveries/*.html` when the current tmux session is NOT a properly-spawned `<parent>-disco-sub-<scope>` sub-CXO session.

## Why

SCOPE-005 (PR #1154) shipped `block-parent-cxo-disco-without-spawn` listening for `pre-slack-post` events. That rule scans Slack post content for disco-claim regexes — but only when a Slack post is about to fire. A parent CXO can entirely bypass the gate by writing the disco HTML directly via `Write` / `Edit` tool calls, then posting only the merge-receipt to Slack (which doesn't match the disco-claim regex).

This rule closes Gap D from the SCOPE-005.1 v1.1 disco: every `Write` / `Edit` to `docs/discoveries/*.html` must originate from a sub-CXO session whose name matches `^(\w+)-disco-sub-(\S+)$`.

## Effect

When the rule fires and blocks:
- The Write/Edit tool call is rejected before it executes
- The blocking message tells the user to run `scripts/spawn-subcxo-disco.sh --parent <warrior> --scope-id <id> --brief <path>` first
- A violation is logged to `~/.claude/hooks/violation-log.jsonl`

## Allow path

If the current tmux session matches `^(\w+)-disco-sub-(\S+)$`, the Write/Edit is allowed. The sub-CXO IS authorized to write inside `docs/discoveries/`.

## Belt + suspenders

Companion rule: `block-parent-cxo-disco-without-spawn` covers the `pre-slack-post` event for parent-session disco-claim drumming. Together, the two rules make the parent-CXO bypass class structurally impossible.

## Scope

`SCOPE-005-1-L` — ZRD-SCOPE-005-1 v1.1
