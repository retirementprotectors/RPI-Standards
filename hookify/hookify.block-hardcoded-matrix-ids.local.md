---
name: block-hardcoded-matrix-ids
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w|1nnSY-J3n6DtVvKqyC40zpEt1sROtHkIEqmSwG-5d9dU)
  # TRK-HOOK-203 (2026-07-30, ronin): the `exclude:` key was DEAD — zero implementations
  # across rule_engine.py, config_loader.py, enforce.sh and all four dispatchers. Every
  # exclusion below was therefore inert: this rule has been blocking .md/.html docs,
  # templates, discoveries and /inbox/ the whole time its author believed they were exempt.
  # PROVEN, not argued: the Edit that first tried to write this very comment was DENIED by
  # this rule, because a rule file that detects an ID must contain that ID, and the `.md`
  # exemption meant to permit it was inert. The repair was blocked by the defect it repairs.
  #
  # Re-expressed as ONE negative-lookahead file_path condition rather than a chain of
  # not_contains, deliberately: the extension exclusions are ANCHORED (`$`). As
  # not_contains they would lose the anchor and exempt any path merely CONTAINING ".md"
  # — e.g. `docs/my.md.backup.ts` — which widens what the rule PERMITS. The lookahead
  # preserves the original semantics exactly.
  - field: file_path
    operator: regex_match
    pattern: \A(?!.*(?:docs/templates/|docs/discoveries/|/inbox/))(?!.*\.(?:md|html|txt|json|yaml|yml|csv|jsonl)$).*
owner: megazord
---

**BLOCKED: Hardcoded MATRIX Spreadsheet ID**

A literal MATRIX spreadsheet ID was found in source code. Never hardcode MATRIX IDs — use `RAPID_CORE.getMATRIX_ID()` or environment variables.

**Why this matters:**
MATRIX spreadsheet IDs are the load-bearing handles for RPI's data engines (RAPID_MATRIX, PRODASH_MATRIX, SENTINEL_MATRIX, etc.). Hardcoding them in source bypasses the registry pattern, breaks environment-isolated runs, and makes future MATRIX migration painful (rename → grep → replace, everywhere).

**Fix:**
- GAS code: `const sheet = RAPID_CORE.getMATRIX_ID('PRODASH_MATRIX')`
- Cloud Run / Node: read from env var seeded by Secret Manager / GCP config
- Tests: use a mocked or fixture ID, not the production value

**Scope of this rule (v2 — 2026-04-29 narrowing):**
- Pattern matches ONLY the *known production MATRIX spreadsheet IDs* (whitelist). Drive Doc / Slide / Folder / Sheet IDs in the wild (43-char Drive resource ID shape) are NOT caught — false-positive trap of the v1 broad regex eliminated.
- Doc / scope / config files (`.md`, `.html`, `.txt`, `.json`, `.yaml`, `.yml`, `.csv`, `.jsonl`) are excluded — legitimate places to reference any Drive ID by value (e.g. ATLAS scriptId in CLAUDE.md, Doug Schroeder Statements OCR Doc ID in follow-up Discovery Doc).
- `docs/templates/`, `docs/discoveries/`, and `/inbox/` paths excluded so authoring artifacts can cite IDs without rewriting around them.

**Adding a new MATRIX:**
When a new MATRIX spreadsheet is created (rare — happens at most quarterly), append its ID to the regex alternation in this rule. Coordinate with MEGAZORD (registry stewardship).
