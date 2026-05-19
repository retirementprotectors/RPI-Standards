---
name: warn-backup-file-outside-archive
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(backup|bak)([.0-9\-]|$)
owner: shinob1
---

**WARNING: Backup file creation detected outside `exports/archive/`**

You're about to create a `.backup` or `.bak` file. These tend to accumulate
in `$HOME` and `~/.claude/` and become stale clutter — confirmed in the
2026-05-11 hot-mess sweep (3 stale CLAUDE.md backups + 2 stale .mcp.json
backups deleted).

**The canonical home for snapshots is:**
```
~/.claude/exports/archive/<YYYY-MM-DD>/<descriptive-name>
```

Example: `~/.claude/exports/archive/2026-05-11/claude-md-pre-trim.md`

The weekly cleanup wires (`claude-state-trim.timer`, planned for ZRD-SYS-SYNERGY-PROACTIVE)
spare the `archive/` subdir but prune stale backups elsewhere.

**If this IS the right place:** ignore this warning. Hookify warns, doesn't
block — proceed if you have a reason.
