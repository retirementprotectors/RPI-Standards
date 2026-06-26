---
name: block-canonical-doctrine-write-outside-ssot
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: /(ORCHESTRATION|MEMORY_DISCIPLINE|TAXONOMY|RESPONSIBILITIES|TEAM_PROTOCOL|_INDEX)\.md$
  - field: file_path
    operator: not_contains
    pattern: docs/warriors/
owner: shinob1
---

🛑 **BLOCKED: Canonical doctrine file written outside SSOT path**

Files named `ORCHESTRATION.md`, `MEMORY_DISCIPLINE.md`, `TAXONOMY.md`, `RESPONSIBILITIES.md`, `TEAM_PROTOCOL.md`, or `_INDEX.md` are part of the **canonical doctrine SSOT** per `docs/warriors/shinob1/_INDEX.md`. They MUST live under `toMachina/docs/warriors/<warrior-name>/`.

**Canonical path:**
```
toMachina/docs/warriors/<warrior-name>/<filename>
```

Per the SSOT registry at `dojo-warriors/mdj-agent/.../dojo-state.json` `canonical_doctrine_docs` array, these are the 7 files that ARE the warrior's authoritative doctrine. Scattering them across worktrees or project directories breaks the SSOT and creates ambiguity about which is canonical.

**Why this rule exists (the 2026-05-30 failure):**
Parent SHINOB1 rebuilt `dojo-warriors/warriors/<name>/WORKFLOW.md` files at 145-206 lines without consulting the canonical 75-line `toMachina/docs/warriors/<name>/WORKFLOW.md` SSOT. The rebuild duplicated + drifted from the canonical doctrine. The Alt B consolidation (2026-05-18) explicitly named these 7 as the canonical set; nothing else should carry their filenames.

**Override (rare):**
- If this isn't actually canonical doctrine (e.g., you have an unrelated `_INDEX.md` for navigation in another doc tree), rename it. The block fires on the literal filename — a different name passes.
- The canonical-7 names are reserved for the SHINOB1 doctrine cluster only.

**Note on WORKFLOW.md:** `WORKFLOW.md` is handled separately. It has TWO valid locations:
- `toMachina/docs/warriors/<name>/WORKFLOW.md` (canonical SSOT doctrine, "Session start — always")
- `dojo-warriors/warriors/<name>/WORKFLOW.md` (FORGE 2.0 Symphony runtime config, schema v1.0 frontmatter only — should be ≤80 lines, point at canonical for doctrine)

**Why BLOCK, not WARN:** doctrine drift is the most expensive bug class. A future session that reads a stale/conflicting canonical doc inherits drift. One canonical location = one source of truth. Per `RESPONSIBILITIES.md` A2 (doctrine authorship + refinement), revisions to these 6 names go through SHINOB1 audit; new locations don't.

**Cross-reference:**
- `block-warrior-doctrine-write-outside-warriors-cluster` — sister rule for `soul.md` / `spirit.md` / `brain.txt` (identity layer, lives in `dojo-warriors/warriors/`)
- `docs/warriors/shinob1/_INDEX.md` — the SSOT navigation map (load-context tags per doc)
