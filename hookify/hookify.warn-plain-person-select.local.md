---
name: warn-plain-person-select
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(html)$
  - field: content
    operator: regex_match
    pattern: <select[^>]*id="[^"]*(agent|owner|producer|user|assigned|manager|leader|client)[^"]*"
---

**WARNING: Possible Plain Dropdown for Person Selection**

You are writing a `<select>` element with an ID that suggests person selection (agent, owner, producer, user, assigned, manager, leader, client).

**RPI Standard:** Person-selection fields that reference known entities MUST use the Smart Lookup type-ahead component, not plain `<select>` dropdowns.

**Exceptions (where plain select/text IS correct):**
- Self-identification (user entering their own name)
- External contacts not in any RPI database
- Multi-select assignment (use checkbox checklists)
- Non-person selects that happen to contain these keywords

**If this IS a person-selection field:**
Replace with `buildSmartLookup()` — see `_RPI_STANDARDS/reference/patterns/SMART_LOOKUP.md`

**If this is NOT a person field:** Ignore this warning and proceed.
