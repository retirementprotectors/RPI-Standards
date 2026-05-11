---
name: block-mcp-config-write
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^/home/jdm/\.mcp\.json$
---

**BLOCKED: Direct write to `~/.mcp.json`**

Per CLAUDE.md doctrine (line 565):
> *"MCPs are configured via CLI, NOT settings.json"*

The same rule applies to `~/.mcp.json`. Direct file edits cause:
- MCP servers in stale list but not registered with the harness
- OAuth scope drift between actual auth and what `~/.mcp.json` claims
- Backup files (`.mcp.json.backup-XXXXX`) accumulating in HOME (verified
  in 2026-05-11 sweep — 2 stale backups deleted)

**Use the CLI instead:**

```bash
# Add MCP globally (available in all projects)
claude mcp add <name> -e 'KEY=value' --scope user -- <command>

# Add MCP to current project only
claude mcp add <name> -e 'KEY=value' -- <command>

# List configured MCPs
claude mcp list

# Remove an MCP
claude mcp remove <name> --scope user
```

After adding/removing MCPs: restart Claude Code for changes to take effect.

**If you have a JDM directive to edit `.mcp.json` directly:** include the
bypass acknowledgment in the prompt:
> "JDM directive 2026-XX-XX: direct edit of ~/.mcp.json approved because <reason that the CLI cannot accomplish>."

Why this exists: ZRD-SHINOB1-AUDIT-POSTURE-001 + 2026-05-11 hot-mess sweep.
