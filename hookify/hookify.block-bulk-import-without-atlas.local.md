---
name: block-bulk-import-without-atlas
enabled: true
event: prompt
action: block
conditions:
  - field: prompt
    operator: regex_match
    pattern: (?:import|bulk|batch).*(?:data|write|update|firestore|migration)|(?:migrate|seed).*(?:firestore|collection)
exclude:
  - pattern: atlas|ATLAS|guardian|snapshot
---

**BLOCKED: Data Import/Migration Without ATLAS Consultation**

A bulk data import or migration was detected without referencing ATLAS or GUARDIAN safeguards.

**Why this is blocked:**
- ATLAS is the source of truth for all data sources, pipelines, and tools
- Bulk writes without pre-run snapshots risk irreversible data corruption
- Existing tools and pipelines may already handle this use case

**MANDATORY steps before any bulk data work:**

1. **Consult ATLAS registry** — Query `tool_registry` in Firestore to check what intake/processing tools already exist. Do NOT build new import scripts when registered tools exist.

2. **Run guardian-snapshot.ts** BEFORE any bulk write — Creates a point-in-time backup of affected collections for rollback capability.

3. **Use --dry-run first** — Preview all changes before executing. Verify counts, field mappings, and target collections match expectations.

4. **Reference _SOURCE_REGISTRY** — Check if this data source is already cataloged. If not, flag for JDM before proceeding.

**To proceed, include one of these in your prompt:**
- "ATLAS" or "atlas" — confirms registry was consulted
- "guardian" — confirms GUARDIAN protections are in place
- "snapshot" — confirms backup strategy is planned

See: `hookify.intent-atlas-consult.local.md` for full ATLAS consultation protocol
