---
name: block-seed-without-snapshot
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: npx tsx.*(?:seed-|migrate-|backfill-)
exclude:
  - pattern: --snapshot
  - pattern: --dry-run
---

**BLOCKED: Seed/Migration Script Without Safety Flag**

You are running a seed or migration script without the required safety flags.

**Why this is blocked:**
- Seed and migration scripts perform bulk writes that can corrupt production data
- A pre-run snapshot ensures rollback capability if something goes wrong
- Dry-run previews catch issues before they hit real data

**Fix:**
1. First, run with `--dry-run` to preview changes:
   ```bash
   npx tsx scripts/seed-example.ts --dry-run
   ```
2. Then, run with `--snapshot` to create a backup before executing:
   ```bash
   npx tsx scripts/seed-example.ts --snapshot
   ```

**Required flags (at least one):**
- `--dry-run` — Preview changes without writing
- `--snapshot` — Create a Firestore backup before executing

See: GUARDIAN sprint data protection protocols
