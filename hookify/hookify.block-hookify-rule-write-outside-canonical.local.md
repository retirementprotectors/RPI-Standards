---
name: block-hookify-rule-write-outside-canonical
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: hookify\.[^/]+\.local\.md$
  - field: file_path
    operator: not_contains
    pattern: _RPI_STANDARDS/hookify/
---

🛑 **BLOCKED: hookify rule write outside canonical location**

All hookify rules MUST live under `_RPI_STANDARDS/hookify/`. They're symlinked to `~/.claude/` (global) and `<project>/.claude/` (per-project) by `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh`. Editing the symlink directly creates source-of-truth drift.

**Canonical path:**
```
/home/jdm/Projects/_RPI_STANDARDS/hookify/hookify.<name>.local.md
```

**After editing/creating the rule:**
```bash
/home/jdm/Projects/_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh
```
to refresh the symlinks across all consumers.

**Override (rare — repointing a stale symlink):** the block reads the file_path STRING, not the symlink target. Always pass the canonical path to Write/Edit — that bypasses the regex cleanly.

**Why BLOCK, not WARN:** symlink-source drift has been a recurring bug class (hookify stale plugin hash · symlink-vs-canonical confusion across 2026-04-27 and 2026-05-11 sessions). The fix is one rule that enforces canonical-path-or-nothing at moment of action.
