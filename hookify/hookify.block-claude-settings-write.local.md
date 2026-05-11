---
name: block-claude-settings-write
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.claude/settings(\.local)?\.json$
---

**BLOCKED: Direct write to `~/.claude/settings.json` (or `settings.local.json`)**

`~/.claude/settings.json` is the Claude Code harness configuration. Direct
edits by warriors have caused: hooks misregistered, MCP servers ghost-listed,
auto-merge disabled, plugins silently dropped.

**Use the proper paths:**

| Change you want to make | Right way |
|---|---|
| Add/remove an MCP server | `claude mcp add <name>` / `claude mcp remove <name>` (per CLAUDE.md doctrine) |
| Add/remove a plugin | `/plugin` slash command in Claude Code |
| Configure hooks | Use the hookify plugin: write rules in `_RPI_STANDARDS/hookify/`, run `setup-hookify-symlinks.sh` |
| Change theme/model | `/config` slash command |
| Add a permission | Use the `update-config` skill, OR direct PR review by SHINOB1 |
| Custom hook scripts (PreToolUse / PostToolUse / SessionStart) | Drop a script in `~/.claude/hooks/`, then JDM/SHINOB1 reviews + adds the registration |

**If you have a JDM directive to edit settings.json directly:** invoke this rule's bypass by including in the prompt:
> "JDM directive 2026-XX-XX: editing ~/.claude/settings.json to <reason>. Reviewed by SHINOB1."

The rule will still fire but the message documents the intent for the audit log.

Why this exists: ZRD-SHINOB1-AUDIT-POSTURE-001 + 2026-05-11 hot-mess sweep.
