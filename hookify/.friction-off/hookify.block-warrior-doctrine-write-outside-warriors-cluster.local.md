---
name: block-warrior-doctrine-write-outside-warriors-cluster
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: /(soul\.md|spirit\.md|brain\.txt)$
  - field: file_path
    operator: not_contains
    pattern: dojo-warriors/warriors/
owner: shinob1
---

🛑 **BLOCKED: Warrior doctrine file written outside canonical cluster**

Files named `soul.md`, `spirit.md`, or `brain.txt` MUST live under `dojo-warriors/warriors/<warrior-name>/`. These ARE the warrior's identity — scattering them across worktrees or project directories creates ambiguity about which is canonical.

**Canonical path:**
```
/home/jdm/Projects/dojo-warriors/warriors/<warrior-name>/<filename>
```

Where `<warrior-name>` is one of: `shinob1`, `megazord`, `musashi`, `voltron`, `raiden`, `ronin`, `taiko` (or a `<parent>-<variant>` sub-warrior name).

**Override (rare):**

- If this isn't actually a warrior identity file, rename it. The block fires on the literal filename `soul.md` / `spirit.md` / `brain.txt` — a different name won't match.
- If editing through a worktree, the canonical path still works. Worktrees of `dojo-warriors` (e.g. `dojo-warriors-shinob1-coach`) follow the SAME relative structure — the regex matches `dojo-warriors/warriors/` anywhere in the path, so worktree edits pass through fine.

**Why BLOCK, not WARN:** warrior identity drift is the single most expensive bug class for COACH spawns. A sub-warrior reading a stale or out-of-place soul.md inherits the wrong identity. One canonical location = one source of truth.

**Note on `brain.txt`:** the Stop-event hook (`session-end-brain-export.sh`) appends to brain.txt via shell `>>` (Bash event), not Write tool. This rule fires on `event: file` only — so the Stop hook's automatic appends are unaffected.
