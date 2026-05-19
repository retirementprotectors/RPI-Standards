---
name: gate-data-migration
enabled: true
event: PreToolUse
action: block
conditions:
  - field: tool
    operator: equals
    value: Edit
  - field: content
    operator: regex_match
    pattern: FieldValue\.delete\(\)|deleteField\(\)|\.delete\(\).*field|remove.*field
owner: megazord
---

**BLOCKED: Data Migration Gate — MEGAZORD Protocol Required**

You are writing code that deletes a Firestore field. This triggers the Data Migration Protocol.

**YOU CANNOT DELETE, RENAME, OR RESTRUCTURE FIRESTORE FIELDS WITHOUT COMPLETING ALL 7 STAGES:**

**Stage 1 — INVENTORY**
- grep the ENTIRE codebase (apps/, packages/, services/) for the field name
- Count every reference: UI queries, API routes, normalizers, types, schemas, seed scripts
- Check Firestore indexes that reference the field (`firebase.json` + console)
- Check collectionGroup queries that orderBy/where on the field

**Stage 2 — IMPACT REPORT**
- List every file that will break if this field disappears
- Identify every `orderBy()`, `where()`, and display reference
- Identify Firestore indexes that need recreation
- Build an HTML or table showing the full blast radius
- **JDM GATE: JDM must review and approve the impact report**

**Stage 3 — CODE FIRST**
- Update ALL code references to support BOTH old and new field names
- Example: `data.carrier || data.carrier_name` (reads both)
- Update TypeScript interfaces to include the new field
- Deploy the code change to production
- Verify it's live and working

**Stage 4 — DRY RUN**
- Run the data migration in READ-ONLY mode
- Show before/after for a sample of records
- Count total documents affected
- **JDM GATE: JDM must approve the dry run results**

**Stage 5 — EXECUTE**
- Run the migration (SET new field, then DELETE old field in same atomic write)
- Batch commits (450 per batch max)
- Log results: updated, skipped, errors

**Stage 6 — VERIFY**
- Hit every affected page/endpoint
- Confirm data renders correctly
- Check Firestore indexes are serving queries
- Screenshot or API response proof

**Stage 7 — CLEANUP**
- Remove support for old field name from code (the `|| data.old_name` fallbacks)
- Delete old Firestore indexes
- Update TypeScript types (remove old field)
- Deploy final cleanup

**Stage 8 — COMMUNICATE + MONITOR**
- Draft a team message: what changed, why, what they should see differently
- **JDM GATE: JDM must approve the message before it goes to the team**
- Send to appropriate channel (Slack, email, or team call depending on impact)
- Monitor window: team reports any issues for 3-5 business days
- Migration is NOT complete until monitor window passes clean

**Lesson learned:** On 2026-04-08, MEGAZORD skipped stages 1-3, migrated carrier_name → carrier in Firestore before updating 249 code references across 52 files. Production accounts page broke — showed 35 records instead of 12,000+. Firestore index for the new field didn't exist. Three separate production incidents from one migration.

**If you are JDM, MEGAZORD, or SHINOB1:** Acknowledge and confirm you are following the 8-stage protocol. Then proceed.
